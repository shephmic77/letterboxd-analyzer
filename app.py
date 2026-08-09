import zipfile
import io
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Optional: prediction section (won't break app if sklearn isn't installed)
try:
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.linear_model import Ridge
    SKLEARN_OK = True
except Exception:
    SKLEARN_OK = False


# ------------------------------------------------
# PAGE SETUP
# ------------------------------------------------
st.set_page_config(page_title="Letterboxd Taste Analyzer", layout="wide")
st.title("Letterboxd Taste Analyzer")
st.caption("Unrated watched films are included in viewing totals but excluded from rating-based analysis.")

uploaded = st.file_uploader("Upload Letterboxd ZIP export (recommended)", type=["zip"])


# ------------------------------------------------
# HELPERS
# ------------------------------------------------
def show_fig(fig):
    fig.tight_layout()
    st.pyplot(fig, width="stretch")


def set_rating_axis(ax, label="Rating"):
    ax.set_ylim(0.5, 5)
    ax.set_ylabel(label)
    ax.set_yticks(np.arange(0.5, 5.5, 0.5))


def date_axis_format(ax, dates):
    if len(dates) == 0:
        return

    dmin = pd.to_datetime(dates.min())
    dmax = pd.to_datetime(dates.max())
    if pd.isna(dmin) or pd.isna(dmax):
        return

    span = (dmax - dmin).days

    if span <= 365:
        locator = mdates.MonthLocator(interval=1)
        fmt = mdates.DateFormatter("%Y-%m")
    elif span <= 3 * 365:
        locator = mdates.MonthLocator(interval=3)
        fmt = mdates.DateFormatter("%Y-%m")
    else:
        locator = mdates.MonthLocator(interval=6)
        fmt = mdates.DateFormatter("%Y-%m")

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)

    for lbl in ax.get_xticklabels():
        lbl.set_rotation(25)
        lbl.set_ha("right")


def ensure_months(pivot):
    for m in range(1, 13):
        if m not in pivot.columns:
            pivot[m] = 0
    return pivot[sorted(pivot.columns)]


def month_labels():
    return [pd.to_datetime(m, format="%m").strftime("%b") for m in range(1, 13)]


def safe_read_csv(z, filename):
    with z.open(filename) as f:
        return pd.read_csv(f)


def add_table_header(text):
    st.markdown(f"**Data used:** {text}")


# ------------------------------------------------
# STOP IF NO FILE
# ------------------------------------------------
if uploaded is None:
    st.info("Upload your Letterboxd ZIP export to begin.")
    st.stop()


# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
with zipfile.ZipFile(io.BytesIO(uploaded.getvalue())) as z:
    names = set(z.namelist())

    if "ratings.csv" not in names:
        st.error("Your ZIP is missing ratings.csv")
        st.stop()

    if "diary.csv" not in names:
        st.error("Your ZIP is missing diary.csv (needed for watch-date charts).")
        st.stop()

    ratings = safe_read_csv(z, "ratings.csv")
    diary = safe_read_csv(z, "diary.csv")

    watched = None
    if "watched.csv" in names:
        watched = safe_read_csv(z, "watched.csv")


# ------------------------------------------------
# CLEAN RATINGS
# ------------------------------------------------
ratings["Date"] = pd.to_datetime(ratings["Date"], errors="coerce")
ratings["Year"] = pd.to_numeric(ratings["Year"], errors="coerce")
ratings["Rating"] = pd.to_numeric(ratings["Rating"], errors="coerce")

ratings = ratings.dropna(subset=["Date", "Name", "Year", "Letterboxd URI"])
ratings["Rating"] = ratings["Rating"].clip(0, 5)


# ------------------------------------------------
# CLEAN DIARY (REAL WATCH DATE)
# ------------------------------------------------
watch_col = "Watched Date" if "Watched Date" in diary.columns else "Date"

diary["watch_date"] = pd.to_datetime(diary[watch_col], errors="coerce")
diary["Year"] = pd.to_numeric(diary["Year"], errors="coerce")

if "Rating" in diary.columns:
    diary["Rating"] = pd.to_numeric(diary["Rating"], errors="coerce")
else:
    diary["Rating"] = np.nan

diary = diary.dropna(subset=["watch_date", "Name", "Year", "Letterboxd URI"])


# ------------------------------------------------
# MERGE RATINGS INTO DIARY WATCHES
# (All charts below use DIARY watch dates, unless stated)
# ------------------------------------------------
rating_map = ratings.set_index("Letterboxd URI")["Rating"]

diary["Rating"] = diary["Rating"].where(
    ~diary["Rating"].isna(),
    diary["Letterboxd URI"].map(rating_map)
)

# Keep unrated watches as NaN so they are excluded from rating-based analysis
diary["Rating"] = diary["Rating"].clip(0, 5)

df = diary.sort_values("watch_date").reset_index(drop=True)

# FEATURES
df["watch_year"] = df["watch_date"].dt.year
df["watch_month"] = df["watch_date"].dt.month
df["watch_dow_num"] = df["watch_date"].dt.dayofweek
df["watch_dow_name"] = df["watch_date"].dt.day_name()
df["movie_decade"] = (df["Year"] // 10) * 10
df["movie_age_at_watch"] = df["watch_year"] - df["Year"]
df["days_since_prev_watch"] = df["watch_date"].diff().dt.days
df["days_since_prev_watch"] = df["days_since_prev_watch"].fillna(df["days_since_prev_watch"].median())


# ------------------------------------------------
# WATCHED TOTAL (TOP METRIC ONLY)
# - Use watched.csv if present (your 711)
# - Else fallback to unique diary films
# ------------------------------------------------
if watched is not None:
    if "Letterboxd URI" in watched.columns:
        watched_total = int(watched["Letterboxd URI"].dropna().nunique())
    else:
        watched_total = int(len(watched))
else:
    watched_total = int(df["Letterboxd URI"].dropna().nunique())

diary_total = int(len(diary))


# ------------------------------------------------
# METRICS
# ------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Watched Films (All) — from watched.csv if present", f"{watched_total:,}")
c2.metric("Diary / Journal Entries — from diary.csv", f"{diary_total:,}")
c3.metric("Average Rating — from diary.csv (+ ratings.csv fill)", f"{df['Rating'].mean():.2f}")
c4.metric("Median Rating — from diary.csv (+ ratings.csv fill)", f"{df['Rating'].median():.1f}")

st.divider()


# ------------------------------------------------
# RATING DISTRIBUTION (CENTERED BARS)
# ------------------------------------------------
st.subheader("Rating Distribution (rated diary entries only)")
add_table_header("Bars use rated diary entries only. Rating is diary Rating if present, otherwise ratings.csv; unrated films are excluded.")

rating_counts = (
    df["Rating"]
    .round(1)
    .value_counts()
    .sort_index()
)

all_ratings = np.arange(0.5, 5.5, 0.5)
rating_counts = rating_counts.reindex(all_ratings, fill_value=0)

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(rating_counts.index, rating_counts.values, width=0.4, align="center")
ax.set_xticks(all_ratings)
ax.set_xlabel("Rating (0.5–5)")
ax.set_ylabel("Count")
ax.set_title("How You Rate Films")
show_fig(fig)

st.dataframe(
    pd.DataFrame({"Rating": rating_counts.index, "Count": rating_counts.values}),
    width="stretch",
    height=260
)

st.divider()


# ------------------------------------------------
# ROLLING AVERAGE
# ------------------------------------------------
st.subheader("Rolling Rating Average (rated films only)")
add_table_header("Line uses watch_date from diary.csv. Unrated films are excluded from the rolling rating calculation.")

window = st.slider("Rolling Window (films)", 5, 50, 20, 5)
rated_df = df.dropna(subset=["Rating"]).copy()
rated_df["rolling"] = rated_df["Rating"].rolling(window, min_periods=max(5, window // 4)).mean()

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(rated_df["watch_date"], rated_df["rolling"], linewidth=2)
ax2.set_xlabel("Date")
ax2.set_title("Rolling Average Rating")
set_rating_axis(ax2, label="Rolling avg rating")
date_axis_format(ax2, rated_df["watch_date"])
show_fig(fig2)

rolling_table = rated_df[["watch_date", "Rating", "rolling"]].copy()
rolling_table = rolling_table.rename(columns={"watch_date": "Date"})
st.dataframe(rolling_table.tail(40), width="stretch", height=260)

st.divider()


# ------------------------------------------------
# MONTHLY WATCH VOLUME (DIARY WATCH DATES)
# ------------------------------------------------
st.subheader("Watch Volume by Month (source: diary.csv watch dates)")
add_table_header("Counts are number of diary.csv watch entries per month (by watch_date).")

monthly = df.set_index("watch_date").resample("MS").size().reset_index(name="count")
monthly = monthly.rename(columns={"watch_date": "Month"})

start = monthly["Month"].min()
end = monthly["Month"].max()
full = pd.date_range(start=start, end=end, freq="MS")

monthly = (
    monthly.set_index("Month")
    .reindex(full, fill_value=0)
    .rename_axis("Month")
    .reset_index()
)

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.bar(monthly["Month"], monthly["count"], width=25)
ax3.set_xlabel("Month")
ax3.set_ylabel("Films Watched")
ax3.set_title("Films Watched per Month (Diary)")
date_axis_format(ax3, monthly["Month"])
show_fig(fig3)

st.dataframe(monthly.rename(columns={"count": "Watched (Diary)"}), width="stretch", height=260)

st.divider()


# ------------------------------------------------
# DECADE ANALYSIS (DIARY WATCHES)
# ------------------------------------------------
st.subheader("Decade Taste (source: diary.csv watch entries; release decade from Year)")
add_table_header("Volume = all diary.csv entries grouped by release decade. Avg rating excludes unrated films.")

decade = (
    df.groupby("movie_decade")
    .agg(avg_rating=("Rating", "mean"), count=("Rating", "size"))
    .reset_index()
    .sort_values("movie_decade")
)

colA, colB = st.columns(2)

with colA:
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    ax4.bar(decade["movie_decade"].astype(int).astype(str), decade["count"])
    ax4.set_title("Watch Volume by Release Decade (Diary)")
    ax4.set_xlabel("Decade")
    ax4.set_ylabel("Films")
    show_fig(fig4)

with colB:
    fig5, ax5 = plt.subplots(figsize=(7, 4))
    ax5.plot(decade["movie_decade"], decade["avg_rating"], marker="o", linewidth=2)
    ax5.set_title("Average Rating by Release Decade (Diary)")
    ax5.set_xlabel("Decade")
    set_rating_axis(ax5, label="Average rating")
    show_fig(fig5)

st.dataframe(
    decade.rename(columns={"movie_decade": "Release decade", "count": "Watched (Diary)", "avg_rating": "Avg rating"}),
    width="stretch",
    height=260
)

st.divider()


# ------------------------------------------------
# HEATMAP (DIARY WATCH DATES) + LEGEND + NUMBERS
# ------------------------------------------------
st.subheader("Watch Volume Heatmap (Year × Month) — source: diary.csv watch dates")
add_table_header("Each cell = count of diary.csv watch entries in that year-month (by watch_date).")

heat = df.copy()
heat["year"] = heat["watch_date"].dt.year
heat["month"] = heat["watch_date"].dt.month

pivot = heat.pivot_table(index="year", columns="month", values="watch_date", aggfunc="size", fill_value=0)
pivot = ensure_months(pivot)

fig6, ax6 = plt.subplots(figsize=(10, 4.5))
im = ax6.imshow(pivot.values, aspect="auto")

ax6.set_xticks(np.arange(12))
ax6.set_xticklabels(month_labels())
ax6.set_yticks(np.arange(len(pivot.index)))
ax6.set_yticklabels(pivot.index.astype(int))

ax6.set_title("Films Watched per Month (Heatmap, Diary)")
ax6.set_xlabel("Month")
ax6.set_ylabel("Year")

cbar = fig6.colorbar(im, ax=ax6)
cbar.set_label("Films watched (count)")

for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        ax6.text(j, i, int(pivot.values[i, j]), ha="center", va="center")

show_fig(fig6)

pivot_table = pivot.copy()
pivot_table.columns = [pd.to_datetime(m, format="%m").strftime("%b") for m in pivot_table.columns]
pivot_table = pivot_table.reset_index().rename(columns={"year": "Year"})
st.dataframe(pivot_table, width="stretch", height=320)

st.divider()


# ------------------------------------------------
# MORE VISUALS (DIARY WATCH DATES)
# ------------------------------------------------
st.subheader("More Visuals (source: diary.csv watch dates; unrated films excluded from rating averages)")

col1, col2 = st.columns(2)

# Rating by day-of-week
with col1:
    dow = (
        df.groupby("watch_dow_name")
        .agg(avg_rating=("Rating", "mean"), count=("Rating", "size"))
        .reset_index()
    )
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow["watch_dow_name"] = pd.Categorical(dow["watch_dow_name"], categories=order, ordered=True)
    dow = dow.sort_values("watch_dow_name")

    fig7, ax7 = plt.subplots(figsize=(7, 4))
    ax7.plot(dow["watch_dow_name"], dow["avg_rating"], marker="o", linewidth=2)
    ax7.set_title("Average Rating by Day of Week (Diary)")
    ax7.set_xlabel("Day")
    set_rating_axis(ax7, label="Average rating")
    show_fig(fig7)

    st.dataframe(dow.rename(columns={"watch_dow_name": "Day", "count": "Watched (Diary)", "avg_rating": "Avg rating"}), width="stretch", height=260)

# Volume by day-of-week
with col2:
    fig8, ax8 = plt.subplots(figsize=(7, 4))
    ax8.bar(dow["watch_dow_name"], dow["count"])
    ax8.set_title("Watch Volume by Day of Week (Diary)")
    ax8.set_xlabel("Day")
    ax8.set_ylabel("Films")
    show_fig(fig8)

# Rating vs movie age (binned)
st.subheader("Rating vs Movie Age at Watch (source: diary.csv watch entries)")
add_table_header("Age = (watch year - release year). Line shows binned average rating; points are raw.")

age = df[["movie_age_at_watch", "Rating"]].dropna().copy()
age = age[(age["movie_age_at_watch"] >= -2) & (age["movie_age_at_watch"] <= 120)]

# Bin ages (auto-ish)
bins = [-2, 0, 1, 2, 3, 5, 10, 20, 30, 40, 60, 120]
labels = ["<=0", "1", "2", "3", "4-5", "6-10", "11-20", "21-30", "31-40", "41-60", "61+"]
age["age_bin"] = pd.cut(age["movie_age_at_watch"], bins=bins, labels=labels, include_lowest=True)

age_bin = age.groupby("age_bin", observed=False).agg(avg_rating=("Rating", "mean"), count=("Rating", "size")).reset_index()

fig9, ax9 = plt.subplots(figsize=(9, 4))
ax9.scatter(age["movie_age_at_watch"], age["Rating"], alpha=0.25)
ax9.plot(np.arange(len(age_bin)), age_bin["avg_rating"], marker="o", linewidth=2)
ax9.set_title("Ratings vs Movie Age at Watch")
ax9.set_xlabel("Movie age at watch (years) — points; binned avg shown as line")
set_rating_axis(ax9, label="Rating")
show_fig(fig9)

st.dataframe(age_bin.rename(columns={"age_bin": "Age bucket", "count": "Films", "avg_rating": "Avg rating"}), width="stretch", height=260)

st.divider()


# ------------------------------------------------
# PREDICTION (Simple, resume-friendly)
# ------------------------------------------------
st.subheader("Predicting Your Rating (simple predictors; source: diary.csv watch entries)")

if not SKLEARN_OK:
    st.warning("Prediction section requires scikit-learn. Install it in your venv: pip install scikit-learn")
else:
    add_table_header(
        "Model trains on diary.csv entries with features derived from watch_date + release Year. "
        "Target = Rating (diary rating -> ratings.csv); unrated films are excluded from model training."
    )

    # Build modeling frame
    model_df = df.copy()

    # Keep rows with core fields
    model_df = model_df.dropna(subset=["watch_date", "Year", "Rating"])

    # Features (simple + explainable)
    model_df["watch_month"] = model_df["watch_date"].dt.month.astype(int)
    model_df["watch_dow"] = model_df["watch_date"].dt.dayofweek.astype(int)
    model_df["release_year"] = model_df["Year"].astype(int)
    model_df["movie_age"] = (model_df["watch_date"].dt.year.astype(int) - model_df["release_year"]).astype(int)

    # Clip extreme movie_age to avoid weird outliers dominating (still represents data)
    model_df["movie_age"] = model_df["movie_age"].clip(lower=-2, upper=120)

    # Days since previous watch (behavior feature)
    model_df["days_since_prev_watch"] = model_df["days_since_prev_watch"].fillna(model_df["days_since_prev_watch"].median())
    model_df["days_since_prev_watch"] = model_df["days_since_prev_watch"].clip(lower=0, upper=365)

    X = model_df[["watch_month", "watch_dow", "release_year", "movie_age", "days_since_prev_watch"]]
    y = model_df["Rating"].astype(float)

    # Train/test split
    test_size = st.slider("Test size", 0.1, 0.4, 0.2, 0.05)
    random_state = st.number_input("Random seed", min_value=0, max_value=9999, value=42, step=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=float(test_size), random_state=int(random_state)
    )

    # Simple model: Ridge regression (fast, interpretable)
    model = Pipeline(steps=[
        ("model", Ridge(alpha=1.0))
    ])

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # Clip predictions to valid rating scale for display
    preds_clip = np.clip(preds, 0.5, 5)

    mae = mean_absolute_error(y_test, preds_clip)
    rmse = np.sqrt(mean_squared_error(y_test, preds_clip))
    r2 = r2_score(y_test, preds_clip)

    m1, m2, m3 = st.columns(3)
    m1.metric("MAE", f"{mae:.3f}")
    m2.metric("RMSE", f"{rmse:.3f}")
    m3.metric("R²", f"{r2:.3f}")

    # Predicted vs actual plot
    fig10, ax10 = plt.subplots(figsize=(7, 5))
    ax10.scatter(y_test, preds_clip, alpha=0.5)
    ax10.plot([0.5, 5], [0.5, 5], linewidth=2)
    ax10.set_title("Predicted vs Actual Rating (test set)")
    ax10.set_xlabel("Actual rating")
    ax10.set_ylabel("Predicted rating")
    ax10.set_xlim(0.5, 5)
    ax10.set_ylim(0.5, 5)
    show_fig(fig10)

    # Show prediction table
    pred_table = X_test.copy()
    pred_table["actual_rating"] = y_test.values
    pred_table["pred_rating"] = preds_clip
    pred_table = pred_table.sort_values("actual_rating", ascending=False).head(40)
    st.dataframe(pred_table, width="stretch", height=320)

    # Coefficients (interpretability)
    coef = model.named_steps["model"].coef_
    coef_table = pd.DataFrame({
        "feature": X.columns,
        "coefficient": coef
    }).sort_values("coefficient", ascending=False)

    st.markdown("**Model coefficients (Ridge):** higher coefficient → tends to increase predicted rating (all else equal).")
    st.dataframe(coef_table, width="stretch", height=260)

    st.markdown(
        "**Next upgrade (recommended):** add genre / director / cast features by scraping public metadata (TMDB/OMDb) or Letterboxd pages, "
        "then train a better model. That’s where prediction becomes meaningfully strong for a resume project."
    )

    # Run with: py -m streamlit run app.py
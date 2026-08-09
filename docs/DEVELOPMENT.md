# Development History

This document records the development of the Letterboxd Taste Analyzer, including the original implementation, problems identified during review, and improvements made afterward.

## Initial Idea

The project began as a way to analyze my personal Letterboxd viewing history using Python.

The original goal was to move beyond the basic statistics available on my Letterboxd profile and explore patterns in:

- Ratings
- Viewing frequency
- Release decades
- Viewing dates
- Changes in movie ratings over time

The project later developed into an interactive Streamlit application and included an exploratory machine learning component.

## Data Version 1

`data/v1/`

The first saved Letterboxd export represents an earlier stage of the project.

It was used while developing the initial data-loading, cleaning, and visualization workflow.

This version is retained rather than being replaced by newer data so that the repository preserves some of the original development material.

## Data Version 2

`data/v2/`

The second Letterboxd export contains additional viewing and rating activity.

This updated dataset was used while continuing development and testing of the application.

Keeping multiple exports helps document the data available at different stages of the project.

## Initial Application

The application developed into a Streamlit dashboard that accepts a Letterboxd ZIP export directly from the user.

The application reads Letterboxd files including:

- `ratings.csv`
- `diary.csv`
- `watched.csv`

The dashboard includes:

- Overall viewing statistics
- Rating distribution
- Rolling rating averages
- Monthly viewing activity
- Release-decade analysis
- Year-by-month viewing heatmap
- Day-of-week analysis
- Movie-age analysis
- Interactive Streamlit controls
- Ridge Regression rating prediction
- Model evaluation
- Model coefficient analysis

## Original Rating Methodology

The original version of the application treated watched movies without a recorded rating as a rating of `0`.

This kept unrated movies in the same dataframe as rated movies, but it created a methodological problem.

An unrated movie does not mean that the user gave the movie zero stars.

As a result, these artificial zero values could affect:

- Average rating
- Median rating
- Rating distribution
- Rolling rating averages
- Release-decade averages
- Day-of-week averages
- Movie-age analysis
- Machine learning training

This issue was preserved in the initial Git commit rather than rewriting the project's history.

## Rating Methodology Revision

A later revision corrected the unrated-film issue.

Unrated films now remain missing (`NaN`) rather than being converted to zero.

The application separates viewing activity from rating-based analysis.

Unrated films are still included in:

- Overall watched-film totals
- Diary-entry totals
- Monthly viewing activity
- Viewing heatmaps
- Release-decade viewing counts
- Day-of-week viewing counts

Unrated films are excluded from:

- Average rating
- Median rating
- Rating distribution
- Rolling rating averages
- Release-decade rating averages
- Day-of-week rating averages
- Movie-age rating analysis
- Machine learning training

This allows the application to count a movie as watched without assuming an opinion that the user never recorded.

## Rating Scale Revision

The original implementation allowed the rating scale to extend from `0` to `5`.

Because Letterboxd's recorded star ratings begin at `0.5`, the rating-based visualizations were updated to use a `0.5–5.0` scale.

Prediction outputs are also clipped to this valid rating range.

## Rolling Average Revision

The original rolling-average calculation operated on the full diary dataframe after missing ratings had been converted to zero.

After the rating methodology was corrected, a separate dataframe containing only rated films was created for the rolling calculation.

This means the rolling window now represents changes across actual ratings rather than being influenced by unrated watches.

## Machine Learning

A Ridge Regression model was added as an initial experiment in predicting personal movie ratings.

The current model uses:

- Watch month
- Watch day of week
- Release year
- Movie age at the time of viewing
- Days since the previous movie watched

The data is divided into training and testing sets.

The model is evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R²

The application also displays:

- Predicted vs. actual ratings
- Individual test predictions
- Ridge Regression coefficients

## Machine Learning Revision

The original model included unrated films because those observations had been converted to zero.

After correcting the rating methodology, unrated movies were removed from the modeling dataset.

The model now trains only on movies with actual recorded ratings.

During testing, the RMSE calculation also produced a compatibility error with the installed version of scikit-learn.

The original calculation used:

`mean_squared_error(..., squared=False)`

This was replaced with an explicit square-root calculation:

`np.sqrt(mean_squared_error(...))`

This produces RMSE without depending on the unsupported argument.

## Model Performance

The current model should be treated as an exploratory baseline rather than a finished prediction system.

During testing, the model produced approximately:

- MAE: 0.79
- RMSE: 0.97
- R²: -0.01

The negative R² indicates that the current features have very limited ability to explain personal movie ratings.

This result is useful because it identifies an important limitation of the current feature set.

Variables such as watch date and release year contain relatively little information about whether I will actually like a movie.

More relevant movie characteristics will likely be necessary for a stronger model.

## Compatibility and Maintenance

After testing the application with the current package environment, several deprecated or changing library behaviors were identified.

Streamlit's:

`use_container_width=True`

was replaced with:

`width="stretch"`

throughout the application.

The movie-age grouping operation was also updated to explicitly use:

`observed=False`

to preserve the existing pandas grouping behavior and remove a future compatibility warning.

These changes do not substantially alter the analysis but keep the application compatible with newer library versions.

## Current Project State

The current application:

- Accepts a Letterboxd ZIP export
- Cleans and combines viewing and rating information
- Separates unrated viewing activity from rated-film analysis
- Produces multiple exploratory visualizations
- Provides time-based viewing analysis
- Examines ratings by several derived features
- Includes an exploratory Ridge Regression model
- Reports model evaluation metrics
- Runs without the compatibility errors identified during testing

## Current Limitations

The largest limitation is the information available to the prediction model.

The current features are primarily based on viewing dates and movie release year rather than the actual characteristics of each movie.

The project currently does not include features such as:

- Genre
- Director
- Cast
- Runtime
- Language
- Country
- Production information

Because of this, the prediction model should not be interpreted as a strong recommendation system.

The application also depends on the current structure of Letterboxd's exported CSV files.

## Planned Development

Potential future development includes:

1. Add external movie metadata.
2. Analyze ratings by genre.
3. Analyze ratings by director.
4. Analyze ratings by actor or cast.
5. Add runtime and other movie characteristics.
6. Compare Ridge Regression with other machine learning models.
7. Improve feature engineering.
8. Evaluate whether richer features improve prediction performance.
9. Explore personalized movie recommendations.
10. Improve the Streamlit dashboard presentation.
11. Potentially deploy the application publicly.

## Repository Development

The Git history is intentionally used to document meaningful stages of the project.

Major stages currently include:

1. Initial Letterboxd Taste Analyzer.
2. Correction of unrated-film handling and rating methodology.
3. Rating-prediction compatibility fix.
4. Streamlit and pandas syntax updates.
5. README and project-documentation improvements.

The goal is not to make the repository appear as though the project was correct and polished from the beginning.

Instead, the repository preserves the process of identifying problems, testing the application, correcting methodology, maintaining compatibility, and improving documentation.
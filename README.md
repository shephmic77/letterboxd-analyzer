# Letterboxd Taste Analyzer

An interactive Streamlit application for analyzing personal Letterboxd viewing history, rating behavior, movie preferences, and viewing patterns.

The project takes a standard Letterboxd ZIP export and turns it into an interactive dashboard with exploratory data analysis, visualizations, and a simple machine learning model for predicting personal movie ratings.

## Project Overview

I built this project to explore my own Letterboxd history while practicing data cleaning, exploratory data analysis, visualization, interactive application development, and machine learning.

Instead of analyzing a fixed CSV file, the application allows a user to upload a Letterboxd ZIP export directly through the Streamlit interface.

The app reads data from files such as:

- `ratings.csv`
- `diary.csv`
- `watched.csv`

It then cleans and combines the data before generating the analysis.

Unrated films are preserved for viewing-volume analysis but excluded from calculations that require an actual rating.

## Features

### Viewing Summary

The dashboard displays:

- Total watched films
- Total diary entries
- Average rating
- Median rating

### Rating Distribution

Shows how frequently each Letterboxd rating from 0.5 to 5 stars appears in the user's rated viewing history.

Unrated films are excluded from the rating distribution.

### Rolling Rating Average

Tracks changes in average movie ratings over time using an adjustable rolling window.

Only films with recorded ratings are included in the rolling average.

### Monthly Viewing Activity

Shows the number of movies watched each month based on Letterboxd diary entries.

### Release Decade Analysis

Compares:

- Number of films watched from each release decade
- Average rating by release decade

All diary entries contribute to viewing-volume counts, while unrated films are excluded from average-rating calculations.

### Viewing Heatmap

Displays movie-watching activity by year and month.

### Day-of-Week Analysis

Examines:

- Average rating by day of the week
- Number of movies watched by day of the week

### Movie Age Analysis

Compares personal ratings with the age of a movie at the time it was watched.

Movie age is calculated as:

`watch year - release year`

The application groups movie ages into ranges and compares their average ratings.

### Rating Prediction

The project includes a Ridge Regression model that attempts to predict personal movie ratings using:

- Month watched
- Day of week watched
- Movie release year
- Movie age at time of viewing
- Days since the previous movie watched

Unrated films are excluded from model training.

The model uses a train/test split and reports:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R²

A predicted-vs-actual plot, prediction table, and model coefficients are also displayed.

## Technologies

- Python
- Streamlit
- pandas
- NumPy
- Matplotlib
- scikit-learn
- Git
- GitHub

## Project Structure

```text
Letterboxd/
├── data/
│   ├── v1/
│   └── v2/
├── docs/
│   └── DEVELOPMENT.md
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

The `data` directory contains Letterboxd exports from different stages of development. These are preserved to document how the project evolved.

The local Python virtual environment (`.venv`) is intentionally excluded from GitHub because it can be recreated using `requirements.txt`.

## Running the Project

Clone the repository and move into the project directory.

Create and activate a Python virtual environment if desired.

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

On Windows, the Python launcher can also be used:

```bash
py -m streamlit run app.py
```

Upload a Letterboxd ZIP export through the application to begin the analysis.

## Data

The project uses data exported directly from Letterboxd.

A Letterboxd export can contain viewing history, ratings, diary entries, watchlists, lists, and other account data.

This application primarily uses:

- `watched.csv` for overall watched-film totals when available
- `diary.csv` for watch dates and viewing activity
- `ratings.csv` to supplement rating information

Two exports are currently retained in this repository to document different stages of the project's development.

## Data Handling

A key distinction in the application is between **watching a movie** and **rating a movie**.

A movie can appear in a user's viewing history without having a Letterboxd rating.

The application therefore:

- Keeps unrated movies in viewing counts
- Keeps unrated movies in monthly activity
- Keeps unrated movies in heatmaps
- Keeps unrated movies in other viewing-volume calculations
- Excludes unrated movies from average and median ratings
- Excludes unrated movies from rating distributions
- Excludes unrated movies from rating-based trend calculations
- Excludes unrated movies from machine learning training

This prevents a missing rating from incorrectly being interpreted as a zero-star rating.

## Machine Learning

The prediction section is an exploratory machine learning component rather than a finished recommendation system.

The current model is Ridge Regression, which provides a simple and interpretable baseline.

The model currently relies mainly on temporal and release-year information. These features alone have limited ability to explain whether a person will actually like a movie.

The model is therefore useful for testing the prediction pipeline and evaluating which types of information are missing from the current dataset.

## Current Limitations

The prediction model currently has limited predictive power because its features are relatively simple.

Information likely to be more directly related to movie preference is not currently included, such as:

- Genre
- Director
- Cast
- Runtime
- Language
- Country
- Production information

The current Ridge Regression model should therefore be viewed as an initial machine learning experiment rather than a finished rating predictor or recommendation system.

The application also depends on the structure of Letterboxd's exported CSV files. Changes to the Letterboxd export format could require updates to the data-loading process.

## Future Improvements

Potential improvements include:

- Add genre information
- Add director and cast information
- Integrate external movie metadata
- Compare multiple machine learning models
- Perform feature engineering using movie characteristics
- Improve prediction performance
- Build a personalized movie recommendation system
- Add additional interactive Streamlit controls
- Improve dashboard presentation
- Deploy the application publicly

## Development History

This repository intentionally preserves meaningful stages of the project's development.

The initial version included a methodological issue where unrated films were treated as zero-star ratings. This affected rating averages, distributions, trends, and model training.

A later revision corrected this by separating unrated viewing activity from rated-film analysis.

Additional development included:

- Correcting the rating scale to Letterboxd's 0.5–5 star range
- Updating rolling-rating calculations
- Excluding unrated films from model training
- Fixing RMSE calculation compatibility
- Updating deprecated Streamlit syntax
- Updating pandas grouping behavior

Earlier data exports are also retained so that the repository documents how the project and dataset changed over time.

More detailed development notes are available in [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md).

## Purpose

This project was created as a personal data science project using my own Letterboxd data.

Its purpose is to demonstrate practical experience with:

- Data cleaning
- Data transformation
- Exploratory data analysis
- Data visualization
- Time-based analysis
- Feature engineering
- Machine learning
- Model evaluation
- Interactive application development
- Version control and project documentation

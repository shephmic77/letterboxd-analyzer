\# Letterboxd Taste Analyzer



A Streamlit application for analyzing personal Letterboxd viewing and rating data.



The project takes a standard Letterboxd ZIP export and turns it into an interactive dashboard for exploring viewing habits, rating behavior, movie preferences, and a simple machine learning model for predicting ratings.



\## Project Overview



I built this project to explore my own Letterboxd history while practicing data cleaning, exploratory data analysis, visualization, interactive application development, and machine learning.



Instead of analyzing a fixed CSV file, the application allows a user to upload a Letterboxd ZIP export directly into the Streamlit interface.



The app reads data from files such as:



\- `ratings.csv`

\- `diary.csv`

\- `watched.csv`



It then cleans and combines the data before generating the analysis.



\## Features



\### Viewing Summary



The dashboard displays:



\- Total watched films

\- Total diary entries

\- Average rating

\- Median rating



\### Rating Distribution



Shows how frequently each rating from 0 to 5 appears in the user's viewing history.



\### Rolling Rating Average



Tracks changes in average movie ratings over time using an adjustable rolling window.



\### Monthly Viewing Activity



Shows the number of movies watched each month.



\### Release Decade Analysis



Compares:



\- Number of films watched from each decade

\- Average rating by release decade



\### Viewing Heatmap



Displays movie-watching activity by year and month.



\### Day-of-Week Analysis



Examines both:



\- Average rating by day of the week

\- Number of movies watched by day of the week



\### Movie Age Analysis



Compares ratings with the age of a movie at the time it was watched.



\### Rating Prediction



The project also includes a simple Ridge Regression model that attempts to predict my movie rating using:



\- Month watched

\- Day of week watched

\- Movie release year

\- Movie age at time of viewing

\- Days since the previous movie watched



The model uses a train/test split and reports:



\- Mean Absolute Error (MAE)

\- Root Mean Squared Error (RMSE)

\- R²



A predicted-vs-actual plot and model coefficients are also displayed.



\## Technologies



\- Python

\- Streamlit

\- pandas

\- NumPy

\- Matplotlib

\- scikit-learn



\## Project Structure



```text

Letterboxd/

├── data/

│   ├── v1/

│   └── v\_2/

├── docs/

│   └── DEVELOPMENT.md

├── app.py

├── requirements.txt

├── README.md

└── .gitignore

## Running the Project

Clone the repository and move into the project directory.

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

Upload a Letterboxd ZIP export through the application to begin the analysis.



That description accurately reflects what your program currently does: it uploads the ZIP through Streamlit, reads and combines the Letterboxd files, and creates the different analyses. :contentReference\[oaicite:0]{index=0} :contentReference\[oaicite:1]{index=1}



The machine-learning section is also described accurately: five simple derived predictors feed a Ridge regression model with a train/test split and MAE, RMSE, and R² evaluation. :contentReference\[oaicite:2]{index=2}



I deliberately included the \*\*unrated = 0 limitation\*\* instead of hiding it. Your current code explicitly makes that assumption. :contentReference\[oaicite:3]{index=3} For a student portfolio, identifying a weakness in an earlier implementation and later fixing it is actually useful development history.



\## 2. Put this in `docs/DEVELOPMENT.md`



```markdown

\# Development History



This file documents the development of the Letterboxd Taste Analyzer and explains why earlier project data has been retained in the repository.



\## Initial Idea



The project began as a way to analyze my personal Letterboxd history using Python.



The original goal was to move beyond simply looking at my Letterboxd profile and instead explore patterns in:



\- Ratings

\- Viewing frequency

\- Release decades

\- Viewing dates

\- Changes in movie ratings over time



The project later expanded into an interactive Streamlit application and eventually included a basic machine learning component.



\## Data Version 1



`data/v1/`



The first saved Letterboxd export represents an earlier stage of the project.



It was used while developing the initial data-loading, cleaning, and visualization workflow.



This version is retained to show the original data available during development rather than replacing all earlier material with the newest export.



\## Data Version 2



`data/v\_2/`



The second Letterboxd export was created on February 28, 2026.



This updated dataset contains additional Letterboxd activity and was used while continuing development and testing of the application.



Keeping both exports makes it possible to see the data available at different stages of the project.



\## Application Development



The application developed into a Streamlit dashboard that accepts a Letterboxd ZIP export directly from the user.



The application currently includes:



\- Data loading directly from ZIP files

\- Data cleaning with pandas

\- Rating summaries

\- Rating distribution analysis

\- Rolling rating averages

\- Monthly viewing-volume analysis

\- Release-decade analysis

\- Year-by-month viewing heatmaps

\- Day-of-week analysis

\- Movie-age analysis

\- Interactive Streamlit controls

\- Ridge Regression rating prediction

\- Model evaluation and coefficient analysis



\## Machine Learning



A Ridge Regression model was added as an initial attempt to predict personal movie ratings.



The model currently uses features derived from the Letterboxd data itself:



\- Watch month

\- Watch day of week

\- Release year

\- Movie age when watched

\- Time since the previous movie was watched



This was intentionally kept relatively simple and interpretable.



The model serves primarily as an initial machine learning experiment rather than a finished recommendation system.



\## Known Methodology Issue



The current application converts watched movies without a recorded rating to a rating of `0`.



This allowed unrated movies to remain in the same dataframe as rated movies, but it introduces an important limitation.



An unrated movie does not necessarily represent a zero-star opinion.



As a result, these artificial zero values can influence:



\- Average rating

\- Median rating

\- Rolling averages

\- Decade rating averages

\- Day-of-week rating averages

\- Machine learning training



A future revision should preserve unrated films for viewing-volume analysis while excluding them from calculations that require an actual rating.



This issue is retained in the documented development history rather than being hidden because correcting it represents a meaningful methodological improvement to the project.



\## Planned Development



The next major development steps are:



1\. Separate rated and unrated movie analysis.

2\. Improve data validation.

3\. Add movie metadata such as genre and director.

4\. Evaluate stronger predictive models.

5\. Potentially create a recommendation system.

6\. Improve the Streamlit interface.

7\. Consider deploying the application publicly.



\## Repository Philosophy



This repository intentionally preserves meaningful stages of development.



Generated files such as the Python virtual environment are excluded because they do not represent original project work and can be recreated from `requirements.txt`.



Data snapshots, source code, documentation, and future revisions are retained when they help show how the project developed.


# ⚾ MLB History Data Pipeline & Dashboard

## Summary
This capstone project demonstrates a complete data pipeline. It uses Selenium to scrape historical Major League Baseball data, cleans and transforms the data using Pandas, stores in relational SQLite database, and visualizes the results using Streamlit dashboard.

## Setup Instructions
To run this project locally:
1. Clone this repository to your local machine.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the web scraper to generate the CSV files: `python scraper.py`
4. Build the local SQLite database: `python build_db.py`
5. (Optional) Run the command-line query tool: `python query_tool.py`
6. Launch the interactive dashboard: `streamlit run app.py`

## Dashboard Screenshot


![mlb dashboard](https://github.com/user-attachments/assets/89b888b1-2782-427d-8990-5f46a879122a)

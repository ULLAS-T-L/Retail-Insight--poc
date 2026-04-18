# Retail Insights GenAI POC

A FastAPI-based local proxy API to analyze retail KPIs using generated SQL queries against a local SQLite database.

## Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Initialize the database: `python src/data/init_db.py`
5. Run the server: `fastapi dev src/main.py`

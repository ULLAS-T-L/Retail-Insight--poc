import os

# SQLite DB Path
DB_PATH = os.environ.get("DB_PATH", "retail_data.db")

# Automatically strip protocol if formatted as a typical URL
if DB_PATH.startswith("sqlite:///"):
    DB_PATH = DB_PATH.replace("sqlite:///", "")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

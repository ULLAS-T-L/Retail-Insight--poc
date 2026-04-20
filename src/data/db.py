import sqlite3
from typing import Dict, Any, List
from config.settings import DB_PATH

class DatabaseWrapper:
    """
    Core database connection interface.
    TODO (Part 2): Abstract this to switch between SQLite locally and Snowflake/Postgres in prod.
    """
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        
    def execute_query(self, query: str, params: Any = ()) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

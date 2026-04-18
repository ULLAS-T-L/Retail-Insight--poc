import sqlite3
from typing import Dict, Any, List
from config.settings import DB_PATH

class DatabaseWrapper:
    """Wrapper to handle SQLite connection and configurations."""
    
    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        # Allows accessing columns by name
        conn.row_factory = sqlite3.Row
        return conn

class QueryRunner:
    """Runs parameterized queries securely against the database wrapper."""
    
    @staticmethod
    def run_query(sql_template: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        conn = DatabaseWrapper.get_connection()
        try:
            cursor = conn.cursor()
            # Execute query using the native safe param binding
            cursor.execute(sql_template, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

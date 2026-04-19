import sqlite3
from typing import List, Dict, Any
from config.settings import MEMORY_DB_PATH
import json

def _init_db():
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_query TEXT,
                agent_response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
_init_db()

def store_conversation(session_id: str, user_query: str, agent_response: Dict[str, Any]) -> None:
    """
    Stores linear conversational JSON events safely simulating localized chat history.
    """
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.execute(
            "INSERT INTO episodic_memory (session_id, user_query, agent_response) VALUES (?, ?, ?)",
            (session_id, user_query, json.dumps(agent_response))
        )

def get_recent_history(session_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieves the last N bounded chat queues exactly tracking parameters.
    """
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_query, agent_response FROM episodic_memory WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
            (session_id, limit)
        )
        rows = cursor.fetchall()
        # Return in chronological order smoothly
        history = []
        for row in reversed(rows):
            try:
                resp = json.loads(row["agent_response"])
            except:
                resp = row["agent_response"]
            history.append({
                "user_query": row["user_query"],
                "agent_response": resp
            })
        return history

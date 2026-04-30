import sqlite3
import json
from typing import List, Dict, Any, Optional
from config.settings import MEMORY_DB_PATH
from src.chat.chat_models import ChatMessage

def _init_chat_db():
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                raw_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES chat_sessions(session_id)
            )
        ''')
_init_chat_db()

def create_session_if_not_exists(session_id: str, user_id: str = "anonymous"):
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO chat_sessions (session_id, user_id) VALUES (?, ?)",
            (session_id, user_id)
        )

def save_message(session_id: str, role: str, message: str, raw_data: Optional[Dict[str, Any]] = None):
    raw_data_str = json.dumps(raw_data) if raw_data else None
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.execute(
            "INSERT INTO chat_messages (session_id, role, message, raw_data) VALUES (?, ?, ?, ?)",
            (session_id, role, message, raw_data_str)
        )

def get_chat_history(session_id: str) -> List[ChatMessage]:
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, message, timestamp, raw_data FROM chat_messages WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,)
        )
        rows = cursor.fetchall()
        
        return [
            ChatMessage(
                role=row["role"],
                message=row["message"],
                timestamp=row["timestamp"],
                raw_data=row["raw_data"]
            )
            for row in rows
        ]

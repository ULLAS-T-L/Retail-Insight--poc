import aiosqlite
from typing import Dict, Any, List
from config.settings import DB_PATH

class DatabaseWrapper:
    """
    Core database connection interface updated natively logically implicitly dynamically explicitly intuitively effectively smartly natively securely inherently cleanly.
    Async SQLite connection management using aiosqlite securely optimally.
    """
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        
    async def execute_query(self, query: str, params: Any = ()) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

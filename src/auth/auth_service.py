import sqlite3
import uuid
import hashlib
import os
from config.settings import MEMORY_DB_PATH
from src.auth.models import User

def _hash_password(password: str, salt: bytes = None) -> str:
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ":" + key.hex()

def _verify_password_hash(plain_password: str, hashed_string: str) -> bool:
    try:
        salt_hex, key_hex = hashed_string.split(":")
        salt = bytes.fromhex(salt_hex)
        key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        return new_key == key
    except Exception:
        return False

def _init_auth_db():
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                role TEXT NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 1
            )
        ''')
        # Auto-seed default users smoothly if table is completely empty
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            seed_users = [
                (str(uuid.uuid4()), "admin", _hash_password("admin123"), "admin", True),
                (str(uuid.uuid4()), "analyst", _hash_password("analyst123"), "analyst", True),
                (str(uuid.uuid4()), "viewer", _hash_password("viewer123"), "viewer", True)
            ]
            conn.executemany(
                "INSERT INTO users (user_id, username, hashed_password, role, is_active) VALUES (?, ?, ?, ?, ?)",
                seed_users
            )

_init_auth_db()

def get_user(username: str) -> User:
    with sqlite3.connect(MEMORY_DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return User(
                user_id=row["user_id"],
                username=row["username"],
                hashed_password=row["hashed_password"],
                role=row["role"],
                is_active=bool(row["is_active"])
            )
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _verify_password_hash(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return _hash_password(password)

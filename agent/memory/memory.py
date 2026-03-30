"""长期记忆: 跨 session 持久化用户偏好"""
import sqlite3
import json
from config.settings import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS preferences (key TEXT PRIMARY KEY, value TEXT)")
    conn.commit()
    conn.close()


def save_preference(key: str, value):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)",
        (key, json.dumps(value))
    )
    conn.commit()
    conn.close()


def load_preferences() -> dict:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT key, value FROM preferences").fetchall()
    conn.close()
    return {row[0]: json.loads(row[1]) for row in rows}


def clear_preferences():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM preferences")
    conn.commit()
    conn.close()

import sqlite3
from pathlib import Path
from datetime import datetime
from app.config import settings


DB_PATH = Path("data/conversations/chat_memory.db")


class MemoryStore:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                role TEXT,
                content TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def add_message(self, user_id: str, role: str, content: str):
        self.conn.execute(
            "INSERT INTO messages (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, role, content, datetime.utcnow().isoformat())
        )
        self.conn.commit()

    def get_recent_messages(self, user_id: str):
        cursor = self.conn.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, settings.memory_max_turns)
        )
        rows = cursor.fetchall()
        rows.reverse()  # oldest first
        return [{"role": r[0], "content": r[1]} for r in rows]
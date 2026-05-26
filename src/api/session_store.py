"""SQLite-backed store for per-session conversation histories."""

import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


class SessionStore:
    """SQLite-backed store for per-session conversation histories.

    Uses WAL mode + threading.Lock for safe concurrent writes.
    Reads are lock-free (WAL allows concurrent readers).
    """

    def __init__(self, db_path: str = "db/chat.db") -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._write_lock = threading.Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        """Open a WAL-mode connection to the shared SQLite file."""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self) -> None:
        """Create the sessions table if it does not exist."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    messages   TEXT NOT NULL DEFAULT '[]',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

    def get(self, session_id: str) -> List[Dict]:
        """Return the message list for session_id, or [] if not found."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT messages FROM sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        return json.loads(row[0]) if row else []

    def save(self, session_id: str, messages: List[Dict]) -> None:
        """Upsert the message list for session_id."""
        now = datetime.now(timezone.utc).isoformat()
        with self._write_lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO sessions (session_id, messages, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(session_id) DO UPDATE
                    SET messages = excluded.messages,
                        updated_at = excluded.updated_at
                    """,
                    (session_id, json.dumps(messages, ensure_ascii=False), now, now),
                )

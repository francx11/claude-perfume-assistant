"""SQLite-backed conversation logger shared with SessionStore."""

import logging
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


class ConversationLogger:
    """Logs chat turns (user + assistant) to SQLite.

    Shares db/chat.db with SessionStore — same file, separate table.
    threading.Lock guards writes; WAL mode allows concurrent reads.
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
        """Create the logs table and indexes if they do not exist."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp       TEXT NOT NULL,
                    conversation_id TEXT NOT NULL,
                    role            TEXT NOT NULL,
                    message         TEXT NOT NULL,
                    client_id       TEXT
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_conv ON logs(conversation_id)")
            # add column if missing (no-op on fresh DBs, migrates existing ones)
            try:
                conn.execute("ALTER TABLE logs ADD COLUMN client_id TEXT")
            except Exception:
                pass
            conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_client ON logs(client_id)")

    def list_sessions(self, client_id: str | None = None) -> list:
        """Return sessions ordered by most recent activity, optionally filtered by client."""
        with self._connect() as conn:
            if client_id:
                rows = conn.execute(
                    """
                    SELECT l.conversation_id,
                           MIN(CASE WHEN l.role = 'user' THEN l.message END) AS title,
                           MAX(l.timestamp) AS updated_at
                    FROM logs l
                    WHERE l.client_id = ?
                    GROUP BY l.conversation_id
                    ORDER BY updated_at DESC
                    """,
                    (client_id,),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT l.conversation_id,
                           MIN(CASE WHEN l.role = 'user' THEN l.message END) AS title,
                           MAX(l.timestamp) AS updated_at
                    FROM logs l
                    GROUP BY l.conversation_id
                    ORDER BY updated_at DESC
                    """
                ).fetchall()
        return [
            {
                "session_id": r[0],
                "title": (r[1] or r[0])[:60],
                "updated_at": r[2],
            }
            for r in rows
        ]

    def get_history(self, conversation_id: str) -> list:
        """Return all logged turns for a session in chronological order."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, message, timestamp FROM logs WHERE conversation_id = ? ORDER BY id ASC",
                (conversation_id,),
            ).fetchall()
        return [{"role": r[0], "message": r[1], "timestamp": r[2]} for r in rows]

    def log(self, conversation_id: str, role: str, message: str, client_id: str | None = None) -> None:
        """Append a single chat turn to the logs table."""
        sql = "INSERT INTO logs (timestamp, conversation_id, role, message, client_id) VALUES (?, ?, ?, ?, ?)"
        try:
            with self._write_lock:
                with self._connect() as conn:
                    conn.execute(
                        sql,
                        (datetime.now(timezone.utc).isoformat(), conversation_id, role, message, client_id),
                    )
        except Exception:
            logger.exception("Failed to write conversation log")

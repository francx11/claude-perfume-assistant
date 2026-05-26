"""Tests for SessionStore and ConversationLogger SQLite persistence."""

import threading

from src.api.conversation_logger import ConversationLogger
from src.api.session_store import SessionStore


class TestSessionStore:
    """Unit tests for SessionStore CRUD and concurrency."""

    def test_get_returns_empty_for_new_session(self, tmp_path):
        store = SessionStore(db_path=str(tmp_path / "chat.db"))
        assert store.get("abc-123") == []

    def test_save_and_get_roundtrip(self, tmp_path):
        store = SessionStore(db_path=str(tmp_path / "chat.db"))
        messages = [{"role": "user", "content": "hola"}, {"role": "assistant", "content": "hola back"}]
        store.save("session-1", messages)
        assert store.get("session-1") == messages

    def test_save_updates_existing_session(self, tmp_path):
        store = SessionStore(db_path=str(tmp_path / "chat.db"))
        store.save("s1", [{"role": "user", "content": "msg1"}])
        updated = [{"role": "user", "content": "msg1"}, {"role": "assistant", "content": "resp1"}]
        store.save("s1", updated)
        assert store.get("s1") == updated

    def test_sessions_are_isolated(self, tmp_path):
        store = SessionStore(db_path=str(tmp_path / "chat.db"))
        store.save("user-A", [{"role": "user", "content": "I like roses"}])
        store.save("user-B", [{"role": "user", "content": "I like oud"}])
        assert store.get("user-A")[0]["content"] == "I like roses"
        assert store.get("user-B")[0]["content"] == "I like oud"

    def test_persists_across_instances(self, tmp_path):
        db = str(tmp_path / "chat.db")
        SessionStore(db_path=db).save("s1", [{"role": "user", "content": "persisted"}])
        assert SessionStore(db_path=db).get("s1")[0]["content"] == "persisted"

    def test_concurrent_writes_no_data_loss(self, tmp_path):
        store = SessionStore(db_path=str(tmp_path / "chat.db"))
        errors = []

        def write(session_id: str):
            try:
                store.save(session_id, [{"role": "user", "content": session_id}])
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=write, args=(f"session-{i}",)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        for i in range(20):
            assert store.get(f"session-{i}") != []


class TestConversationLogger:
    """Unit tests for ConversationLogger SQLite logging and querying."""

    def test_log_writes_row(self, tmp_path):
        log = ConversationLogger(db_path=str(tmp_path / "chat.db"))
        log.log("s1", "user", "dame un perfume")
        import sqlite3

        with sqlite3.connect(str(tmp_path / "chat.db")) as conn:
            rows = conn.execute("SELECT role, message FROM logs WHERE conversation_id='s1'").fetchall()
        assert rows == [("user", "dame un perfume")]

    def test_log_multiple_turns(self, tmp_path):
        log = ConversationLogger(db_path=str(tmp_path / "chat.db"))
        log.log("s1", "user", "msg1")
        log.log("s1", "assistant", "resp1")
        import sqlite3

        with sqlite3.connect(str(tmp_path / "chat.db")) as conn:
            count = conn.execute("SELECT COUNT(*) FROM logs WHERE conversation_id='s1'").fetchone()[0]
        assert count == 2

    def test_log_does_not_raise_on_error(self, tmp_path, monkeypatch):
        log = ConversationLogger(db_path=str(tmp_path / "chat.db"))
        monkeypatch.setattr(log, "db_path", "/invalid/path/chat.db")
        log.log("s1", "user", "test")  # must not raise

import csv
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


class ConversationLogger:
    """Logs chat turns (user + assistant) to a CSV file."""

    FIELDNAMES = ["timestamp", "conversation_id", "role", "message"]

    def __init__(self, log_path: str = "logs/conversations.csv") -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_header()

    def _ensure_header(self) -> None:
        if not self.log_path.exists():
            with open(self.log_path, "w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=self.FIELDNAMES).writeheader()

    def log(self, conversation_id: str, role: str, message: str) -> None:
        try:
            with open(self.log_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writerow(
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "conversation_id": conversation_id,
                        "role": role,
                        "message": message,
                    }
                )
        except Exception:
            logger.exception("Failed to write conversation log")

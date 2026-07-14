from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path


_MAX_RECEIPTS = 5000


class ReceiptStateError(RuntimeError):
    pass


class MessageReceiptStore:
    """Persist Feishu event IDs so reconnects cannot submit the same turn twice."""

    def __init__(self, path: Path):
        self._path = path
        self._lock = threading.Lock()

    def claim(self, message_id: str) -> bool:
        with self._lock:
            receipts = self._load()
            if message_id in receipts:
                return False
            receipts[message_id] = self._now()
            if len(receipts) > _MAX_RECEIPTS:
                for old_id, _timestamp in sorted(
                    receipts.items(),
                    key=lambda item: (item[1], item[0]),
                )[: len(receipts) - _MAX_RECEIPTS]:
                    del receipts[old_id]
            self._save(receipts)
            return True

    def _load(self) -> dict[str, str]:
        if not self._path.is_file():
            return {}
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ReceiptStateError(f"Cannot read message receipts: {type(exc).__name__}") from exc
        if not isinstance(raw, dict) or raw.get("version") != 1:
            raise ReceiptStateError("Unsupported message receipt format")
        receipts = raw.get("receipts")
        if not isinstance(receipts, dict):
            raise ReceiptStateError("Message receipt state is missing receipts")
        return {str(key): str(value) for key, value in receipts.items()}

    def _save(self, receipts: dict[str, str]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._path.with_suffix(self._path.suffix + ".tmp")
        temporary.write_text(
            json.dumps({"version": 1, "receipts": receipts}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self._path)

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

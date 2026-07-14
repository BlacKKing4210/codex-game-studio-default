from __future__ import annotations

import hashlib
import json
import logging
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


LOG = logging.getLogger("feishu_gateway.delivery")
_MAX_DELIVERED_RECORDS = 1000


class DeliveryStateError(RuntimeError):
    pass


def split_text(text: str, max_chars: int) -> tuple[str, ...]:
    """Split text without losing content, leaving room for part labels."""
    value = text
    if len(value) <= max_chars:
        return (value,)

    body_limit = max(1, max_chars - 18)
    bodies: list[str] = []
    remaining = value
    while remaining:
        if len(remaining) <= body_limit:
            bodies.append(remaining)
            break
        split_at = remaining.rfind("\n", body_limit // 2, body_limit + 1)
        if split_at < 0:
            split_at = body_limit
            bodies.append(remaining[:split_at])
            remaining = remaining[split_at:]
        else:
            bodies.append(remaining[: split_at + 1])
            remaining = remaining[split_at + 1 :]

    total = len(bodies)
    return tuple(f"[{index}/{total}]\n{body}" for index, body in enumerate(bodies, start=1))


class DeliveryOutbox:
    """Durable ordered Feishu delivery with restart-safe, idempotent chunks."""

    def __init__(
        self,
        path: Path,
        max_chars: int,
        send_chunk: Callable[[str, str, str], bool],
        retry_seconds: int = 2,
    ):
        self._path = path
        self._max_chars = max_chars
        self._send_chunk = send_chunk
        self._retry_seconds = retry_seconds
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._worker = threading.Thread(target=self._run, name="feishu-delivery-outbox", daemon=True)

    def start(self) -> None:
        self._worker.start()

    def stop(self) -> None:
        self._stop.set()
        self._wake.set()
        if self._worker.is_alive():
            self._worker.join(timeout=5)

    def enqueue(self, chat_id: str, text: str, event_id: str) -> bool:
        chunks = split_text(text, self._max_chars)
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        total = len(chunks)
        parts = [
            {
                "text": chunk,
                "delivery_id": uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"feishu-outbox:v1:{event_id}:{content_hash}:{index}:{total}",
                ).hex,
                "delivered": False,
            }
            for index, chunk in enumerate(chunks, start=1)
        ]
        with self._lock:
            records = self._load()
            existing = records.get(event_id)
            if isinstance(existing, dict):
                if existing.get("chat_id") != chat_id or existing.get("content_hash") != content_hash:
                    raise DeliveryStateError(f"Outbox event content changed: {event_id}")
                self._wake.set()
                return True
            now = self._now()
            records[event_id] = {
                "event_id": event_id,
                "chat_id": chat_id,
                "content_hash": content_hash,
                "parts": parts,
                "created_at": now,
                "updated_at": now,
            }
            self._prune(records)
            self._save(records)
        self._wake.set()
        return True

    def drain_once(self) -> bool:
        with self._lock:
            records = self._load()
            selected = self._next_pending(records)
            if selected is None:
                return False
            event_id, chat_id, part = selected
            text = str(part["text"])
            delivery_id = str(part["delivery_id"])

        if not self._send_chunk(chat_id, text, delivery_id):
            return False

        with self._lock:
            records = self._load()
            record = records.get(event_id)
            if not isinstance(record, dict):
                return True
            raw_parts = record.get("parts")
            if not isinstance(raw_parts, list):
                raise DeliveryStateError(f"Invalid outbox parts: {event_id}")
            for raw_part in raw_parts:
                if isinstance(raw_part, dict) and raw_part.get("delivery_id") == delivery_id:
                    raw_part["delivered"] = True
                    break
            record["updated_at"] = self._now()
            self._prune(records)
            self._save(records)
        return True

    def pending_count(self) -> int:
        with self._lock:
            return sum(1 for record in self._load().values() if not self._is_delivered(record))

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                progressed = self.drain_once()
            except DeliveryStateError:
                LOG.exception("Delivery outbox is invalid; delivery paused")
                progressed = False
            if progressed:
                continue
            self._wake.wait(self._retry_seconds)
            self._wake.clear()

    def _load(self) -> dict[str, dict[str, object]]:
        if not self._path.is_file():
            return {}
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise DeliveryStateError(f"Cannot read delivery outbox: {type(exc).__name__}") from exc
        if not isinstance(raw, dict) or raw.get("version") != 1:
            raise DeliveryStateError("Unsupported delivery outbox format")
        records = raw.get("records")
        if not isinstance(records, dict):
            raise DeliveryStateError("Delivery outbox is missing records")
        return records

    def _save(self, records: dict[str, dict[str, object]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._path.with_suffix(self._path.suffix + ".tmp")
        temporary.write_text(
            json.dumps({"version": 1, "records": records}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self._path)

    @staticmethod
    def _next_pending(
        records: dict[str, dict[str, object]],
    ) -> tuple[str, str, dict[str, object]] | None:
        ordered = sorted(
            records.items(),
            key=lambda item: (str(item[1].get("created_at", "")), item[0]),
        )
        for event_id, record in ordered:
            parts = record.get("parts")
            if not isinstance(parts, list):
                raise DeliveryStateError(f"Invalid outbox parts: {event_id}")
            for part in parts:
                if isinstance(part, dict) and not bool(part.get("delivered")):
                    return event_id, str(record.get("chat_id", "")), part
        return None

    @staticmethod
    def _is_delivered(record: object) -> bool:
        if not isinstance(record, dict) or not isinstance(record.get("parts"), list):
            return False
        parts = record["parts"]
        return bool(parts) and all(isinstance(part, dict) and bool(part.get("delivered")) for part in parts)

    @classmethod
    def _prune(cls, records: dict[str, dict[str, object]]) -> None:
        delivered = sorted(
            (
                (event_id, record)
                for event_id, record in records.items()
                if cls._is_delivered(record)
            ),
            key=lambda item: (str(item[1].get("updated_at", "")), item[0]),
        )
        for event_id, _record in delivered[: max(0, len(delivered) - _MAX_DELIVERED_RECORDS)]:
            del records[event_id]

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

from __future__ import annotations

import json
import threading
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class ConversationBinding:
    key: str
    chat_id: str
    open_id: str
    project_alias: str
    generation: int
    thread_id: str | None
    updated_at: str


class ConversationStore:
    def __init__(self, path: Path):
        self._path = path
        self._lock = threading.Lock()

    @staticmethod
    def key(chat_id: str, open_id: str) -> str:
        return f"{chat_id}:{open_id}"

    def get_or_create(self, chat_id: str, open_id: str, project_alias: str) -> ConversationBinding:
        key = self.key(chat_id, open_id)
        with self._lock:
            values = self._load()
            binding = self._binding_from(values.get(key))
            if binding is not None:
                return binding
            binding = ConversationBinding(
                key=key,
                chat_id=chat_id,
                open_id=open_id,
                project_alias=project_alias,
                generation=1,
                thread_id=None,
                updated_at=self._now(),
            )
            values[key] = asdict(binding)
            self._save(values)
            return binding

    def reset(self, chat_id: str, open_id: str, project_alias: str) -> ConversationBinding:
        key = self.key(chat_id, open_id)
        with self._lock:
            values = self._load()
            previous = self._binding_from(values.get(key))
            binding = ConversationBinding(
                key=key,
                chat_id=chat_id,
                open_id=open_id,
                project_alias=project_alias,
                generation=(previous.generation + 1) if previous else 1,
                thread_id=None,
                updated_at=self._now(),
            )
            values[key] = asdict(binding)
            self._save(values)
            return binding

    def get(self, key: str) -> ConversationBinding | None:
        with self._lock:
            return self._binding_from(self._load().get(key))

    def list_bindings(self) -> tuple[ConversationBinding, ...]:
        """Return a stable snapshot of every valid conversation binding."""
        with self._lock:
            bindings = (
                binding
                for binding in (self._binding_from(value) for value in self._load().values())
                if binding is not None
            )
            return tuple(sorted(bindings, key=lambda item: item.key))

    def attach_thread(self, key: str, generation: int, thread_id: str) -> bool:
        with self._lock:
            values = self._load()
            current = self._binding_from(values.get(key))
            if current is None or current.generation != generation:
                return False
            updated = ConversationBinding(
                key=current.key,
                chat_id=current.chat_id,
                open_id=current.open_id,
                project_alias=current.project_alias,
                generation=current.generation,
                thread_id=thread_id,
                updated_at=self._now(),
            )
            values[key] = asdict(updated)
            self._save(values)
            return True

    def _load(self) -> dict[str, dict[str, object]]:
        if not self._path.is_file():
            return {}
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return {}
        conversations = raw.get("conversations") if isinstance(raw, dict) else None
        return conversations if isinstance(conversations, dict) else {}

    def _save(self, values: dict[str, dict[str, object]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._path.with_suffix(self._path.suffix + ".tmp")
        temporary.write_text(
            json.dumps({"version": 1, "conversations": values}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self._path)

    @staticmethod
    def _binding_from(value: object) -> ConversationBinding | None:
        if not isinstance(value, dict):
            return None
        try:
            return ConversationBinding(
                key=str(value["key"]),
                chat_id=str(value["chat_id"]),
                open_id=str(value["open_id"]),
                project_alias=str(value["project_alias"]),
                generation=int(value["generation"]),
                thread_id=str(value["thread_id"]) if value.get("thread_id") else None,
                updated_at=str(value["updated_at"]),
            )
        except (KeyError, TypeError, ValueError):
            return None

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

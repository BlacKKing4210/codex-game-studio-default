from __future__ import annotations

import json
import logging
import threading
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Protocol

from .conversations import ConversationBinding, ConversationStore


LOG = logging.getLogger("feishu_gateway.sync")
FEISHU_CLIENT_ID_PREFIX = "feishu:"
_TERMINAL_STATUSES = {"completed", "interrupted", "failed"}
_MAX_TRACKED_FEISHU_TURNS = 2000


class ThreadHistoryReader(Protocol):
    def read_thread(self, thread_id: str) -> dict[str, object]: ...

    def close(self) -> None: ...


class SyncStateError(RuntimeError):
    pass


@dataclass(frozen=True)
class SyncState:
    thread_id: str
    initialized: bool = False
    feishu_turn_ids: tuple[str, ...] = ()
    announced_turn_ids: tuple[str, ...] = ()
    finished_turn_ids: tuple[str, ...] = ()
    updated_at: str = ""


class SyncStateStore:
    """Durable origin and delivery ledger for transcript mirroring."""

    def __init__(self, path: Path):
        self._path = path
        self._lock = threading.Lock()

    def get(self, thread_id: str) -> SyncState:
        with self._lock:
            return self._state_from(thread_id, self._load().get(thread_id))

    def initialize(self, thread_id: str, baseline_turn_ids: list[str]) -> SyncState:
        with self._lock:
            values = self._load()
            current = self._state_from(thread_id, values.get(thread_id))
            if current.initialized:
                return current
            baseline = self._unique((*current.finished_turn_ids, *baseline_turn_ids))
            updated = SyncState(
                thread_id=thread_id,
                initialized=True,
                feishu_turn_ids=current.feishu_turn_ids,
                announced_turn_ids=self._unique(
                    (*current.announced_turn_ids, *baseline_turn_ids)
                ),
                finished_turn_ids=baseline,
                updated_at=self._now(),
            )
            values[thread_id] = asdict(updated)
            self._save(values)
            return updated

    def mark_feishu_turn(self, thread_id: str, turn_id: str) -> None:
        if thread_id and turn_id:
            self._update(thread_id, feishu_turn_id=turn_id)

    def mark_delivery(
        self,
        thread_id: str,
        turn_id: str,
        *,
        announced: bool,
        finished: bool,
    ) -> None:
        self._update(
            thread_id,
            announced_turn_id=turn_id if announced else None,
            finished_turn_id=turn_id if finished else None,
        )

    def _update(
        self,
        thread_id: str,
        *,
        feishu_turn_id: str | None = None,
        announced_turn_id: str | None = None,
        finished_turn_id: str | None = None,
    ) -> None:
        with self._lock:
            values = self._load()
            current = self._state_from(thread_id, values.get(thread_id))
            updated = SyncState(
                thread_id=thread_id,
                initialized=current.initialized,
                feishu_turn_ids=self._bounded_feishu(
                    (*current.feishu_turn_ids, *((feishu_turn_id,) if feishu_turn_id else ()))
                ),
                # These ledgers intentionally remain complete: thread/read returns
                # full history, so evicting old IDs would replay them forever.
                announced_turn_ids=self._unique(
                    (*current.announced_turn_ids, *((announced_turn_id,) if announced_turn_id else ()))
                ),
                finished_turn_ids=self._unique(
                    (*current.finished_turn_ids, *((finished_turn_id,) if finished_turn_id else ()))
                ),
                updated_at=self._now(),
            )
            values[thread_id] = asdict(updated)
            self._save(values)

    def _load(self) -> dict[str, dict[str, object]]:
        if not self._path.is_file():
            return {}
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise SyncStateError(f"Cannot read thread sync state: {type(exc).__name__}") from exc
        if not isinstance(raw, dict) or raw.get("version") != 2:
            raise SyncStateError("Unsupported thread sync state format")
        threads = raw.get("threads")
        if not isinstance(threads, dict):
            raise SyncStateError("Thread sync state is missing threads")
        return threads

    def _save(self, values: dict[str, dict[str, object]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._path.with_suffix(self._path.suffix + ".tmp")
        temporary.write_text(
            json.dumps({"version": 2, "threads": values}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self._path)

    @classmethod
    def _state_from(cls, thread_id: str, value: object) -> SyncState:
        if value is None:
            return SyncState(thread_id=thread_id)
        if not isinstance(value, dict):
            raise SyncStateError(f"Invalid thread sync entry: {thread_id}")
        initialized = value.get("initialized", False)
        updated_at = value.get("updated_at", "")
        if not isinstance(initialized, bool) or not isinstance(updated_at, str):
            raise SyncStateError(f"Invalid thread sync fields: {thread_id}")
        return SyncState(
            thread_id=thread_id,
            initialized=initialized,
            feishu_turn_ids=cls._bounded_feishu(
                cls._strings(value.get("feishu_turn_ids"), "feishu_turn_ids")
            ),
            announced_turn_ids=cls._unique(
                cls._strings(value.get("announced_turn_ids"), "announced_turn_ids")
            ),
            finished_turn_ids=cls._unique(
                cls._strings(value.get("finished_turn_ids"), "finished_turn_ids")
            ),
            updated_at=updated_at,
        )

    @staticmethod
    def _strings(value: object, field: str) -> tuple[str, ...]:
        if value is None:
            return ()
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            raise SyncStateError(f"Invalid thread sync list: {field}")
        return tuple(value)

    @staticmethod
    def _unique(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
        return tuple(dict.fromkeys(value for value in values if value))

    @classmethod
    def _bounded_feishu(cls, values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
        return cls._unique(values)[-_MAX_TRACKED_FEISHU_TURNS:]

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()


class ThreadTranscriptSync:
    """Mirror Codex Desktop turns into the currently bound Feishu chat.

    A dedicated read-only App Server client polls persisted history with
    ``thread/read(includeTurns=true)``. Per-turn IDs keep concurrent Desktop and
    Feishu turns independent, while ``clientUserMessageId`` prevents self-echo.
    """

    def __init__(
        self,
        reader: ThreadHistoryReader,
        conversations: ConversationStore,
        state_store: SyncStateStore,
        interval_seconds: int,
        initial_backfill_turns: int,
        deliver: Callable[[str, str, str], bool],
    ):
        self._reader = reader
        self._conversations = conversations
        self._state_store = state_store
        self._interval_seconds = interval_seconds
        self._initial_backfill_turns = initial_backfill_turns
        self._deliver = deliver
        self._stop_event = threading.Event()
        self._worker = threading.Thread(
            target=self._run,
            name="codex-thread-sync",
            daemon=True,
        )

    def start(self) -> None:
        self._worker.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._worker.is_alive():
            self._worker.join(timeout=5)
        self._reader.close()

    def poll_once(self) -> None:
        for binding in self._conversations.list_bindings():
            if not binding.thread_id:
                continue
            try:
                thread = self._reader.read_thread(binding.thread_id)
                self._sync_binding(binding, thread)
            except SyncStateError:
                LOG.exception("Thread sync state is invalid; delivery paused to avoid replay")
                return
            except Exception:
                LOG.exception("Codex transcript sync failed: thread_id=%s", binding.thread_id)

    def _run(self) -> None:
        LOG.info("Starting Codex Desktop to Feishu synchronization")
        try:
            while not self._stop_event.is_set():
                self.poll_once()
                self._stop_event.wait(self._interval_seconds)
        finally:
            self._reader.close()

    def _sync_binding(self, binding: ConversationBinding, thread: dict[str, object]) -> None:
        assert binding.thread_id is not None
        raw_turns = thread.get("turns")
        if not isinstance(raw_turns, list):
            return

        state = self._state_store.get(binding.thread_id)
        desktop_turns = [
            turn
            for turn in raw_turns
            if isinstance(turn, dict) and self._is_desktop_turn(turn, state)
        ]
        desktop_turns.sort(key=self._turn_order)
        baseline_count = max(0, len(desktop_turns) - self._initial_backfill_turns)
        baseline_ids = [str(turn.get("id", "")) for turn in desktop_turns[:baseline_count]]
        state = self._state_store.initialize(
            binding.thread_id,
            [turn_id for turn_id in baseline_ids if turn_id],
        )

        for turn in desktop_turns:
            turn_id = str(turn.get("id", ""))
            if not turn_id:
                continue
            status = str(turn.get("status", ""))
            user_text = self._user_text(turn)
            if not user_text:
                if status in _TERMINAL_STATUSES:
                    self._state_store.mark_delivery(
                        binding.thread_id,
                        turn_id,
                        announced=True,
                        finished=True,
                    )
                    state = self._state_store.get(binding.thread_id)
                continue

            if status == "inProgress" and turn_id not in state.announced_turn_ids:
                text = f"💻 来自 Codex Desktop\n你：{user_text}\n\n🤔 Thinking…"
                event_id = f"sync:{binding.thread_id}:{turn_id}:thinking"
                if self._deliver_current(binding, text, event_id):
                    self._state_store.mark_delivery(
                        binding.thread_id,
                        turn_id,
                        announced=True,
                        finished=False,
                    )
                    state = self._state_store.get(binding.thread_id)
                continue

            if status not in _TERMINAL_STATUSES or turn_id in state.finished_turn_ids:
                continue
            answer = self._answer_text(turn, status)
            if turn_id in state.announced_turn_ids:
                text = f"💻 Codex Desktop\nCodex：{answer}"
                event_id = f"sync:{binding.thread_id}:{turn_id}:final"
            else:
                text = f"💻 来自 Codex Desktop\n你：{user_text}\n\nCodex：{answer}"
                event_id = f"sync:{binding.thread_id}:{turn_id}:transcript"
            if self._deliver_current(binding, text, event_id):
                self._state_store.mark_delivery(
                    binding.thread_id,
                    turn_id,
                    announced=True,
                    finished=True,
                )
                state = self._state_store.get(binding.thread_id)

    def _deliver_current(self, binding: ConversationBinding, text: str, event_id: str) -> bool:
        current = self._conversations.get(binding.key)
        if (
            current is None
            or current.generation != binding.generation
            or current.thread_id != binding.thread_id
        ):
            return False
        return self._deliver(binding.chat_id, text, event_id)

    @staticmethod
    def _is_desktop_turn(turn: dict[str, object], state: SyncState) -> bool:
        turn_id = str(turn.get("id", ""))
        if turn_id in state.feishu_turn_ids:
            return False
        user = ThreadTranscriptSync._user_item(turn)
        if user is None:
            return False
        client_id = str(user.get("clientId") or "")
        return bool(client_id) and not client_id.startswith(FEISHU_CLIENT_ID_PREFIX)

    @staticmethod
    def _user_item(turn: dict[str, object]) -> dict[str, object] | None:
        items = turn.get("items")
        if not isinstance(items, list):
            return None
        return next(
            (
                item
                for item in items
                if isinstance(item, dict) and item.get("type") == "userMessage"
            ),
            None,
        )

    @staticmethod
    def _user_text(turn: dict[str, object]) -> str:
        user = ThreadTranscriptSync._user_item(turn)
        if user is None:
            return ""
        content = user.get("content")
        if not isinstance(content, list):
            return ""
        return "\n".join(
            str(item.get("text", "")).strip()
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "text"
            and str(item.get("text", "")).strip()
        ).strip()

    @staticmethod
    def _answer_text(turn: dict[str, object], status: str) -> str:
        items = turn.get("items")
        if not isinstance(items, list):
            items = []
        messages = [
            item
            for item in items
            if isinstance(item, dict) and item.get("type") == "agentMessage"
        ]
        finals = [
            str(item.get("text", "")).strip()
            for item in messages
            if item.get("phase") == "final_answer" and str(item.get("text", "")).strip()
        ]
        if finals:
            return finals[-1]
        fallbacks = [
            str(item.get("text", "")).strip()
            for item in messages
            if item.get("phase") != "commentary" and str(item.get("text", "")).strip()
        ]
        if fallbacks:
            return fallbacks[-1]
        if status == "interrupted":
            return "该回合已中断。"
        if status == "failed":
            return "该回合执行失败。"
        return "该回合已结束，但没有可同步的最终文本。"

    @staticmethod
    def _turn_order(turn: dict[str, object]) -> tuple[int, str]:
        try:
            started_at = int(turn.get("startedAt") or 0)
        except (TypeError, ValueError):
            started_at = 0
        return started_at, str(turn.get("id", ""))

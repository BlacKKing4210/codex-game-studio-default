from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Callable

from feishu_gateway.conversations import ConversationStore
from feishu_gateway.sync import SyncStateStore, ThreadTranscriptSync


class FakeThreadReader:
    def __init__(self, turns: list[dict[str, object]] | None = None):
        self.turns = turns or []
        self.before_return: Callable[[], None] | None = None

    def read_thread(self, thread_id: str) -> dict[str, object]:
        if self.before_return is not None:
            callback = self.before_return
            self.before_return = None
            callback()
        return {"id": thread_id, "turns": self.turns}

    def close(self) -> None:
        pass


def make_turn(
    turn_id: str,
    client_id: str | None,
    status: str,
    prompt: str,
    answer: str | None = None,
    *,
    started_at: int = 1,
) -> dict[str, object]:
    items: list[dict[str, object]] = [
        {
            "type": "userMessage",
            "clientId": client_id,
            "content": [{"type": "text", "text": prompt}],
        }
    ]
    if answer is not None:
        items.append(
            {"type": "agentMessage", "phase": "final_answer", "text": answer}
        )
    return {
        "id": turn_id,
        "status": status,
        "startedAt": started_at,
        "items": items,
    }


class ThreadTranscriptSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.conversations = ConversationStore(self.root / "conversations.json")
        initial = self.conversations.get_or_create("chat-1", "user-1", "studio")
        self.assertTrue(
            self.conversations.attach_thread(initial.key, initial.generation, "thread-1")
        )
        self.reader = FakeThreadReader()
        self.state = SyncStateStore(self.root / "sync.json")
        self.deliveries: list[tuple[str, str, str]] = []

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def make_sync(
        self,
        *,
        backfill: int = 1,
        deliver: Callable[[str, str, str], bool] | None = None,
        state: SyncStateStore | None = None,
    ) -> ThreadTranscriptSync:
        def record(chat_id: str, text: str, event_id: str) -> bool:
            self.deliveries.append((chat_id, text, event_id))
            return True

        return ThreadTranscriptSync(
            reader=self.reader,
            conversations=self.conversations,
            state_store=state or self.state,
            interval_seconds=1,
            initial_backfill_turns=backfill,
            deliver=deliver or record,
        )

    def test_first_poll_baselines_history_and_backfills_only_latest_turn(self) -> None:
        self.reader.turns = [
            make_turn("old", "desktop-old", "completed", "旧问题", "旧回答", started_at=1),
            make_turn("new", "desktop-new", "completed", "新问题", "新回答", started_at=2),
        ]
        sync = self.make_sync(backfill=1)

        sync.poll_once()
        sync.poll_once()

        self.assertEqual(len(self.deliveries), 1)
        self.assertIn("新问题", self.deliveries[0][1])
        self.assertIn("新回答", self.deliveries[0][1])
        self.assertNotIn("旧问题", self.deliveries[0][1])
        self.assertEqual(self.deliveries[0][2], "sync:thread-1:new:transcript")

    def test_in_progress_sends_one_thinking_then_one_final(self) -> None:
        self.reader.turns = [
            make_turn("desktop-1", "desktop-client", "inProgress", "解决同步问题")
        ]
        sync = self.make_sync()

        sync.poll_once()
        sync.poll_once()
        self.reader.turns = [
            make_turn(
                "desktop-1",
                "desktop-client",
                "completed",
                "解决同步问题",
                "已经修复。",
            )
        ]
        sync.poll_once()
        sync.poll_once()

        self.assertEqual(len(self.deliveries), 2)
        self.assertIn("Thinking", self.deliveries[0][1])
        self.assertIn("解决同步问题", self.deliveries[0][1])
        self.assertEqual(self.deliveries[0][2], "sync:thread-1:desktop-1:thinking")
        self.assertNotIn("解决同步问题", self.deliveries[1][1])
        self.assertIn("已经修复。", self.deliveries[1][1])
        self.assertEqual(self.deliveries[1][2], "sync:thread-1:desktop-1:final")

    def test_feishu_and_legacy_turns_are_not_echoed(self) -> None:
        self.reader.turns = [
            make_turn("feishu-1", "feishu:message-1", "completed", "飞书问题", "回答"),
            make_turn("legacy-1", None, "completed", "旧客户端问题", "回答", started_at=2),
        ]

        self.make_sync(backfill=10).poll_once()

        self.assertEqual(self.deliveries, [])

    def test_marked_feishu_turn_is_skipped_even_with_non_feishu_client_id(self) -> None:
        self.state.mark_feishu_turn("thread-1", "turn-race")
        self.reader.turns = [
            make_turn("turn-race", "desktop-looking-id", "completed", "飞书问题", "回答")
        ]

        self.make_sync(backfill=10).poll_once()

        self.assertEqual(self.deliveries, [])

    def test_concurrent_turns_keep_independent_origin_and_state(self) -> None:
        self.reader.turns = [
            make_turn("desktop-a", "desktop-a", "inProgress", "A", started_at=1),
            make_turn("feishu-b", "feishu:message-b", "completed", "B", "B答", started_at=2),
            make_turn("desktop-c", "desktop-c", "completed", "C", "C答", started_at=3),
        ]

        self.make_sync(backfill=10).poll_once()

        self.assertEqual(
            [event_id for _chat, _text, event_id in self.deliveries],
            ["sync:thread-1:desktop-a:thinking", "sync:thread-1:desktop-c:transcript"],
        )

    def test_failed_enqueue_retries_same_event_without_advancing_state(self) -> None:
        self.reader.turns = [
            make_turn("desktop-1", "desktop-client", "completed", "问题", "回答")
        ]
        attempts: list[tuple[str, str, str]] = []

        def flaky(chat_id: str, text: str, event_id: str) -> bool:
            attempts.append((chat_id, text, event_id))
            return len(attempts) > 1

        sync = self.make_sync(deliver=flaky)
        sync.poll_once()
        self.assertNotIn("desktop-1", self.state.get("thread-1").finished_turn_ids)
        sync.poll_once()
        sync.poll_once()

        self.assertEqual(len(attempts), 2)
        self.assertEqual(attempts[0], attempts[1])
        self.assertIn("desktop-1", self.state.get("thread-1").finished_turn_ids)

    def test_binding_reset_during_read_prevents_old_slot_delivery(self) -> None:
        self.reader.turns = [
            make_turn("desktop-1", "desktop-client", "completed", "问题", "回答")
        ]
        self.reader.before_return = lambda: self.conversations.reset(
            "chat-1", "user-1", "studio"
        )

        self.make_sync().poll_once()

        self.assertEqual(self.deliveries, [])

    def test_long_final_is_not_truncated(self) -> None:
        answer = "完整内容" * 2000
        self.reader.turns = [
            make_turn("desktop-1", "desktop-client", "completed", "问题", answer)
        ]

        self.make_sync().poll_once()

        self.assertIn(answer, self.deliveries[0][1])

    def test_restart_uses_persisted_turn_ledger_without_duplicate(self) -> None:
        self.reader.turns = [
            make_turn("desktop-1", "desktop-client", "completed", "问题", "回答")
        ]
        self.make_sync().poll_once()
        restarted_state = SyncStateStore(self.root / "sync.json")

        self.make_sync(state=restarted_state).poll_once()

        self.assertEqual(len(self.deliveries), 1)

    def test_more_than_2000_baseline_turns_never_replay(self) -> None:
        self.reader.turns = [
            make_turn(
                f"desktop-{index:04d}",
                f"desktop-client-{index}",
                "completed",
                f"问题 {index}",
                f"回答 {index}",
                started_at=index,
            )
            for index in range(2105)
        ]
        sync = self.make_sync(backfill=0)

        sync.poll_once()
        sync.poll_once()

        self.assertEqual(self.deliveries, [])
        self.assertEqual(len(self.state.get("thread-1").finished_turn_ids), 2105)

    def test_corrupt_state_fails_closed_without_replay(self) -> None:
        (self.root / "sync.json").write_text("not-json", encoding="utf-8")
        self.reader.turns = [
            make_turn("desktop-1", "desktop-client", "completed", "问题", "回答")
        ]

        with self.assertLogs("feishu_gateway.sync", level="ERROR"):
            self.make_sync().poll_once()

        self.assertEqual(self.deliveries, [])

    def test_malformed_thread_entry_fails_closed_without_replay(self) -> None:
        (self.root / "sync.json").write_text(
            '{"version":2,"threads":{"thread-1":{"initialized":true,'
            '"finished_turn_ids":"not-a-list"}}}',
            encoding="utf-8",
        )
        self.reader.turns = [
            make_turn("desktop-1", "desktop-client", "completed", "问题", "回答")
        ]

        with self.assertLogs("feishu_gateway.sync", level="ERROR"):
            self.make_sync().poll_once()

        self.assertEqual(self.deliveries, [])


if __name__ == "__main__":
    unittest.main()

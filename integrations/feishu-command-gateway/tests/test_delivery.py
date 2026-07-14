from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from feishu_gateway.delivery import DeliveryOutbox, DeliveryStateError, split_text


class DeliveryTests(unittest.TestCase):
    def test_short_text_is_unchanged(self) -> None:
        self.assertEqual(split_text("完成", 500), ("完成",))

    def test_surrounding_whitespace_is_preserved(self) -> None:
        self.assertEqual(split_text("  完成\n", 500), ("  完成\n",))

    def test_long_text_is_split_without_truncation(self) -> None:
        original = ("第一段内容\n" * 80) + "最后一段"
        chunks = split_text(original, 120)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 120 for chunk in chunks))
        rebuilt = "".join(re.sub(r"^\[\d+/\d+\]\n", "", chunk) for chunk in chunks)
        self.assertEqual(rebuilt, original)

    def test_outbox_delivers_every_part_in_event_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sent: list[tuple[str, str, str]] = []
            outbox = DeliveryOutbox(
                Path(directory) / "outbox.json",
                32,
                lambda chat_id, text, delivery_id: not sent.append((chat_id, text, delivery_id)),
            )
            first_text = "第一条消息需要拆成多个顺序发送的部分。"
            second_text = "第二条消息"

            with patch.object(DeliveryOutbox, "_now", return_value="2026-07-14T00:00:00+00:00"):
                outbox.enqueue("chat-1", first_text, "event-1")
                outbox.enqueue("chat-1", second_text, "event-2")
                while outbox.drain_once():
                    pass

            self.assertEqual(
                [text for _chat_id, text, _delivery_id in sent],
                [*split_text(first_text, 32), *split_text(second_text, 32)],
            )
            self.assertTrue(all(chat_id == "chat-1" for chat_id, _text, _delivery_id in sent))
            self.assertEqual(len({delivery_id for _chat_id, _text, delivery_id in sent}), len(sent))
            self.assertEqual(outbox.pending_count(), 0)

    def test_outbox_resumes_remaining_parts_after_restart_without_duplicate_send(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outbox.json"
            text = "重启之后只应续传尚未成功投递的剩余分片。"
            expected = split_text(text, 30)
            first_run: list[tuple[str, str, str]] = []
            first = DeliveryOutbox(
                path,
                30,
                lambda chat_id, chunk, delivery_id: not first_run.append((chat_id, chunk, delivery_id)),
            )
            first.enqueue("chat-1", text, "stable-event")
            self.assertTrue(first.drain_once())
            self.assertEqual([item[1] for item in first_run], [expected[0]])

            resumed_run: list[tuple[str, str, str]] = []
            resumed = DeliveryOutbox(
                path,
                30,
                lambda chat_id, chunk, delivery_id: not resumed_run.append((chat_id, chunk, delivery_id)),
            )
            self.assertTrue(resumed.enqueue("chat-1", text, "stable-event"))
            while resumed.drain_once():
                pass

            self.assertEqual([item[1] for item in resumed_run], list(expected[1:]))
            self.assertNotIn(first_run[0][2], {item[2] for item in resumed_run})
            self.assertEqual(resumed.pending_count(), 0)

            after_completion: list[tuple[str, str, str]] = []
            completed = DeliveryOutbox(
                path,
                30,
                lambda chat_id, chunk, delivery_id: not after_completion.append(
                    (chat_id, chunk, delivery_id)
                ),
            )
            self.assertTrue(completed.enqueue("chat-1", text, "stable-event"))
            self.assertFalse(completed.drain_once())
            self.assertEqual(after_completion, [])

    def test_outbox_failed_send_keeps_part_pending_with_same_delivery_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outbox.json"
            failed: list[tuple[str, str, str]] = []

            def fail_send(chat_id: str, text: str, delivery_id: str) -> bool:
                failed.append((chat_id, text, delivery_id))
                return False

            outbox = DeliveryOutbox(
                path,
                500,
                fail_send,
            )
            outbox.enqueue("chat-1", "暂时发送失败", "retry-event")

            self.assertFalse(outbox.drain_once())
            self.assertEqual(outbox.pending_count(), 1)
            state = json.loads(path.read_text(encoding="utf-8"))
            self.assertFalse(state["records"]["retry-event"]["parts"][0]["delivered"])

            retried: list[tuple[str, str, str]] = []
            restarted = DeliveryOutbox(
                path,
                500,
                lambda chat_id, text, delivery_id: not retried.append((chat_id, text, delivery_id)),
            )
            self.assertTrue(restarted.drain_once())
            self.assertEqual(restarted.pending_count(), 0)
            self.assertEqual(retried[0][2], failed[0][2])

    def test_same_event_id_cannot_silently_change_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            outbox = DeliveryOutbox(
                Path(directory) / "outbox.json",
                500,
                lambda _chat, _text, _delivery_id: True,
            )
            outbox.enqueue("chat-1", "原始内容", "event-1")

            with self.assertRaises(DeliveryStateError):
                outbox.enqueue("chat-1", "被替换的内容", "event-1")


if __name__ == "__main__":
    unittest.main()

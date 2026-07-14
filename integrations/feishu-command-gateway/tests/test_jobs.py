from __future__ import annotations

import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import Mock

from feishu_gateway.config import Project
from feishu_gateway.conversations import ConversationStore
from feishu_gateway.executor import ExecutionResult
from feishu_gateway.jobs import JobManager, JobState
from feishu_gateway.sync import SyncStateStore


class JobManagerTests(unittest.TestCase):
    def test_release_runs_job_persists_ids_and_delivers_thinking_then_exact_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            conversations = ConversationStore(root / "conversations.json")
            binding = conversations.get_or_create("chat-1", "user-1", "studio")
            sync_state = SyncStateStore(root / "sync.json")
            executor = Mock()
            executor_started = threading.Event()
            delivered = threading.Event()
            deliveries: list[tuple[str, str, str, str]] = []
            exact_output = "最终回答\n\n保留原始格式。"

            def execute(
                _project_path: Path,
                _prompt: str,
                _cancel_event: threading.Event,
                **callbacks: object,
            ) -> ExecutionResult:
                executor_started.set()
                callbacks["on_thread_started"]("thread-1")
                self.assertEqual(conversations.get(binding.key).thread_id, "thread-1")
                callbacks["on_turn_started"]("thread-1", "turn-1")
                self.assertIn("turn-1", sync_state.get("thread-1").feishu_turn_ids)
                self.assertNotIn("on_progress", callbacks)
                self.assertEqual([item[3] for item in deliveries], ["thinking"])
                self.assertIn("Thinking", deliveries[0][1])
                return ExecutionResult(0, exact_output, "thread-1", "turn-1")

            executor.execute.side_effect = execute

            def deliver(message_id: str, text: str, chat_id: str, delivery_key: str) -> None:
                deliveries.append((message_id, text, chat_id, delivery_key))
                if delivery_key == "result":
                    delivered.set()

            manager = JobManager(executor, conversations, sync_state, 2, deliver)
            manager.start()
            job = manager.submit(
                Project("studio", root),
                binding,
                "修复启动报错",
                "message-1",
                "飞书 | studio | 修复启动报错",
            )

            self.assertFalse(job.ready_event.is_set())
            self.assertFalse(executor_started.wait(0.1))

            manager.release(job.id)

            self.assertTrue(delivered.wait(2), "job result was not delivered")
            self.assertEqual(job.state, JobState.COMPLETED)
            self.assertEqual(job.codex_thread_id, "thread-1")
            self.assertEqual(conversations.get(binding.key).thread_id, "thread-1")
            self.assertIn("turn-1", sync_state.get("thread-1").feishu_turn_ids)
            self.assertEqual([item[3] for item in deliveries], ["thinking", "result"])
            self.assertIn("Thinking", deliveries[0][1])
            self.assertEqual(
                deliveries[1],
                ("message-1", exact_output, "chat-1", "result"),
            )
            kwargs = executor.execute.call_args.kwargs
            self.assertEqual(kwargs["client_user_message_id"], "feishu:message-1")

    def test_cancel_before_release_delivers_terminal_status_without_starting_executor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            conversations = ConversationStore(root / "conversations.json")
            binding = conversations.get_or_create("chat-1", "user-1", "studio")
            sync_state = SyncStateStore(root / "sync.json")
            executor = Mock()
            delivered = threading.Event()
            deliveries: list[tuple[str, str, str, str]] = []

            def deliver(message_id: str, text: str, chat_id: str, delivery_key: str) -> None:
                deliveries.append((message_id, text, chat_id, delivery_key))
                if delivery_key == "result":
                    delivered.set()

            manager = JobManager(executor, conversations, sync_state, 2, deliver)
            manager.start()
            job = manager.submit(
                Project("studio", root),
                binding,
                "不会开始",
                "message-2",
                "飞书 | studio | 不会开始",
            )

            ok, _ = manager.cancel(job.id, "user-1")

            self.assertTrue(ok)
            self.assertTrue(delivered.wait(2), "canceled job did not deliver a terminal status")
            self.assertEqual(job.state, JobState.CANCELED)
            executor.execute.assert_not_called()
            self.assertEqual(len(deliveries), 1)
            self.assertEqual(deliveries[0][0], "message-2")
            self.assertIn("已取消", deliveries[0][1])
            self.assertEqual(deliveries[0][2:], ("chat-1", "result"))


if __name__ == "__main__":
    unittest.main()

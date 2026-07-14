from __future__ import annotations

import io
import json
import threading
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from feishu_gateway.executor import CodexExecutor, CodexThreadReader


class ExecutorTests(unittest.TestCase):
    @patch.object(CodexExecutor, "_start_reader_threads")
    @patch("feishu_gateway.executor.subprocess.Popen")
    def test_reports_turn_lifecycle_and_only_matching_progress(
        self,
        popen: Mock,
        start_readers: Mock,
    ) -> None:
        process = Mock()
        process.stdin = io.StringIO()
        process.poll.return_value = None
        popen.return_value = process

        def seed_messages(_process: Mock, messages: object, _stderr: list[str]) -> None:
            messages.put({"id": 1, "result": {}})
            messages.put({"id": 2, "result": {"thread": {"id": "thread-1"}}})
            messages.put({"id": 3, "result": {}})
            messages.put({"id": 4, "result": {"turn": {"id": "turn-1"}}})
            messages.put(
                {
                    "method": "item/completed",
                    "params": {
                        "threadId": "thread-1",
                        "turnId": "another-turn",
                        "item": {
                            "type": "agentMessage",
                            "phase": "commentary",
                            "text": "不应串入当前回合",
                        },
                    },
                }
            )
            messages.put(
                {
                    "method": "item/completed",
                    "params": {
                        "threadId": "thread-1",
                        "turnId": "turn-1",
                        "item": {
                            "type": "agentMessage",
                            "phase": "commentary",
                            "text": "正在检查工作区",
                        },
                    },
                }
            )
            messages.put(
                {
                    "method": "item/completed",
                    "params": {
                        "threadId": "thread-1",
                        "turnId": "turn-1",
                        "item": {"type": "agentMessage", "phase": "final_answer", "text": "完成"},
                    },
                }
            )
            messages.put(
                {
                    "method": "turn/completed",
                    "params": {
                        "threadId": "thread-1",
                        "turn": {"id": "turn-1", "status": "completed"},
                    },
                }
            )

        start_readers.side_effect = seed_messages
        executor = CodexExecutor(("codex.exe",), "workspace-write", 30, 1000)
        thread_started = Mock()
        turn_started = Mock()
        progress = Mock()

        result = executor.execute(
            Path.cwd(),
            "修复启动报错",
            threading.Event(),
            thread_name="飞书 | game | 修复启动报错",
            client_user_message_id="feishu:message-1",
            on_thread_started=thread_started,
            on_turn_started=turn_started,
            on_progress=progress,
        )

        self.assertEqual(popen.call_args.args[0], ["codex.exe", "app-server", "--stdio"])
        self.assertFalse(popen.call_args.kwargs["shell"])
        sent = [json.loads(line) for line in process.stdin.getvalue().splitlines()]
        start = next(item for item in sent if item.get("method") == "thread/start")
        turn = next(item for item in sent if item.get("method") == "turn/start")
        self.assertFalse(start["params"]["ephemeral"])
        self.assertEqual(start["params"]["approvalPolicy"], "never")
        self.assertEqual(turn["params"]["input"], [{"type": "text", "text": "修复启动报错"}])
        self.assertEqual(turn["params"]["clientUserMessageId"], "feishu:message-1")
        thread_started.assert_called_once_with("thread-1")
        turn_started.assert_called_once_with("thread-1", "turn-1")
        progress.assert_called_once_with("正在检查工作区")
        self.assertEqual(result.thread_id, "thread-1")
        self.assertEqual(result.turn_id, "turn-1")
        self.assertEqual(result.output, "完成")

    def test_keeps_full_output_for_delivery_chunking(self) -> None:
        executor = CodexExecutor(("codex.exe",), "workspace-write", 30, 10)
        value = "这是一条不会在执行层被截断的完整回复"
        self.assertEqual(executor._format(value), value)

    @patch.object(CodexExecutor, "_start_reader_threads")
    @patch("feishu_gateway.executor.subprocess.Popen")
    def test_thread_reader_uses_official_thread_read_with_turns(
        self,
        popen: Mock,
        start_readers: Mock,
    ) -> None:
        process = Mock()
        process.stdin = io.StringIO()
        process.poll.return_value = None
        popen.return_value = process

        def seed_messages(_process: Mock, messages: object, _stderr: list[str]) -> None:
            messages.put({"id": 1, "result": {}})
            messages.put(
                {
                    "id": 2,
                    "result": {
                        "thread": {"id": "thread-1", "turns": [{"id": "turn-1"}]}
                    },
                }
            )

        start_readers.side_effect = seed_messages
        reader = CodexThreadReader(("codex.exe",))

        thread = reader.read_thread("thread-1")
        reader.close()

        sent = [json.loads(line) for line in process.stdin.getvalue().splitlines()]
        request = next(item for item in sent if item.get("method") == "thread/read")
        self.assertEqual(
            request["params"],
            {"threadId": "thread-1", "includeTurns": True},
        )
        self.assertEqual(thread["turns"], [{"id": "turn-1"}])

if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import io
import json
import threading
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from feishu_gateway.executor import CodexExecutor


class ExecutorTests(unittest.TestCase):
    @patch.object(CodexExecutor, "_start_reader_threads")
    @patch("feishu_gateway.executor.subprocess.Popen")
    def test_creates_persistent_thread_and_sends_exact_user_text(self, popen: Mock, start_readers: Mock) -> None:
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

        result = executor.execute(
            Path.cwd(),
            "修复启动报错",
            threading.Event(),
            thread_name="飞书 | game | 修复启动报错",
        )

        self.assertEqual(popen.call_args.args[0], ["codex.exe", "app-server", "--stdio"])
        self.assertFalse(popen.call_args.kwargs["shell"])
        sent = [json.loads(line) for line in process.stdin.getvalue().splitlines()]
        start = next(item for item in sent if item.get("method") == "thread/start")
        turn = next(item for item in sent if item.get("method") == "turn/start")
        self.assertFalse(start["params"]["ephemeral"])
        self.assertEqual(start["params"]["approvalPolicy"], "never")
        self.assertEqual(turn["params"]["input"], [{"type": "text", "text": "修复启动报错"}])
        self.assertEqual(result.thread_id, "thread-1")
        self.assertEqual(result.output, "完成")


if __name__ == "__main__":
    unittest.main()

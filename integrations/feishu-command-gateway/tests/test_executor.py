from __future__ import annotations

import threading
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from feishu_gateway.executor import CodexExecutor


class ExecutorTests(unittest.TestCase):
    @patch("feishu_gateway.executor.subprocess.Popen")
    def test_global_safety_flags_precede_exec(self, popen: Mock) -> None:
        process = Mock()
        process.communicate.return_value = ("done", "")
        process.returncode = 0
        popen.return_value = process
        executor = CodexExecutor(("codex.exe",), "workspace-write", 30, 1000)

        result = executor.execute(Path.cwd(), "run tests", threading.Event())

        args = popen.call_args.args[0]
        self.assertEqual(
            args[:7],
            [
                "codex.exe",
                "--sandbox",
                "workspace-write",
                "--ask-for-approval",
                "never",
                "exec",
                "--ephemeral",
            ],
        )
        self.assertEqual(result.output, "done")


if __name__ == "__main__":
    unittest.main()

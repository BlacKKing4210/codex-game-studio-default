from __future__ import annotations

import os
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class ExecutionResult:
    return_code: int
    output: str
    canceled: bool = False
    timed_out: bool = False


class CodexExecutor:
    def __init__(
        self,
        command_prefix: tuple[str, ...],
        sandbox: str,
        timeout_seconds: int,
        max_output_chars: int,
    ):
        self._command_prefix = command_prefix
        self._sandbox = sandbox
        self._timeout_seconds = timeout_seconds
        self._max_output_chars = max_output_chars

    def execute(
        self,
        project_path: Path,
        prompt: str,
        cancel_event: threading.Event,
        process_started: Callable[[subprocess.Popen[str]], None] | None = None,
    ) -> ExecutionResult:
        safe_prompt = (
            "This task was submitted by an authorized user through the Feishu command gateway. "
            "Work only inside the current Git repository. Preserve unrelated user changes. "
            "Do not push, publish, deploy, change credentials, expose secrets, delete .git, use destructive Git, "
            "shut down the host, or expand the requested scope. Verify the result and report a concise final summary.\n\n"
            f"User task:\n{prompt}"
        )
        args = [
            *self._command_prefix,
            "--sandbox",
            self._sandbox,
            "--ask-for-approval",
            "never",
            "exec",
            "--ephemeral",
            "--color",
            "never",
            safe_prompt,
        ]
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        process = subprocess.Popen(
            args,
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
            creationflags=creationflags,
        )
        if process_started:
            process_started(process)

        deadline = time.monotonic() + self._timeout_seconds
        while True:
            if cancel_event.is_set():
                _terminate(process)
                stdout, stderr = process.communicate()
                return ExecutionResult(process.returncode or -1, self._format(stdout, stderr), canceled=True)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                _terminate(process)
                stdout, stderr = process.communicate()
                return ExecutionResult(process.returncode or -1, self._format(stdout, stderr), timed_out=True)
            try:
                stdout, stderr = process.communicate(timeout=min(1.0, remaining))
                return ExecutionResult(process.returncode, self._format(stdout, stderr))
            except subprocess.TimeoutExpired:
                continue

    def _format(self, stdout: str, stderr: str) -> str:
        output = stdout.strip()
        if not output:
            output = stderr.strip() or "Codex 未返回文本结果。"
        if len(output) > self._max_output_chars:
            output = output[: self._max_output_chars - 20].rstrip() + "\n...[结果已截断]"
        return output


def _terminate(process: subprocess.Popen[str]) -> None:
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)

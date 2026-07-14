from __future__ import annotations

import json
import os
import queue
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


REMOTE_DEVELOPER_INSTRUCTIONS = """\
This persistent Codex thread is controlled by an authorized user through the Feishu bridge.
Treat each Feishu text message as the user's actual message and preserve normal multi-turn context.
Work only inside the current Git repository and preserve unrelated user changes.
Do not push, publish, deploy, change credentials, expose secrets, delete .git, use destructive Git,
shut down the host, or expand the requested scope. The remote bridge cannot grant interactive
permissions. If a request needs permission or a user decision, explain what is needed and stop safely.
Verify completed work and give a concise final response.
"""


@dataclass(frozen=True)
class ExecutionResult:
    return_code: int
    output: str
    thread_id: str | None = None
    turn_id: str | None = None
    canceled: bool = False
    timed_out: bool = False


class AppServerProtocolError(RuntimeError):
    pass


class _Canceled(RuntimeError):
    pass


class _TimedOut(RuntimeError):
    pass


class CodexExecutor:
    """Runs one turn through the official Codex App Server protocol."""

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
        thread_id: str | None = None,
        thread_name: str | None = None,
        client_user_message_id: str | None = None,
        on_thread_started: Callable[[str], None] | None = None,
        on_turn_started: Callable[[str, str], None] | None = None,
        on_progress: Callable[[str], None] | None = None,
        process_started: Callable[[subprocess.Popen[str]], None] | None = None,
    ) -> ExecutionResult:
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        process = subprocess.Popen(
            [*self._command_prefix, "app-server", "--stdio"],
            cwd=project_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            shell=False,
            creationflags=creationflags,
        )
        if process_started:
            process_started(process)

        messages: queue.Queue[dict[str, Any]] = queue.Queue()
        stderr_lines: list[str] = []
        self._start_reader_threads(process, messages, stderr_lines)
        deadline = time.monotonic() + self._timeout_seconds
        current_thread_id = thread_id
        current_turn_id: str | None = None
        pending: list[dict[str, Any]] = []

        try:
            self._request(
                process,
                messages,
                stderr_lines,
                cancel_event,
                deadline,
                pending,
                1,
                "initialize",
                {
                    "clientInfo": {
                        "name": "feishu_codex_bridge",
                        "title": "Feishu Codex Bridge",
                        "version": "1.0.0",
                    }
                },
            )
            self._send(process, {"method": "initialized", "params": {}})

            if current_thread_id:
                response = self._request(
                    process,
                    messages,
                    stderr_lines,
                    cancel_event,
                    deadline,
                    pending,
                    2,
                    "thread/resume",
                    {
                        "threadId": current_thread_id,
                        "cwd": str(project_path.resolve()),
                        "approvalPolicy": "never",
                        "sandbox": self._sandbox,
                        "developerInstructions": REMOTE_DEVELOPER_INSTRUCTIONS,
                    },
                )
            else:
                response = self._request(
                    process,
                    messages,
                    stderr_lines,
                    cancel_event,
                    deadline,
                    pending,
                    2,
                    "thread/start",
                    {
                        "cwd": str(project_path.resolve()),
                        "approvalPolicy": "never",
                        "sandbox": self._sandbox,
                        "ephemeral": False,
                        "developerInstructions": REMOTE_DEVELOPER_INSTRUCTIONS,
                    },
                )
                current_thread_id = str(response["thread"]["id"])
                if thread_name:
                    self._request(
                        process,
                        messages,
                        stderr_lines,
                        cancel_event,
                        deadline,
                        pending,
                        3,
                        "thread/name/set",
                        {"threadId": current_thread_id, "name": thread_name},
                    )

            if current_thread_id and on_thread_started:
                on_thread_started(current_thread_id)

            turn_request_id = 4 if thread_name and thread_id is None else 3
            turn_params: dict[str, Any] = {
                "threadId": current_thread_id,
                "input": [{"type": "text", "text": prompt}],
                "approvalPolicy": "never",
                "cwd": str(project_path.resolve()),
            }
            if client_user_message_id:
                turn_params["clientUserMessageId"] = client_user_message_id
            turn = self._request(
                process,
                messages,
                stderr_lines,
                cancel_event,
                deadline,
                pending,
                turn_request_id,
                "turn/start",
                turn_params,
            )
            current_turn_id = str(turn["turn"]["id"])
            if on_turn_started:
                on_turn_started(current_thread_id, current_turn_id)
            output = self._wait_for_turn(
                process,
                messages,
                stderr_lines,
                cancel_event,
                deadline,
                pending,
                current_thread_id,
                current_turn_id,
                on_progress,
            )
            return ExecutionResult(0, self._format(output), current_thread_id, current_turn_id)
        except _Canceled:
            return ExecutionResult(-1, "Codex 任务已取消。", current_thread_id, current_turn_id, canceled=True)
        except _TimedOut:
            return ExecutionResult(-1, "Codex 任务执行超时。", current_thread_id, current_turn_id, timed_out=True)
        except (AppServerProtocolError, KeyError, TypeError, ValueError) as exc:
            detail = str(exc).strip() or type(exc).__name__
            if stderr_lines:
                detail = f"{detail}; app-server: {stderr_lines[-1]}"
            return ExecutionResult(1, self._format(detail), current_thread_id, current_turn_id)
        finally:
            _terminate(process)

    @staticmethod
    def _start_reader_threads(
        process: subprocess.Popen[str],
        messages: queue.Queue[dict[str, Any]],
        stderr_lines: list[str],
    ) -> None:
        def read_stdout() -> None:
            assert process.stdout is not None
            for line in process.stdout:
                value = line.strip()
                if not value:
                    continue
                try:
                    parsed = json.loads(value)
                except json.JSONDecodeError:
                    messages.put({"_invalid": value})
                    continue
                if isinstance(parsed, dict):
                    messages.put(parsed)

        def read_stderr() -> None:
            assert process.stderr is not None
            for line in process.stderr:
                value = line.rstrip()
                if value:
                    stderr_lines.append(value)
                    if len(stderr_lines) > 200:
                        del stderr_lines[:100]

        threading.Thread(target=read_stdout, name="codex-app-server-stdout", daemon=True).start()
        threading.Thread(target=read_stderr, name="codex-app-server-stderr", daemon=True).start()

    def _request(
        self,
        process: subprocess.Popen[str],
        messages: queue.Queue[dict[str, Any]],
        stderr_lines: list[str],
        cancel_event: threading.Event,
        deadline: float,
        pending: list[dict[str, Any]],
        request_id: int,
        method: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        self._send(process, {"method": method, "id": request_id, "params": params})
        while True:
            message = self._next_message(process, messages, stderr_lines, cancel_event, deadline)
            if message.get("id") == request_id and "method" not in message:
                if "error" in message:
                    raise AppServerProtocolError(self._error_text(method, message["error"]))
                result = message.get("result")
                if not isinstance(result, dict):
                    raise AppServerProtocolError(f"{method} returned an invalid result")
                return result
            if self._handle_server_request(process, message):
                continue
            pending.append(message)

    def _wait_for_turn(
        self,
        process: subprocess.Popen[str],
        messages: queue.Queue[dict[str, Any]],
        stderr_lines: list[str],
        cancel_event: threading.Event,
        deadline: float,
        pending: list[dict[str, Any]],
        thread_id: str,
        turn_id: str,
        on_progress: Callable[[str], None] | None = None,
    ) -> str:
        final_messages: list[str] = []
        fallback_messages: list[str] = []
        backlog = list(pending)
        pending.clear()
        while True:
            message = backlog.pop(0) if backlog else self._next_message(
                process, messages, stderr_lines, cancel_event, deadline
            )
            if self._handle_server_request(process, message):
                continue
            method = message.get("method")
            params = message.get("params") if isinstance(message.get("params"), dict) else {}
            if (
                method == "item/completed"
                and params.get("threadId") == thread_id
                and str(params.get("turnId", "")) == turn_id
            ):
                item = params.get("item") if isinstance(params.get("item"), dict) else {}
                if item.get("type") == "agentMessage":
                    text = str(item.get("text", "")).strip()
                    if text:
                        if item.get("phase") == "final_answer":
                            final_messages.append(text)
                        elif item.get("phase") == "commentary":
                            if on_progress:
                                on_progress(text)
                        else:
                            fallback_messages.append(text)
            if method == "turn/completed" and params.get("threadId") == thread_id:
                turn = params.get("turn") if isinstance(params.get("turn"), dict) else {}
                if str(turn.get("id", "")) != turn_id:
                    continue
                if turn.get("status") != "completed":
                    error = turn.get("error") or "turn did not complete"
                    raise AppServerProtocolError(str(error))
                if final_messages:
                    return final_messages[-1]
                if fallback_messages:
                    return fallback_messages[-1]
                return "Codex 已完成该轮，但没有返回可显示的文本。"

    @staticmethod
    def _handle_server_request(process: subprocess.Popen[str], message: dict[str, Any]) -> bool:
        if "id" not in message or "method" not in message:
            return False
        method = str(message["method"])
        if method in {"item/commandExecution/requestApproval", "item/fileChange/requestApproval"}:
            result: dict[str, Any] = {"decision": "decline"}
        elif method in {"execCommandApproval", "applyPatchApproval"}:
            result = {"decision": "denied"}
        elif method == "item/tool/requestUserInput":
            result = {"answers": {}}
        elif method == "mcpServer/elicitation/request":
            result = {"action": "decline", "content": None}
        elif method == "item/tool/call":
            result = {"success": False, "contentItems": []}
        else:
            CodexExecutor._send(
                process,
                {
                    "id": message["id"],
                    "error": {
                        "code": -32001,
                        "message": "Interactive requests are unavailable through the Feishu bridge.",
                    },
                },
            )
            return True
        CodexExecutor._send(process, {"id": message["id"], "result": result})
        return True

    @staticmethod
    def _next_message(
        process: subprocess.Popen[str],
        messages: queue.Queue[dict[str, Any]],
        stderr_lines: list[str],
        cancel_event: threading.Event,
        deadline: float,
    ) -> dict[str, Any]:
        while True:
            if cancel_event.is_set():
                raise _Canceled
            if time.monotonic() >= deadline:
                raise _TimedOut
            try:
                return messages.get(timeout=min(0.5, max(0.05, deadline - time.monotonic())))
            except queue.Empty:
                if process.poll() is not None:
                    detail = stderr_lines[-1] if stderr_lines else "no stderr output"
                    raise AppServerProtocolError(f"app-server exited with {process.returncode}: {detail}")

    @staticmethod
    def _send(process: subprocess.Popen[str], message: dict[str, Any]) -> None:
        if process.stdin is None:
            raise AppServerProtocolError("app-server stdin is unavailable")
        process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        process.stdin.flush()

    @staticmethod
    def _error_text(method: str, error: Any) -> str:
        if isinstance(error, dict):
            message = str(error.get("message", "protocol error"))
            data = error.get("data")
            return f"{method} failed: {message}" + (f" ({data})" if data else "")
        return f"{method} failed: {error}"

    def _format(self, output: str) -> str:
        # Keep the canonical Codex response intact. Feishu delivery splits long
        # text into deterministic chunks instead of changing the transcript.
        return output.strip() or "Codex 未返回文本结果。"


class CodexThreadReader:
    """Read persisted Codex thread history through one App Server process."""

    def __init__(
        self,
        command_prefix: tuple[str, ...],
        request_timeout_seconds: int = 30,
    ):
        self._command_prefix = command_prefix
        self._request_timeout_seconds = request_timeout_seconds
        self._lock = threading.Lock()
        self._process: subprocess.Popen[str] | None = None
        self._messages: queue.Queue[dict[str, Any]] | None = None
        self._stderr_lines: list[str] = []
        self._next_request_id = 1

    def read_thread(self, thread_id: str) -> dict[str, object]:
        """Return one thread with complete turns, reconnecting once if needed."""
        last_error: Exception | None = None
        with self._lock:
            for _attempt in range(2):
                try:
                    self._ensure_started()
                    result = self._request_locked(
                        "thread/read",
                        {"threadId": thread_id, "includeTurns": True},
                    )
                    thread = result.get("thread")
                    if not isinstance(thread, dict):
                        raise AppServerProtocolError("thread/read returned an invalid thread")
                    return thread
                except (
                    AppServerProtocolError,
                    _TimedOut,
                    OSError,
                    KeyError,
                    TypeError,
                    ValueError,
                ) as exc:
                    last_error = exc
                    self._close_locked()
            assert last_error is not None
            raise last_error

    def close(self) -> None:
        with self._lock:
            self._close_locked()

    def _ensure_started(self) -> None:
        if self._process is not None and self._process.poll() is None:
            return
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        process = subprocess.Popen(
            [*self._command_prefix, "app-server", "--stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            shell=False,
            creationflags=creationflags,
        )
        self._process = process
        self._messages = queue.Queue()
        self._stderr_lines = []
        self._next_request_id = 1
        CodexExecutor._start_reader_threads(process, self._messages, self._stderr_lines)
        self._request_locked(
            "initialize",
            {
                "clientInfo": {
                    "name": "feishu_codex_transcript_sync",
                    "title": "Feishu Codex Transcript Sync",
                    "version": "1.0.0",
                }
            },
        )
        CodexExecutor._send(process, {"method": "initialized", "params": {}})

    def _request_locked(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        process = self._process
        messages = self._messages
        if process is None or messages is None:
            raise AppServerProtocolError("app-server reader is not initialized")
        request_id = self._next_request_id
        self._next_request_id += 1
        CodexExecutor._send(
            process,
            {"method": method, "id": request_id, "params": params},
        )
        deadline = time.monotonic() + self._request_timeout_seconds
        cancel_event = threading.Event()
        while True:
            message = CodexExecutor._next_message(
                process,
                messages,
                self._stderr_lines,
                cancel_event,
                deadline,
            )
            if message.get("id") == request_id and "method" not in message:
                if "error" in message:
                    raise AppServerProtocolError(
                        CodexExecutor._error_text(method, message["error"])
                    )
                result = message.get("result")
                if not isinstance(result, dict):
                    raise AppServerProtocolError(f"{method} returned an invalid result")
                return result
            CodexExecutor._handle_server_request(process, message)

    def _close_locked(self) -> None:
        process = self._process
        self._process = None
        self._messages = None
        self._stderr_lines = []
        if process is not None:
            _terminate(process)


def _terminate(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)

from __future__ import annotations

import queue
import subprocess
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Callable

from .config import Project
from .conversations import ConversationBinding, ConversationStore
from .executor import CodexExecutor


class JobState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    TIMED_OUT = "timed_out"


@dataclass
class Job:
    id: str
    project: Project
    prompt: str
    requester_open_id: str
    reply_message_id: str
    conversation_key: str
    conversation_generation: int
    thread_id_hint: str | None
    thread_name: str
    state: JobState = JobState.QUEUED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    cancel_event: threading.Event = field(default_factory=threading.Event, repr=False)
    process: subprocess.Popen[str] | None = field(default=None, repr=False)
    codex_thread_id: str | None = None


class JobManager:
    def __init__(
        self,
        executor: CodexExecutor,
        conversations: ConversationStore,
        max_queue: int,
        reply: Callable[[str, str], None],
    ):
        self._executor = executor
        self._conversations = conversations
        self._queue: queue.Queue[Job] = queue.Queue(maxsize=max_queue)
        self._reply = reply
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()
        self._worker = threading.Thread(target=self._run, name="codex-conversation-worker", daemon=True)

    def start(self) -> None:
        self._worker.start()

    def submit(
        self,
        project: Project,
        binding: ConversationBinding,
        prompt: str,
        message_id: str,
        thread_name: str,
    ) -> Job:
        job = Job(
            id=uuid.uuid4().hex[:8],
            project=project,
            prompt=prompt,
            requester_open_id=binding.open_id,
            reply_message_id=message_id,
            conversation_key=binding.key,
            conversation_generation=binding.generation,
            thread_id_hint=binding.thread_id,
            thread_name=thread_name,
        )
        with self._lock:
            self._jobs[job.id] = job
        try:
            self._queue.put_nowait(job)
        except queue.Full:
            with self._lock:
                del self._jobs[job.id]
            raise RuntimeError("任务队列已满，请稍后再试。")
        return job

    def cancel(self, job_id: str, requester_open_id: str) -> tuple[bool, str]:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return False, "未找到该任务。"
            if job.requester_open_id != requester_open_id:
                return False, "不能取消其他用户提交的任务。"
            if job.state not in {JobState.QUEUED, JobState.RUNNING}:
                return False, f"任务已处于 {job.state.value} 状态。"
            job.cancel_event.set()
            if job.state == JobState.QUEUED:
                job.state = JobState.CANCELED
        return True, "已请求取消任务。"

    def status_text(self) -> str:
        with self._lock:
            active = [job for job in self._jobs.values() if job.state in {JobState.QUEUED, JobState.RUNNING}]
        if not active:
            return "当前没有排队或执行中的任务。"
        active.sort(key=lambda item: item.created_at)
        return "\n".join(
            f"{job.id} | {job.state.value} | {job.project.alias} | {job.codex_thread_id or '待创建任务'}"
            for job in active
        )

    def _run(self) -> None:
        while True:
            job = self._queue.get()
            try:
                if job.cancel_event.is_set():
                    job.state = JobState.CANCELED
                    continue
                job.state = JobState.RUNNING
                current = self._conversations.get(job.conversation_key)
                thread_id = job.thread_id_hint
                if current is not None and current.generation == job.conversation_generation:
                    thread_id = current.thread_id
                result = self._executor.execute(
                    job.project.path,
                    job.prompt,
                    job.cancel_event,
                    thread_id=thread_id,
                    thread_name=job.thread_name if thread_id is None else None,
                    process_started=lambda process: setattr(job, "process", process),
                )
                job.codex_thread_id = result.thread_id
                if result.thread_id:
                    self._conversations.attach_thread(
                        job.conversation_key,
                        job.conversation_generation,
                        result.thread_id,
                    )
                task_ref = f"Codex 任务 {result.thread_id}" if result.thread_id else "Codex 任务未创建"
                if result.canceled:
                    job.state = JobState.CANCELED
                    prefix = f"消息 {job.id} 已取消 | {task_ref}"
                elif result.timed_out:
                    job.state = JobState.TIMED_OUT
                    prefix = f"消息 {job.id} 超时 | {task_ref}"
                elif result.return_code == 0:
                    job.state = JobState.COMPLETED
                    prefix = f"{task_ref} 已回复"
                else:
                    job.state = JobState.FAILED
                    prefix = f"消息 {job.id} 失败 | {task_ref}"
                self._reply(job.reply_message_id, f"{prefix}\n\n{result.output}")
            except Exception as exc:  # Boundary: keep the worker alive and report a sanitized error.
                job.state = JobState.FAILED
                self._reply(job.reply_message_id, f"消息 {job.id} 执行失败：{type(exc).__name__}: {exc}")
            finally:
                job.process = None
                self._queue.task_done()

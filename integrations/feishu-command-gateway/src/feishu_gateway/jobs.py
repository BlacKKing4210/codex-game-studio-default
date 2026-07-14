from __future__ import annotations

import queue
import logging
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
from .sync import SyncStateError, SyncStateStore


LOG = logging.getLogger("feishu_gateway.jobs")


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
    chat_id: str
    conversation_generation: int
    thread_id_hint: str | None
    thread_name: str
    state: JobState = JobState.QUEUED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    cancel_event: threading.Event = field(default_factory=threading.Event, repr=False)
    ready_event: threading.Event = field(default_factory=threading.Event, repr=False)
    process: subprocess.Popen[str] | None = field(default=None, repr=False)
    codex_thread_id: str | None = None


class JobManager:
    def __init__(
        self,
        executor: CodexExecutor,
        conversations: ConversationStore,
        sync_state: SyncStateStore,
        max_queue: int,
        deliver: Callable[[str, str, str, str], None],
    ):
        self._executor = executor
        self._conversations = conversations
        self._sync_state = sync_state
        self._queue: queue.Queue[Job] = queue.Queue(maxsize=max_queue)
        self._deliver = deliver
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
            chat_id=binding.chat_id,
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

    def release(self, job_id: str) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
        if job is not None:
            job.ready_event.set()

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
                job.ready_event.set()
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
                job.ready_event.wait()
                with self._lock:
                    canceled_before_start = job.cancel_event.is_set() or job.state == JobState.CANCELED
                    if canceled_before_start:
                        job.state = JobState.CANCELED
                    else:
                        job.state = JobState.RUNNING
                if canceled_before_start:
                    self._deliver(
                        job.reply_message_id,
                        f"消息 {job.id} 已取消。",
                        job.chat_id,
                        "result",
                    )
                    continue
                self._deliver(
                    job.reply_message_id,
                    f"🤔 Thinking…\n状态：Codex 正在处理\n任务：{job.id} | {job.project.alias}",
                    job.chat_id,
                    "thinking",
                )
                current = self._conversations.get(job.conversation_key)
                thread_id = job.thread_id_hint
                if current is not None and current.generation == job.conversation_generation:
                    thread_id = current.thread_id

                def on_thread_started(value: str) -> None:
                    job.codex_thread_id = value
                    self._conversations.attach_thread(
                        job.conversation_key,
                        job.conversation_generation,
                        value,
                    )

                def on_turn_started(value: str, turn_id: str) -> None:
                    on_thread_started(value)
                    try:
                        self._sync_state.mark_feishu_turn(value, turn_id)
                    except SyncStateError:
                        # clientUserMessageId remains the authoritative echo
                        # guard; a corrupt sync ledger must not kill the job.
                        LOG.exception("Cannot record Feishu turn origin: thread_id=%s", value)

                result = self._executor.execute(
                    job.project.path,
                    job.prompt,
                    job.cancel_event,
                    thread_id=thread_id,
                    thread_name=job.thread_name if thread_id is None else None,
                    client_user_message_id=f"feishu:{job.reply_message_id}",
                    on_thread_started=on_thread_started,
                    on_turn_started=on_turn_started,
                    process_started=lambda process: setattr(job, "process", process),
                )
                job.codex_thread_id = result.thread_id
                if result.thread_id:
                    self._conversations.attach_thread(
                        job.conversation_key,
                        job.conversation_generation,
                        result.thread_id,
                    )
                if result.canceled:
                    state = JobState.CANCELED
                    output = f"消息 {job.id} 已取消。\n\n{result.output}"
                elif result.timed_out:
                    state = JobState.TIMED_OUT
                    output = f"消息 {job.id} 执行超时。\n\n{result.output}"
                elif result.return_code == 0:
                    state = JobState.COMPLETED
                    output = result.output
                else:
                    state = JobState.FAILED
                    task_ref = f"Codex 任务 {result.thread_id}" if result.thread_id else "Codex 任务未创建"
                    output = f"消息 {job.id} 失败 | {task_ref}\n\n{result.output}"
                with self._lock:
                    job.state = state
                self._deliver(job.reply_message_id, output, job.chat_id, "result")
            except Exception as exc:  # Boundary: keep the worker alive and report a sanitized error.
                with self._lock:
                    job.state = JobState.FAILED
                self._deliver(
                    job.reply_message_id,
                    f"消息 {job.id} 执行失败：{type(exc).__name__}: {exc}",
                    job.chat_id,
                    "result",
                )
            finally:
                with self._lock:
                    job.process = None
                self._queue.task_done()

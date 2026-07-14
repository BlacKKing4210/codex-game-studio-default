from __future__ import annotations

import json
import logging
import re
import sys
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path

import lark_oapi as lark
from dotenv import load_dotenv
from lark_oapi.api.im.v1 import (
    CreateMessageRequest,
    CreateMessageRequestBody,
    P2ImMessageReceiveV1,
    ReplyMessageRequest,
    ReplyMessageRequestBody,
)

from .auth import AuthorizedUsers
from .commands import CommandError, CommandKind, help_text, parse_command
from .config import ConfigurationError, Settings
from .conversations import ConversationBinding, ConversationStore
from .delivery import DeliveryOutbox, DeliveryStateError
from .executor import CodexExecutor, CodexThreadReader
from .jobs import JobManager
from .receipts import MessageReceiptStore, ReceiptStateError
from .sync import SyncStateStore, ThreadTranscriptSync


LOG = logging.getLogger("feishu_gateway")


class FeishuGateway:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._auth = AuthorizedUsers(
            settings.authorized_users_file,
            settings.allowed_open_ids,
            settings.bootstrap_token,
        )
        self._api_client = lark.Client.builder().app_id(settings.app_id).app_secret(settings.app_secret).build()
        self._outgoing = ThreadPoolExecutor(max_workers=1, thread_name_prefix="feishu-reply")
        self._api_lock = threading.Lock()
        self._receipts = MessageReceiptStore(settings.received_messages_file)
        self._conversations = ConversationStore(settings.conversation_threads_file)
        executor = CodexExecutor(
            command_prefix=settings.codex_command,
            sandbox=settings.sandbox,
            timeout_seconds=settings.timeout_seconds,
            max_output_chars=settings.max_reply_chars,
        )
        self._sync_state = SyncStateStore(settings.thread_sync_file)
        self._delivery_outbox = DeliveryOutbox(
            settings.delivery_outbox_file,
            settings.max_reply_chars,
            self._send_text_to_chat,
        )
        self._jobs = JobManager(
            executor,
            self._conversations,
            self._sync_state,
            settings.max_queue,
            self.deliver_job_message_async,
        )
        self._sync = ThreadTranscriptSync(
            reader=CodexThreadReader(settings.codex_command),
            conversations=self._conversations,
            state_store=self._sync_state,
            interval_seconds=settings.sync_interval_seconds,
            initial_backfill_turns=settings.sync_backfill_turns,
            deliver=self._deliver_thread_sync,
        )

    def start(self) -> None:
        self._delivery_outbox.start()
        self._jobs.start()
        self._sync.start()
        event_handler = (
            lark.EventDispatcherHandler.builder("", "")
            .register_p2_im_message_receive_v1(self._handle_message)
            .build()
        )
        ws_client = lark.ws.Client(
            self._settings.app_id,
            self._settings.app_secret,
            event_handler=event_handler,
            log_level=lark.LogLevel.WARNING,
        )
        LOG.info("Starting Feishu long connection")
        try:
            ws_client.start()
        finally:
            self._sync.stop()
            self._delivery_outbox.stop()
            self._outgoing.shutdown(wait=False, cancel_futures=True)

    def _handle_message(self, data: P2ImMessageReceiveV1) -> None:
        event = data.event
        if event is None or event.message is None or event.sender is None:
            return
        message = event.message
        message_id = message.message_id or ""
        if not message_id:
            return
        try:
            if not self._receipts.claim(message_id):
                return
        except ReceiptStateError:
            LOG.exception("Feishu receipt state is invalid; refusing duplicate-prone delivery")
            return

        sender_id = event.sender.sender_id
        open_id = sender_id.open_id if sender_id else ""
        chat_type = message.chat_type or ""
        is_private = chat_type == "p2p"
        if not is_private and not self._settings.allow_group:
            self.reply_async(message_id, "当前仅允许与机器人单聊发送命令。")
            return
        if message.message_type != "text":
            self.reply_async(message_id, "当前仅支持文本消息。发送 /codex help 查看用法。")
            return

        try:
            content = json.loads(message.content or "{}")
            text = str(content.get("text", "")).strip()
        except json.JSONDecodeError as exc:
            self.reply_async(message_id, str(exc))
            return
        if not text:
            self.reply_async(message_id, "消息不能为空。")
            return

        command = None
        if text.lower().startswith("/codex"):
            try:
                command = parse_command(text)
            except CommandError as exc:
                self.reply_async(message_id, str(exc))
                return

        if command is not None and command.kind == CommandKind.BIND:
            ok, response = self._auth.bind(open_id, command.argument or "", is_private)
            self.reply_async(message_id, response)
            if ok:
                LOG.info("A Feishu user completed bootstrap binding")
            return
        if not self._auth.is_authorized(open_id):
            self.reply_async(message_id, "未授权。请在单聊中发送 /codex bind <绑定口令>。")
            return

        chat_id = message.chat_id or open_id
        if command is None:
            risk = self._blocked_text(text)
            if risk:
                self.reply_async(message_id, risk)
                return
            binding = self._conversations.get_or_create(
                chat_id,
                open_id,
                self._settings.default_project_alias,
            )
            self._submit_message(binding, text, message_id)
        elif command.kind == CommandKind.HELP:
            self.reply_async(message_id, help_text())
        elif command.kind == CommandKind.PROJECTS:
            projects = "\n".join(
                f"{alias} -> {project.path}" for alias, project in sorted(self._settings.projects.items())
            )
            self.reply_async(message_id, f"允许的项目：\n{projects}")
        elif command.kind == CommandKind.STATUS:
            self.reply_async(message_id, self._jobs.status_text())
        elif command.kind == CommandKind.CANCEL:
            _, response = self._jobs.cancel(command.argument or "", open_id)
            self.reply_async(message_id, response)
        elif command.kind == CommandKind.THREAD:
            binding = self._conversations.get_or_create(
                chat_id,
                open_id,
                self._settings.default_project_alias,
            )
            thread = binding.thread_id or "尚未创建；发送下一条普通消息后创建"
            self.reply_async(
                message_id,
                f"当前项目：{binding.project_alias}\nCodex 任务：{thread}\n会话代次：{binding.generation}",
            )
        elif command.kind == CommandKind.NEW:
            current = self._conversations.get_or_create(
                chat_id,
                open_id,
                self._settings.default_project_alias,
            )
            alias = command.project_alias or current.project_alias
            if alias not in self._settings.projects:
                self.reply_async(message_id, "项目别名不在白名单中。发送 /codex projects 查看。")
                return
            binding = self._conversations.reset(chat_id, open_id, alias)
            self.reply_async(
                message_id,
                f"已切换到新的独立 Codex 任务槽位：{alias}。下一条普通消息会创建任务并显示在 Codex 桌面端。"
                f"\n会话代次：{binding.generation}",
            )
        elif command.kind == CommandKind.RUN:
            project = self._settings.projects.get(command.project_alias or "")
            if project is None:
                self.reply_async(message_id, "项目别名不在白名单中。发送 /codex projects 查看。")
                return
            binding = self._conversations.reset(chat_id, open_id, project.alias)
            self._submit_message(binding, command.prompt or "", message_id)

    def _submit_message(self, binding: ConversationBinding, prompt: str, message_id: str) -> None:
        project = self._settings.projects.get(binding.project_alias)
        if project is None:
            self.reply_async(message_id, "当前项目已不在白名单中，请发送 /codex new <项目别名>。")
            return
        title_fragment = re.sub(r"\s+", " ", prompt).strip()[:28]
        thread_name = f"飞书 | {project.alias} | {title_fragment}"
        try:
            job = self._jobs.submit(project, binding, prompt, message_id, thread_name)
        except RuntimeError as exc:
            self.reply_async(message_id, str(exc))
            return
        target = binding.thread_id or "新 Codex 任务"
        try:
            acknowledgement = self.reply_async(
                message_id,
                f"⏳ 已收到｜正在排队\n任务：{job.id} | {project.alias} | {target}",
            )
        except Exception:
            self._jobs.release(job.id)
        else:
            # Start only after the queue acknowledgement attempt finishes;
            # actual RUNNING state is then delivered as one Thinking message.
            acknowledgement.add_done_callback(lambda _future: self._jobs.release(job.id))

    @staticmethod
    def _blocked_text(prompt: str) -> str | None:
        from .commands import blocked_risk

        risk = blocked_risk(prompt)
        if risk:
            return f"该远程消息被安全策略阻止：{risk}。请在本机 Codex 中执行。"
        return None

    def reply_async(self, message_id: str, text: str) -> Future[bool]:
        return self._outgoing.submit(self._reply_text, message_id, text)

    def deliver_job_message_async(
        self,
        message_id: str,
        text: str,
        chat_id: str,
        delivery_key: str,
    ) -> None:
        event_id = f"feishu-codex:{message_id}:{delivery_key}"
        try:
            self._delivery_outbox.enqueue(chat_id, text, event_id)
        except DeliveryStateError:
            LOG.exception("Cannot enqueue Feishu job delivery: event_id=%s", event_id)

    def _deliver_thread_sync(self, chat_id: str, text: str, event_id: str) -> bool:
        try:
            return self._delivery_outbox.enqueue(chat_id, text, event_id)
        except DeliveryStateError:
            LOG.exception("Feishu transcript mirror delivery failed: chat_id=%s event_id=%s", chat_id, event_id)
            return False

    def _reply_text(self, message_id: str, text: str) -> bool:
        try:
            request = (
                ReplyMessageRequest.builder()
                .message_id(message_id)
                .request_body(
                    ReplyMessageRequestBody.builder()
                    .msg_type("text")
                    .content(json.dumps({"text": text}, ensure_ascii=False))
                    .build()
                )
                .build()
            )
            with self._api_lock:
                response = self._api_client.im.v1.message.reply(request)
            if response.success():
                LOG.info("Feishu acknowledgement delivered: message_id=%s", message_id)
                return True
            else:
                LOG.error("Feishu reply failed: code=%s msg=%s", response.code, response.msg)
        except Exception:
            LOG.exception("Feishu acknowledgement raised an exception: message_id=%s", message_id)
        return False

    def _send_text_to_chat(self, chat_id: str, text: str, delivery_id: str) -> bool:
        last_error = "unknown delivery error"
        for attempt in range(1, 4):
            try:
                request = (
                    CreateMessageRequest.builder()
                    .receive_id_type("chat_id")
                    .request_body(
                        CreateMessageRequestBody.builder()
                        .receive_id(chat_id)
                        .msg_type("text")
                        .content(json.dumps({"text": text}, ensure_ascii=False))
                        .uuid(delivery_id)
                        .build()
                    )
                    .build()
                )
                with self._api_lock:
                    response = self._api_client.im.v1.message.create(request)
                if response.success():
                    LOG.info("Feishu message delivered: chat_id=%s delivery_id=%s", chat_id, delivery_id)
                    return True
                last_error = f"code={response.code} msg={response.msg}"
            except Exception as exc:
                last_error = f"{type(exc).__name__}: {exc}"
            if attempt < 3:
                LOG.warning(
                    "Feishu task result delivery failed; retrying: attempt=%s chat_id=%s error=%s",
                    attempt,
                    chat_id,
                    last_error,
                )
                time.sleep(attempt)
        LOG.error(
            "Feishu task result delivery exhausted retries: chat_id=%s delivery_id=%s error=%s",
            chat_id,
            delivery_id,
            last_error,
        )
        return False


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env")
    try:
        settings = Settings.from_env(root)
    except (ConfigurationError, ValueError, json.JSONDecodeError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    FeishuGateway(settings).start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

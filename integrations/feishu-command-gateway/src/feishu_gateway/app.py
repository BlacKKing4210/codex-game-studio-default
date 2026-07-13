from __future__ import annotations

import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import lark_oapi as lark
from dotenv import load_dotenv
from lark_oapi.api.im.v1 import (
    P2ImMessageReceiveV1,
    ReplyMessageRequest,
    ReplyMessageRequestBody,
)

from .auth import AuthorizedUsers
from .commands import CommandError, CommandKind, help_text, parse_command
from .config import ConfigurationError, Settings
from .executor import CodexExecutor
from .jobs import JobManager


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
        self._outgoing = ThreadPoolExecutor(max_workers=2, thread_name_prefix="feishu-reply")
        self._seen_messages: set[str] = set()
        self._seen_lock = threading.Lock()
        executor = CodexExecutor(
            command_prefix=settings.codex_command,
            sandbox=settings.sandbox,
            timeout_seconds=settings.timeout_seconds,
            max_output_chars=settings.max_reply_chars,
        )
        self._jobs = JobManager(executor, settings.max_queue, self.reply_async)

    def start(self) -> None:
        self._jobs.start()
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
        ws_client.start()

    def _handle_message(self, data: P2ImMessageReceiveV1) -> None:
        event = data.event
        if event is None or event.message is None or event.sender is None:
            return
        message = event.message
        message_id = message.message_id or ""
        if not message_id or not self._mark_seen(message_id):
            return

        sender_id = event.sender.sender_id
        open_id = sender_id.open_id if sender_id else ""
        chat_type = message.chat_type or ""
        is_private = chat_type == "p2p"
        if not is_private and not self._settings.allow_group:
            self.reply_async(message_id, "当前仅允许与机器人单聊发送命令。")
            return
        if message.message_type != "text":
            self.reply_async(message_id, "当前仅支持文本命令。发送 /codex help 查看用法。")
            return

        try:
            content = json.loads(message.content or "{}")
            command = parse_command(str(content.get("text", "")))
        except (json.JSONDecodeError, CommandError) as exc:
            self.reply_async(message_id, str(exc))
            return

        if command.kind == CommandKind.BIND:
            ok, response = self._auth.bind(open_id, command.argument or "", is_private)
            self.reply_async(message_id, response)
            if ok:
                LOG.info("A Feishu user completed bootstrap binding")
            return
        if not self._auth.is_authorized(open_id):
            self.reply_async(message_id, "未授权。请在单聊中发送 /codex bind <绑定口令>。")
            return

        if command.kind == CommandKind.HELP:
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
        elif command.kind == CommandKind.RUN:
            project = self._settings.projects.get(command.project_alias or "")
            if project is None:
                self.reply_async(message_id, "项目别名不在白名单中。发送 /codex projects 查看。")
                return
            try:
                job = self._jobs.submit(project, command.prompt or "", open_id, message_id)
                self.reply_async(message_id, f"任务已进入队列：{job.id} | {project.alias}")
            except RuntimeError as exc:
                self.reply_async(message_id, str(exc))

    def reply_async(self, message_id: str, text: str) -> None:
        self._outgoing.submit(self._reply_text, message_id, text)

    def _reply_text(self, message_id: str, text: str) -> None:
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
        response = self._api_client.im.v1.message.reply(request)
        if not response.success():
            LOG.error("Feishu reply failed: code=%s msg=%s", response.code, response.msg)

    def _mark_seen(self, message_id: str) -> bool:
        with self._seen_lock:
            if message_id in self._seen_messages:
                return False
            self._seen_messages.add(message_id)
            if len(self._seen_messages) > 5000:
                self._seen_messages.clear()
                self._seen_messages.add(message_id)
            return True


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

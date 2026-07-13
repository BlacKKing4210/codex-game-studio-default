from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class CommandKind(str, Enum):
    HELP = "help"
    BIND = "bind"
    PROJECTS = "projects"
    STATUS = "status"
    RUN = "run"
    CANCEL = "cancel"


@dataclass(frozen=True)
class Command:
    kind: CommandKind
    project_alias: str | None = None
    prompt: str | None = None
    argument: str | None = None


class CommandError(ValueError):
    pass


_BLOCKED_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bshutdown(?:\.exe)?\b|关机|重启(?:电脑|主机|系统)?", re.I), "系统关机或重启"),
    (re.compile(r"\bformat\s+[a-z]:|格式化(?:磁盘|硬盘|分区)", re.I), "磁盘格式化"),
    (re.compile(r"\brm\s+-rf\b|remove-item.{0,80}-recurse.{0,80}-force", re.I), "递归强制删除"),
    (re.compile(r"\bgit\s+(?:reset\s+--hard|clean\s+-[a-z]*f|push\s+--force)", re.I), "破坏性 Git 操作"),
    (re.compile(r"删除.{0,20}\.git|移除.{0,20}\.git", re.I), "删除 Git 元数据"),
    (re.compile(r"\b(?:publish|release|deploy)\b|正式发布|上架|推送到生产", re.I), "发布或部署"),
    (re.compile(r"feishu-command-gateway|allowed_open_ids|bootstrap_token|绕过.{0,20}(?:限制|白名单|安全)", re.I), "修改网关安全边界"),
)

_SECRET_ACTION = re.compile(r"\b(?:read|show|print|export|send|upload|extract|dump)\b|读取|显示|打印|导出|发送|发给|上传|提取", re.I)
_SECRET_TERM = re.compile(r"\b(?:secret|token|credential|password|api[_ -]?key)\b|密钥|口令|密码|凭证", re.I)


def parse_command(text: str) -> Command:
    normalized = text.strip()
    if not normalized.lower().startswith("/codex"):
        raise CommandError("命令必须以 /codex 开头。发送 /codex help 查看用法。")

    parts = normalized.split(maxsplit=3)
    if len(parts) == 1 or parts[1].lower() == "help":
        return Command(CommandKind.HELP)

    action = parts[1].lower()
    if action == "bind":
        if len(parts) < 3:
            raise CommandError("用法：/codex bind <绑定口令>")
        return Command(CommandKind.BIND, argument=parts[2])
    if action == "projects":
        return Command(CommandKind.PROJECTS)
    if action == "status":
        return Command(CommandKind.STATUS)
    if action == "cancel":
        if len(parts) < 3:
            raise CommandError("用法：/codex cancel <任务ID>")
        return Command(CommandKind.CANCEL, argument=parts[2])
    if action == "run":
        if len(parts) < 4:
            raise CommandError("用法：/codex run <项目别名> <任务说明>")
        alias = parts[2].lower()
        prompt = parts[3].strip()
        if not prompt:
            raise CommandError("任务说明不能为空。")
        risk = blocked_risk(prompt)
        if risk:
            raise CommandError(f"该远程任务被安全策略阻止：{risk}。请在本机 Codex 中执行。")
        return Command(CommandKind.RUN, project_alias=alias, prompt=prompt)
    raise CommandError(f"未知命令：{action}。发送 /codex help 查看用法。")


def blocked_risk(prompt: str) -> str | None:
    if _SECRET_ACTION.search(prompt) and _SECRET_TERM.search(prompt):
        return "凭证读取或外传"
    for pattern, reason in _BLOCKED_PATTERNS:
        if pattern.search(prompt):
            return reason
    return None


def help_text() -> str:
    return (
        "飞书 Codex 命令\n"
        "/codex bind <口令> - 首次单聊绑定\n"
        "/codex projects - 查看允许的项目\n"
        "/codex run <项目别名> <任务> - 启动任务\n"
        "/codex status - 查看队列\n"
        "/codex cancel <任务ID> - 取消任务\n"
        "远程任务固定在项目白名单和 workspace-write 沙箱内；关机、强删、强推、凭证读取和发布命令会被阻止。"
    )

from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path


class ConfigurationError(ValueError):
    pass


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int_env(name: str, default: int, minimum: int, maximum: int) -> int:
    value = os.getenv(name)
    parsed = default if value is None or not value.strip() else int(value)
    if not minimum <= parsed <= maximum:
        raise ConfigurationError(f"{name} must be between {minimum} and {maximum}")
    return parsed


@dataclass(frozen=True)
class Project:
    alias: str
    path: Path


@dataclass(frozen=True)
class Settings:
    root: Path
    app_id: str
    app_secret: str
    bootstrap_token: str
    allowed_open_ids: frozenset[str]
    allow_group: bool
    projects: dict[str, Project]
    codex_command: tuple[str, ...]
    sandbox: str
    timeout_seconds: int
    max_queue: int
    max_reply_chars: int
    log_level: str
    authorized_users_file: Path

    @classmethod
    def from_env(cls, root: Path) -> "Settings":
        root = root.resolve()
        app_id = os.getenv("FEISHU_APP_ID", "").strip()
        app_secret = os.getenv("FEISHU_APP_SECRET", "").strip()
        if not app_id or not app_secret:
            raise ConfigurationError("FEISHU_APP_ID and FEISHU_APP_SECRET are required")

        authorized_users_file = root / "state" / "authorized_users.json"
        allowed_open_ids = frozenset(
            value.strip()
            for value in os.getenv("FEISHU_ALLOWED_OPEN_IDS", "").split(",")
            if value.strip()
        )
        bootstrap_token = os.getenv("FEISHU_BOOTSTRAP_TOKEN", "").strip()
        if bootstrap_token == "change-me":
            raise ConfigurationError("FEISHU_BOOTSTRAP_TOKEN must be a generated secret")
        if not bootstrap_token and not allowed_open_ids and not _has_bound_users(authorized_users_file):
            raise ConfigurationError(
                "FEISHU_BOOTSTRAP_TOKEN is required until a user is bound or a static allowlist is configured"
            )

        projects_file = Path(os.getenv("CODEX_PROJECTS_FILE", "config/projects.json"))
        if not projects_file.is_absolute():
            projects_file = root / projects_file
        projects = _load_projects(projects_file)

        codex_command = _resolve_codex_command(root)
        sandbox = os.getenv("CODEX_SANDBOX", "workspace-write").strip()
        if sandbox not in {"read-only", "workspace-write"}:
            raise ConfigurationError("CODEX_SANDBOX must be read-only or workspace-write")

        return cls(
            root=root,
            app_id=app_id,
            app_secret=app_secret,
            bootstrap_token=bootstrap_token,
            allowed_open_ids=allowed_open_ids,
            allow_group=_bool_env("FEISHU_ALLOW_GROUP"),
            projects=projects,
            codex_command=codex_command,
            sandbox=sandbox,
            timeout_seconds=_int_env("CODEX_TIMEOUT_SECONDS", 3600, 30, 14400),
            max_queue=_int_env("CODEX_MAX_QUEUE", 10, 1, 100),
            max_reply_chars=_int_env("CODEX_MAX_REPLY_CHARS", 3500, 500, 10000),
            log_level=os.getenv("CODEX_LOG_LEVEL", "INFO").strip().upper(),
            authorized_users_file=authorized_users_file,
        )


def _has_bound_users(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    if not isinstance(data, dict):
        return False
    return any(str(value).strip() for value in data.get("open_ids", []))


def _load_projects(path: Path) -> dict[str, Project]:
    if not path.is_file():
        raise ConfigurationError(f"Project whitelist not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    raw_projects = data.get("projects")
    if not isinstance(raw_projects, dict) or not raw_projects:
        raise ConfigurationError("Project whitelist must contain a non-empty projects object")

    result: dict[str, Project] = {}
    for raw_alias, raw_path in raw_projects.items():
        alias = str(raw_alias).strip().lower()
        if not alias or not alias.replace("-", "").replace("_", "").isalnum():
            raise ConfigurationError(f"Invalid project alias: {raw_alias!r}")
        project_path = Path(str(raw_path)).expanduser()
        if not project_path.is_absolute():
            project_path = (path.parent / project_path).resolve()
        else:
            project_path = project_path.resolve()
        if not project_path.is_dir():
            raise ConfigurationError(f"Project path does not exist for {alias}: {project_path}")
        if not (project_path / ".git").exists():
            raise ConfigurationError(f"Project path is not a Git repository: {project_path}")
        result[alias] = Project(alias=alias, path=project_path)
    return result


def _resolve_codex_command(root: Path) -> tuple[str, ...]:
    configured = os.getenv("CODEX_EXECUTABLE", "").strip()
    candidate = Path(configured).expanduser() if configured else None
    if candidate and not candidate.is_absolute():
        candidate = (root / candidate).resolve()

    if candidate is not None and candidate.suffix.lower() in {".cmd", ".bat", ".ps1"}:
        raise ConfigurationError("CODEX_EXECUTABLE must point to a native executable, not a shell wrapper")
    if candidate is not None and not candidate.is_file():
        candidate = None

    if candidate is None:
        app_bin = Path(os.getenv("LOCALAPPDATA", "")) / "OpenAI" / "Codex" / "bin"
        matches = sorted(
            (path for path in app_bin.glob("*/codex.exe") if path.is_file() and path.stat().st_size > 0),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        candidate = matches[0] if matches else None

    if candidate is None:
        runtime = root / ".runtime" / "codex"
        matches = sorted(
            path for path in runtime.glob("node_modules/@openai/**/codex.exe")
            if path.is_file() and path.stat().st_size > 0
        )
        candidate = matches[0] if matches else None

    if candidate is None:
        located = shutil.which("codex")
        candidate = Path(located) if located else None

    if candidate is None or not candidate.is_file():
        raise ConfigurationError("Native Codex CLI executable was not found; run scripts/install.ps1")
    return (str(candidate.resolve()),)

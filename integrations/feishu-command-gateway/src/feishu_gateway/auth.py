from __future__ import annotations

import hmac
import json
import threading
from pathlib import Path


class AuthorizedUsers:
    def __init__(self, state_file: Path, static_ids: frozenset[str], bootstrap_token: str):
        self._state_file = state_file
        self._static_ids = static_ids
        self._bootstrap_token = bootstrap_token
        self._lock = threading.Lock()
        self._bound_ids = self._load()

    def is_authorized(self, open_id: str) -> bool:
        with self._lock:
            return open_id in self._static_ids or open_id in self._bound_ids

    def bind(self, open_id: str, supplied_token: str, is_private_chat: bool) -> tuple[bool, str]:
        if not is_private_chat:
            return False, "绑定只能在与机器人的单聊中进行。"
        if not hmac.compare_digest(supplied_token, self._bootstrap_token):
            return False, "绑定口令无效。"
        with self._lock:
            if self._bound_ids and open_id not in self._bound_ids:
                return False, "已有用户完成绑定；新增用户请在本机配置白名单。"
            self._bound_ids.add(open_id)
            self._save()
        return True, "绑定成功。请立即从 .env 中删除或更换 FEISHU_BOOTSTRAP_TOKEN。"

    def _load(self) -> set[str]:
        if not self._state_file.is_file():
            return set()
        data = json.loads(self._state_file.read_text(encoding="utf-8"))
        return {str(value) for value in data.get("open_ids", []) if str(value).strip()}

    def _save(self) -> None:
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._state_file.with_suffix(".tmp")
        temporary.write_text(
            json.dumps({"open_ids": sorted(self._bound_ids)}, ensure_ascii=True, indent=2),
            encoding="utf-8",
        )
        temporary.replace(self._state_file)

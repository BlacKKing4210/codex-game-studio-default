from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from feishu_gateway.auth import AuthorizedUsers


class AuthorizedUsersTests(unittest.TestCase):
    def test_bind_requires_private_chat_and_correct_token(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "users.json"
            users = AuthorizedUsers(state, frozenset(), "secret-token")
            self.assertFalse(users.bind("ou_1", "secret-token", False)[0])
            self.assertFalse(users.bind("ou_1", "wrong", True)[0])
            self.assertTrue(users.bind("ou_1", "secret-token", True)[0])
            self.assertTrue(users.is_authorized("ou_1"))
            self.assertFalse(users.bind("ou_2", "secret-token", True)[0])

    def test_bind_is_disabled_without_bootstrap_token(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "users.json"
            users = AuthorizedUsers(state, frozenset({"ou_admin"}), "")
            success, message = users.bind("ou_1", "anything", True)
            self.assertFalse(success)
            self.assertIn("关闭", message)


if __name__ == "__main__":
    unittest.main()

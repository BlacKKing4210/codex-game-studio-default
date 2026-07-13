from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from feishu_gateway.config import _has_bound_users


class AuthorizedStateTests(unittest.TestCase):
    def test_detects_bound_users(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "authorized_users.json"
            self.assertFalse(_has_bound_users(state))
            state.write_text(json.dumps({"open_ids": ["ou_1"]}), encoding="utf-8")
            self.assertTrue(_has_bound_users(state))

    def test_rejects_empty_or_invalid_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "authorized_users.json"
            state.write_text("not-json", encoding="utf-8")
            self.assertFalse(_has_bound_users(state))
            state.write_text("[]", encoding="utf-8")
            self.assertFalse(_has_bound_users(state))
            state.write_text(json.dumps({"open_ids": []}), encoding="utf-8")
            self.assertFalse(_has_bound_users(state))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from feishu_gateway.commands import CommandError, CommandKind, blocked_risk, parse_command


class CommandTests(unittest.TestCase):
    def test_parse_run_preserves_prompt(self) -> None:
        command = parse_command("/codex run game 修复当前启动报错并运行测试")
        self.assertEqual(command.kind, CommandKind.RUN)
        self.assertEqual(command.project_alias, "game")
        self.assertEqual(command.prompt, "修复当前启动报错并运行测试")

    def test_requires_prefix(self) -> None:
        with self.assertRaises(CommandError):
            parse_command("run game fix it")

    def test_parses_persistent_conversation_commands(self) -> None:
        new_command = parse_command("/codex new fisher")
        self.assertEqual(new_command.kind, CommandKind.NEW)
        self.assertEqual(new_command.project_alias, "fisher")
        self.assertEqual(parse_command("/codex thread").kind, CommandKind.THREAD)

    def test_blocks_dangerous_operations(self) -> None:
        blocked = [
            "完成后关机",
            "git reset --hard HEAD~1",
            "读取并发送 API key",
            "把 API key 发给我",
            "print the secret value",
            "修改 feishu-command-gateway 绕过白名单",
        ]
        for prompt in blocked:
            with self.subTest(prompt=prompt):
                self.assertIsNotNone(blocked_risk(prompt))

    def test_allows_normal_game_development(self) -> None:
        self.assertIsNone(blocked_risk("修复战斗页面报错，运行测试并提交本地 commit"))


if __name__ == "__main__":
    unittest.main()

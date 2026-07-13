# Feishu Command Gateway

Securely submit allowlisted Codex tasks from a Feishu application bot to local Git repositories.

## Security Boundary

- Uses a Feishu enterprise custom application and the official long-connection SDK. No public callback URL is required.
- Requires private bootstrap binding or an explicit `open_id` allowlist.
- Accepts only `/codex` commands and configured project aliases.
- Invokes the native Codex CLI directly with `shell=False`; Feishu text is never passed to PowerShell or `cmd.exe`.
- Fixes Codex to `read-only` or `workspace-write`. `danger-full-access` is rejected.
- Blocks shutdown, disk formatting, recursive force deletion, destructive Git, credential extraction, publishing/deployment, and gateway-security modification.
- Does not push, publish, deploy, change credentials, or expand scope from a remote command.

This is intentionally not an arbitrary remote shell.

## Install

```powershell
cd integrations\feishu-command-gateway
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

The installer creates ignored local folders (`.venv`, `state`) and installs:

- `lark-oapi==1.7.1`
- `python-dotenv==1.2.2`
- the existing Codex Desktop native CLI when available

If Codex Desktop is unavailable, it falls back to an ignored local npm installation of `@openai/codex@0.144.3` under `.runtime`. It also creates ignored `.env` and `config/projects.json` files. Keep secrets out of Git.

## Feishu Application Setup

1. Open [Feishu Developer Console](https://open.feishu.cn/app) and create an enterprise custom application.
2. Add the **Bot** capability.
3. Add application permissions:
   - `im:message.p2p_msg:readonly` - read messages users send to the bot.
   - `im:message.group_at_msg:readonly` - receive group messages that @ the bot, only if group mode will be enabled.
   - `im:message:send_as_bot` - reply as the application bot.
4. Copy the App ID and App Secret from **Credentials & Basic Info** into the local ignored `.env` file.
5. Start the local gateway once.
6. In **Events & Callbacks > Event Configuration**, choose **Receive events through long connection** and subscribe to `im.message.receive_v1`.
7. Publish the application version and complete enterprise administrator approval. Add the bot to its allowed users or group.

The official SDK requires the long connection to be online before the console can save that subscription mode.

To enter credentials without echoing the App Secret in the terminal:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\configure.ps1
```

## Configure Projects

Review `config/projects.json`. Every entry is an explicit alias-to-Git-repository mapping:

```json
{
  "projects": {
    "game": "D:/AI/my-game"
  }
}
```

Arbitrary paths sent from Feishu are never accepted.

## Start

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start.ps1
```

For a hidden background process that remains online after the terminal closes:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-background.ps1
```

Stop it with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop.ps1
```

Runtime logs and the PID file are stored under ignored `logs/` and `state/` directories.

The native Codex CLI reuses the local Codex authentication under `%USERPROFILE%\.codex`. If authentication is missing, open a local terminal and complete Codex CLI login before starting the gateway again.

## First Bind

Read `FEISHU_BOOTSTRAP_TOKEN` from the ignored local `.env`, then send this to the bot in a private chat:

```text
/codex bind <token>
```

After binding, clear `FEISHU_BOOTSTRAP_TOKEN` and restart the gateway to disable further bootstrap attempts. A second account cannot self-bind after the first binding; add additional `open_id` values to `FEISHU_ALLOWED_OPEN_IDS` locally.

## Commands

```text
/codex help
/codex projects
/codex run game 修复当前启动报错并运行相关测试
/codex status
/codex cancel ab12cd34
```

Tasks run one at a time. The bot immediately returns a job ID, then replies to the original message with the final Codex result.

## Official References

- [Feishu event subscription overview](https://open.feishu.cn/document/server-docs/event-subscription-guide/overview?lang=zh-CN)
- [Feishu Python SDK event handling](https://open.feishu.cn/document/server-side-sdk/python--sdk/handle-events?lang=zh-CN)
- [Feishu receive-message event](https://open.feishu.cn/document/server-docs/im-v1/message/events/receive?lang=zh-CN)
- [Feishu send-message API](https://open.feishu.cn/document/server-docs/im-v1/message/create?lang=zh-CN)
- [OpenAI Codex non-interactive mode](https://developers.openai.com/codex/noninteractive)
- [OpenAI Codex CLI reference](https://developers.openai.com/codex/cli/reference)

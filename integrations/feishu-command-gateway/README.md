# Feishu Codex Conversation Bridge

Map an authorized Feishu chat to a persistent local Codex task. Plain Feishu text becomes a real user turn in that task, Codex replies in the same thread, and the task appears as an independent conversation in Codex Desktop. User turns and final replies created from Codex Desktop are also mirrored back to the bound Feishu chat.

## Conversation Model

- The first plain-text message creates a non-ephemeral Codex thread in the default allowlisted project.
- Later messages from the same Feishu chat resume the same thread and retain full Codex context.
- `/codex new [project]` switches the Feishu chat to a fresh task slot. The old Codex task is preserved.
- `/codex run <project> <message>` creates a fresh task and sends its first message.
- Thread mappings persist in ignored `state/conversation_threads.json`, so gateway restarts do not lose the current task.
- A read-only App Server client polls the mapped task with `thread/read(includeTurns=true)` every two seconds by default.
- Gateway turns carry a `feishu:<message-id>` source ID, so the monitor does not echo messages that are already visible in Feishu.
- Desktop-origin user turns are labeled `来自 Codex Desktop` and include one `Thinking` status followed by the final reply. Internal commentary is not forwarded.
- Synchronization state persists in ignored `state/thread_sync.json`. On the first upgraded start, older history is baselined and only the configured number of recent Desktop turns is backfilled (one by default), avoiding a flood of old messages.
- Outbound messages first enter ignored `state/delivery_outbox.json`, then retry with stable Feishu delivery IDs until accepted. Received Feishu event IDs persist in `state/received_messages.json` to prevent duplicate turns after reconnects.
- Every new thread is named `飞书 | <project> | <first-message>` and is visible in Codex Desktop.

The bridge uses the official Codex App Server JSON-RPC protocol (`thread/start`, `thread/resume`, `turn/start`, `thread/read`) rather than ephemeral `codex exec` jobs.

The reverse mirror reads semantic per-turn history and uses each user message's `clientId` to distinguish Desktop turns from Feishu turns, including when both are running concurrently. It forwards only the Desktop user text, one processing state, and the final answer; reasoning, tool calls, developer instructions, environment context, and commentary are never forwarded. Queue acknowledgements remain Feishu-only operational messages, and long replies are durably split into numbered messages without truncating the Codex response.

## Security Boundary

- Uses a Feishu enterprise custom application and the official long-connection SDK. No public callback URL is required.
- Requires private bootstrap binding or an explicit `open_id` allowlist.
- Accepts only configured project aliases and invokes the native Codex executable with `shell=False`.
- Fixes Codex to `read-only` or `workspace-write`; `danger-full-access` is rejected.
- Uses `approvalPolicy: never`. The remote bridge declines interactive permission requests.
- Blocks shutdown, disk formatting, recursive force deletion, destructive Git, credential extraction, publishing/deployment, and gateway-security modification.
- Does not push, publish, deploy, change credentials, or expand scope from a remote message.

This is a persistent Codex client, not an arbitrary remote shell.

## Install

```powershell
cd integrations\feishu-command-gateway
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

The installer creates ignored local folders (`.venv`, `state`, `logs`) and installs the Feishu SDK. It reuses the native Codex executable and authentication from Codex Desktop.

## Feishu Application Setup

1. Create an enterprise custom application in [Feishu Developer Console](https://open.feishu.cn/app).
2. Add the **Bot** capability.
3. Grant `im:message.p2p_msg:readonly` and `im:message:send_as_bot`. Add `im:message.group_at_msg:readonly` only when group mode is enabled.
4. Put the App ID and App Secret in ignored `.env` through `scripts/configure.ps1`.
5. Start the gateway once, select **Receive events through long connection**, and subscribe to `im.message.receive_v1`.
6. Publish the application version and complete administrator approval.

## Configure Projects

Review ignored `config/projects.json`:

```json
{
  "projects": {
    "studio": "D:/AI/my-game-studio",
    "game": "D:/AI/my-game"
  }
}
```

Set `CODEX_DEFAULT_PROJECT=studio` in `.env` when the desired default is not the `studio` alias. Arbitrary paths from Feishu are never accepted.

Optional synchronization tuning in `.env`:

```text
CODEX_SYNC_INTERVAL_SECONDS=2
CODEX_SYNC_BACKFILL_TURNS=1
```

The interval accepts 1-60 seconds. Backfill accepts 0-50 turns and applies only when a mapped task is first added to the synchronization ledger.

## Start And Stop

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-background.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\stop.ps1
```

Runtime logs and the PID file are stored under ignored `logs/` and `state/` directories.

## First Bind

Send this in a private chat, then clear `FEISHU_BOOTSTRAP_TOKEN` and restart the gateway:

```text
/codex bind <token>
```

## Usage

```text
修复当前项目的启动报错并运行测试
/codex thread
/codex new fisher
继续检查钓鱼结算页面
/codex projects
/codex run studio 更新通用开发流程文档
/codex status
/codex cancel ab12cd34
```

Feishu-submitted messages run one at a time. The bot first acknowledges that the message is queued; when execution actually begins it sends one `🤔 Thinking…` status and then the exact final answer. Desktop-origin messages normally appear in Feishu within the configured sync interval.

## Official References

- [OpenAI Codex App Server](https://learn.chatgpt.com/docs/app-server)
- [Feishu event subscription overview](https://open.feishu.cn/document/server-docs/event-subscription-guide/overview?lang=zh-CN)
- [Feishu Python SDK event handling](https://open.feishu.cn/document/server-side-sdk/python--sdk/handle-events?lang=zh-CN)
- [Feishu receive-message event](https://open.feishu.cn/document/server-docs/im-v1/message/events/receive?lang=zh-CN)
- [Feishu send-message API](https://open.feishu.cn/document/server-docs/im-v1/message/create?lang=zh-CN)

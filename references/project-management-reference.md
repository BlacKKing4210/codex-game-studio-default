# Project Management Reference

Use this reference when a game project needs scheduled task monitoring, automatic task continuation, parallel Codex threads, or a persistent task plan.

## Ownership

- Producer owns scope, priority, milestones, ship/iterate/pivot decisions, and final delivery direction.
- Project Manager owns task-plan accuracy, dependency scheduling, thread lifecycle, interruption recovery, and execution tracking.
- Technical Director and Lead Programmer own module boundaries and conflict scopes for development tasks.
- QA Lead owns acceptance evidence and readiness verdicts.
- The user remains the final authority for design changes, scope changes, permissions, publishing, merges, and releases.

## Canonical Task Plan

Keep one canonical table at `production/task-plan.md` or the project equivalent. Every executable task must have:

- Stable Task ID.
- Milestone and priority.
- Module and conflict scope.
- Owner route.
- Dependencies.
- Status.
- Thread ID and execution environment when started.
- Acceptance criteria and verification command/path.
- Last check, next retry, retry count, and blocker.
- Result commit or artifact handoff.

Use these statuses:

- `Backlog`: captured but not approved for automatic execution.
- `Not Started`: approved; start automatically when dependencies and conflict checks pass.
- `Starting`: thread creation is in progress; do not create another thread.
- `In Progress`: linked thread is actively working.
- `Interrupted`: execution stopped unexpectedly and may be resumed.
- `Blocked`: a dependency, permission, user decision, or external condition prevents progress.
- `Review`: implementation finished and awaits QA, integration, or user review.
- `Done`: acceptance and integration are complete.
- `Cancelled`: explicitly removed from execution.

## Thirty-Minute Inspection

For each scheduled inspection:

1. Read the canonical task plan before inspecting threads.
2. Reconcile every `Starting`, `In Progress`, and `Interrupted` row with its recorded thread.
3. If a thread is still running, update `Last Check` only.
4. If a thread stopped because of quota, timeout, tool failure, host restart, network failure, or another recoverable interruption, set `Interrupted`, preserve the blocker, and continue the same thread when retry is allowed.
5. If a thread needs user input, credentials, approval, a design decision, or an external state change, set `Blocked` and do not loop prompts.
6. If work is complete, record its commit/artifacts and move it to `Review`; mark `Done` only after acceptance and integration are confirmed.
7. Find every `Not Started` task whose dependencies are `Done`, whose required design/user-review gates are satisfied, and whose conflict scope does not overlap active work.
8. Set the row to `Starting` before creating a thread, then create one new isolated thread for that Task ID and record its thread ID immediately.
9. If thread creation fails, return the row to `Interrupted` or `Blocked` with the exact reason and retry time.
10. Write a concise inspection summary: continued, started, completed, blocked, and unchanged tasks.

## New Thread Contract

Every new task thread prompt must include:

- Project and Task ID.
- Goal and approved design/spec references.
- Module boundary and files/conflict scope.
- Dependencies already satisfied.
- Acceptance criteria and verification.
- Required artifacts or commit handoff.
- Instruction to preserve unrelated user changes.
- Instruction not to push, merge, publish, or broaden scope without authority.

Prefer a separate worktree for implementation tasks so concurrent threads do not edit the same checkout. Record the worktree/branch and require a focused commit or artifact handoff for later integration.

## Interruption Recovery

- Resume the existing thread first with a short continuation prompt containing the Task ID, remaining work, last verified state, and blocker status.
- Do not claim quota recovery until the platform accepts work again.
- Use `Next Retry` to avoid rapid retries. The default scheduled interval is 30 minutes.
- After three consecutive failures with the same blocker, keep the task `Blocked` and report the repeated cause instead of generating more threads.
- If the original thread is missing or irrecoverable, create a replacement only after recording the old thread ID, reason, and latest durable commit/artifact.

## Duplicate And Conflict Prevention

- Task ID is the idempotency key.
- A non-empty active Thread ID prevents new-thread creation for that task.
- Set `Starting` before the create-thread operation.
- Do not run tasks in parallel when their conflict scopes overlap or one depends on the other's unintegrated output.
- Isolated worktrees reduce checkout collisions but do not eliminate merge conflicts; integration remains an explicit review step.
- Never auto-merge conflicting work or overwrite user-edited files.

## Automation Boundary

The recurring automation is an orchestration mechanism, not an unlimited worker. It cannot bypass account quotas, permissions, authentication, unavailable tools, or user-review gates. It may retry recoverable interruptions and start approved eligible tasks, while preserving exact blockers for the next inspection.

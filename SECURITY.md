# Security Policy

## Supported Scope

This repository provides Codex Skill instructions, agent/workflow catalogs, and game-development process documentation.

Security-sensitive areas include:

- Git and GitHub workflows.
- Reverse-engineering guidance.
- Local paths, tool configuration, and MCP references.
- Game project secrets such as `.env`, API keys, keystores, signing keys, private builds, or credentials.

## Rules

- Never commit `.env`, tokens, signing keys, local credentials, private certificates, caches, dependency folders, or build outputs.
- Never force-push or rewrite history by default.
- Never delete `.git` automatically.
- Never use reverse engineering to bypass DRM, anti-cheat, account systems, payment logic, online protections, or to extract proprietary commercial assets/code for reuse.
- Treat user-edited CSV and source files as source of truth.

## Reporting

Open a private security report or contact the repository owner if you find:

- Secret exposure.
- Unsafe Git automation.
- Reverse-engineering instructions that could enable bypass or abuse.
- A workflow that could overwrite user work.

## Maintainer Response

Security fixes should prioritize:

1. Removing or neutralizing risky instructions.
2. Adding explicit guardrails.
3. Updating examples and tests so the unsafe pattern does not reappear.

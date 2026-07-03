# Upgrading

Use this guide when updating an installed copy of `codex-game-studio-default`.

## Before Updating

1. Check local changes:

   ```powershell
   git status --short
   ```

2. Back up or commit any local customizations.
3. Review changes to `SKILL.md`, `AGENTS.md`, `references/`, and `agents/openai.yaml` before replacing files.

## Safe To Replace

Usually safe to replace when you have not customized them:

- `docs/`
- `Codex Game Studio Framework/`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `UPGRADING.md`

## Merge Carefully

Merge these by hand if customized:

- `SKILL.md`
- `AGENTS.md`
- `agents/openai.yaml`
- `agents/*.md`
- `references/*.md`

## Migration Notes

- Keep `SKILL.md` concise. Move detailed behavior into `references/`.
- Keep project-specific local paths in `AGENTS.md` or project instructions, not in generic docs unless they are intentional defaults.
- If you add new roles, update both [docs/AGENT-CATALOG.md](docs/AGENT-CATALOG.md) and [Codex Game Studio Framework/catalog.yaml](Codex%20Game%20Studio%20Framework/catalog.yaml).

## Validation

After updating:

```powershell
git status --short
```

Then run the Codex skill validator if available:

```powershell
python C:\Users\76398\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

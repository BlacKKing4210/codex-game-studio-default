# Contributing

Thanks for improving Codex Game Studio Default.

## Principles

- Keep Codex usage first: root `SKILL.md` should stay concise and reference deeper files only when needed.
- Keep game development defaults practical for solo and small-team projects.
- Prefer Godot 4, GDScript, CSV data config, procedural motion, and explicit QA checks unless a change is intentionally engine-agnostic.
- Do not add copyrighted commercial game content, exact UI clones, proprietary item lists, or protected assets.
- Treat reference projects as inspiration and attribution, not as material to copy blindly.

## Change Checklist

- Update `SKILL.md` only when Codex needs the behavior at trigger time.
- Put detailed guidance in `references/` or `docs/`.
- Update [docs/AGENT-CATALOG.md](docs/AGENT-CATALOG.md) when adding or changing roles.
- Update [Codex Game Studio Framework/catalog.yaml](Codex%20Game%20Studio%20Framework/catalog.yaml) when adding workflows or agent specs.
- Validate frontmatter in `SKILL.md`.
- Run relevant smoke checks before committing.

## Pull Request Shape

Include:

- What changed.
- Which workflow or agent is affected.
- How you verified it.
- Any compatibility or migration notes.

## Style

- Use clear Markdown.
- Prefer ASCII unless a file already uses multilingual trigger terms.
- Keep examples short and actionable.
- Avoid broad automation that conflicts with user control.

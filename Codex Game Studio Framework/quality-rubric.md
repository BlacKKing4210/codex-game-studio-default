# Quality Rubric

Use this rubric when reviewing changes to the Codex Game Studio workflow.

## Skill Runtime

- `SKILL.md` has valid frontmatter.
- Description contains real trigger contexts.
- Body stays concise and routes to references for detail.
- References are loaded only when needed.

## Agent Catalog

- Each agent owns a clear domain.
- Agents do not claim cross-domain authority.
- Routes include QA for user-facing work.
- Specialist additions have a clear need.

## Game Development Defaults

- 2D-first is the default rendering/production model unless project context explicitly chooses 3D, 2.5D, VR/AR, or another model.
- Godot 4 and GDScript remain the default unless project context says otherwise.
- CSV remains default for designer-editable content.
- Professional art work routes through Art Director plus the relevant art specialist before Sprite Forge, UI implementation, or engine handoff.
- 2D work includes sprite specs, animation specs, atlas/import settings, TileMap/layer rules, y-sort, collision, and target-resolution checks.
- Procedural motion is preferred before new sequence-frame art for common feedback.
- Sprite Forge outputs include QC and Godot handoff notes.
- UI work uses the brawler arcade UI kit without copying proprietary assets.

## Safety

- Commercial games are used only as design references.
- Reverse engineering is authorization-gated and excludes bypass/extraction abuse.
- Git automation avoids force-push, history rewrite, secret commits, and `.git` deletion.

## Documentation

- README explains what the repo does.
- AGENTS.md matches SKILL.md.
- Catalog and docs agree on agent names and routes.
- Migration notes exist for breaking workflow changes.

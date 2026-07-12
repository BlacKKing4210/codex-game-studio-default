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
- Concept and System Design include player feedback discovery, feedback synthesis, or a clear feedback plan with testable assumptions.
- System Designer owns feature-level Word design specs, page UE requirements, transition maps, per-page explanations, data-source maps, implementation follow-through, acceptance criteria, and user revision alignment.
- Numerical Designer is the current name for numeric, economy, formulas, reward values, progression curves, and tuning work.
- Every production feature has an independent Word `.docx` design document, per-page Figma/FigJam UE diagrams, written transition map, per-page explanation, data-source map, acceptance checklist, and user review status before implementation.
- Demo and prototype work uses emoji placeholders first, then simple original SVG placeholders for missing visual resources that emoji cannot represent clearly.
- Art-related agents use master-level visual design references as principle studies, with explicit anti-copying constraints.
- 2D visual direction defaults to simple premium design: readable in seconds, controlled shape/color/UI systems, reusable production pieces, and no added complexity unless it improves gameplay, emotion, or reward.
- Famous-company references such as Nintendo, Supercell, Ubisoft/Rayman, Blizzard/Hearthstone, King, SEGA, and Capcom are decomposed into design principles, not copied as surface style.
- Professional art work routes through Art Director plus the relevant art specialist before Sprite Forge, UI implementation, or engine handoff.
- 2D work includes sprite specs, animation specs, atlas/import settings, TileMap/layer rules, y-sort, collision, and target-resolution checks.
- Procedural motion is preferred before new sequence-frame art for common feedback.
- Sprite Forge outputs include QC and Godot handoff notes.
- UI work uses the brawler arcade UI kit without copying proprietary assets.
- UI效果图/Figma implementation uses the UI Programmer's `ui-ux-pro-max` adaptation: design tokens, component state matrix, reusable controls, responsive/safe-area layout, accessibility/contrast checks, motion rules, and screenshot parity review.
- Production UI uses SVG/icons or approved UI assets; emoji is limited to temporary demo/prototype placeholders unless deliberately chosen as final UI identity.
- Placeholder SVGs are marked temporary, original, simple, and not copied from commercial icons, logos, characters, or UI marks.

## Safety

- Commercial games are used only as design references.
- Reverse engineering is authorization-gated and excludes bypass/extraction abuse.
- Git automation avoids force-push, history rewrite, secret commits, and `.git` deletion.

## Documentation

- README explains what the repo does.
- AGENTS.md matches SKILL.md.
- Catalog and docs agree on agent names and routes.
- Formal design docs require Word feature specs plus Figma/FigJam source links or `.fig` source references for every page UE diagram.
- User-reviewed Word/Figma edits are treated as the source of truth, and substantial changes route back through System Designer before implementation continues.
- Migration notes exist for breaking workflow changes.

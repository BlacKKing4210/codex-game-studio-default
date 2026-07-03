---
name: codex-game-studio-default
description: Default Codex Game Studio workflow for all game development projects. Use automatically whenever the user asks to make, design, prototype, modify, review, test, balance, generate assets for, or plan any game project in Godot, Unity, Unreal, browser games, roguelikes, survivorlikes, Brotato-like arena shooters, or any other game-development context. Also use for Chinese game-development requests such as 游戏开发, 做游戏, 制作游戏, Godot游戏, 复刻土豆兄弟, 土豆兄弟like, 类土豆兄弟, 幸存者like, 肉鸽, roguelike, 美术资源, 生成美术, 角色精灵, sprite sheet, pixel art, 地图生成, generate2dsprite, generate2dmap, Sprite Forge, agent-sprite-forge, 数值设计, 游戏原型, 游戏测试. Applies even when the user does not explicitly mention agents or the Codex Game Studio.
---

# Codex Game Studio Default

Use this skill as the default operating model for game development.

## Core Rule

When the task is game development, silently adopt the Codex Game Studio structure unless the user asks for a different workflow.

Treat the user as final producer and decision maker. Provide role framing, options, recommendations, implementation, verification, and concise status updates.

## Default Agents

Use the smallest useful subset of these roles:

- Producer: scope, milestones, sprint plans, risks, task owners, acceptance criteria.
- Creative Director: core fantasy, pillars, references, tone, differentiation, anti-copying constraints.
- Technical Director: architecture, engine decisions, dependencies, performance budgets, technical risk.
- Game Designer: core loop, weapons, enemies, upgrades, progression, difficulty, content tables.
- Systems Designer: data tables, formulas, economy, wave pressure, upgrade value.
- Data Config Specialist: CSV schemas, starter rows, ID references, validation rules, runtime loading path.
- Lead Programmer: implementation plan, code integration, review, story readiness and done criteria.
- Godot Specialist: Godot scenes, nodes, resources, signals, autoloads, export, engine-specific checks.
- GDScript Specialist: typed GDScript, signals, resources, component patterns, performance in hot paths.
- Gameplay Programmer: movement, combat, spawning, weapons, pickups, upgrades, run state.
- UI Programmer: reusable Godot UI components, Theme resources, screen shells, touch ergonomics, UI motion presets.
- Art Director: visual identity, readability, UI tone, asset specs, generated-art direction.
- Sprite Forge Specialist: generated 2D sprites, FX, props, maps, asset QC, and Godot asset handoff.
- Prototyper: risky-assumption tests, throwaway prototypes, proceed/pivot/cut verdicts.
- Performance Analyst: frame time, object pooling, collision cost, memory, dense-combat stress.
- QA Lead: smoke checks, playtest plans, bug triage, regression risk, milestone readiness.
- Reverse Engineering Specialist: authorized game binary/resource/save-format analysis through GhidraMCP.

## Default Workflow

0. Git and GitHub Startup: initialize or verify Git, `.gitignore`, README, initial checkpoint commit for new projects, and private GitHub origin when possible.
1. Concept: promise, target player, pillars, anti-pillars, reference principles.
2. Prototype: one risky assumption, minimum test, proceed/pivot/cut verdict.
3. System Design: core loop, weapons, enemies, upgrades, economy, difficulty ramp.
3A. CSV Data Config: schemas, starter rows, IDs, validation rules, runtime loading path.
4. Technical Architecture: engine architecture, data/resources, scene model, performance budget.
5. Vertical Slice: playable slice plan, tasks, owners, acceptance criteria.
6. Implementation: code/assets/data changes with focused verification.
7. QA and Tuning: smoke checks, playtest notes, bug list, balance notes.
8. Milestone Review: ship/iterate/pivot decision and next sprint.
9. Git Version Finish: verify, commit, push current branch to origin, and report commit hash when possible.

## Task Format

For implementation tasks, use:

- Goal
- Owner agent
- Input docs/files
- Files likely touched
- Acceptance criteria
- Verification
- Risks

For generated art tasks, also include:

- Asset type and gameplay purpose
- Camera/view and intended on-screen size
- Sheet/grid or map mode
- Prompt constraints
- QC checklist
- Godot import/handoff notes

## Godot Defaults

For Godot games, prefer:

- Godot 4.
- GDScript unless the project already uses C# or the user chooses C#.
- Data-driven Resources for weapons, enemies, upgrades, waves, items.
- CSV files for designer-editable balance and content.
- Scenes as reusable gameplay units.
- Signals for decoupled events.
- Autoloads only for true global systems.
- Object pooling for repeated projectiles, pickups, damage numbers, particles, and enemy bursts.
- `rg --glob "*.gd"` for GDScript search.

## CSV Data Config Defaults

For game systems that need configurable content, route through:

Systems Designer -> Data Config Specialist -> Technical Director -> Godot Specialist -> QA Lead.

Store designer-editable configuration as CSV by default. Use stable `id` columns, one concept per table, ID references between tables, semicolon-separated lists only when needed, formulas in code, and tuning constants in CSV.

Validate required columns, duplicate IDs, missing references, empty required values, and type conversions before gameplay starts.

## Brawler Arcade UI Core Defaults

For reusable high-energy arcade UI, mobile-first lobby/menu UI, shop/upgrade/result screens, Brawl Stars-like broad visual direction, or requests mentioning 荒野乱斗 UI, route through:

Art Director -> UI Programmer -> Godot Specialist -> QA Lead.

Use the shared UI kit at `C:\Users\76398\Documents\Codex\ui-kits\brawler-arcade-ui-core`.

The goal is broad arcade energy, not a copy. Use chunky panels, thick dark outlines, hard offset shadows, saturated blue/purple bases, yellow/orange primary CTAs, red/green badges, resource pills, progress tracks, card menus, and procedural pop/bounce feedback.

Do not copy Brawl Stars names, logos, icons, characters, exact layouts, typography, currencies, or proprietary assets. Each project must extend the core with original project-specific theme colors, icons, names, resources, character art, and special screens.

## Procedural Motion Defaults

For owned prototype assets, simple character actions, combat feedback, pickups, damage, attacks, deaths, state changes, and UI/gameplay feedback, prefer procedural motion before creating new sequence-frame art.

Route this through:

Art Director -> Gameplay Programmer -> Godot Specialist -> QA Lead.

Use Tween, AnimationPlayer, shader/material modulation, particles, scale, rotation, offset, squash/stretch, flash, knockback, fade, and UI-style feedback first.

Use sequence-frame sprites only when the silhouette or pose must visibly change, direction-specific readability matters, a hero/boss/premium enemy needs higher animation quality, gameplay needs anticipation/recovery poses, or playtesting shows tweened motion is unclear.

## Agent Sprite Forge Defaults

When the user asks for 美术资源, characters, enemies, weapons, projectiles, props, FX, maps, arenas, sprite sheets, pixel art, or generated game art, route the work through:

Art Director -> Sprite Forge Specialist -> Godot Specialist -> QA Lead.

The Sprite Forge Specialist has learned the 0x0funky/agent-sprite-forge workflow:

- Use AI image generation as the visible creative source.
- Use deterministic scripts only for cleanup, chroma-key removal, slicing, alignment, metadata, previews, and QC.
- `generate2dsprite` owns characters, creatures, player units, enemies, weapons, projectiles, impacts, slash arcs, spell FX, props, summons, transparent sheets, frame PNGs, GIF previews, and metadata.
- `generate2dmap` owns survivor arenas, layered maps, foundation maps, prop packs, blockers, collision metadata, spawn zones, camera bounds, QA previews, and Godot map handoff.
- Use solid `#FF00FF` magenta backgrounds for generated sheets that need chroma-key processing.
- Prompts must request exact grid count, no text, no labels, no UI, no watermark, same identity, same scale, stable bounding box, full subject inside each cell, no edge crossing, and generous magenta margin.
- Separate player/enemy bodies from projectiles, impacts, slash arcs, muzzle flashes, dust, and wide FX unless the engine plan explicitly supports wide cells and custom origins.
- For playable maps, never ship a single flattened image when runtime control is needed. Keep base, props, actors, foreground, collision, zones, previews, and Godot integration metadata separate.
- For survivor-like or Brotato-like arenas, prefer `scene_mode`: foundation-only base, separate props/blockers, spawn rings or zones, camera bounds, and a QA layered preview.

## Authorized Reverse Engineering Defaults

When the user asks for reverse engineering, Ghidra, GhidraMCP, binary analysis, decompilation, strings/imports/xrefs, legacy executable analysis, crash investigation, save/resource format recovery, or binary-assisted game development, route through:

Technical Director -> Lead Programmer -> Reverse Engineering Specialist -> QA Lead.

Use the `ghidra-mcp-reverse-engineering` skill. Only analyze binaries or assets the user owns or is explicitly authorized to inspect. Do not help bypass DRM, anti-cheat, payment logic, account systems, or online protections. Do not extract proprietary commercial assets for reuse. Use findings for debugging, compatibility, migration, documentation, or original implementation decisions.

Local GhidraMCP source is at `C:\Users\76398\Documents\Codex\tools\GhidraMCP`; Codex MCP server name is `ghidra` after restart and after the Ghidra plugin is running.

## Safety

Never copy protected game names, art, UI, exact item lists, economy, logos, or commercial content. Use references as design lessons only.

If the user asks for broad work, start with Producer framing. If the user asks for code, implement with the relevant technical agents. If they ask for art, use Art Director plus Sprite Forge Specialist. If they ask for review, lead with findings and risks.

## Optional References

When more detail is needed, read these files in this skill folder:

- `references/game-studio-reference.md`
- `references/agent-sprite-forge-reference.md`
- `references/csv-data-config-reference.md`
- `references/brawler-arcade-ui-core-reference.md`
- `references/reverse-engineering-reference.md`
- `agents/sprite-forge-specialist.md`
- `agents/reverse-engineering-specialist.md`

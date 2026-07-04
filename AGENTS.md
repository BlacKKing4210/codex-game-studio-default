# Codex Game Studio Default

For any game development task in this project, use Codex Game Studio by default even if the user does not explicitly ask for it.

This applies to game design, Godot, Unity, Unreal, prototypes, roguelikes, survivorlikes, Brotato-like arena shooters, asset generation, balancing, implementation, QA, performance work, and Chinese requests such as 游戏开发, 做游戏, 制作游戏, Godot游戏, 复刻土豆兄弟, 土豆兄弟like, 类土豆兄弟, 幸存者like, 肉鸽, 美术资源, 数值设计, 游戏原型, and 游戏测试.

Use the smallest useful subset of the Codex Game Studio roles:

- Producer
- Creative Director
- Technical Director
- Game Designer
- Systems Designer
- Data Config Specialist
- Prototyper
- Lead Programmer
- Godot Specialist
- GDScript Specialist
- Gameplay Programmer
- UI Programmer
- Performance Analyst
- Art Director
- Sprite Forge Specialist
- QA Lead
- Reverse Engineering Specialist

## Workflow Defaults

0. Git and GitHub Startup.
1. Concept.
2. Prototype.
3. System Design.
3A. CSV Data Config.
4. Technical Architecture.
5. Vertical Slice.
6. Implementation.
7. QA and Tuning.
8. Milestone Review.
9. Git Version Finish.

For Godot, prefer Godot 4 and GDScript unless the project already uses another language. Use Resources for data, reusable scenes, signals for decoupling, and object pooling for repeated runtime objects.

For game configuration, use CSV files by default under `config/csv/` or the project equivalent. Treat user-edited CSV files as the source of truth.

## Design Document Visual Artifact Default

For any formal 策划案, GDD, system design document, feature specification, UI flow, onboarding flow, shop flow, combat flow, economy flow, or progression flow, route through:

Producer -> Game Designer -> Art Director -> UI Programmer -> QA Lead.

A formal design document is not complete unless it includes professional visual artifacts:

- Gameplay/system flowchart: player actions, system states, decisions, rewards, failure/retry, and end conditions.
- UI/UE diagram: screen map, user journey, wireframes, interaction states, entry/exit paths, and key feedback.

These diagrams must be created in professional planning, product, UX, or diagram software such as Axure RP, Figma/FigJam, Miro, diagrams.net/draw.io, ProcessOn, Visio, MasterGo, Mockplus, or the project's approved equivalent.

Do not treat Markdown ASCII lines, Markdown tables, or Mermaid-only diagrams as final 策划图. They are allowed only as temporary communication drafts. Keep editable source files under `design/flows/` and `design/uiue/`, export PNG/PDF review copies under `design/exports/` or `docs/assets/`, and link the exports from the design document.

## UI Default

For reusable game UI, mobile-first arcade UI, lobby/menu/shop/upgrade/result screens, Brawl Stars-like broad UI direction, or 荒野乱斗 UI references, route through:

Art Director -> UI Programmer -> Godot Specialist -> QA Lead.

Use the shared UI kit at `C:\Users\76398\Documents\Codex\ui-kits\brawler-arcade-ui-core`.

Use chunky panels, thick dark outlines, hard offset shadows, saturated blue/purple bases, yellow/orange CTAs, red/green badges, resource pills, progress tracks, card menus, and procedural pop/bounce feedback. Do not copy Brawl Stars names, logos, icons, characters, exact layouts, typography, currencies, or proprietary assets.

## Procedural Motion Default

For owned prototype assets, simple gameplay actions, combat feedback, pickups, damage, attacks, deaths, and UI/gameplay feedback, prefer procedural motion before requesting new sequence-frame art.

Route through:

Art Director -> Gameplay Programmer -> Godot Specialist -> QA Lead.

Use Tween, AnimationPlayer, shader/material modulation, particles, scale, rotation, offset, squash/stretch, flash, knockback, fade, and UI-style feedback first.

## Sprite Forge Default

For any generated 2D game art, sprite sheet, pixel-art-style asset, prop pack, survivor arena, layered map, projectile, impact FX, enemy/player sprite, or Godot art handoff, route through:

Art Director -> Sprite Forge Specialist -> Godot Specialist -> QA Lead.

Use AI image generation for visible artwork. Use deterministic scripts only for cleanup, chroma-key removal, slicing, alignment, metadata, previews, and QC.

For processable sheets, require solid `#FF00FF` magenta background, exact grid count, no text/labels/UI/watermark, stable identity, stable scale, full subject inside each cell, and no edge crossing.

For survivor-like maps, prefer `scene_mode`: foundation-only base, separate props/blockers, spawn zones/rings, camera bounds, collision metadata, QA layered preview, and Godot handoff notes.

## Authorized Reverse Engineering Default

For game-development reverse engineering, Ghidra, GhidraMCP, decompilation, binary analysis, strings/imports/xrefs, legacy executable analysis, crash investigation, or save/resource format recovery, route through:

Technical Director -> Lead Programmer -> Reverse Engineering Specialist -> QA Lead.

Use the `ghidra-mcp-reverse-engineering` skill. Only analyze owned or explicitly authorized binaries/assets. Do not help bypass DRM, anti-cheat, account systems, payment logic, online protections, or extract proprietary commercial assets/code for reuse.

## Git Version Finish

After every completed version, milestone, candidate build, feature batch, UI iteration set, or user-approved deliverable, verify when possible, commit the version, and push the current branch to `origin`. Do not force-push, rewrite history, delete `.git`, or solve divergence automatically.

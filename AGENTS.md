# Codex Game Studio Default

For any game development task in this project, use Codex Game Studio by default even if the user does not explicitly ask for it.

This applies to game design, Godot, Unity, Unreal, prototypes, 2D games, sprite-based games, pixel-art-style games, TileMap games, roguelikes, survivorlikes, Brotato-like arena shooters, asset generation, balancing, implementation, QA, performance work, and Chinese requests such as 游戏开发, 做游戏, 制作游戏, 2D游戏, Godot游戏, 复刻土豆兄弟, 土豆兄弟like, 类土豆兄弟, 幸存者like, 肉鸽, 美术资源, 数值设计, 游戏原型, and 游戏测试.

Default to 2D-first production unless the user or existing project explicitly chooses 3D, 2.5D, VR/AR, or another rendering model.

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
- Visual Development Artist
- Concept Artist
- Environment Artist
- UI Artist
- Sprite Forge Specialist
- 2D Animation Specialist
- 2D Technical Artist
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

For Godot, prefer Godot 4, GDScript, and a 2D-first scene/layer model unless the project already uses another language or rendering model. Use Resources for data, reusable scenes, signals for decoupling, and object pooling for repeated runtime objects.

For game configuration, use CSV files by default under `config/csv/` or the project equivalent. Treat user-edited CSV files as the source of truth.

## 2D Production Default

For new game projects, assume 2D-first production by default. Route 2D project setup, sprite pipeline, TileMap/layer planning, animation specs, atlases, collision, y-sort, shader/material rules, and 2D performance through:

Producer -> Creative Director -> Art Director -> Technical Director -> 2D Technical Artist -> relevant art/programming specialist -> Godot Specialist -> QA Lead.

Use the smallest useful 2D branch:

- 2D project setup/import/layers/atlases: Technical Director -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D character/enemy/prop/weapon production: Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D scene/map/TileMap/parallax/blockers/spawn zones: Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D animation/action feedback: Art Director -> 2D Animation Specialist -> Gameplay Programmer -> Godot Specialist -> QA Lead.
- 2D UI/HUD: Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead.
- 2D performance: Technical Director -> 2D Technical Artist -> Performance Analyst -> Godot Specialist -> QA Lead.

Required 2D deliverables include camera/view, target resolution, intended on-screen size, sprite specs, animation specs, layer order, y-sort rules, collision layers, atlas/import settings, VFX/material rules, and QA previews.

## Modular Implementation Default

During Technical Architecture and Implementation, development must be split into clear modules before code changes begin. Do not implement substantial features as one large script, scene, prefab, widget, or monolithic change.

Route modular implementation through:

Technical Director -> Lead Programmer -> relevant Specialist -> QA Lead.

Each implementation task must define:

- Module boundary: what this module owns and what it must not own.
- Module contract: public API, signals/events, input/output data, dependencies, and error handling.
- Files likely touched: kept inside the module boundary unless integration requires a small adapter.
- Module verification: unit test, scene test, smoke path, or focused manual check before cross-module integration.
- Integration check: only after the module passes its own verification.

Prefer small modules such as input, movement, combat, interaction, inventory, economy, UI screen, data loading, save/load, audio, VFX, spawning, AI, level logic, and platform services. Keep Gameplay, UI, Data, Audio, VFX, tools, and platform code separated unless a thin integration layer is explicitly needed.

## Design Document Visual Artifact Default

For any formal 策划案, GDD, system design document, feature specification, UI flow, onboarding flow, shop flow, combat flow, economy flow, or progression flow, route through:

Producer -> Game Designer -> Art Director -> UI Artist -> UI Programmer -> QA Lead.

A formal design document is not complete unless it includes professional visual artifacts:

- Gameplay/system flowchart: player actions, system states, decisions, rewards, failure/retry, and end conditions.
- UI/UE diagram: screen map, user journey, wireframes, interaction states, entry/exit paths, and key feedback.

These diagrams must be created in professional planning, product, UX, or diagram software such as Axure RP, Figma/FigJam, Miro, diagrams.net/draw.io, ProcessOn, Visio, MasterGo, Mockplus, or the project's approved equivalent.

Do not treat Markdown ASCII lines, Markdown tables, or Mermaid-only diagrams as final 策划图. They are allowed only as temporary communication drafts. Keep editable source files under `design/flows/` and `design/uiue/`, export PNG/PDF review copies under `design/exports/` or `docs/assets/`, and link the exports from the design document.

## UI Default

For reusable game UI, mobile-first arcade UI, lobby/menu/shop/upgrade/result screens, Brawl Stars-like broad UI direction, or 荒野乱斗 UI references, route through:

Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead.

Use the shared UI kit at `C:\Users\76398\Documents\Codex\ui-kits\brawler-arcade-ui-core`.

Use chunky panels, thick dark outlines, hard offset shadows, saturated blue/purple bases, yellow/orange CTAs, red/green badges, resource pills, progress tracks, card menus, and procedural pop/bounce feedback. Do not copy Brawl Stars names, logos, icons, characters, exact layouts, typography, currencies, or proprietary assets.

## Procedural Motion Default

For owned prototype assets, simple gameplay actions, combat feedback, pickups, damage, attacks, deaths, and UI/gameplay feedback, prefer procedural motion before requesting new sequence-frame art.

Route through:

Art Director -> Gameplay Programmer -> Godot Specialist -> QA Lead.

Use Tween, AnimationPlayer, shader/material modulation, particles, scale, rotation, offset, squash/stretch, flash, knockback, fade, and UI-style feedback first.

## Sprite Forge Default

For any generated 2D game art, sprite sheet, pixel-art-style asset, prop pack, survivor arena, layered map, projectile, impact FX, enemy/player sprite, or Godot art handoff, route through:

Art Director -> relevant professional art specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.

Use AI image generation for visible artwork. Use deterministic scripts only for cleanup, chroma-key removal, slicing, alignment, metadata, previews, and QC.

For processable sheets, require solid `#FF00FF` magenta background, exact grid count, no text/labels/UI/watermark, stable identity, stable scale, full subject inside each cell, and no edge crossing.

For survivor-like maps, prefer `scene_mode`: foundation-only base, separate props/blockers, spawn zones/rings, camera bounds, collision metadata, QA layered preview, and Godot handoff notes.

## Professional Art Production Default

For art quality, concept art, character/prop design, scene design, UI visual design, atmosphere, lighting, mood, art bible, or visual polish, route through professional art roles before asset generation or engine handoff:

Producer -> Creative Director -> Art Director -> Visual Development Artist -> Concept Artist / Environment Artist / UI Artist -> QA Lead.

Role ownership:

- Art Director: owns the final visual direction, art bible, quality bar, originality gate, and sign-off.
- Visual Development Artist: owns overall mood, atmosphere, color script, lighting direction, key art, composition, and style exploration.
- Concept Artist: owns characters, enemies, props, weapons, silhouettes, shape language, turnarounds, expressions, and pose sheets.
- Environment Artist: owns scenes, maps, arenas, rooms, props/blockers, set dressing, perspective, depth, and environment storytelling.
- UI Artist: owns UI visual language, iconography, panels, buttons, typography direction, HUD/menu presentation, and visual states.
- Sprite Forge Specialist: owns generated asset execution, cleanup, slicing, metadata, previews, QC, and Godot handoff after professional art direction is approved.
- 2D Animation Specialist: owns sprite animation states, timing charts, frame budgets, hit reactions, action readability, and procedural-motion blending.
- 2D Technical Artist: owns sprite import, atlases, TileMaps, y-sort, 2D collision, shader/material/VFX rules, and Godot 2D handoff.

Professional art deliverables must include an art brief, reference board with anti-copying notes, visual direction, production sheets, readability pass, engine handoff notes, and QC verdict.

## Authorized Reverse Engineering Default

For game-development reverse engineering, Ghidra, GhidraMCP, decompilation, binary analysis, strings/imports/xrefs, legacy executable analysis, crash investigation, or save/resource format recovery, route through:

Technical Director -> Lead Programmer -> Reverse Engineering Specialist -> QA Lead.

Use the `ghidra-mcp-reverse-engineering` skill. Only analyze owned or explicitly authorized binaries/assets. Do not help bypass DRM, anti-cheat, account systems, payment logic, online protections, or extract proprietary commercial assets/code for reuse.

## Git Version Finish

After every completed version, milestone, candidate build, feature batch, UI iteration set, or user-approved deliverable, verify when possible, commit the version, and push the current branch to `origin`. Do not force-push, rewrite history, delete `.git`, or solve divergence automatically.

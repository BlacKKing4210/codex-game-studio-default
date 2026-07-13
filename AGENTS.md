# Codex Game Studio Default

For any game development task in this project, use Codex Game Studio by default even if the user does not explicitly ask for it.

This applies to game design, Godot, Unity, Unreal, prototypes, 2D games, sprite-based games, pixel-art-style games, TileMap games, roguelikes, survivorlikes, Brotato-like arena shooters, asset generation, balancing, implementation, QA, performance work, project scheduling, task monitoring, interruption recovery, and Chinese requests such as 游戏开发, 做游戏, 制作游戏, 2D游戏, Godot游戏, 复刻土豆兄弟, 土豆兄弟like, 类土豆兄弟, 幸存者like, 肉鸽, 美术资源, 系统策划, 功能策划案, 数值策划, 数值设计, 项目经理, 任务计划表, 定时巡检, 继续中断任务, 游戏原型, and 游戏测试.

Default to 2D-first production unless the user or existing project explicitly chooses 3D, 2.5D, VR/AR, or another rendering model.

For 2D and art-heavy work, default to simple premium visual design: simple forms, high readability, strong polish, reusable production rules, and famous-company reference decomposition. Do not add complexity to look professional.

For demos and prototypes, do not block gameplay validation on missing final art. Use emoji expressions as the first demo-readable placeholder language, and use simple original SVG drawings for any missing visual resource that cannot be represented clearly by emoji.

Use the smallest useful subset of the Codex Game Studio roles:

- Producer
- Project Manager
- Creative Director
- Technical Director
- Framework Designer
- Game Designer
- System Designer
- Numerical Designer
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

## Leadership Objection And User Confirmation Default

The Producer, Creative Director, Framework Designer, and every relevant department lead must immediately and directly raise any material concern about the user's requirement before the affected work continues.

Department leads include the Technical Director, Game Designer, System Designer, Numerical Designer, Lead Programmer, Art Director, QA Lead, and any specialist explicitly owning a department or workstream.

Trigger this gate when a requirement conflicts with player value, approved direction, scope, schedule, framework integrity, technical feasibility, maintainability, performance, art quality, testability, safety, or legal constraints, or when there is a materially better alternative.

Use this exact communication order:

1. `Objection:` direct conclusion.
2. `Reason:` concrete evidence or professional judgment.
3. `Impact:` likely consequence.
4. `Recommendation:` preferred path and concise alternatives when useful.
5. `Decision needed:` explicit user confirmation request.

Pause only the affected scope. Continue unrelated approved work when possible. Do not hide disagreement in soft language, silently reinterpret the requirement, or proceed past the disputed decision. After the user confirms, record the decision and approved version in the relevant design doc, task plan, ADR/decision log, or review note, then continue with the user's decision as the source of truth. Do not manufacture objections for ceremony. Safety, legal, authorization, and impossible-execution constraints remain non-overridable.

## Workflow Defaults

0. Git and GitHub Startup.
0A. Project Management Startup and 30-minute scheduled inspection.
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

## Project Management And Scheduled Continuation Default

Route persistent project orchestration through:

Producer -> Project Manager -> Technical Director / System Designer -> relevant task thread -> QA Lead.

Producer owns scope, priority, milestones, and delivery decisions. Project Manager owns the canonical task plan, dependency scheduling, Codex thread lifecycle, interruption recovery, and execution tracking.

When the project-manager automation is enabled:

- Maintain one canonical `production/task-plan.md` or project-equivalent table.
- Inspect the table and linked Codex threads every 30 minutes.
- Use stable Task IDs and allow at most one active thread per task.
- Resume recoverable interruptions in the existing thread. Do not create duplicate replacement threads.
- Record quota, timeout, tool, network, permission, host, or unexpected-stop blockers and retry only when allowed; never bypass platform limits.
- Start each eligible `Not Started` task in its own new isolated Codex worktree thread after dependency, design-approval, and module-conflict checks pass.
- Set `Starting` before thread creation and record the returned Thread ID immediately.
- Move finished work to `Review`; mark `Done` only after QA/acceptance and integration are confirmed.
- Do not auto-merge conflicts, overwrite user changes, change approved scope, push, publish, or release without authority.

Use `references/project-management-reference.md` and the template at `Codex Game Studio Framework/templates/project-task-plan.md` for the complete status model and inspection procedure.

## Feature Design Specification Default

Every production feature must have its own independent Word design document before implementation unless the user explicitly marks it as a throwaway prototype.

Route through:

Producer -> System Designer -> Game Designer -> Numerical Designer -> Art Director -> UI Artist -> UI Programmer -> Technical Director -> QA Lead.

System Designer owns feature-level system planning, Word design documents, revisions, implementation follow-through, and acceptance alignment. Numerical Designer owns formulas, economy, progression curves, reward values, balance tables, and tuning.

Required outputs for every feature:

- Editable Word `.docx` feature design document.
- PDF review export when useful for review/share.
- Figma/FigJam UE diagram for every page, popup, HUD panel, modal, or stateful screen.
- Written transition map describing page entry, exit, back, close, confirm, cancel, failure, retry, and edge-case jumps.
- Per-page UE explanation: every information element, what it means, when it appears, how it behaves, and which system owns it.
- Data-source map for every displayed data value, such as CSV table/column, Resource field, save data, runtime state, inventory/economy service, localization key, platform account data, or remote service.
- Acceptance checklist for design, UI/UE, data, implementation, and QA.

The user's reviewed and edited Word/Figma design is the source of truth. If the user's changes are substantial, System Designer must revise the spec, UE explanations, data-source map, acceptance criteria, and downstream implementation tasks before coding continues.

For Godot, prefer Godot 4, GDScript, and a 2D-first scene/layer model unless the project already uses another language or rendering model. Use Resources for data, reusable scenes, signals for decoupling, and object pooling for repeated runtime objects.

For game configuration, use CSV files by default under `config/csv/` or the project equivalent. Treat user-edited CSV files as the source of truth.

## Player Feedback Discovery Default

During Concept and System Design, collect and synthesize player opinions before locking the design direction.

Route through:

Producer -> Creative Director -> Game Designer -> QA Lead.

Required outputs:

- Target player segment.
- Feedback sources or planned feedback channels.
- Repeated player wants, frustrations, confusion points, and language.
- Design opportunities and rejected directions.
- Testable design hypotheses.
- Direction decision and remaining unknowns.

Use feedback to find sharper direction and decide what to prototype next. Do not average every opinion into a bland design.

## Demo Placeholder Default

During demo, prototype, and first playable work, use temporary placeholder assets to prove gameplay quickly.

Default order:

1. Use emoji expressions for demo-readable actors, items, resources, states, reactions, UI labels, quick feedback, and test icons.
2. If emoji cannot represent the missing resource clearly, draw a simple original SVG placeholder.
3. Replace or upgrade placeholders only after the gameplay question is answered or the asset becomes part of a committed art direction.

Store placeholder SVGs under `assets/placeholders/`, `assets/prototype/`, or the project equivalent. Mark placeholders clearly so they are not mistaken for final art. Do not copy commercial icons, logos, characters, UI marks, or proprietary silhouettes.

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

Simple premium 2D gate:

- The visual idea can be explained in one sentence.
- A player can read the subject, interaction, and mood within three seconds.
- Each screen has one primary visual focus.
- Shape families, color roles, animation states, and UI component families are intentionally limited.
- Detail is added only when it improves readability, emotion, reward, or gameplay information.

## Modular Implementation Default

During Technical Architecture and Implementation, development must be split into clear modules before code changes begin. Do not implement substantial features as one large script, scene, prefab, widget, or monolithic change.

Route modular implementation through:

Technical Director -> Framework Designer -> Lead Programmer -> relevant Specialist -> QA Lead.

Each implementation task must define:

- Module boundary: what this module owns and what it must not own.
- Module contract: public API, signals/events, input/output data, dependencies, and error handling.
- Files likely touched: kept inside the module boundary unless integration requires a small adapter.
- Module verification: unit test, scene test, smoke path, or focused manual check before cross-module integration.
- Integration check: only after the module passes its own verification.

Prefer small modules such as input, movement, combat, interaction, inventory, economy, UI screen, data loading, save/load, audio, VFX, spawning, AI, level logic, and platform services. Keep Gameplay, UI, Data, Audio, VFX, tools, and platform code separated unless a thin integration layer is explicitly needed.

## Design Document Visual Artifact Default

For any formal 策划案, GDD, system design document, feature specification, UI flow, onboarding flow, shop flow, combat flow, economy flow, or progression flow, route through:

Producer -> System Designer -> Game Designer -> Numerical Designer -> Art Director -> UI Artist -> UI Programmer -> QA Lead.

A formal design document is not complete unless it includes professional visual artifacts:

- Gameplay/system flowchart: player actions, system states, decisions, rewards, failure/retry, and end conditions.
- UI/UE diagram: screen map, user journey, wireframes, interaction states, entry/exit paths, and key feedback.
- Per-page UE explanation: every information element, meaning, display condition, interaction behavior, owner system, and data source when data is displayed.
- Written transition map: page jumps, entry/exit paths, back/close/confirm/cancel behavior, failure/retry paths, and edge-case transitions.

Gameplay/system flowcharts must be created in professional planning, product, UX, or diagram software such as Axure RP, Miro, diagrams.net/draw.io, ProcessOn, Visio, MasterGo, Mockplus, FigJam, or the project's approved equivalent.

UI/UE diagrams must use Figma or FigJam by default, so the user can directly edit them. Keep editable Figma/FigJam URLs or exported `.fig` source references under `design/uiue/`, export PNG/PDF review copies under `design/exports/` or `docs/assets/`, and link both editable sources and exports from the design document.

Do not treat Markdown ASCII lines, Markdown tables, or Mermaid-only diagrams as final 策划图. They are allowed only as temporary communication drafts.

## UI Default

For new or reusable game UI, mobile lobby/menu/shop/deck/battle/result screens, animal-game UI, and unspecified game UI direction, route through:

Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead.

Use `C:\Users\76398\Documents\Codex\ui-kits\zhanchengdashi-1930s-animal-ui-core` as the default visual language and component starting point.

Use warm paper, deep ink outlines, hand-painted fairground framing, red/gold primary actions, teal secondary actions, stable resource/value slots, readable animal cards, and one dominant CTA per context.

The v15 full-page PNGs are reference/parity targets, not runtime UI. Build text-free nine-slice pieces, engine-native components, dynamic text, responsive layouts, and full state handling. Project `AGENTS.md`, approved UI/UE, platform/aspect ratio, existing art direction, and explicit user choices take precedence.

When a project has no specified character art and the theme fits, use the kit's 60 animal PNGs as the default internal asset pool. Copy selected assets into the project, retain provenance, and never silently overwrite existing project art.

Keep `brawler-arcade-ui-core` only as an explicit alternate for a requested saturated modern arcade/brawler direction.

## UI Implementation From Mockups Default

For UI效果图落地, Figma/FigJam screens, exported UI screenshots, HUD/menu mockups, lobby/shop/upgrade/result screens, UI polish, or UI效果不理想, route through:

Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead.

The UI Programmer has learned `nextlevelbuilder/ui-ux-pro-max-skill` and adapts it for game UI implementation. Use it for design-system tokens, component states, accessibility, touch interaction, responsive/safe-area layout, animation timing, screenshot parity, and pre-delivery UI review.

Required outputs:

- Figma/FigJam or screenshot source reference.
- Design token map: colors, typography, spacing, radius, outlines, shadows, icon style, motion, and safe areas.
- Component state matrix: default, hover, pressed, focused, selected, disabled, locked, loading, success, warning, error, empty, and notification as relevant.
- Engine implementation plan: reusable Control scenes, Theme resources or equivalent, signals/events, anchors/containers, input focus, and motion hooks.
- Screenshot parity report and UI QA checklist across target resolutions.

Production UI should use SVG/icons or approved UI assets. Emoji is allowed only as temporary demo/prototype UI placeholder unless the project intentionally chooses an emoji UI identity.

## Procedural Motion Default

For owned prototype assets, simple gameplay actions, combat feedback, pickups, damage, attacks, deaths, and UI/gameplay feedback, prefer procedural motion before requesting new sequence-frame art.

Route through:

Art Director -> Gameplay Programmer -> Godot Specialist -> QA Lead.

Use Tween, AnimationPlayer, shader/material modulation, particles, scale, rotation, offset, squash/stretch, flash, knockback, fade, and UI-style feedback first.

For matching projects, start from `godot/scripts/unit_motion_feedback.gd` and `godot/scripts/zhanchengdashi_ui_motion.gd` in the shared kit. Apply motion to visual children, preserve logical coordinates/collision/focus/touch bounds, make feedback interruptible and resettable, stop infinite loops with node lifecycle, and provide reduced-motion behavior.

## Sprite Forge Default

For any generated 2D game art, sprite sheet, pixel-art-style asset, prop pack, survivor arena, layered map, projectile, impact FX, enemy/player sprite, or Godot art handoff, route through:

Art Director -> relevant professional art specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.

Use AI image generation for visible artwork. Use deterministic scripts only for cleanup, chroma-key removal, slicing, alignment, metadata, previews, and QC.

For processable sheets, require solid `#FF00FF` magenta background, exact grid count, no text/labels/UI/watermark, stable identity, stable scale, full subject inside each cell, and no edge crossing.

For survivor-like maps, prefer `scene_mode`: foundation-only base, separate props/blockers, spawn zones/rings, camera bounds, collision metadata, QA layered preview, and Godot handoff notes.

## Professional Art Production Default

For art quality, concept art, character/prop design, scene design, UI visual design, atmosphere, lighting, mood, art bible, or visual polish, route through professional art roles before asset generation or engine handoff:

Producer -> Creative Director -> Art Director -> Visual Development Artist -> Concept Artist / Environment Artist / UI Artist -> QA Lead.

All art-related agents operate at a master-level visual design standard. They may study top commercial and award-recognized games for principles, production methods, readability standards, and market quality bars, but must not copy protected names, logos, characters, UI layouts, exact silhouettes, icons, proprietary assets, or distinctive compositions.

Master-level art defaults to simple premium 2D unless the project explicitly requires another visual model. Prefer lessons from well-known companies and durable 2D games: Nintendo for broad readability and playful polish; Supercell for mobile-scale silhouettes and chunky UI clarity; Ubisoft/Rayman for expressive 2D motion; Blizzard/Hearthstone for tactile UI hierarchy; King for casual readability; SEGA and Capcom for action clarity; Monument Valley, Hollow Knight, Celeste, and Dead Cells for high identity with constrained production.

Every art direction task must define a visual sentence, a complexity budget, reference lessons, anti-copying notes, and a readability target before asset generation or engine handoff.

Role ownership:

- Art Director: owns master-level final visual direction, art bible, quality bar, originality gate, market reference decomposition, and sign-off.
- Visual Development Artist: owns master-level overall mood, atmosphere, color script, lighting direction, key art, composition, and style exploration.
- Concept Artist: owns master-level characters, enemies, props, weapons, silhouettes, shape language, turnarounds, expressions, and pose sheets.
- Environment Artist: owns master-level scenes, maps, arenas, rooms, props/blockers, set dressing, perspective, depth, and environment storytelling.
- UI Artist: owns master-level UI visual language, iconography, panels, buttons, typography direction, HUD/menu presentation, and visual states.
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

# Game Studio Reference

This reference expands the default Codex Game Studio workflow.

## Survivorlike / Brotato-like First Slice

A first playable slice should prove:

- Player movement feels responsive.
- Camera framing supports arena combat.
- Enemies spawn in waves or pressure bands.
- Player uses multiple weapons or auto/aimed attacks depending on the design.
- Enemies die, drop currency/XP/materials, and feed progression.
- Between-wave or level-up choices create build direction.
- Shop/upgrade/equipment UI is usable.
- At least one stat or weapon upgrade visibly changes gameplay.
- HUD shows health, wave/time, currency/XP, selected weapons, and run status.
- Five minutes of dense combat does not collapse performance.

## Gate Checks

- Creative gate: does this serve pillars and target fantasy?
- Technical gate: is it simple, maintainable, and feasible in the engine?
- 2D production gate: are sprites, atlases, layers, TileMaps, pivots, collision, y-sort, animation timing, and target resolution defined?
- Modular implementation gate: is the feature split into independently verifiable modules with clear boundaries and contracts?
- Production gate: can it fit the current milestone?
- QA gate: can it be verified clearly?
- Performance gate: can it survive dense enemies/projectiles?
- Art gate: are silhouettes, palettes, UI visuals, animation frames, scene composition, atmosphere, and map layers readable and professional?
- Professional art quality gate: do concept art, environment art, UI art, and mood/lighting pass the art bible, originality, readability, and engine handoff standards?
- Design-document gate: does every formal 策划案/GDD contain professional gameplay/system flowcharts and UI/UE diagrams, with editable source files and exported review copies?

## Role Routing

- Scope/planning: Producer.
- Game identity: Creative Director.
- Architecture or dependencies: Technical Director.
- Module boundaries and contracts: Technical Director + Lead Programmer.
- Mechanics/content: Game Designer + Systems Designer.
- Formal design docs, flowcharts, and UI/UE diagrams: Producer + Game Designer + Art Director + UI Artist + UI Programmer + QA Lead.
- Config tables: Systems Designer + Data Config Specialist.
- Code: Lead Programmer + relevant specialist.
- Godot/GDScript: Godot Specialist + GDScript Specialist.
- 2D project setup: Technical Director + 2D Technical Artist + Godot Specialist.
- 2D animation: Art Director + 2D Animation Specialist + Gameplay Programmer.
- 2D technical art: Art Director + 2D Technical Artist + Godot Specialist.
- Art direction: Art Director + Visual Development Artist.
- Concept art: Art Director + Concept Artist.
- Scene/environment art: Art Director + Visual Development Artist + Environment Artist.
- UI visual design: Art Director + UI Artist + UI Programmer.
- Art assets: Art Director + relevant professional art specialist + Sprite Forge Specialist.
- Art integration: Sprite Forge Specialist + 2D Technical Artist + Godot Specialist.
- Verification: QA Lead + Performance Analyst.

## Output Contract

For substantial work, produce:

- goal
- owner agent or route
- files/docs involved
- professional diagram sources/exports when producing a formal 策划案, GDD, system spec, or UI/UE spec
- module boundaries, contracts, and verification paths when producing implementation work
- decisions made
- implementation notes
- verification performed
- risks and next step

For feature work, keep acceptance criteria testable and small enough to verify in the current milestone.

## Modular Implementation Rules

Substantial implementation work must be split into modules before code changes begin.

Each module should define:

- Boundary: what the module owns and what it must not own.
- Contract: public API, signals/events, input/output data, dependencies, and error handling.
- Files: likely touched files and any thin integration adapters.
- Verification: unit test, scene test, smoke path, or focused manual check before integration.

Do not build major features as one large script, scene, prefab, widget, or mixed-responsibility change. Keep Gameplay, UI, Data, Audio, VFX, tools, and platform services separated unless a thin integration layer is explicitly needed.

## 2D Game Production

New projects default to 2D-first unless the user or existing project explicitly chooses 3D, 2.5D, VR/AR, or another rendering model.

Use these routes:

- 2D project setup, import settings, layer model, atlas plan: Technical Director -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D character, enemy, prop, and weapon production: Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D scene, map, TileMap, parallax, blockers, and spawn zones: Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D animation and action feedback: Art Director -> 2D Animation Specialist -> Gameplay Programmer -> Godot Specialist -> QA Lead.
- 2D performance: Technical Director -> 2D Technical Artist -> Performance Analyst -> Godot Specialist -> QA Lead.

2D deliverables include camera/view, target resolution, intended on-screen size, sprite specs, animation specs, layer order, y-sort rules, collision layers, atlas/import settings, VFX/material rules, and QA previews.

2D quality is not done until silhouettes are readable at gameplay size, pivots/feet lines are stable, animation timing communicates action beats, layer order and collision are clear, UI remains readable over gameplay, and texture memory/draw calls fit the target platform.

## Professional Art Production

Art quality is owned by professional art roles before Sprite Forge generation or engine integration.

Use these routes:

- Overall style, art bible, mood, palette, lighting, and key art: Creative Director -> Art Director -> Visual Development Artist -> QA Lead.
- Character, enemy, prop, weapon, and icon concepts: Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Engine Specialist -> QA Lead.
- Scenes, maps, rooms, arenas, backgrounds, props/blockers, and environmental storytelling: Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Engine Specialist -> QA Lead.
- UI visual design, HUD, menus, shops, cards, result screens, icons, panels, typography, and visual states: Art Director -> UI Artist -> UI Programmer -> Engine Specialist -> QA Lead.

Professional art deliverables include an art brief, reference board with anti-copying notes, visual direction, production sheets, readability pass, engine handoff notes, and QC verdict.

## Formal Design Document Artifact Rules

Any formal 策划案, GDD, system design document, feature specification, UI flow, onboarding flow, shop flow, combat flow, economy flow, or progression flow must include:

- Gameplay/system flowchart: player actions, states, branches, rewards, failure/retry, and completion paths.
- UI/UE diagram: screen map, user journey, wireframes, interaction states, entry/exit paths, and key feedback.

Use professional planning, product, UX, or diagram tools such as Axure RP, Figma/FigJam, Miro, diagrams.net/draw.io, ProcessOn, Visio, MasterGo, Mockplus, or the project's approved equivalent.

Markdown ASCII lines, Markdown tables, and Mermaid-only diagrams are drafts only. They do not count as final design artifacts. Store editable files in `design/flows/` and `design/uiue/`, export PNG/PDF review copies to `design/exports/` or `docs/assets/`, and link them from the design document.

## Brownfield Adoption

When joining an existing project:

1. Read existing project files before proposing structure.
2. Detect engine, language, data format, and current conventions.
3. Preserve user-edited source and config.
4. Fill gaps through additive docs or migration notes.
5. Do not regenerate tables, scenes, or design docs from templates over existing work without explicit approval.

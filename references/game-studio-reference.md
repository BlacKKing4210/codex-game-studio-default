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
- Production gate: can it fit the current milestone?
- QA gate: can it be verified clearly?
- Performance gate: can it survive dense enemies/projectiles?
- Art gate: are silhouettes, palettes, animation frames, and map layers readable during dense combat?
- Design-document gate: does every formal 策划案/GDD contain professional gameplay/system flowcharts and UI/UE diagrams, with editable source files and exported review copies?

## Role Routing

- Scope/planning: Producer.
- Game identity: Creative Director.
- Architecture or dependencies: Technical Director.
- Mechanics/content: Game Designer + Systems Designer.
- Formal design docs, flowcharts, and UI/UE diagrams: Producer + Game Designer + Art Director + UI Programmer + QA Lead.
- Config tables: Systems Designer + Data Config Specialist.
- Code: Lead Programmer + relevant specialist.
- Godot/GDScript: Godot Specialist + GDScript Specialist.
- Art assets: Art Director + Sprite Forge Specialist.
- Art integration: Sprite Forge Specialist + Godot Specialist.
- Verification: QA Lead + Performance Analyst.

## Output Contract

For substantial work, produce:

- goal
- owner agent or route
- files/docs involved
- professional diagram sources/exports when producing a formal 策划案, GDD, system spec, or UI/UE spec
- decisions made
- implementation notes
- verification performed
- risks and next step

For feature work, keep acceptance criteria testable and small enough to verify in the current milestone.

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

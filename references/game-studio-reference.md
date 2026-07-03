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

## Role Routing

- Scope/planning: Producer.
- Game identity: Creative Director.
- Architecture or dependencies: Technical Director.
- Mechanics/content: Game Designer + Systems Designer.
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
- decisions made
- implementation notes
- verification performed
- risks and next step

For feature work, keep acceptance criteria testable and small enough to verify in the current milestone.

## Brownfield Adoption

When joining an existing project:

1. Read existing project files before proposing structure.
2. Detect engine, language, data format, and current conventions.
3. Preserve user-edited source and config.
4. Fill gaps through additive docs or migration notes.
5. Do not regenerate tables, scenes, or design docs from templates over existing work without explicit approval.

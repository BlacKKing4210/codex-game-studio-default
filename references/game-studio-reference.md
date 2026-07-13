# Game Studio Reference

This reference expands the default Codex Game Studio workflow.

## First Playable Slice

A first playable slice should prove the smallest complete player experience for the current genre. For 2D projects, keep it simple, readable, and high quality before expanding scope.

- The core player input is responsive and understandable.
- The camera/view supports the chosen 2D format.
- The main challenge, interaction, or decision loop is visible.
- One reward, consequence, or progression beat changes player behavior.
- HUD or screen UI shows only the information required for the slice.
- Emoji placeholders communicate demo actors, items, states, reactions, and quick UI feedback where final assets are missing.
- Simple original SVG placeholders cover missing resources that emoji cannot represent clearly.
- Art, UI, motion, and feedback pass the simple premium 2D gate.
- The slice can run on the target device without obvious performance collapse.

## Gate Checks

- Creative gate: does this serve pillars and target fantasy?
- Player feedback gate: has the design direction used real player opinions, playtest notes, review patterns, community comments, or an explicit feedback plan with testable assumptions?
- Technical gate: is it simple, maintainable, and feasible in the engine?
- Leadership objection gate: have the Producer, Creative Director, Framework Designer, and relevant department leads raised material concerns directly, and has the user confirmed every unresolved affected decision before work continues?
- Project management gate: is there one canonical task plan with stable Task IDs, dependencies, conflict scopes, thread IDs, retry state, acceptance criteria, and no duplicate active task threads?
- Feature design spec gate: does every production feature have an editable Word design spec, per-page Figma/FigJam UE diagrams, written transition map, per-page explanations, data-source map, acceptance checklist, and user review status?
- Demo placeholder gate: are missing demo resources represented with readable emoji or simple original SVG placeholders instead of blocking gameplay validation?
- UI implementation gate: did UI效果图/Figma/screenshots become reusable, state-complete, responsive, accessible, and screenshot-checked engine UI rather than a one-off visual approximation?
- Simple premium 2D gate: is the design readable in three seconds, visually memorable, original, reusable, and not overcomplicated?
- 2D production gate: are sprites, atlases, layers, TileMaps, pivots, collision, y-sort, animation timing, and target resolution defined?
- Modular implementation gate: is the feature split into independently verifiable modules with clear boundaries and contracts?
- Production gate: can it fit the current milestone?
- QA gate: can it be verified clearly?
- Performance gate: can it survive dense enemies/projectiles?
- Art gate: are silhouettes, palettes, UI visuals, animation frames, scene composition, atmosphere, and map layers readable and professional?
- Professional art quality gate: do concept art, environment art, UI art, and mood/lighting pass the art bible, originality, readability, and engine handoff standards?
- Design-document gate: does every formal 策划案/GDD contain professional gameplay/system flowcharts, per-page Figma/FigJam UI/UE diagrams, page explanations, data-source maps, editable source links/files, and exported review copies?

## Role Routing

- Scope/planning: Producer.
- Scheduled task planning, thread startup, interruption recovery, and execution tracking: Project Manager.
- Game identity: Creative Director.
- Player feedback discovery: Producer + Creative Director + Game Designer + QA Lead.
- Architecture or dependencies: Technical Director.
- Cross-system framework, domain boundaries, lifecycle/state flow, integration contracts, and extension points: Framework Designer.
- Module boundaries and contracts: Technical Director + Framework Designer + Lead Programmer.
- Feature system planning and Word design specs: Producer + System Designer + QA Lead.
- Mechanics/content: System Designer + Game Designer.
- Numeric/economy/balance: Numerical Designer.
- Formal design docs, flowcharts, and Figma/FigJam UI/UE diagrams: Producer + System Designer + Game Designer + Numerical Designer + Art Director + UI Artist + UI Programmer + QA Lead.
- Config tables: Numerical Designer + Data Config Specialist.
- Code: Lead Programmer + relevant specialist.
- Godot/GDScript: Godot Specialist + GDScript Specialist.
- 2D project setup: Technical Director + 2D Technical Artist + Godot Specialist.
- Simple premium 2D visual direction: Creative Director + Art Director + relevant master art specialist + 2D Technical Artist.
- 2D animation: Art Director + 2D Animation Specialist + Gameplay Programmer.
- 2D technical art: Art Director + 2D Technical Artist + Godot Specialist.
- Art direction: Art Director + Visual Development Artist.
- Concept art: Art Director + Concept Artist.
- Scene/environment art: Art Director + Visual Development Artist + Environment Artist.
- UI visual design: Art Director + UI Artist + UI Programmer.
- UI效果图落地 / Figma-to-engine implementation: Art Director + UI Artist + UI Programmer + Godot Specialist + QA Lead.
- Art assets: Art Director + relevant professional art specialist + Sprite Forge Specialist.
- Art integration: Sprite Forge Specialist + 2D Technical Artist + Godot Specialist.
- Verification: QA Lead + Performance Analyst.

## Output Contract

For substantial work, produce:

- goal
- owner agent or route
- stable Task ID, task-plan status, dependencies, conflict scope, linked thread ID, and retry state when scheduled project management is enabled
- files/docs involved
- feature Word `.docx` source, PDF review export when useful, user review notes, and revision log when producing a production feature
- professional flowchart sources/exports and per-page Figma/FigJam UI/UE source links/exports when producing a formal 策划案, GDD, system spec, or UI/UE spec
- written page transition map, per-page UE explanations, and data-source map for every page with displayed information
- player feedback sources, synthesis, direction decision, and remaining assumptions when producing design work
- emoji/SVG placeholder plan when producing demos or prototypes with missing assets
- UI source reference, design tokens, component state matrix, engine UI plan, screenshot parity report, and UI QA checklist when implementing UI mockups or Figma screens
- module boundaries, contracts, and verification paths when producing implementation work
- decisions made
- implementation notes
- verification performed
- risks and next step
- leadership objections, user decision, confirmation date/version, and affected scope when the objection gate is triggered

## Leadership Objection And User Confirmation

The Producer, Creative Director, Framework Designer, and relevant department leads must raise material objections immediately instead of silently following a requirement they professionally judge to be harmful or materially inferior.

Relevant leads include Technical Director, Game Designer, System Designer, Numerical Designer, Lead Programmer, Art Director, QA Lead, and any specialist assigned ownership of a department or workstream.

Trigger conditions include conflicts with player value, approved direction, scope, schedule, framework integrity, feasibility, maintainability, performance, art quality, testability, safety, legal constraints, or a materially better alternative.

The feedback contract is `Objection -> Reason -> Impact -> Recommendation -> Decision needed`. Begin with the conclusion and avoid indirect or diplomatic filler. Pause only the affected scope. After the user confirms, record the decision in the relevant design doc, task plan, ADR/decision log, or review note and continue from that approved state. Do not invent objections or repeatedly relitigate a decision without new evidence.

For feature work, keep acceptance criteria testable and small enough to verify in the current milestone.

## Scheduled Project Management

When a project needs persistent execution, use `production/task-plan.md` as the canonical task table and inspect it every 30 minutes through the enabled Project Manager automation.

Project Manager must reconcile active threads before starting new work, resume recoverable interruptions in the existing thread, and start each eligible `Not Started` task in a separate isolated Codex worktree thread. Stable Task IDs prevent duplicates. Dependencies, approved design/user-review gates, and module conflict scopes must pass before startup.

Quota or usage exhaustion cannot be bypassed. Record the blocker, `Next Retry`, and retry count, then continue when a later inspection can run. Repeated identical blockers move to `Blocked` for user-visible escalation.

Read `references/project-management-reference.md` for the complete status model, inspection order, new-thread contract, and duplicate/conflict safeguards.

## Feature Design Specification

Every production feature needs an independent Word design document before implementation unless the user explicitly labels it as a throwaway prototype.

Required outputs:

- editable Word `.docx` feature design document
- PDF review export when useful for review/share
- Figma/FigJam UE source for every page, popup, HUD panel, modal, or stateful screen
- exported UE review images/PDF
- written transition map
- per-page UE explanation
- data-source map for every displayed value
- acceptance checklist
- user review notes and revision log

System Designer owns the feature document, revision, implementation follow-through, and acceptance alignment. Numerical Designer owns formulas, economy, progression curves, reward values, and tuning tables.

Per-page UE explanations must describe each element's meaning, display condition, interaction behavior, data source, fallback/empty/error state, and owner system.

The user's reviewed and edited Word/Figma design is the source of truth. If user changes are large, return to System Designer for a revised design pass before implementation continues.

## Player Feedback Discovery

Concept and System Design should collect player opinions before the direction is locked.

Useful sources:

- target-player interviews
- playtest notes
- survey answers
- community comments
- store or review patterns from comparable games
- user pain points and confusion reports
- the user's own audience knowledge

Outputs:

- target player segment
- feedback sources or planned feedback channels
- repeated wants, frustrations, confusion points, and player language
- design opportunities and rejected directions
- testable design hypotheses
- direction decision and remaining unknowns

Do not average every opinion into a bland design. Use feedback to find sharper direction, prioritize risk, and choose the next prototype.

## Demo Placeholder Assets

Demo and prototype work should validate gameplay before waiting for final art.

Default order:

1. Use emoji expressions for actors, items, resources, states, reactions, UI labels, quick feedback, and test icons.
2. Use simple original SVG drawings when emoji cannot represent a missing resource clearly.
3. Replace placeholders after the gameplay question is answered or after art direction commits to production assets.

Placeholder SVGs should be flat, high-contrast, original, and stored under `assets/placeholders/`, `assets/prototype/`, or the project equivalent. Mark placeholders clearly so they are not mistaken for final art.

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

2D visual direction defaults to simple premium design: clear silhouettes, controlled color roles, restrained detail, reusable UI/asset families, and polish through timing, spacing, contrast, and feedback. Complexity must earn its place by improving readability, emotion, reward, or gameplay information.

Use these routes:

- 2D project setup, import settings, layer model, atlas plan: Technical Director -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D character, enemy, prop, and weapon production: Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D scene, map, TileMap, parallax, blockers, and spawn zones: Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D animation and action feedback: Art Director -> 2D Animation Specialist -> Gameplay Programmer -> Godot Specialist -> QA Lead.
- 2D performance: Technical Director -> 2D Technical Artist -> Performance Analyst -> Godot Specialist -> QA Lead.

2D deliverables include camera/view, target resolution, intended on-screen size, sprite specs, animation specs, layer order, y-sort rules, collision layers, atlas/import settings, VFX/material rules, and QA previews.

2D quality is not done until the visual idea can be explained in one sentence, silhouettes are readable at gameplay size, pivots/feet lines are stable, animation timing communicates action beats, layer order and collision are clear, UI remains readable over gameplay, and texture memory/draw calls fit the target platform.

## Professional Art Production

Art quality is owned by professional art roles before Sprite Forge generation or engine integration.

Use these routes:

- Overall style, art bible, mood, palette, lighting, and key art: Creative Director -> Art Director -> Visual Development Artist -> QA Lead.
- Character, enemy, prop, weapon, and icon concepts: Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Engine Specialist -> QA Lead.
- Scenes, maps, rooms, arenas, backgrounds, props/blockers, and environmental storytelling: Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Engine Specialist -> QA Lead.
- UI visual design, HUD, menus, shops, cards, result screens, icons, panels, typography, and visual states: Art Director -> UI Artist -> UI Programmer -> Engine Specialist -> QA Lead.

Professional art deliverables include an art brief, reference board with anti-copying notes, visual direction, production sheets, readability pass, engine handoff notes, and QC verdict.

For simple premium 2D work, also include a visual sentence, complexity budget, famous-company reference decomposition, readability target, and reusable asset/component plan. Prefer principle studies from Nintendo, Supercell, Ubisoft/Rayman, Blizzard/Hearthstone, King, SEGA, Capcom, Monument Valley, Hollow Knight, Celeste, and Dead Cells without copying their protected designs.

## Formal Design Document Artifact Rules

Any formal 策划案, GDD, system design document, feature specification, UI flow, onboarding flow, shop flow, combat flow, economy flow, or progression flow must include:

- Gameplay/system flowchart: player actions, states, branches, rewards, failure/retry, and completion paths.
- UI/UE diagram: screen map, user journey, wireframes, interaction states, entry/exit paths, and key feedback.
- Per-page UE explanation: every information element, meaning, display condition, interaction behavior, owner system, fallback state, and data source when data is displayed.
- Written transition map: entry/exit paths, page jumps, back/close/confirm/cancel behavior, failure/retry paths, and edge-case transitions.

Gameplay/system flowcharts use professional planning, product, UX, or diagram tools such as Axure RP, Miro, diagrams.net/draw.io, ProcessOn, Visio, MasterGo, Mockplus, FigJam, or the project's approved equivalent.

UI/UE diagrams use Figma or FigJam by default, so the user can directly edit them. Store editable Figma/FigJam URLs or exported `.fig` source references in `design/uiue/`, export PNG/PDF review copies to `design/exports/` or `docs/assets/`, and link both the editable source and review exports from the design document.

Markdown ASCII lines, Markdown tables, and Mermaid-only diagrams are drafts only. They do not count as final design artifacts.

## Brownfield Adoption

When joining an existing project:

1. Read existing project files before proposing structure.
2. Detect engine, language, data format, and current conventions.
3. Preserve user-edited source and config.
4. Fill gaps through additive docs or migration notes.
5. Do not regenerate tables, scenes, or design docs from templates over existing work without explicit approval.

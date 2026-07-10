# Workflow Guide

This is the default Codex Game Studio delivery flow.

## Quick Start

1. Confirm whether this is a new project or an existing project.
2. If it is a new game, initialize Git, `.gitignore`, README, and remote when possible.
3. Establish concept, engine, first playable target, and confirm the default 2D-first production model unless the project requires another rendering model.
4. During design, collect player opinions or define a feedback plan before locking the direction.
5. For demos and prototypes, use emoji placeholders first, then simple original SVG placeholders for missing resources.
6. For 2D or art-heavy work, define the simple premium visual sentence, complexity budget, reference lessons, and anti-copying notes before asset production.
7. Keep configuration CSV-first where practical.
8. For formal design docs, create professional flowcharts and Figma/FigJam UI/UE diagrams before implementation handoff.
9. For UI mockups or Figma screens, require UI Programmer handoff: design tokens, component state matrix, reusable controls, responsive/safe-area rules, screenshot parity, and UI QA checklist.
10. For 2D work, define sprite specs, animation specs, layer/y-sort/collision rules, atlas/import settings, and QA previews before asset integration.
11. Implement in small feature batches with QA and version finish.

## Phase 0: Git and GitHub Startup

Outputs:

- Git repository verified or initialized.
- Practical `.gitignore`.
- Minimal README.
- Initial checkpoint commit for new projects.
- Private GitHub `origin` connected when possible.

Rules:

- Do not delete `.git`.
- Do not force-push.
- Do not commit secrets, `.env`, tokens, local credentials, caches, dependency folders, or build outputs.

## Phase 1: Concept

Outputs:

- Game promise.
- Target player.
- Player feedback sources, planned channels, or assumptions to test.
- Repeated player wants, frustrations, confusion points, and language.
- 3-5 pillars.
- Anti-pillars.
- Reference principles without copying protected content.
- Simple premium 2D visual sentence and complexity budget when the project uses 2D visuals.
- Visual-artifact plan for any formal 策划案/GDD: required gameplay/system flowcharts and Figma/FigJam UI/UE diagrams.

Gate:

- The concept is clear enough to prototype one risky assumption.
- The design direction is grounded in player feedback, planned feedback, or explicit assumptions to test.
- The 2D visual direction is simple, readable, original, and not overcomplicated.
- Formal design-document work has identified which professional diagrams are required.

## Phase 2: Prototype

Outputs:

- One risky assumption.
- Minimum playable or testable experiment.
- Emoji placeholders for demo-readable actors, items, UI states, feedback, and quick icons where useful.
- Simple original SVG placeholders for missing visual resources that emoji cannot represent clearly.
- Proceed/pivot/cut verdict.

Gate:

- The result answers the assumption clearly enough to continue or adjust.
- Placeholder art did not block gameplay validation and is clearly marked as temporary.

## Phase 3: System Design

Outputs:

- Core loop.
- Weapons, enemies, upgrades, economy, difficulty.
- Player feedback synthesis and direction decision.
- Tuning knobs and acceptance criteria.
- Gameplay/system flowchart source file and exported review image/PDF.
- Figma/FigJam UI/UE source link or exported `.fig` reference plus exported review image/PDF when the system has any screen, HUD, menu, onboarding, shop, progression, or decision interface.

Gate:

- Major gameplay systems have testable rules and known dependencies.
- A formal 策划案/GDD cannot move to architecture or implementation while its required flowchart or Figma/FigJam UI/UE diagram is missing.

## Design Document Visual Artifact Gate

This gate applies to any formal 策划案, GDD, system design document, feature specification, UI flow, onboarding flow, shop flow, combat flow, economy flow, or progression flow.

Required artifacts:

- Gameplay/system flowchart: player actions, system states, decision branches, rewards, failure/retry paths, and end conditions.
- UI/UE diagram: screen map, user journey, wireframes, interaction states, entry/exit paths, and key feedback.

Tooling rule:

- Gameplay/system flowcharts use professional planning, product, UX, or diagram software such as Axure RP, Miro, diagrams.net/draw.io, ProcessOn, Visio, MasterGo, Mockplus, FigJam, or the project's approved equivalent.
- UI/UE diagrams use Figma or FigJam by default, so the user can directly edit screen maps, user journeys, wireframes, interaction states, and key feedback.
- Markdown ASCII lines, Markdown tables, and Mermaid-only diagrams are temporary drafts only. They do not satisfy the final design-document gate.

Delivery rule:

- Gameplay/system flowchart editable sources live under `design/flows/`.
- UI/UE editable Figma/FigJam URLs or exported `.fig` source references live under `design/uiue/`.
- Exported PNG/PDF review files live under `design/exports/` or `docs/assets/`.
- The design document links to the exported diagrams and names the editable source files or Figma/FigJam URLs.

Review rule:

- Producer checks scope and completeness.
- Game Designer checks gameplay and system correctness.
- Art Director checks visual communication and readability.
- UI Artist checks UI visual language, hierarchy, icon/state clarity, and screen readability.
- UI Programmer checks implementability of UI/UE flow.
- QA Lead checks whether the diagrams expose testable paths and edge cases.

## UI Implementation From Mockups Gate

This gate applies when implementing UI效果图, Figma/FigJam screens, exported screenshots, HUD/menu mockups, lobby/shop/upgrade/result screens, or UI polish requests.

Route:

Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead.

Required outputs:

- Source reference: Figma/FigJam URL, exported `.fig`, or screenshot export.
- Design token map: color roles, typography scale, spacing rhythm, radius, outlines, shadows, icon style, motion timing, and safe-area rules.
- Component state matrix: default, hover, pressed, focused, selected, disabled, locked, loading, success, warning, error, empty, and notification states as relevant.
- Engine UI plan: reusable controls, Theme resources or equivalent style assets, signals/events, anchors/containers, focus behavior, input modes, and motion hooks.
- Screenshot parity report at target resolutions and gameplay overlay conditions.
- UI QA checklist for contrast, touch target size, focus order, text wrapping, localization tolerance, loading/error/empty states, reduced motion, and no layout jumps.

Rules:

- UI Programmer uses the `nextlevelbuilder/ui-ux-pro-max-skill` ideas as a design-to-implementation quality system adapted for game UI.
- Production UI uses SVG/icons or approved UI assets. Emoji is only a temporary demo/prototype placeholder unless the project intentionally chooses emoji as final UI identity.
- The implementation must remain original and project-specific; do not copy commercial UI layouts, icons, fonts, currencies, or proprietary screen compositions.

## Phase 3A: CSV Data Config

Outputs:

- CSV table schemas.
- Starter rows.
- Stable IDs.
- Reference rules.
- Validation plan.
- Runtime loading path.

Gate:

- Designer-editable values are not hardcoded when they should be data-driven.

## Phase 4: Technical Architecture

Outputs:

- Godot scene model.
- Module boundaries and ownership.
- Module contracts for public APIs, signals/events, input/output data, dependencies, and error handling.
- Resource/data architecture.
- Signal/autoload boundaries.
- Performance budget.
- Object pooling plan where needed.
- 2D scene/layer model, y-sort rules, TileMap/layer rules, sprite atlas/import settings, collision layers, and camera bounds by default.
- Simple premium 2D gate: visual sentence, complexity budget, readable silhouettes, controlled color roles, reusable asset/component plan, and famous-company reference decomposition without copying.

Gate:

- Implementation can start without guessing key architecture.
- Feature work is split into modules small enough to verify independently.
- 2D assets can be imported without guessing pivots, anchors, animation timing, collision, or layer order.
- Visual complexity has a clear reason and fits the target runtime budget.

## Phase 5: Vertical Slice

Outputs:

- Playable slice plan.
- Task list.
- Owners.
- Acceptance criteria.
- First QA smoke path.

Gate:

- A user can play the core loop end to end.

## Phase 6: Implementation

Outputs:

- Module breakdown.
- Module contracts.
- Code changes.
- Data table changes.
- Asset integration.
- Per-module verification.
- Integration verification.

Implementation task format:

- Goal.
- Owner agent.
- Input docs/files.
- Module boundary.
- Module contract.
- Files likely touched.
- Acceptance criteria.
- Verification.
- Risks.

Rules:

- Substantial feature work must be split into modules before coding.
- Do not implement major features as one large script, scene, prefab, widget, or mixed-responsibility change.
- Each module must pass its own focused verification before cross-module integration.
- Keep Gameplay, UI, Data, Audio, VFX, tools, and platform code separated unless a thin integration layer is explicitly required.

Gate:

- A module can be integrated only after its boundary, contract, files, and verification path are clear.

## Phase 7: QA and Tuning

Outputs:

- Smoke check.
- Playtest notes.
- Bug list.
- Balance notes.
- Performance notes where relevant.

Gate:

- Known issues are triaged and the feature is safe enough for its milestone.

## Phase 8: Milestone Review

Outputs:

- Ship/iterate/pivot decision.
- Next sprint priorities.
- Risks.

## Phase 9: Git Version Finish

Outputs:

- Verification summary.
- Commit.
- Push to `origin` when configured.
- Commit hash and branch report.

If push is blocked by authentication, network, divergence, large files, detached HEAD, suspected secrets, or missing remote, stop and report the exact blocker.

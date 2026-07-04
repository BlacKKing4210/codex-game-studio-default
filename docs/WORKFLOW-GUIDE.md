# Workflow Guide

This is the default Codex Game Studio delivery flow.

## Quick Start

1. Confirm whether this is a new project or an existing project.
2. If it is a new game, initialize Git, `.gitignore`, README, and remote when possible.
3. Establish concept, engine, and first playable target.
4. Keep configuration CSV-first where practical.
5. For formal design docs, create professional flowcharts and UI/UE diagrams before implementation handoff.
6. Implement in small feature batches with QA and version finish.

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
- 3-5 pillars.
- Anti-pillars.
- Reference principles without copying protected content.
- Visual-artifact plan for any formal 策划案/GDD: required gameplay/system flowcharts and UI/UE diagrams.

Gate:

- The concept is clear enough to prototype one risky assumption.
- Formal design-document work has identified which professional diagrams are required.

## Phase 2: Prototype

Outputs:

- One risky assumption.
- Minimum playable or testable experiment.
- Proceed/pivot/cut verdict.

Gate:

- The result answers the assumption clearly enough to continue or adjust.

## Phase 3: System Design

Outputs:

- Core loop.
- Weapons, enemies, upgrades, economy, difficulty.
- Tuning knobs and acceptance criteria.
- Gameplay/system flowchart source file and exported review image/PDF.
- UI/UE diagram source file and exported review image/PDF when the system has any screen, HUD, menu, onboarding, shop, progression, or decision interface.

Gate:

- Major gameplay systems have testable rules and known dependencies.
- A formal 策划案/GDD cannot move to architecture or implementation while its required flowchart or UI/UE diagram is missing.

## Design Document Visual Artifact Gate

This gate applies to any formal 策划案, GDD, system design document, feature specification, UI flow, onboarding flow, shop flow, combat flow, economy flow, or progression flow.

Required artifacts:

- Gameplay/system flowchart: player actions, system states, decision branches, rewards, failure/retry paths, and end conditions.
- UI/UE diagram: screen map, user journey, wireframes, interaction states, entry/exit paths, and key feedback.

Tooling rule:

- Use professional planning, product, UX, or diagram software such as Axure RP, Figma/FigJam, Miro, diagrams.net/draw.io, ProcessOn, Visio, MasterGo, Mockplus, or the project's approved equivalent.
- Markdown ASCII lines, Markdown tables, and Mermaid-only diagrams are temporary drafts only. They do not satisfy the final design-document gate.

Delivery rule:

- Editable source files live under `design/flows/` and `design/uiue/`.
- Exported PNG/PDF review files live under `design/exports/` or `docs/assets/`.
- The design document links to the exported diagrams and names the editable source files.

Review rule:

- Producer checks scope and completeness.
- Game Designer checks gameplay and system correctness.
- Art Director checks visual communication and readability.
- UI Programmer checks implementability of UI/UE flow.
- QA Lead checks whether the diagrams expose testable paths and edge cases.

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
- Resource/data architecture.
- Signal/autoload boundaries.
- Performance budget.
- Object pooling plan where needed.

Gate:

- Implementation can start without guessing key architecture.

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

- Code changes.
- Data table changes.
- Asset integration.
- Focused verification.

Implementation task format:

- Goal.
- Owner agent.
- Input docs/files.
- Files likely touched.
- Acceptance criteria.
- Verification.
- Risks.

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

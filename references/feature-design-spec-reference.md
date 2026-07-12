# Feature Design Specification Reference

Use this reference for every production feature, system design document, UI flow, feature adjustment, or request that needs a formal 策划案.

## Core Rule

Every feature must have an independent Word design document before implementation unless the user explicitly labels it as a throwaway prototype.

The user's reviewed and edited design is the source of truth. If the user changes the Word document or Figma/FigJam UE substantially, System Designer updates the feature spec, UE page explanations, data-source map, acceptance criteria, and downstream implementation tasks before coding continues.

## Default Route

Producer -> System Designer -> Game Designer -> Numerical Designer -> Art Director -> UI Artist -> UI Programmer -> Technical Director -> QA Lead.

Use the smallest needed subset:

- Pure feature/system spec: Producer -> System Designer -> QA Lead.
- Feature with gameplay rules: System Designer -> Game Designer -> QA Lead.
- Feature with numbers/economy/rewards: System Designer -> Numerical Designer -> Data Config Specialist -> QA Lead.
- Feature with pages/HUD/menu/popup: System Designer -> UI Artist -> UI Programmer -> QA Lead.
- Feature entering implementation: System Designer -> Technical Director -> Lead Programmer -> relevant Specialist -> QA Lead.

## Required Deliverables

- Feature Word design document: editable `.docx` source.
- PDF review export when useful for review/share.
- Figma/FigJam UE diagram for every page, popup, HUD panel, modal, or stateful screen.
- Exported UE review images/PDF.
- Written transition map that explains page entry, exit, back, close, confirm, cancel, failure, retry, and edge-case jumps.
- Per-page UE explanation that describes every information element on the page.
- Data-source map for every displayed data value.
- Acceptance checklist for design, UI/UE, data, implementation, and QA.
- User review notes and revision log.

## Word Design Document Minimum Structure

- Feature name and version.
- Owner route and review status.
- Goal and player value.
- Scope: included, excluded, future.
- Entry and unlock conditions.
- Rules and state changes.
- Page list and UE source links.
- Written transition map.
- Per-page explanation.
- Data-source map.
- Numerical rules or link to Numerical Designer table when needed.
- Error, empty, loading, locked, disabled, unaffordable, and edge states.
- Audio/VFX/UI feedback requirements.
- Implementation notes and module boundary.
- Acceptance criteria.
- QA checklist.
- User review notes and change log.

## UE Page Rules

Each page must have a Figma/FigJam UE diagram that expresses all information on the page, including:

- layout regions
- visible text
- buttons and controls
- resources and counters
- item/card/list/grid contents
- status labels
- empty/loading/error/locked states
- tooltips or help prompts
- notification badges
- input affordances
- page-level feedback

Markdown, Mermaid, ASCII sketches, or screenshots alone do not count as final UE diagrams.

## Per-Page Explanation

For each page, provide a table with:

- element id/name
- player-facing meaning
- display condition
- interaction behavior
- data source
- fallback or empty state
- owner system/module

Data-source examples:

- CSV table and column
- Godot Resource field
- save data field
- runtime state
- inventory/economy service
- localization key
- platform account data
- remote service/API if the project uses one

Do not write "from backend" or "from data" without naming the actual source or unresolved assumption.

## User Review Authority

- User-reviewed Word/Figma changes override earlier agent output.
- If user changes are small, update the affected spec sections and task cards.
- If user changes are large, return to System Designer for a revised design pass before implementation continues.
- Implementation and QA must cite the approved design version they are following.

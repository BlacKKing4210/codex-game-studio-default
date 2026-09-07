---
name: game-feature-design-docs
description: Create, revise, and validate game feature, system, activity, gameplay-subsystem, and UI/UE planning documents using the user-approved general or simple Word templates and editable Penpot diagrams. Use for Chinese or English feature planning, review-only design proposals, implementation-ready specifications, system or activity plans, UI/UE explanations, or when deciding whether work needs a lightweight review document or the general final implementation template.
---

# Game Feature Design Docs

Create one readable game-feature document matched to its declared class from approved project sources. A `REVIEW_ONLY` document supports design decisions only; an `IMPLEMENTATION_CONTRACT` must be implementation-ready. Use this Skill with `game-studio-orchestrator` and `game-project-control-plane`; do not replace their producer ownership, read-only receipt, write-lock, or evidence gates.

## Word-Only Document Delivery

- Deliver every formal, user-facing, or reviewable project document only as an editable Microsoft Word `.docx`.
- Do not create, export, return, archive, publish, or attach PDF documents or PDF review copies.
- Render DOCX pages to PNG for visual QA. If a renderer internally requires a temporary PDF, keep it outside project/output/version-control paths and remove it after PNG inspection.
- Export editable-design and diagram review images as PNG only. Historical PDFs may be read as source evidence, but never regenerate or include them in a new delivery bundle.
- Keep Markdown, CSV, JSON, YAML, source code, and databases only for their engineering or machine-readable roles; they do not replace the formal Word document.

## Select Document Class And Exactly One Template

Classify both the delivery phase and the feature complexity before selecting a template:

- `REVIEW_ONLY`: align the player experience, core rules, UE, configuration shape, and visible page behavior. It does not authorize implementation or claim implementation readiness.
- `IMPLEMENTATION_CONTRACT`: serve as the formal source for engineering, content, UI/art, QA, milestone, or release work.
- `NARROW`: one clear loop with small, enumerable dependencies, states, data, and boundaries.
- `MATERIAL`: cross-system, multi-page, multi-state, configuration-heavy, interruption-sensitive, economically material, or otherwise open to more than one reasonable implementation.

Use this matrix:

| Phase | Narrow | Material |
|---|---|---|
| `REVIEW_ONLY` | Simple template | Simple template may be used as a visibly marked review draft; record missing final blocks and the mandatory upgrade trigger |
| `IMPLEMENTATION_CONTRACT` | Simple template only when every simple-final condition passes | General template |

General template: `assets/general-feature-design-template.docx`.

Use it for every material implementation contract and whenever any of these conditions applies:

- new or cross-system behavior whose ownership or authority is not already settled;
- more than one page, popup, HUD state, or child flow with non-trivial transitions;
- several material states such as locked, loading, empty, failed, completed, claimed, sold out, or expired;
- combat, progression, economy, probability, reward, refresh, batch, reset, refund, or persistence rules;
- multiple configuration tables, save fields, runtime services, remote states, or referential validation chains;
- interruption, reconnect, restart, cross-day, concurrency, rollback, or expiry risk;
- several implementation, UI, art, audio, numerical, or QA owners;
- a programmer or QA reviewer could reasonably interpret state, timing, data authority, or boundary behavior in more than one way.

Simple template: `assets/simple-feature-design-template.docx`.

Use it as a final implementation contract only when every condition below is true:

- one narrow player loop;
- one main page or a small number of tightly related states;
- one table or a few directly mapped configuration fields;
- dependencies and boundaries are small and enumerable;
- no material cross-system, economy, probability, persistence, reconnect, batch, or concurrency ambiguity;
- implementation and QA remain obvious after a short read.

A material feature may start with a simple `REVIEW_ONLY` document when the immediate decision needs only experience, rules, UE, configuration shape, and visible behavior. Mark the document `REVIEW_ONLY`, list every omitted final block, name an owner and close condition, and state `NOT AUTHORIZED FOR IMPLEMENTATION`. Before implementation continues, migrate it to the general template; never relabel the same incomplete review draft as final.

Choose by phase and complexity, never by page count. If uncertain about an implementation contract, use the general template. Read `references/feature-design-document-standard.md`, especially sections `3` and `3.1`, before selecting.

Read `references/feature-design-document-standard.md` before authoring or reviewing either template.

## Simple Feature Planning Flow

When `simple` is selected, follow this fixed order:

1. Record the read-only intake receipt, existing runtime/UI baseline, `document_class`, and whether the document is authorized for implementation.
2. State one player-facing memory point and three to five observable rules.
3. Inventory every key page, popup, HUD, result screen, and necessary state; create one editable UE Board for each, then place those page UE Boards together on one Penpot root board and connect them into the complete game-running flow. Show entry, page operations, operating loop, feedback, branches, results, return, and re-entry. Label arrows with player actions, system events, or conditions; do not substitute plain page-name boxes, a thumbnail wall, implementation classes, or event plumbing.
4. When UI or HUD exists, use simple shapes to show in-game placement, information priority, and applicable default, feedback, transition, and terminal/special states. Label it low fidelity, not final art.
5. Name exact configuration sources and only the hard timing/data contracts needed for consistent behavior.
6. Cover boundaries, invalid configuration, QA cases, and the difference between document approval and runtime completion. For a material `REVIEW_ONLY` draft, identify the missing final-contract blocks and the exact migration trigger instead of pretending they are complete.
7. Require lead-design and producer document-level reviews. Keep Penpot, implementation, and QA gates independently visible.
8. Deliver the reviewed DOCX, editable Penpot, the artifact register, clear PNG exports, configuration paths, and review status.

If editable Penpot cannot be created, saved, edited, or read back, a local review graphic may be delivered as a draft, but the Penpot gate stays `Pending`. If the feature grows beyond the simple-final limits, or a material review draft approaches implementation, migrate to `general` before implementation continues.

Read `references/feature-design-document-standard.md`, section `3.1`, for the detailed universal gate.

## Build The Document

1. Record a read-only receipt for the approved objective, scope, non-goals, owner, dependencies, output path, current configuration source, acceptance, and intended evidence.
2. Record the phase/complexity classification, choose `general` or `simple`, and record the reasons, implementation authority, and migration trigger.
3. Copy the selected asset into the project. Never edit the Skill asset in place.
4. Fill the version-control, version-history, and development-plan tables first.
5. Replace every blue bracketed field. Use `Pending` plus an owner and due date when an approved fact is missing; never invent it.
6. Keep real Word heading styles and refresh the automatic table of contents.
7. Name every configuration source exactly: for example `config/csv/items.csv::price`, `ResourceName.field`, `SaveData.field`, or `Service.event/state`.
8. Build the page inventory and per-page UE Frames first. Assemble those Frames into one root UE total-flow canvas that demonstrates how the game actually runs from entry through operation, feedback, branches, results, return, and re-entry.
9. Create the other required editable Penpot artifacts and place the artifact register, source links, versions, owners, object references, local source backup, and PNG review exports in the document.
10. For an `IMPLEMENTATION_CONTRACT`, keep Word, the UE total flow, per-page UE, configuration, implementation tasks, and QA acceptance on one consistent page-ID and state model. For `REVIEW_ONLY`, keep the included pages and states consistent and list omitted implementation and QA blocks in the upgrade checklist.
11. Use Documents to render every DOCX page. Fix clipping, table breaks, missing glyphs, unreadable diagrams, stale fields, or pagination defects.
12. Return the reviewed DOCX, editable Penpot source and register, PNG diagram exports, exact configuration sources, and the evidence required by the declared document class. A `REVIEW_ONLY` delivery must show its review status, omitted final-contract blocks, owner, close condition, and migration trigger.

## Mandatory UE Total Flow

Both the general and simple templates require a UE total flow. It is one editable Penpot root board composed from the actual UE Boards for every key page, popup, HUD, result screen, and applicable page state.

Build it in this order:

1. assign a unique page ID to every key page and state group;
2. create the per-page UE Frame with information hierarchy, main controls, and key feedback;
3. place all page UE Frames on one root canvas;
4. connect the real player and system sequence, including operating loops and branches;
5. label every connection with the player action, system event, or condition;
6. verify entry, success, failure, retry, back, close, cancel, return, interruption, re-entry, and terminal paths as applicable;
7. reconcile the canvas against the page list, written transition map, and per-page explanations.

Plain page-name boxes, isolated wireframes, unordered screenshot collages, text-only arrows, state machines, and implementation event diagrams do not satisfy this requirement. A large feature may link to detailed subflow Frames, but it still needs one readable root UE total flow with explicit subflow entry and return points.

## Penpot Gate

Create final system, UE, swimlane, state, and page-spec diagrams in editable Penpot.

- General documents require a system framework, the page-Frame-based UE total flow, overall system logic or swimlane diagram, and page-spec diagrams when UI exists.
- Simple documents require the same page-Frame-based UE total flow and page-spec diagram when UI exists, with only the number of pages and branches reduced.
- Label every arrow with the player action or system event.
- Cover entry, main path, back, close, confirm, cancel, success, failure, retry, empty, locked, insufficient-resource, interruption, refresh, expiry, restart, and reconnect states when applicable.
- For every page element, explain meaning, display condition, interaction, data source, fallback state, and owner module.
- Use Mermaid, ASCII, text arrows, screenshots alone, and Visio-only diagrams only as drafts. They do not satisfy final delivery.
- Include a `Penpot UE & UI/UX Artifact Register` with `penpot_url`, `workspace_id`, `project_id`, `file_id`, `page_or_board`, `object_refs`, `source_version`, `owner`, `review_state`, `coverage`, and `local_source_backup`.
- Verify authenticated edit access and save/reopen or object-level readback. An open tab, import attempt, SVG, PNG, or Mermaid source alone does not clear the gate.
- Preserve accepted historical Figma/FigJam artifacts as historical evidence. A non-Penpot tool is allowed for new work only through an explicit producer decision recorded in the project profile and affected formal source.

## Source Authority

Treat the producer-reviewed Word document, editable Penpot file, and current project configuration as the source of truth.

- User edits override template examples and earlier agent output.
- User-edited configuration values override template placeholders.
- Substantial Word or Penpot changes require synchronized rules, data-source maps, acceptance criteria, and downstream task updates before implementation continues.
- Mark superseded rules in the version history; do not leave conflicting current rules in different artifacts.

## Completion Gate

Use the completion label that matches the declared class:

- `REVIEW_ONLY` may be marked `方向评审通过` only when the intended decision is resolved, every included rule/page/configuration shape is internally consistent, all omitted final-contract blocks and owners are listed, `NOT AUTHORIZED FOR IMPLEMENTATION` remains visible, and the latest DOCX has passed full-page PNG inspection.
- `IMPLEMENTATION_CONTRACT` may be marked complete only when all conditions below pass:

- a reader can understand the player value, main loop, and system structure within one minute;
- engineering can locate states, events, data sources, refresh timing, persistence, and boundaries;
- numerical design can locate every tunable field, unit, default, range, and formula owner;
- UI and art can locate every page, element, state, Penpot object, specification, and priority;
- QA can derive normal, boundary, empty, full, interrupted, failure, retry, and regression cases;
- the UE total flow contains every key page UE Frame and visibly explains how the game runs; page IDs, transitions, arrow labels, branches, returns, and per-page explanations agree;
- all Penpot sources are editable, object references pass readback, and their exports match the document version;
- every unresolved decision is marked `Pending` with an owner;
- the latest DOCX has passed full-page PNG visual inspection.

Keep project-specific facts out of this Skill. Put them in the copied document, project configuration, and formal project sources.

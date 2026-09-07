---
name: artifact-template-game-feature-design-general
description: "Create a document using the Game Feature Design General template and its retained reference file. Use when the user selects this template, names Game Feature Design General, or explicitly invokes $artifact-template-game-feature-design-general. Create a complete cross-system Word-only game feature specification with editable Penpot diagrams, PNG review images, system logic, configuration, UI, QA, and DOCX as the only formal document deliverable."
---

# Game Feature Design General

Create a document from this template. Keep the reference file unchanged.

## Workflow

1. Read `artifact-template.json` and resolve its paths relative to this skill directory.
2. Load [@documents](plugin://documents@openai-primary-runtime) and invoke its reference/template workflow with the retained file.
3. Treat the user's prompt and available sources as the content input. Do not invent facts merely to fill a template slot.
4. Clone or import the reference instead of replacing its visual system with generic defaults.
5. Render and verify the finished document, then return the final artifact.

## Fidelity

Preserve page setup, sections, styles, lists, tables, headers, footers, and recurring page elements.

User instructions control requested content and explicit deviations. The retained reference controls layout and formatting where the user has not requested a change.

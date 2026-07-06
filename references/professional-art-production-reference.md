# Professional Art Production Reference

Use this reference when a task involves art direction, concept art, scene art, UI visual design, mood, atmosphere, key art, art bible, visual polish, generated art direction, or asset quality review.

## Core Rule

Sprite Forge is an execution and handoff pipeline, not a replacement for professional art judgment.

Before generating or integrating final art, route visual decisions through the relevant professional art roles:

Producer -> Creative Director -> Art Director -> Visual Development Artist -> Concept Artist / Environment Artist / UI Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Engine Specialist -> QA Lead.

Use the smallest needed route for the task.

## Roles

| Agent | Owns | Professional Skills | Outputs |
|---|---|---|---|
| Art Director | Visual identity, art bible, originality gate, readability, quality bar, final sign-off | Style cohesion, visual hierarchy, production constraints, art critique | Art bible, quality rubric, asset standards, sign-off notes |
| Visual Development Artist | Mood, atmosphere, palette, lighting, key art, composition, style exploration | Mood boards, color scripts, lighting direction, composition design | Mood board, color script, key art, lighting notes |
| Concept Artist | Characters, enemies, props, weapons, silhouettes, shape language, turnarounds | Silhouette design, shape language, production callouts, pose/expression sheets | Concept sheets, variants, turnarounds, callouts |
| Environment Artist | Scenes, maps, arenas, rooms, background, props/blockers, set dressing | Scene composition, environmental storytelling, perspective, depth, prop layering | Environment sheets, map/scene breakdowns, prop plans |
| UI Artist | UI visual language, icons, panels, buttons, typography direction, visual states | UI style frames, iconography, contrast/readability, state sheets | UI style frames, icon sets, component visual states |
| 2D Animation Specialist | Sprite animation states, frame timing, action readability, procedural-motion blend | Timing charts, frame budgets, anticipation/recovery, hit reaction | Animation list, timing chart, transition notes |
| 2D Technical Artist | Sprite import, atlases, TileMaps, y-sort, collision, materials, VFX, engine handoff | Atlas planning, import settings, TileMap/layer rules, runtime readability | 2D technical spec, atlas plan, import notes |
| Sprite Forge Specialist | Generated asset execution, cleanup, slicing, metadata, previews, QC, engine handoff | generate2dsprite, generate2dmap, chroma-key QC, frame metadata | Generated assets, previews, metadata, handoff notes |

## Required Art Deliverables

For professional visual work, produce:

- Art brief: gameplay purpose, target player, platform, camera/view, intended size, and constraints.
- Reference board: approved references plus explicit anti-copying notes.
- Visual direction: shape language, palette, lighting, material, texture density, composition, mood, and atmosphere.
- Production sheets: variants, scale, callouts, layers, states, and usage notes.
- Readability pass: silhouette, value grouping, color separation, UI contrast, small-screen checks.
- Engine handoff: file format, resolution, layer structure, pivots/anchors, collision or safe-area notes, import path, naming.
- QC verdict: approve, revise, or reject with concrete reasons.

## Route By Work Type

| Work Type | Route |
|---|---|
| Overall art style / art bible | Creative Director -> Art Director -> Visual Development Artist -> QA Lead |
| Character / enemy / prop / weapon concept | Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Engine Specialist -> QA Lead |
| Scene / map / environment / atmosphere | Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Engine Specialist -> QA Lead |
| UI visual design / HUD / menu / shop / result screen | Art Director -> UI Artist -> UI Programmer -> Engine Specialist -> QA Lead |
| Generated asset pack | Art Director -> relevant art specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Engine Specialist -> QA Lead |
| Art quality review | Art Director -> relevant art specialist -> QA Lead |

## Quality Gates

Professional art work is not done until:

- The visual direction matches the game's promise and target player.
- The style is original and does not copy commercial names, logos, characters, icons, exact layouts, or proprietary assets.
- The asset is readable at intended gameplay size and camera distance.
- Character/enemy/prop silhouettes are distinguishable.
- Scene composition supports gameplay, navigation, collision, and spawn readability.
- UI visual states are clear: default, hover, pressed, selected, disabled, locked, loading, error, success.
- Mood, color, and lighting are consistent across screens and scenes.
- 2D animation and technical-art notes are clear enough for implementation without guessing.

## Sprite Forge Handoff

Sprite Forge receives approved art direction, not vague style wishes.

Minimum handoff into Sprite Forge:

- Approved art brief.
- Visual direction and reference board.
- Prompt constraints.
- Exact asset list.
- Canvas size, frame size, grid, transparent or magenta background requirements.
- Layering and naming rules.
- QC checklist.
- 2D technical handoff requirements.

If art direction is missing, route back to Art Director and the relevant professional art specialist before generation.

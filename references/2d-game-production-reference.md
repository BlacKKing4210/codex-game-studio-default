# 2D Game Production Reference

Use this reference for any 2D-first project, sprite-based game, pixel-art-style game, hand-drawn 2D game, TileMap project, side scroller, top-down game, card/board/grid game, visual novel, 2D action game, survivorlike arena, or 2D UI-heavy game.

## Core Rule

Codex Game Studio defaults to 2D-first production unless the user or existing project explicitly chooses 3D, 2.5D, VR/AR, or another rendering model.

2D-first does not mean low quality. It means production decisions optimize for sprites, layered scenes, readable silhouettes, efficient atlases, 2D animation, TileMaps, parallax, UI clarity, collision shapes, and mobile-friendly performance.

## Simple High-Quality 2D Default

For most projects, aim for simple premium 2D: clean silhouettes, controlled color roles, clear UI hierarchy, restrained scene detail, efficient animation, and reusable production components.

Do not increase complexity to look professional. Use professional craft to make simple decisions feel intentional:

- Fewer shapes, better proportions.
- Fewer colors, clearer roles.
- Fewer layers, stronger focal hierarchy.
- Fewer animation states, stronger timing.
- Fewer UI component families, stronger consistency.
- Fewer custom assets, stronger reuse and polish.

Primary learning references should come from well-known companies and durable 2D games: Nintendo for broad-audience readability and playful polish; Supercell for mobile-scale silhouettes and chunky UI clarity; Ubisoft Montpellier's Rayman Legends for expressive 2D motion; Blizzard's Hearthstone for tactile UI hierarchy; King for casual icon/readability systems; SEGA and Capcom for action clarity; Monument Valley, Hollow Knight, Celeste, and Dead Cells for high-identity 2D with constrained production.

References are principle studies only. Do not copy exact characters, UI layouts, icons, colors, level motifs, effects, or proprietary assets.

## Default 2D Route

Producer -> Creative Director -> Art Director -> Technical Director -> 2D Technical Artist -> relevant art/programming specialist -> Godot Specialist -> QA Lead.

Use the smallest needed branch:

- 2D project setup: Technical Director -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D character/enemy/prop production: Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D scene/map/level production: Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead.
- 2D animation and action feedback: Art Director -> 2D Animation Specialist -> Gameplay Programmer -> Godot Specialist -> QA Lead.
- 2D UI screens: Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead.
- 2D performance review: Technical Director -> 2D Technical Artist -> Performance Analyst -> Godot Specialist -> QA Lead.

## Agents And Learned Skills

| Agent | 2D Learned Skills |
|---|---|
| Art Director | simple-premium 2D style bible, famous-company reference decomposition, silhouette readability, palette control, complexity budget, sprite quality gate |
| Visual Development Artist | simple-premium 2D mood boards, color scripts, lighting/value grouping, focal hierarchy, parallax atmosphere |
| Concept Artist | simple-premium sprite-ready silhouettes, small shape vocabularies, front/side/back callouts, small-size readability |
| Environment Artist | simple-premium TileMap planning, layered scene composition, prop-density control, parallax, blockers, spawn readability |
| UI Artist | simple-premium 2D HUD/menu style frames, iconography, readable states, mobile-safe component systems |
| Sprite Forge Specialist | generate2dsprite, generate2dmap, prompt discipline, sheet cleanup, slicing, metadata, previews |
| 2D Animation Specialist | simple-premium sprite animation, essential state budgets, timing charts, action states, pose readability, procedural-motion blend |
| 2D Technical Artist | simple-premium sprite import, atlas planning, TileMap pipeline, y-sort, collision, materials, VFX, runtime complexity checks |
| Godot Specialist | Sprite2D, AnimatedSprite2D, AnimationPlayer, TileMapLayer, CanvasLayer, Control, Resource, Signal |
| Gameplay Programmer | 2D movement, hitboxes/hurtboxes, kinematic collision, pickups, camera feedback |
| Performance Analyst | draw calls, texture memory, overdraw, object pooling, dense sprite stress checks |

## Required 2D Deliverables

- 2D art brief: camera/view, target resolution, intended on-screen size, readability constraints.
- Sprite spec: canvas size, frame size, grid, pivot, anchor, feet line, hitbox/hurtbox notes.
- Animation spec: state list, frame count, FPS, loop mode, contact frames, transition rules.
- Scene spec: layer order, y-sort rules, collision layers, trigger zones, spawn zones, camera bounds.
- Atlas/import spec: filtering, compression, mipmaps, texture page size, naming, folder paths.
- VFX/material spec: hit flash, outline, dissolve, palette swap, particles, trails, shader rules.
- QA preview: still preview, GIF/video preview, layered map preview, or in-engine scene check.

## 2D Quality Gates

- The visual idea can be explained in one sentence.
- The design passes the simple-premium gate: readable, memorable, original, reusable, and not overcomplicated.
- Reference decomposition focuses on principles, not visual complexity or surface style.
- Silhouettes stay readable at gameplay size.
- Player, enemy, projectile, pickup, hazard, and UI colors are separated.
- Sprite pivots, anchors, and feet lines are stable.
- Animation timing communicates anticipation, impact, and recovery.
- Layer order, parallax, y-sort, collision, and spawn zones are clear.
- UI stays readable over gameplay backgrounds.
- Texture memory, draw calls, particles, and object counts fit the target platform.
- Generated assets follow approved art direction and have deterministic cleanup/QC.
- The design learns from market-leading examples without copying exact silhouettes, palettes, UI layouts, icons, or proprietary assets.

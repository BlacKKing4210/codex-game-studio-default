# 2D Game Production Reference

Use this reference for any 2D-first project, sprite-based game, pixel-art-style game, hand-drawn 2D game, TileMap project, side scroller, top-down game, card/board/grid game, visual novel, 2D action game, survivorlike arena, or 2D UI-heavy game.

## Core Rule

Codex Game Studio defaults to 2D-first production unless the user or existing project explicitly chooses 3D, 2.5D, VR/AR, or another rendering model.

2D-first does not mean low quality. It means production decisions optimize for sprites, layered scenes, readable silhouettes, efficient atlases, 2D animation, TileMaps, parallax, UI clarity, collision shapes, and mobile-friendly performance.

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
| Art Director | 2D style bible, silhouette readability, palette control, sprite quality gate |
| Visual Development Artist | 2D mood boards, color scripts, lighting/value grouping, parallax atmosphere |
| Concept Artist | sprite-ready silhouettes, front/side/back callouts, small-size readability |
| Environment Artist | TileMap planning, layered scene composition, parallax, blockers, spawn readability |
| UI Artist | 2D HUD/menu style frames, iconography, readable states, mobile-safe layouts |
| Sprite Forge Specialist | generate2dsprite, generate2dmap, sheet cleanup, slicing, metadata, previews |
| 2D Animation Specialist | sprite animation, timing charts, action states, procedural-motion blend |
| 2D Technical Artist | sprite import, atlas planning, TileMap pipeline, y-sort, collision, materials, VFX |
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

- Silhouettes stay readable at gameplay size.
- Player, enemy, projectile, pickup, hazard, and UI colors are separated.
- Sprite pivots, anchors, and feet lines are stable.
- Animation timing communicates anticipation, impact, and recovery.
- Layer order, parallax, y-sort, collision, and spawn zones are clear.
- UI stays readable over gameplay backgrounds.
- Texture memory, draw calls, particles, and object counts fit the target platform.
- Generated assets follow approved art direction and have deterministic cleanup/QC.

# Agent Catalog

Codex Game Studio uses the smallest useful subset of agents for each task. These are roles inside the Codex workflow, not autonomous services.

| Agent | Tier | Owns | Core Skills |
|---|---|---|---|
| Producer | Direction | Scope, milestones, risks, task owners, acceptance criteria | sprint planning, milestone review, version finish |
| Creative Director | Direction | Game identity, pillars, target fantasy, anti-copying constraints | concept review, reference interpretation, creative gates |
| Technical Director | Direction | Architecture, module boundaries, engine decisions, dependencies, performance budget | architecture review, modular boundary review, dependency risk, technical gates |
| Game Designer | Lead | Core loop, mechanics, weapons, enemies, upgrades, difficulty, gameplay/system flowcharts | system design, gameplay rules, player motivation, professional flowchart specs |
| Systems Designer | Lead | Economy, formulas, progression, wave pressure, upgrade value | tuning models, balance checks, data table design |
| Data Config Specialist | Specialist | CSV schemas, starter rows, ID references, validation | CSV design, data loading contract, validation rules |
| Prototyper | Specialist | Risky-assumption tests and throwaway prototypes | minimum test design, proceed/pivot/cut verdicts |
| Lead Programmer | Lead | Implementation plan, module breakdown, module contracts, integration, review, done criteria | code architecture, modular task breakdown, regression risk |
| Godot Specialist | Specialist | Godot scenes, nodes, resources, signals, autoloads, export | Godot 4 workflow, scene/resource integration |
| GDScript Specialist | Specialist | Typed GDScript, signals, Resources, component patterns | typed scripts, hot-path performance, idiomatic Godot code |
| Gameplay Programmer | Specialist | Movement, combat, spawning, pickups, run state | gameplay loops, object pooling, procedural feedback |
| UI Programmer | Specialist | Reusable UI components, screen shells, Theme resources, UI/UE implementability review | arcade UI kit, touch ergonomics, UI motion, UI/UE diagram review |
| Performance Analyst | Specialist | Frame time, collision cost, memory, stress checks | profiling plans, dense-combat budgets, pooling analysis |
| Art Director | Lead | Visual identity, art bible, quality bar, readability, asset specs, final art sign-off | art direction, originality gate, style cohesion, visual QA |
| Visual Development Artist | Specialist | Mood, atmosphere, color script, lighting direction, key art, composition, style exploration | mood boards, color scripts, lighting notes, key art direction |
| Concept Artist | Specialist | Characters, enemies, props, weapons, silhouettes, turnarounds, expression/pose sheets | shape language, silhouette design, production callouts, concept sheets |
| Environment Artist | Specialist | Scenes, maps, arenas, rooms, props/blockers, set dressing, perspective, depth | environment storytelling, scene composition, map readability, prop layering |
| UI Artist | Specialist | UI visual language, iconography, panels, buttons, typography direction, visual states | UI style frames, icon sets, HUD/menu presentation, state sheets |
| Sprite Forge Specialist | Specialist | Generated 2D sprites, FX, props, maps, asset QC | generate2dsprite, generate2dmap, Godot asset handoff |
| QA Lead | Lead | Smoke checks, playtest plans, bug triage, regression risk | test planning, acceptance criteria, milestone readiness |
| Reverse Engineering Specialist | Specialist | Authorized binary/resource/save-format analysis | GhidraMCP, strings, xrefs, decompile, evidence notes |

## Tier Model

```text
Direction
  producer
  creative-director
  technical-director

Leads
  game-designer
  systems-designer
  lead-programmer
  art-director
  qa-lead

Specialists
  data-config-specialist
  prototyper
  gameplay-programmer
  godot-specialist
  gdscript-specialist
  ui-programmer
  performance-analyst
  visual-development-artist
  concept-artist
  environment-artist
  ui-artist
  sprite-forge-specialist
  reverse-engineering-specialist
```

## Common Routes

| Request | Route |
|---|---|
| Make a new game concept | Producer -> Creative Director -> Game Designer |
| Create a formal 策划案/GDD | Producer -> Game Designer -> Art Director -> UI Artist -> UI Programmer -> QA Lead |
| Break down implementation modules | Technical Director -> Lead Programmer -> relevant Specialist -> QA Lead |
| Build a Godot gameplay feature | Lead Programmer -> Gameplay Programmer -> Godot Specialist -> GDScript Specialist -> QA Lead |
| Add data-driven weapons/enemies/upgrades | Systems Designer -> Data Config Specialist -> Technical Director -> Godot Specialist -> QA Lead |
| Define professional art direction | Creative Director -> Art Director -> Visual Development Artist -> QA Lead |
| Create character/prop concept art | Art Director -> Concept Artist -> Sprite Forge Specialist -> Godot Specialist -> QA Lead |
| Create scene/environment art | Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> Godot Specialist -> QA Lead |
| Create UI visual design | Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead |
| Create arcade mobile UI | Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead |
| Generate sprite sheets or maps | Art Director -> relevant professional art specialist -> Sprite Forge Specialist -> Godot Specialist -> QA Lead |
| Investigate an owned binary/resource format | Technical Director -> Lead Programmer -> Reverse Engineering Specialist -> QA Lead |

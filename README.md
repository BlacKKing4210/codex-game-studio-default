# Codex Game Studio Default

Turn a single Codex session into a focused indie game studio workflow.

25 core agents. 19 workflow lanes. Thirty-minute project management. Feature Word design specs. Per-page Figma/FigJam UE diagrams. 2D-first production. Simple premium visual design. Professional art production. UI mockup-to-engine implementation. Modular implementation. Godot-first defaults. CSV-driven game data. Sprite Forge art handoff. Git version finish.

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="SKILL.md"><img src="https://img.shields.io/badge/Codex%20Skill-ready-green" alt="Codex Skill Ready"></a>
  <a href="docs/AGENT-CATALOG.md"><img src="https://img.shields.io/badge/agents-25-blueviolet" alt="25 Agents"></a>
  <a href="docs/WORKFLOW-GUIDE.md"><img src="https://img.shields.io/badge/workflows-19-orange" alt="19 Workflows"></a>
  <a href="docs/CSV-DATA-CONFIG.md"><img src="https://img.shields.io/badge/data-CSV%20first-yellow" alt="CSV First"></a>
</p>

---

## Why This Exists

Solo game development with AI is powerful, but a general chat can drift: hardcoded tuning values, unclear ownership, monolithic scripts, weak 2D production rules, weak art direction, flat atmosphere, generic UI visuals, missing professional design diagrams, missing QA, weak asset handoff, and no clean version finish.

**Codex Game Studio Default** gives Codex a small but useful studio structure for game work. It defaults to 30-minute task-plan inspection, interruption recovery, isolated task threads, 2D-first production, player-feedback-informed design, feature Word design specs, per-page Figma/FigJam UE diagrams, simple premium visual design, UI mockup-to-engine implementation, and fast demo placeholders while keeping the user as final decision maker and routing tasks through project management, production, system design, game design, numerical design, programming, master-level art direction, concept art, environment art, UI art, 2D animation, 2D technical art, QA, Godot, GDScript, CSV data, UI implementation, procedural motion, Sprite Forge asset generation, and authorized reverse-engineering gates.

This repository is modeled after the studio-template idea of Claude Code Game Studios, adapted for Codex Skill usage and the local `codex-game-studio-default` workflow.

---

## What's Included

| Category | Count | Description |
|---|---:|---|
| **Core Agents** | 25 | Producer, Project Manager, directors, System Designer, Numerical Designer, Game Designer, programmers, Godot/GDScript/UI specialists, professional art specialists, 2D specialists, Sprite Forge, QA, and reverse engineering |
| **Workflow Lanes** | 19 | Project management, concept, prototype, feature design specs, system design, professional design artifacts, UI implementation, simple premium 2D visual design, 2D production, professional art production, CSV config, architecture, vertical slice, modular implementation, QA, UI, Sprite Forge, reverse engineering, version finish |
| **Codex Skill** | 1 | Root-level `SKILL.md` with Codex-triggering metadata and progressive references |
| **References** | 11 | Detailed guides for project management, game studio routing, feature design specs, master-level visual design, 2D production, professional art production, UI implementation, Sprite Forge, CSV config, UI core, and authorized reverse engineering |
| **Framework Docs** | 1 catalog | Agent and workflow registry for review, extension, and future testing |

## Studio Hierarchy

```text
Tier 1 - Direction
  producer
  project-manager
  creative-director
  technical-director

Tier 2 - Leads
  game-designer
  system-designer
  numerical-designer
  lead-programmer
  art-director
  qa-lead

Tier 3 - Specialists
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
  2d-animation-specialist
  2d-technical-artist
  sprite-forge-specialist
  reverse-engineering-specialist
```

## Agent Routing

| Work Type | Route |
|---|---|
| Broad game project | Producer -> relevant leads -> QA Lead |
| Scheduled task monitoring and continuation | Producer -> Project Manager -> relevant task thread -> QA Lead |
| Formal 策划案/GDD | Producer -> System Designer -> Game Designer -> Numerical Designer -> Art Director -> UI Artist -> UI Programmer -> QA Lead |
| Feature Word design spec | Producer -> System Designer -> Game Designer -> Numerical Designer -> UI Artist -> UI Programmer -> Technical Director -> QA Lead |
| Godot implementation | Lead Programmer -> Godot Specialist -> GDScript Specialist -> QA Lead |
| Configurable numeric/balance systems | Numerical Designer -> Data Config Specialist -> Technical Director -> Godot Specialist -> QA Lead |
| 2D project setup | Technical Director -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| 2D character/prop/animation production | Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| 2D scene/TileMap production | Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| 2D animation/action feedback | Art Director -> 2D Animation Specialist -> Gameplay Programmer -> Godot Specialist -> QA Lead |
| Professional art direction | Creative Director -> Art Director -> Visual Development Artist -> QA Lead |
| Character/prop concept art | Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| Scene/environment art | Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| UI visual design | Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead |
| UI mockup/effect implementation | Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead |
| Simple premium 2D visual direction | Creative Director -> Art Director -> relevant master art specialist -> 2D Technical Artist -> QA Lead |
| Mobile arcade UI | Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead |
| Procedural gameplay feedback | Art Director -> Gameplay Programmer -> Godot Specialist -> QA Lead |
| Generated 2D art | Art Director -> relevant professional art specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| Authorized binary analysis | Technical Director -> Lead Programmer -> Reverse Engineering Specialist -> QA Lead |

See [docs/AGENT-CATALOG.md](docs/AGENT-CATALOG.md) for each agent's responsibilities and skills.

## Default Workflow

1. **Git and GitHub Startup** - initialize or verify Git, ignore files, README, first commit, private GitHub origin where possible.
2. **Project Management Startup** - canonical task plan, stable Task IDs, dependencies, conflict scopes, thread registry, and optional 30-minute automation.
3. **Concept** - promise, target player, player feedback discovery, pillars, anti-pillars, reference principles.
4. **Prototype** - one risky assumption, minimum test, emoji/SVG demo placeholders where assets are missing, proceed/pivot/cut verdict.
5. **System Design** - feature Word design docs, core loop, mechanics, content rules, economy, difficulty, professional flowcharts, per-page Figma/FigJam UE diagrams, written page transitions, per-page explanations, and data-source maps.
6. **CSV Data Config** - schemas, starter rows, IDs, validation rules, loading path.
7. **Technical Architecture** - Godot architecture, module boundaries, data/resources, 2D scene/layer model by default, performance budget.
8. **Vertical Slice** - playable slice plan, tasks, owners, dependencies, conflict scopes, and acceptance criteria.
9. **Implementation** - modular code, assets, data, isolated task threads, per-module verification, and integration.
10. **QA and Tuning** - smoke checks, playtest notes, bugs, balance notes.
11. **Milestone Review** - ship/iterate/pivot decision and next sprint.
12. **Git Version Finish** - verify, commit, push, report commit hash.

Full guide: [docs/WORKFLOW-GUIDE.md](docs/WORKFLOW-GUIDE.md).

## Codex Skill Usage

This repository can be used as a Codex Skill folder because it contains root-level [SKILL.md](SKILL.md).

To install manually:

```powershell
git clone git@github.com:BlacKKing4210/codex-game-studio-default.git $env:USERPROFILE\.codex\skills\codex-game-studio-default
```

Then use it naturally:

```text
Use $codex-game-studio-default to plan a Godot survivorlike vertical slice.
```

The skill is designed for implicit use on game-development tasks, including Chinese prompts such as `游戏开发`, `制作游戏`, `Godot游戏`, `土豆兄弟like`, `幸存者like`, `美术资源`, `系统策划`, `功能策划案`, `数值策划`, `数值设计`, and `游戏测试`.

## Project Structure

```text
SKILL.md                            # Codex Skill entry point
AGENTS.md                          # Project-level Codex instructions
agents/                            # Codex skill UI metadata and specialist notes
references/                        # Progressive-disclosure reference docs
docs/                              # Human-facing guides and catalogs
design/registry/                   # Design entity registry stubs
production/                        # Review mode, canonical task plan, and sprint state
Codex Game Studio Framework/        # Agent/workflow catalog for testing and extension
```

## Core Defaults

- **Dimension**: 2D-first unless the project explicitly chooses 3D, 2.5D, VR/AR, or another rendering model.
- **Visual design**: simple premium 2D by default: clear silhouettes, controlled palettes, restrained detail, reusable UI/components, and polish through timing, spacing, contrast, and feedback.
- **Engine**: Godot 4 unless the project already uses another engine.
- **Language**: GDScript unless the project already uses C# or the user chooses it.
- **Feature specs**: every production feature requires an independent Word `.docx` design document, per-page Figma/FigJam UE diagrams, written transition map, per-page explanation, data-source map, acceptance checklist, and user review/revision log before implementation.
- **Design docs**: formal 策划案/GDD/system specs require professional gameplay/system flowcharts and Figma/FigJam UI/UE diagrams; Markdown-only diagrams are drafts, not final artifacts.
- **User review**: the user's edited Word/Figma design is the source of truth; substantial user changes return to System Designer before implementation continues.
- **Player feedback**: Concept and System Design collect player opinions, playtest notes, review patterns, community comments, or planned feedback channels before locking direction.
- **Demo placeholders**: demos and prototypes use emoji expressions first; missing resources that emoji cannot represent clearly use simple original SVG drawings.
- **Implementation**: substantial features must be split into modules with boundaries, contracts, per-module verification, and small integration steps.
- **Project management**: Project Manager checks `production/task-plan.md` every 30 minutes when enabled, resumes recoverable interruptions in their existing thread, and starts each eligible not-started task in a separate worktree thread without duplicating Task IDs.
- **Game config**: CSV by default under `config/csv/` or equivalent.
- **Art direction**: master-level art roles own original concept art, scene art, UI visual design, atmosphere, art bible, readability, market reference decomposition, complexity budgets, and final visual quality before Sprite Forge execution.
- **References**: prefer well-known company lessons from Nintendo, Supercell, Ubisoft/Rayman, Blizzard/Hearthstone, King, SEGA, Capcom, and durable 2D references such as Monument Valley, Hollow Knight, Celeste, and Dead Cells; never copy proprietary designs.
- **2D production**: 2D Animation Specialist and 2D Technical Artist own sprite animation, frame timing, atlases, TileMaps, y-sort, collision, import settings, materials, VFX, and Godot 2D handoff.
- **UI**: UI Artist owns visual design; UI Programmer implements mobile-first arcade UI through `brawler-arcade-ui-core` when appropriate.
- **UI implementation**: UI Programmer has learned `nextlevelbuilder/ui-ux-pro-max-skill` as a game-adapted design-to-implementation quality system for design tokens, component states, responsive/safe-area layout, accessibility, motion, and screenshot parity.
- **Motion**: procedural motion first for common feedback.
- **2D art**: AI image generation plus deterministic cleanup/QC through Sprite Forge.
- **Maps**: layered scene mode for survivorlike arenas when collision, props, y-sort, or spawn zones matter.
- **Version finish**: after meaningful feature batches, verify, commit, and push when a remote exists.

## Safety

Do not copy commercial game names, logos, characters, exact UI layouts, item lists, economies, protected assets, or proprietary code. References are used as design lessons only.

Reverse engineering is limited to owned or explicitly authorized binaries/assets and cannot be used to bypass DRM, anti-cheat, account systems, payment logic, online protections, or to extract proprietary commercial assets for reuse.

## License

MIT License. See [LICENSE](LICENSE) for details.

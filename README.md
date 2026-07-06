# Codex Game Studio Default

Turn a single Codex session into a focused indie game studio workflow.

23 core agents. 16 workflow lanes. 2D-first production. Simple premium visual design. Professional design artifacts. Professional art production. Modular implementation. Godot-first defaults. CSV-driven game data. Sprite Forge art handoff. Git version finish.

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="SKILL.md"><img src="https://img.shields.io/badge/Codex%20Skill-ready-green" alt="Codex Skill Ready"></a>
  <a href="docs/AGENT-CATALOG.md"><img src="https://img.shields.io/badge/agents-23-blueviolet" alt="23 Agents"></a>
  <a href="docs/WORKFLOW-GUIDE.md"><img src="https://img.shields.io/badge/workflows-16-orange" alt="16 Workflows"></a>
  <a href="docs/CSV-DATA-CONFIG.md"><img src="https://img.shields.io/badge/data-CSV%20first-yellow" alt="CSV First"></a>
</p>

---

## Why This Exists

Solo game development with AI is powerful, but a general chat can drift: hardcoded tuning values, unclear ownership, monolithic scripts, weak 2D production rules, weak art direction, flat atmosphere, generic UI visuals, missing professional design diagrams, missing QA, weak asset handoff, and no clean version finish.

**Codex Game Studio Default** gives Codex a small but useful studio structure for game work. It defaults to 2D-first production and simple premium visual design while keeping the user as final decision maker and routing tasks through production, design, programming, master-level art direction, concept art, environment art, UI art, 2D animation, 2D technical art, QA, Godot, GDScript, CSV data, UI implementation, procedural motion, Sprite Forge asset generation, and authorized reverse-engineering gates.

This repository is modeled after the studio-template idea of Claude Code Game Studios, adapted for Codex Skill usage and the local `codex-game-studio-default` workflow.

---

## What's Included

| Category | Count | Description |
|---|---:|---|
| **Core Agents** | 23 | Producer, directors, designers, programmers, Godot/GDScript/UI specialists, professional art specialists, 2D specialists, Sprite Forge, QA, and reverse engineering |
| **Workflow Lanes** | 16 | Concept, prototype, system design, professional design artifacts, simple premium 2D visual design, 2D production, professional art production, CSV config, architecture, vertical slice, modular implementation, QA, UI, Sprite Forge, reverse engineering, version finish |
| **Codex Skill** | 1 | Root-level `SKILL.md` with Codex-triggering metadata and progressive references |
| **References** | 8 | Detailed guides for game studio routing, master-level visual design, 2D production, professional art production, Sprite Forge, CSV config, UI core, and authorized reverse engineering |
| **Framework Docs** | 1 catalog | Agent and workflow registry for review, extension, and future testing |

## Studio Hierarchy

```text
Tier 1 - Direction
  producer
  creative-director
  technical-director

Tier 2 - Leads
  game-designer
  systems-designer
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
| Formal 策划案/GDD | Producer -> Game Designer -> Art Director -> UI Artist -> UI Programmer -> QA Lead |
| Godot implementation | Lead Programmer -> Godot Specialist -> GDScript Specialist -> QA Lead |
| Configurable game systems | Systems Designer -> Data Config Specialist -> Technical Director -> Godot Specialist -> QA Lead |
| 2D project setup | Technical Director -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| 2D character/prop/animation production | Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| 2D scene/TileMap production | Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| 2D animation/action feedback | Art Director -> 2D Animation Specialist -> Gameplay Programmer -> Godot Specialist -> QA Lead |
| Professional art direction | Creative Director -> Art Director -> Visual Development Artist -> QA Lead |
| Character/prop concept art | Art Director -> Concept Artist -> 2D Animation Specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| Scene/environment art | Art Director -> Visual Development Artist -> Environment Artist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| UI visual design | Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead |
| Simple premium 2D visual direction | Creative Director -> Art Director -> relevant master art specialist -> 2D Technical Artist -> QA Lead |
| Mobile arcade UI | Art Director -> UI Artist -> UI Programmer -> Godot Specialist -> QA Lead |
| Procedural gameplay feedback | Art Director -> Gameplay Programmer -> Godot Specialist -> QA Lead |
| Generated 2D art | Art Director -> relevant professional art specialist -> Sprite Forge Specialist -> 2D Technical Artist -> Godot Specialist -> QA Lead |
| Authorized binary analysis | Technical Director -> Lead Programmer -> Reverse Engineering Specialist -> QA Lead |

See [docs/AGENT-CATALOG.md](docs/AGENT-CATALOG.md) for each agent's responsibilities and skills.

## Default Workflow

1. **Git and GitHub Startup** - initialize or verify Git, ignore files, README, first commit, private GitHub origin where possible.
2. **Concept** - promise, target player, pillars, anti-pillars, reference principles.
3. **Prototype** - one risky assumption, minimum test, proceed/pivot/cut verdict.
4. **System Design** - core loop, mechanics, content rules, economy, difficulty, professional flowcharts, and UI/UE diagrams for formal design docs.
5. **CSV Data Config** - schemas, starter rows, IDs, validation rules, loading path.
6. **Technical Architecture** - Godot architecture, module boundaries, data/resources, 2D scene/layer model by default, performance budget.
7. **Vertical Slice** - playable slice plan, tasks, owners, acceptance criteria.
8. **Implementation** - modular code, assets, data, per-module verification, and integration.
9. **QA and Tuning** - smoke checks, playtest notes, bugs, balance notes.
10. **Milestone Review** - ship/iterate/pivot decision and next sprint.
11. **Git Version Finish** - verify, commit, push, report commit hash.

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

The skill is designed for implicit use on game-development tasks, including Chinese prompts such as `游戏开发`, `制作游戏`, `Godot游戏`, `土豆兄弟like`, `幸存者like`, `美术资源`, `数值设计`, and `游戏测试`.

## Project Structure

```text
SKILL.md                            # Codex Skill entry point
AGENTS.md                          # Project-level Codex instructions
agents/                            # Codex skill UI metadata and specialist notes
references/                        # Progressive-disclosure reference docs
docs/                              # Human-facing guides and catalogs
design/registry/                   # Design entity registry stubs
production/                        # Review mode and future sprint state
Codex Game Studio Framework/        # Agent/workflow catalog for testing and extension
```

## Core Defaults

- **Dimension**: 2D-first unless the project explicitly chooses 3D, 2.5D, VR/AR, or another rendering model.
- **Visual design**: simple premium 2D by default: clear silhouettes, controlled palettes, restrained detail, reusable UI/components, and polish through timing, spacing, contrast, and feedback.
- **Engine**: Godot 4 unless the project already uses another engine.
- **Language**: GDScript unless the project already uses C# or the user chooses it.
- **Design docs**: formal 策划案/GDD/system specs require professional gameplay/system flowcharts and UI/UE diagrams; Markdown-only diagrams are drafts, not final artifacts.
- **Implementation**: substantial features must be split into modules with boundaries, contracts, per-module verification, and small integration steps.
- **Game config**: CSV by default under `config/csv/` or equivalent.
- **Art direction**: master-level art roles own original concept art, scene art, UI visual design, atmosphere, art bible, readability, market reference decomposition, complexity budgets, and final visual quality before Sprite Forge execution.
- **References**: prefer well-known company lessons from Nintendo, Supercell, Ubisoft/Rayman, Blizzard/Hearthstone, King, SEGA, Capcom, and durable 2D references such as Monument Valley, Hollow Knight, Celeste, and Dead Cells; never copy proprietary designs.
- **2D production**: 2D Animation Specialist and 2D Technical Artist own sprite animation, frame timing, atlases, TileMaps, y-sort, collision, import settings, materials, VFX, and Godot 2D handoff.
- **UI**: UI Artist owns visual design; UI Programmer implements mobile-first arcade UI through `brawler-arcade-ui-core` when appropriate.
- **Motion**: procedural motion first for common feedback.
- **2D art**: AI image generation plus deterministic cleanup/QC through Sprite Forge.
- **Maps**: layered scene mode for survivorlike arenas when collision, props, y-sort, or spawn zones matter.
- **Version finish**: after meaningful feature batches, verify, commit, and push when a remote exists.

## Safety

Do not copy commercial game names, logos, characters, exact UI layouts, item lists, economies, protected assets, or proprietary code. References are used as design lessons only.

Reverse engineering is limited to owned or explicitly authorized binaries/assets and cannot be used to bypass DRM, anti-cheat, account systems, payment logic, online protections, or to extract proprietary commercial assets for reuse.

## License

MIT License. See [LICENSE](LICENSE) for details.

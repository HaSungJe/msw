<!-- >>> managed by mswai >>> -->
# ROLE

You are an expert assistant for **MapleStory World (MSW)** development. You help users — from complete beginners to experienced developers — build games using **mLua** scripts, entity/config setup (`.model`, `.ui`, `.map`), and the MSW APIs.

# PROJECT CONTEXT (MANDATORY)

**This project is an MSW (MapleStory Worlds) project.** Treat every request as an MSW task.

### Foundation: must be in context on every turn

Before analyzing, planning, searching, or editing, all of the Foundation context below must be **present in your context window**. On the first turn of a session that means loading all of it; on later turns load only what is missing — never loaded yet, or lost to context compaction. Do **not** re-read a Foundation file that is already fully in context this session. Already having a *different* MSW skill in context from a previous turn is **not** a substitute for a missing Foundation item.

**1. Two Foundation Skills via the `Skill` tool, in order:**

| # | Skill identifier | What it covers |
|:-:|---|---|
| 1 | `msw-general` | Workspace structure, platform rules (`TileMapMode↔Body`, world unit, `SpriteRUID`, spawn), MCP tools, `.model`/`.map`/`.ui`/`.dataset` authoring, validated template catalog. Every other MSW skill assumes this is loaded. |
| 2 | `msw-ui-system` | UI single entry point — HUDs, popups, toasts, menus, tabs, dialogs. Even "Galaga" needs a score/lives HUD. `.ui` files MUST go through a builder; never edit raw JSON. |

> ⛔ **Never** load a skill by path (`Read("plugins/msw-maker-base-skill/skills/...")`, `Glob`, `ls`, `Grep`). The plugin lives in Claude Code's global plugin cache, not in the workspace's `plugins/` folder. Use the `Skill` tool — it resolves the absolute path automatically.

**2. Four Foundation references via `Read` (in full, no `offset`/`limit`):**

| Reference | Why it is required in context |
|---|---|
| `msw-general/references/platform.md` (core) | 8 core rules / `TileMapMode↔Body` / `[LEA-3004]` / coordinate system / SortingLayer·OrderInLayer / `SpriteRUID` / `SpawnByModelId` / `MovementComponent` per-map InputSpeed scaling / `.directory` / `.config` / CoreVersion. Every other reference assumes you have Read this. |
| `msw-general/references/workspace.md` | World instance / Room / DataStorage / Play mode / `refresh` / mid-workflow recovery — the operations rule for "how does an edit get reflected and where do I verify it". |
| `msw-general/references/entity.md` | Entity Work Preflight (Absolute Principle #0). inline `@components` vs `modelId`, snapshot workflow, RUID & coordinate rules. |
| `msw-general/references/authoring.md` | Shared schema-consistency and hand-edit hazards across `.mlua` / `.model` / `.map` / `.ui` / `.userdataset` / `.config`. |

Once `MapComponent.TileMapMode` is identified, also Read the matching `platform-{maple|rect|sideview}.md`. For silent-failure debugging, also Read `troubleshooting.md`.

#### MSW silent-failure zones (why generic game-design intuition fails)

Generic knowledge of "top-down RPG" / "side-scrolling platformer" / "Entity-Component" / "popup UI" matches MSW's rules only superficially. Recognizing a genre ("Galaga / Mario / Bomberman / dungeon RPG / boss fight") is at most a hint for which `platform-{type}.md` to read — not a substitute for reading it. These are the silent-failure zones (no error → broken behavior):

| MSW-specific rule | How it diverges from generic knowledge |
|---|---|
| `TileMapMode` ↔ Body (`Rigidbody`/`Kinematicbody`/`Sideviewbody`) | Wrong pairing → no error, doesn't move (or `[LEA-3004]`) |
| Coordinates are world units (1 unit = 100 px) | Raw pixel values → off by 100× |
| `SpriteRUID = ""` | Invisible on screen with no error |
| `.mlua` + `.codeblock` pair + Maker `refresh` | `.mlua` alone won't register |
| Maker registers **new** file entries only from `RootDesk/` | A new file created in `Global/` won't appear. Existing `Global/*.model` files can be edited in place through `ModelBuilder` + Maker Refresh |
| `SpawnByModelId(parent=nil)` | Runtime error. Use `self.Entity.CurrentMap` |
| `_LocalizationService` is ClientOnly | Returns nil if called on the server |
| `MovementComponent.InputSpeed` per-map scaling (×1 / ÷1.2 / ×1.5) | Same value, different perceived speed |
| `.ui` must go through the builder (no raw JSON edit/grep) | Block your generic JSON-editing instinct |

#### Self-check before Plan (## 0)

If any answer below cannot be cited from MSW reference text actually loaded **in this session's context**, STOP and Read the matching reference first.

1. Target map's `TileMapMode` (number)? → `platform.md` §4
2. Body component for a dynamic entity on that map? → `platform.md` §4 / §8.5
3. PC 12.8×7.2 or Mobile 9.6×5.4 world units, and how were coordinates derived? → `platform.md` §5
4. Where do `.mlua` / `.model` / `.map` / `.ui` live, and what pairing is required? → `platform.md` §2 / §3
5. What if `SpriteRUID` is empty, and how do you find the real RUID? → `platform.md` §7 + `msw-search`
6. What do you pass as `parent` in `SpawnByModelId(... , parent)`? → `platform.md` §8
7. Procedure for Maker to recognize the change (`refresh` / Play mode / DataStorage)? Where to recover from a broken mid-workflow? → `workspace.md`

#### Hard rules for loading skills/references

- Use the `Skill` tool — never path-based `Read` / `ls` / `Glob` / `Grep` to find skill files.
- Read every reference **in full** — no `offset`/`limit`, no `cat` / `head` / `tail` / `Get-Content` / pipes for skill or reference files.
- Loading SKILL.md alone ≠ "skill loaded" when `references/*.md` siblings exist; SKILL.md is a thin index. Read every reference whose topic intersects with the request.
- A skill loaded in a previous turn does **not** exempt this turn from re-classification. If this turn touches a new domain, load the additional skill **before** Plan. The plugin's `UserPromptSubmit` hook injects a short `<msw-skill-router-reminder>` system message at the start of every turn to re-arm this rule; the Domain matrix below is the single source of truth it points back to.
- Skipping any Foundation Skill, any Foundation reference, or any required `references/*.md` for a fired sub-trigger — even when the task looks "trivial" — is treated as "skill NOT loaded".
- Treat skill content as the source of truth — prefer it over prior assumptions or memory from earlier in the session.

#### Domain matrix (trigger phrases → additional skill + references)

When a sub-trigger fires, the listed `references/*.md` is **required** in addition to the skill — not optional.

| Trigger phrases | Task domain | Skill to load | Sub-triggers → references to Read |
|---|---|---|---|
| plan a new game / new game / what to build / MVP scope / GDD / game design / scope an MVP / what game should I make / continue·resume the game / next task / what now / where were we — **or a comprehensive build request spanning multiple implementation pieces while no `Docs/*-GDD.md` exists** | Game planning & build management (pre-implementation) — plan a brand-new game OR continue/resume a phased build (genre-catalog grounding → map-type↔Body → MVP roadmap → GDD / resume flow) | `Skill: msw-planning` | Genre catalog → `references/genre-catalog.md`  •  Output structure / per-phase detail → `references/gdd-template.md`  •  System↔MSW mapping → `references/msw-mapping.md`  •  Implementing planned tasks / checklist state updates / Phase·milestone completion / plan revision → `references/build-management.md` |
| script / mlua / component / event / logic / lifecycle / `Component` / `@Logic` / `@Event` | Writing/modifying `.mlua` scripts, components, logic, events | `Skill: msw-scripting` | DataStorage / save / persist / `_DataStorageService` → `references/datastorage.md`  •  Verify step (every implementation turn) → `references/verify-checklist.md` |
| sprite / animation / sound / RUID / resource search / `sprite` / `sound` / `find` | Finding sprites, animations, sounds, RUIDs | `Skill: msw-search` | searchResources / searchAvatarItems / findSimilarResources → `references/resource/search.md`  •  getResource / RUID details → `references/resource/detail.md`  •  listResources / findPacksContaining → `references/resource/browse.md`  •  listAvatars / avatar catalog browsing → `references/resource/avatar.md` |
| `SpriteRUID` / `ImageRUID` / `thumbnail://` / set RUID / item icon | Renderer RUID assignment — `animationclip` direct playback, `thumbnail://` prefix for `avataritem` / `skeleton` / `animationclip` thumbnails | `Skill: msw-sprite-ruid` | (no `references/`) |
| draw a sprite directly / pixel art / custom sprite / make an icon / image generation / maple-style character | Hand-draw and upload a sprite RUID — **only after `msw-search` finds no suitable resource** | `Skill: msw-painter` | Canvas & size rules → `references/size-guide.md`  •  chunky pixel style → `references/style-chunky-pixel.md`  •  maple cartoon style → `references/style-maple-cartoon.md` |
| avatar / costume / equipment / outfit / animation state / attack motion | Avatar / player appearance | `Skill: msw-avatar` | (no `references/`) |
| DefaultPlayer / player / jump / move speed / HP / camera / respawn | DefaultPlayer customization | `Skill: msw-defaultplayer` | (no `references/`) |
| attack / hit / damage / monster combat / critical / knockback / hit effect | Combat, damage, monster battles | `Skill: msw-combat-system` (concepts + API tables only; full implementation in `references/`) | Monster `.model` / ActionSheet / MonsterAI / Pattern A Soldier canonical → `../msw-general/references/monster.md` (consolidated)  •  HP gauge / `PixelRendererComponent` → `references/hp-gauge.md`  •  projectile / arrow / bullet / homing / piercing / splash → `references/projectile.md`  •  FSM / `StateComponent` / `@State` / boss phase → `../msw-general/references/animation-state.md` (unified)  •  BT / `AIComponent` / `@BTNode` / Composite / Decorator / Threat → `references/ai-bt.md` |
| `.behaviourtree` / BT node graph / SequenceNode / SelectorNode / Blackboard variable / `ActionNode` / `DecoratorNode` / bt-spec | Authoring `.behaviourtree` files + the per-project BT node spec (`.behaviourDocs/bt-spec.md`) | `Skill: msw-behaviourtree` | Node catalog → `references/node-catalog.md`  •  tree skeletons → `references/skeleton-minimal.json` / `references/skeleton-full.json` |
| inventory / shop / ranking / mail / quest / collection / key binding / GM / slash command | Standard game systems — **check before writing from scratch** | `Skill: msw-packages` | (no `references/`; each package's README is fetched on demand from GitHub) |
| popup / HUD / button / toast / menu / tab / layout / `.ui` | UI screens / widgets | `Skill: msw-ui-system` | Style template bundle → `references/templates/templates.md` + chosen `references/templates/style-N-*/{ruid-map.md, structure.md, Popupbutton.mlua}`  •  Component API / enum tables → `references/component-api.md`  •  Runtime patterns (toasts / popups / HP bar / tabs / drag-drop) → `references/runtime-patterns.md`  •  Builder protocol (unified entry point — core + per-builder files) → `../msw-general/references/builder-protocol.md` + `../msw-general/references/builder-protocol-ui.md` §3 |
| entity placement / `.map` / spawn / `SpawnByModelId` / coordinate / transform | Entity placement, `.map` editing | `Skill: msw-general` | Entity Work Preflight + `.map` builder / entity placement / component patching → `references/entity.md` |
| `.model` / template / EntryKey / Properties / Values / model catalog | `.model` authoring | `Skill: msw-general` | `.model` authoring / `Values` serialization → `references/model.md`  •  JSON schema details → `references/model/model-schema.md`  •  monster `.model` (lowercase ActionSheet / IsLegacy / SortingLayer / canonical 11 components) → `references/monster.md` |
| TileMapMode / Body / side-view / top-down / gravity / SortingLayer / SpriteRUID / 8 core / `MovementComponent` / `InputSpeed` / `.directory` | Platform rules, physics, troubleshooting | `Skill: msw-general` | All-map-types-common (8 core / TileMapMode↔Body+LEA-3004 / SpriteRUID / `SpawnByModelId` / coordinate system / `.config`·CoreVersion) → `references/platform.md`  •  **MapleTile** (`= 0`) — Foothold / `Gravity` / `PredictFootholdEnd` / `DownJump` → `references/platform-maple.md`  •  **RectTile** (`= 1`) — `SpeedFactor` / 4-directional / Movable / dynamic tiles → `references/platform-rect.md`  •  **SideViewRectTile** (`= 2`) — `JumpSpeed` / `JumpDrag` / wall detection / `EnableDownJump` → `references/platform-sideview.md`  •  Symptom debugging (`[LEA-3004]` / "doesn't move" / "invisible" / "100x off") → `references/troubleshooting.md`  •  tile painting / `RectTileMap` / `FootholdComponent` → `references/tile.md` |
| DataSet / userdataset / `.csv` / localize / i18n / LocaleDataSet / `_LocalizationService` | Datasets / i18n | `Skill: msw-general` | UserDataSet / LocaleDataSet runtime / ClientOnly rule → `references/dataset.md` |
| MCP tool calls / `refresh` / `play` / `stop` / `logs` / `screenshot` / Room / DataStorage location | MCP tools, workspace flow | `Skill: msw-general` | Workspace / Room / DataStorage / Play mode / recovery → `references/workspace.md`  •  Shared authoring → `references/authoring.md`  •  MCP setup issues → share this link with the user: https://maplestoryworlds-creators.nexon.com/ko/docs?postId=1368 |

**Routing notes:**

- **Planning gate**: a comprehensive build request spanning multiple implementation pieces, made while no `Docs/*-GDD.md` exists, routes to **`msw-planning` FIRST** — before any implementation domain above; it is a planning trigger, not a plain implementation request. **NO 'small/simple game' exception** — apparent concept simplicity is not MSW implementation simplicity and does not waive this gate; do not self-judge "this one is simple enough to skip planning" (if the game really is small, the planning flow itself scopes it down in minutes). Likewise, a bare **continue / resume / next-task** request ("continue", "what's next", "what should I do now" — in any language) is **NOT ambiguous — it fires this row as-is**: load `msw-planning` FIRST and let its **resume flow** determine the state (it detects `Docs/`·`Archive/` itself and handles the no-plan case too). Do **not** reply with clarifying questions before loading it, and never jump into a phase doc as plain implementation.
- For standard game features matching the catalog (ranking / inventory / shop / etc.), check **`msw-packages` first** — a prebuilt package may eliminate from-scratch implementation.
- When a UI request is ambiguous between **full system** (`msw-packages`) and **UI screen only** (`msw-ui-system`), ask ONE short Scope-First question before fetching files. Skip the question if the user explicitly says "from scratch" / "just the UI" → `msw-ui-system`, or "with data" / "full system" → `msw-packages`.
- ⛔ Never call `msw-mcp`'s `asset_search_resources` directly. Use the **`msw-search`** skill — it routes to the correct, validated retrieval pipeline.

# RULE

### Workspace structure

- **NativeScripts**: Native API definitions (`.d.mlua`)
- **RootDesk**: Working workspace (`.mlua`, `.model`)
- **map**: `.map` files
- **ui**: `.ui` files

**⛔ Restricted directories:**

- `Global/` — engine defaults + world settings. **Never create new files here** (Maker registers new entries only from `RootDesk/`) or delete. Existing `Global/*.model` files may be modified in place through `ModelBuilder` + Maker Refresh; create new custom models under `RootDesk/MyDesk/Models/`. `.config` (WorldConfig, SectorConfig) is values-only and Maker-managed; do not touch `common.gamelogic` or the `common` entity.
  - `Global/NativeModel/` — MSW built-in `.model` templates (monsters, NPCs, items). Read-only reference — copy into `MyDesk/Models/` to customize; read to learn JSON structure and component composition.
- `Environment/` — `.d.mlua` API definitions. Read-only.

### Cross-platform tool rules

⛔ **Never use shell commands to inspect the workspace.** Shell behavior differs across Windows PowerShell, Git Bash, and macOS bash (path separator, escape rules, encoding, command names). Cursor / Claude Code's built-in tools are the only portable choice.

| To do this | ✅ Use this | ❌ Never use |
|---|---|---|
| List files | `Glob("RootDesk/MyDesk/**/*.mlua")` | `ls`, `dir`, `Get-ChildItem`, `gci` |
| Check folder | `Glob("map/*")` | `ls`, `Test-Path`, `dir` |
| Read a file | `Read("RootDesk/MyDesk/Foo.mlua")`; for `.map` use `MapBuilder.read(...)` | `cat`, `type`, `Get-Content`, `gc`, `head`, `tail`, `more`, `less` |
| Search contents | `Grep("@Logic", glob: "*.mlua")` | `grep`, `findstr`, `Select-String`, `sls`, `rg` directly |
| Find file by name | `Glob("**/PlayerController.mlua")` | `find`, `where`, `Get-ChildItem -Recurse` |

The `Bash` / shell tool is reserved for actual programs (`git`, `npm`, MCP, build scripts). When you must invoke one:

1. Prefer workspace-relative paths (`git add RootDesk/MyDesk/Foo.mlua`).
2. If an absolute path is unavoidable, use forward slashes and double-quote: `"D:/msw-world-projects/.../map/"` — never `D:\...`. In bash on Windows, `\` is an escape character; `D:\foo\bar\` collapses to `D:foobar`.
3. Always double-quote paths containing spaces or non-ASCII.
4. Prefer POSIX commands (`ls`, `mv`, `cp`, `rm`) over OS-specific (`dir`, `type`, `del`).

> Symptom of violation: `ls: cannot access 'D:msw-world-projects...'` — the backslashes were eaten by bash. Stop and re-issue as `Glob` / `Read` / `Grep`.

### Runtime interaction requires MCP — no exceptions

⛔ **Never claim a runtime result without an actual MCP tool call.**

- Saying "I clicked the button" without calling `mouse_input` is a hallucination.
- Saying "it works" without calling `play` → `logs` is a hallucination.
- Saying "no errors" without calling `logs(kind="build")` or `logs(kind="normal")` is a hallucination.

If a task requires runtime interaction (playing, clicking, typing, verifying behavior, checking logs), you **must** invoke the corresponding Maker MCP tool (`play`, `stop`, `logs`, `keyboard_input`, `mouse_input`, `maker_execute_script`). Text alone cannot substitute for tool execution. Use `screenshot` when you need to identify screen coordinates for input targeting or when the user explicitly requests it.

## 0. Plan (MANDATORY)

> **Prerequisite:** Foundation Skills (2) + Foundation references (4) + the matching `platform-{maple|rect|sideview}.md` + every triggered domain skill/reference must already be loaded (see PROJECT CONTEXT). Pass the 7 self-check questions before continuing.

1. **Classify the task:**
   - **New only** — add new scripts/entities/UI; no existing files to change.
   - **Modify existing** — change or extend existing files only.
   - **Both**.

2. **Branch:**
   - **New only** → skip workspace analysis; go to step 3.
   - **Modify existing / Both** → analyze the workspace by domain:

     | Domain | Editable | Reference | Search in |
     |---|---|---|---|
     | **Script** (logic, components, events) | `.mlua` | `.d.mlua` | RootDesk |
     | **Entity** (models, config, spawning) | `.model` | `.d.mlua` | RootDesk |
     | **UI** (widgets, layouts, bindings) | `.ui` | `.d.mlua` | ui |

     Search only the file types relevant to the request; read matches to learn patterns and dependencies.

3. **`TodoWrite`** — break the task into concrete, verifiable steps. A **Verify** todo (load `msw-scripting`, then Read `references/verify-checklist.md`) is required (see ## 3). Mark each todo `in_progress` when starting; `completed` only after verification passes.

## 1. Analyze

- Read `.d.mlua` for available APIs, signatures, parameter types.
- Read existing `.mlua` to learn current code patterns and conventions.
- For config tasks, read existing `.model` / `.ui` / other JSON config to understand structure.
- For new `.model` files, read examples from `Global/NativeModel/`.

## 2. Implement

- **Editable:** `.mlua`, `.model`, `.ui`, `.map` only. All other file types are read-only.
- **Never modify `.codeblock`** — auto-generated metadata for `.mlua`. Read for reference only; the runtime manages it.
- **New file paths:** `.mlua` → `RootDesk/MyDesk/`, `.model` → `RootDesk/MyDesk/Models/`, `.map` → `map/`, `.ui` → `ui/`. New files outside these paths won't be recognized.
- **`Global/`**: never create new files here (Maker won't register them) or delete. Existing `Global/*.model` files may be edited in place via `ModelBuilder` + Maker Refresh; create new custom models under `RootDesk/MyDesk/Models/`. `Environment/` (`.d.mlua`) is read-only; `.config` files are values-only and Maker-managed.
- **Use builders for structured files:** `.model`, `.ui`, and `.map` edits must go through their skill-local builders (`ModelBuilder`, `UIBuilder`, `MapBuilder`) instead of raw JSON patching unless the relevant reference explicitly permits an exception.
- **Property types:** use `integer` (not `int`), `number` (not `float`).
- **Add `log()` calls** at critical checkpoints (e.g. `OnBeginPlay` entry, key variable values, important events) so Verify can confirm behavior.
- **`SpawnService` parent must NOT be nil.** Pass the target map entity (`self.Entity.CurrentMap`, or `_EntityService:GetEntityByPath("/maps/map01")`).

  ```
  -- ✅ Correct
  local map = self.Entity.CurrentMap
  _SpawnService:SpawnByModelId(modelId, name, pos, map)

  -- ❌ Wrong — LWA-3019 warning, undefined behavior
  _SpawnService:SpawnByModelId(modelId, name, pos, nil)
  ```

- **Pick the right script scope** based on lifetime, not just "globalness":

  | Scope | Use | Why |
  |---|---|---|
  | World-wide global manager (login session, account data, world-wide event bus, global UI manager) | `@Logic` | Engine-managed singleton; lives the entire world session, persists across map transitions; auto-registered. |
  | Map-scoped content (that map's quest controller, wave spawner, mini-game, NPC dialog) | `@Component` on the map entity (in `.map`'s `@components` or via `AddComponent`) | A `@Logic` survives map transitions and would leak state. The map-entity component participates in `OnBeginPlay` / `OnEndPlay` / `OnMapEnter` / `OnMapLeave` and is cleaned up on map unload. |
  | Per-entity behavior (monster AI, item pickup, player skill on a specific actor) | `@Component` on that entity (via `.model` or `AddComponent`) | Lifetime is tied to the actor. |

  Rule of thumb: *"Should this still be running when the player walks into another map?"* → Yes ⇒ `@Logic`. → No, only this map ⇒ map-entity `@Component`. → No, only this actor ⇒ actor `@Component`.

### Camera → Everything mapping

The camera perspective (`TileMapMode`) determines the entire physics, movement, map, and collision stack. **An entity with the wrong Body component will not move.**

| TileMapMode | View | Body | Map structure | Gravity | Movement |
|---|---|---|---|---|---|
| `MapleTile` | Side-view | `RigidbodyComponent` | `FootholdComponent` platforms | Yes | Left/right + jump |
| `RectTile` | Top-down | `KinematicbodyComponent` | `RectTileMapComponent` tiles | No | Free 4-directional |
| `SideViewRectTile` | Side-view | `SideviewbodyComponent` | `RectTileMapComponent` tiles | Yes | Left/right + jump (tile-based) |

### Script lifecycle

**Component lifecycle methods** (execute in this order based on entity state):

- `OnInitialize` — once after the entity and its components are created. Earliest point to reference other components, but they may not all be ready yet.
- `OnBeginPlay` — once when logic starts. Guarantees other components/entities exist; safe to reference.
- `OnMapEnter(Entity)` / `OnMapLeave(Entity)` — fires on every map transition. On the client, `OnMapEnter` also fires for other players already in the map. Both server and client.
- `OnSyncProperty(string name, any value)` — client-only. Called when a `@Sync` property finishes synchronizing. Not called if sync setting is None.
- `OnUpdate(number delta)` — every frame.
- `OnEndPlay` — when the entity is removed from the map.
- `OnDestroy` — immediately before the entity is destroyed.

**Logic lifecycle** — Logic is an engine-managed global singleton: created **once per world session** and persists across **all** map transitions. Its lifecycle is a **subset** of Component's — `OnMapEnter` / `OnMapLeave` do **NOT** fire on `@Logic`.

- `OnInitialize`, `OnBeginPlay` — once at world start.
- `OnUpdate` — every frame; runs **before** any Component's `OnUpdate`.
- `OnEndPlay` — only at world session end (e.g. shutdown). **Not** on map change.
- `OnDestroy` — when the Logic is removed (rare).

> ⚠️ **`OnMapEnter` / `OnMapLeave` do not fire on `@Logic`** — they are dispatched only to Components attached to map-scoped entities. Writing `method void OnMapEnter(Entity m) ... end` on a Logic compiles but the method is never invoked (silent dead code). For per-map setup/cleanup either (1) move the behavior to a `@Component` on the map entity (preferred), or (2) inside the Logic, poll `_UserService.LocalPlayer.CurrentMap` from `OnUpdate` and react to changes. Because a Logic survives map transitions, any timer / event handler / mutable state in a Logic that should reset per map must be cleared by one of these workarounds — there is no automatic hook.

**ExecSpace annotations** — control where code runs:

| Annotation | Behavior |
|---|---|
| `@ExecSpace("ServerOnly")` | Server only. |
| `@ExecSpace("ClientOnly")` | Client only. |
| `@ExecSpace("Server")` | Server; if called from client, sends a request to the server. |
| `@ExecSpace("Client")` | Client; if called from server, sends a request to the client. |

## 3. Verify

Load `msw-scripting` (`Skill: msw-scripting`) if not already loaded this turn, then Read `references/verify-checklist.md` in full and follow it.

## 4. On Failure

- Check ExecSpace first — confirm `_Service` calls run on the correct side (Client vs Server).
- Fix the code, then return to step 3 (Verify).
- Do not mark the todo as completed until verification passes.

## 5. Finally

If none of the above resolves the issue, tell the user:

> I could not find a solution through local implementation, Maker MCP, or Guide documents.
> You can get help from the MapleStory Worlds official Discord community:
>
> **https://discord.com/invite/maplestoryworlds**
<!-- <<< managed by mswai <<< -->

# 프로젝트 작업 규칙

## 먼저 읽을 것

- 작업 전 `.beaver/memory/MEMORY.md`와 관련 주제 파일을 읽는다. 우선순위는 사용자 지시 → `.beaver/memory/` → 이 문서와 연결된 `docs/` → 일반 관례다. 답변과 진행 보고는 한국어로 쓴다 (`.beaver/memory/workflow.md:70-71`).
- 화면은 `docs/ui-screens.md`, 엔진 실측은 `docs/msw-engine.md`, 맵 테마는 `docs/theme-presets.md`, 유닛 원화는 `docs/unit-art.md`를 따른다. 남은 일은 `.beaver/output/roadmap/maple-augment-defense-roadmap.md`에서 확인한다.
- `.info/`는 로컬 설계 원본이다. 관련 기능을 만들거나 수치를 바꿀 때 읽되 커밋하지 않는다 (`.beaver/memory/workflow.md:64-65`).
- 게임 내용이 바뀌면 같은 작업에서 관련 `.info/` 설정 문서도 동기화한다. 외형·프레임·흉상·자산 경로, 능력치·스킬·증강·비용·전투 규칙, 테마·UI·진행 규칙까지 포함한다. 코드·실제 사용 자산·문서의 본문/요약/표/연결 경로를 함께 대조하고, 바뀐 수치의 파생 표도 갱신한다. 예정안과 과거 기록은 현재 적용 정보와 명확히 구분한다. 완료 보고 전에 이 대조를 끝낸다 (`.info/README.md`, `.beaver/memory/workflow.md`).

## 주의

- `Environment/NativeScripts/**/*.d.mlua`는 엔진 선언 레퍼런스이므로 수정하지 않는다. `.mcp.json`과 `.codex/`에는 접속 정보가 있을 수 있어 커밋하지 않는다 (`docs/architecture.md`, `.gitignore`).
- `*.map`, `*.model`, `*.config`는 Maker 직렬화 자산이다. 구조를 추측해 직접 바꾸지 말고 가능하면 Maker 도구를 쓴다. 맵 이동·Play 전에 `maker_save`를 한다 (`docs/testing.md`).
- 사용자가 Maker에서 플레이 중이면 시험 스폰이나 화면 조작을 하지 않는다. Play 화면에 영향을 주는 캡처·슬로모·루프 중지는 미리 알리고 끝나면 복구한다 (`.beaver/memory/workflow.md:45-49,117-122`).

## 구조

- MapleStory Worlds Maker(CoreVersion 26.7.0.0)의 ExtendedScriptFormat mlua 프로젝트다 (`Environment/config:1`, `Global/WorldConfig.config:16-21`). 현재 맵은 `map/RtsMap.map`, 게임 코드는 `RootDesk/MyDesk/Rts*.mlua` 30개와 대응 `.codeblock` 30개다 (`docs/architecture.md`).
- 입장 이벤트 → `RtsBootstrapLogic` → 구역·카메라·스테이지·프로필 초기화 → HUD와 서버 스테이지 루프의 흐름을 따른다. 엔티티별 동작은 `Component`, 전역 게임 규칙·표·UI는 해당 `Logic`에 둔다 (`docs/architecture.md`).
- 정의만 있는 기능을 활성 기능으로 취급하지 않는다. 진입점과 호출 지점까지 확인한다.

## 코드 작성

- 게임 스크립트는 PascalCase의 `Rts…Logic`·`Rts…Component`; `property`·`method`는 PascalCase, 지역 변수는 camelCase다 (`docs/conventions.md`).
- 서버 RPC는 `@ExecSpace("Server")`로 표시하고 `senderUserId`로 호출자·소유 구역·유닛·상태·입력 범위를 재검증한다. 서버 내부 처리와 클라이언트 연출은 해당 실행 공간으로 나눈다. 공용 계산 메서드는 주석이 없는 기존 사례도 있으므로 모든 메서드에 `@ExecSpace`를 강제하지 않는다 (`docs/conventions.md`).
- 로그는 `_RtsConfigLogic:Log`를 사용한다. `DebugLog=false`가 기본이다 (`RootDesk/MyDesk/RtsConfigLogic.mlua:1-9`). 숫자 식별자·표시값에는 정수 포맷을 쓴다 (`docs/conventions.md`).
- `RtsStageTableLogic.mlua`의 생성 구간은 직접 수정하지 않는다. `.info/` 또는 `tools/gen-stage-table.py`를 고치고 `python tools/gen-stage-table.py --check`로 검산한다 (`docs/conventions.md`).
- 입력 거부와 화면 전달은 [요청·결과 규칙](docs/error-handling.md), 영구 저장은 [데이터 규칙](docs/data-layer.md)을 따른다. 불확실한 mlua API는 엔진 선언 또는 msw-mcp 문서 검색으로 확인한다.

## 화면·자산 협업

- 일반 UI 디자인은 ChatGPT가 이미지와 `docs/design/<주제>.md` 가이드라인을 만들고 `assets/design/<주제>/`에 둔다. Claude는 구현 요청 상태의 가이드라인을 바탕으로 리소스 연결·코드·Maker 확인을 맡는다. 가이드에 없는 디자인 판단은 사용자에게 묻는다 (`.beaver/memory/workflow.md:139-143`, `docs/design-handoff.md`).
- 캐릭터 원화·대기·스킬 프레임·흉상은 별도 규칙인 `docs/unit-art.md`를 따른다. 맡은 에이전트가 생성·적용·검증까지 한다. 원화의 표정·외모·의상을 사용자에게 보여 주고 OK를 받은 뒤에만 프레임을 만든다.
- 팝업 일부가 바뀌면 해당 컨테이너·선택 표시만 갱신하고 창 전체를 다시 열지 않는다 (`docs/ui-screens.md:510-518`). 화면 문구에는 티어·서포터 같은 개발용 분류를 쓰지 않는다 (`.beaver/memory/workflow.md:110-114`).

## 검증과 기록

- `.mlua`용 CLI 테스트·빌드 러너는 없다. Maker의 build 로그, Play Test, normal 로그, 화면 확인으로 검증한다. 외부에서 Play 중 코드를 고쳤다면 `maker_stop → maker_refresh_workspace → maker_save → maker_play` 순서로 다시 시작한다 (`docs/testing.md`).
- 커밋·푸시는 각각 사용자의 명시 승인을 받은 뒤에만 한다 (`.beaver/memory/workflow.md:17-22`). 커밋 메시지는 첫 줄 `YYYY.MM.DD vYYMMDD-N`(N은 그날의 순번, 날짜가 바뀌면 1), 빈 줄 뒤 `* ` 불릿으로 쓰고 Co-Authored-By·Generated-with 같은 트레일러를 붙이지 않는다 (`.beaver/memory/workflow.md:97-101`).

## 점검

- [ ] 엔진 선언과 비밀 설정을 수정·커밋하지 않았다.
- [ ] 새 스크립트 이름과 책임이 `Logic`·`Component` 경계에 맞는다.
- [ ] 서버 요청이 `senderUserId`와 소유권·입력 범위를 검증한다.
- [ ] 생성 테이블을 직접 고치지 않았고 필요하면 생성기 검산을 했다.
- [ ] 게임 변경에 영향받는 `.info/` 본문·요약·표·자산 경로를 코드·현재 자산·연결된 `docs/`와 동기화했다.
- [ ] UI는 바뀐 부분만 갱신하며 기존 화면 상태를 보존한다.
- [ ] 저장 기능은 재접속 후 읽기까지 확인했다.
- [ ] Maker build·Play 로그와 화면에서 관련 기능을 확인했다.

---
name: aigc-init
description: "Use when initializing or reinitializing a lightweight AIGC film/video project scaffold under projects/aigc/."
governance_tier: full
metadata:
  short-description: AIGC project scaffold initialization
---

# aigc 0-初始化

`aigc-init` is now a scaffold-only project kickoff skill. It creates the current AIGC 0-14 runtime directory structure under `projects/aigc/<项目名>/`, project `MEMORY.md`, and project `CONTEXT/`. It no longer creates the former initialization artifact set such as `north_star.yaml`, `init_handoff.yaml`, `story-source-manifest.yaml`, `team.yaml`, `STATE.json`, project `CHANGELOG.md`, or source folders.

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- Every call to `$aigc-init` must load this `SKILL.md` and the same-directory `CONTEXT.md`.
- If an existing project root is bound, inspect `projects/aigc/<项目名>/MEMORY.md` when present before updating it.
- Do not load `templates/`, `references/`, `review/`, `steps/`, or `types/` as active runtime truth unless the current node below explicitly authorizes the file.
- Conflict order: user explicit request > root `AGENTS.md` / repository meta policy > this `SKILL.md` > authorized local modules > same-directory `CONTEXT.md`.

## Runtime Spine Contract

Initialization has one runtime path:

`N0-intake -> N1-project-root -> N2-scaffold -> N3-memory -> N4-readback`

The skill performs filesystem scaffolding only. It does not run smart-advisor lineup selection, planning direct-answer packets, north-star synthesis, story-source readiness checks, state routing, governance sidecar generation, or next-stage recommendation.

## Multi-Subskill Continuous Workflow

When `$aigc-init` is called, this skill may complete all scaffold nodes in one pass after the project name is clear. It does not dispatch sibling stages or satellite skills. Empty stage directories are readiness containers only and must never be treated as completed stage outputs.

## When to Use

- 用户要求初始化影片、电影、影视、视频、AIGC 短剧项目。
- Create a new project scaffold under `projects/aigc/<项目名>/`.
- Recreate missing scaffold directories for an existing AIGC project without rewriting business artifacts.
- Create or update project `MEMORY.md` with initialization-time user requirements or stable long-term project inclinations, and create project `CONTEXT/` as the shared context root.

## When Not to Use

- 用户要求初始化小说、网文、书或长篇故事；route to story initialization.
- 用户要求初始化漫画；route to comic initialization.
- 用户要求生成剧本、分镜、设计、图像、视频、审片报告或其他阶段 canonical outputs；route to the owning stage.
- 用户要求恢复、查询、审查或修复已有项目状态；route to `resume/`, `query/`, `review/`, or `repair/`.
- 用户要求删除既有产物；destructive cleanup requires an explicit deletion task outside this scaffold-only contract.

## Input Contract

| input slot | required shape | handling |
| --- | --- | --- |
| `task_intent` | first scaffold initialization, scaffold repair, or rebootstrap-to-scaffold | Must be clear enough to stay in `projects/aigc/`. |
| `project_identity` | project name, working title, or explicit path under `projects/aigc/<项目名>/` | Required before writing. |
| `memory_requirements` | user-stated preferences, constraints, exclusions, special elements, or "remember this" instructions | Write to `MEMORY.md`; if absent, create a clean placeholder memory file. |
| `existing_project_state` | required only when project root already exists | Preserve existing files; create missing scaffold directories, ensure `CONTEXT/`, and merge/update `MEMORY.md` only. |

Reject or clarify when the project name is missing, the target path is outside `projects/aigc/`, or the user asks to overwrite/delete existing files without explicit scope.

## Type Routing Matrix

| type | trigger | route |
| --- | --- | --- |
| `new_scaffold` | project root does not exist | create all required directories, `MEMORY.md`, and `CONTEXT/` |
| `repair_scaffold` | project root exists but scaffold directories, `MEMORY.md`, or `CONTEXT/` are missing | create only missing scaffold pieces |
| `memory_update` | user supplies long-term project preference or replacement | update `MEMORY.md` without creating other artifacts |
| `unsafe_reset` | deletion, purge, overwrite, or non-AIGC target is implied | block and request explicit scope |

## Module Loading Matrix

| module | load condition | permission boundary |
| --- | --- | --- |
| `references/scope-and-runtime.md` | scaffold path or directory allowlist needs confirmation | May define paths only; may not reintroduce removed artifact generation. |
| `templates/project-memory.template.md` | creating a new `MEMORY.md` | Template source for memory shape only. |
| `templates/project-context-readme.template.md` | creating a new project `CONTEXT/README.md` | Template source for the project context root readme only; may not introduce north-star, team, state, source, or governance carriers. |
| `review/init-review-gate.md` | maintenance review or final readback check | Checklist only. |
| `steps/init-workflow.md` | workflow maintenance or implementation review | Node expansion only. |

All former artifact templates are inactive for initialization writeback unless a later explicit migration task re-enables them in this `SKILL.md`.

## Thinking-Action Node Map

| node_id | objective | action | write_scope | gate |
| --- | --- | --- | --- | --- |
| `N0-intake` | confirm this is an AIGC film/video scaffold task | classify task and reject/reroute non-AIGC media | none | project type clear |
| `N1-project-root` | resolve canonical root | derive `projects/aigc/<项目名>/` and prevent path escape | none | root is canonical |
| `N2-scaffold` | create current 0-14 runtime directories and project context root | create only missing directories in the allowlist, including `CONTEXT/` | directories only | all stage directories and `CONTEXT/` exist |
| `N3-memory` | create or update project memory and context readme | write `MEMORY.md` from template or merge user long-term requirements; create `CONTEXT/README.md` when missing | `MEMORY.md`, `CONTEXT/README.md` | memory exists and context root is readable |
| `N4-readback` | verify completion | read back paths and report created/skipped items | none | no removed artifact was created |

## Canonical Runtime Skeleton

New initialization creates or verifies exactly these project directories:

```text
projects/aigc/<项目名>/
├── 0-初始化/
├── 1-分集/
├── 2-编剧/
├── 3-美学/
├── 4-导演/
├── 5-表演/
├── 6-氛围/
├── 7-分镜/
├── 8-摄影/
├── 9-光影/
├── 10-分组/
├── 11-主体/
├── 12-图像/
├── 13-画布/
├── 14-审片/
├── CONTEXT/
│   └── README.md
└── MEMORY.md
```

Bootstrap runtime marker allowlist:

- `projects/aigc/<项目名>/0-初始化/`
- `projects/aigc/<项目名>/1-分集/`
- `projects/aigc/<项目名>/2-编剧/`
- `projects/aigc/<项目名>/3-美学/`
- `projects/aigc/<项目名>/4-导演/`
- `projects/aigc/<项目名>/5-表演/`
- `projects/aigc/<项目名>/6-氛围/`
- `projects/aigc/<项目名>/7-分镜/`
- `projects/aigc/<项目名>/8-摄影/`
- `projects/aigc/<项目名>/9-光影/`
- `projects/aigc/<项目名>/10-分组/`
- `projects/aigc/<项目名>/11-主体/`
- `projects/aigc/<项目名>/12-图像/`
- `projects/aigc/<项目名>/13-画布/`
- `projects/aigc/<项目名>/14-审片/`
- `projects/aigc/<项目名>/CONTEXT/`
- `projects/aigc/<项目名>/CONTEXT/README.md`
- `projects/aigc/<项目名>/MEMORY.md`

Do not create these former initialization outputs during scaffold initialization:

- `0-初始化/north_star.yaml`
- `0-初始化/init_handoff.yaml`
- `0-初始化/story-source-manifest.yaml`
- `team.yaml`
- `STATE.json`
- `CHANGELOG.md`
- `源/`
- `governance-state.yaml`
- `mandate.yaml`
- `mission-brief.yaml`
- `route-plan.yaml`
- `preflight-verdict.yaml`
- `validation-report.md`
- `learning-record.md`

Forbidden bootstrap paths remain forbidden for new initialization:

- `Original/`, `Story/`
- `1-Planning/`, `2-Global/`, `3-Detail/`, `4-Design/`, `5-Image/`, `6-Video/`, `7-Cut/`
- stale Chinese aliases such as `2-编导/`, `3-运动/`, old `4-摄影/`, old `5-分组/`, `6-图像/`, `8-图像/`, `9-视频/`, `10-审片/`

## Convergence Contract

Initialization passes only when:

- the project root is under `projects/aigc/<项目名>/`
- every active stage directory from `0-初始化/` through `14-审片/` exists with names matching the current skill package names
- `MEMORY.md` exists at the project root
- `CONTEXT/` exists at the project root, with `README.md` created when absent
- initialization-time user requirements that are long-term preferences or constraints are recorded in `MEMORY.md`
- no removed initialization artifact listed above was created by this run

Initialization fails or blocks when the project name is ambiguous, the path escapes `projects/aigc/`, an existing `MEMORY.md` would be overwritten instead of merged, or the requested operation requires deletion/overwrite without explicit scope.

## Review Gate Binding

Use `review/init-review-gate.md` for scaffold review. The active gate is `FIELD-INIT-05`: current 0-14 scaffold directories plus project `MEMORY.md` and project `CONTEXT/`; no former multi-file initialization artifact generation.

## Root-Cause Execution Contract

When initialization fails, trace:

`Symptom -> Direct Technical Cause -> Rule Source -> Fix Landing Points`

Priority repair targets:

| failure area | first repair target |
| --- | --- |
| wrong stage names or missing scaffold directory | `references/scope-and-runtime.md` and this `Canonical Runtime Skeleton` |
| former artifact created during initialization | this `Output Contract` and `review/init-review-gate.md` |
| project memory missing or overwritten | `templates/project-memory.template.md` and `N3-memory` |
| project context root missing | `templates/project-context-readme.template.md` and `N2/N3` |
| path outside canonical namespace | `N1-project-root` and `references/scope-and-runtime.md` |

## Field Mapping

| field_id | owner | canonical output | required gate |
| --- | --- | --- | --- |
| `FIELD-INIT-03` | `N0/N1` | project scope note | AIGC project name and root are clear. |
| `FIELD-INIT-05` | `N2/N4` | directory scaffold | Current 0-14 directories and project `CONTEXT/` exist; removed artifacts are absent. |
| `FIELD-INIT-09` | `N3` | `MEMORY.md`, `CONTEXT/README.md` | User initialization requirements and stable inclinations are captured or placeholder sections exist; context root has a readable readme. |

## Thought Pass Map

| step_id | focus | core question | action | fail signal |
| --- | --- | --- | --- | --- |
| `N0` | `FIELD-INIT-03` | Is this an AIGC film/video scaffold task? | classify or reroute | wrong media route |
| `N1` | `FIELD-INIT-03` | Is the project root canonical? | resolve `projects/aigc/<项目名>/` | path escape or missing project name |
| `N2` | `FIELD-INIT-05` | Do current 0-14 directories and project `CONTEXT/` exist? | create missing directories | old alias, missing stage root, or missing context root |
| `N3` | `FIELD-INIT-09` | Does project memory exist and does context root have a readable readme? | create or merge `MEMORY.md`; create `CONTEXT/README.md` when missing | missing memory, overwrite risk, or missing context readme |
| `N4` | `FIELD-INIT-05/09` | Did scaffold-only readback pass? | inspect allowlist and denylist | removed artifact created |

## Pass Table

| field_id | pass standard | fail code | rework entry |
| --- | --- | --- | --- |
| `FIELD-INIT-03` | Project root is resolved under `projects/aigc/<项目名>/` | `FAIL-INIT-03` | `N1` |
| `FIELD-INIT-05` | Current 0-14 stage directories and project `CONTEXT/` exist, and forbidden bootstrap paths were not created | `FAIL-INIT-05` | `N2/N4` |
| `FIELD-INIT-09` | Project `MEMORY.md` exists, supplied long-term requirements are captured without overwriting prior memory, and `CONTEXT/README.md` exists | `FAIL-INIT-09` | `N3` |

## Output Contract

`$aigc-init` has exactly one canonical business output: a scaffolded project root with current stage directories, project `MEMORY.md`, and project `CONTEXT/`.

- Required output: `projects/aigc/<项目名>/0-初始化/` through `14-审片/` directories, `projects/aigc/<项目名>/MEMORY.md`, and `projects/aigc/<项目名>/CONTEXT/README.md`.
- Output format: directories plus Markdown memory and context-readme files.
- Output path: `projects/aigc/<项目名>/`.
- Naming convention: stage directory names must match the current `.agents/skills/aigc/0-14` package names.
- Completion gate: pass `FIELD-INIT-05` and `FIELD-INIT-09`; former initialization artifacts must not be created.

Final user-facing answer must state the project root, created or already-present scaffold paths, `MEMORY.md` path, `CONTEXT/` path, any memory items captured, and any blocked or skipped artifact creation.

## Learning / Context Writeback

- Reusable scaffold drift, wrong stage-name aliases, or memory merge failures should be recorded in this skill's `CONTEXT.md`.
- Project-specific long-term preferences, constraints, exclusions, special elements, and "以后都按这个来" requirements belong in project `MEMORY.md`.
- Do not write one-off task instructions, script debugging notes, or cross-project skill failures into project `MEMORY.md`.

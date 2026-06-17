# Scope And Runtime Contract

This file owns the scaffold path allowlist for `$aigc-init`. It expands the active `SKILL.md` contract; it does not authorize former initialization artifact generation.

## Business Goal

- Create or repair the project root under `projects/aigc/<项目名>/`.
- Create the current 0-10 AIGC stage directory structure using the latest skill package names.
- Create or update project `MEMORY.md` as the centralized project context hub for initialization-time user requirements, team configuration, supplied-reference absorption summaries, stable long-term inclinations, production constraints, exclusions, and downstream context-reading guidance.
- Create project `CONTEXT/` with a minimal `README.md` so downstream project-context loading has a stable root.
- Preserve existing files and avoid deleting, overwriting, or creating former multi-file initialization outputs.

## Business Objects

Active initialization writeback is limited to:

- `projects/aigc/<项目名>/0-初始化/`
- `projects/aigc/<项目名>/1-分集/`
- `projects/aigc/<项目名>/2-美学/`
- `projects/aigc/<项目名>/4-编剧/`
- `projects/aigc/<项目名>/5-导演/`
- `projects/aigc/<项目名>/6-分镜/`
- `projects/aigc/<项目名>/7-摄影/`
- `projects/aigc/<项目名>/8-分组/`
- `projects/aigc/<项目名>/3-主体/`
- `projects/aigc/<项目名>/9-图像/`
- `projects/aigc/<项目名>/10-画布/`
- `projects/aigc/<项目名>/CONTEXT/`
- `projects/aigc/<项目名>/CONTEXT/README.md`
- `projects/aigc/<项目名>/MEMORY.md`

The previous initialization business objects are inactive for scaffold initialization: `north_star.yaml`, `init_handoff.yaml`, `story-source-manifest.yaml`, `team.yaml`, `STATE.json`, `CHANGELOG.md`, `源/`, and governance sidecars.

## Canonical Project Root

The canonical runtime root is:

```text
projects/aigc/<项目名>/
```

Initialization creates or verifies only the active business objects above.

## Bootstrap Runtime Skeleton

```text
0-初始化/
1-分集/
2-美学/
3-主体/
4-编剧/
5-导演/
6-分镜/
7-摄影/
8-分组/
9-图像/
10-画布/
CONTEXT/
  README.md
MEMORY.md
```

Empty stage directories are readiness containers. They do not prove that a stage has executed.

## Forbidden Bootstrap Outputs

New scaffold initialization must not create:

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

Forbidden legacy bootstrap paths include:

- `Original/`, `Story/`
- `1-Planning/`, `2-Global/`, `3-Detail/`, `4-Design/`, `5-Image/`, `6-Video/`, `7-Cut/`
- stale Chinese aliases: `2-编导/`, `3-运动/`, old `4-摄影/`, old `5-分组/`, `6-图像/`, `8-图像/`, `9-视频/`, `10-审片/`

Existing historical projects may keep legacy paths as compatibility inputs, but new scaffold initialization must not create them.

## Runtime Interpretation

- `0-初始化/` is only an empty initialization stage container after scaffold creation.
- `2-美学/`, `3-主体/`, `4-编剧/`, `5-导演/`, `6-分镜/`, `7-摄影/`, and `8-分组/` replace the older `2-编导/`, `3-运动/`, and `4-摄影/` bootstrap naming; `backup/5-表演`, `backup/6-氛围`, and `backup/9-光影` are not scaffolded as active project directories.
- `3-主体/` is created only as the stage root. Its scene, role, and prop subdirectories are created by the owning `3-主体` workflow when needed.
- `MEMORY.md` records project-level long-term preferences, constraints, exclusions, special elements, user initialization requirements, team configuration, supplied-reference absorption summaries, and stage context-reading guidance.
- `CONTEXT/README.md` is a neutral project-context root marker; later workflows may add source indexes, large reference sidecars, model notes, or other supplemental context files under `CONTEXT/`, but those sidecars must not replace `MEMORY.md` as the project memory hub.

## Truth Ownership

`0-初始化` owns:

- project scaffold creation
- project `MEMORY.md` creation or merge
- project `CONTEXT/` creation
- scaffold readback and drift reporting

`0-初始化` does not own canonical truth for later stage deliverables, route state, source readiness, governance state, or north-star creative design. It does own the initialization memory writeback for user-specified team configuration and collaboration preferences, but only as project context inside `MEMORY.md`, not as an executable team roster or advisor runtime.

## Project Memory Rules

1. `MEMORY.md` records stable project preferences, tastes, special elements, exclusions, long-term requirements, initialization-time requirements that should persist, user-specified team configuration, collaboration/reviewer preferences, supplied-reference absorption summaries, production constraints, and context-reading guidance.
2. If `MEMORY.md` already exists, merge or append relevant new memory items; do not overwrite existing memory silently.
3. Supplied reference materials should be summarized into durable memory items; large raw materials or volatile indexes may live in `CONTEXT/`, with a short absorbed summary and pointer in `MEMORY.md`.
4. Team configuration in `MEMORY.md` is context, not a permission to call team member personas, create `team.yaml`, or fabricate advisor Q&A.
5. One-off task instructions, execution logs, script failures, and cross-project heuristics do not belong in project `MEMORY.md`.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Is the canonical project root `projects/aigc/<项目名>/`? | `FIELD-INIT-03` | `FAIL-INIT-03` | `SKILL.md` `N1-project-root` | Resolved project root path. |
| Does initialization create or verify the current 0-10 scaffold directories using latest skill package names? | `FIELD-INIT-05` | `FAIL-INIT-05` | `SKILL.md` `N2-scaffold` | Directory readback or dry-run manifest. |
| Does project `CONTEXT/` exist without becoming a second rules source? | `FIELD-INIT-05` | `FAIL-INIT-05` | `SKILL.md` `N2-scaffold`; `templates/project-context-readme.template.md` | `CONTEXT/README.md` path plus neutral boundary text. |
| Does initialization avoid former multi-file outputs and forbidden legacy paths? | `FIELD-INIT-05` | `FAIL-INIT-05` | `SKILL.md` `Forbidden Bootstrap Outputs` | Absence check for removed artifacts and legacy aliases. |
| Does project `MEMORY.md` exist and preserve user initialization requirements, team configuration, supplied-reference absorption summaries, stable inclinations, and downstream context guidance? | `FIELD-INIT-09` | `FAIL-INIT-09` | `SKILL.md` `N3-memory`; `templates/project-memory.template.md` | Memory file path plus summarized captured items and any deferred raw material pointers. |

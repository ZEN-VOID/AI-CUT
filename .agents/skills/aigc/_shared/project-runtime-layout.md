# AIGC Project Runtime Layout

本文件是 `.agents/skills/aigc` 当前项目 runtime 的共享说明。它只定义项目落盘与兼容边界，不替代各阶段 `SKILL.md` 的业务合同。

## Canonical Runtime Root

| scope | canonical path | owner |
| --- | --- | --- |
| project root | `projects/aigc/<项目名>/` | root `aigc` skill |
| memory | `projects/aigc/<项目名>/MEMORY.md` | project memory |
| project state | `projects/aigc/<项目名>/STATE.json` | root / resume, created only when the owning workflow needs live route truth |
| governance state | `projects/aigc/<项目名>/governance-state.yaml` | root / resume / review, created only when governance state is needed |
| changelog | `projects/aigc/<项目名>/CHANGELOG.md` | project timeline, created only when a workflow needs chronological logging |
| context | `projects/aigc/<项目名>/CONTEXT/` | project context root, created by `0-初始化`; populated by later owning workflows when supplemental context is needed |
| source | `projects/aigc/<项目名>/源/` | source material landing, created only when source intake is needed |

## Bootstrap Scaffold Rows

`0-初始化` creates only the current active stage roots, project `MEMORY.md`, and project `CONTEXT/`.

| stage | runtime root | note |
| --- | --- | --- |
| `0-初始化` | `projects/aigc/<项目名>/0-初始化/` | scaffold container only |
| `1-分集` | `projects/aigc/<项目名>/1-分集/` | episode source split |
| `2-美学` | `projects/aigc/<项目名>/2-美学/` | post-split genre type profile, global visual tone, and style protocols; includes `类型风格.md` |
| `3-主体` | `projects/aigc/<项目名>/3-主体/` | subject registry, scene/role/prop list, design, and generation runtime; owns `主体注册表.md` and `subject-registry.yaml` |
| `4-编剧` | `projects/aigc/<项目名>/4-编剧/` | novel-to-screenplay adaptation using `1-分集`, `2-美学/类型风格.md`, and `3-主体/主体注册表.md`; short-drama rhythm, climax, hook, and AIGC field routing |
| `5-导演` | `projects/aigc/<项目名>/5-导演/` | director annotation runtime |
| `6-分镜` | `projects/aigc/<项目名>/6-分镜/` | inline storyboard split runtime |
| `7-摄影` | `projects/aigc/<项目名>/7-摄影/` | camera movement and cinematography injection runtime |
| `8-分组` | `projects/aigc/<项目名>/8-分组/` | storyboard group runtime; YAML subjects read `3-主体/subject-registry.yaml` and do not add subject info |
| `9-图像` | `projects/aigc/<项目名>/9-图像/` | current Chinese image runtime |
| `10-画布` | `projects/aigc/<项目名>/10-画布/` | current Chinese video/canvas runtime |

## Scaffold-Only Initialization Rule

Current `0-初始化` does not create former initialization carriers:

- `projects/aigc/<项目名>/0-初始化/north_star.yaml`
- `projects/aigc/<项目名>/0-初始化/init_handoff.yaml`
- `projects/aigc/<项目名>/0-初始化/story-source-manifest.yaml`
- `projects/aigc/<项目名>/team.yaml`
- `projects/aigc/<项目名>/STATE.json`
- `projects/aigc/<项目名>/CHANGELOG.md`
- `projects/aigc/<项目名>/源/`
- governance sidecars

Except for project `CONTEXT/`, these carriers may be created later only by an owning workflow that explicitly needs them.

## Bootstrap Compatibility

Legacy roots are compatibility inputs only and must not be created by new scaffold initialization:

| legacy / stale root | current handling |
| --- | --- |
| `2-编导/` | legacy readback only; current stage roots are `4-编剧/`, `5-导演/`, and `6-分镜/` |
| `3-运动/` | legacy readback only; current motion/camera-related flow is expressed through active stages `6-分镜/`, `7-摄影/`, and `8-分组/` |
| `5-表演/`, `6-氛围/`, `9-光影/` | archived stage outputs only; current skill packages live under `.agents/skills/aigc/backup/` and are not scaffolded by new initialization |
| old `4-摄影/` | legacy readback only; current active root is `7-摄影/` |
| old `5-分组/` | legacy readback only; current active root is `8-分组/` |
| `5-Image/`, `6-Video/`, `7-Cut/` | legacy/readback only; current active roots are `9-图像/` and `10-画布/` |
| `Original/`, `Story/` | legacy source aliases only; current source intake creates `源/` only when source intake is explicitly needed |

Empty scaffold directories never count as completed stage outputs.

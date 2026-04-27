# AIGC Project Runtime Layout

本文件是 `.agents/skills/aigc` 当前项目 runtime 的共享说明。它只定义项目落盘与兼容边界，不替代各阶段 `SKILL.md` 的业务合同。

## Canonical Runtime Root

| scope | canonical path | owner |
| --- | --- | --- |
| project root | `projects/aigc/<项目名>/` | root `aigc` skill |
| project state | `projects/aigc/<项目名>/STATE.json` | root / resume |
| governance state | `projects/aigc/<项目名>/governance-state.yaml` | root / resume / review |
| memory | `projects/aigc/<项目名>/MEMORY.md` | project memory |
| changelog | `projects/aigc/<项目名>/CHANGELOG.md` | project timeline |
| context | `projects/aigc/<项目名>/CONTEXT/` | project context |

## Stage Runtime Rows

| stage | runtime root | note |
| --- | --- | --- |
| `0-初始化` | `projects/aigc/<项目名>/0-初始化/` | north star, init handoff, story source manifest |
| `1-分集` | `projects/aigc/<项目名>/1-分集/` | episode source split |
| `2-编导` | `projects/aigc/<项目名>/2-编导/` | screenplay/directing projection |
| `3-摄影` | `projects/aigc/<项目名>/3-摄影/` | shot language enrichment |
| `4-分组` | `projects/aigc/<项目名>/4-分组/` | storyboard group runtime |
| `5-设计` | `projects/aigc/<项目名>/5-设计/` | scene, role, prop design runtime |
| `6-图像` | `projects/aigc/<项目名>/6-图像/` | current Chinese image runtime |
| `7-视频` | `projects/aigc/<项目名>/7-视频/` | current Chinese video runtime |
| `源` | `projects/aigc/<项目名>/源/` | source material landing |
| `CONTEXT` | `projects/aigc/<项目名>/CONTEXT/` | project-side supplemental context |

## Bootstrap Compatibility

Current image and video migration keeps several legacy-compatible skill packages discoverable while preventing them from becoming new project runtime truth.

| compatibility skill | current default | runtime rule |
| --- | --- | --- |
| `.agents/skills/aigc/5-Image/A.分镜画面` | superseded by `.agents/skills/aigc/6-图像/A-分镜画面` | `projects/aigc/<项目名>/5-Image/A-分镜帧/` is legacy/readback only |
| `.agents/skills/aigc/5-Image/B.分镜故事板` | superseded by `.agents/skills/aigc/6-图像/B-分镜故事板` | `projects/aigc/<项目名>/5-Image/B-分镜故事板/` is legacy/readback only |
| `.agents/skills/aigc/7-视频/A-分镜画面参照` | active video leaf | writes `projects/aigc/<项目名>/7-视频/A-分镜画面参照/` |
| `.agents/skills/aigc/7-视频/B-分镜故事板参照` | active video leaf | writes `projects/aigc/<项目名>/7-视频/B-分镜故事板参照/` |
| `.agents/skills/aigc/7-视频/C-主体参照` | active video leaf | writes `projects/aigc/<项目名>/7-视频/C-主体参照/` |
| `.agents/skills/aigc/7-视频/D-主板混合参照` | active video leaf | writes `projects/aigc/<项目名>/7-视频/D-主板混合参照/` |

Forbidden new bootstrap roots are maintained by `scripts/aigc_skill_audit.py`. Keep this shared layout focused on active rows and explicitly allowed compatibility aliases so stale roots do not become discoverable by copy-paste.

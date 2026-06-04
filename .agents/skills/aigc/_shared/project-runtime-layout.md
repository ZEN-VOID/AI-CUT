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
| `2-编剧` | `projects/aigc/<项目名>/2-编剧/` | novel-to-screenplay adaptation, genre/narrative parsing, short-drama rhythm, climax, hook, and AIGC field routing |
| `2-编导` | `projects/aigc/<项目名>/2-编导/` | directing intent, performance craft, and concrete visual language; consumes `2-编剧` when present |
| `3-运动` | `projects/aigc/<项目名>/3-运动/` | character motion enrichment with start, path, end, reference frame, and adjacent-frame state continuity |
| `4-摄影` | `projects/aigc/<项目名>/4-摄影/` | shot language enrichment |
| `5-分组` | `projects/aigc/<项目名>/5-分组/` | storyboard group runtime |
| `6-设计` | `projects/aigc/<项目名>/6-设计/` | scene, role, prop design runtime |
| `7-分镜` | `projects/aigc/<项目名>/7-分镜/` | inline storyboard split runtime; consumes `6-氛围` or user-specified source |
| `7-图像` | `projects/aigc/<项目名>/7-图像/` | current Chinese image runtime |
| `8-视频` | `projects/aigc/<项目名>/8-视频/` | current Chinese video runtime |
| `9-审片` | `projects/aigc/<项目名>/9-审片/` | generated footage review reports and repair evidence |
| `源` | `projects/aigc/<项目名>/源/` | source material landing |
| `shot-by-shot` | `projects/aigc/<项目名>/shot-by-shot/` | reference film/video analysis and imitation packets for `2-编导` / `3-运动` / `4-摄影` |
| `CONTEXT` | `projects/aigc/<项目名>/CONTEXT/` | project-side supplemental context |

`2-编剧` 是 active screenplay runtime，不再作为 `2-编导` legacy 触发词处理。旧 `3-导演` / `4-表演` 阶段不再保留技能目录或新 runtime root；旧名称直接兼容路由到 `2-编导` 内部 director / performance layer。

## Bootstrap Compatibility

Current image and video migration keeps several legacy-compatible skill packages discoverable while preventing them from becoming new project runtime truth.

| compatibility skill | current default | runtime rule |
| --- | --- | --- |
| `.agents/skills/aigc/5-Image/A.分镜画面` | superseded by `.agents/skills/aigc/7-图像/A-分镜画面` | `projects/aigc/<项目名>/5-Image/A-分镜帧/` is legacy/readback only |
| `.agents/skills/aigc/5-Image/B.分镜故事板` | superseded by `.agents/skills/aigc/7-图像/B-分镜故事板` | `projects/aigc/<项目名>/5-Image/B-分镜故事板/` is legacy/readback only |
| `.agents/skills/aigc/8-视频/libTV画布流` | active video leaf | writes `projects/aigc/<项目名>/8-视频/libTV画布流/` |
| `.agents/skills/aigc/9-审片` | active footage review stage | writes `projects/aigc/<项目名>/9-审片/` reports and may repair owning `5-分组` groups |

Forbidden new bootstrap roots are maintained by `scripts/aigc_skill_audit.py`. Keep this shared layout focused on active rows and explicitly allowed compatibility aliases so stale roots do not become discoverable by copy-paste.

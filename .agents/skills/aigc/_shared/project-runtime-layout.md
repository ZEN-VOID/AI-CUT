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
| `2-编剧` | `projects/aigc/<项目名>/2-编剧/` | faithful screenplay projection |
| `3-导演` | `projects/aigc/<项目名>/3-导演/` | directing intent and visual dramatic design |
| `4-表演` | `projects/aigc/<项目名>/4-表演/` | actor-performance and staging enrichment |
| `5-摄影` | `projects/aigc/<项目名>/5-摄影/` | shot language enrichment |
| `6-分组` | `projects/aigc/<项目名>/6-分组/` | storyboard group runtime |
| `7-设计` | `projects/aigc/<项目名>/7-设计/` | scene, role, prop design runtime |
| `8-图像` | `projects/aigc/<项目名>/8-图像/` | current Chinese image runtime |
| `9-视频` | `projects/aigc/<项目名>/9-视频/` | current Chinese video runtime |
| `10-审片` | `projects/aigc/<项目名>/10-审片/` | generated footage review reports and repair evidence |
| `源` | `projects/aigc/<项目名>/源/` | source material landing |
| `shot-by-shot` | `projects/aigc/<项目名>/shot-by-shot/` | reference film/video analysis and imitation packets for `3-导演` / `4-表演` / `5-摄影` |
| `CONTEXT` | `projects/aigc/<项目名>/CONTEXT/` | project-side supplemental context |

## Bootstrap Compatibility

Current image and video migration keeps several legacy-compatible skill packages discoverable while preventing them from becoming new project runtime truth.

| compatibility skill | current default | runtime rule |
| --- | --- | --- |
| `.agents/skills/aigc/5-Image/A.分镜画面` | superseded by `.agents/skills/aigc/8-图像/A-分镜画面` | `projects/aigc/<项目名>/5-Image/A-分镜帧/` is legacy/readback only |
| `.agents/skills/aigc/5-Image/B.分镜故事板` | superseded by `.agents/skills/aigc/8-图像/B-分镜故事板` | `projects/aigc/<项目名>/5-Image/B-分镜故事板/` is legacy/readback only |
| `.agents/skills/aigc/9-视频/libTV画布流` | active video leaf | writes `projects/aigc/<项目名>/9-视频/libTV画布流/` |
| `.agents/skills/aigc/backup/A-分镜画面参照` | compatibility video leaf | writes or repairs `projects/aigc/<项目名>/9-视频/A-分镜画面参照/` |
| `.agents/skills/aigc/backup/B-分镜故事板参照` | compatibility video leaf | writes or repairs `projects/aigc/<项目名>/9-视频/B-分镜故事板参照/` |
| `.agents/skills/aigc/backup/C-主体参照` | compatibility video leaf | writes or repairs `projects/aigc/<项目名>/9-视频/C-主体参照/` |
| `.agents/skills/aigc/backup/D-主板混合参照` | compatibility video leaf | writes or repairs `projects/aigc/<项目名>/9-视频/D-主板混合参照/` |
| `.agents/skills/aigc/10-审片` | active footage review stage | writes `projects/aigc/<项目名>/10-审片/` reports and may repair owning `6-分组` groups |

Forbidden new bootstrap roots are maintained by `scripts/aigc_skill_audit.py`. Keep this shared layout focused on active rows and explicitly allowed compatibility aliases so stale roots do not become discoverable by copy-paste.

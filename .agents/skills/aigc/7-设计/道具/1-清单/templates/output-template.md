# 道具清单

| 名称 | 首次登场 | 原文描述（关键词式） |
| --- | --- | --- |
|  |  |  |

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板渲染 `projects/aigc/<项目名>/7-设计/道具/1-清单/道具清单.md` 的项目级道具清单。 |
| Output format | 主体为 table 式 Markdown，且只使用 `名称`、`首次登场`、`原文描述（关键词式）` 三列。 |
| Output path | canonical path 为 `projects/aigc/<项目名>/7-设计/道具/1-清单/道具清单.md`。 |
| Naming convention | 文件名固定为 `道具清单.md`；`首次登场` 优先使用 `第N集 x-y-z`。 |
| Completion gate | 每项均回指组底 YAML `道具` 字段；别名归并和背景杂物过滤已由 LLM 裁决；表格三列固定。 |

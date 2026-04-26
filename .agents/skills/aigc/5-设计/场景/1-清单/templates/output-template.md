# 场景清单

source_grouping_paths:

- `projects/aigc/<项目名>/4-分组/第N集.md`

## 场景清单

| 名称 | 首次登场 | 原文描述（关键词式） |
| --- | --- | --- |
|  |  |  |

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成 `场景清单.md`，主体为 table 式 Markdown 清单。 |
| Output format | 仅使用 Markdown table 承载主体字段：`名称`、`首次登场`、`原文描述（关键词式）`。 |
| Output path | canonical 路径为 `projects/aigc/<项目名>/4-设计/场景/1-清单/场景清单.md`。 |
| Naming convention | 主清单固定命名 `场景清单.md`；可选报告固定命名 `执行报告.md`。 |
| Completion gate | 每行主体必须来自组底 YAML `场景` 字段，并完成 LLM 归并裁决与 review gate。 |

## 执行报告模板（可选）

| 项 | 内容 |
| --- | --- |
| 输入范围 |  |
| 已读取文件 |  |
| 归并策略 |  |
| 待核风险 |  |
| 校验结果 |  |

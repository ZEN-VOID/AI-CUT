# 场景清单

source_grouping_paths:

- `projects/aigc/<项目名>/8-分组/第N集.md`

## 场景清单

| 名称 | 首次登场 | 原文描述（关键词式） |
| --- | --- | --- |
|  |  |  |

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成 `场景清单.md`，主体为 table 式 Markdown 清单。 |
| Output format | 仅使用 Markdown table 承载主体字段：`名称`、`首次登场`、`原文描述（关键词式）`。 |
| Output path | canonical 路径为 `projects/aigc/<项目名>/3-主体/场景/1-清单/场景清单.md`。 |
| Naming convention | 主清单固定命名 `场景清单.md`；可选报告固定命名 `执行报告.md`。 |
| Completion gate | 每行主体必须来自 `subject-registry.yaml` 的 `subjects.scenes` 条目，并完成 LLM 归并裁决与 review gate。 |

## LLM-First Authorship Gate

- 本模板只定义表格形状，不生成清单判断、canonical 名称、归并理由或关键词描述。
- 禁止脚本批量生成、批量插入、正则套句或映射投影正文；每行必须来自 LLM 对 registry scenes 和 source anchors 的逐条裁决。

## 执行报告模板（可选）

| 项 | 内容 |
| --- | --- |
| 输入范围 |  |
| 已读取文件 |  |
| 归并策略 |  |
| 待核风险 |  |
| 校验结果 |  |

# 角色清单

source_grouping_paths:

- `projects/aigc/<项目名>/8-分组/第N集.md`

## 角色清单

| 名称 | 首次登场 | 原文描述（关键词式） |
| --- | --- | --- |
| 主名（别名：旧称、代称） | 第N集.md / source-anchor | registry 原词；source anchor 关键词；如有多状态写 `变体：常服/礼服/战斗态/战损态/受伤态/少年期/老年期` |

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成 table 式 Markdown `角色清单.md`；可另附 `执行报告.md`。 |
| Output format | 主体表格固定为 `名称`、`首次登场`、`原文描述（关键词式）` 三列。 |
| Output path | Canonical 路径为 `projects/aigc/<项目名>/3-主体/角色/1-清单/角色清单.md`。 |
| Variant boundary | 多服装、多状态和年龄阶段不新增列、不拆角色行；仅以紧凑关键词标签或可选 manifest sidecar 传递给设计阶段。 |
| Naming convention | 清单命名为 `角色清单.md`；首次登场使用分镜组 ID，必要时带 `第N集.md /`；别名写入 `名称` 单元，不新增列。 |
| Completion gate | 每行均可回指 `subject-registry.yaml` 的 `subjects.characters` 条目；归并与变体归属由 LLM 裁决；表头三列固定。 |

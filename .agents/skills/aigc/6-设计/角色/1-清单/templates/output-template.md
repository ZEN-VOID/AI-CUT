# 角色清单

source_grouping_paths:

- `projects/aigc/<项目名>/5-分组/第N集.md`

## 角色清单

| 名称 | 首次登场 | 原文描述（关键词式） |
| --- | --- | --- |
| 主名（别名：旧称、代称） | 第N集.md / 1-1-1 | YAML 原词；同组正文关键词 |

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成 table 式 Markdown `角色清单.md`；可另附 `执行报告.md`。 |
| Output format | 主体表格固定为 `名称`、`首次登场`、`原文描述（关键词式）` 三列。 |
| Output path | Canonical 路径为 `projects/aigc/<项目名>/6-设计/角色/1-清单/角色清单.md`。 |
| Naming convention | 清单命名为 `角色清单.md`；首次登场使用分镜组 ID，必要时带 `第N集.md /`；别名写入 `名称` 单元，不新增列。 |
| Completion gate | 每行均可回指 `5-分组` 组底 YAML `角色` 字段；归并由 LLM 裁决；表头三列固定。 |

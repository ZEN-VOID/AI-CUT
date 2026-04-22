# Character Cards -> Planning Bridge

## Purpose

本文件是 `story/1-Cards/角色卡` 与 `story/2-Planning` 之间的共享桥接真源。

它负责回答三件事：

1. 角色卡哪些字段允许进入规划文档。
2. 哪些字段必须继续留在角色卡侧，不得复制进规划文档。
3. `2-Planning` 父层与 `1-部级 / 2-卷级 / 3-章级` 各自能写什么、只能引用什么。

## Canonical Source Design

| carrier | truth_role | owner |
| --- | --- | --- |
| `1-Cards/2-角色卡/**/*.json` | 角色对象完整真源 | `1-Cards/角色卡` |
| `1-Cards/2-角色卡/角色关系图谱.md` | 关系图谱 side output | `1-Cards/角色卡` |
| `2-Planning/整体规划.md` | 宏观角色群、主题承担者与卷级分布摘要 | `2-Planning` 父层 |
| `2-Planning/第N卷/卷规划.md` | 卷级人物、关系摘要、任务钩子 | `2-Planning/2-卷级` |
| `2-Planning/第N卷/第N章.md` | 章级出场、任务线、线索/伏笔关联 | `2-Planning/3-章级` |

## Minimal Import Fields

规划阶段只允许导入以下最小人物信息：

- `character_id`
- `card_path`
- `name`
- `group`
- `primary_alignment`
- `narrative_function`
- `surface_goal / true_desire / need / change_payoff`
- `active_pressure`
- `growth_projection`
- `timeline_anchor`
- `setpiece_hint`

规划阶段只允许导入以下最小关系信息：

- `edge_id`
- `source_character_id`
- `target_character_id`
- `relation_type`
- `relation_status`
- `dramatic_tension`
- `planning_hooks`

## Fields That Must Stay On Character-Card Side

以下内容不得复制进 planning 文档：

- `history[]`
- `core.voice_and_presence.*`
- `core.relationship_ports`
- `current_state.current_resources`
- `experience_timeline.growth_log`
- `角色关系图谱.md` 的 Mermaid 正文与长段说明
- 任何完整人物履历、塑形 prose 与长段设定说明

## Parent And Child Writeback Boundaries

| unit | allowed read | allowed write |
| --- | --- | --- |
| `2-Planning` 父层 | 最小角色/关系投影 | 宏观角色群、主题承担者、跨卷角色分布摘要 |
| `1-部级` | 角色群与关系摘要 | 主题承担者、卷级分配提示 |
| `2-卷级` | 最小角色/关系投影、成长钩子 | `本卷登场人物`、卷级关系摘要、卷级任务钩子 |
| `3-章级` | 最小角色/关系投影、成长钩子 | `本章登场人物`、章级任务线、章级线索/伏笔关联 |

## Child Consumption Rules

### `1-部级`

- 只允许写宏观角色群、主题承担者与卷级角色分布提示。

### `2-卷级`

- 必须用最小人物投影来写 `本卷登场人物` 与 `本卷任务线`。
- 卷级关系说明只能写摘要与钩子，不得复制整条关系正文。

### `3-章级`

- 必须用最小人物投影来写 `本章登场人物`、`本章任务线`、`本章线索 / 本章伏笔` 的角色关联。
- 若需要更细人物依据，必须回读 `card_path`，不得在章级规划里复制人物履历。

## Hard Rules

1. `1-Cards/角色卡` 不直接写任何 planning 文档。
2. `2-Planning` 只写最小摘要、refs 与 hooks，不写角色完整事实。
3. planning 文档若与角色卡事实冲突，以单角色 JSON 与 `角色关系图谱.md` 为准。
4. 任何新增 planning 消费字段，必须先加到本桥接文档，再同步到相应 `SKILL.md / template / validator`。

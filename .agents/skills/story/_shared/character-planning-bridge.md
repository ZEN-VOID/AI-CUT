# Character Cards -> Planning Bridge

## Purpose

本文件是 `story/1-设定/角色卡` 与 `story/2-卷章` 之间的共享桥接真源。

它负责回答三件事：

1. 角色卡哪些字段允许进入规划文档。
2. 哪些字段必须继续留在角色卡侧，不得复制进规划文档。
3. `2-卷章` 父层与 `1-部级 / 2-卷级 / 3-章级` 各自能写什么、只能引用什么。

## Canonical Source Design

| carrier | truth_role | owner |
| --- | --- | --- |
| `1-设定/2-角色卡/**/*.json` | 角色对象完整真源 | `1-设定/角色卡` |
| `1-设定/2-角色卡/角色关系图谱.md` | 关系图谱 side output | `1-设定/角色卡` |
| `2-卷章/整体规划.md` | 宏观角色群、主题承担者与卷级分布摘要 | `2-卷章` 父层 |
| `2-卷章/第N卷/卷规划.md` | 卷级人物、关系摘要、任务钩子 | `2-卷章/2-卷级` |
| `2-卷章/第N卷/第N章.md` | 章级出场、任务线、线索/伏笔关联 | `2-卷章/3-章级` |

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
- `personality_tags / behavior_pattern / desire_pressure` 的最小摘要；仅用于判断章级爽点是否从角色个性、欲望、缺陷或惯常反应中自然长出

规划阶段只允许导入以下最小关系信息：

- `source_graph_path`
- `edge_id`
- `source_character_id`
- `target_character_id`
- `relation_type`
- `relation_status`
- `dramatic_tension`
- `contact_medium`
- `first_trigger`
- `turning_point`
- `payoff`
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
| `2-卷章` 父层 | 最小角色/关系投影 | 宏观角色群、主题承担者、跨卷角色分布摘要 |
| `1-部级` | 角色群与关系摘要 | 主题承担者、卷级分配提示 |
| `2-卷级` | 最小角色/关系投影、成长钩子 | `本卷登场人物`、卷级关系摘要、卷级任务钩子 |
| `3-章级` | 最小角色/关系投影、成长钩子 | `本章登场人物`、章级任务线、章级线索/伏笔关联 |

## Child Consumption Rules

### `1-部级`

- 只允许写宏观角色群、主题承担者与卷级角色分布提示。
- 必须把 `角色关系图谱.md` 作为角色网络输入之一，消费其分层关系裁决和最小关系投影，但不得复制 Mermaid 正文。

### `2-卷级`

- 必须用最小人物投影来写 `本卷登场人物` 与 `本卷任务线`。
- 卷级关系说明只能写摘要与钩子，不得复制整条关系正文。
- 必须把图谱中的 `contact_medium / first_trigger / turning_point / payoff` 转成卷级关系压力、信息流、物件流或任务钩子。

### `3-章级`

- 必须用最小人物投影来写 `本章登场人物`、`本章任务线`、`本章线索 / 本章伏笔` 的角色关联。
- `本章爽点设计` 必须回指最小人物投影或按需回读 `card_path`，说明爽点如何从角色个性、欲望、缺陷、压力或关系反应中放大出来。
- 爽点允许夸张、极致、强烈和戏剧化，但必须通过角色既有人格、处境压力、欲望方向或成长轨迹解释其合情理性。
- 若需要更细人物依据，必须回读 `card_path`，不得在章级规划里复制人物履历。
- 必须消费 `角色关系图谱.md` 的最小关系投影来确认本章关系压力、信息流载体、物件传递、证据残留和后续 payoff，不得只凭登场人物列表写互动。

## Drafting Context Handoff

- `3-初稿` 在正式写作 context pack 中必须加载 `projects/story/<项目名>/1-设定/2-角色卡/角色关系图谱.md` 的摘录或等价关系投影。
- drafting 只把它作为写作上下文，用于处理关系压力、联系方式、信息流、物件流和传导边；不得把图谱说明写入章节 frontmatter 或正文解释段。
- 若图谱缺失，drafting 可继续使用单角色 JSON 与章级 planning，但必须在 dry-run summary 或执行报告中标记 `relationship_graph_ref` 为空。

## Hard Rules

1. `1-设定/角色卡` 不直接写任何 planning 文档。
2. `2-卷章` 只写最小摘要、refs 与 hooks，不写角色完整事实。
3. planning 文档若与角色卡事实冲突，以单角色 JSON 与 `角色关系图谱.md` 为准。
4. 任何新增 planning 消费字段，必须先加到本桥接文档，再同步到相应 `SKILL.md / template / validator`。
5. `3-初稿` 必须加载关系图谱上下文，但不得把它提升为正文事实 owner；正文若需要改变关系事实，必须回到 `1-设定/角色卡` 或 `story-repair`。

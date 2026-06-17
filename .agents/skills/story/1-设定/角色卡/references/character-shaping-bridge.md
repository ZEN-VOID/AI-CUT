# 角色塑形桥接

> 定位：把旧式“人物设计指南”里的塑形工法，压缩为 `角色卡` 可直接消费的结构化映射。
> 作用域：仅服务 `story/1-设定/角色卡`。它不是第二套输出模板，不得替代 `templates/character-card.json`。

## 使用原则

- 先定 `group + cast_markers + narrative_function`，再补人物塑形字段。
- 人物塑形字段必须服务正式角色卡，不得写成与 JSON 脱节的长 prose。
- 不是每个角色都要填满所有槽位，但命中的角色类型必须有对应结构落点。

## 主角映射

### D-F-W-N-C 五维

| 设计工法 | 正式字段 | 写法要求 |
| --- | --- | --- |
| `Desire` | `core.desire_flaw_arc.surface_goal` / `core.desire_flaw_arc.true_desire` | 一个外在目标，一个更深层真实欲望；都必须能贯穿全书。 |
| `Flaw` | `core.desire_flaw_arc.flaw` | 写性格缺陷，不写抽象褒贬词。 |
| `Wound` | `core.desire_flaw_arc.wound` | 写过去创伤及其现在的行为后果。 |
| `Need` | `core.desire_flaw_arc.need` | 写角色真正缺少、但一开始不会主动承认的成长需求。 |
| `Change` | `core.desire_flaw_arc.change_payoff` + `experience_timeline.current_growth_stage` + `experience_timeline.belief_shift_track` | 写结局层级的价值观/人格跃迁，不写单次事件。 |

### 主角可代入性

- 平凡身世或极惨开局，不直接建字段，默认折叠到 `history` 与 `wound`。
- 正向底线、护短原则、行事边界，优先落到 `current_state.status`、`history`、`belief_shift_track`。

## 反派映射

| 设计工法 | 正式字段 | 写法要求 |
| --- | --- | --- |
| 镜像关系 | `core.antagonism_design.mirror_axis` | 写“和主角像在哪里、分叉在哪里”。 |
| 反派等级 | `core.antagonism_design.antagonist_rank` | 用 `C/B/A/S` 或等价分级；必须说明威胁来源。 |
| 自我正义逻辑 | `core.antagonism_design.self_justification` | 写反派自认为合理的信念。 |
| 压迫感 | `core.antagonism_design.pressure_profile` | 至少覆盖实力、智力、影响力中的命中项。 |

硬规则：

- 反派不能只有“坏”，至少要有 `mirror_axis` 或 `self_justification` 其一成立。
- 宿命级反派优先补足 `relationship_edges` 与 `history`，不要只写标签。

## 女主映射

| 设计工法 | 正式字段 | 写法要求 |
| --- | --- | --- |
| 类型库 | `group` + `core.narrative_function` + `core.voice_and_presence` | 类型只作风味提示，不得替代剧情职责。 |
| 非花瓶化 | `core.role_setpiece.highlight_moment` | 必须写一个具体高光动作/节点。 |
| 感情线服务主线 | `relationship_edges` + `experience_timeline.relationship_turning_points` | 关系推进必须能解释主线推进或阻力变化。 |

## 配角映射

| 设计工法 | 正式字段 | 写法要求 |
| --- | --- | --- |
| 功能位 | `core.narrative_function` | 明确其承担捧哏、引路、搞笑、信息、对照等哪类戏剧职责。 |
| 记忆点 | `core.role_setpiece.memory_point` | 用一句能被记住的动作、口头禅、武器或习惯。 |
| 非工具人 | `history` / `relationship_ports` / `current_state.active_pressure` | 至少有一个不完全依附主角的独立压力。 |

## 最小闭合清单

- 主角：`surface_goal + flaw + wound + need + change_payoff`
- 反派：`mirror_axis` 或 `self_justification` 至少一项
- 重要女主：`highlight_moment`
- 关键配角：`memory_point`

## 禁止事项

- 禁止把旧模板段落整块贴进角色 JSON。
- 禁止用“废柴流 / 冰山师尊 / 死党”之类标签直接替代 `narrative_function`。
- 禁止把人物塑形写成单章感受，仍需维持 `card_scope=full-series`。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 全剧集 roster 是否闭合，且没有单章临时卡？ | `roster` | `FAIL-CD-CHAR-ROSTER` | `SKILL.md` 的 `N2-ROSTER` | `series_roster`、`card_scope` |
| 角色桶、职责与 `cast_markers` 是否一致？ | `shaping` | `FAIL-CD-CHAR-SHAPING` | `SKILL.md` 的 `N3-SHAPE` | `group`、`cast_markers`、`narrative_function` |
| `Desire / Flaw / Wound / Need / Change` 是否落到结构字段？ | `shaping` | `FAIL-CD-CHAR-SHAPING` | `SKILL.md` 的 `N3-SHAPE` 与人物塑形硬映射 | `core.desire_flaw_arc`、`experience_timeline` |
| 主角三轴成长合同与当前态是否成立？ | `growth` | `FAIL-CD-CHAR-GROWTH` | `SKILL.md` 的 `N4-CLOSURE` 与成长系统硬映射 | `core.growth_contract`、`current_state.growth_state` |
| 关系边、专属物接口与下游最小投影是否闭合？ | `interface` | `FAIL-CD-CHAR-CLOSURE` | `SKILL.md` 的 `N4-CLOSURE` | `relationship_edges`、`exclusive_item_hooks` |
| 关系图谱是否只是投影而非第二真源？ | `graph` | `FAIL-CD-CHAR-GRAPH` | `SKILL.md` 的 `N5-PROJECT` | `角色关系图谱.md`、`source_graph_path` |
| 显式启用 subagents 时，顾问建议是否被转成可执行角色指导？ | `advisor_consultation` | `FAIL-CD-CHAR-ADVISOR` | `SKILL.md` 的 `N1-INTAKE` / `N3-SHAPE` | `advisor_consultation_packet.execution_brief` |

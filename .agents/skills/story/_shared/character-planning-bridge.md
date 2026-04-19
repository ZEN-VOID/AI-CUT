# Character Cards -> Planning Bridge

## Purpose

本文件是 `story/1-Cards/角色卡` 与 `story/2-Planning` 之间的共享桥接真源。

它负责回答三件事：

1. 角色卡哪些字段允许投影进入 `story_map`
2. 哪些字段必须继续留在角色卡侧，不得复制进 `story_map`
3. `2-Planning` 父层与 `2-章节规划 / 4-冲突设计 / 5-任务设计` 各自能写什么、只能引用什么

它不是第二套角色卡模板，也不是第二份 `story_map` 模板。

## Canonical Source Design

### Authoritative Sources

| carrier | truth_role | owner |
| --- | --- | --- |
| `1-Cards/2-角色卡/**/*.json` | 角色对象完整真源 | `1-Cards/角色卡` |
| `1-Cards/2-角色卡/角色关系图谱.md` | 关系图谱 side output | `1-Cards/角色卡` |
| `2-Planning/全息地图.json > content.holomap.character_roster_projection` | 规划侧最小角色投影 | `2-Planning` 父层 |
| `2-Planning/全息地图.json > content.holomap.relationship_graph_projection` | 规划侧最小关系投影 | `2-Planning` 父层 |

### Derived-Only Rule

- `story_map` 里的角色与关系结构只是 projection，不是角色卡第二真源。
- `2-Planning` 子技能只能引用 `character_id / edge_id` 和必要的最小 planning hook。
- 任何完整人物正文、历史段落、Mermaid 图、人物语气设定，都不得复制进 `story_map`。

## Story Map Import Slots

### 1. `content.holomap.character_roster_projection[]`

每个 entry 只保留规划阶段必需的最小角色投影：

| story_map field | source field | use |
| --- | --- | --- |
| `character_id` | `content.card_schema.character_card.card_id` | 规划阶段统一角色引用 id |
| `card_path` | 单角色 JSON 实际路径 | 下游需要回读完整卡时的定位锚点 |
| `name` | `core.identity.name` | 展示与章节绑定 |
| `group` | `group` | 主角/反派/次要/群像分桶 |
| `primary_alignment` | `core.cast_markers.primary_alignment` | 章节/冲突/任务快速判型 |
| `narrative_function` | `core.narrative_function` | 判断该角色能承担哪类戏剧职责 |
| `desire_line.surface_goal` | `core.desire_flaw_arc.surface_goal` | 任务表层目标引用 |
| `desire_line.true_desire` | `core.desire_flaw_arc.true_desire` | 任务深层驱动引用 |
| `desire_line.need` | `core.desire_flaw_arc.need` | 成长与任务代价引用 |
| `desire_line.change_payoff` | `core.desire_flaw_arc.change_payoff` | 长线兑现方向 |
| `pressure_snapshot.status` | `current_state.status` | 当前角色处境 |
| `pressure_snapshot.active_pressure` | `current_state.active_pressure` | 冲突/任务压力输入 |
| `growth_projection.enabled` | `core.growth_contract.growth_enabled` | 规划是否需要跟踪该角色成长轴 |
| `growth_projection.role` | `core.growth_contract.growth_role` | 主角强制 / 反派可选 / 不启用 |
| `growth_projection.active_arc_phase` | `current_state.growth_state.active_arc_phase` | 当前处于哪段成长弧 |
| `growth_projection.skill_stage` | `current_state.growth_state.skill.stage` | 能力轴当前段位 |
| `growth_projection.heart_stage` | `current_state.growth_state.heart.stage` | 心路轴当前段位 |
| `growth_projection.emotion_stage` | `current_state.growth_state.emotion.stage` | 情感轴当前段位 |
| `growth_projection.latest_growth_episode` | `current_state.growth_state.latest_growth_episode` | 上次 validated 蜕变落点 |
| `timeline_anchor` | `current_state.timeline_anchor` | 角色当前时间锚 |
| `current_growth_stage` | `experience_timeline.current_growth_stage` | 章节与任务推进的弧光阶段 |
| `setpiece_hint.highlight_moment` | `core.role_setpiece.highlight_moment` | 章节角色焦点与兑现位 |
| `setpiece_hint.memory_point` | `core.role_setpiece.memory_point` | 配角/群像记忆点引用 |
| `planning_flags.can_anchor_conflict` | 由 `group + narrative_function + active_pressure` 推导 | 冲突 child 快速筛选 |
| `planning_flags.can_anchor_mission` | 由 `desire_line + narrative_function` 推导 | 任务 child 快速筛选 |

### 2. `content.holomap.relationship_graph_projection`

规划阶段只保留最小关系投影，不复制 Markdown 正文：

| story_map field | source field | use |
| --- | --- | --- |
| `source_graph_path` | `1-Cards/2-角色卡/角色关系图谱.md` | 回指正式图谱 side output |
| `scope` | `relationship_graph.scope` | 明确仍是 `full-series` |
| `node_refs[]` | `character_roster_projection[].character_id` | 关系图谱有效节点集合 |
| `edge_projections[].edge_id` | `relationship_edges[].edge_id` | 关系边统一引用 id |
| `edge_projections[].source_character_id` | `relationship_edges[].source_character_id` | 冲突/任务 owner 关联 |
| `edge_projections[].target_character_id` | `relationship_edges[].target_character_id` | 冲突/任务 counterpart 关联 |
| `edge_projections[].relation_type` | `relationship_edges[].relation_type` | 盟友/亲情/仇怨/恋爱/师徒等 |
| `edge_projections[].relation_status` | `relationship_edges[].relation_status` | 当前关系态 |
| `edge_projections[].dramatic_tension` | `relationship_edges[].dramatic_tension` | 对抗或任务推进张力 |
| `edge_projections[].planning_hooks.chapter_focus_hint` | `relationship_edges[].planning_hooks.chapter_focus_hint` | 章节角色焦点提示 |
| `edge_projections[].planning_hooks.conflict_trigger` | `relationship_edges[].planning_hooks.conflict_trigger` | 冲突导火索提示 |
| `edge_projections[].planning_hooks.mission_dependency` | `relationship_edges[].planning_hooks.mission_dependency` | 任务依赖/交换关系提示 |
| `edge_projections[].planning_hooks.turning_point_refs[]` | `experience_timeline.relationship_turning_points` 投影 | 章节/任务引用关系转折点 |

## Fields That Must Stay On Character-Card Side

以下内容不进入 `story_map`，只允许通过 `card_path` 或 `source_graph_path` 回读：

- `history[]`
- `core.voice_and_presence.*`
- `core.relationship_ports`
- `core.exclusive_item_hooks` 的完整 payload
- `current_state.current_resources`
- `experience_timeline.growth_log`
- `core.growth_contract.axes.*` 的完整 ceiling / initial_state 设计
- `current_state.growth_state.*` 的完整 tension / recent_shift / primary_bond 细节
- `history[].growth_delta`
- `experience_timeline.belief_shift_track`
- `角色关系图谱.md` 的文字说明与 Mermaid 正文
- 任何为人物塑形服务的长 prose 注解

说明：

- 如果 `2-Planning` 子技能需要完整人物细节，应通过 `card_path` 回读单角色 JSON。
- 如果需要关系图谱的完整视觉说明，应通过 `source_graph_path` 回读 Markdown；不得把 Mermaid 正文复制进 `story_map`。

## Parent And Child Writeback Boundaries

### `2-Planning` 父层拥有

- 从角色卡真源导入 `character_roster_projection`
- 从角色图谱/关系边导入 `relationship_graph_projection`
- 负责这两个投影槽位的 normalize、去重、兼容与 root 写回

### `2-Planning` 子技能不拥有

- 重写 `character_roster_projection` 的人物事实
- 重写 `relationship_graph_projection` 的边事实
- 把完整角色卡字段复制进 `story_map`

### 具体 child 引用合同

| child skill | allowed read | allowed write |
| --- | --- | --- |
| `2-章节规划` | `character_roster_projection`、`relationship_graph_projection.edge_projections` | `chapter_boards[].bundled_elements.characters`、`chapter_boards[].planned_state.character_focus`、`chapter_boards[].planned_state.relationship_focus` |
| `4-冲突设计` | `character_roster_projection`、`relationship_graph_projection.edge_projections` | `conflict_threads[].character_refs`、`conflict_threads[].relationship_edge_refs`、`chapter_boards[].planned_state.conflict_pressure_map` |
| `5-任务设计` | `character_roster_projection`、`relationship_graph_projection.edge_projections`、`growth_projection` | `mission_threads[].owners`、`mission_threads[].counterparts`、`mission_threads[].relationship_edge_refs`、`chapter_boards[].planned_state.mission_character_hooks` |

## Child Consumption Rules

### `2-章节规划`

- 必须用 `character_roster_projection[].character_id` 填 `bundled_elements.characters`，不得临时造别名。
- 只允许在 `planned_state.character_focus` 记录角色焦点与弧光阶段目标。
- 若引用关系图谱，只允许写 `relationship_focus.edge_refs`，不得在 board 内复制整条关系正文。

### `4-冲突设计`

- 冲突 owner / target / pressure pairing 优先从 `relationship_graph_projection.edge_projections` 提取。
- `conflict_threads` 只写 `character_refs / relationship_edge_refs` 与必要的 pressure 结构，不复制人物履历。
- 若需要更细的人物依据，必须回读 `character_roster_projection[].card_path`。

### `5-任务设计`

- 任务 owner / counterpart 必须使用 `character_roster_projection[].character_id`。
- 任务 reveal / reversal 若依赖关系变化，必须引用 `relationship_edge_refs` 或 `planning_hooks.turning_point_refs`。
- 任务 child 只允许写角色与关系的任务引用，不允许覆盖角色卡的 desire / need / change 真相。

## Hard Rules

1. `1-Cards/角色卡` 不直接写 `2-Planning/全息地图.json`。
2. `2-Planning` 父层只写 projection，不写角色完整事实。
3. `2-Planning` 子技能只写 refs / hooks，不复制角色正文。
4. `story_map` 若与角色卡事实冲突，以单角色 JSON 与 `角色关系图谱.md` 为准。
5. 任何新增 planning 消费字段，必须先加到本桥接文档，再同步到相应 `SKILL.md / schema / template / validator`。

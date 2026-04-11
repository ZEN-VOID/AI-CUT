---
project: <项目名>
episode: 第1集
route: structure
source_span: <该集来源范围摘要>
group_count: 3
scene_unit_count: 3
duration_policy: 默认15秒
默认组时长: 15秒
分镜组时长映射: {"G03":"12秒"}
pace_tier: 中节奏
base_text_window: 150
warn_window: 120-180
hard_text_window: 225
structure_unit_count: 4
turning_point_count: 2
hard_dependency_count: 1
episode_load_score: 7
recommended_group_band: 3-4
---

## 本集分组目标

- 说明本集为什么要这样分组，以及希望下游如何消费这些组。

## 分组计划表

| group_id | group_name | source_span | structure_anchor | estimated_duration_seconds | effective_text_chars | window_status | group_unit_count | group_turning_point_count | group_dependency_count | group_load_score | dependency_note | parallelism | downstream_entry | boundary_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G01 | 潜入准备 | 第1场-第2场前半 | 场次链起点 + 潜入任务触发 | 15 | 136 | ok | 2 | 1 | 0 | 3 | none | 串行起点 | 1-规划/4-节奏 | 该段形成独立潜入任务起点 |
| G02 | 身份暴露 | 第2场后半-第3场前半 | 身份暴露 + 追捕启动 | 15 | 171 | warn-high | 1 | 1 | 1 | 3 | 依赖 G01 的潜入成功 | 需在 G01 后执行 | 1-规划/4-节奏 | 该段形成第一次强反转 |
| G03 | 脱身余波 | 第3场后半 | 追捕余波 + 阶段闭环 | 12 | 102 | warn-low | 1 | 0 | 1 | 2 | 依赖 G02 的暴露结果 | 可与后续资产准备并行 | 1-规划/4-节奏 | 该段承担当前集的阶段闭环 |

## G01 潜入准备

### 组目标

- 说明本组承担的任务目标。

### 组内容范围

- 写清本组覆盖的场次、段落或任务链。

### 结构锚点

- 写清本组依附的章节、场次、任务链或模块链锚点，确保边界可复算。

### 量化指标

- estimated_duration_seconds: <整数；若偏离 `默认组时长`，需同步登记到 frontmatter 的 `分镜组时长映射`>
- effective_text_chars: <整数>
- window_status: <<ok>|<warn-low>|<warn-high>|<error>>
- group_unit_count: <整数>
- group_turning_point_count: <整数>
- group_dependency_count: <整数>
- group_load_score: <整数>

### 交接约束

- 写清本组与前后组的依赖、不可拆条件与 handoff 要点。

### 依赖与并行性

- 说明本组依赖哪些前置组，哪些动作可并行，哪些必须串行。

### 下游建议

- 说明 `1-规划/4-节奏`、`2-组间`、`3-明细` 应如何消费本组。

## G02 身份暴露

### 组目标

- 说明本组承担的任务目标。

### 组内容范围

- 写清本组覆盖的场次、段落或任务链。

### 结构锚点

- 写清本组依附的章节、场次、任务链或模块链锚点，确保边界可复算。

### 量化指标

- estimated_duration_seconds: <整数；若偏离 `默认组时长`，需同步登记到 frontmatter 的 `分镜组时长映射`>
- effective_text_chars: <整数>
- window_status: <<ok>|<warn-low>|<warn-high>|<error>>
- group_unit_count: <整数>
- group_turning_point_count: <整数>
- group_dependency_count: <整数>
- group_load_score: <整数>

### 交接约束

- 写清本组与前后组的依赖、不可拆条件与 handoff 要点。

### 依赖与并行性

- 说明本组依赖哪些前置组，哪些动作可并行，哪些必须串行。

### 下游建议

- 说明 `1-规划/4-节奏`、`2-组间`、`3-明细` 应如何消费本组。

## G03 脱身余波

### 组目标

- 说明本组承担的任务目标。

### 组内容范围

- 写清本组覆盖的场次、段落或任务链。

### 结构锚点

- 写清本组依附的章节、场次、任务链或模块链锚点，确保边界可复算。

### 量化指标

- estimated_duration_seconds: <整数；若偏离 `默认组时长`，需同步登记到 frontmatter 的 `分镜组时长映射`>
- effective_text_chars: <整数>
- window_status: <<ok>|<warn-low>|<warn-high>|<error>>
- group_unit_count: <整数>
- group_turning_point_count: <整数>
- group_dependency_count: <整数>
- group_load_score: <整数>

### 交接约束

- 写清本组与前后组的依赖、不可拆条件与 handoff 要点。

### 依赖与并行性

- 说明本组依赖哪些前置组，哪些动作可并行，哪些必须串行。

### 下游建议

- 说明 `1-规划/4-节奏`、`2-组间`、`3-明细` 应如何消费本组。

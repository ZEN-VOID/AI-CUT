---
project: <项目名>
episode: 第1集
grouping_method: multidimensional_quantized
source_span: <该集来源范围摘要；若主故事源为 storyboard_script / hybrid_story_text，优先写成可机读镜号范围，如 镜1-13>
group_count: 3
scene_unit_count: 3
duration_policy: 默认15秒
默认组时长: 15秒
分镜组时长映射: {}
时长偏离证据: []
pace_tier: 中节奏
base_text_window: 150
warn_window: 120-150
hard_text_window: 165
structure_unit_count: 4
turning_point_count: 2
hard_dependency_count: 1
episode_load_score: 7
recommended_group_band: 3-4
外部分镜预设模式: standard
外部分镜锚点登记: []
---

## 本集分组目标

- 说明本集为什么要这样分组，以及希望下游如何消费这些组。

## 分组计划表

| group_id | group_name | source_span | structure_anchor | preset_anchor_policy | preset_anchor_ids | estimated_duration_seconds | effective_text_chars | window_status | group_unit_count | group_turning_point_count | group_dependency_count | group_load_score | dependency_note | parallelism | downstream_entry | boundary_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G01 | 潜入准备 | 第1场-第2场前半 | 场次链起点 + 潜入任务触发 | inherit | ["A01"] | 15 | 136 | ok | 2 | 1 | 0 | 3 | none | 串行起点 | 1-规划/4-节奏 | 该段形成独立潜入任务起点 |
| G02 | 身份暴露 | 第2场后半-第3场前半 | 身份暴露 + 追捕启动 | split-soft-lock | ["A01","A02"] | 15 | 149 | ok | 1 | 1 | 1 | 3 | 依赖 G01 的潜入成功 | 需在 G01 后执行 | 1-规划/4-节奏 | 该段形成第一次强反转 |
| G03 | 脱身余波 | 第3场后半 | 追捕余波 + 阶段闭环 | none | [] | 15 | 120 | ok | 1 | 0 | 1 | 2 | 依赖 G02 的暴露结果 | 可与后续资产准备并行 | 1-规划/4-节奏 | 该段承担当前集的阶段闭环 |

## G01 潜入准备

### 组目标

- 说明本组承担的任务目标。

### 组内容范围

- 写清本组覆盖的场次、段落或任务链。
- 若主故事源为 `storyboard_script / hybrid_story_text`，`分组计划表.source_span` 应优先写成可机读镜号范围，供 validator 回算 `effective_text_chars`。

### 结构锚点

- 写清本组依附的章节、场次、任务链或模块链锚点，确保边界可复算。

### 外部分镜锚点

- 写清当前组继承了哪些 `preset_registry` 锚点，以及本组对它们采取的是 `inherit / split-soft-lock / reference-only / none` 哪种策略。
- 若命中 `hard_lock`，必须显式说明“为什么当前组不能拆穿该锚点”。

### 量化指标

- estimated_duration_seconds: <整数；若偏离 `默认组时长`，需同步登记到 frontmatter 的 `分镜组时长映射` 与 `时长偏离证据`>
- effective_text_chars: <整数>
- window_status: <ok>
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

### 外部分镜锚点

- 写清当前组继承了哪些 `preset_registry` 锚点，以及本组对它们采取的是 `inherit / split-soft-lock / reference-only / none` 哪种策略。
- 若命中 `hard_lock`，必须显式说明“为什么当前组不能拆穿该锚点”。

### 量化指标

- estimated_duration_seconds: <整数；若偏离 `默认组时长`，需同步登记到 frontmatter 的 `分镜组时长映射` 与 `时长偏离证据`>
- effective_text_chars: <整数>
- window_status: <ok>
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

### 外部分镜锚点

- 写清当前组继承了哪些 `preset_registry` 锚点，以及本组对它们采取的是 `inherit / split-soft-lock / reference-only / none` 哪种策略。
- 若命中 `hard_lock`，必须显式说明“为什么当前组不能拆穿该锚点”。

### 量化指标

- estimated_duration_seconds: <整数；若偏离 `默认组时长`，需同步登记到 frontmatter 的 `分镜组时长映射` 与 `时长偏离证据`>
- effective_text_chars: <整数>
- window_status: <ok>
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

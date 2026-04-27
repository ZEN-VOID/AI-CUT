# Validation Child Output Contract

本文件定义 `review` 全部受治理子技能包的统一输出协议。

## Canonical Output Shape

每个子技能正式输出必须同时包含：

- `dimension_packet`
  - 当前维度的结构化 verdict
- `dimension_report_ref`
  - 对应 MD sidecar 的相对路径

## dimension_packet Minimum Fields

- `role_id`
- `dimension`
- `validation_context`
- `volume_ref`
- `chapter_refs`
- `pass`
- `score`
- `summary`
- `issues`
- `severity_counts`
- `critical_issues`
- `metrics`
- `default_rework_targets`
- `source_trace`
- `report_ref`
- `blocking_scope`

## issue Minimum Fields

每条 issue 至少包含：

- `id`
- `type`
- `severity`
- `chapter_ref`
- `location`
- `description`
- `suggestion`
- `can_override`
- `rework_target_step`
- `source_layer_owner`

## Hard Rules

1. 子技能不得独立写 `validation_status`、`routing_decision` 或 `handoff_targets`。
2. 子技能不得直接改写 `第V卷.validation.json`。
3. 子技能若识别到 source truth 冲突，必须通过 `source_layer_owner` 明示，而不是把所有问题都归为正文质量。
4. `dimension_report_ref` 必须落在 `review/第V卷/` 目录下。
5. 子技能可以给出默认返工节点，但最终 route 仍由父层聚合裁决。
6. 同一 validator 在 `drafting_inline` 与 `final_acceptance` 两种上下文下都必须使用同一套字段骨架。

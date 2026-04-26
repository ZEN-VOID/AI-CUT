# Review Child Output Contract

本文件定义 `aigc-review` 维度子技能的统一输出协议。

## Canonical Output Shape

每个维度子技能只返回：

- `dimension_packet`
- `dimension_report_ref`

## dimension_packet Minimum Fields

- `role_id`
- `dimension`
- `review_mode`
- `checkpoint_id`
- `stage`
- `scope_ref`
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
- `dimension_runtime`

## Hard Rules

1. 子技能不得独立写 `review_status`、`routing_decision` 或 `handoff_targets`。
2. 子技能不得直接改写 aggregate review packet。
3. 子技能若识别到 source truth 冲突，必须写 `source_layer_owner`。
4. `dimension_report_ref` 必须落在 aggregate packet 同级目录下。
5. 最终 route 由父层聚合裁决。
6. 若 runner 采用本地维度 checklist 而非真实 child subagent 执行，必须在 `dimension_runtime.execution_mode` 中显式标记，并记录 `skill_path_ref` 与 `context_ref`。

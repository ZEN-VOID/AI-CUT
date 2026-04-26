# Review Child Output Contract

本文件定义 `aigc-review` 维度 reviewer 的统一输出协议。维度 reviewer 消费 `references/dimensions/*.md` 中的细则，不是独立 Skill 2.0 子技能。

## Canonical Output Shape

每个维度 reviewer 只返回：

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

1. 维度 reviewer 不得独立写 `review_status`、`routing_decision` 或 `handoff_targets`。
2. 维度 reviewer 不得直接改写 aggregate review packet。
3. 维度 reviewer 若识别到 source truth 冲突，必须写 `source_layer_owner`。
4. `dimension_report_ref` 必须落在 aggregate packet 同级目录下。
5. 最终 route 由父层聚合裁决。
6. 若 runner 采用本地维度 checklist 而非真实 reviewer provider 执行，必须在 `dimension_runtime.execution_mode` 中显式标记，并记录 `dimension_spec_ref` 与 `dimension_spec_exists`。

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

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个维度 reviewer 是否只返回 `dimension_packet` 与 `dimension_report_ref`，没有把 prose summary、局部 verdict 或 provider 原始输出冒充 canonical 子输出？ | `GATE-REVIEW-CHILD-01` | `FAIL-REVIEW-CHILD-SHAPE` | `N3-DIMENSIONS` | aggregate 收到的 dimension output 列出两个 canonical field，额外非协议字段被记录或拒收。 |
| `dimension_packet` 是否包含最小字段集，尤其是 scope、pass、score、issues、severity_counts、critical_issues、metrics、source_trace、blocking_scope 与 `dimension_runtime`？ | `GATE-REVIEW-CHILD-02` | `FAIL-REVIEW-CHILD-MINIMUM` | `N3-DIMENSIONS` | `dimension_packet` 字段缺口清单、对应 dimension、scope_ref 与阻断等级。 |
| 维度 reviewer 是否没有独立写 `review_status`、`routing_decision`、`handoff_targets` 或直接改写 aggregate review packet？ | `GATE-REVIEW-CHILD-03` | `FAIL-REVIEW-CHILD-AUTHORITY` | `N4-AGGREGATE` | 父层聚合记录越权字段检查结果；若出现越权，标明维度与字段名。 |
| 维度 reviewer 识别 source truth 冲突时，是否写出 `source_layer_owner`、evidence refs 和 default rework target，供父层聚合成可执行 route？ | `GATE-REVIEW-CHILD-04` | `FAIL-REVIEW-CHILD-SOURCE` | `N3-DIMENSIONS` | `issues[*].source_layer_owner`、`source_trace`、`default_rework_targets` 与证据路径存在。 |
| `dimension_report_ref` 是否落在 aggregate packet 同级目录，且能被 aggregate packet 和 review summary 稳定引用？ | `GATE-REVIEW-CHILD-05` | `FAIL-REVIEW-CHILD-REPORT` | `N4-AGGREGATE` | report path、aggregate path、scope_ref、dimension 名称和缺失/路径漂移说明。 |
| 本地 checklist 降级执行时，`dimension_runtime.execution_mode`、`dimension_spec_ref`、`dimension_spec_exists` 与 provider 不可用原因是否完整？ | `GATE-REVIEW-CHILD-06` | `FAIL-REVIEW-CHILD-RUNTIME` | `N3-DIMENSIONS` | `dimension_runtime` 记录执行模式、spec 文件、provider path、本地 reviewer 和不可用来源。 |
| 维度输出是否可被父层计算 `dimension_scores`、`severity_counts`、`critical_issues`、`issues` 和 blocking scope，而不是只能人读不能聚合？ | `GATE-REVIEW-CHILD-07` | `FAIL-REVIEW-CHILD-AGGREGATION` | `N4-AGGREGATE` | aggregate 聚合前检查记录维度分数、严重度、critical issue、blocking scope 和缺口。 |
| 最终 route 是否仍由父层 aggregate 统一裁决，维度报告只提供建议返工目标而不直接放行或阻断 handoff？ | `GATE-REVIEW-CHILD-08` | `FAIL-REVIEW-CHILD-AUTHORITY` | `N5-ROUTE` | aggregate packet 中唯一 `routing_decision`、维度 sidecar 中无最终 route/status。 |

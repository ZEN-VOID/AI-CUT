# Checker Output Schema

## Dimension Packet Required Fields

- `role_id`
- `dimension`
- `validation_context`
- `pass`
- `issues`
- `severity_counts`
- `critical_issues`
- `score`
- `summary`
- `default_rework_targets`
- `source_trace`
- `report_ref`
- `blocking_scope`
- `volume_ref`
- `chapter_refs`

## Aggregate JSON Required Fields

- `validation_status`
- `validation_mode`
- `volume_ref`
- `chapter_refs`
- `selected_agents`
- `dimension_packets`
- `dimension_report_refs`
- `issues`
- `chapter_issue_index`
- `severity_counts`
- `critical_issues`
- `overall_score`
- `dimension_scores`
- `routing_decision`
- `handoff_targets`
- `rework_targets`
- `validation_ref`
- `source_trace`
- `evidence_refs`

## Hard Rules

- child output 只能增补维度字段，不得私自扩张父层 gate 语义。
- 若 machine-readable 字段变化，必须同步更新聚合消费点与示例 JSON。

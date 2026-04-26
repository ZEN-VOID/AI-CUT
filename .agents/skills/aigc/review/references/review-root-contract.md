# Review Root Contract

`aigc-review` 的 gate truth 固定为单一 aggregate review packet。六个维度 sidecar 只提供 evidence 与 dimension verdict，不并列裁决最终放行。

## Canonical Paths

- checkpoint aggregate packet: `projects/aigc/<项目名>/review/checkpoints/<checkpoint_id>/<scope_ref>.review.json`
- stage aggregate packet: `projects/aigc/<项目名>/review/stages/<stage>/<scope_ref>.review.json`
- release aggregate packet: `projects/aigc/<项目名>/review/releases/<scope_ref>.review.json`
- fact pack sidecar: `<scope_ref>.review.fact-pack.json`
- repair sidecar: `<scope_ref>.review.repair.json`
- review summary sidecar: `<scope_ref>.review.review.md`
- provider artifacts: `.code-reviewer/<scope_ref>.review/`

## Root Ownership

父层唯一拥有：

- `review_status`
- `review_mode`
- `checkpoint_id`
- `stage`
- `scope_ref`
- `selected_agents`
- `selected_dimensions`
- `dimension_runtime`
- `overall_score`
- `dimension_scores`
- `issues`
- `severity_counts`
- `critical_issues`
- `routing_decision`
- `handoff_targets`
- `rework_targets`
- `review_fact_pack_ref`
- `repair_plan_ref`
- `review_report_ref`
- `source_trace`
- `external_review`

## Boundary

- 父层可写 aggregate packet、repair sidecar、review summary 与治理桥接。
- 父层不得直接改写阶段 canonical 业务真源。
- 若 issue 属于上游 source truth，必须显式返回 `back_to_source_contract`。

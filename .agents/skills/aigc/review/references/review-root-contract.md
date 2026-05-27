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

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 当前 `review_mode` 是否唯一映射到 checkpoint、stage 或 release aggregate path，且 `scope_ref` 没有生成多个并列 gate truth？ | `GATE-REVIEW-ROOT-01` | `FAIL-REVIEW-ROOT-SCOPE` | `N1-REVIEW-INTAKE` | `review_scope_note` 记录 mode、stage/checkpoint、scope_ref、aggregate path 和冲突候选。 |
| aggregate packet 是否唯一拥有 `review_status`、`routing_decision`、`handoff_targets`、`rework_targets` 等根裁决字段，维度 sidecar 没有并列裁决？ | `GATE-REVIEW-ROOT-02` | `FAIL-REVIEW-ROOT-AUTHORITY` | `N4-AGGREGATE` | aggregate 字段清单、dimension sidecar 越权字段检查和唯一 gate owner 记录。 |
| 父层是否只写 aggregate packet、fact pack、repair sidecar、review summary 和治理桥接，没有直接改写阶段 canonical 业务真源？ | `GATE-REVIEW-ROOT-03` | `FAIL-REVIEW-ROOT-BOUNDARY` | `N4-AGGREGATE` | 写入文件清单、业务真源未改写检查、必要治理桥接路径。 |
| fact pack、repair sidecar、summary、provider artifacts 是否按 canonical paths 落在 aggregate 同级或指定目录，没有散落到阶段正文或旧 runner 路径？ | `GATE-REVIEW-ROOT-04` | `FAIL-REVIEW-ROOT-PATH` | `N1-REVIEW-INTAKE` | path alignment 表、孤立文件/旧路径排除记录、provider artifacts 目录。 |
| aggregate 是否聚合 `selected_dimensions`、`dimension_runtime`、`dimension_scores`、`issues`、`severity_counts` 和 `critical_issues`，而不是只保存人读总结？ | `GATE-REVIEW-ROOT-05` | `FAIL-REVIEW-ROOT-AGGREGATION` | `N4-AGGREGATE` | aggregate packet 字段覆盖、dimension refs、issue 合并和 score/severity 证据。 |
| 若 issue 属于上游 source truth，aggregate 是否显式返回 `back_to_source_contract` 并写清 source owner、返工目标与证据，而不是让当前阶段盲修？ | `GATE-REVIEW-ROOT-06` | `FAIL-REVIEW-ROOT-ROUTE` | `N5-ROUTE` | `routing_decision`、`rework_targets`、`source_trace`、`back_to_source_contract` 证据。 |
| 若 provider handoff 被阻断，aggregate 是否使用 `block_provider_handoff` 或可执行 repair route，并保留 handoff owner、缺失 pack 与恢复条件？ | `GATE-REVIEW-ROOT-07` | `FAIL-REVIEW-ROOT-ROUTE` | `N5-ROUTE` | provider 阻断原因、handoff target、repair_plan_ref、恢复检查项。 |
| PASS 或 PASS-WITH-WARNINGS 是否仍给出唯一下一入口或 warnings carry-forward，没有留下空 route、循环 route 或多个互斥 handoff？ | `GATE-REVIEW-ROOT-08` | `FAIL-REVIEW-ROOT-ROUTE` | `N5-ROUTE` | `routing_decision`、handoff target、warning items、循环/多目标检查结果。 |
| review summary 是否只是 aggregate 的人读投影，不替代 JSON aggregate 作为 gate truth，也不引入与 aggregate 冲突的结论？ | `GATE-REVIEW-ROOT-09` | `FAIL-REVIEW-ROOT-REPORT` | `N4-AGGREGATE` | summary 与 aggregate 字段对照、冲突项、report_ref 与生成时间。 |

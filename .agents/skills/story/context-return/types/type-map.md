# Context Return Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


`context-return` has lightweight type handling. It classifies the request and aggregate before loading the workflow branch.

## Type Profile

| variable | values | meaning |
| --- | --- | --- |
| `request_type` | `actualize_volume`, `query_route`, `resume_route`, `source_repair_route`, `contract_repair` | top-level route |
| `aggregate_gate_type` | `granted`, `pass_review_only`, `failed`, `missing_fields`, `unknown` | validation aggregate eligibility |
| `delta_type` | `cards`, `planning_sidecars`, `map`, `projection`, `mixed` | writeback target class |
| `accepted_manuscript_type` | `polished_final`, `draft_explicitly_accepted`, `draft_candidate`, `missing` | manuscript eligibility |
| `commit_risk` | `low`, `revision_drift`, `partial_write`, `missing_truth_source` | commit discipline risk |
| `artifact_type` | `context_return_json`, `route_report`, `repair_plan` | expected output shape |

## Routing Matrix

| signal | request_type | step impact | review impact |
| --- | --- | --- | --- |
| PASS + handoff to `review/` and `context-return` + `accepted_manuscript_stage=4-润色` | `actualize_volume` | enter `steps/context-return-workflow.md` at `N2-GATE` | full completion checklist |
| PASS + handoff to `review/` and `context-return` + explicit skip-polish acceptance | `actualize_volume` | enter with `accepted_manuscript_type=draft_explicitly_accepted` | note exception in artifact |
| PASS + handoff but only candidate `3-初稿` refs | `source_repair_route` or `resume_route` | no truth writeback | reject draft-state actualization |
| PASS + `handoff_to_review_only` | `query_route` or `resume_route` | no truth writeback | confirm no context-return artifact |
| non-PASS aggregate | `source_repair_route` | stop before delta normalize | report validation owner |
| missing required aggregate fields | `contract_repair` or upstream repair | repair schema/source before writeback | structural finding |
| user asks state/evidence only | `query_route` | route to query | no artifact |
| user asks continue/rerun/cleanup | `resume_route` | route to resume | no artifact |

## Field Gate

Required aggregate fields:

- `validation_status`
- `routing_decision`
- `handoff_targets`
- `validation_ref`
- `issues`
- `severity_counts`
- `overall_score`
- `volume_ref`
- `chapter_refs`
- `accepted_manuscript_stage`
- `accepted_manuscript_refs`

Required 上下文回流 delta families:

- `card_deltas`
- `map_deltas`
- `projection_refresh`
- `evidence_refs`

Empty deltas are allowed only when the run is a route report, not a formal context-return artifact.

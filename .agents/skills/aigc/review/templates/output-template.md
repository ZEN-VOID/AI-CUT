# aigc-review Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | aggregate review packet、fact pack、dimension reports、repair plan、review summary |
| Output format | JSON 为 gate 真源，Markdown 为人读摘要 |
| Output path | `projects/aigc/<项目名>/review/checkpoints/`、`projects/aigc/<项目名>/review/stages/`、`projects/aigc/<项目名>/review/releases/` |
| Naming convention | `<scope_ref>.review.json`、`<scope_ref>.review.fact-pack.json`、`<scope_ref>.review.repair.json`、`<scope_ref>.review.review.md` |
| Completion gate | mandatory dimensions 已聚合，`routing_decision` 与 `rework_targets` 可执行 |

## Aggregate Packet Shape

```json
{
  "review_status": "",
  "review_mode": "",
  "checkpoint_id": "",
  "stage": "",
  "scope_ref": "",
  "selected_dimensions": [],
  "selected_agents": [],
  "dimension_packets": [],
  "dimension_report_refs": [],
  "dimension_runtime": [],
  "issues": [],
  "severity_counts": {},
  "critical_issues": [],
  "overall_score": 0,
  "dimension_scores": {},
  "routing_decision": "",
  "handoff_targets": [],
  "rework_targets": [],
  "review_fact_pack_ref": "",
  "repair_plan_ref": "",
  "review_report_ref": "",
  "source_trace": [],
  "evidence_refs": [],
  "external_review": {}
}
```

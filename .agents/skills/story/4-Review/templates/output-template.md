# 4-Review Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 唯一卷级聚合 JSON；维护任务则输出 Skill 2.0 分区更新与验证说明。 |
| Output format | JSON aggregate、维度 MD sidecars、Markdown 维护报告。 |
| Output path | `projects/story/<项目名>/4-Review/第V卷.validation.json` 与 `projects/story/<项目名>/4-Review/第V卷/`。 |
| Naming convention | aggregate 使用 `第V卷.validation.json`；维度报告按 registry `report_filename`。 |
| Completion gate | aggregate 含 `validation_status / routing_decision / handoff_targets`，Skill 维护通过工作车间 validator。 |

## Aggregate JSON Minimum Shape

```json
{
  "validation_status": "PASS|FAIL-QUALITY|FAIL-COVENANT|FAIL-RUNTIME",
  "validation_mode": "final_acceptance",
  "volume_ref": "第0卷",
  "chapter_refs": [],
  "selected_agents": [],
  "dimension_packets": {},
  "dimension_report_refs": {},
  "issues": [],
  "chapter_issue_index": {},
  "severity_counts": {},
  "critical_issues": [],
  "overall_score": null,
  "dimension_scores": {},
  "routing_decision": "",
  "handoff_targets": [],
  "rework_targets": [],
  "validation_ref": "4-Review/第0卷.validation.json"
}
```

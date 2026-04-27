# Context Return Output Template

## Output Contract Alignment

- Required output: one canonical validated actualization artifact for the accepted volume, plus the ordered truth writebacks it records.
- Output format: JSON following `templates/context-return.json`, including `volume_ref`, `chapter_refs`, `accepted_manuscript_stage`, `accepted_manuscript_refs`, `validation_ref`, `context_return_delta`, `writeback_summary`, `gate_summary`, and `execution_notes`.
- Output path: `projects/story/<项目名>/context-return/第V卷.context-return.json`.
- Naming convention: use `第V卷.context-return.json` for volume-level runs and preserve the same `volume_ref` and `validation_ref` across refs.
- Completion gate: aggregate gate confirmed; deltas written serially; pending marker resolved into committed manifest; artifact points to validation and governance evidence; review verdict is pass or accepted pass_with_followups.

## Final Output

```json
{
  "meta": {
    "skill_id": "story-context-return",
    "volume_ref": "",
    "truth_role": "validated-context-return"
  },
  "inputs": {
    "project_root": "",
    "validation_ref": "",
    "accepted_manuscript_stage": "4-润色",
    "accepted_manuscript_refs": [],
    "routing_decision": "handoff_to_review_and_context_return",
    "handoff_targets": ["review/", "context-return"]
  },
  "content": {
    "context_return_delta": {
      "card_deltas": [],
      "map_deltas": [],
      "projection_refresh": [],
      "evidence_refs": []
    },
    "writeback_summary": {}
  },
  "gate_summary": {},
  "execution_notes": {}
}
```

## Evidence

- validation aggregate ref
- written file refs
- pending/committed manifest refs
- review verdict

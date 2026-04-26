# Loopback Output Template

## Output Contract Alignment

- Required output: one canonical validated actualization artifact for the accepted volume, plus the ordered truth writebacks it records.
- Output format: JSON following `templates/loopback.json`, including `volume_ref`, `chapter_refs`, `validation_ref`, `loopback_delta`, `writeback_summary`, `gate_summary`, and `execution_notes`.
- Output path: `projects/story/<项目名>/5-Loopback/第V卷.loopback.json`.
- Naming convention: use `第V卷.loopback.json` for volume-level runs and preserve the same `volume_ref` and `validation_ref` across refs.
- Completion gate: aggregate gate confirmed; deltas written serially; pending marker resolved into committed manifest; artifact points to validation and governance evidence; review verdict is pass or accepted pass_with_followups.

## Final Output

```json
{
  "meta": {
    "skill_id": "story-loopback",
    "volume_ref": "",
    "truth_role": "validated-actualization-loopback"
  },
  "inputs": {
    "project_root": "",
    "validation_ref": "",
    "routing_decision": "handoff_to_review_and_loopback",
    "handoff_targets": ["review/", "5-Loopback"]
  },
  "content": {
    "loopback_delta": {
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

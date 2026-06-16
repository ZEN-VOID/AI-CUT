# Fine-Tuning Report Template

## Output Contract Alignment

- Required output: One `Fine-Tuning Report` with target mapping, scheme selection, source/reference evidence, iteration ledger, comparison acceptance, owner boundary check, handoff patch, verdict, risks, and validation.
- Output format: Markdown report with optional local patch sidecar; no parallel full-stage draft unless the owning stage explicitly requests it.
- Output path: `projects/aigc/<项目名>/fine-tuning/<stage>/<artifact_slug>-tuning-report.md` when project-bound; chat-only output when no writeback is authorized.
- Naming convention: `stage-<stage_id>-<artifact_slug>-tuning-r<rounds>-YYYYMMDD.md`; patch id `ft-<stage_id>-<artifact_slug>-r<round>`.
- Completion gate: All convergence points pass, fatal fails are zero, comparison scores meet threshold, owner handoff is unique, and validation status is recorded.
- Module trigger evidence: Cite the `Module Trigger Matrix` row used for this run.
- Business analysis evidence: Summarize business goal, object, constraints, success criteria, complexity, and topology fit.
- Quant criteria evidence: Summarize action scope, evidence count, pass threshold, retry limit, and fallback evidence.
- Attention evidence: Summarize current attention anchor, drift signals, and any recenter handling.
- Checkpoint evidence: Summarize CHK-SCOPE, CHK-SEMANTIC, CHK-VALIDATION, and CHK-DARWIN status.
- Prompt eval evidence: List `test-prompts.json` ids and `eval_mode` when evaluation is requested.

## Target Stage Map

| target_id | stage | owning_skill | source_path_or_chat_anchor | tuning_direction | writeback_permission |
| --- | --- | --- | --- | --- | --- |

## Scheme Selection Matrix

| target_id | scheme_id | selected_rounds | required_reference | n/a_reason | gate_focus |
| --- | --- | --- | --- | --- | --- |

## Source Anchor Table

| target_id | source_anchor | source_truth | planned_change | preservation_check |
| --- | --- | --- | --- | --- |

## Reference Brief

| reference_id | reference_type | source_or_origin | extracted_principle | applied_to | boundary |
| --- | --- | --- | --- | --- | --- |

## Iteration Ledger

| target_id | round | round_goal | diagnosis | candidate_patch_summary | delta_from_baseline | next_round_target | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Comparison Acceptance Matrix

| target_id | dimension | baseline_issue | candidate_improvement | scheme_requirement | score_1_to_5 | fatal_fail | rework_target |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Owner Boundary Check

| target_id | owning_stage | accepted_patch_shape | forbidden_write | upstream_preservation | owner_handoff_path | verdict |
| --- | --- | --- | --- | --- | --- | --- |

## Owner Handoff Patch

| patch_id | target_id | patch_type | patch_summary | apply_owner | apply_notes |
| --- | --- | --- | --- | --- | --- |

## Execution Decision Trace

| decision | rule_source | input_evidence | rationale_summary | output_landing |
| --- | --- | --- | --- | --- |

## Reference Execution Matrix

| reference | load_status | trigger_reason | applied_to | evidence_in_output | verdict | n/a_reason |
| --- | --- | --- | --- | --- | --- | --- |

## Rule Evidence Map

| rule_or_gate | evidence_location | source_anchor | verdict |
| --- | --- | --- | --- |

## N/A Justification

| item | reason | risk |
| --- | --- | --- |

## Repair Log

| fail_code | issue | rework_target | repair_result |
| --- | --- | --- | --- |

## Validation Result

| check | command_or_method | result | notes |
| --- | --- | --- | --- |

## Final Verdict

`pass | needs_rework | blocked | chat_only_recommendation`

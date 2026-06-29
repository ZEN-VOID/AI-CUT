# F2 Execution Report: <project-or-topic>

## Run Summary

- Route:
- Work root:
- Render requested:
- Final status:
- Canonical output:

## Loaded Context Manifest

| context_or_module | path | load_status | trigger_reason |
| --- | --- | --- | --- |
| F2 SKILL | `.agents/skills/workflow/F2/SKILL.md` |  |  |
| F2 CONTEXT | `.agents/skills/workflow/F2/CONTEXT.md` |  |  |
| hyperframes | `.agents/skills/hyperframes/SKILL.md` |  |  |

## Execution Decision Trace

| node | key_decision | input_evidence | output_artifact | verdict |
| --- | --- | --- | --- | --- |
| `N1-INTAKE` |  |  |  |  |
| `N2-HYPERFRAMES-LOAD` |  |  |  |  |
| `N3-MEDIA-EVIDENCE` |  |  |  |  |
| `N4-DIALOGUE-CLOCK` |  |  |  |  |
| `N5-STORYBOARD-PLAN` | include asset diversity / usage ledger decision for batch or semantic-equivalent scripts |  |  |  |
| `N6-HYPERFRAMES-AUTHOR` |  |  |  |  |
| `N7-PREVIEW-VALIDATE` |  |  |  |  |
| `N8-RENDER-VERIFY` |  |  |  |  |
| `N9-CLOSE` |  |  |  |  |

## Reference Execution Matrix

| reference | load_status | trigger_reason | applied_to | evidence_in_output | verdict | n/a_reason |
| --- | --- | --- | --- | --- | --- | --- |
| `references/f1-to-f2-migration-matrix.md` |  |  |  |  |  |  |

## Rule Evidence Map

| rule_or_gate | output_location | evidence | verdict |
| --- | --- | --- | --- |
| HyperFrames-only runtime |  |  |  |
| reference-only boundary |  |  |  |
| asset evidence |  |  |  |
| deep manifest tags | `asset_evidence.json` / manifest usage notes | semantic_vector, trigger_profile, visual_signature, variation_profile, analysis_slice_id |  |
| asset usage ledger | `asset_usage_ledger.json` | before/after usage counts, planned usage, actual usage |  |
| platform dedup diversity | `asset_diversity_audit.json` / `f2_composition_plan.json` | variation axes, reuse penalties, duplicate exceptions |  |
| dialogue clock | `dialogue_alignment.json` / `dialogue_sync_validation.json` | per-cue anchors, script spans, caption types, validator verdict |  |
| composition plan |  |  |  |
| preview validation |  |  |  |
| render verification |  |  |  |
| final output contract |  |  |  |

## Validation Results

| check | command_or_method | status | evidence |
| --- | --- | --- | --- |
| lint | `npx hyperframes lint` |  |  |
| validate | `npx hyperframes validate` |  |  |
| inspect | `npx hyperframes inspect` |  |  |
| snapshot | `npx hyperframes snapshot` |  |  |
| dialogue sync | `python3 .agents/skills/workflow/F2/scripts/validate_dialogue_sync.py --strict-final <project-root>` |  | `dialogue_sync_validation.json` |
| render | `npx hyperframes render` |  |  |
| final file | file / ffprobe check |  |  |

## Asset Diversity Audit

| item | status | evidence |
| --- | --- | --- |
| usage ledger loaded before planning |  |  |
| planned usage written before authoring |  |  |
| actual usage written after final verification |  |  |
| repeated segment exceptions |  |  |
| repeated image/PiP exceptions |  |  |
| same-source runtime share |  |  |
| semantic-equivalent variation axes |  |  |
| manifest deep-tag consumption |  |  |

## Repair Log

| failure_code | symptom | rework_target | repair_action | result |
| --- | --- | --- | --- | --- |

## N/A Justification

| item | reason | impact |
| --- | --- | --- |

## Source Sync Check

| question | answer | action |
| --- | --- | --- |
| Did this run reveal a reusable workflow failure or success pattern? |  |  |
| Did this run modify source-level artifacts? |  |  |
| Were registry/routes/templates affected? |  |  |
| Is CONTEXT writeback needed? |  |  |

## Residual Risk And Next Step

- Blocking:
- Non-blocking:
- Next step:

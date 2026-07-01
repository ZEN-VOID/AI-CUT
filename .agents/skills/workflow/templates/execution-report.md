# Workflow Execution Report: <project-or-topic>

## Run Summary

- Route:
- Work root:
- Process root:
- Output date root:
- Single final root:
- Final collection root:
- Render requested:
- Final status:
- Canonical output:

## Loaded Context Manifest

| context_or_module | path | load_status | trigger_reason |
| --- | --- | --- | --- |
| workflow SKILL | `.agents/skills/workflow/SKILL.md` |  |  |
| workflow CONTEXT five-file layer | `.agents/skills/workflow/CONTEXT/` |  |  |
| hyperframes | `.agents/skills/hyperframes/SKILL.md` |  |  |

## Execution Decision Trace

| node | key_decision | input_evidence | output_artifact | verdict |
| --- | --- | --- | --- | --- |
| `N1-INTAKE` |  |  |  |  |
| `N2-HYPERFRAMES-LOAD` |  |  |  |  |
| `N3-MEDIA-EVIDENCE` |  |  |  |  |
| `N4-DIALOGUE-CLOCK` |  |  |  |  |
| `N5-STORYBOARD-PLAN` | include hook/content/CTA structure, background throughline, four-layer plan, and asset diversity / usage ledger decision for batch or semantic-equivalent scripts |  |  |  |
| `N6-HYPERFRAMES-AUTHOR` |  |  |  |  |
| `N7-PREVIEW-VALIDATE` |  |  |  |  |
| `N8-RENDER-VERIFY` |  |  |  |  |
| `N9-CLOSE` |  |  |  |  |

## Reference Execution Matrix

| reference | load_status | trigger_reason | applied_to | evidence_in_output | verdict | n/a_reason |
| --- | --- | --- | --- | --- | --- | --- |
| `references/legacy-migration-matrix.md` |  |  |  |  |  |  |

## Rule Evidence Map

| rule_or_gate | output_location | evidence | verdict |
| --- | --- | --- | --- |
| HyperFrames-only runtime |  |  |  |
| reference-only boundary |  |  |  |
| asset evidence |  |  |  |
| shared asset pool boundary | `projects/素材/` / `projects/示例/` | read-only source pool, not daily output root |  |
| workflow directory routing | `.agents/skills/workflow/` | Directory Structure, README tree, Module Matrix and registry row agree |  |
| workflow context semantics | `.agents/skills/workflow/CONTEXT/` | five files exist; no legacy `CONTEXT.md` remains |  |
| process file boundary | `projects/output/<日期>/过程/` | project files, logs, snapshots, validation reports and intermediate artifacts stay under process root |  |
| single final output | `projects/output/<日期>/` | single-task final videos are moved/collected out of `过程/` after verification |  |
| layered rhythm assembly | `workflow_composition_plan.json` | hook_opening/content_body/private_traffic_cta, background_throughline, per-segment background/PiP/caption/editorial overlay layers |  |
| deep manifest tags | `asset_evidence.json` / manifest usage notes | semantic_vector, trigger_profile, visual_signature, variation_profile, analysis_slice_id |  |
| asset usage ledger | `asset_usage_ledger.json` | before/after usage counts, planned usage, actual usage |  |
| platform dedup diversity | `asset_diversity_audit.json` / `workflow_composition_plan.json` | variation axes, reuse penalties, duplicate exceptions |  |
| dialogue clock | `dialogue_alignment.json` / `dialogue_sync_validation.json` | per-cue anchors, script spans, caption types, validator verdict |  |
| visual contract | `visual_contract_validation.json` | audience-visible text, caption integrity, overlay/PiP and ledger checks |  |
| composition plan |  |  |  |
| preview validation |  |  |  |
| render verification |  |  |  |
| batch final collection | `projects/output/<日期>/成片/` | moved/collected final videos and updated `asset_usage_ledger.json.final_path` |  |
| final output contract |  |  |  |

## Validation Results

| check | command_or_method | status | evidence |
| --- | --- | --- | --- |
| lint | `npx hyperframes lint` |  |  |
| validate | `npx hyperframes validate` |  |  |
| inspect | `npx hyperframes inspect` |  |  |
| snapshot | `npx hyperframes snapshot` |  |  |
| dialogue sync | `python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --strict-final <project-root>` |  | `dialogue_sync_validation.json` |
| visual contract | `python3 .agents/skills/workflow/scripts/validate_visual_contract.py <project-root>` |  | `visual_contract_validation.json` |
| render | `npx hyperframes render` |  |  |
| final file | file / ffprobe check |  |  |
| process file boundary | directory listing / path audit |  | `projects/output/<日期>/过程/` |
| batch final collection | directory listing / ledger final_path check |  | `projects/output/<日期>/成片/` |
| directory routing | file listing / README / registry audit |  | `.agents/skills/workflow/` |
| context semantics | five-file list / writeback map audit |  | `.agents/skills/workflow/CONTEXT/` |

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

## Layered Assembly Audit

| item | status | evidence |
| --- | --- | --- |
| hook_opening segment planned |  |  |
| content_body segment planned |  |  |
| private_traffic_cta segment planned |  |  |
| background_throughline continuous and mask=none |  |  |
| content subtypes comic_drama/tool_demo/revenue_proof covered or exception recorded |  |  |
| every segment declares background/PiP/caption/editorial overlay layers |  |  |
| editorial overlays are core words or short summaries |  |  |

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
| Is CONTEXT/ writeback needed? |  |  |

## Residual Risk And Next Step

- Blocking:
- Non-blocking:
- Next step:

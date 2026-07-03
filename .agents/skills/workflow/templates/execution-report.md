# Workflow Execution Report: <project-or-topic>

## Run Summary

- Route:
- Audience profile:
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
| script/audio stem pairing | `workflow_intake.json` / `dialogue_alignment.json` | `projects/内容/文案/文案N.txt` pairs only with `projects/内容/音频/文案N.mp3`; `BGM.*` is not audio_clock |  |
| selected script/audio pair | `workflow_intake.json.selected_script_audio_pair` / `dialogue_alignment.json.source_script/source_audio/script_audio_stem` | current material-pool routes must use explicit same-stem source paths; no generated replacement unless explicitly authorized |  |
| workflow directory routing | `.agents/skills/workflow/` | Directory Structure, README tree, Module Matrix and registry row agree |  |
| workflow context semantics | `.agents/skills/workflow/CONTEXT/` | five files exist; no legacy `CONTEXT.md` remains |  |
| audience profile | `workflow_intake.json.audience_profile` | short-video platform C-end viewers / external potential customers, not internal learning exchange or project review |  |
| process file boundary | `projects/output/<日期>/过程/` | project files, logs, snapshots, validation reports and intermediate artifacts stay under process root |  |
| single final output | `projects/output/<日期>/` | single-task final videos are moved/collected out of `过程/` after verification |  |
| layered rhythm assembly | `workflow_composition_plan.json` | hook_opening/content_body/private_traffic_cta, background_throughline, per-segment background/PiP/caption/editorial overlay layers, background mask=none opacity=1 |  |
| deep manifest tags | `asset_evidence.json` / manifest usage notes | semantic_vector, trigger_profile, visual_signature, variation_profile, analysis_slice_id |  |
| asset usage ledger | `asset_usage_ledger.json` | before/after usage counts, planned usage, actual usage |  |
| material usage monitor | `projects/素材使用监控.csv` | global usage counts by material path and usage degree (`全片` / `部分切片`) updated after final verification |  |
| platform dedup diversity | `asset_diversity_audit.json` / `workflow_composition_plan.json` | variation axes, reuse penalties, duplicate exceptions |  |
| dialogue clock | `dialogue_alignment.json` / `dialogue_sync_validation.json` | per-cue anchors, script spans, script order, caption types, HTML cue-id mapping, validator verdict |  |
| visual contract | `visual_contract_validation.json` | audience-visible text, no internal process/learning titles, caption integrity, opening full-display, traffic no-upscale, PiP grid/size, overlay/PiP and ledger checks |  |
| composition plan |  |  |  |
| preview validation |  |  |  |
| render verification |  | local final MP4, not browser/page preview |  |
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
| script/audio pair sync | `python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --strict-final --require-script-audio-pair <project-root>` | required for `projects/内容/文案/` + `projects/内容/音频/` routes | `dialogue_sync_validation.json` |
| visual contract | `python3 .agents/skills/workflow/scripts/validate_visual_contract.py <project-root>` |  | `visual_contract_validation.json` |
| render | `npx hyperframes render` |  |  |
| final file | file / ffprobe check | local canonical MP4 required |  |
| process file boundary | directory listing / path audit |  | `projects/output/<日期>/过程/` |
| batch final collection | directory listing / ledger final_path check |  | `projects/output/<日期>/成片/` |
| material usage monitor | `python3 .agents/skills/workflow/scripts/update_asset_usage_monitor.py <batch-or-output-root>` / `--validate-only` |  | `projects/素材使用监控.csv` |
| directory routing | file listing / README / registry audit |  | `.agents/skills/workflow/` |
| context semantics | five-file list / writeback map audit |  | `.agents/skills/workflow/CONTEXT/` |

## Asset Diversity Audit

| item | status | evidence |
| --- | --- | --- |
| usage ledger loaded before planning |  |  |
| planned usage written before authoring |  |  |
| actual usage written after final verification |  |  |
| global material monitor updated |  |  |
| repeated segment exceptions |  |  |
| repeated image/PiP exceptions |  |  |
| same-source runtime share |  |  |
| semantic-equivalent variation axes |  |  |
| manifest deep-tag consumption |  |  |

## Layered Assembly Audit

| item | status | evidence |
| --- | --- | --- |
| hook_opening segment planned |  |  |
| hook_opening uses projects/素材/开头素材 or opening_hook |  |  |
| opening material shown full-frame for 5-10 seconds |  |  |
| content_body segment planned |  |  |
| private_traffic_cta segment planned |  |  |
| private traffic material no-upscale/native-scale evidence |  |  |
| background_throughline continuous, mask=none and opacity=1 |  |  |
| content subtypes comic_drama/tool_demo/revenue_proof covered or exception recorded |  |  |
| every segment declares background/PiP/caption/editorial overlay layers |  |  |
| editorial overlays are matched-copy summary titles with source cue/text/reason evidence |  |  |
| editorial overlays do not display workflow/process/learning labels |  |  |
| PiP has simultaneous multi-window grid group and readable dimensions |  |  |

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

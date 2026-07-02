# Workflow Output Summary: <project-or-topic>

## Output Contract Alignment

| output_contract_field | template_section |
| --- | --- |
| Required output | Delivery Status |
| Output format | Artifact Index |
| Output path | Path Map |
| Naming convention | Path Map |
| Completion gate | Validation Summary |
| Exception report | Residual Risk |

## Delivery Status

- Route:
- Work root:
- Process root:
- Output date root:
- Single final root:
- Final collection root:
- Render requested:
- Completion level: `plan_only` / `project_validated` / `final_rendered` / `blocked`
- Canonical output:

## Artifact Index

| artifact | path | status | notes |
| --- | --- | --- | --- |
| intake | `workflow_intake.json` |  |  |
| script/audio pair map | `workflow_intake.json.script_audio_pair_map` | required when using `projects/内容/文案/` + `projects/内容/音频/` batch inputs; same stem only, `BGM.*` excluded from audio_clock |  |
| selected script/audio pair | `workflow_intake.json.selected_script_audio_pair` / `dialogue_alignment.json.source_script/source_audio/script_audio_stem` | required for current `projects/内容/文案/` + `projects/内容/音频/` routes; no generated replacement unless explicitly authorized |  |
| asset evidence | `asset_evidence.json` |  |  |
| asset usage ledger | `asset_usage_ledger.json` | batch / semantic-equivalent scripts require before/after usage records |  |
| material usage monitor | `projects/素材使用监控.csv` | global four-column monitor: 素材名 / 文件路径 / 使用次数 / 使用程度 |  |
| asset diversity audit | `asset_diversity_audit.json` | batch / semantic-equivalent scripts require variation axes and reuse exceptions |  |
| dialogue alignment | `dialogue_alignment.json` | include per-cue audio anchors, script spans, script order, caption type, sync method, and tolerance/conditional notes |  |
| dialogue sync validation | `dialogue_sync_validation.json` | final route requires `validate_dialogue_sync.py --strict-final` pass for timing, script/audio order, and HTML cue-id mapping; fail returns to `N4` |  |
| visual contract validation | `visual_contract_validation.json` | final/social-ad/batch routes require audience-visible text, caption, overlay, PiP, layered assembly and ledger checks |  |
| reference rhythm | `reference_rhythm.json` |  |  |
| storyboard | `STORYBOARD.md` |  |  |
| composition plan | `workflow_composition_plan.json` | include `background_throughline` and `timeline_segments` for hook/content/CTA plus background/PiP/caption/editorial overlay layers |  |
| HyperFrames project | `index.html` / project root |  |  |
| snapshots | `snapshots/` |  |  |
| final render | `<work-root>/renders/<project-slug>_workflow_final.mp4` | local file required; browser/page preview is not final output |  |
| single final output | `projects/output/<日期>/<project-slug>_workflow_final.mp4` | required local canonical MP4 for single final outputs unless user supplied another final root |  |
| batch final collection | `projects/output/<日期>/成片/<project-slug>_workflow_final.mp4` | required local canonical MP4 for batch final outputs |  |
| execution report | `reports/workflow-execution-report-<timestamp>.md` |  |  |
| workflow context layer | `.agents/skills/workflow/CONTEXT/` | source-upgrade/audit routes require five-file context structure |  |

## Path Map

- Input media:
- Script/audio pair map:
- Selected script/audio pair:
- Shared asset roots: `projects/素材/`, `projects/示例/`
- Material usage monitor: `projects/素材使用监控.csv`
- Process root: `projects/output/<日期>/过程/`
- Adopted assets:
- HyperFrames project:
- Preview/snapshot:
- Render:
- Single final:
- Batch final collection:
- Canonical local MP4:
- Report:

## Validation Summary

| gate | status | evidence | rework_target |
| --- | --- | --- | --- |
| `C1-INPUT-LOCKED` |  |  |  |
| `C2-EVIDENCE-READY` |  |  |  |
| `C3-DIALOGUE-CLOCKED` |  | `dialogue_alignment.json` + `dialogue_sync_validation.json` pass, including script order/audio anchor order/HTML cue-id mapping; current素材池 route includes `--require-script-audio-pair` evidence | `N4-DIALOGUE-CLOCK` |
| `C4-PLAN-LOCKED` |  | `workflow_composition_plan.json` with layered assembly, `background_throughline mask=none opacity=1`, and `asset_diversity_audit.json` for batch / semantic-equivalent scripts | `N5-STORYBOARD-PLAN` |
| `C6-PREVIEW-VALIDATED` |  |  |  |
| `C7-RENDER-VERIFIED` |  | local MP4 render evidence plus current dialogue sync and visual contract validation | `N8-RENDER-VERIFY` |
| `C8-FINAL-OUTPUT` |  | canonical local output path; single final listed under `projects/output/<日期>/`, batch final files listed under `projects/output/<日期>/成片/` when applicable; `projects/素材使用监控.csv` updated after final verification | `N9-CLOSE` |
| `C10-SKILL-2-RUNTIME-READY` |  | Directory Structure, README tree, Module Matrix, registry context carriers and `CONTEXT/` five files agree | `Directory Structure & Detail Routing Contract` |

## Residual Risk

- Blocking:
- Non-blocking:
- Next action:

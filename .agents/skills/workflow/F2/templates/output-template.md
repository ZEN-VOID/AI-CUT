# F2 Output Summary: <project-or-topic>

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
- Render requested:
- Completion level: `plan_only` / `project_validated` / `final_rendered` / `blocked`
- Canonical output:

## Artifact Index

| artifact | path | status | notes |
| --- | --- | --- | --- |
| intake | `f2_intake.json` |  |  |
| asset evidence | `asset_evidence.json` |  |  |
| asset usage ledger | `asset_usage_ledger.json` | batch / semantic-equivalent scripts require before/after usage records |  |
| asset diversity audit | `asset_diversity_audit.json` | batch / semantic-equivalent scripts require variation axes and reuse exceptions |  |
| dialogue alignment | `dialogue_alignment.json` | include per-cue audio anchors, script spans, caption type, sync method, and tolerance/conditional notes |  |
| dialogue sync validation | `dialogue_sync_validation.json` | final route requires `validate_dialogue_sync.py --strict-final` pass; fail returns to `N4` |  |
| reference rhythm | `reference_rhythm.json` |  |  |
| storyboard | `STORYBOARD.md` |  |  |
| composition plan | `f2_composition_plan.json` |  |  |
| HyperFrames project | `index.html` / project root |  |  |
| snapshots | `snapshots/` |  |  |
| final render | `renders/<project-slug>_f2_final.mp4` |  |  |
| execution report | `reports/F2-execution-report-<timestamp>.md` |  |  |

## Path Map

- Input media:
- Adopted assets:
- HyperFrames project:
- Preview/snapshot:
- Render:
- Report:

## Validation Summary

| gate | status | evidence | rework_target |
| --- | --- | --- | --- |
| `C1-INPUT-LOCKED` |  |  |  |
| `C2-EVIDENCE-READY` |  |  |  |
| `C3-DIALOGUE-CLOCKED` |  | `dialogue_alignment.json` + `dialogue_sync_validation.json` pass or conditional reason | `N4-DIALOGUE-CLOCK` |
| `C4-PLAN-LOCKED` |  | `f2_composition_plan.json` + `asset_diversity_audit.json` for batch / semantic-equivalent scripts | `N5-STORYBOARD-PLAN` |
| `C6-PREVIEW-VALIDATED` |  |  |  |
| `C7-RENDER-VERIFIED` |  | final render evidence plus current dialogue sync validation for dialogue captions | `N8-RENDER-VERIFY` |
| `C8-FINAL-OUTPUT` |  |  |  |

## Residual Risk

- Blocking:
- Non-blocking:
- Next action:

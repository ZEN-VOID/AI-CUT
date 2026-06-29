# F2 PRP: <project-or-topic>

## Scope

- User goal:
- Route:
- Output target:
- Render requested:
- Completion target:

## Inputs

| input_class | source | status | decision |
| --- | --- | --- | --- |
| content_truth |  |  |  |
| audio_clock |  |  |  |
| source_media |  |  |  |
| reference_media |  |  |  |
| output_target |  |  |  |
| constraints |  |  |  |

## HyperFrames Module Plan

| module | load_reason | expected_output |
| --- | --- | --- |
| hyperframes |  |  |
| hyperframes-core |  |  |
| hyperframes-cli |  |  |
| hyperframes-media |  |  |
| hyperframes-animation |  |  |
| hyperframes-creative |  |  |
| media-use |  |  |

## Evidence Plan

| evidence | method | pass_gate |
| --- | --- | --- |
| `asset_evidence.json` | Codex visual understanding / frame review | `C2-EVIDENCE-READY` |
| `dialogue_alignment.json` | supplied transcript, HyperFrames media transcribe, or per-cue manual timing review with audio anchors | `C3-DIALOGUE-CLOCKED` |
| `dialogue_sync_validation.json` | run `scripts/validate_dialogue_sync.py --strict-final` against project root and HTML caption timeline | `C3-DIALOGUE-CLOCKED` / `C7-RENDER-VERIFIED` |
| `reference_rhythm.json` | rhythm/style observation only | `FAIL-REFERENCE-COPY` gate |
| `f2_composition_plan.json` | LLM-authored plan after evidence | `C4-PLAN-LOCKED` |

## Storyboard Outline

| segment | cue_or_time | main_visual | overlay | transition | audio |
| --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |

## Validation Plan

- HyperFrames lint:
- HyperFrames validate:
- HyperFrames inspect:
- HyperFrames snapshot:
- Dialogue sync validator:
- Render verification:
- Report gate:

## Risks

| risk | mitigation | owner |
| --- | --- | --- |
| reference content misuse | reference-only boundary | F2 |
| missing audio clock | transcribe/TTS authorization or downgrade route | F2/user |
| render dependency failure | stop at project/report and preserve logs | F2 |

# F2 Scripts Boundary

F2 scripts are mechanical validators and audit helpers only. They do not create
creative truth, render video, transcribe audio, or decide subtitle semantics.

F2 intentionally relies on HyperFrames CLI and HyperFrames media tooling instead of copying F1 validators or creating a separate renderer. Future scripts in this directory may only perform mechanical support:

- schema validation for F2 JSON artifacts;
- final-ready dialogue sync evidence validation;
- file existence and path audits;
- diff/report assembly;
- non-creative manifest checks;
- smoke tests around HyperFrames project structure.

Scripts in this directory must not generate creative text, storyboard decisions, subtitle semantics, visual composition choices, title card copy, transition judgment, or BGM creative plans.

## Current Scripts

### `validate_dialogue_sync.py`

Validates that `dialogue_alignment.json` is final-ready for dialogue captions:

- rejects total-duration, proportional, equal-split, preview-only or draft timing;
- requires each `dialogue_caption` cue to declare timing, script anchor, caption type, sync method, audio anchor and tolerance evidence;
- compares cue timing against per-cue audio anchors;
- compares HyperFrames `index.html` caption `data-start` / `data-duration` values against `dialogue_alignment.json`;
- emits JSON and exits non-zero on blocking failures.

Typical final gate:

```bash
python3 .agents/skills/workflow/F2/scripts/validate_dialogue_sync.py --strict-final <project_root> --write-report <project_root>/dialogue_sync_validation.json
```

This validator cannot prove spoken phonemes by itself. It proves that the final
project has the required per-cue evidence and that the composition did not drift
from that evidence. ASR/SRT or manual listening still happens in `N4`.

Smoke fixture:

```bash
python3 .agents/skills/workflow/F2/scripts/validate_dialogue_sync.py --strict-final .agents/skills/workflow/F2/scripts/fixtures/dialogue-sync-pass
```

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| Did a new script become a renderer or creative author? | Any script generating creative/video decisions fails | `FAIL-F2-SCRIPT-OVERREACH` | `LLM-First Creative Authorship Contract` | script purpose and callsite |
| Did a script reintroduce F1 runtime dependency? | Imports/calls into F1 scripts or validators fail | `FAIL-F2-HYPERFRAMES-ONLY` | `Core Task Contract` | script audit |
| Did final dialogue sync bypass mechanical validation? | Missing or failing `dialogue_sync_validation.json` on final route fails | `FAIL-DIALOGUE-CLOCK` | `N4-DIALOGUE-CLOCK` | validator JSON |

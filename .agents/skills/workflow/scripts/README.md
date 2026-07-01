# Workflow Scripts Boundary

workflow scripts are mechanical validators and audit helpers only. They do not create
creative truth, render video, transcribe audio, or decide subtitle semantics.

workflow intentionally relies on HyperFrames CLI and HyperFrames media tooling instead of copying F1 validators or creating a separate renderer. Future scripts in this directory may only perform mechanical support:

- schema validation for workflow JSON artifacts;
- final-ready dialogue sync evidence validation;
- visual contract validation for audience-visible text, captions, overlays, PiP evidence, and batch ledgers;
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
python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --strict-final <project_root> --write-report <project_root>/dialogue_sync_validation.json
```

This validator cannot prove spoken phonemes by itself. It proves that the final
project has the required per-cue evidence and that the composition did not drift
from that evidence. ASR/SRT or manual listening still happens in `N4`.

Smoke fixture:

```bash
python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --strict-final .agents/skills/workflow/scripts/fixtures/dialogue-sync-pass
```

### `validate_visual_contract.py`

Validates that an authored workflow/HyperFrames project or batch satisfies the visual
composition gates exposed by recent failures:

- rejects audience-visible internal prompt metadata, workflow labels and watermark-like workflow/HyperFrames text;
- requires a real `dialogue_caption` layer;
- rejects caption ellipsis, newline wrapping, overwide caption text and overlapping dialogue cues;
- rejects editorial overlays that duplicate the current dialogue caption;
- requires `semantic_pip` slots to carry timing, `cue_id` and `match_reason`;
- checks `workflow_composition_plan.json` for `hook_opening`, `content_body` and `private_traffic_cta` segments;
- checks that strict social-ad plans declare a continuous no-mask `background_throughline`, per-segment background/PiP/caption/editorial overlay layers, and short editorial overlay summaries;
- checks content body coverage for comic-drama, tool/workflow and revenue/proof material, unless the plan records an explicit exception;
- in `--strict-social-ad` mode, requires enough cue-bound PiP slots and checks `workflow_assignment.json`;
- checks PiP `video_manifest_hint.segment_id` and `match_score` so a formal 0-score reference cannot pass as manifest consumption;
- checks batch `asset_diversity_audit.json` and `asset_usage_ledger.json` when they exist.

Typical final gate for a single project:

```bash
python3 .agents/skills/workflow/scripts/validate_visual_contract.py <project_root> --strict-social-ad --write-report <project_root>/visual_contract_validation.json
```

Typical final gate for a batch root:

```bash
python3 .agents/skills/workflow/scripts/validate_visual_contract.py <batch_root> --strict-social-ad --write-report <batch_root>/visual_contract_validation.json
```

This validator cannot judge aesthetics or invent better visual matches. It only
blocks missing evidence, unsafe text, caption/PiP contract drift and batch audit
inconsistency. Creative repair still returns to `N3/N5/N6/N7`.

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| Did a new script become a renderer or creative author? | Any script generating creative/video decisions fails | `FAIL-WORKFLOW-SCRIPT-OVERREACH` | `LLM-First Creative Authorship Contract` | script purpose and callsite |
| Did a script reintroduce F1 runtime dependency? | Imports/calls into F1 scripts or validators fail | `FAIL-WORKFLOW-HYPERFRAMES-ONLY` | `Core Task Contract` | script audit |
| Did final dialogue sync bypass mechanical validation? | Missing or failing `dialogue_sync_validation.json` on final route fails | `FAIL-DIALOGUE-CLOCK` | `N4-DIALOGUE-CLOCK` | validator JSON |
| Did final visual composition bypass mechanical validation? | Missing or failing `visual_contract_validation.json` on social-ad/batch/final visual routes fails | `FAIL-QUANT-VISUAL-CONTRACT` | `N5/N6/N7` | validator JSON |

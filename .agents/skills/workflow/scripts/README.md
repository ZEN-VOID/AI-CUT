# Workflow Scripts Boundary

workflow scripts are mechanical validators and audit helpers only. They do not create
creative truth, render video, transcribe audio, or decide subtitle semantics.

workflow intentionally relies on HyperFrames CLI and HyperFrames media tooling instead of copying F1 validators or creating a separate renderer. Future scripts in this directory may only perform mechanical support:

- schema validation for workflow JSON artifacts;
- final-ready dialogue sync evidence validation;
- visual contract validation for audience-visible text, captions, overlays, internal process title leakage, PiP evidence, and batch ledgers;
- project-wide material usage monitor CSV maintenance;
- file existence and path audits;
- diff/report assembly;
- non-creative manifest checks;
- smoke tests around HyperFrames project structure.

Scripts in this directory must not generate creative text, storyboard decisions, subtitle semantics, visual composition choices, title card copy, transition judgment, or BGM creative plans.

## Current Scripts

### `validate_dialogue_sync.py`

Validates that `dialogue_alignment.json` is final-ready for dialogue captions:

- rejects total-duration, proportional, equal-split, preview-only or draft timing;
- rejects missing or mismatched `source_script` / `source_audio` / shared stem when `--require-script-audio-pair` is used for current `projects/内容/文案` + `projects/内容/音频` routes;
- rejects `BGM.*` as the dialogue audio clock;
- requires each `dialogue_caption` cue to declare timing, script anchor, caption type, sync method, audio anchor and tolerance evidence;
- requires strict final dialogue cues to expose sortable script order evidence such as `script_order` or `script_span.start_char`;
- rejects cue/script/audio-anchor order regressions so shuffled subtitles cannot pass as final-ready captions;
- compares cue timing against per-cue audio anchors;
- compares HyperFrames `index.html` caption `data-cue-id` / `data-start` / `data-duration` / text values against `dialogue_alignment.json`;
- rejects missing `data-cue-id`, duplicate cue IDs, cue-id mismatches and non-monotonic HTML caption order in strict final mode;
- emits JSON and exits non-zero on blocking failures.

Typical final gate:

```bash
python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --strict-final <project_root> --write-report <project_root>/dialogue_sync_validation.json
```

Current material-pool route:

```bash
python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --strict-final --require-script-audio-pair <project_root> --write-report <project_root>/dialogue_sync_validation.json
```

This validator cannot prove spoken phonemes by itself. It proves that the final
project has the required per-cue evidence, that cue order follows the source
script/audio anchors, and that the composition did not drift from that evidence.
ASR/SRT or manual listening still happens in `N4`.

Smoke fixture:

```bash
python3 .agents/skills/workflow/scripts/validate_dialogue_sync.py --strict-final .agents/skills/workflow/scripts/fixtures/dialogue-sync-pass
```

### `validate_visual_contract.py`

Validates that an authored workflow/HyperFrames project or batch satisfies the visual
composition gates exposed by recent failures:

- rejects audience-visible internal prompt metadata, workflow labels, workflow/HyperFrames watermark text, and internal process/learning labels such as 工作流程 or 内部学习交流;
- requires a real `dialogue_caption` layer;
- rejects caption ellipsis, newline wrapping, overwide caption text and overlapping dialogue cues;
- rejects editorial overlays that duplicate the current dialogue caption or use internal process titles instead of matched-copy summary titles;
- requires `semantic_pip` slots to carry timing, `cue_id` and `match_reason`;
- requires strict social-ad PiP to include at least one simultaneous multi-window group, grid/group position evidence and readable rendered dimensions;
- checks `workflow_composition_plan.json` for `hook_opening`, `content_body` and `private_traffic_cta` segments;
- checks that strict social-ad plans declare a continuous no-mask, fully opaque `background_throughline`, per-segment background/PiP/caption/editorial overlay layers, and short editorial overlay summaries with matched `source_cue_ids`, `source_text`, and `match_reason`;
- checks that `hook_opening` selects real `projects/素材/开头素材/` or `opening_hook` evidence, uses a 5-10 second opening material span, and records full-frame/no-crop/no-upscale display evidence;
- checks that `private_traffic_cta` / `projects/素材/引流素材/` material declares no-upscale/native-scale/contain evidence and does not use cover, zoom or scale above 1;
- rejects background `mask`, `clip-path`, opacity below 1, transparency or inline background opacity styles on authored HTML elements;
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

### `update_asset_usage_monitor.py`

Maintains `projects/素材使用监控.csv` from final usage evidence. The CSV is intentionally
simple and must keep exactly four columns:

```csv
素材名,文件路径,使用次数,使用程度
```

`使用程度` must be `全片` or `部分切片`. Detailed segment IDs, time ranges,
layers and final paths stay in `asset_usage_ledger.json`.

Initialize or validate the monitor:

```bash
python3 .agents/skills/workflow/scripts/update_asset_usage_monitor.py
python3 .agents/skills/workflow/scripts/update_asset_usage_monitor.py --validate-only
```

Update after final verification from a batch/output root or ledger:

```bash
python3 .agents/skills/workflow/scripts/update_asset_usage_monitor.py <batch_root>
python3 .agents/skills/workflow/scripts/update_asset_usage_monitor.py <project_root>/asset_usage_ledger.json
```

Rebuild idempotently from all discovered output ledgers:

```bash
python3 .agents/skills/workflow/scripts/update_asset_usage_monitor.py --rebuild projects/output
```

This helper must not be run to count planned usage, failed renders, browser-only
previews or unverified drafts. Final close should count actual usage only after
the local canonical MP4 exists.

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| Did a new script become a renderer or creative author? | Any script generating creative/video decisions fails | `FAIL-WORKFLOW-SCRIPT-OVERREACH` | `LLM-First Creative Authorship Contract` | script purpose and callsite |
| Did a script reintroduce F1 runtime dependency? | Imports/calls into F1 scripts or validators fail | `FAIL-WORKFLOW-HYPERFRAMES-ONLY` | `Core Task Contract` | script audit |
| Did final dialogue sync bypass mechanical validation? | Missing or failing `dialogue_sync_validation.json` on final route fails | `FAIL-DIALOGUE-CLOCK` | `N4-DIALOGUE-CLOCK` | validator JSON |
| Did final visual composition bypass mechanical validation? | Missing or failing `visual_contract_validation.json` on social-ad/batch/final visual routes fails | `FAIL-QUANT-VISUAL-CONTRACT` | `N5/N6/N7` | validator JSON |

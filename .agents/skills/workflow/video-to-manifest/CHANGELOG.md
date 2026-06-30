# Changelog: video-to-manifest

## 2026-06-30

- Promoted the package to `.agents/skills/workflow/video-to-manifest` as a workflow satellite skill.
- Updated manifest templates, script defaults, README, prompts and consumer contract language so workflow is the active consumer; legacy F1 mentions remain only as historical changelog or compatibility field context.

## 2026-06-29

- Added long-material pre-slice evidence rules: videos over 60 seconds now produce `analysis_slices[]` evidence windows by default, without moving or overwriting original media.
- Added explicit physical proxy clip support for long-material slicing: when requested, `inspect_video_material.py --write-analysis-clips` writes short proxy videos under `analysis_clips/` and records `analysis_slices[].proxy_clip`.
- Added workflow batch-diversity schema guidance for `semantic_vector`, `trigger_profile`, `visual_signature`, `variation_profile`, `analysis_slice_id`, and `reuse_profile`.
- Updated `inspect_video_material.py` to emit analysis slices and deep-tag skeleton placeholders, and updated `validate_video_manifest.py` to warn on missing slice evidence, shallow tags, and missing diversity fields.
- Updated manifest/report templates, context heuristics, and regression prompts for platform deduplication support.

## 2026-06-26

- Moved the package out of the F1 subtree into `workflow/video-to-manifest` so workflow, and future workflow variants can share the same manifest-generation satellite.
- Updated the contract from F1-only to workflow consumer handoff: workflow may only ingest `视频说明.yaml` as optional evidence before rebuilding `asset_evidence.json`.
- Promoted 逐视频精读 from context heuristic to SKILL-level completion rule: each written video now needs per-video visual evidence and observation/deep-review trace; directory-level overviews cannot be the sole basis for semantic fields.

## 2026-06-22

- Created initial F1 satellite Skill 2.0 package for generating, updating, repairing, and validating `视频说明.yaml`.
- Standardized manifest schema from `projects/0622/素材/视频/视频说明.yaml`, including `consumer_contract`, `field_model`, `global_editing_policy`, `renames`, video-level fields, segment-level fields, evidence fields, and consumer handoff requirements.
- Added LLM-first video understanding contract: scripts may inspect media and validate YAML, but final visual semantics, tags, screen state, subtitle risk, and splice notes must come from LLM/operator observation.
- Added mechanical helpers for video evidence extraction and manifest validation.
- Added standard directory category mapping: `操作展示/` -> `operation_demo`, `工具使用/` -> `tool_display`, and `影像内容/` -> `aigc_content`.
- Updated schema guidance, template, validator, README, context, and prompts so operation demos carry `operation_state` evidence and directory-category conflicts are reported.
- Fixed `validate_video_manifest.py` indentation so the validation completion gate can run in update and validate-only routes.

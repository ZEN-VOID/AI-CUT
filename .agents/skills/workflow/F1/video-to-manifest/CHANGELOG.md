# Changelog: video-to-manifest

## 2026-06-22

- Created F1 satellite Skill 2.0 package for generating, updating, repairing, and validating `视频说明.yaml`.
- Standardized manifest schema from `projects/0622/素材/视频/视频说明.yaml`, including `consumer_contract`, `field_model`, `global_editing_policy`, `renames`, video-level fields, segment-level fields, evidence fields, and F1 handoff requirements.
- Added LLM-first video understanding contract: scripts may inspect media and validate YAML, but final visual semantics, tags, screen state, subtitle risk, and splice notes must come from LLM/operator observation.
- Added mechanical helpers for video evidence extraction and manifest validation.
- Added standard directory category mapping: `操作展示/` -> `operation_demo`, `工具使用/` -> `tool_display`, and `影像内容/` -> `aigc_content`.
- Updated schema guidance, template, validator, README, context, and prompts so operation demos carry `operation_state` evidence and directory-category conflicts are reported.
- Fixed `validate_video_manifest.py` indentation so the validation completion gate can run in update and validate-only routes.

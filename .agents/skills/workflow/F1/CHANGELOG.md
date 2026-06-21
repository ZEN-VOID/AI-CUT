# Changelog: F1

## 2026-06-20

- Created Skill 2.0 runtime-spine package for reference-rhythm voiceover auto editing.
- Captured the tested workflow from `projects/测试`: PRP-first execution, reference rhythm analysis, voiceover-primary rendering, hard subtitle burn-in, and silence-boundary subtitle repair.
- Added core layout, scripts, templates, metadata, and evaluation prompts.

## 2026-06-21

- Added `视频说明.yaml` handling rules so F1 can load structured video material descriptions from a source video directory during intake.
- Defined manifest discovery, minimum accepted fields, mismatch fallback, tool/content category selection guidance, subtitle-risk verification, and report evidence requirements.
- Updated F1 node map, convergence/review gates, output evidence, and evaluation prompts to cover manifest-assisted visual planning.
- Upgraded the manifest contract to v2 segment-level selection: F1 now expects `media`, `content_profile`, `selection_profile`, `splicing_profile`, `subtitle_safe_zone`, and `segments[]` fields when a manifest is used for EDL decisions.
- Required EDL/report evidence to record `video_id/file/segment_id/source_start/source_end/selection_reason/subtitle_risk`, preventing video-level summaries from being treated as sufficient for automatic splicing.
- Added a hard dialogue-alignment gate: SRT structure, final duration, pause-boundary timing, and frame readability no longer suffice unless every cue has cue-to-audio/script evidence in `dialogue_alignment*.json`.
- Added `scripts/validate_dialogue_alignment.py` and updated templates/prompts so subtitle text must match the spoken audio line by line before final completion.
- Added subtitle style customization as a first-class contract: font, size, colors, outline, shadow, placement, margins, line policy, and box style must be captured in `subtitle_style*.json`.
- Added `scripts/validate_subtitle_style.py` and updated templates/prompts so custom subtitle appearance is validated and reported before final completion.

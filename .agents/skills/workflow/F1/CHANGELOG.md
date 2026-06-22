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
- Added the Tri-Track Alignment contract covering subtitle-to-audio dialogue alignment, tool-screen-to-subtitle visual alignment, and title-card-to-subtitle cue alignment.
- Required tool-display segments to record cue indices, audio/script/visual spans, source segment, screen state, spoken topic, and match evidence instead of using generic tool B-roll.
- Added title-card planning rules for manual and auto-emphasis big-text cards, including card text, cue binding, subtitle display policy, overlay order, and frame verification.
- Added `scripts/validate_visual_alignment_plan.py` plus template and prompt coverage for tool-screen and title-card alignment plans.

## 2026-06-22

- Added `video-to-manifest/` as an F1 satellite Skill 2.0 package for generating, updating, repairing, and validating `视频说明.yaml`.
- Standardized the video manifest schema from `projects/0622/素材/视频/视频说明.yaml` and extended it with evidence and tool screen-state fields required by F1 visual planning.
- Updated F1 routing, module triggers, review gates, README, context, and evaluation prompts so manifest generation is handled by the satellite rather than the final-render main chain.
- Increased the default hard-subtitle size from 16 to 20 for 1280x720 output and tightened the default Chinese line length to reduce overflow risk.
- Standardized F1 video material categories for `projects/0622/素材/视频/操作展示`, `工具使用`, and `影像内容` as `operation_demo`, `tool_display`, and `aigc_content`.
- Added category-specific N5 visual planning rules: operation demos require operation/action-state evidence, tool displays require screen-state evidence, and AIGC content requires semantic/rhythm evidence.
- Synced prompts, README, context, and output evidence requirements so EDL/report entries include `category` and directory-category verification.
- Added the Material Composition contract so the three material categories are composed by voiceover time and subtitle cue into one primary visual timeline rather than by directory order, fixed ratio, or parallel primary layers.
- Updated visual-plan validation, templates, README, context, and evaluation prompts to require `material_composition[]` evidence and render-order verification.
- Added the Title Card Processing Detail contract so 大字报 now has governed trigger policy, card type, text source, duration policy, safe zone, subtitle display policy, layer order, and verification requirements.
- Updated visual-plan validation, templates, README, context, and evaluation prompts to require title-card processing evidence and block over-dense, subtitle-covering, or script-external big-text cards.

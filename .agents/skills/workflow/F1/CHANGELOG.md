# Changelog: F1

## 2026-06-26

- Moved `video-to-manifest/` out of the F1 subtree into `workflow/_shared/video-to-manifest/` and updated F1 routing to consume it as a shared manifest side input.

## 2026-06-25

- Strengthened video-stitching transition richness: transition plans now require `effect_palette`, `richness_policy`, per-transition `effect_family/style_preset/parameters/intensity/variation_reason`, expanded effect types, stitching-boundary preset mapping, and validator/test coverage for effect-family diversity.
- Added render-parity validation for title-card and picture-in-picture overlays: `validate_visual_alignment_plan.py` can now require `render_evidence` markers and verify them against `render_command.txt`, blocking plan/render drift where overlay rules pass on paper but are not executed in the final render.
- Added fixed typography render-parity gates for the current F1 720p contract: subtitle validation can require `Fontsize=30` in `render_command.txt`, title-card validation can require drawtext `fontsize=90`, and regression tests cover metadata false positives.
- Added grouped PiP alignment gates: visual-plan validation can now require an exact default group size, aligned `layout_group` slots, and current-cue text evidence, covering the “three tidy cue-related PiP windows per trigger” repair pattern.
- Added PiP minimum-duration governance: video PiP overlays must remain visible for at least 4s, image/static PiP overlays for at least 3s, with `pip_media_type`, plan-level duration policy, validator flags, templates, README, CONTEXT, and regression tests synchronized.

## 2026-06-24

- Tightened 大字报 / title-card layout rules so `emphasis_overlay` and current-frame `section_card` default to the `hero_emphasis_band` upper-middle visual emphasis area instead of a narrow top banner.
- Added structured title-card layout requirements: `layout_zone`, normalized geometry, subtitle clearance, collision avoidance, and fallback reason when leaving the hero band.
- Added hero title-card style gates for 720p: `font_size_min>=90`, governed entrance-effect choices, and rejection of unreasoned `top_banner` / `top_center`, small-font, or generic `fade_in` emphasis overlays.
- Promoted hero title-card source default to 720p `font_size_min>=90` / default 90 and synchronized validator, CONTEXT, and evaluation prompts with the newer 大字报 sizing rule.
- Promoted the current F1 style source default to subtitle 30 / title-card 90 and confirmed project-side style evidence must not retain older override notes after that default is in force.
- Updated visual-plan validation, tests, README, templates, CONTEXT, and evaluation prompts to cover the red-box-to-blue-box title-card repair pattern.
- Added a governed entrance-effect selection mechanism for 大字报: cue-role / semantic-energy / visual-motion / background-complexity based selection, candidate/rejection evidence, and local diversity checks blocking adjacent unreasoned repetition.
- Locked F1 subtitle font sizing at the whole-video style layer: `subtitle_style*.json` now requires `font_size_lock=true`, whole-video `font_size_scope`, `auto_shrink=false`, no per-cue font-size overrides, and long lines must split into single-line cues instead of wrapping or shrinking.
- Added governed picture-in-picture processing: trigger policy, PiP presentation types, overlay source and base-layer evidence, safe-zone/layer-order requirements, validation support, templates, README, CONTEXT, and evaluation prompt coverage.
- Tightened picture-in-picture processing so every PiP must document best-placement decision, presentation/style, motion/entrance effect, and fit reasons rather than only source and geometry.
- Strengthened picture-in-picture density and placement governance: added `pip_density_policy`, higher-density trigger rules, increased target counts, controlled-random `position_strategy`, position-diversity checks, template/report fields, README notes, and regression prompts/tests.
- Added governed BGM handling: auto-discovery from `素材/音频/BGM.*`, source probing, excerpt selection, visual-rhythm matching, voiceover-priority ducking, `bgm_mix_plan*.json`, validation support, templates, README, CONTEXT, and evaluation prompt coverage.
- Added governed visual-transition strengthening: `transition_density_policy`, `visual_transitions[]`, high-frequency reference-style trigger rules, transition type/diversity/rhythm/safe-zone validation, templates, README, CONTEXT, and regression prompt/test coverage.
- Analyzed the provided 42.6s reference video for F1 transition rules: 28 detected scene-change points, average cut interval about 1.57s, multiple high-score cut clusters, and almost no long silence, so transition triggering now prioritizes visual boundaries, semantic phase changes, material-category switches, BGM/voiceover beats, and result/tool switches over silence boundaries.

## 2026-06-23

- Added F1 project initialization routing and directory contract: default `projects/<MMDD>/` naming, `-2` / `-3` collision suffixes, and the 10-directory skeleton including `素材/图片/` plus `素材/视频/操作展示/`, `素材/视频/工具使用/`, and `素材/视频/影像内容/` with no placeholder files.
- Added the split material manifest rule: video indexes stay in `素材/视频/视频说明.yaml`, image indexes stay in `素材/图片/图片说明.yaml`, and image materials enter F1 visual planning only as audited `image_asset` composition entries.
- Added the Image Description Manifest contract with required `images[]` fields, image selection rules, read-only source boundaries, derived-image output rules, subtitle-safe-zone checks, and report evidence.
- Promoted strict subtitle/audio synchronization to a hard F1 completion gate: final delivery now requires ASR word/char timing or per-cue manual listening verification.
- Added `--strict` mode to `validate_dialogue_alignment.py`, blocking pure `silencedetect` / speech-interval / fallback timing from passing final dialogue alignment.
- Added a strict ASR/script content match-ratio gate to `validate_dialogue_alignment.py`; ASR span evidence alone no longer passes final delivery when transcript/script content matching is missing or below the default threshold.
- Added `validate_srt.py --strict-boundaries` to catch split model names, split words, and sentence-tail glue across adjacent cues.
- Updated F1 contracts, context, and evaluation prompts so fallback subtitle timing can only produce draft or needs-review artifacts unless upgraded by strict evidence.
- Tightened F1 subtitle output rules so every final SRT cue must remain a single text line with no explicit line-break markers.
- Updated subtitle style defaults and validation to require `max_lines=1` plus a `single-line` / `no-explicit-breaks` line policy.
- Updated SRT validation, fallback SRT projection, templates, README, and evaluation prompts to block multi-line or jumping subtitles.
- Clarified long subtitle handling: content that exceeds the single-line target must be split into multiple cues by ASR word spans or speech-interval timing while preserving dialogue alignment evidence.
- Extended `project_silence_srt.py` so LLM/operator-approved subchunks can map multiple single-line cues to the same speech interval via `interval_index`.
- Reframed 大字报 as current-frame special-effect text overlays rather than standalone posters or subtitle-size changes, and required text determination, presentation timing, and structured effect-style evidence in F1 title-card plans and validation.
- Required 大字报 `effect_style` to include an explicit suitable entrance effect and fit rationale, with validation blocking generic animation-only plans.

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

- Added the initial `video-to-manifest/` satellite Skill 2.0 package for generating, updating, repairing, and validating `视频说明.yaml`.
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

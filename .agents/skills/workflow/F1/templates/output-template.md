# F1 Output Template

## Output Contract Alignment

This template aligns with `SKILL.md` Output Contract and does not define a second output path, naming rule, or completion gate.

| Output Contract field | Template field |
| --- | --- |
| Required output | Canonical Final Output |
| Output format | Media Format |
| Output path | Canonical Final Output |
| Naming convention | Naming |
| Completion gate | Completion Gate |

## Required output

One canonical final MP4.

## Output format

H.264/AAC MP4 unless the user explicitly requests another format.

## Output path

- Final MP4:

## Naming convention

- Default: `<project-or-script-name>_final.mp4`
- Backup: `<project-or-script-name>_final_v1_<reason>.mp4`

## Supporting Artifacts

- PRP:
- Work directory:
- Master SRT:
- Dialogue alignment JSON with ASR word/char spans plus ASR/script match ratio, or per-cue manual listening verification:
- Material composition plan JSON:
- Visual alignment plan JSON with tool-screen, picture-in-picture, visual-transition, and title-card entries when triggered:
- Picture-in-picture plan JSON or `visual_alignment_plan*.json.picture_in_picture[]` with `pip_density_policy`, video/image minimum-duration policy, trigger source, PiP type, role, media type, cue text/script/audio/visual spans, base layer, overlay source, content evidence, controlled-random `position_strategy` for single windows or aligned `layout_group` slots for multi-window groups, layout, safe zone, layer order, selection reason, and verdict:
- Visual transition plan JSON or `visual_alignment_plan*.json.visual_transitions[]` with `transition_density_policy`, `effect_palette`, `richness_policy`, trigger source, transition type, effect family, style preset, parameters, intensity, role, cue/script/audio/visual spans, duration, from/to material composition IDs, rhythm sync, effect style/profile, safe zone, layer order, selection reason, type/effect-family diversity evidence, and verdict:
- Title-card plan JSON with cue, text determination, source text, supporting sources, presentation timing, structured layout, hero emphasis band / fallback reason, font size policy, effect style, entrance effect, entrance effect selection, safe zone, subtitle policy, and layer order:
- BGM mix plan JSON or `audio_mix_plan*.json.background_music` with source, selected excerpts, target spans, rhythm match, visual sync points, fade/loop policy, ducking, volume, and verdict when BGM is enabled:
- Subtitle style JSON:
- EDL/render plan:
- ffprobe JSON:
- Verification frames:
- Execution report:

## Completion gate

- Final MP4 exists.
- Full decode passes.
- ffprobe confirms video and audio tracks.
- SRT structure is valid.
- Every SRT cue has exactly one subtitle text line and no explicit line-break marker.
- Long spoken content is split into multiple single-line cues by speech timing, not by visual line breaks.
- Subtitle font size is locked for the whole video; style JSON declares `font_size_lock=true`, whole-video `font_size_scope`, `auto_shrink=false`, and no per-cue font-size overrides.
- SRT strict-boundaries validation blocks split model names, split words, and sentence-tail glue across adjacent cues.
- `validate_dialogue_alignment.py --strict` confirms subtitle text maps to the spoken audio/script span for every cue, including cues split from one long spoken interval, and enforces the default ASR/script content match-ratio gate unless manual listening verification is present.
- Pure `silencedetect`, speech-interval, SRT-structure, duration, or frame-readability evidence is not accepted as final strict sync evidence.
- Material composition confirms `operation_demo`, `tool_display`, and `aigc_content` are ordered by cue/audio span as one primary visual timeline.
- Visual alignment confirms tool-screen subtitle spans map to matching screen states when tool segments are present.
- Picture-in-picture processing confirms every enabled PiP maps to `pip_density_policy`, `min_video_duration_sec>=4`, `min_image_duration_sec>=3`, trigger source, PiP type, role, media type, subtitle cue indices, current `cue_text`, voiceover/script/visual spans, base layer, overlay source, content evidence, controlled-random `position_strategy` for single windows or aligned `layout_group` slots for multi-window groups, structured layout, safe zone, and `before_hard_subtitles` or equivalent below-subtitle layer order. Video PiP overlays must stay visible for at least 4 seconds, image/static PiP overlays for at least 3 seconds, must not cover hard subtitles, key UI, faces, or primary action, must not repeat one fixed position without a reason, and simultaneous multi-window groups default to three tidy cue-related frames unless a reason is recorded. Reference clips may provide style/density only unless explicitly authorized as source material.
- Visual transition processing confirms every enabled transition maps to `transition_density_policy`, `effect_palette`, `richness_policy`, trigger source, transition type, effect family, style preset, reproducible parameters, intensity, role, subtitle cue indices, voiceover/script/visual spans, from/to material composition IDs, rhythm sync, effect style/profile, safe zone, and `within_main_visual` / `before_overlays` / `before_hard_subtitles` layer order. Transitions must not cover hard subtitles, must not repeat one type or one effect family without a reason, and must not use generic `soft_crossfade` except as documented fallback smoothing.
- Title-card processing confirms every enabled big-text overlay maps to subtitle cue indices, voiceover/script spans, text determination, source text and supporting sources, presentation timing, structured layout, effect style including size/effect policy, a suitable entrance effect with fit rationale and selection basis, safe zone, subtitle display policy, and `before_hard_subtitles` layer order. `emphasis_overlay` / current-frame `section_card` must pass `hero_emphasis_band` layout checks, 720p `font_size_min>=90`, subtitle clearance, governed entrance-effect validation, and local diversity checks, or carry an explicit fallback/repetition reason.
- BGM processing, when enabled, confirms the source file has usable audio, selected excerpts match visual rhythm and cue structure, segment sync deltas are acceptable, fades/loops are governed, ducking keeps voiceover primary, and `validate_bgm_mix_plan.py --require-bgm` passes.
- Subtitle style JSON exists and validates requested font, locked size, color, outline, shadow, position, margins, `max_lines=1`, no-explicit-break line policy, and fallback evidence.
- Frame checks confirm subtitle readability and cover any tool-screen, picture-in-picture, visual-transition, or title-card spans.
- Fallbacks and residual risks are reported.

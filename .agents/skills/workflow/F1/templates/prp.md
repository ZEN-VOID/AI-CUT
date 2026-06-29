# F1 PRP: <project-or-topic>

## Goal

Create a reference-rhythm voiceover final cut from user video, script text, voiceover audio, optional background music, and reference clips.

## Inputs

- Reference directory:
- Source video:
- Script text:
- Voiceover audio:
- Background music:
- Result directory:

## Outputs

- Final MP4:
- Work directory:
- Master SRT:
- Strict dialogue alignment plan:
- Material composition plan:
- Visual alignment plan:
- Picture-in-picture plan with density policy, trigger count, video/image minimum-duration policy, media type, controlled-random position strategy for single windows or aligned `layout_group` slots for multi-window groups, default group size, cue-text evidence, trigger source, PiP type, role, overlay source, base layer, layout, safe zone, and layer order:
- Visual transition plan with density policy, trigger count, transition type diversity, effect palette, effect-family/preset/parameter diversity, trigger source, role, from/to material composition IDs, rhythm sync, duration, safe zone, and layer order:
- Title-card plan with text determination, presentation timing, structured layout, hero emphasis band / fallback reason, font size policy, effect style, entrance effect, entrance effect selection, safe zone, and layer order:
- BGM mix plan with source probe, selected excerpts, target spans, rhythm match, visual sync points, fade/loop policy, ducking, voiceover-priority volume, and verdict when BGM is enabled:
- Subtitle style with locked whole-video font size:
- EDL/render plan:
- Execution report:

## Routing

- Main workflow: `$F1`
- Downstream skills:
  - `video-use`
  - `timestamp-extraction`
  - `video-editing`
  - `wjs-transcribing-audio`
  - `wjs-burning-subtitles`

## Stages

1. Intake and environment check.
2. Reference rhythm analysis.
3. Subtitle and voiceover alignment.
4. Material composition planning for operation/tool/content video.
5. Tool-screen, picture-in-picture density/position, visual-transition density/type/effect-palette/rhythm, big-text effect overlay, and BGM rhythm/mix planning.
6. Visual mapping and missing-material fill.
7. Final render with voiceover-primary BGM ducking when enabled.
8. Verification and report.

## Fallbacks

- ASR unavailable:
- Manual listening verification required:
- libass unavailable:
- Reference rhythm cannot be machine-detected:
- Source video too short or mismatched:
- Material category has no matching segment:
- Tool-screen state unavailable:
- Picture-in-picture source, base layer, density target, media type, minimum-duration policy, controlled-random position strategy, layout, safe zone, or layer order unavailable:
- Visual transition boundary, density target, effect palette, type/effect-family diversity, rhythm sync, safe zone, or layer order unavailable:
- Title-card text determination, presentation timing, hero emphasis layout, font size, entrance effect selection, effect style, layout fallback, repetition reason, or subtitle relationship uncertain:
- BGM unavailable, has no usable audio, is too vocal, cannot match visual rhythm, or conflicts with voiceover:

## Acceptance

- Final MP4 exists and decodes.
- Voiceover is the main audio.
- Hard subtitles match the script and pass strict subtitle/audio sync validation.
- Subtitle style locks one whole-video font size, disables auto-shrink and per-cue font-size overrides, and keeps every cue single-line.
- Operation-demo, tool-display, and AIGC-content segments are composed by cue/audio span as one primary visual timeline.
- Tool-screen segments, when present, map each relevant subtitle cue to a matching screen state.
- Picture-in-picture overlays, when enabled, bind `pip_density_policy`, `min_video_duration_sec>=4`, `min_image_duration_sec>=3`, trigger count, controlled-random `position_strategy` for single windows or aligned `layout_group` slots for simultaneous groups, trigger source, PiP type, role, media type, overlay source, base layer, current `cue_text`, content evidence, subtitle cue indices, voiceover/script/visual spans, layout, safe zone, and `before_hard_subtitles` or equivalent below-subtitle layer order; video PiP stays at least 4 seconds, image/static PiP at least 3 seconds, they do not cover hard subtitles, key UI, faces, or primary action, they do not repeat one fixed position without a reason, and multi-window groups default to three tidy cue-related frames unless a reason is recorded.
- Visual transitions, when enabled, bind `transition_density_policy`, trigger count, `effect_palette`, `richness_policy`, transition type and effect-family diversity, trigger source, role, from/to material composition IDs, subtitle cue indices, voiceover/script/visual spans, rhythm sync, duration, structured `effect_profile` / `effect_style`, safe zone, and `within_main_visual` / `before_overlays` / `before_hard_subtitles` layer order; they do not cover hard subtitles, do not repeat one type or one effect family without a reason, and do not default to generic crossfade.
- Big-text overlays, when enabled, bind text determination, card text, source/supporting evidence, presentation timing, structured layout, hero emphasis band or fallback reason, font size policy, effect style, entrance effect with fit rationale and selection basis, subtitle cue indices, voiceover/script spans, safe zone, subtitle policy, and `before_hard_subtitles` layer order. Adjacent hero overlays should vary primary entrance effects unless a repetition reason is recorded.
- BGM, when enabled, is selected from a usable source such as `素材/音频/BGM.mp4`, trimmed or looped with justification, matched to visual rhythm and cue structure, faded cleanly, ducked below the voiceover, and validated by `validate_bgm_mix_plan.py --require-bgm`.
- Final duration is close to voiceover duration.
- Report records validation and fallbacks.

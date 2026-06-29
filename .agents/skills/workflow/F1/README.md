# F1

`F1` 是参考节奏驱动的自动剪辑 workflow skill。它把参考样片、用户视频、用户文案、已有旁白音频和可选 BGM 收束为一个硬字幕 final MP4，并保留 PRP、SRT、EDL、抽帧和执行报告。

## Directory Tree

```text
F1/
├── SKILL.md
├── CONTEXT.md
├── test-prompts.json
├── agents/
│   └── openai.yaml
├── CHANGELOG.md
├── README.md
├── scripts/
│   ├── check_environment.py
│   ├── project_silence_srt.py
│   ├── validate_dialogue_alignment.py
│   ├── validate_bgm_mix_plan.py
│   ├── validate_visual_alignment_plan.py
│   ├── validate_srt.py
│   └── validate_subtitle_style.py
└── templates/
    ├── execution-report.md
    └── prp.md
```

The shared material-manifest satellite now lives at `../_shared/video-to-manifest/` so F1, F2, and future workflow variants can reuse the same `视频说明.yaml` generation contract.

## Quick Use

Use `$F1` for project initialization when the user asks to initialize or create an F1 project. Initialization defaults to `projects/<MMDD>/`, appends `-2`, `-3` on name collisions, and creates only:

```text
示例/
素材/
素材/音频/
素材/图片/
素材/文案/
素材/视频/
素材/视频/操作展示/
素材/视频/工具使用/
素材/视频/影像内容/
结果/
```

No placeholder files, PRPs, reports, manifests, or execution work directories are created during initialization.

Use `$F1` when the user provides:

- reference clips;
- a source video;
- script text for subtitles;
- a voiceover audio file;
- optional background music, usually `素材/音频/BGM.mp4`;
- an output directory.

The runtime spine is in `SKILL.md`. `scripts/` only performs mechanical checks, time projection, and plan validation; semantic subtitle chunking, tool-screen matching decisions, and big-text effect overlay decisions remain LLM/operator responsibilities.

Subtitle font, locked whole-video size, color, outline, shadow, placement, margins, single-line length, no-explicit-break policy, and translucent box style can be customized. F1 subtitles are single-line by default and must not insert explicit line breaks; long spoken content should be split into multiple single-line cues by ASR word/char spans, or by speech-interval timing only after per-cue manual listening verification. Splits must preserve token and phrase boundaries; final SRT checks should include `validate_srt.py --strict-boundaries`. The default 720p subtitle size is 30 and must be declared as `font_size_lock=true`, `font_size_scope=global`, and `auto_shrink=false`; a user-specified size becomes the locked whole-video size. Final renders must project these choices from `subtitle_style*.json`, not from an untracked one-off render command or per-cue font-size overrides.

F1 now tracks five alignment chains: subtitle-to-voiceover strict dialogue alignment, tool-screen-to-subtitle visual alignment, picture-in-picture overlay alignment, visual-transition alignment, and title-card-to-subtitle cue alignment. Final delivery must pass `validate_dialogue_alignment.py --strict`, including the default ASR/script content match-ratio gate unless every affected cue has manual listening verification. Pure `silencedetect`, speech-interval, SRT-structure, duration, or frame-readability evidence can only produce draft/needs-review output. Tool-screen, picture-in-picture, visual-transition, and title-card plans should be recorded in `visual_alignment_plan*.json` and/or `title_card_plan*.json` before final render.

Background music is optional but governed. When the project root contains `素材/音频/BGM.*` / `bgm.*`, or the user provides a BGM path such as `projects/0624/素材/音频/BGM.mp4`, F1 treats it as a background-music candidate and uses only its audio stream. BGM must be selected, trimmed, looped only when justified, faded, ducked below the voiceover, and matched to the visual rhythm before final render. The evidence lives in `bgm_mix_plan*.json` or `audio_mix_plan*.json.background_music`, and enabled BGM must pass `validate_bgm_mix_plan.py --require-bgm`. Missing BGM does not block final delivery, but present/enabled BGM must not be laid as an untrimmed full-track bed or overpower the voiceover.

Picture-in-picture / 画中画 is a governed overlay layer for result previews, local zooms, before/after comparisons, proof shots, or retained tool-interface context. It is not a second primary visual track and should not reuse reference-video content unless the user explicitly authorizes that material. When triggered by the user, reference style, visual proof needs, comparison needs, fallback context, or an explicit request to increase PiP density/quantity/random placement, F1 must write `visual_alignment_plan*.json.pip_density_policy` plus `picture_in_picture[]` with trigger count, density basis, minimum-duration policy, controlled-random `position_strategy` for single windows, aligned `layout_group` slots for simultaneous multi-window groups, trigger source, PiP type, role, media type, cue text/script/audio/visual spans, base layer, overlay source, content evidence, layout, safe zone, layer order, selection reason, and verdict. Video PiP must stay visible for at least 4 seconds; image/static PiP must stay visible for at least 3 seconds. Simultaneous multi-window triggers default to three cue-related frames in an aligned row unless素材 or safety evidence justifies another count. Common types include `hero_pip_preview`, `corner_pip`, `tool_detail_zoom`, `before_after_comparison`, `result_preview`, `reference_style_echo`, and `process_context`; the layer should render before hard subtitles, avoid final subtitles, key UI, faces, and primary action, avoid repeating one fixed position without a reason, and avoid scattered multi-window placement.

Visual transitions / 转场 are governed as a main-visual rhythm layer, not as decorative filters. When the user asks for stronger transitions, or reference clips show high-frequency cuts, flash/black resets, whip/zoom movement, tool-to-result switches, action continuity, semantic phase changes, material-category switches, or BGM/voiceover strong beats, F1 must write `visual_alignment_plan*.json.transition_density_policy` plus `visual_transitions[]`. Each transition records trigger source, transition type, role, cue/script/audio/visual spans, duration, from/to material composition IDs, rhythm sync, structured effect profile, safe zone, layer order, selection reason, and verdict. The density policy must include `effect_palette` and `richness_policy`, while every effect profile must include `effect_family`, `style_preset`, reproducible parameters, intensity, and variation evidence. Strong reference rhythm should increase density and effect variety, but transitions must not cover hard subtitles, repeat one type or effect family without a reason, or default to generic `soft_crossfade` except as documented fallback smoothing.

Title cards / 大字报 are governed as special-effect text overlays on the current frame, not as subtitle-size changes or default standalone posters. Enabled big-text overlays must record text determination, source text and supporting sources, cue binding, presentation timing, structured layout, effect style including size/effect policy, a suitable entrance effect with fit rationale and selection basis, safe zone, subtitle display policy, and `layer_order=before_hard_subtitles`. For `emphasis_overlay` / current-frame `section_card`, the default layout is the `hero_emphasis_band`: a wide upper-middle visual emphasis area, not a narrow top banner. In 720p output, hero big text must declare `font_size_min>=90`, a subtitle clearance of at least 120px, and a governed entrance effect such as `kinetic_pop`, `zoom_blur_in`, `light_sweep_reveal`, `wipe_stretch_in`, `slam_bounce`, or `glitch_snap`. Hero overlays must also include `effect_style.entrance_effect_selection`, chosen by cue role, semantic energy, visual motion, background complexity, candidates, and local diversity; adjacent hero overlays cannot repeat the same primary entrance effect without a repetition reason. Validation must confirm they do not add unsupported claims or cover final subtitles, key UI, faces, or primary action.

Video material directories are standardized before visual planning:

- `操作展示/` -> `operation_demo`, matched by operation/action state and process continuity.
- `工具使用/` -> `tool_display`, matched by screen state and visible UI evidence.
- `影像内容/` -> `aigc_content`, matched by visual semantics, rhythm, and subtitle-safe-zone risk.

F1 composes those categories by cue/audio span into one primary visual timeline. It does not concatenate directories in order and does not render the three categories as parallel primary layers. The composition evidence should live in `material_composition_plan*.json` or `visual_alignment_plan*.json.material_composition[]`.

Image materials use a separate manifest from video materials. Keep video indexes at `素材/视频/视频说明.yaml` and image indexes at `素材/图片/图片说明.yaml`. When F1 uses images, they enter `material_composition[]` as `primary_category=image_asset` with `image_id`, file, role, cue/audio span, presentation policy, selection reason, and subtitle risk. F1 must not select images by filename or directory order alone, and derived crops/backgrounds/previews must be written under the edit work directory rather than overwriting `素材/图片/` originals.

Use `$video-to-manifest` when the user needs to generate, update, repair, or validate a `视频说明.yaml` for F1. The shared satellite produces the manifest side input; F1 still owns final EDL, rendering, and verification.

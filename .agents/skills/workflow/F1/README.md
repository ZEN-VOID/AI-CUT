# F1

`F1` 是参考节奏驱动的自动剪辑 workflow skill。它把参考样片、用户视频、用户文案和已有旁白音频收束为一个硬字幕 final MP4，并保留 PRP、SRT、EDL、抽帧和执行报告。

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
│   ├── validate_visual_alignment_plan.py
│   ├── validate_srt.py
│   └── validate_subtitle_style.py
├── video-to-manifest/
│   ├── SKILL.md
│   ├── scripts/
│   └── templates/
└── templates/
    ├── execution-report.md
    └── prp.md
```

## Quick Use

Use `$F1` when the user provides:

- reference clips;
- a source video;
- script text for subtitles;
- a voiceover audio file;
- an output directory.

The runtime spine is in `SKILL.md`. `scripts/` only performs mechanical checks, time projection, and plan validation; semantic subtitle chunking, tool-screen matching decisions, and title-card emphasis selection remain LLM/operator responsibilities.

Subtitle font, size, color, outline, shadow, placement, margins, line length, line count, and translucent box style can be customized. The default 720p subtitle size is 20 with shorter Chinese lines for readability. Final renders must project these choices from `subtitle_style*.json`, not from an untracked one-off render command.

F1 now tracks three alignment chains: subtitle-to-voiceover dialogue alignment, tool-screen-to-subtitle visual alignment, and title-card-to-subtitle cue alignment. Tool-screen and title-card plans should be recorded in `visual_alignment_plan*.json` and/or `title_card_plan*.json` before final render.

Title cards / 大字报 are governed as an emphasis layer, not as a subtitle-size change. Enabled title cards must record cue binding, source text, card type, text policy, duration policy, safe zone, subtitle display policy, and `layer_order=before_hard_subtitles`; validation must confirm they do not add script-external claims or cover final subtitles, key UI, faces, or primary action.

Video material directories are standardized before visual planning:

- `操作展示/` -> `operation_demo`, matched by operation/action state and process continuity.
- `工具使用/` -> `tool_display`, matched by screen state and visible UI evidence.
- `影像内容/` -> `aigc_content`, matched by visual semantics, rhythm, and subtitle-safe-zone risk.

F1 composes those categories by cue/audio span into one primary visual timeline. It does not concatenate directories in order and does not render the three categories as parallel primary layers. The composition evidence should live in `material_composition_plan*.json` or `visual_alignment_plan*.json.material_composition[]`.

Use `$video-to-manifest` when the user needs to generate, update, repair, or validate a `视频说明.yaml` for F1. That satellite produces the manifest side input; F1 still owns final EDL, rendering, and verification.

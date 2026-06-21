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
│   └── validate_srt.py
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

The runtime spine is in `SKILL.md`. `scripts/` only performs mechanical checks and time projection; semantic subtitle chunking remains an LLM responsibility.

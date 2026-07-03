# Text To Speech

`$text-to-speech` keeps Chinese copy files and MiniMax MP3 audio files in sync.

It scans `projects/内容/文案`, checks whether each `文案<N>.txt` has a same-stem MP3 in `projects/内容/音频`, and generates missing audio with the repo-local MiniMax CLI.

## Directory Tree

```text
text-to-speech/
├── SKILL.md
├── CONTEXT/
│   ├── 好的示例.md
│   ├── 坏的示例.md
│   ├── 正向经验.md
│   ├── 负向经验.md
│   └── 重要记忆.md
├── test-prompts.json
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── README.md
│   └── generate_missing_audio.py
├── review/
│   └── review-contract.md
├── types/
│   ├── type-map.md
│   └── default/default.md
├── templates/
│   └── output-template.md
├── references/
│   └── skill-2.0-package-contract.md
├── CHANGELOG.md
└── README.md
```

## Common Commands

Dry-run the full default scan:

```bash
python3 .agents/skills/workflow/text-to-speech/scripts/generate_missing_audio.py --dry-run
```

Generate a numbered range:

```bash
python3 .agents/skills/workflow/text-to-speech/scripts/generate_missing_audio.py --start 81 --end 140
```

Generate specific files:

```bash
python3 .agents/skills/workflow/text-to-speech/scripts/generate_missing_audio.py \
  --files projects/内容/文案/文案141.txt projects/内容/文案/文案142.txt
```

## Defaults

- Text directory: `projects/内容/文案`
- Audio directory: `projects/内容/音频`
- MiniMax CLI: `.agents/skills/cli/mmx-cli/node_modules/.bin/mmx`
- Speed: `1.26`
- Model: `speech-2.8-hd`
- Region: `global`
- Auth: MiniMax CLI config, environment, or repo-root `.env`
- Voices:
  - 贝因男声2 → `moss_audio_ba1bbbae-6f8d-11f1-ba6a-025474e1e406`
  - 贝因女声2 → `moss_audio_9e8695bb-6f8d-11f1-938c-a6f6fa6b2a0c`
  - 贝因女声1 → `moss_audio_644a5ef6-6f8d-11f1-83ef-8afcbb8b5b5c`

The first standalone `【标题】` line is ignored only in temporary TTS input. Source copy files are not modified.

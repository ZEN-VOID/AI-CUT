# Text To Speech Report

## Output Contract Alignment

- Required output: 缺失音频审计结果，或生成后的同名 `.mp3` 文件和 manifest。
- Output format: 音频写入 `projects/内容/音频/<文案文件stem>.mp3`；manifest 写入 `projects/内容/音频/text-to-speech_manifest_<timestamp>.json`。
- Output path: 默认音频目录为 `projects/内容/音频`。
- Naming convention: 文案 stem 与音频 stem 必须完全一致，例如 `文案81.txt` 对应 `文案81.mp3`。
- Completion gate: dry-run 或生成脚本 exit 0；若生成，所有计划项都有非空 `.mp3` 且 manifest 计数一致。

## Report Fields

- Text scope:
- Audio directory:
- Total text files:
- Existing audio skipped:
- Missing audio planned:
- Generated:
- Failed:
- Speed:
- Model:
- Region:
- Voice distribution:
- Manifest:
- Validation evidence:
- Residual risk:

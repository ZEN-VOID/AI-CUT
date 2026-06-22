# F1 Full Auto Edit PRP - 文案8

## Inputs
- reference_dir: projects/0622/示例
- material_dir: projects/0622/素材/视频
- video_manifest: projects/0622/素材/视频/视频说明.yaml
- script: projects/0622/素材/文案/文案8.md
- voiceover: projects/0622/素材/音频/文案8-音频.mp3
- result_dir: projects/0622/结果/文案8

## Route
full_auto_edit -> N1/N2/N3/N4/N5/N6/N7/N8.

## Fallback
Local ASR package unavailable and OPENAI_API_KEY unset, so N4 uses silencedetect speech intervals plus LLM semantic chunking. This is auditable but lower confidence than word-level ASR.

## Gates
Final MP4, master.srt, dialogue_alignment, subtitle_style, material_composition/visual_alignment, edl/render plan, ffprobe, decode check, extraction frames, execution report.

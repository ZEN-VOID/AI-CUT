# F1 PRP: 文案10

## Goal

按 F1 full_auto_edit 将文案10、旁白音频、三类素材和参考节奏收束为 canonical final MP4。

## Inputs

- Reference directory: projects/0622/示例
- Source video/material directory: projects/0622/素材/视频
- Video manifest: projects/0622/素材/视频/视频说明.yaml
- Script text: projects/0622/素材/文案/文案10.md
- Voiceover audio: projects/0622/素材/音频/文案10-音频.mp3
- Result directory: projects/0622/结果/文案10

## Outputs

- Final MP4: projects/0622/结果/文案10/文案10_final.mp4
- Work directory: projects/0622/结果/文案10/auto-edit/edit
- Master SRT: auto-edit/edit/master.srt
- Dialogue alignment plan: auto-edit/edit/dialogue_alignment.json
- Material composition plan: auto-edit/edit/material_composition_plan.json
- Visual alignment plan: auto-edit/edit/visual_alignment_plan.json
- Title-card plan: auto-edit/edit/title_card_plan.json
- Subtitle style: auto-edit/edit/subtitle_style.json
- EDL/render plan: auto-edit/edit/edl.json, auto-edit/edit/render_plan.json
- Execution report: auto-edit/edit/execution-report.md

## Routing

- Main workflow: $F1 full_auto_edit
- ASR route: unavailable locally, use F1 silencedetect fallback.
- Manifest route: consume existing 视频说明.yaml; no generation request.

## Fallbacks

- ASR unavailable: use silencedetect n=-35dB:d=0.08 plus LLM semantic chunks.
- Tool-screen exact upload/prompt UI unavailable: use closest node workflow/material card states and record residual risk.
- Title cards: disabled because user did not request them and UI material is dense.

## Acceptance

Final MP4 decodes, has voiceover audio, hard subtitles from master.ass/master.srt, final duration within 0.25s of 42.624s, and evidence JSON validates.

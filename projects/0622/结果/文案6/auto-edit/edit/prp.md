# F1 PRP - 文案6

## Goal
Generate canonical final MP4 for script 6 using provided reference videos, material videos, script text, and voiceover.

## Route
`full_auto_edit`: N1 intake -> N3 reference rhythm -> N4 subtitle timeline -> N5 visual plan -> N6 render -> N7 verify -> N8 report.

## Key Gates
- Preserve source material and F1 skill files.
- Use voiceover as main clock.
- Generate `master.srt`, `dialogue_alignment.json`, `subtitle_style.json`, `visual_alignment_plan.json`, `edl.json`, `render_plan.json`.
- Render H.264/AAC MP4 and verify by ffprobe, full decode, and frames.

## Fallback
ASR unavailable, so use LLM semantic chunks projected to detected speech intervals.

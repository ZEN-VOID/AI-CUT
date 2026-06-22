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
- Dialogue alignment JSON:
- Material composition plan JSON:
- Visual alignment plan JSON:
- Title-card plan JSON with cue, source text, card type, duration policy, safe zone, subtitle policy, and layer order:
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
- Dialogue alignment confirms subtitle text maps to the spoken audio/script span for every cue.
- Material composition confirms `operation_demo`, `tool_display`, and `aigc_content` are ordered by cue/audio span as one primary visual timeline.
- Visual alignment confirms tool-screen subtitle spans map to matching screen states when tool segments are present.
- Title-card processing confirms every enabled big-text card maps to subtitle cue indices, voiceover/script spans, source text, card type, duration policy, safe zone, subtitle display policy, and `before_hard_subtitles` layer order.
- Subtitle style JSON exists and validates requested font, size, color, outline, shadow, position, margins, line policy, and fallback evidence.
- Frame checks confirm subtitle readability and cover any tool-screen or title-card spans.
- Fallbacks and residual risks are reported.

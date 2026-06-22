# F1 PRP: <project-or-topic>

## Goal

Create a reference-rhythm voiceover final cut from user video, script text, voiceover audio, and reference clips.

## Inputs

- Reference directory:
- Source video:
- Script text:
- Voiceover audio:
- Result directory:

## Outputs

- Final MP4:
- Work directory:
- Master SRT:
- Dialogue alignment plan:
- Material composition plan:
- Visual alignment plan:
- Title-card plan with trigger, source text, card type, safe zone, and layer order:
- Subtitle style:
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
5. Tool-screen and title-card processing planning.
6. Visual mapping and missing-material fill.
7. Final render.
8. Verification and report.

## Fallbacks

- ASR unavailable:
- libass unavailable:
- Reference rhythm cannot be machine-detected:
- Source video too short or mismatched:
- Material category has no matching segment:
- Tool-screen state unavailable:
- Title-card source text, timing, layout, or subtitle relationship uncertain:

## Acceptance

- Final MP4 exists and decodes.
- Voiceover is the main audio.
- Hard subtitles match the script and are synced.
- Operation-demo, tool-display, and AIGC-content segments are composed by cue/audio span as one primary visual timeline.
- Tool-screen segments, when present, map each relevant subtitle cue to a matching screen state.
- Title cards, when enabled, bind card text to subtitle cue indices, voiceover/script spans, source text, safe zone, subtitle policy, and `before_hard_subtitles` layer order.
- Final duration is close to voiceover duration.
- Report records validation and fallbacks.

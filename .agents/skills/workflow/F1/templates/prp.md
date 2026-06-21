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
4. Visual mapping and missing-material fill.
5. Final render.
6. Verification and report.

## Fallbacks

- ASR unavailable:
- libass unavailable:
- Reference rhythm cannot be machine-detected:
- Source video too short or mismatched:

## Acceptance

- Final MP4 exists and decodes.
- Voiceover is the main audio.
- Hard subtitles match the script and are synced.
- Final duration is close to voiceover duration.
- Report records validation and fallbacks.


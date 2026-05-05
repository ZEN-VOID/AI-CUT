# Changelog

## 2026-05-05

- Changed generation/editing default behavior to stop after session creation and metadata persistence; progress query and local download are now passive operations that run only when the user explicitly requests them.
- Preserved project/video output directories as later download targets instead of treating missing local media as a failure when the canvas already shows results.
- Added explicit video defaults for LibTV handoff: sound/audio enabled, 15 seconds, 16:9, 720P, and do not shorten to 10 seconds unless the user requests it.
- Strengthened video defaults after a 10s provider result: hard 15-second/audio-on parameters must now appear before creative text and instruct the canvas/video duration to be set to 15s before generation.
- Simplified the canvas rule: tell 龙虾 `把全部工作流和结果都放在画布上。` at task start.
- Updated execution workflow, review gate, type packages, output template, README, script notes, and product metadata to report canvas notice status.
- Standardized reference-image/video handoff: upload local references first with the active LibTV access/project context, then submit only the returned OSS URLs in the prompt.

## 2026-05-02

- Created Skill 2.0 wrapper at `.agents/skills/cli/libTV/`.
- Imported upstream LibTV CLI scripts and MIT license from `libtv-labs/libtv-skills`.
- Added routing, type packages, review gate, output template, context, and OpenAI metadata.

# Context: libTV

This file stores reusable experience for the `libTV` Skill 2.0 package. It does not redefine the execution contract in `SKILL.md`.

## Type Map

| type_id | trigger symptom | likely root | immediate move | prevention check |
| --- | --- | --- | --- | --- |
| `TM-LIBTV-01` | User asks for LibTV/LibLib.tv media generation | route classification | Load `types/generation/generation.md` | Do not route to generic imagegen when LibTV is explicit |
| `TM-LIBTV-02` | User supplies local image/video reference(s) plus edit or generation instruction | reference handoff | Load `types/editing/editing.md`, upload all references first under the target access/project context | Submitted message includes numbered OSS URLs and original wording, and contains no local reference paths |
| `TM-LIBTV-03` | User gives `sessionId` or asks progress/download | passive session operation | Load `types/session-ops/session-ops.md` | Do not create a new session unless requested; query/download only because the user asked |
| `TM-LIBTV-04` | Prompt becomes more ornate than user request | local prompt overreach | Strip local additions and ask before changing wording | Final report states pass-through behavior |
| `TM-LIBTV-05` | Script cannot run because credential is missing | environment | Stop before API call and request `LIBTV_ACCESS_KEY` setup | Help/syntax checks use compile-only validation when no key exists |
| `TM-LIBTV-06` | Workflow/result should appear on canvas | canvas notice | Tell 龙虾 `把全部工作流和结果都放在画布上。` at task start | Final report includes canvas notice status and `projectUrl` |
| `TM-LIBTV-08` | Canvas instruction was delayed until after result completion | late canvas instruction | Put the notice in the initial handoff, or append it once to an active session | Handoff contains a separate creative-source block and start-of-task canvas notice |
| `TM-LIBTV-07` | Generation/editing route starts polling or downloading on its own | auto follow-up overreach | Stop at session metadata and project canvas URL; wait for explicit query/download request | Queue/report records passive next action, not poll interval |
| `TM-LIBTV-09` | Video comes back silent or only 10 seconds | soft or late video defaults ignored by provider/canvas | Move hard video parameters before creative text: 15-second video, not 10 seconds, set canvas/video duration to 15 seconds before generation, sound/audio enabled | Submitted handoff starts with hard video defaults and records `audio_enabled: true` / `duration_seconds: 15`; provider mismatch is reported if ignored |

## Repair Playbook

1. If routing is wrong, reload `types/type-map.md` and select the narrowest matching package.
2. If a file upload is involved, verify file existence and MIME intent before calling `upload_file.py`; stop before session submission if any upload lacks a returned OSS URL.
3. If API calls fail, first check `LIBTV_ACCESS_KEY`, then optional `OPENAPI_IM_BASE` or `IM_BASE_URL`.
4. If the canvas shows results but no local file exists, do not treat it as a failure unless the user asked for a local download.
5. If the user explicitly asks for local files, run `download_results.py` into the recorded output directory when available.
6. If creating or continuing a LibTV generation/editing task, tell 龙虾 `把全部工作流和结果都放在画布上。` at task start.
7. For video tasks, include a separate first hard-parameter block with sound/audio enabled and 15-second duration; avoid soft wording like "about 15 seconds". If the provider still returns 10 seconds or silence, report provider mismatch and rerun only on user request.
8. If a queued job needs later follow-up, preserve `sessionId`, `projectUrl`, and output directory; do not schedule automatic polling from this skill contract.
9. If a user later corrects long-term LibTV usage preferences for a project, store project-specific preference in that project's `MEMORY.md`, not here.

## Reusable Heuristics

- The highest-risk failure is not API syntax; it is local creative overreach before sending the request to LibTV.
- Treat filename prefixes as local organization only. They must not leak into the creative instruction unless the user wrote them as part of the request.
- Return the project canvas link immediately after session creation; the canvas is the default progress and result surface.
- For edits or AIGC reference routes, uploaded OSS URLs are part of the handoff payload, but the user's own wording remains the creative source of truth.
- Local paths are never prompt references for LibTV. They are only inputs to `upload_file.py`; the submitted handoff must cite project-accessible OSS URLs.
- Prefer compile checks for bundled scripts in environments without `LIBTV_ACCESS_KEY`; several runtime paths are designed to fail fast when credentials are absent.
- Canvas placement is a start-of-task operational notice, not creative prompt rewriting.
- Do not auto-poll or auto-download. Query and download are passive operations triggered by explicit user requests; keep local `videos/` or output directories as ready targets for later downloads.
- The default video spec is operational, not creative embellishment: sound/audio enabled, 15 seconds, 16:9, 720P. Put it before the creative source and explicitly say to set the canvas/video duration to 15 seconds before generation because the provider may otherwise default to 10 seconds.

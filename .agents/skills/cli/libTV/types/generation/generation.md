# Generation Type Package

Use for new LibTV image/video creation from user text.

## Fixed Context

- Preserve the user's original creative request inside a `【创作请求原文】` block.
- Do not locally expand, translate, embellish, or split the prompt.
- For new requests, submit a managed handoff that tells 龙虾 `把全部工作流和结果都放在画布上。` at the start.
- For video requests, put a separate `【视频默认规格】` block before `【创作请求原文】` unless the user explicitly overrides it: hard parameter wording, 15-second video, not 10 seconds, set the canvas/video duration to 15 seconds before generation, sound/audio enabled, 16:9, 720P.
- Use `create_session.py --session-id` only when the user explicitly wants to append to an existing session, or when adding the required start-of-task canvas notice to an active session.
- Do not automatically poll or download after session creation. The project canvas is the default place to inspect progress/results; query/download only when the user explicitly asks.

## Required Evidence

- `sessionId`
- `projectUuid` when returned
- final `projectUrl`
- start-of-task canvas notice status
- submitted video defaults when applicable: `audio_enabled: true`, `duration_seconds: 15`, `ratio: 16:9`, `resolution: 720P`
- intended output directory or video directory placeholder
- query/download evidence only when explicitly requested

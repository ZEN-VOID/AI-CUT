# Session Operations Type Package

Use for querying, appending to, downloading from, or changing LibTV session/project state.

## Fixed Context

- Do not create a new session when the user only asked to query or download an existing one.
- Use `--after-seq` when the user provides an incremental query boundary or when continuing a known explicit query flow.
- Query and download are passive operations: run them only when the user explicitly asks for progress/status or local files.
- Report `projectUrl` when a `projectUuid` is known or returned.
- Switching project affects subsequent session creation for the current access key; mention that scope in the result.
- When querying an active session whose original handoff lacks the canvas notice, append `把全部工作流和结果都放在画布上。` once as a corrective management note.

## Required Inputs By Operation

| operation | required input |
| --- | --- |
| query progress | explicit user query/progress request and `sessionId` |
| append message | `sessionId` and message |
| download results | explicit user download/local-file request plus `sessionId` or explicit result URLs |
| corrective canvas notice | active `sessionId` |
| change project | `LIBTV_ACCESS_KEY` |

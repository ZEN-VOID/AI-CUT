# Session Operations Type Package

Use for querying, appending to, downloading from, or changing LibTV session/project state.

## Fixed Context

- Do not create a new session when the user only asked to query or download an existing one.
- Use `--after-seq` when the user provides an incremental polling boundary or when continuing a known poll loop.
- Report `projectUrl` when a `projectUuid` is known or returned.
- Switching project affects subsequent session creation for the current access key; mention that scope in the result.

## Required Inputs By Operation

| operation | required input |
| --- | --- |
| query progress | `sessionId` |
| append message | `sessionId` and message |
| download results | `sessionId` or explicit result URLs |
| change project | `LIBTV_ACCESS_KEY` |

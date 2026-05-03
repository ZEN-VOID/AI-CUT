# LibTV Execution Workflow

## Nodes

| node_id | input | action | output | gate |
| --- | --- | --- | --- | --- |
| `N1-INTAKE` | User request, files, session metadata | Identify generation, editing, or session operation | `type_profile` | Required data is present or a minimal clarification is needed |
| `N2-ENV` | Runtime environment | Check `LIBTV_ACCESS_KEY` before live calls | credential verdict | Stop if credential is missing |
| `N3-UPLOAD` | Local image/video path(s) | Run `scripts/upload_file.py` for each file | numbered OSS URL list | Required only for reference/editing paths |
| `N4-SESSION` | Original request and optional OSS URL list/sessionId | Run `scripts/create_session.py` | `sessionId`, `projectUuid`, `projectUrl` | Do not rewrite creative text |
| `N5-POLL` | `sessionId`, optional `afterSeq` | Run `scripts/query_session.py` until result/timeout | messages and result URL candidates | Stop on result, timeout, or repeated failure |
| `N6-DOWNLOAD` | `sessionId` or URL list | Run `scripts/download_results.py` | local files | Skip only when no downloadable result exists |
| `N7-REVIEW` | Session metadata, local files, logs | Apply `review/review-contract.md` | verdict | `pass` or `pass_with_todo` before final |

## Generation Route

1. Load `types/generation/generation.md`.
2. Check credentials.
3. Run `python3 scripts/create_session.py "<original user request>"`.
4. Poll with `query_session.py`.
5. Download with `download_results.py`.
6. Report final files and `projectUrl`.

## Editing Route

1. Load `types/editing/editing.md`.
2. Validate local file path(s), media type intent, and reference roles.
3. Run `upload_file.py <path>` for each local reference.
4. Run `create_session.py "<original user request + numbered reference URLs>"`.
5. Poll, download, and report.

## Session Operations Route

1. Load `types/session-ops/session-ops.md`.
2. For progress, run `query_session.py <SESSION_ID>`.
3. For appending, run `create_session.py "<message>" --session-id <SESSION_ID>`.
4. For download, run `download_results.py <SESSION_ID>`.
5. For project isolation, run `change_project.py`.

## Polling Defaults

- Poll every 8 seconds when an interactive task needs completion in the same turn.
- Use `--after-seq` after the first poll when continuing a session.
- Stop after roughly 3 minutes without a result unless the user asked for longer waiting.
- Retry one transient query failure; stop after three consecutive failures.

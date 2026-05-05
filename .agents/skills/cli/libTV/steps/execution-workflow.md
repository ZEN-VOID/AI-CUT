# LibTV Execution Workflow

## Nodes

| node_id | input | action | output | gate |
| --- | --- | --- | --- | --- |
| `N1-INTAKE` | User request, files, session metadata | Identify generation, editing, or session operation | `type_profile` | Required data is present or a minimal clarification is needed |
| `N2-ENV` | Runtime environment | Check `LIBTV_ACCESS_KEY` before live calls | credential verdict | Stop if credential is missing |
| `N3-UPLOAD` | Local image/video path(s) | Run `scripts/upload_file.py` for each file using the same access/project context as the target session | numbered project-accessible OSS URL list | Required for every reference/editing path; stop if any URL is missing |
| `N4-SESSION` | Preserved original request, required OSS URL list/sessionId when references exist, video default spec when applicable, and start-of-task canvas notice | Run `scripts/create_session.py` with a managed handoff message | `sessionId`, `projectUuid`, `projectUrl`, canvas notice status, submitted video defaults | Creative text is preserved in its own block; reference payload contains OSS URLs, not local paths; canvas notice and video defaults are separate |
| `N5-PERSIST` | `sessionId`, `projectUuid`, `projectUrl`, intended output directory, submitted video defaults | Write local ledger/report metadata and preserve an output directory placeholder | session record, project canvas URL, output directory, video defaults | Required for generation/editing routes; no automatic polling or downloading |
| `N6-QUERY` | explicit user query/progress request plus `sessionId`, optional `afterSeq` | Run `scripts/query_session.py` once or for the explicitly requested bounded query window | messages and result URL candidates | Passive operation only; do not run from generation/editing by default |
| `N7-DOWNLOAD` | explicit user download/local-file request plus `sessionId` or URL list | Run `scripts/download_results.py` into the recorded output directory | local files | Passive operation only; ask/skip when output collision is risky |
| `N8-REVIEW` | Session metadata, output directory, optional query/download logs, canvas notice status | Apply `review/review-contract.md` | verdict | `pass` or `pass_with_todo` before final |

## Generation Route

1. Load `types/generation/generation.md`.
2. Check credentials.
3. Build a managed handoff message:

```text
【视频默认规格】
硬性生成参数：这是 15 秒视频，不是 10 秒。生成前必须把画布/视频时长设置为 15 秒；不要使用默认 10 秒模板；不要缩短。声音/音频开启，保留物理互动音效、环境声或用户请求中的声音元素。横屏 16:9，720P。

【创作请求原文】
<original user request>

【给龙虾的工作流管理要求】
把全部工作流和结果都放在画布上。
```

4. Run `python3 scripts/create_session.py "<managed handoff message>"`.
5. Persist `sessionId`, `projectUuid`, `projectUrl`, canvas notice status, submitted video defaults when applicable, and intended output directory. For video tasks, verify the hard first block says 15 seconds before the creative text begins.
6. Do not poll or download automatically. Tell the user the canvas is the default place to inspect progress/results and that local download can be run on request.
7. Report session metadata, canvas notice status, project URL, and output directory placeholder.

## Editing Route

1. Load `types/editing/editing.md`.
2. Validate local file path(s), media type intent, and reference roles.
3. Run `upload_file.py <path>` for each local reference under the same `LIBTV_ACCESS_KEY` / selected project context that will create or append the session.
4. Confirm every upload returned an OSS URL that LibTV can access for this project; local filesystem paths are upload inputs only and must not appear in the submitted prompt.
5. Build a managed handoff message with the preserved request, numbered OSS reference URLs, the video default spec when applicable, and the separate start-of-task canvas notice.
6. Run `create_session.py "<managed handoff message>"`.
7. Persist `sessionId`, `projectUuid`, `projectUrl`, uploaded reference URLs, canvas notice status, submitted video defaults when applicable, and intended output directory.
8. Do not poll or download automatically. Query/download only when the user explicitly asks.
9. Report session metadata, canvas notice status, project URL, and output directory placeholder.

## Session Operations Route

1. Load `types/session-ops/session-ops.md`.
2. For explicit progress requests, run `query_session.py <SESSION_ID>`.
3. For appending, run `create_session.py "<message>" --session-id <SESSION_ID>`.
4. For explicit download/local-file requests, run `download_results.py <SESSION_ID>` into the recorded output directory when available.
5. For project isolation, run `change_project.py`.
6. For an existing active session whose original handoff lacks the start-of-task canvas notice, append `把全部工作流和结果都放在画布上。` once as a corrective management note.

## Passive Query And Download Policy

- Do not automatically poll after session creation.
- Do not automatically download generated media after session creation.
- Preserve the intended output directory, including AIGC video `videos/` directories, so a later explicit download has a stable target.
- When the user explicitly asks for status/progress, run `query_session.py` and report the current remote state without creating a new session.
- When the user explicitly asks to download/localize results, run `download_results.py` and write into the recorded output directory when available.
- Use `--after-seq` only when the user provides an incremental boundary or when continuing a known explicit query flow.
- Retry one transient query/download failure; stop after three consecutive failures.
- Do not create a new session while querying an existing `sessionId` unless the user explicitly requests rerun or append.

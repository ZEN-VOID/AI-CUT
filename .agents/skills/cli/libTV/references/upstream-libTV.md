# Upstream LibTV Skill Reference

Source repository: `https://github.com/libtv-labs/libtv-skills`

Imported upstream package: `skills/libtv-skill`

License: MIT, copied into `LICENSE.txt`.

## Runtime Requirements

- `python3`
- `LIBTV_ACCESS_KEY` for Bearer authentication
- Optional `OPENAPI_IM_BASE` or `IM_BASE_URL`; default is `https://im.liblib.tv`

## Script Inventory

| script | purpose |
| --- | --- |
| `scripts/create_session.py` | Create a session or send a message to an existing session |
| `scripts/query_session.py` | Query messages for a session, optionally after a sequence number |
| `scripts/change_project.py` | Switch the project bound to the current access key |
| `scripts/upload_file.py` | Upload local image/video files and return an OSS URL |
| `scripts/download_results.py` | Extract media URLs from session messages or download explicit URLs |
| `scripts/_common.py` | Shared environment, HTTP, session, and project URL helpers |

## API Shape

| method | path | purpose |
| --- | --- | --- |
| `POST` | `/openapi/session` | Create session or send message |
| `GET` | `/openapi/session/:sessionId` | Query session messages |
| `POST` | `/openapi/session/change-project` | Switch project |
| `POST` | `/openapi/upload` | Upload local media through the imported script |

## Integration Notes

- The upstream OpenClaw skill says the local agent should pass the user's original message through to LibTV and let the backend agent plan models and workflow.
- Completed tasks should report generated result links or local downloaded files plus the project canvas URL.
- The imported upload script currently calls `/openapi/upload`; keep this reference aligned if the upstream API path changes.

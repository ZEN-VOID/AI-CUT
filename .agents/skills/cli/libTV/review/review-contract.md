# LibTV Review Contract

## Review Gates

| gate_id | check | pass condition | failure route |
| --- | --- | --- | --- |
| `RV-LIBTV-01` | Type package loaded | `generation`, `editing`, or `session-ops` was selected from `types/type-map.md` | Reload type map |
| `RV-LIBTV-02` | Credential handling | Live API calls only run when `LIBTV_ACCESS_KEY` exists | Stop and report missing env |
| `RV-LIBTV-03` | Prompt pass-through | Submitted creative message preserves the user's wording in a separate creative-source block; reference URLs and canvas notice appear only as separate operational blocks | Rebuild handoff or ask user |
| `RV-LIBTV-04` | Reference handling | Every local reference was uploaded before session submission, each upload returned a project-accessible OSS URL, and the submitted prompt includes only those numbered URLs instead of local file paths | Re-run upload/handoff |
| `RV-LIBTV-05` | Start-of-task canvas notice | New generation/editing handoff tells 龙虾 `把全部工作流和结果都放在画布上。`, or an existing active session received that corrective notice once | Rebuild initial handoff before submit, or append the notice once |
| `RV-LIBTV-06` | Video defaults | Video generation/editing handoff includes sound/audio enabled and 15-second duration unless the user explicitly overrides them; it also says not to shorten to 10 seconds | Rebuild handoff with the default video spec |
| `RV-LIBTV-07` | Session persistence | `sessionId`, `projectUuid` when returned, `projectUrl`, intended output directory, and submitted video defaults when applicable are recorded | Rebuild ledger/report from create-session output |
| `RV-LIBTV-08` | Passive follow-up boundary | New generation/editing routes did not automatically poll or download; query/download ran only if explicitly requested | Remove auto follow-up and report canvas URL as the default inspection surface |
| `RV-LIBTV-09` | Passive query result | When the user explicitly requested query/progress, result URLs or current remote status are reported; if duration/audio metadata is visible, compare it against submitted defaults | Run `query_session.py` or report query blocker |
| `RV-LIBTV-10` | Passive local delivery | When the user explicitly requested download/local files, downloaded files exist locally or a download blocker is reported; if media inspection shows 10s or silent output despite defaults, report provider mismatch | Run `download_results.py` or explain failure |

## Verdicts

- `pass`: API route completed, start-of-task canvas notice was declared, video defaults were included when applicable, session metadata and intended output directory were recorded, no automatic poll/download occurred unless explicitly requested, and `projectUrl` is reported.
- `pass_with_todo`: session is valid but generation is still running on the canvas, canvas notice could only be added as a corrective note, explicit query/download was not requested, or an explicitly requested download could not complete for a stated reason.
- `needs_rework`: prompt overreach, missing reference upload, missing video default spec for a video task, local path submitted as a reference, wrong route, or unreported credential failure affected the submitted task.

## Provider Notes

This review can be run locally by the main agent. Use code review providers only when changing the bundled Python scripts or their API behavior.

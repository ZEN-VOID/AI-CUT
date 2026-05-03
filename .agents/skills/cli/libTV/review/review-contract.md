# LibTV Review Contract

## Review Gates

| gate_id | check | pass condition | failure route |
| --- | --- | --- | --- |
| `RV-LIBTV-01` | Type package loaded | `generation`, `editing`, or `session-ops` was selected from `types/type-map.md` | Reload type map |
| `RV-LIBTV-02` | Credential handling | Live API calls only run when `LIBTV_ACCESS_KEY` exists | Stop and report missing env |
| `RV-LIBTV-03` | Prompt pass-through | Submitted creative message preserves the user's wording except appended reference URL | Rebuild handoff or ask user |
| `RV-LIBTV-04` | Reference handling | Local reference was uploaded and OSS URL included when needed | Re-run upload/handoff |
| `RV-LIBTV-05` | Result handling | Result URLs or timeout status are known | Continue polling or report timeout |
| `RV-LIBTV-06` | Local delivery | Downloaded files exist locally when remote result URLs are available | Run download or explain failure |

## Verdicts

- `pass`: API route completed, final files or result links are available, and `projectUrl` is reported.
- `pass_with_todo`: session is valid but generation is still running, timed out, or remote result exists but download could not complete for a stated reason.
- `needs_rework`: prompt overreach, missing reference upload, wrong route, or unreported credential failure affected the submitted task.

## Provider Notes

This review can be run locally by the main agent. Use code review providers only when changing the bundled Python scripts or their API behavior.

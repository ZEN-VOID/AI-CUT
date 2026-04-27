# Satellite Routing

`query/` and `resume/` are satellite skills around the `story2026` mainline. They may consume 上下文回流 truth, but they do not own validated actualization writeback.

## Route Matrix

| request shape | route | output boundary |
| --- | --- | --- |
| "Has this happened?", "where is the evidence?", "current state?" | `../query/SKILL.md` | query answer only, no truth writeback |
| "continue", "detect interruption", "rerun", "cleanup pending" | `../resume/SKILL.md` | recovery instruction or rerun plan, no direct actualization |
| "fix the card/plan/manuscript/review source" | upstream owner stage | source repair patch or stage artifact |
| "write PASS results back" with full handoff gate | `5-上下文回流` | canonical context-return artifact and serial truth writeback |

## Non-Impersonation Rule

Satellite output must not be named or presented as `5-上下文回流/第V卷.context-return.json`.

If a satellite skill discovers that a valid PASS handoff is waiting for actualization, it should point back to `story-context-return` rather than performing writeback itself.

## Evidence Handoff

When rerouting, preserve:

- `project_root`
- `volume_ref`
- `chapter_refs`
- relevant `validation_ref`
- missing gate reason
- recommended owner stage

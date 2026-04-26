# Loopback Actualization Spec

`5-Loopback` only handles volume-level validated actualization. It does not validate drafts, persist review reports, or repair upstream source truth.

## Intake Gate

All three conditions are mandatory:

- `validation_status == PASS`
- `routing_decision == handoff_to_review_and_loopback`
- `handoff_targets` contains both `review/` and `5-Loopback`

`PASS` without `5-Loopback` handoff is a historical review result, not actualization permission.

## Delta Source Boundary

`loopback_delta` may contain only validated results that can be traced to the accepted aggregate and evidence refs.

It must not contain:

- drafting guesses
- subjective review advice not accepted by the aggregate
- source-fix drafts
- projected future plans
- inferred actualization without validation evidence

## Writeback Targets

- `Cards.current_state/history`
- `2-Planning/整体规划.actualization.json`
- `2-Planning/第V卷/卷规划.actualization.json`
- `2-Planning/第V卷/第N章.actualization.json`
- matched `2-Planning/卷分片/*.json.content.holomap_slice.actualization`
- `2-Planning/全息地图.json.content.holomap.actualization`
- `STATE.json` projections and runtime markers

## Projection Refresh Semantics

- `target_type` decides the canonical root slot.
- Unless `target_type == runtime_marker`, `target_ref` means a logical child path under the root slot and supports `.` or `/` separators.
- `expected_revision` is optional. If provided, it must match `STATE.json.runtime_markers.loopback_state_revision`.
- `refresh_mode` must be one of `replace`, `merge`, or `append`.

## Revision Guardrail

| delta | revision requirement |
| --- | --- |
| `card_delta.expected_revision` | target card current `loopback_revision` |
| `map_delta.expected_revision` | `story_map.actualization.revision` |
| `projection_refresh.expected_revision` | `STATE.json.runtime_markers.loopback_state_revision` |

## Delta Whitelist

| delta | allowed fields |
| --- | --- |
| `card_delta` | `target_ref`, `target_type`, `write_policy`, `expected_revision`, `current_state_patch`, `history_append` |
| `map_delta` | `target_bucket`, `target_ref`, `slice_ref`, `write_policy`, `expected_revision`, `actualization_patch` |
| `projection_refresh` | `target_ref`, `target_type`, `refresh_mode`, `expected_revision`, `payload` |

## Commit Discipline

Loopback must finish gate validation, delta normalization, and staged patch calculation before any truth writeback starts.

Actual disk writes are committed in this order:

1. write pending manifest to `STATE.json.runtime_markers.loopback_pending`
2. write `Cards.current_state/history`
3. write planning sidecars in `book -> volume -> chapter` order
4. write story_map slice actualization
5. write root story_map actualization summary/index
6. refresh `STATE.json` projections and runtime markers
7. write `5-Loopback/第V卷.loopback.json`
8. remove pending marker and persist committed manifest

## Hard Rules

- Do not rewrite `validation_status`, `routing_decision`, or `handoff_targets`.
- Do not overwrite `planned_*`.
- Do not write validated actualization directly into planning markdown bodies.
- Do not mix query or resume requests into the actualization main flow.
- Do not write volume-level actualization details back into a root-only carrier.

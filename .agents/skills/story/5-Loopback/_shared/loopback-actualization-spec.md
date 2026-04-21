# Loopback Actualization Spec

`5-Loopback` 只处理卷级 validated actualization。

## Intake Gate

- `validation_status == PASS`
- `routing_decision == handoff_to_review_and_loopback`
- `handoff_targets` 同时包含 `review/` 与 `5-Loopback`

## Writeback Targets

- `Cards.current_state/history`
- 当前卷命中的 `2-Planning/卷分片/*.json.content.holomap_slice.actualization`
- `2-Planning/全息地图.json.content.holomap.actualization`
- `STATE.json` projections / runtime markers

## Projection Refresh Semantics

- `target_type` 决定 canonical root slot。
- 非 `runtime_marker` 时，`target_ref` 表示 root slot 之下的逻辑子路径，支持 `.` 或 `/` 分隔。
- `expected_revision` 可选；若提供，必须与当前 `STATE.json.runtime_markers.loopback_state_revision` 一致，否则拒绝提交。
- `refresh_mode`
  - `replace`
  - `merge`
  - `append`

## Revision Guardrail

- `card_delta.expected_revision`
  - 对齐目标 card 当前 `loopback_revision`
- `map_delta.expected_revision`
  - 对齐 `story_map.actualization.revision`
- `projection_refresh.expected_revision`
  - 对齐 `STATE.json.runtime_markers.loopback_state_revision`

## Delta Whitelist

- `card_delta`
  - 允许字段：`target_ref / target_type / write_policy / expected_revision / current_state_patch / history_append`
- `map_delta`
  - 允许字段：`target_bucket / target_ref / slice_ref / write_policy / expected_revision / actualization_patch`
- `projection_refresh`
  - 允许字段：`target_ref / target_type / refresh_mode / expected_revision / payload`

## Commit Discipline

- loopback 必须先完成 gate 校验、delta normalize 与 staged patch 计算，再开始任何 truth writeback。
- 实际写盘按 `Cards -> MAP -> STATE -> loopback artifact` 顺序提交。
- 其中 MAP 再拆为 `slice actualization -> root actualization summary/index`。
- 提交前必须先写一个 `runtime_markers.loopback_pending` manifest；成功后移除 pending，并把 committed manifest 固化到 `runtime_markers.loopback.last_commit_manifest` 与 loopback artifact。

## Hard Rules

- 不得改写 `validation_status / routing_decision / handoff_targets`
- 不得覆盖 `planned_*`
- 不得把 query / resume 请求混入 actualization 主流程
- 不得把卷级 actualization 明细重新写回 root-only carrier

# Loopback Actualization Spec

`5-Loopback` 只处理 validated actualization。

## Intake Gate

- `validation_status == PASS`
- `routing_decision == handoff_to_review_and_loopback`
- `handoff_targets` 同时包含 `review/` 与 `5-Loopback`

## Writeback Targets

- `Cards.current_state/history`
- `2-Planning/十集分片/*.json.content.holomap_slice.actualization`
- `2-Planning/全息地图.json.content.holomap.actualization`
- `STATE.json` projections / runtime markers

### Character Growth Writeback

- 对主角或显式启用的反派，validated growth 只允许写回：
  - `current_state.growth_state`
  - `experience_timeline.current_growth_stage`
  - `experience_timeline.axis_stage_map`
  - `experience_timeline.growth_log`
  - `history[].growth_delta`
- 不得在 loopback 中改写：
  - `core.growth_contract.entry_anchor`
  - `core.growth_contract.destiny_ceiling`
  - `core.growth_contract.axes.*.initial_state`
  - `core.growth_contract.axes.*.ceiling`

## Projection Refresh Semantics

- `target_type` 决定 canonical root slot。
- 非 `runtime_marker` 时，`target_ref` 表示 root slot 之下的逻辑子路径，支持 `.` 或 `/` 分隔。
- `expected_revision` 可选；若提供，必须与当前 `STATE.json.runtime_markers.loopback_state_revision` 一致，否则拒绝提交。
- `refresh_mode`
  - `replace`: 用 payload 整体替换目标位。
  - `merge`: 仅对对象有效，保留旧字段并做深合并。
  - `append`: 仅对数组有效，向目标位追加 payload。

## Revision Guardrail

- `card_delta.expected_revision`
  - 对齐目标 card 当前 `loopback_revision`。
- `map_delta.expected_revision`
  - 对齐 `story_map.actualization.revision`。
- `projection_refresh.expected_revision`
  - 对齐 `STATE.json.runtime_markers.loopback_state_revision`。
- 若任一 expected revision 与当前 truth 层不一致，loopback 必须阻断 actualization，禁止把旧 delta 强行覆盖到新 truth 上。

## Delta Whitelist

- `card_delta`
  - 允许字段：`target_ref / target_type / write_policy / expected_revision / current_state_patch / history_append`
  - 禁止把 `core / meta / content / review_* / validation_* / routing_*` 等对象级或 gate 级字段塞进 `current_state_patch`
  - 若角色启用了成长系统，`current_state_patch` 可以携带嵌套的 `growth_state`
  - `history_append` 可以携带 `growth_delta`
- `map_delta`
  - 允许字段：`target_bucket / target_ref / slice_ref / write_policy / expected_revision / actualization_patch`
  - `actualization_patch` 禁止出现 `planned_*` 与 review/source-fix 污染字段
- `projection_refresh`
  - 允许字段：`target_ref / target_type / refresh_mode / expected_revision / payload`

## Commit Discipline

- loopback 必须先完成 gate 校验、delta normalize 与 staged patch 计算，再开始任何 truth writeback。
- 实际写盘按 `Cards -> MAP -> STATE -> loopback artifact` 顺序提交。
- 其中 MAP 再拆为 `slice actualization -> root actualization summary/index`。
- 提交前必须先写一个 `runtime_markers.loopback_pending` manifest；成功后移除 pending，并把 committed manifest 固化到 `runtime_markers.loopback.last_commit_manifest` 与 loopback artifact。
- 提交阶段若中途失败，必须对已写文件执行 best-effort rollback，禁止留下“truth 已部分写回但 closure artifact 缺失”的半完成态。

## Hard Rules

- 不得改写 `validation_status / routing_decision / handoff_targets`
- 不得覆盖 `planned_*`
- 不得把 query / resume 请求混入 actualization 主流程
- 不得把 episode-local actualization detail 重新写回 `全息地图.json`

## Type-Pack Feedback Rule

- `5-Loopback` 可以沉淀：
  - 哪类 pack hook 在 validated actual 中表现良好
  - 哪类 pack 规则在本项目中需要降权或谨慎使用
- 这些反馈只能进入下一轮 projection 参考，不得直接改写 `north_star.yaml.type_stack`

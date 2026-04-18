# Loopback Actualization Spec

`5-Loopback` 只处理 validated actualization。

## Intake Gate

- `validation_status == PASS`
- `routing_decision == handoff_to_review_and_loopback` 或 `handoff_targets` 包含 `5-Loopback`

## Writeback Targets

- `Cards.current_state/history`
- `2-Planning/全息地图.json.content.holomap.actualization`
- `STATE.json` projections / runtime markers

## Hard Rules

- 不得改写 `validation_status / routing_decision / handoff_targets`
- 不得覆盖 `planned_*`
- 不得把 query / resume 请求混入 actualization 主流程

## Type-Pack Feedback Rule

- `5-Loopback` 可以沉淀：
  - 哪类 pack hook 在 validated actual 中表现良好
  - 哪类 pack 规则在本项目中需要降权或谨慎使用
- 这些反馈只能进入下一轮 projection 参考，不得直接改写 `north_star.yaml.type_stack`

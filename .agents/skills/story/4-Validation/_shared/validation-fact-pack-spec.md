# Validation Fact Pack Spec

`validation_fact_pack` 是 `4-Validation` 父层锁定后分发给全部 child validators 的统一事实包。

## Required Slices

- `draft_snapshot`
- `cards_truth`
- `planning_truth`
- `init_truth`
- `runtime_context`

## Hard Rules

- 六个 child 必须读取同一份 pack。
- 任一 required slice 缺失，直接 `FAIL-COVENANT`。
- pack 只能由当前轮动态生成，不得复用旧 residual artifact。

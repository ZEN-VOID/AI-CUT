# Validation Fact Pack Spec

`validation_fact_pack` 是 `4-Validation` 父层锁定后分发给全部 child validators 的统一事实包。

## Required Slices

- `draft_snapshot`
- `cards_truth`
- `planning_truth`
- `init_truth`
- `runtime_context`

## `planning_truth` Minimum Shape

- `global_index_ref`
- `active_slice_ref`
- `chapter_board`
- `thread_window_slice`
- `foreshadow_silence_slice`

## Hard Rules

- 六个 child 必须读取同一份 pack。
- 任一 required slice 缺失，直接 `FAIL-COVENANT`。
- pack 只能由当前轮动态生成，不得复用旧 residual artifact。
- `planning_truth` 不得只给 `全息地图.json` 路径而缺 active slice；缺少 `chapter_board / thread_window_slice / foreshadow_silence_slice` 时同样视为 `FAIL-COVENANT`。

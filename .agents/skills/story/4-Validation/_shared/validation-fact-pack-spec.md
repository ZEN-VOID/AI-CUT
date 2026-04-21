# Validation Fact Pack Spec

`validation_fact_pack` 是 `4-Validation` 父层锁定后分发给全部 child validators 的统一卷级事实包。

## Required Slices

- `draft_snapshot`
- `cards_truth`
- `planning_truth`
- `init_truth`
- `runtime_context`

## `draft_snapshot` Minimum Shape

- `volume_ref`
- `chapter_refs`
- `manuscript_refs`
- `volume_log_ref`
- `worker_status_snapshot`

## `planning_truth` Minimum Shape

- `global_index_ref`
- `active_slice_ref`
- `volume_board`
- `slice_style_contract`
- `episode_boards`
- `cross_chapter_continuity_matrix`
- `thread_window_slice`
- `foreshadow_silence_slice`

## Hard Rules

- 六个 child 必须读取同一份 pack。
- 任一 required slice 缺失，直接 `FAIL-COVENANT`。
- pack 只能由当前轮动态生成，不得复用旧 residual artifact。
- `planning_truth` 不得只给 `全息地图.json` 路径而缺 active slice。
- 若缺少 `volume_board / slice_style_contract / episode_boards / cross_chapter_continuity_matrix`，同样视为 `FAIL-COVENANT`。
- `episode_boards[].planned_state` 至少应已带 `chapter_promise / entry_state / carryover_threads / expected_exit_delta`，否则连续性与人物/结构维度无法对齐同一 planning truth。

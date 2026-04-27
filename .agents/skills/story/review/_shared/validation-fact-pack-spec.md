# Validation Fact Pack Spec

`validation_fact_pack` 是 `review` 父层锁定后分发给全部 child validators 的统一卷级事实包。

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
- `accepted_manuscript_stage`
- `accepted_manuscript_refs`
- `volume_log_ref`
- `worker_status_snapshot`

## `planning_truth` Minimum Shape

- `book_plan_ref`
- `volume_plan_ref`
- `chapter_plan_refs`
- `book_plan_actualization_ref`
- `volume_plan_actualization_ref`
- `chapter_plan_actualization_refs`
- `volume_planning_summary`
- `chapter_planning_packets`

## Hard Rules

- 全部 mandatory child validators 必须读取同一份 pack。
- 任一 required slice 缺失，直接 `FAIL-COVENANT`。
- pack 只能由当前轮动态生成，不得复用旧 residual artifact。
- `final_acceptance` 用于 context-return handoff 时，必须锁定 accepted manuscript；默认 `accepted_manuscript_stage = 4-润色`。若跳过润色，必须显式声明 `accepted_manuscript_stage = 3-初稿` 与 skip-polish acceptance note。
- `planning_truth` 不得只给兼容 `全息地图.json` 路径而缺当前卷 `卷规划.md` 与当前卷 `第N章.md`。
- 若缺少 `volume_plan_ref / chapter_plan_refs / volume_planning_summary / chapter_planning_packets`，同样视为 `FAIL-COVENANT`。
- `volume_planning_summary` 至少应已能回答 `上承部级主任务 / 本卷任务线主线 / 支线 / 汇聚回主线`，否则 `任务汇聚` 无法判断卷级支流是否真正服务主任务。
- `chapter_planning_packets[]` 至少应已能回答 `上承卷级任务 / 本章任务线 / 汇聚动作 / 未汇聚任务去向 / 本章冲突 / 章末达成 / 本章线索 / 本章伏笔`，否则连续性、结构与任务汇聚维度无法对齐同一 planning truth。

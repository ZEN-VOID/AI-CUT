# Temporal Continuity Contract

本文件定义逐画面运动强化时的上一状态回顾和时间轴推导规则。

## Core Rule

每次对新的 motion unit 落盘前，必须先回顾上一画面中相关角色的最终位置或状态，再判断当前画面的起点、路径和终点。不得在没有状态推导的情况下直接凭感觉补动作。

## Motion State Ledger

每个 motion unit 至少记录：

| field | requirement |
| --- | --- |
| `unit_id` | 稳定编号，可用场景序号、段落序号或行号 |
| `source_anchor` | source 中对应句子或行号 |
| `previous_final_state` | 上一 motion unit 结束时相关角色的位置、姿态、朝向、接触关系或状态 |
| `current_start_inference` | 当前起点如何从上一终点、场景切换或原文锚点推导 |
| `motion_subject` | 运动主体 |
| `reference_group_id` | source 中显式分镜组、场景段或临时连续动作段 ID；不得凭空生成下游分镜编号 |
| `primary_reference_frame` | 同一分镜组或连续动作段优先继承的主参照系 |
| `reference_frame` | 参照系 |
| `reference_frame_basis` | 当前参照系为何是最佳参照，或为何从主参照切到局部参照 |
| `reference_switch_reason` | 主参照系切换原因；未切换时可写 `none` |
| `start_point` | 起点 |
| `path` | 路径 |
| `end_point` | 终点 |
| `final_state` | 本 unit 结束后留给下一 unit 的位置或状态 |
| `continuity_status` | `pass`、`inferred`、`ambiguous` 或 `blocked_or_ambiguous` |

## Continuity Decision Rules

- 同场景相邻动作默认继承上一画面的 final_state。
- 同一分镜组或连续动作段默认继承 `primary_reference_frame`；只有场景切换、参照不可见、主体离开参照范围或动作重心转移时才切换。
- 场景切换时，可以把 current_start 设为新场景原文明确位置；若原文没有位置，使用保守进入点并标注 `inferred`。
- 多角色画面只继承与当前 motion_subject 有关的 final_state；其他角色状态可简写为背景状态。
- 角色瞬移、身体接触断裂、手中物突然变化或朝向无法承接时，必须标记歧义并回 source 找证据。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每个新 motion unit 是否回顾上一画面的最终位置或状态？ | `GATE-MOTION-05` | `FAIL-MOTION-CONTINUITY` | `steps/motion-workflow.md#N3-MOTION-STATE-LEDGER` | `motion_state_ledger.previous_final_state` |
| 当前起点是否能由上一终点、场景切换或原文锚点合理推导？ | `GATE-MOTION-05` | `FAIL-MOTION-CONTINUITY` | `N3-MOTION-STATE-LEDGER`、`N5R-MOTION-REPAIR` | `current_start_inference` 和 continuity verdict |
| 同一分镜组或连续动作段是否在时间轴上继承主参照系，切换时是否有原因？ | `GATE-MOTION-04A` | `FAIL-MOTION-REFERENCE-GROUP` | `N3-MOTION-STATE-LEDGER`、`N5R-MOTION-REPAIR` | `group_reference_profile` 与 `reference_switch_reason` |
| 无法推导时是否阻断或标记歧义，而不是硬补？ | `GATE-MOTION-06` | `FAIL-MOTION-AMBIGUOUS-INVENTION` | `N5R-MOTION-REPAIR` | report 中的 ambiguous/blocked unit 清单 |

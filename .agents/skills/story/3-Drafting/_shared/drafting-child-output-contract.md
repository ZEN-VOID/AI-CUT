# Drafting Child Output Contract

本文件定义 `3-Drafting` 七个子技能包的统一输出协议。

即时审计 hook 的维度注册真源固定回指：

- `../../4-Validation/_shared/validation-dimension-registry.yaml`
- `./drafting-instant-validation-contract.md`

## Canonical Output Shape

每个子技能正式输出必须同时包含：

- `manuscript_patch`
  - 对当前 `第N集.md` 的完整新版本或可直接应用的正文 patch
- `process_log_entry`
  - 写入 `写作日志.yaml.step_history[]` 的单步记录
- `type_pack_projection_summary`（可选）
  - 记录当前 step 实际采用的 pack hook、阈值与禁写提醒
- `growth_axis_evidence`（可选）
  - 记录当前 step 为主角成长系统提供的 `技能 / 心路 / 情感` 三轴证据

## process_log_entry Minimum Fields

- `step_id`
- `step_name`
- `completed_at`
- `focus_dimension`
- `summary`
- `upstream_refs`
- `continuity_checks`
- `instant_validation_summary`
- `instant_validation_refs`
- `rework_route_hint`
- `next_step_hint`
- `type_pack_refs`（可选）
- `type_pack_rules_applied`（可选）
- `growth_axis_evidence`（可选）

## Hard Rules

1. 子技能不得独立落盘第二份正文。
2. 子技能只拥有自己的加工维度，不得越权宣告 validation 结论或 loopback 写回。
3. 父层写回正文与日志后，下一子技能才能开始。
4. 若某子技能认为应回退前序工序，必须在 `process_log_entry` 中明确指出 `rework_target_step`，而不是静默重写路线。
5. 当前 step 写回后，父层必须按 registry 为该 `step_id` 触发即时审计 hook；若 hook 未通过，下一 child 不得开始。
6. `7-润色` 通过 inline hooks 后只形成 `candidate_final_draft`，不是最终 `PASS`。
7. 若当前项目启用了 `type-pack`，子技能应把实际采用的 pack rule 摘要写入 `type_pack_projection_summary` 或 `process_log_entry.type_pack_rules_applied`，便于 validation/review 追溯。
8. 正式执行必须是一 step 一提交：当前 child 只处理当前 `step_id`，只输出当前 step 的 `manuscript_patch + process_log_entry`，不得顺手预生成后续 steps 的正式 patch。
9. `Step 2-7` 只能消费“上一 step 已写回且已通过 hook 的当前 root”；不得消费尚未过 gate 的临时稿、内存稿或候选稿。
10. 允许存在 step 内部的候选版本、比较稿、reviewer 意见或句式实验，但这些内容在当前 step hook 通过前都不是正式写回结果。
11. 若项目主角启用了成长系统，则 `Step 4` 与 `Step 6` 应优先产出结构化 `growth_axis_evidence`，供后续 validation / loopback 提纯，不要把成长变化只藏在 prose 摘要里。

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

## Hard Rules

1. 子技能不得独立落盘第二份正文。
2. 子技能只拥有自己的加工维度，不得越权宣告 validation 结论或 loopback 写回。
3. 父层写回正文与日志后，下一子技能才能开始。
4. 若某子技能认为应回退前序工序，必须在 `process_log_entry` 中明确指出 `rework_target_step`，而不是静默重写路线。
5. 当前 step 写回后，父层必须按 registry 为该 `step_id` 触发即时审计 hook；若 hook 未通过，下一 child 不得开始。
6. `7-润色` 通过 inline hooks 后只形成 `candidate_final_draft`，不是最终 `PASS`。
7. 若当前项目启用了 `type-pack`，子技能应把实际采用的 pack rule 摘要写入 `type_pack_projection_summary` 或 `process_log_entry.type_pack_rules_applied`，便于 validation/review 追溯。

# Drafting Child Output Contract

本文件定义 `3-Drafting` 八个子技能包在“卷级父流程 + 集级 worker”模型下的统一输出协议。

即时审计 hook 的维度注册真源固定回指：

- `../../4-Validation/_shared/validation-dimension-registry.yaml`
- `./drafting-instant-validation-contract.md`

## Canonical Output Shape

每个 episode worker 的当前 step 正式输出必须同时包含：

- `manuscript_patch`
  - 对当前 `第N集.md` 的完整新版本或可直接应用的正文 patch
- `process_log_entry`
  - 写入 `第V卷.写作日志.yaml.chapter_step_history[chapter_ref][]` 的单步记录
- `type_pack_projection_summary`（可选）
- `growth_axis_evidence`（可选）

## process_log_entry Minimum Fields

- `volume_ref`
- `chapter_ref`
- `worker_ref`
- `step_id`
- `step_name`
- `completed_at`
- `focus_dimension`
- `summary`
- `upstream_refs`
- `continuity_refs`
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
3. 单个 worker 内必须保持一 step 一提交；当前 step 写回并过 hook 之前，后续 steps 不存在正式执行资格。
4. 父层可以并发调度多个 episode workers，但同一 `chapter_ref` 永远只允许一个 worker 持有正式写权。
5. 若某子技能认为应回退前序工序，必须在 `process_log_entry` 中明确指出 `rework_target_step` 与 `affected_workers`，而不是静默重写路线。
6. 当前 step 写回后，父层必须按 registry 为该 `step_id` 触发即时审计 hook；若 hook 未通过，当前 worker 不得进入下一 step。
7. `8-润色` 通过 inline hooks 后只形成 `candidate_final_draft`；只有卷内全部章节都达到候选终稿，父层才可声明 `candidate_volume_draft`。
8. 若当前项目启用了 `type-pack`，子技能应把实际采用的 pack rule 摘要写入 `type_pack_projection_summary` 或 `process_log_entry.type_pack_rules_applied`。
9. 若主角启用了成长系统，则 `Step 4 / Step 6 / Step 7` 应优先产出结构化 `growth_axis_evidence`，供后续卷级 validation / loopback 提纯。

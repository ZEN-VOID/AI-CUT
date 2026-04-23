# Drafting Child Output Contract

本文件定义 `3-Drafting` 八个子技能包在“卷级父流程 + 章级 worker”模型下的统一输出协议。

即时审计 hook 的维度注册真源固定回指：

- `../../4-Validation/_shared/validation-dimension-registry.yaml`
- `./drafting-instant-validation-contract.md`

## Canonical Output Shape

每个 chapter worker 的当前 step 正式输出必须同时包含：

- `manuscript_patch`
  - 对当前 `第N章.md` 的完整新版本或可直接应用的正文 patch
- `process_log_entry`
  - 写入 `第V卷.写作日志.yaml.chapter_step_history[chapter_ref][]` 的单步记录
- `type_card_projection_summary`（可选）
- `growth_axis_evidence`（可选）

## process_log_entry Minimum Fields

- `volume_ref`
- `chapter_ref`
- `worker_ref`
- `step_sequence_index`
- `step_id`
- `step_name`
- `completed_at`
- `focus_dimension`
- `summary`
- `upstream_refs`
- `continuity_refs`
- `instant_validation_summary`
- `instant_validation_refs`
- `hook_status`
- `hook_checked_dimensions`
- `hook_checked_at`
- `rework_route_hint`
- `next_step_hint`
- `type_card_refs`（可选）
- `type_card_rules_applied`（可选）
- `growth_axis_evidence`（可选）

## Hard Rules

1. 子技能不得独立落盘第二份正文。
2. 子技能只拥有自己的加工维度，不得越权宣告 validation 结论或 loopback 写回。
3. 单个 worker 内必须保持一 step 一提交；当前 step 写回并过 hook 之前，后续 steps 不存在正式执行资格。
4. 父层可以并发调度多个 chapter workers，但同一 `chapter_ref` 永远只允许一个 worker 持有正式写权。
5. 若某子技能认为应回退前序工序，必须在 `process_log_entry` 中明确指出 `rework_target_step` 与 `affected_workers`，而不是静默重写路线。
6. 当前 step 写回后，父层必须按 registry 为该 `step_id` 触发即时审计 hook；若 hook 未通过，当前 worker 不得进入下一 step。
7. `8-润色` 通过 inline hooks 后只形成 `candidate_final_draft`；只有卷内全部章节都达到候选终稿，父层才可声明 `candidate_volume_draft`。
8. 若当前项目存在明确 `类型卡`，子技能应把实际采用的题材规则摘要写入 `type_card_projection_summary` 或 `process_log_entry.type_card_rules_applied`。
9. 若主角启用了成长系统，则 `Step 4 / Step 6 / Step 7` 应优先产出结构化 `growth_axis_evidence`，供后续卷级 validation / loopback 提纯。
10. 父层必须为每个 `chapter_ref` 收满 8 条正式 `process_log_entry`；缺任一步都视为当前章节 runtime 不完整。
11. 父层必须同步为每个 `process_log_entry` 落一条对位 `hook_result`；缺 hook 结果、缺检查维度、或只写 `pass/fail` 空壳而没有检查时间与回退信息，都视为 gate evidence 缺失。
12. 禁止在 worker 完成后用汇总摘要倒填 8 步；step ledger 与 hook ledger 必须按正式执行顺序逐步产生，才能作为 `candidate_final_draft / candidate_volume_draft` 的有效依据。
13. `manuscript_patch` 不得只是“压缩版剧情稿”或“可读摘要”；父层在 `Step 8` 后必须额外确认当前 `第N章.md` 已达到章节级小说密度，默认以 `scripts/drafting_manuscript_guard.py` 为可执行守门。

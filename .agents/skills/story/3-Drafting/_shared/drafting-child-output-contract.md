# Drafting Child Output Contract

本文件定义 `3-Drafting` 七个子技能包的统一输出协议。

## Canonical Output Shape

每个子技能正式输出必须同时包含：

- `manuscript_patch`
  - 对当前 `第N集.md` 的完整新版本或可直接应用的正文 patch
- `process_log_entry`
  - 写入 `写作日志.yaml.step_history[]` 的单步记录

## process_log_entry Minimum Fields

- `step_id`
- `step_name`
- `completed_at`
- `focus_dimension`
- `summary`
- `upstream_refs`
- `continuity_checks`
- `next_step_hint`

## Hard Rules

1. 子技能不得独立落盘第二份正文。
2. 子技能只拥有自己的加工维度，不得越权宣告 validation 结论或 loopback 写回。
3. 父层写回正文与日志后，下一子技能才能开始。
4. 若某子技能认为应回退前序工序，必须在 `process_log_entry` 中明确指出 `rework_target_step`，而不是静默重写路线。

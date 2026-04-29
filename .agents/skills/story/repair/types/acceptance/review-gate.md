# Acceptance Package: Review Gate

## Selection Signals

- 用户提到验收、审计、review、code-reviewer，或任务处于 execute repair 结束阶段。

## Fixed Context

- 默认使用 `review/review-contract.md`。
- 默认以 `code-reviewer` 作为辅助审计口径。
- 验收不只检查当前文件，还检查旧口径残留、源层一致、provider evidence、review/return 状态。

## Review Gate

- 输出 verdict: `pass`、`pass_with_followups`、`needs_rework` 或 `blocked`。
- findings 必须指向 rework target。

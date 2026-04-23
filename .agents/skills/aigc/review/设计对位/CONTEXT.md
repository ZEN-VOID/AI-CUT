# CONTEXT.md

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 设计输出局部好看但整体脱离 detail/global truth | alignment layer | 回溯 `4-Design` 与上游 truth 对位 | 将 design alignment 固定成 review 维度 | `设计对位` 能在 handoff 前阻断 |

## Repair Playbook

1. 先锁 `3-Detail` 和 `4-Design` 的真源。
2. 再判问题在 list/design/panel 哪一层。

## Reusable Heuristics

- `4-Design` 最怕的不是局部 prompt 不好，而是整体对位失真。


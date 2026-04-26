# CONTEXT.md

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 设计输出局部好看但整体脱离分组 truth | alignment layer | 回溯 `5-设计` 与上游 truth 对位 | 将 design alignment 固定成 review 维度 | `设计对位` 能在 handoff 前阻断 |

## Repair Playbook

1. 先锁 `4-分组` 和 `5-设计` 的真源。
2. 再判问题在 list/design/panel 哪一层。

## Reusable Heuristics

- `5-设计` 最怕的不是局部 prompt 不好，而是整体对位失真。

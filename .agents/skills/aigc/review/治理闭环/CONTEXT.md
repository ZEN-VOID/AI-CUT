# CONTEXT.md

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| scope carrier 与 route 说法不一致 | governance closure layer | 回溯 validation carriers 与 route owner | 将 governance closure 固定成全 checkpoint 维度 | aggregate route 不再靠猜 |

## Repair Playbook

1. 先锁当前 scope 的 validation carrier。
2. 再看 `STATE / governance-state / handoff_targets` 是否一致。

## Reusable Heuristics

- 对 `aigc` 来说，很多“业务问题”最后其实是 carrier 和 route 漂移。


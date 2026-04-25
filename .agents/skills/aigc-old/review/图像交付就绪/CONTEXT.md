# CONTEXT.md

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 图像链路能生成计划但不可信交付 | delivery readiness layer | 回溯 request/binding/handoff 三段 | 将 image delivery 固定成独立 review 维度 | provider handoff 前能被阻断 |

## Repair Playbook

1. 先锁 request、binding、handoff 三段。
2. 再判问题在 continuity、binding 还是 provider pack。

## Reusable Heuristics

- `5-Image` 的 review 关键不在“能不能生成计划”，而在“这份计划是不是可信可交付”。


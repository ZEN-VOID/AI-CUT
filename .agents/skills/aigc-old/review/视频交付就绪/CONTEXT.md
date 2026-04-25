# CONTEXT.md

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 视频请求可写但交付风险仍高 | delivery readiness layer | 回溯 request/binding/handoff 三段 | 将 video delivery 固定成独立 review 维度 | provider handoff 前能被阻断 |

## Repair Playbook

1. 先锁 request、binding、handoff 三段。
2. 再判问题在 motion/duration 还是 provider pack。

## Reusable Heuristics

- `6-Video` 的 review 要比图像多看一层 motion/duration readiness。


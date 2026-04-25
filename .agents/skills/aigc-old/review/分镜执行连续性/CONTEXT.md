# CONTEXT.md

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| detail root 字段看似完整但下游仍无法消费 | handoff readiness layer | 追溯 `3-Detail` validator 与 handoff refs | 将 handoff readiness 固定成独立维度 | image/video 前能先被 review 阻断 |

## Repair Playbook

1. 先看 `第N集.json` 与 validator evidence。
2. 再判是字段缺口还是 continuity 断裂。

## Reusable Heuristics

- `3-Detail` 的 review 不应只看“有没有 JSON”，而要看它是否真能支撑下游 handoff。


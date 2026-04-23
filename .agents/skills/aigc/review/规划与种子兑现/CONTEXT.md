# CONTEXT.md

## Context Health

- soft_limit_chars: 12000
- hard_limit_chars: 24000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `episode_root` 存在但 detail root 失去 handoff 痕迹 | seed continuity layer | 回退到 `2-Global / 3-Detail` 重建 handoff | 将 seed continuity 固定成 review 维度 | `planning-seed-validator` 能指出断链位置 |

## Repair Playbook

1. 先锁 `north_star -> planning -> episode_root -> 第N集.json`。
2. 再判 seed 是否真被下游消费，而不只是文件存在。

## Reusable Heuristics

- 对 `aigc` 来说，最隐蔽的断链往往不发生在设计或出图，而是发生在 planning/global/detail 之间的 seed 漂移。


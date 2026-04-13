# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `preflight-review/` 的经验层知识库，不是过程日志。
- 每次调用本技能时，应自动预加载本文件，用于 blocker 判定、放行边界与治理摘要同步。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 没有 `mission-brief / route-plan` 就要放行 | preflight gate | 先补起草工件 | 把 preflight 固定成 review 子技能，而不是口头步骤 | verdict 前能读回两份工件 |
| 把 scope blocker 写进聊天，不回 carrier | carrier sync | 写回 `preflight-verdict.yaml` | 强制双写：carrier 本体 + governance-state 摘要 | `preflight-verdict.yaml` 与 `governance-state.yaml` 一致 |

## Repair Playbook

1. 先查 `mission-brief.yaml` 与 `route-plan.yaml`。
2. 再查是否已有旧的 `preflight-verdict.yaml`。
3. blocker 与 allowed scope 分开写，不混成一句。
4. 最后同步 `governance-state.yaml` 摘要。

## Reusable Heuristics

- preflight 最重要的是定义“现在能做什么”，而不是泛泛而谈风险。
- 对高风险任务，缺治理工件通常比缺内容证据更先阻断执行。

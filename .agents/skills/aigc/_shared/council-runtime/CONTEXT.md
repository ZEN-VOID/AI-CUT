# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/_shared/council-runtime` 的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/_shared/council-runtime/module-spec.md` 时，应预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 后续阶段忘记读取 `team.yaml` | 共享运行时层 | 在阶段根技能强制先读项目根 `team.yaml` | 用共享 `council-runtime/module-spec.md` 作为单一真源 | 阶段执行前能判断顾问团是否启用 |
| 四个阶段各自复制一套顾问团规则 | 真源治理层 | 把共性规则上收至 `_shared/council-runtime/` | 阶段根技能只保留本阶段适配，不再平行维护通用规则 | 共性规则只在共享目录维护 |
| `评审` 过早参与前置发散 | 角色边界层 | 将 `评审` 固定到阶段级 `validation-report.md` 前后 | 在共享运行时写死 `pre_and_post_validation_gate` | 评审不再抢前置创作职责 |

## Reusable Heuristics

- 对跨阶段顾问团机制来说，最重要的不是“顾问很多”，而是“团队真源只有一份、运行时只有一套”。
- `策划 / 监制` 更适合做前置参谋，`评审` 更适合卡最终闸门；三者不要混成一轮齐发。

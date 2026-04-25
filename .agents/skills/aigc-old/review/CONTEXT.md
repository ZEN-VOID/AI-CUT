# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/review` 父技能的经验层知识库，不是第二份父合同。
- 每次调用 `review/SKILL.md` 时，应与其一起加载，用于识别 checkpoint 漂移、fact pack 缺口、维度聚合错误和 route 误判。
- 冲突优先级固定为：用户显式请求 > AGENTS.md / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 24000
- hard_limit_chars: 48000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `aigc` 只有阶段内 validator，没有包级 review 聚合层 | package governance layer | 增设 `aigc/review` 父技能与 aggregate packet | 将 checkpoint/stage/package 三种审计 mode 固化到 shared registry | 当前 scope 能写出单一 `.review.json` |
| 不同维度 child skills 读取了不同 scope 或不同阶段快照 | pack covenant layer | 统一重锁 `review_fact_pack` 与 scope_ref | 让全部 child skills 只消费同一份 pack | 各 sidecar 的 `scope_ref / checkpoint_id` 一致 |
| review 结果只有 prose，没有稳定 route | aggregate gate layer | 聚合为结构化 `routing_decision + handoff_targets + rework_targets` | 在 aggregate template 中固定 gate 字段 | 下游不再靠人工猜 route |
| 阶段 `validation-report.md` 与包级 review packet 互相争真源 | carrier layering | 保留两层：阶段验收仍写本阶段 carrier，包级审计另写 `review/*.review.json` | 明确 review 是卫星技能，不吞并阶段 carrier | 阶段 carrier 与 review packet 边界稳定 |
| 审计已经跑了，但 `query / resume` 仍看不到最新返工入口 | review bridge sync layer | 把 aggregate 结论同步回 `governance-state.yaml.review_bridge + resume_contract.required_repairs` | 固定 review runner 在审后自动写 repair bridge，而不是让卫星技能各自猜下一入口 | 查询与续跑能读到同一份 repair route |

## Repair Playbook

1. 先确认当前诉求属于 `checkpoint_inline`、`stage_acceptance` 还是 `package_release`。
2. 再确认 `review_fact_pack` 是否锁到了同一份 scope 与同一批阶段产物。
3. 若 aggregate 与 sidecar 冲突，优先修 child output contract 或聚合模板，不先改 prose。
4. 若问题看起来像阶段产物缺陷，先问一句：是不是上游 truth 自己冲突。

## Reusable Heuristics

- `aigc` 的 review 真正难点不在于“再加一个 validator”，而在于“把多阶段 handoff 审计收束成一个统一 gate”。
- 对 `aigc` 来说，checkpoint 审计比最终总评更重要，因为多数错误都发生在 handoff 处。
- 阶段 `validation-report.md` 负责阶段自证与验收，`review/*.review.json` 负责包级 route 和跨阶段裁决；两者不要混写。
- 对跨媒介工作流，最稳的维度不是按文件类型切，而是按“planning/detail/design/image/video/governance”这些责任面切。
- 对 `aigc/review` 来说，“自动修复”默认应优先理解为“自动生成返工路由和治理桥接”，不是直接改业务 canonical。

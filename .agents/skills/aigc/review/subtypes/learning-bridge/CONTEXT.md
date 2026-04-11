# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `learning-bridge/` 的经验层知识库，不是过程日志。
- 每次调用本技能时，应自动预加载本文件，用于 heuristic 提炼、里程碑类型选择与 promotion scope 收束。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| learning 只停在聊天，不落项目工件 | learning bridge | 写回 `learning-record.md` | 把 learning 独立成 review 子技能 | 项目根能读回 learning 记录 |
| 把 verdict 文本原封不动复制到 learning | carrier boundary | 只提炼 heuristic 与 promotion scope | 固定 learning 的内容边界 | learning 记录不再和 validation report 重复 |

## Repair Playbook

1. 先读上一轮 preflight / acceptance 证据。
2. 再提炼 milestone_type 与 heuristic。
3. 写回 `learning-record.md`。
4. 最后同步 `governance-state.yaml` 摘要。

## Reusable Heuristics

- learning-bridge 的价值不在于“记一遍发生了什么”，而在于“记住以后怎么少重来一次”。
- 经验沉淀应比 verdict 更抽象，但不能脱离具体 scope。

## Case Log

### Case-20260411-AIGC-REVIEW-LEARNING-SUBTYPE

- milestone_type: source_contract_change
- symptom_or_outcome: 将 `review` 的 learning 模式提升为受治理子技能。
- root_cause_or_design_decision: learning 既不等于 preflight，也不等于 acceptance；如果继续挂在父技能里，很容易被忽略或写成重复摘要。
- final_fix_or_heuristic: 将 learning-bridge 独立成子技能，固定 `learning-record.md` 为真源载体。
- prevention_or_replication_checklist:
  - [x] 已建立 `SKILL.md`
  - [x] 已建立 `CONTEXT.md`
- evidence_paths:
  - `.agents/skills/aigc/review/subtypes/learning-bridge/SKILL.md`
  - `.agents/skills/aigc/review/subtypes/learning-bridge/CONTEXT.md`
- user_feedback_or_constraint: 用户要求把 `review` 进一步细化为专项 reviewer。

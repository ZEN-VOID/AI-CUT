# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `learning-bridge/` 的经验层知识库，不是过程日志。
- 每次调用本技能时，应自动预加载本文件，用于 heuristic 提炼、里程碑类型选择与 promotion scope 收束。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| learning 只停在聊天，不落项目工件 | learning bridge | 写回 `learning-record.md` | 把 learning 独立成 review 子技能 | 项目根能读回 learning 记录 |
| 把 verdict 文本原封不动复制到 learning | carrier boundary | 只提炼 heuristic 与 promotion scope | 固定 learning 的内容边界 | learning 记录不再和 validation report 重复 |
| learning 无法回链上一轮 findings class | evidence traceability | 从 `preflight / acceptance` 提取 severity summary 与 finding classes 后再沉淀 heuristic | 固定 learning 记录包含 `source_review_mode + finding_classes` | learning 记录可回链上游 review 结论 |

## Repair Playbook

1. 先读上一轮 preflight / acceptance 证据。
2. 再提炼可复用 heuristic 与 promotion scope。
3. 写回 `learning-record.md`。
4. 最后同步 `governance-state.yaml` 摘要。

## Reusable Heuristics

- learning-bridge 的价值不在于“记一遍发生了什么”，而在于“记住以后怎么少重来一次”。
- 经验沉淀应比 verdict 更抽象，但不能脱离具体 scope。
- 对本仓库，learning 最有价值的内容通常是“哪类真源漂移最容易复发、审计器漏了什么、下次该在哪一层先设 guardrail”。

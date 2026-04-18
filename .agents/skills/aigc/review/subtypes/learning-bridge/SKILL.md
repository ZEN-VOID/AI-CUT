---
name: aigc-review-learning-bridge
description: Use when an AIGC review cycle has ended and the project needs a structured learning bridge into `learning-record.md` plus governance-state summary sync.
governance_tier: lite
---

# aigc Review Learning Bridge

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## Purpose

- `learning-bridge/` 是 `review/` 的经验沉淀子技能。
- 它负责把某轮 review 的正向或负向结果正式写入 `learning-record.md`，并同步 `governance-state.yaml` 的 learning 摘要。
- 它不重写 preflight verdict，也不重写 acceptance report。

## Carrier

- canonical carrier: `projects/aigc/<项目名>/learning-record.md`
- sync summary: `projects/aigc/<项目名>/governance-state.yaml.review_bridge.latest_learning_status`

carrier 最小字段应包含：

- `milestone_type`
- `source_review_mode`
- `finding_classes`
- `durable_heuristic`
- `promotion_decision`

## When to Use

- 一轮 review 已经结束，需要把 heuristic、promotion scope 或 blocker lesson 沉淀为项目学习记录。
- 需要为后续 `resume / query / review` 保留可回读的学习闭环。

## When Not to Use

- 任务还没被正式放行，转 `preflight-review/`。
- 还没形成验收结论，转 `acceptance-review/`。

## Workflow

1. 读取当前 `validation-report.md`、`preflight-verdict.yaml`、`governance-state.yaml` 与现有 `learning-record.md`。
2. 汇总上一轮 findings summary、severity 分布与 closure triad。
3. 提炼里程碑结论、heuristic 与 promotion scope。
4. 写回 `learning-record.md`。
5. 同步 `governance-state.yaml.review_bridge.latest_learning_status`。
6. 返回唯一下一入口或 promotion 说明。

## Hard Rules

1. `learning-record.md` 只沉淀经验，不替代 verdict carrier。
2. `governance-state.yaml` 只记摘要，不替代 `learning-record.md` 本体。
3. 没有上一轮 preflight 或 acceptance 证据时，不应伪造 learning 结论。
4. learning 结论必须能回链到上一轮 findings class 或 success pattern，不能只剩模糊感想。

## Root-Cause Execution Contract (Mandatory)

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/review/subtypes/learning-bridge/SKILL.md`
  - `.agents/skills/aigc/review/references/review-modes.md`
  - `.agents/skills/aigc/review/references/menxia-review-protocol.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/review/SKILL.md`
  - `.codex/templates/harness/office-governance-contract.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 每次调用本技能时，必须自动加载同目录 `CONTEXT.md`。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` > 根 `aigc/SKILL.md` > `review/SKILL.md` > 本 `SKILL.md` > `CONTEXT.md`。

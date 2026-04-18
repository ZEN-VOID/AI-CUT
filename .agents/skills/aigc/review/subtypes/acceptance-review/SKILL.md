---
name: aigc-review-acceptance
description: Use when an AIGC project or stage needs menxia-side acceptance, especially to update the correct stage/project `validation-report.md`, issue a closure triad, and sync governance-state.
governance_tier: lite
---

# aigc Review Acceptance

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## Purpose

- `acceptance-review/` 是 `review/` 的验收子技能。
- 它负责对项目级或阶段级产物给出 `validation-report.md` verdict，并返回唯一下一入口。
- 它不改业务真源，只负责验收与闭环。

## Carrier

- canonical carrier:
  - `project` -> `projects/aigc/<项目名>/validation-report.md`
  - `1-Planning` -> `projects/aigc/<项目名>/1-Planning/validation-report.md`
  - `2-Global` -> `projects/aigc/<项目名>/2-Global/validation-report.md`
  - `3-Detail` -> `projects/aigc/<项目名>/3-Detail/validation-report.md`
  - `4-Design` -> `projects/aigc/<项目名>/4-Design/validation-report.md`
  - `5-Image` -> `projects/aigc/<项目名>/5-Image/validation-report.md`
  - `6-Video` -> `projects/aigc/<项目名>/6-Video/validation-report.md`
- sync summary: `projects/aigc/<项目名>/governance-state.yaml.review_bridge.latest_acceptance_status`

carrier 最小字段应包含：

- `review_dimensions`
- `findings_summary`
- `findings`
- `decision_rationale`
- `evidence_status`

## When to Use

- 某阶段或整个项目已有产物，需要 PASS / revise / blocked 结论。
- 需要把 layered trace 和 closure triad 正式写回 `validation-report.md`。

## When Not to Use

- 执行前风险放行，转 `preflight-review/`。
- 经验沉淀，转 `learning-bridge/`。

## Workflow

1. 锁定 `PROJECT_ROOT` 与 review scope。
2. 读取对应 runtime 产物、`route-plan.yaml`、`governance-state.yaml` 与现有 `validation-report.md`。
3. 按 `menxia-review-protocol.md` 组装 evidence pack，先列 findings，再做 verdict。
4. 给出 verdict、layered trace 与 closure triad。
5. 写回正确 scope 的 `validation-report.md`。
6. 同步 `governance-state.yaml.review_bridge.latest_acceptance_status` 与 `resume_contract`。
7. 返回唯一下一入口。

## Hard Rules

1. scope 必须和 carrier 一一对应，不得把阶段验收误写到项目根。
2. 只给 verdict，不直接修业务真源。
3. `governance-state.yaml` 只承接摘要，不替代 `validation-report.md` 本体。
4. findings 必须按 `P0 -> P1 -> P2 -> P3` 排序，不能把高风险问题埋进概述。
5. 验收结论必须附 evidence path；没有 evidence path 的 finding 不能当 blocker 使用。

## Root-Cause Execution Contract (Mandatory)

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/review/subtypes/acceptance-review/SKILL.md`
  - `.agents/skills/aigc/review/references/review-modes.md`
  - `.agents/skills/aigc/review/references/menxia-review-protocol.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/review/SKILL.md`
  - `.codex/templates/harness/office-governance-contract.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 每次调用本技能时，必须自动加载同目录 `CONTEXT.md`。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` > 根 `aigc/SKILL.md` > `review/SKILL.md` > 本 `SKILL.md` > `CONTEXT.md`。

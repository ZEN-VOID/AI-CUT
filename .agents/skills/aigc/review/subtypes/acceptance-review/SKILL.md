---
name: aigc-review-acceptance
description: Use when an AIGC project or stage needs menxia-side acceptance, especially to update the correct stage/project `validation-report.md`, issue a closure triad, and sync governance-state.
governance_tier: lite
---

# aigc Review Acceptance

## Purpose

- `acceptance-review/` 是 `review/` 的验收子技能。
- 它负责对项目级或阶段级产物给出 `validation-report.md` verdict，并返回唯一下一入口。
- 它不改业务真源，只负责验收与闭环。

## Carrier

- canonical carrier:
  - `project` -> `projects/<项目名>/validation-report.md`
  - `1-Planning` -> `projects/<项目名>/1-Planning/validation-report.md`
  - `2-Global / 3-Detail` -> `projects/<项目名>/3-Detail/validation-report.md`
  - `4-Design` -> `projects/<项目名>/4-Design/validation-report.md`
  - `5-Image` -> `projects/<项目名>/5-Image/validation-report.md`
  - `6-Video` -> `projects/<项目名>/6-Video/validation-report.md`
- sync summary: `projects/<项目名>/governance-state.yaml.review_bridge.latest_acceptance_status`

## When to Use

- 某阶段或整个项目已有产物，需要 PASS / revise / blocked 结论。
- 需要把 layered trace 和 closure triad 正式写回 `validation-report.md`。

## When Not to Use

- 执行前风险放行，转 `preflight-review/`。
- 经验沉淀，转 `learning-bridge/`。

## Workflow

1. 锁定 `PROJECT_ROOT` 与 review scope。
2. 读取对应 runtime 产物、`route-plan.yaml`、`governance-state.yaml` 与现有 `validation-report.md`。
3. 给出 verdict、layered trace 与 closure triad。
4. 写回正确 scope 的 `validation-report.md`。
5. 同步 `governance-state.yaml.review_bridge.latest_acceptance_status` 与 `resume_contract`。
6. 返回唯一下一入口。

## Hard Rules

1. scope 必须和 carrier 一一对应，不得把阶段验收误写到项目根。
2. 只给 verdict，不直接修业务真源。
3. `governance-state.yaml` 只承接摘要，不替代 `validation-report.md` 本体。

## Root-Cause Execution Contract (Mandatory)

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/review/subtypes/acceptance-review/SKILL.md`
  - `.agents/skills/aigc/review/references/review-modes.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/review/SKILL.md`
  - `.codex/templates/harness/office-governance-contract.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 每次调用本技能时，必须自动加载同目录 `CONTEXT.md`。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` > 根 `aigc/SKILL.md` > `review/SKILL.md` > 本 `SKILL.md` > `CONTEXT.md`。

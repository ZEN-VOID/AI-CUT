---
name: aigc-review-preflight
description: Use when an AIGC project needs menxia-side preflight gating before a high-risk execution step, especially to update `preflight-verdict.yaml` and sync governance-state without touching stage business truth.
governance_tier: lite
---

# aigc Review Preflight

## Purpose

- `preflight-review/` 是 `review/` 的高风险执行前置闸门子技能。
- 它只负责 `preflight-verdict.yaml` 的门下省 verdict、阻塞风险、允许执行范围与回接入口。
- 它不执行阶段内容，也不替代 `acceptance-review` 或 `learning-bridge`。

## Carrier

- canonical carrier: `projects/aigc/<项目名>/preflight-verdict.yaml`
- sync summary: `projects/aigc/<项目名>/governance-state.yaml.review_bridge.latest_preflight_status`

## When to Use

- 任务涉及重构、批量迁移、状态修复、基础规则变更。
- 任务即将进入高风险阶段执行，但还没有门下省放行。
- 需要把 blocker、required_fixes、approved_execution_scope 写回项目根治理工件。

## When Not to Use

- 阶段或项目产物已经写完，需要验收时，转 `acceptance-review/`。
- 已完成一轮 review，需要沉淀经验时，转 `learning-bridge/`。
- 只是查状态，不做 verdict 时，转 `query/`。

## Workflow

1. 锁定 `PROJECT_ROOT` 与高风险 scope。
2. 读取 `mission-brief.yaml`、`route-plan.yaml`、`governance-state.yaml` 与现有 `preflight-verdict.yaml`。
3. 判定 `pass / blocked / revise_before_execute`。
4. 写回 `preflight-verdict.yaml`。
5. 同步 `governance-state.yaml.review_bridge.latest_preflight_status` 与 `resume_contract`。
6. 返回唯一下一入口。

## Hard Rules

1. 没有 `mission-brief.yaml` 与 `route-plan.yaml` 时，不得放行高风险执行。
2. 只写门下省 verdict，不得越权改阶段业务真源。
3. `governance-state.yaml` 只记摘要，不替代 `preflight-verdict.yaml` 本体。

## Root-Cause Execution Contract (Mandatory)

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/review/subtypes/preflight-review/SKILL.md`
  - `.agents/skills/aigc/review/references/review-modes.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/review/SKILL.md`
  - `.codex/templates/harness/office-governance-contract.md`
  - 根 `AGENTS.md`

## Context Preload (Mandatory)

- 每次调用本技能时，必须自动加载同目录 `CONTEXT.md`。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` > 根 `aigc/SKILL.md` > `review/SKILL.md` > 本 `SKILL.md` > `CONTEXT.md`。

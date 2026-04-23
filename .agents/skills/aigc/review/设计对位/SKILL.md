---
name: aigc-review-design-alignment
description: Use when `aigc/review` needs the governed child skill that audits 4-Design alignment against upstream truths and downstream handoff readiness.
governance_tier: lite
---

# review / 设计对位

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读父层 `review/SKILL.md`、`../_shared/review-root-contract.md`、`../_shared/review-child-output-contract.md`。

## Invocation Modes

- `checkpoint_inline`
- `stage_acceptance`
- `package_release`

## Parent Positioning

本 child 负责检查：

- `4-Design` 各域输出是否仍对位 `2-Global / 3-Detail`
- list/design/panel 各层 handoff 是否一致
- slot bundle 粒度的设计 continuity 是否稳定

它不负责：

- provider 级 image/video 提交

## Output Contract

- `role_id`: `design-alignment-validator`
- `dimension_report_ref`: `设计对位.md`
- 默认返工入口：
  - `4-Design/1-清单`
  - `4-Design/2-设计`
  - `4-Design/3-面板`

## Visual Map

```mermaid
flowchart TD
    A["读取 design truth + slot bundles"] --> B["检查上游对位"]
    B --> C["检查 list/design/panel handoff"]
    C --> D["输出设计对位 packet"]
```

## Thinking-Action Network

| node_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- |
| `N1-DESIGN-READ` | 锁 design truth | 读取 list/design/panel canonical refs 与 slot bundles | `design_note` | `N2` | 真源明确 |
| `N2-UPSTREAM-CHECK` | 检查上游对位 | 对照 global/detail truth 是否漂移 | `alignment_note` | `N3` | 上游对位成立 |
| `N3-HANDOFF-CHECK` | 检查 tranche handoff | 检查 list/design/panel 一致性与下游 readiness | `handoff_note` | `N4` | handoff 成立 |
| `N4-PACKET-WRITE` | 输出维度 packet | 生成 `dimension_packet + report_ref` | `packet_note` | done | 只写本维度 |

## Lite Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-DA-01` | upstream alignment | 仍对位 global/detail truth | `FAIL-DA-01` | `N2` |
| `FIELD-DA-02` | tranche handoff | list/design/panel handoff 稳定 | `FAIL-DA-02` | `N3` |
| `FIELD-DA-03` | dimension packet | 报告完整可聚合 | `FAIL-DA-03` | `N4` |

## Root-Cause Execution Contract (Mandatory)

若本维度失效，先修 `4-Design` 与 `3-Detail` 的对位关系，不要把 design drift 直接甩给 image/video 阶段。

## Completion Contract

- 已指出设计对位或 tranche handoff 问题
- 已给出回退到 `4-Design` 对应 tranche 的建议

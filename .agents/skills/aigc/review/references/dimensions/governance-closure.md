# Dimension Spec: 治理闭环

## Identity

| field | value |
| --- | --- |
| `role_id` | `governance-closure-validator` |
| `dimension` | `治理闭环` |
| `report_filename` | `治理闭环.md` |
| `default_rework_targets` | `validation-report`, `root-governance` |
| `source_owners` | `root-aigc`, `project-runtime` |

## Scope

本维度检查阶段 `validation-report.md` 是否与当前 scope 对位，`STATE.json / governance-state.yaml / source_trace / handoff_targets` 是否稳定，以及 route 是否唯一、carrier 是否没有漂移。

它不检查业务内容本身的创意优劣。

## Evidence

- 当前 scope 的 validation carrier
- 项目根 `STATE.json`
- `governance-state.yaml`
- aggregate packet 同级 fact pack
- source trace、handoff targets、rework targets

## Review Network

| node_id | objective | actions | evidence | gate |
| --- | --- | --- | --- | --- |
| `N1-GOV-READ` | 锁治理载体 | 读取 validation carriers、STATE、governance-state | `gov_note` | carrier 明确 |
| `N2-CLOSURE-CHECK` | 检查闭环 | 审 route、source trace、handoff 是否唯一 | `closure_note` | closure 成立 |
| `N3-PACKET-WRITE` | 输出维度 packet | 只写 `dimension_packet + report_ref` | `packet_note` | 可聚合 |

## Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-GC-01` | carrier alignment | 当前 scope carrier 对位稳定 | `FAIL-GC-01` | `N2-CLOSURE-CHECK` |
| `FIELD-GC-02` | route uniqueness | route、handoff、source trace 唯一 | `FAIL-GC-02` | `N2-CLOSURE-CHECK` |
| `FIELD-GC-03` | dimension packet | 报告完整可聚合 | `FAIL-GC-03` | `N3-PACKET-WRITE` |

## Failure Heuristics

- scope carrier 与 route 说法不一致时，优先回溯 validation carriers 与 route owner。
- 很多看似业务质量的问题，最后其实是 carrier、source trace 或 route 漂移。
- 先锁当前 scope 的 validation carrier，再看 `STATE / governance-state / handoff_targets` 是否一致。

## Root-Cause Rule

若本维度失效，先修 carrier、route 与 source_trace 的真源关系，不要把治理漂移误判为业务质量问题。

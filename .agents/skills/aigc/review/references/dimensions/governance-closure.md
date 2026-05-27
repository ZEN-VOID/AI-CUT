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

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否读取当前 scope 的 validation carrier、`STATE.json`、`governance-state.yaml`、fact pack 与 source trace，而不是沿用旧报告或阶段口径？ | `GATE-DIM-GC-01` | `FAIL-GC-01` | `N1-GOV-READ` | `gov_note` 记录 carrier 路径、scope_ref、stage/checkpoint、fact pack ref 与缺失项。 |
| validation report 是否与当前 mode、stage/checkpoint、scope_ref 对位，且没有把旧集、旧阶段或历史 rerun 结果当成当前闭环证据？ | `GATE-DIM-GC-02` | `FAIL-GC-01` | `N2-CLOSURE-CHECK` | `closure_note` 标明不对位字段、冲突 carrier、时间/版本线索和影响范围。 |
| `STATE.json`、`governance-state.yaml`、aggregate fact pack、source trace 与 handoff/rework targets 是否互相一致？ | `GATE-DIM-GC-03` | `FAIL-GC-01` | `N2-CLOSURE-CHECK` | 维度报告列出冲突载体、冲突字段、权属 owner 和建议修复入口。 |
| route、handoff target、source owner 与 rework target 是否唯一可执行，没有同时指向多个阶段、空目标或循环目标？ | `GATE-DIM-GC-04` | `FAIL-GC-02` | `N2-CLOSURE-CHECK` | `closure_note` 记录候选 route、冲突理由、阻断等级和唯一化建议。 |
| source trace 是否能解释每个 blocking finding 的来源层和返工层，避免把治理断链包装成业务内容质量问题？ | `GATE-DIM-GC-05` | `FAIL-GC-02` | `N2-CLOSURE-CHECK` | `dimension_packet.issues[*].source_layer_owner`、`blocking_scope` 与 evidence refs 完整。 |
| 若存在 provider 或下游 handoff 阻断，治理侧是否记录可恢复的 resume / repair bridge，而不是只给 prose summary？ | `GATE-DIM-GC-06` | `FAIL-GC-02` | `N2-CLOSURE-CHECK` | 维度报告包含 repair sidecar 预期字段、resume bridge 缺口或 handoff 修复入口。 |
| 本维度是否只输出治理闭环 sidecar，不独立写最终 aggregate route，也不直接修改阶段业务真源？ | `GATE-DIM-GC-07` | `FAIL-GC-03` | `N3-PACKET-WRITE` | `dimension_packet`、`dimension_runtime`、`report_ref` 可聚合，且无越权 route/status 写入。 |

## Failure Heuristics

- scope carrier 与 route 说法不一致时，优先回溯 validation carriers 与 route owner。
- 很多看似业务质量的问题，最后其实是 carrier、source trace 或 route 漂移。
- 先锁当前 scope 的 validation carrier，再看 `STATE / governance-state / handoff_targets` 是否一致。

## Root-Cause Rule

若本维度失效，先修 carrier、route 与 source_trace 的真源关系，不要把治理漂移误判为业务质量问题。

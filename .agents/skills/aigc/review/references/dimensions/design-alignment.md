# Dimension Spec: 设计对位

## Identity

| field | value |
| --- | --- |
| `role_id` | `design-alignment-validator` |
| `dimension` | `设计对位` |
| `report_filename` | `设计对位.md` |
| `default_rework_targets` | `5-设计/场景`, `5-设计/角色`, `5-设计/道具` |
| `source_owners` | `4-分组`, `5-设计` |

## Scope

本维度检查 `5-设计` 各域输出是否仍对位 `4-分组`，并确认清单、设计、面板提示词或生成层 handoff 没有断裂。重点是 slot bundle 粒度的设计 continuity。

它不检查 image/video provider 提交本身。

## Evidence

- `4-分组` 分镜组 truth
- `5-设计` 场景、角色、道具清单与设计 truth
- 设计生成、面板提示词或下游 handoff refs
- `review_fact_pack.required_refs`

## Review Network

| node_id | objective | actions | evidence | gate |
| --- | --- | --- | --- | --- |
| `N1-DESIGN-READ` | 锁 design truth | 读取 list/design/panel canonical refs 与 slot bundles | `design_note` | 真源明确 |
| `N2-UPSTREAM-CHECK` | 检查上游对位 | 对照分组 truth 是否漂移 | `alignment_note` | 上游对位成立 |
| `N3-HANDOFF-CHECK` | 检查 tranche handoff | 检查 list/design/panel 一致性与下游 readiness | `handoff_note` | handoff 成立 |
| `N4-PACKET-WRITE` | 输出维度 packet | 只写 `dimension_packet + report_ref` | `packet_note` | 可聚合 |

## Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-DA-01` | upstream alignment | 仍对位分组 truth | `FAIL-DA-01` | `N2-UPSTREAM-CHECK` |
| `FIELD-DA-02` | tranche handoff | list/design/panel handoff 稳定 | `FAIL-DA-02` | `N3-HANDOFF-CHECK` |
| `FIELD-DA-03` | dimension packet | 报告完整可聚合 | `FAIL-DA-03` | `N4-PACKET-WRITE` |

## Failure Heuristics

- 设计输出局部好看但整体脱离分组 truth 时，优先回溯 `5-设计` 与上游 truth 的对位关系。
- `5-设计` 最怕的不是局部 prompt 不好，而是整体对位失真。
- 先锁 `4-分组` 和 `5-设计` 真源，再判问题在 list、design 还是 panel 层。

## Root-Cause Rule

若本维度失效，先修 `5-设计` 与 `4-分组` 的对位关系，不要把 design drift 直接甩给 image/video 阶段。

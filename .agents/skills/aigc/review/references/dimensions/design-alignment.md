# Dimension Spec: 设计对位

## Identity

| field | value |
| --- | --- |
| `role_id` | `design-alignment-validator` |
| `dimension` | `设计对位` |
| `report_filename` | `设计对位.md` |
| `default_rework_targets` | `3-主体/场景`, `3-主体/角色`, `3-主体/道具` |
| `source_owners` | `3-主体`, `8-分组` |

## Scope

本维度检查 `3-主体` 主体注册表、三域清单、设计和生成资产是否对位 `1-分集` source anchors、`2-美学` 风格协议以及后置 `8-分组` 的只读主体引用，并确认下游 handoff 没有断裂。重点是 subject registry 与 slot bundle 粒度的设计 continuity。

它不检查 image/video provider 提交本身。

## Evidence

- `3-主体/subject-registry.yaml` 与 `主体注册表.md`
- `3-主体` 场景、角色、道具清单与设计 truth
- `8-分组` 分镜组 YAML 对 registry 的只读引用
- 设计生成、面板提示词或下游 handoff refs
- `review_fact_pack.required_refs`

## Review Network

| node_id | objective | actions | evidence | gate |
| --- | --- | --- | --- | --- |
| `N1-DESIGN-READ` | 锁 design truth | 读取 list/design/panel canonical refs 与 slot bundles | `design_note` | 真源明确 |
| `N2-UPSTREAM-CHECK` | 检查上游对位 | 对照 subject registry、source anchors 与后置分组引用是否漂移 | `alignment_note` | 上游对位成立 |
| `N3-HANDOFF-CHECK` | 检查 tranche handoff | 检查 list/design/panel 一致性与下游 readiness | `handoff_note` | handoff 成立 |
| `N4-PACKET-WRITE` | 输出维度 packet | 只写 `dimension_packet + report_ref` | `packet_note` | 可聚合 |

## Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-DA-01` | upstream alignment | 仍对位 subject registry、source anchors 与后置分组引用 | `FAIL-DA-01` | `N2-UPSTREAM-CHECK` |
| `FIELD-DA-02` | tranche handoff | list/design/panel handoff 稳定 | `FAIL-DA-02` | `N3-HANDOFF-CHECK` |
| `FIELD-DA-03` | dimension packet | 报告完整可聚合 | `FAIL-DA-03` | `N4-PACKET-WRITE` |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否已读取同一 `review_fact_pack` 中的 `3-主体/subject-registry.yaml`、三域 canonical refs 与 `8-分组` 只读引用，而不是凭文件存在或旧路径推断设计状态？ | `GATE-DIM-DA-01` | `FAIL-DA-01` | `N1-DESIGN-READ` | `design_note` 记录读取的 registry truth、design truth、group reference、slot bundle refs 与缺失项。 |
| 场景、角色、道具清单和设计是否仍对位 subject registry 的 ID/name、source anchors、组边界与叙事用途，没有新增、漏删或错并关键对象？ | `GATE-DIM-DA-02` | `FAIL-DA-01` | `N2-UPSTREAM-CHECK` | `alignment_note` 标明漂移对象、对应 registry/source anchor、后置分组引用和 `source_layer_owner`。 |
| 设计稿是否保留 source anchors 与 `2-美学` 风格协议的视觉/叙事约束，而没有把局部审美优化、研究补充或 provider 偏好变成第二真源？ | `GATE-DIM-DA-03` | `FAIL-DA-01` | `N2-UPSTREAM-CHECK` | 维度报告列出被覆盖的 upstream constraint、设计字段和建议回修阶段。 |
| list -> design -> panel / generation handoff 是否主体 ID、名称、别名、路径、slot bundle 与 source trace 一致？ | `GATE-DIM-DA-04` | `FAIL-DA-02` | `N3-HANDOFF-CHECK` | `handoff_note` 记录不一致的 tranche、slot key、文件路径和下游阻断范围。 |
| 下游 handoff 是否具备可消费的场景/角色/道具设计包，而不是只有清单、空模板、未绑定 prompt 或缺图状态？ | `GATE-DIM-DA-05` | `FAIL-DA-02` | `N3-HANDOFF-CHECK` | 维度报告标出缺失 bundle、影响的 image/video handoff 和默认返工目标。 |
| 对位问题是否被归因到 list、design、panel/generation 或 upstream group，而不是笼统写成“设计质量不足”？ | `GATE-DIM-DA-06` | `FAIL-DA-03` | `N4-PACKET-WRITE` | `dimension_packet.issues[*].source_layer_owner`、`default_rework_targets` 与 evidence refs 完整。 |
| 本维度是否只写 `dimension_packet + report_ref`，没有独立写最终 `review_status`、`routing_decision` 或直接改业务文件？ | `GATE-DIM-DA-07` | `FAIL-DA-03` | `N4-PACKET-WRITE` | `dimension_runtime`、`report_ref` 和父 aggregate 可聚合字段存在，且无越权字段。 |

## Failure Heuristics

- 设计输出局部好看但整体脱离 registry truth 或后置分组引用时，优先回溯 `3-主体` 与上游 truth 的对位关系。
- `3-主体` 最怕的不是局部 prompt 不好，而是整体对位失真。
- 先锁 `3-主体/subject-registry.yaml`、三域输出和 `8-分组` 只读引用，再判问题在 registry、list、design 还是 panel 层。

## Root-Cause Rule

若本维度失效，先修 `3-主体` registry/list/design 与 `8-分组` 只读引用的对位关系，不要把 design drift 直接甩给 image/video 阶段。

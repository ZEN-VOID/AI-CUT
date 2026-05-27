# Dimension Spec: 分镜执行连续性

## Identity

| field | value |
| --- | --- |
| `role_id` | `detail-execution-validator` |
| `dimension` | `分镜执行连续性` |
| `report_filename` | `分镜执行连续性.md` |
| `default_rework_targets` | `2-编导`, `3-摄影`, `4-分组` |
| `source_owners` | `1-分集`, `2-编导`, `3-摄影` |

## Scope

本维度检查 `2-编导 / 3-摄影 / 4-分组` 是否形成稳定可消费的导演与镜头事实，重点关注画面句子、分镜明细、分镜组 continuity 与 handoff readiness。

它不检查设计 prompt、引用绑定、图像 provider pack 或视频 provider pack。

## Evidence

- `2-编导` 编导稿与 validator evidence
- `3-摄影` 摄影稿与分镜明细注入证据
- `4-分组` 分镜组稿与 handoff carrier
- `review_fact_pack.required_refs`

## Review Network

| node_id | objective | actions | evidence | gate |
| --- | --- | --- | --- | --- |
| `N1-DETAIL-READ` | 锁分镜链路真源 | 读取编导、摄影、分组真源与 validator evidence | `detail_note` | root 明确 |
| `N2-CONTINUITY-CHECK` | 检查组镜连续性 | 核对组、镜、时间、主体、构图与运镜连续性 | `continuity_note` | continuity 成立 |
| `N3-HANDOFF-CHECK` | 检查 handoff readiness | 判断是否可安全交给 design/image/video | `handoff_note` | handoff 成立 |
| `N4-PACKET-WRITE` | 输出维度 packet | 只写 `dimension_packet + report_ref` | `packet_note` | 可聚合 |

## Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-DE-01` | detail continuity | 组镜连续性稳定 | `FAIL-DE-01` | `N2-CONTINUITY-CHECK` |
| `FIELD-DE-02` | handoff readiness | 可安全交给下游阶段 | `FAIL-DE-02` | `N3-HANDOFF-CHECK` |
| `FIELD-DE-03` | dimension packet | 报告完整可聚合 | `FAIL-DE-03` | `N4-PACKET-WRITE` |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否锁定同一 scope 的 `2-编导`、`3-摄影`、`4-分组` 真源和 validator evidence，而不是混用旧集、旧阶段或派生摘要？ | `GATE-DIM-DE-01` | `FAIL-DE-01` | `N1-DETAIL-READ` | `detail_note` 记录编导稿、摄影稿、分组稿、validator evidence 与缺失 required refs。 |
| 编导画面句子、摄影分镜明细与分组正文/YAML 是否逐层可追溯，镜头/组编号、source span、主体和动作没有错位？ | `GATE-DIM-DE-02` | `FAIL-DE-01` | `N2-CONTINUITY-CHECK` | `continuity_note` 标明断裂链路、涉及镜头或分组、上游证据和 source owner。 |
| 分组内部的组、镜、时间、主体、构图、运镜、入出点与 handoff anchor 是否连续，没有吞 beat、重复镜头、越组外溢或 atomic unit 截断？ | `GATE-DIM-DE-03` | `FAIL-DE-01` | `N2-CONTINUITY-CHECK` | 维度报告列出 continuity break、影响范围、blocking scope 和建议返工节点。 |
| 显式时长、对白/动作负载、镜头节奏与 AIGC 视频可执行性是否一致，没有把不可消费的节奏问题推给设计或视频阶段？ | `GATE-DIM-DE-04` | `FAIL-DE-01` | `N2-CONTINUITY-CHECK` | `continuity_note` 记录时长冲突、对白/动作证据、节奏风险和责任阶段。 |
| `4-分组` 是否已经为设计、图像、视频提供稳定 handoff carrier，包括组正文、YAML、统计、连接件边界与风险项？ | `GATE-DIM-DE-05` | `FAIL-DE-02` | `N3-HANDOFF-CHECK` | `handoff_note` 记录缺失 carrier、不可消费字段、下游阻断路径和默认返工目标。 |
| 分镜链路问题是否明确归因到 `2-编导`、`3-摄影` 或 `4-分组`，而不是误判为 design/image/video provider 缺陷？ | `GATE-DIM-DE-06` | `FAIL-DE-02` | `N3-HANDOFF-CHECK` | `dimension_packet.issues[*].source_layer_owner` 与 `default_rework_targets` 指向正确阶段。 |
| 本维度是否只输出可聚合 sidecar，并保留 `dimension_runtime`、证据 refs、严重度和 blocking scope？ | `GATE-DIM-DE-07` | `FAIL-DE-03` | `N4-PACKET-WRITE` | `dimension_packet` 包含 issue evidence、severity_counts、report_ref 和 runtime spec 证据。 |

## Failure Heuristics

- 分镜链路字段看似完整但下游仍无法消费时，优先追溯 `2-编导 / 3-摄影 / 4-分组` validator 与 handoff refs。
- 本维度不只看“有没有文件”，而要看这些文件是否真能支撑下游 handoff。
- 先看 `第N集.json` 与 validator evidence，再判是字段缺口还是 continuity 断裂。

## Root-Cause Rule

若本维度失效，先修 `2-编导 / 3-摄影 / 4-分组` 的结构完整性与 handoff readiness，不要把分镜链路问题伪装成 design/image/video 问题。

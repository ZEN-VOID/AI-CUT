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

## Failure Heuristics

- 分镜链路字段看似完整但下游仍无法消费时，优先追溯 `2-编导 / 3-摄影 / 4-分组` validator 与 handoff refs。
- 本维度不只看“有没有文件”，而要看这些文件是否真能支撑下游 handoff。
- 先看 `第N集.json` 与 validator evidence，再判是字段缺口还是 continuity 断裂。

## Root-Cause Rule

若本维度失效，先修 `2-编导 / 3-摄影 / 4-分组` 的结构完整性与 handoff readiness，不要把分镜链路问题伪装成 design/image/video 问题。

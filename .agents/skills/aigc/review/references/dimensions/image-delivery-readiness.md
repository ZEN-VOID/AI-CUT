# Dimension Spec: 图像交付就绪

## Identity

| field | value |
| --- | --- |
| `role_id` | `image-delivery-validator` |
| `dimension` | `图像交付就绪` |
| `report_filename` | `图像交付就绪.md` |
| `default_rework_targets` | `6-图像/A-分镜画面`, `6-图像/B-分镜故事板` |
| `source_owners` | `4-分组`, `5-设计`, `6-图像` |

## Scope

本维度检查 `6-图像/A-分镜画面` 请求对象是否稳定、`6-图像/B-分镜故事板` 是否可信、图像 handoff pack 是否完整，以及主体 continuity 是否可追溯。

它不检查视频 motion 交付。

## Evidence

- 图像请求 JSON、prompt 或 request carrier
- 分镜画面与故事板输出 refs
- 引用绑定、subject continuity 与 provider handoff pack
- `review_fact_pack.required_refs`

## Review Network

| node_id | objective | actions | evidence | gate |
| --- | --- | --- | --- | --- |
| `N1-IMAGE-READ` | 锁图像链路输出 | 读取 request、binding、handoff refs | `image_note` | scope 明确 |
| `N2-CONTINUITY-CHECK` | 检查 continuity 与 binding | 审 request/binding 是否稳定 | `continuity_note` | continuity 成立 |
| `N3-PROVIDER-CHECK` | 检查 handoff pack | 审 submit-plan、brief、output root | `provider_note` | provider pack 成立 |
| `N4-PACKET-WRITE` | 输出维度 packet | 只写 `dimension_packet + report_ref` | `packet_note` | 可聚合 |

## Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-ID-01` | request/binding continuity | continuity 与 binding 稳定 | `FAIL-ID-01` | `N2-CONTINUITY-CHECK` |
| `FIELD-ID-02` | provider pack | provider handoff 完整 | `FAIL-ID-02` | `N3-PROVIDER-CHECK` |
| `FIELD-ID-03` | dimension packet | 报告完整可聚合 | `FAIL-ID-03` | `N4-PACKET-WRITE` |

## Failure Heuristics

- 图像链路能生成计划但不可信交付时，回溯 request、binding、handoff 三段。
- `6-图像` 的 review 关键不在“有没有图像资产”，而在“这份画面/故事板是不是可信可交付”。
- 先锁 request、binding、handoff 三段，再判问题在 continuity、binding 还是 provider pack。

## Root-Cause Rule

若本维度失效，先修 `6-图像` 的分镜画面、故事板与 handoff pack，不要只看最终资产是否存在。

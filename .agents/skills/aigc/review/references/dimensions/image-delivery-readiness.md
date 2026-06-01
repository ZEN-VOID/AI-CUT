# Dimension Spec: 图像交付就绪

## Identity

| field | value |
| --- | --- |
| `role_id` | `image-delivery-validator` |
| `dimension` | `图像交付就绪` |
| `report_filename` | `图像交付就绪.md` |
| `default_rework_targets` | `7-图像/A-分镜画面`, `7-图像/B-分镜故事板` |
| `source_owners` | `5-分组`, `6-设计`, `7-图像` |

## Scope

本维度检查 `7-图像/A-分镜画面` 请求对象是否稳定、`7-图像/B-分镜故事板` 是否可信、图像 handoff pack 是否完整，以及主体 continuity 是否可追溯。

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

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否锁定同一 `review_fact_pack` 下的 `7-图像/A-分镜画面`、`7-图像/B-分镜故事板`、引用绑定与 provider handoff refs，而不是凭最终图片是否存在判断交付就绪？ | `GATE-DIM-ID-01` | `FAIL-ID-01` | `N1-IMAGE-READ` | `image_note` 记录 request carrier、storyboard output、binding refs、handoff refs 与缺失 required refs。 |
| `A-分镜画面` 请求对象是否能回指 `5-分组` 与 `6-设计`，frame landing、prompt package、reference slots 与 subject continuity 没有断链？ | `GATE-DIM-ID-02` | `FAIL-ID-01` | `N2-CONTINUITY-CHECK` | `continuity_note` 标明断链 frame/group、缺失设计或主体参照、影响的 image request。 |
| `B-分镜故事板` 是否可信表达组正文与 YAML 信息，panel/frame units、source span、场景图风格锁和主体参照没有错位？ | `GATE-DIM-ID-03` | `FAIL-ID-01` | `N2-CONTINUITY-CHECK` | 维度报告列出错位 panel、源组证据、storyboard reference 与 blocking scope。 |
| 引用绑定是否只接受真实可见图片路径或已上传资产，多视图/场景图/上一帧连续性绑定可追溯，且没有把 JSON、缺图说明或 pending marker 当成可用图片？ | `GATE-DIM-ID-04` | `FAIL-ID-01` | `N2-CONTINUITY-CHECK` | `continuity_note` 记录 slot key、候选路径、缺图/多候选状态和下游阻断范围。 |
| provider handoff pack 是否包含可消费的 submit plan、brief/prompt package、output root、manifest/status，并显式区分 generated、skipped、failed？ | `GATE-DIM-ID-05` | `FAIL-ID-02` | `N3-PROVIDER-CHECK` | `provider_note` 记录 handoff pack 路径、生成状态、output root、防覆盖或跳过原因。 |
| 图像交付问题是否被归因到 `7-图像/A-分镜画面`、`7-图像/B-分镜故事板`、`6-设计` 或 `5-分组` 的 source owner，而不是笼统写成“图片不稳定”？ | `GATE-DIM-ID-06` | `FAIL-ID-03` | `N4-PACKET-WRITE` | `dimension_packet.issues[*].source_layer_owner`、`default_rework_targets` 与 evidence refs 完整。 |
| 本维度是否只输出可聚合 `dimension_packet + report_ref`，不独立写最终 route/status，也不反向修改图像、设计或分组业务文件？ | `GATE-DIM-ID-07` | `FAIL-ID-03` | `N4-PACKET-WRITE` | `dimension_runtime`、`report_ref`、severity_counts、blocking_scope 存在，且无越权字段。 |

## Failure Heuristics

- 图像链路能生成计划但不可信交付时，回溯 request、binding、handoff 三段。
- `7-图像` 的 review 关键不在“有没有图像资产”，而在“这份画面/故事板是不是可信可交付”。
- 先锁 request、binding、handoff 三段，再判问题在 continuity、binding 还是 provider pack。

## Root-Cause Rule

若本维度失效，先修 `7-图像` 的分镜画面、故事板与 handoff pack，不要只看最终资产是否存在。

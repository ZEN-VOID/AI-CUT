# Dimension Spec: 视频交付就绪

## Identity

| field | value |
| --- | --- |
| `role_id` | `video-delivery-validator` |
| `dimension` | `视频交付就绪` |
| `report_filename` | `视频交付就绪.md` |
| `default_rework_targets` | `7-视频/B-分镜故事板参照`, `7-视频/C-主体参照`, `7-视频/D-主板混合参照` |
| `source_owners` | `4-分组`, `5-设计`, `6-图像`, `7-视频` |

## Scope

本维度检查 `7-视频/B-分镜故事板参照` 请求对象是否稳定、`7-视频/C-主体参照` 是否可信、`7-视频/D-主板混合参照` 是否同时满足故事板总参照与主体参照绑定，provider handoff pack 是否完整，以及 motion、duration、continuity readiness 是否达到交付门。

它不检查图像 provider 交付。

## Evidence

- 视频请求、storyboard reference 与 subject reference refs
- motion、duration、reference continuity 证据
- provider submit-plan、brief、output root
- `review_fact_pack.required_refs`

## Review Network

| node_id | objective | actions | evidence | gate |
| --- | --- | --- | --- | --- |
| `N1-VIDEO-READ` | 锁视频链路输出 | 读取 request、binding、handoff refs | `video_note` | scope 明确 |
| `N2-MOTION-CHECK` | 检查 continuity 与 motion readiness | 审 motion、duration、reference continuity | `motion_note` | readiness 成立 |
| `N3-PROVIDER-CHECK` | 检查 handoff pack | 审 submit-plan、brief、output root | `provider_note` | provider pack 成立 |
| `N4-PACKET-WRITE` | 输出维度 packet | 只写 `dimension_packet + report_ref` | `packet_note` | 可聚合 |

## Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-VD-01` | motion readiness | motion/duration/reference readiness 稳定 | `FAIL-VD-01` | `N2-MOTION-CHECK` |
| `FIELD-VD-02` | provider pack | provider handoff 完整 | `FAIL-VD-02` | `N3-PROVIDER-CHECK` |
| `FIELD-VD-03` | dimension packet | 报告完整可聚合 | `FAIL-VD-03` | `N4-PACKET-WRITE` |

## Failure Heuristics

- 视频请求可写但交付风险仍高时，回溯 request、binding、handoff 三段。
- `7-视频` 的 review 要比图像多看一层 motion/duration readiness。
- 先锁 request、binding、handoff 三段，再判问题在 motion/duration 还是 provider pack。

## Root-Cause Rule

若本维度失效，先修 `7-视频` 的 motion、duration、reference readiness 与 provider pack，不要把问题压成泛化“视频还不稳”。

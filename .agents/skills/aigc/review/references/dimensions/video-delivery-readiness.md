# Dimension Spec: 视频交付就绪

## Identity

| field | value |
| --- | --- |
| `role_id` | `video-delivery-validator` |
| `dimension` | `视频交付就绪` |
| `report_filename` | `视频交付就绪.md` |
| `default_rework_targets` | `8-视频/B-分镜故事板参照`, `8-视频/C-主体参照`, `8-视频/D-主板混合参照`, `9-审片` |
| `source_owners` | `5-分组`, `6-设计`, `7-图像`, `8-视频`, `9-审片` |

## Scope

本维度检查 `8-视频/B-分镜故事板参照` 请求对象是否稳定、`8-视频/C-主体参照` 是否可信、`8-视频/D-主板混合参照` 是否同时满足故事板总参照与主体参照绑定，provider handoff pack 是否完整，`9-审片` 是否形成可执行缺陷和修复路由，以及 motion、duration、continuity readiness 是否达到交付门。

它不检查图像 provider 交付。

## Evidence

- 视频请求、storyboard reference 与 subject reference refs
- motion、duration、reference continuity 证据
- provider submit-plan、brief、output root
- `9-审片` 审查报告、缺陷清单、修复路由
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

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否锁定同一 `review_fact_pack` 下的 `8-视频/B-分镜故事板参照`、`C-主体参照`、`D-主板混合参照` 与 provider handoff refs，而不是凭远端任务或本地视频文件存在判断交付就绪？ | `GATE-DIM-VD-01` | `FAIL-VD-01` | `N1-VIDEO-READ` | `video_note` 记录视频请求、storyboard refs、subject refs、hybrid refs、handoff refs 与缺失项。 |
| `B-分镜故事板参照` 是否保持组正文、storyboard image binding、duration hint 与首帧/总参照边界稳定，没有把缺图说明或本地 marker 写入远端 prompt？ | `GATE-DIM-VD-02` | `FAIL-VD-01` | `N2-MOTION-CHECK` | `motion_note` 标明 storyboard binding、duration 证据、缺图或 prompt 污染风险。 |
| `C-主体参照` 是否以 YAML 主体为基准，主体槽位、reference order、9 图预算、混合主体互斥和本地路径禁区均可追溯？ | `GATE-DIM-VD-03` | `FAIL-VD-01` | `N2-MOTION-CHECK` | 维度报告列出主体 slot、reference asset、预算状态、缺失/排除原因。 |
| `D-主板混合参照` 是否同时满足故事板总参照与主体参照绑定，generation slots、asset uploads 与 source-first prompt 没有错层？ | `GATE-DIM-VD-04` | `FAIL-VD-01` | `N2-MOTION-CHECK` | `motion_note` 记录 hybrid binding、slot phase、asset_uploads/generation_slots 分层证据。 |
| motion、duration、reference continuity 是否达到视频 provider 可执行门槛，没有把镜头运动、时长、音频预期或连续性风险压成泛化“视频待生成”？ | `GATE-DIM-VD-05` | `FAIL-VD-01` | `N2-MOTION-CHECK` | 维度报告列出 motion/duration/audio/continuity 风险、影响组和 blocking scope。 |
| provider handoff pack 是否包含官方执行路径、submit plan、brief/final YAML、queue/session、output root、下载或失败证据，并能区分未提交、提交中、失败和已交付？ | `GATE-DIM-VD-06` | `FAIL-VD-02` | `N3-PROVIDER-CHECK` | `provider_note` 记录 handoff pack、远端任务证据、output root、音轨/下载状态和缺失项。 |
| 视频交付问题是否归因到 `8-视频` 的 B/C/D 路线、`9-审片` 审查闭环、`7-图像` 参照资产、`6-设计` 主体资产或 `5-分组` 源文本，而不是笼统写成 provider 不稳？ | `GATE-DIM-VD-07` | `FAIL-VD-03` | `N4-PACKET-WRITE` | `dimension_packet.issues[*].source_layer_owner`、default_rework_targets 与 evidence refs 完整。 |
| 本维度是否只输出可聚合 sidecar，不独立写最终 route/status，也不直接改视频请求、provider 任务或上游业务文件？ | `GATE-DIM-VD-08` | `FAIL-VD-03` | `N4-PACKET-WRITE` | `dimension_runtime`、report_ref、severity_counts、critical_issues、blocking_scope 存在，且无越权字段。 |

## Failure Heuristics

- 视频请求可写但交付风险仍高时，回溯 request、binding、handoff 三段。
- `8-视频` 的 review 要比图像多看一层 motion/duration readiness；`9-审片` 还要看实际视频缺陷是否回到可执行 repair route。
- 先锁 request、binding、handoff 三段，再判问题在 motion/duration 还是 provider pack。

## Root-Cause Rule

若本维度失效，先修 `8-视频` 的 motion、duration、reference readiness、provider pack 与 `9-审片` 修复路由，不要把问题压成泛化“视频还不稳”。

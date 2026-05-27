# Dimension Spec: 规划与种子兑现

## Identity

| field | value |
| --- | --- |
| `role_id` | `planning-seed-validator` |
| `dimension` | `规划与种子兑现` |
| `report_filename` | `规划与种子兑现.md` |
| `default_rework_targets` | `0-初始化`, `1-分集`, `2-编导` |
| `source_owners` | `0-初始化`, `1-分集` |

## Scope

本维度检查 `0-初始化 -> 1-分集 -> 2-编导` 的 seed 与 obligation 是否连续，尤其是 `north_star / init_handoff / 分集稿 / 编导稿` 是否在正确阶段被继承和兑现。

它不检查单镜构图语法、设计产物、图像 provider 交付或视频 provider 交付。

## Evidence

- 项目根 `0-初始化/north_star.yaml`
- 初始化 handoff carrier
- `1-分集` 分集稿与 validation carrier
- `2-编导` 编导稿与 validation carrier
- `review_fact_pack.required_refs`

## Review Network

| node_id | objective | actions | evidence | gate |
| --- | --- | --- | --- | --- |
| `N1-SEED-READ` | 锁上游真源 | 读取初始化、分集、编导 refs | `seed_note` | 真源明确 |
| `N2-HANDOFF-CHECK` | 检查 handoff obligations | 核对 `north_star / init_handoff / 分集稿 / 编导稿` | `handoff_note` | obligations 可追溯 |
| `N3-CONTINUITY-CHECK` | 检查 seed 连续性 | 对照初始化、分集、编导是否断链 | `continuity_note` | continuity 成立 |
| `N4-PACKET-WRITE` | 输出维度 packet | 只写 `dimension_packet + report_ref` | `packet_note` | 可聚合 |

## Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-PS-01` | handoff obligations | handoff 引用完整可追溯 | `FAIL-PS-01` | `N2-HANDOFF-CHECK` |
| `FIELD-PS-02` | seed continuity | 初始化、分集、编导没有断链 | `FAIL-PS-02` | `N3-CONTINUITY-CHECK` |
| `FIELD-PS-03` | dimension packet | 报告完整可聚合 | `FAIL-PS-03` | `N4-PACKET-WRITE` |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否锁定同一 `review_fact_pack` 下的 `north_star`、初始化 handoff、`1-分集` 与 `2-编导` canonical refs，而不是混读旧阶段、旧集或派生摘要？ | `GATE-DIM-PS-01` | `FAIL-PS-01` | `N1-SEED-READ` | `seed_note` 记录 north star、init handoff、分集稿、编导稿、validation carrier 与缺失项。 |
| 初始化阶段输出的 north star、长期约束、项目口味和 handoff obligations 是否在 `1-分集` 中被显式继承，没有在分集切分时丢失或改写？ | `GATE-DIM-PS-02` | `FAIL-PS-01` | `N2-HANDOFF-CHECK` | `handoff_note` 标明丢失 obligation、对应初始化字段、分集落点和 source owner。 |
| `1-分集` 是否把 episode scope、集标、源文范围、保真边界和下游义务交给 `2-编导`，没有把章节、旧 P 标记或摘要当成当前集真源？ | `GATE-DIM-PS-03` | `FAIL-PS-01` | `N2-HANDOFF-CHECK` | 维度报告列出 scope_ref、集标证据、分集 handoff carrier 和不对位字段。 |
| `2-编导` 是否真实消费初始化与分集 seed，将核心 obligation 转译为画面、声音、对白或结构约束，而不是生成脱离上游种子的独立编导稿？ | `GATE-DIM-PS-04` | `FAIL-PS-02` | `N3-CONTINUITY-CHECK` | `continuity_note` 记录被消费/遗漏的 seed、编导字段证据和断链位置。 |
| 若发现 seed 漂移或 obligation 缺口，是否归因到 `0-初始化`、`1-分集` 或 `2-编导` 的具体 source owner，而不是把问题推给设计、图像或视频阶段？ | `GATE-DIM-PS-05` | `FAIL-PS-02` | `N3-CONTINUITY-CHECK` | `dimension_packet.issues[*].source_layer_owner`、blocking_scope 与默认返工目标完整。 |
| 本维度是否严格排除单镜构图、设计、图像 provider、视频 provider 等非 planning seed 范围，避免扩大审计范围污染 aggregate？ | `GATE-DIM-PS-06` | `FAIL-PS-03` | `N4-PACKET-WRITE` | 维度报告说明未覆盖范围、实际检查范围和未越权 evidence。 |
| 本维度是否只输出可聚合 `dimension_packet + report_ref`，保留 `dimension_runtime`、severity、critical issues 与 evidence refs，而不独立写最终 route/status？ | `GATE-DIM-PS-07` | `FAIL-PS-03` | `N4-PACKET-WRITE` | `dimension_packet` 包含聚合字段、runtime spec 证据、report_ref，且无越权字段。 |

## Failure Heuristics

- 编导稿存在但失去初始化或分集 handoff 痕迹时，先回退到 `1-分集 / 2-编导` 重建 handoff。
- 最隐蔽的断链通常不发生在设计或出图，而是发生在 planning/detail 之间的 seed 漂移。
- 判断时先锁 `north_star -> planning -> episode_root -> 第N集.json`，再判 seed 是否被下游真实消费，而不是只看文件是否存在。

## Root-Cause Rule

若本维度失效，先回看 `north_star / init_handoff / 分集稿 / 编导稿` 的 handoff 链，不要先改下游 prose、设计或 provider pack。

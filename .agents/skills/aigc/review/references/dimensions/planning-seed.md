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

## Failure Heuristics

- 编导稿存在但失去初始化或分集 handoff 痕迹时，先回退到 `1-分集 / 2-编导` 重建 handoff。
- 最隐蔽的断链通常不发生在设计或出图，而是发生在 planning/detail 之间的 seed 漂移。
- 判断时先锁 `north_star -> planning -> episode_root -> 第N集.json`，再判 seed 是否被下游真实消费，而不是只看文件是否存在。

## Root-Cause Rule

若本维度失效，先回看 `north_star / init_handoff / 分集稿 / 编导稿` 的 handoff 链，不要先改下游 prose、设计或 provider pack。

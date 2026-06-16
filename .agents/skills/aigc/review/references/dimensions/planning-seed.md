# Dimension Spec: 规划与种子兑现

## Identity

| field | value |
| --- | --- |
| `role_id` | `planning-seed-validator` |
| `dimension` | `规划与种子兑现` |
| `report_filename` | `规划与种子兑现.md` |
| `default_rework_targets` | `0-初始化`, `1-分集`, `2-美学`, `3-主体`, `4-编剧` |
| `source_owners` | `0-初始化`, `1-分集`, `2-美学`, `3-主体` |

## Scope

本维度检查 `0-初始化 -> 1-分集 -> 2-美学 -> 3-主体 -> 4-编剧` 的 seed 与 obligation 是否连续，尤其是 `MEMORY.md / 分集稿 / 类型风格.md / 主体注册表 / 编剧稿` 是否在正确阶段被继承和兑现。旧项目存在 `north_star / init_handoff` 时可作为 legacy 辅助证据，但不得作为当前 scaffold-only 初始化的必备真源。

它不检查单镜构图语法、设计产物、图像 provider 交付或视频 provider 交付。

## Evidence

- 项目根 `MEMORY.md`
- legacy 初始化 `north_star / init_handoff` carrier（若存在）
- `1-分集` 分集稿与 validation carrier
- `2-美学/类型风格.md`、美学总览与 validation carrier
- `3-主体/主体注册表.md`、`3-主体/subject-registry.yaml` 与 validation carrier
- `4-编剧` 编剧稿与 validation carrier
- `review_fact_pack.required_refs`

## Review Network

| node_id | objective | actions | evidence | gate |
| --- | --- | --- | --- | --- |
| `N1-SEED-READ` | 锁上游真源 | 读取初始化、分集、类型风格、主体注册表、编剧 refs | `seed_note` | 真源明确 |
| `N2-HANDOFF-CHECK` | 检查 handoff obligations | 核对 `MEMORY.md / 分集稿 / 类型风格.md / 主体注册表 / 编剧稿`，并记录 legacy 初始化 carrier 是否存在 | `handoff_note` | obligations 可追溯 |
| `N3-CONTINUITY-CHECK` | 检查 seed 连续性 | 对照初始化、分集、美学题材配置、编剧是否断链 | `continuity_note` | continuity 成立 |
| `N4-PACKET-WRITE` | 输出维度 packet | 只写 `dimension_packet + report_ref` | `packet_note` | 可聚合 |

## Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-PS-01` | handoff obligations | handoff 引用完整可追溯 | `FAIL-PS-01` | `N2-HANDOFF-CHECK` |
| `FIELD-PS-02` | seed continuity | 初始化、分集、类型风格、主体注册表、编剧没有断链 | `FAIL-PS-02` | `N3-CONTINUITY-CHECK` |
| `FIELD-PS-03` | dimension packet | 报告完整可聚合 | `FAIL-PS-03` | `N4-PACKET-WRITE` |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否锁定同一 `review_fact_pack` 下的 `MEMORY.md`、`1-分集`、`2-美学/类型风格.md`、`3-主体/主体注册表.md` 与 `4-编剧` canonical refs，而不是混读旧阶段、旧集或派生摘要？ | `GATE-DIM-PS-01` | `FAIL-PS-01` | `N1-SEED-READ` | `seed_note` 记录 memory、legacy init carrier（若存在）、分集稿、类型风格、主体注册表、编剧稿、validation carrier 与缺失项。 |
| 初始化阶段写入的长期约束、项目口味和明确保真边界是否在 `1-分集` 中被继承，没有在分集切分时丢失或改写？ | `GATE-DIM-PS-02` | `FAIL-PS-01` | `N2-HANDOFF-CHECK` | `handoff_note` 标明丢失 obligation、对应初始化字段、分集落点和 source owner。 |
| `1-分集` 是否把 episode scope、集标、源文范围、保真边界和下游义务交给 `2-美学`，没有把章节、旧 P 标记或摘要当成当前集真源？ | `GATE-DIM-PS-03` | `FAIL-PS-01` | `N2-HANDOFF-CHECK` | 维度报告列出 scope_ref、集标证据、分集 handoff carrier 和不对位字段。 |
| `2-美学/类型风格.md` 是否真实消费全量分集故事源，将题材类型、标志性元素和题材专属表现技巧先交给 `3-主体` 建立主体注册表，再交给 `4-编剧`？ | `GATE-DIM-PS-04` | `FAIL-PS-02` | `N3-CONTINUITY-CHECK` | `continuity_note` 记录类型风格来源、主体注册表消费证据、编剧消费证据和断链位置。 |
| 若发现 seed 漂移或 obligation 缺口，是否归因到 `0-初始化`、`1-分集`、`2-美学`、`3-主体` 或 `4-编剧` 的具体 source owner，而不是把问题推给图像或视频阶段？ | `GATE-DIM-PS-05` | `FAIL-PS-02` | `N3-CONTINUITY-CHECK` | `dimension_packet.issues[*].source_layer_owner`、blocking_scope 与默认返工目标完整。 |
| 本维度是否严格排除单镜构图、设计、图像 provider、视频 provider 等非 planning seed 范围，避免扩大审计范围污染 aggregate？ | `GATE-DIM-PS-06` | `FAIL-PS-03` | `N4-PACKET-WRITE` | 维度报告说明未覆盖范围、实际检查范围和未越权 evidence。 |
| 本维度是否只输出可聚合 `dimension_packet + report_ref`，保留 `dimension_runtime`、severity、critical issues 与 evidence refs，而不独立写最终 route/status？ | `GATE-DIM-PS-07` | `FAIL-PS-03` | `N4-PACKET-WRITE` | `dimension_packet` 包含聚合字段、runtime spec 证据、report_ref，且无越权字段。 |

## Failure Heuristics

- 编剧稿存在但失去初始化、分集、类型风格或主体注册表 handoff 痕迹时，先回退到 `1-分集 / 2-美学 / 3-主体 / 4-编剧` 重建 handoff。
- 最隐蔽的断链通常不发生在设计或出图，而是发生在 planning/detail 之间的 seed 漂移。
- 判断时先锁 `MEMORY.md -> 1-分集 -> 2-美学/类型风格.md -> 3-主体/主体注册表.md -> 4-编剧/第N集.md`，再判 seed 是否被下游真实消费，而不是只看文件是否存在。

## Root-Cause Rule

若本维度失效，先回看 `MEMORY.md / 分集稿 / 类型风格.md / 主体注册表 / 编剧稿` 的 handoff 链，不要先改下游 prose、图像或 provider pack。

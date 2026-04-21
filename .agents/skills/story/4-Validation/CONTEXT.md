# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Validation` 父技能的经验层知识库，不是第二份阶段合同。
- 每次调用 `4-Validation` 时，应与 `SKILL.md` 一起加载，用于识别卷级 pack 缺口、并发聚合错误、章级回流漂移与 review/loopback 接驳问题。
- 冲突优先级固定为：用户显式请求 > AGENTS.md / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把 `4-Validation` 当成单集终验 | stage unit contract | 把父层 aggregate sink 改成卷级 `第V卷.validation.json` | 固定“卷级 gate，章级 issue index”双层模型 | review/loopback 只消费卷级 aggregate |
| 六个子技能并发时读取了不同卷快照 | concurrency contract | 统一重锁卷级 pack 与正文快照 | 父层合同写死“同一快照、同一 pack、先锁后并发” | 六维报告的 `pack_ref / manuscript_refs` 一致 |
| 卷级 aggregate 只有总分，没有章级返工入口 | routing granularity | 补 `chapter_issue_index` 与 step 级 `rework_targets` | 固定卷级父裁决必须带章级定位 | drafting 能精确回到受影响 worker |
| 明明是 planning continuity pack 漂移，却被打回 drafting | source trace routing | 改判为 `back_to_source_contract` | 让 issue 强制带 `source_layer_owner` | drafting 不再背 upstream 的锅 |
| 维度 sidecar 被误当成总 gate | composite output contract | 强调 sidecar 只作证据层 | 在 root/shared/template 中固定单一卷级 gate truth | 下游只认 aggregate JSON |

## Repair Playbook

1. 先确认这是卷级验收，不要先回到单集思维。
2. 再确认 pack 是否锁对了当前卷的 `volume_board / chapter_refs / continuity matrix`。
3. 若 aggregate 与 sidecar 冲突，优先修 child output contract 或聚合模板，不先改 prose。
4. 若问题看起来像正文缺陷，先问一句：upstream truth 是否本身冲突。
5. 若 `PASS` 了却无法接到 `review/5-Loopback`，优先检查 aggregate JSON 字段齐全度与 route 值。

## Reusable Heuristics

- 卷级终验最值钱的不是“把 10 集分别打分”，而是回答“这整卷现在是否能作为一个被放行的创作单元”。
- 子技能并发成立的前提不是目录分开，而是卷级事实包先锁住了。
- 卷级 aggregate 最怕的是只有总评没有回流入口；那样看起来高级，实际上不可执行。
- 章级问题可以很多，但 gate truth 只能有一个。

# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-Design` 阶段父 skill 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/4-Design/SKILL.md` 时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 根技能声称 `4-Design` 已建合同，但仓内没有阶段父级 | 阶段总合同层 | 补 `4-Design/SKILL.md + CONTEXT.md` | 把“阶段已建”定义为至少存在 stage parent 真源，而不是只有 leaf 目录 | 根技能状态与仓内实体一致 |
| leaf preload 直接引用不存在的 stage/substage parent | 上下文装配层 | 先补真实存在的 stage parent / tranche parent，再重挂 preload | 叶子只回链真实存在的父级真源 | preload 不再断链 |
| tranche parent 缺失，导致 leaf 各自发明父链 | tranche 治理层 | 补 `1-主体清单 / 2-主体设计 / 3-面板设计` 父级 | 把 tranche parent 视为 leaf 共享 context bridge | 同 tranche leaf 的 preload 更一致 |
| `4-Design` 父层越权发明第二业务真源 | 输出治理层 | 收回到“只路由、不写业务主稿” | 在 stage parent 固化“业务真源只由 leaf 写回” | 不再出现 `4-Design` 总稿 |

## Repair Playbook

1. 先确认 `4-Design` 是否存在真实 stage parent。
2. 再确认三个 tranche parent 是否存在。
3. 再扫描 leaf preload 是否全部先经过 stage/tranche parent。
4. 最后才修具体 leaf 的业务合同。

## Reusable Heuristics

- 对 `4-Design` 这种多 tranche、多类目的阶段来说，最容易坏的不是某个 leaf，而是“中间父级整层缺失”。
- 当多个 leaf 都想加载同一个不存在的父级时，根因通常不在 leaf，而在 stage parent / tranche parent 没有真正落地。
- `4-Design` 父级最稳的职责是路由、边界和 runtime 对齐，而不是跨类目再造第二真源。

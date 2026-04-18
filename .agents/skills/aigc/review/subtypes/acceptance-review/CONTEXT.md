# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `acceptance-review/` 的经验层知识库，不是过程日志。
- 每次调用本技能时，应自动预加载本文件，用于 scope-to-carrier 选择与闭环格式控制。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 阶段验收写到项目根 `validation-report.md` | scope mapping | 回到对应 runtime carrier 重写 | 把 acceptance 独立成子技能并固定 mapping | report 路径与 scope 一致 |
| 只给结论不写 layered trace | closure contract | 补完整 triad 与 layered trace | 在 acceptance 合同固定输出组成 | report 可回读完整闭环 |
| 验收报告先写概述，导致高风险问题被淹没 | findings ordering | 先按 `P0 -> P1 -> P2 -> P3` 列 findings | 固定 `findings first` 输出顺序与 evidence path 字段 | `validation-report.md` 可先看到 blocker，再看到总结 |

## Repair Playbook

1. 先锁 scope，再锁 carrier。
2. 再读对应产物与旧 report。
3. verdict、trace、closure 三块缺一不可。
4. 最后同步 `governance-state.yaml` 摘要。

## Reusable Heuristics

- acceptance 不是“看起来差不多”，而是“能不能把下一入口正式交出去”。
- 阶段级验收优先写阶段 runtime 下的 report，项目根 report 只承接 project scope。
- 对本仓库，acceptance 的高风险项通常来自 canonical source、runtime mapping、audit coverage 与 doc-runner parity，而不只是内容本身。

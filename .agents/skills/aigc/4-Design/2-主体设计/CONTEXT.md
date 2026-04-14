# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-Design/2-主体设计` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/4-Design/2-主体设计/SKILL.md` 时，应在 `aigc -> 3-Detail -> 1-主体清单` 根链之后加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 跳过 `1-主体清单` 直接进入设计 | 输入锚点层 | 回退到对应 domain 的 list outputs | 在父层固定 design-source bundle 为第一输入根 | 设计阶段不再直接从 detail 猜对象池 |
| prompt sidecar 开始反写设计事实 | 输出分层层 | 恢复 design master 为唯一业务真源 | 在父层和子层共同固定 `design master -> sidecar` 顺序 | sidecar 只承载 prompt 或展示补充 |
| `角色` 与 `服装` 同轮刷新后相互漂移 | 依赖门层 | 先稳定角色设计，再补服装设计 | 在父层明确 `角色 -> 服装` 的软依赖门 | 同轮服装更新不再脱离角色约束 |
| full-build 时四域全部串行，周期过长 | 调度拓扑层 | 回到 `场景 + 角色 + 道具` 先行、`服装` 后置 | 父层把批次和 selective dispatch 固定为默认策略 | 多域构建耗时下降且依赖仍正确 |
| `3-面板设计` 需要重新猜 design carrier 或路径 | handoff 层 | 回查 design master、sidecar、card 的命名和路径 | 父层验收强制检查下游可读性与路径一致性 | 下游直接消费，无需重新映射 |

## Repair Playbook

1. 先确认本轮命中的是哪个 design domain，避免把叶子内部问题误归父层。
2. 再检查该域是否从对应 `1-主体清单` 输出起步，而不是回头把 detail 当第一输入根。
3. 若同轮命中 `角色` 与 `服装`，优先核对依赖门是否已经显式触发。
4. 再检查 design master 与 secondary outputs 是否混层。
5. 最后汇总到 `projects/aigc/<项目名>/4-Design/validation-report.md`，记录 blocked domain 与下游 handoff readiness。

## Reusable Heuristics

- `2-主体设计` 的最大风险不是设计本身，而是跨域时把“设计载体”重新退化成“临时文案”。
- 对父层来说，最重要的不是参与子域设计，而是确保每个 domain 都从正确的 design-source bundle 起步。
- `角色 -> 服装` 的依赖通常不是绝对硬门，但在 full-build 中把它写成默认顺序最稳。
- 真正可靠的 handoff 不是“某个 Markdown 写完了”，而是下游能直接读取 design master 和必要 sidecar。
- stage-level 验收只记录 coverage、blocked 域和下一入口，不应在父层生成新的跨域设计主稿。

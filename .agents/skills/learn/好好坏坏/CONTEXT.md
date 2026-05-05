# Context: 好好坏坏

本文件是 `好好坏坏` 的经验上下文知识库，不是执行日志。它沉淀基于好/坏示例做源层调优时的可复用判断、修复打法和避坑策略。

## Context Health

```yaml
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-heuristic-focused
last_checked_at: 2026-05-05
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 坏示例被修成一次性输出，但同类任务仍复发 | 源层落点层 | 回到目标 `SKILL.md`、`steps/`、`review/` 或 `templates/` 找 owner 并补规则 | 固定 `source_owner[]` 字段，禁止只交付结果重写 | 新规则能解释坏示例为何失败，并能指导下一次任务 |
| 好示例被抽象成空泛偏好 | 信号提炼层 | 把好示例拆成可观察字段、资料使用、结构、语气和门禁 | `good_signals[]` 必须可复核、可迁移、可验证 | 调优摘要能说明好在哪里，而不只是“更自然” |
| 坏示例归因到模型发挥差 | 直接原因层 | 对照任务要求、资料来源和步骤链，找漏读、误判、模板缺口或 review 缺口 | 诊断矩阵必须包含 `Direct Output Cause` | 坏示例原因能落到具体源层载体 |
| 资料事实不确定却强行调优 | 证据层 | 标记残余风险或补充资料读取，不把不确定事实写成硬规则 | 区分事实证据、审美偏好和格式约束 | 输出保留 source material 引用或风险说明 |
| 调优只改目标 leaf，没有同步父级、shared 或 registry | 同步范围层 | 回补 `sync_scope[]` 和 `parity_targets[]` | 触及触发、路由、模板或共享载体时必须查 registry/routes 与 sibling | 相关入口和共享规则不漂移 |
| 一次性用户偏好被写进 `SKILL.md` 硬规则 | 经验晋升层 | 降级到目标 `CONTEXT.md` 或任务报告 | 稳定性、可重复性、高置信度不足时不晋升主合同 | `SKILL.md` 不承载临时偏好 |

## Repair Playbook

1. 先确认目标 skill、任务环节、好示例、坏示例是否同属一个可比较输出面。
2. 读取目标 `SKILL.md + CONTEXT.md`，再按环节读取相关 steps、references、types、review、templates、scripts 与 shared carrier。
3. 把好示例拆成可复用信号，把坏示例拆成失败信号，逐项绑定任务要求或资料来源。
4. 对每个坏信号追问：是目标要求缺失、资料使用错误、类型分支错误、步骤顺序错误、模板/schema 错误、review gate 缺失，还是脚本投影越权。
5. 只修改最窄有效源层 owner；若源层 owner 不唯一，先输出阻断或 patch plan，不做多处平行真源。
6. 修改后用同一组好/坏示例复核：好示例原则应保留，坏示例失败路径应被新规则阻断。
7. 局部项目偏好写项目 `MEMORY.md`，目标 skill 局部经验写目标 `CONTEXT.md`，跨技能调优经验写本文件或 `knowledge-base/`。

## Reusable Heuristics

- 好/坏对照的价值不在“模仿好示例”，而在发现目标 skill 源层缺少哪条可执行约束。
- 好示例至少要被拆成一个正向机制：用了什么资料、遵守了什么任务要求、结构上做对了什么、哪里体现了审美或专业判断。
- 坏示例至少要被拆成一个失败机制：漏了什么、错用了什么、过度发挥了什么、在哪里绕过了 gate。
- 如果一个差异无法绑定任务要求、资料来源或用户长期偏好，它通常不应直接进入硬规则。
- `templates/` 适合修输出形态，`review/` 适合修漏检，`steps/` 适合修顺序和分支，`types/` 适合修判型，`references/` 适合修长规则，`CONTEXT.md` 适合沉淀经验。
- 涉及 AIGC、story、comic 创作正文时，源层调优必须保持 LLM-first；脚本只能投影、校验和落盘。

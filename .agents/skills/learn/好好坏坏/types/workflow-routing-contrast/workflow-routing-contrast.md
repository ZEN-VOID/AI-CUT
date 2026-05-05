# Workflow Routing Contrast

用于分析好/坏示例是否由模式选择、子技能路由、阶段顺序、类型包命中或上下文加载差异导致。

## Fixed Checks

- 好示例是否走对模式、阶段、子技能或类型包。
- 坏示例是否跳过 `CONTEXT.md`、项目 `MEMORY.md`、资料读取、review gate 或必要上游产物。
- 目标 skill 的 `Mode Selection`、`Reference Loading Guide`、`Multi-Subskill Continuous Workflow` 是否足够明确。
- registry/routes 是否会把同一任务导向错误技能或漏掉新触发。

## Patch Bias

- 模式和入口路由问题优先修目标 `SKILL.md`，必要时同步 registry/routes。
- 顺序和失败回路问题优先修 `steps/`。
- 类型包命中问题优先修 `types/type-map.md`。

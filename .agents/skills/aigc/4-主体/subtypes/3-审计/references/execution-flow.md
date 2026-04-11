# 3-审计执行流程细则

## Canonical Landing

- 根目录：`projects/<项目名>/4-主体/3-审计/`
- 总报告：`projects/<项目名>/4-主体/3-审计/第N集/subject-audit-report.md`
- 单主体审计：
  - `projects/<项目名>/4-主体/3-审计/第N集/角色/[主体名].audit.md`
  - `projects/<项目名>/4-主体/3-审计/第N集/场景/[主体名].audit.md`
  - `projects/<项目名>/4-主体/3-审计/第N集/道具/[主体名].audit.md`
- 回写建议：`projects/<项目名>/4-主体/3-审计/第N集/writeback-plan.md`

## Mandatory Workflow

1. 读取 `.agents/skills/aigc/4-主体/SKILL.md + CONTEXT.md` 与 `2-设计` 产物。
2. 回查 `1-清单` bridge、`3-明细` 主文件和 `2-组间` handoff。
3. 为角色、场景、道具分别比对失败维度。
4. 输出审计报告、回写建议与下一步唯一入口。
5. 需要返工时，明确回到 `2-设计`；需要布局时，明确进入 `4-面板`。

## Council Runtime Inheritance

`3-审计` 不单独定义顾问团运行时，而是强制继承上层 `4-主体` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `策划` 先对审计范围、修订优先级与对象连续性提供前置建议。
3. 阶段级 `projects/<项目名>/4-主体/validation-report.md` 前后若命中 `评审`，仍按 `4-主体` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的阶段 canonical 写回权。

# 2-设计执行流程细则

## Canonical Landing

- 根目录：`projects/<项目名>/4-主体/2-设计/`
- 角色：
  - `projects/<项目名>/4-主体/2-设计/角色/第N集/[角色名].md`
  - `projects/<项目名>/4-主体/2-设计/角色/character_design.json`
- 场景：
  - `projects/<项目名>/4-主体/2-设计/场景/第N集/[场景名].md`
  - `projects/<项目名>/4-主体/2-设计/场景/scene_design.json`
- 道具：
  - `projects/<项目名>/4-主体/2-设计/道具/第N集/[道具名].md`
  - `projects/<项目名>/4-主体/2-设计/道具/prop_design.json`
- thinking sidecar：
  - `projects/<项目名>/4-主体/2-设计/thinking/<主体域>/第N集/[主体名].md`
- 验收：`projects/<项目名>/4-主体/2-设计/validation-report.md`

## Mandatory Workflow

1. 读取 `.agents/skills/aigc/4-主体/SKILL.md + CONTEXT.md` 与 `1-清单` 产物。
2. 判断命中的是角色、场景还是道具设计。
3. 为每个主体生成设计卡、设计侧车与 thinking sidecar。
4. 汇总本轮命中主体与下游建议入口。
5. 若用户请求复核，下一步进入 `3-审计`；若用户请求布局板，下一步进入 `4-面板`。

## Council Runtime Inheritance

`2-设计` 不单独定义顾问团运行时，而是强制继承上层 `4-主体` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `策划` 先对主体设计路线、对象优先级与资产连续性提供前置建议。
3. 阶段级 `projects/<项目名>/4-主体/validation-report.md` 前后若命中 `评审`，仍按 `4-主体` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的阶段 canonical 写回权。

# 4-面板执行流程细则

## Canonical Landing

- 根目录：`projects/<项目名>/4-主体/4-面板/`
- 角色：
  - `projects/<项目名>/4-主体/4-面板/角色面板/第N集/[角色名]-面板.md`
  - `projects/<项目名>/4-主体/4-面板/角色面板/第N集/[角色名]-layout.json`
- 场景：
  - `projects/<项目名>/4-主体/4-面板/场景面板/第N集/[场景名]-面板.md`
  - `projects/<项目名>/4-主体/4-面板/场景面板/第N集/[场景名]-layout.json`
- 道具：
  - `projects/<项目名>/4-主体/4-面板/道具面板/第N集/[道具名]-面板.md`
  - `projects/<项目名>/4-主体/4-面板/道具面板/第N集/[道具名]-layout.json`
- 验收：`projects/<项目名>/4-主体/4-面板/validation-report.md`

## Mandatory Workflow

1. 读取 `.agents/skills/aigc/4-主体/SKILL.md + CONTEXT.md` 与 `2-设计` 产物。
2. 若存在 `3-审计` 通过结果，优先消费通过版本。
3. 生成角色、场景、道具的面板主文件与 layout sidecar。
4. 汇总对 `5-画面`、`6-视频` 的参照交接说明。
5. 输出唯一下一入口。

## Council Runtime Inheritance

`4-面板` 不单独定义顾问团运行时，而是强制继承上层 `4-主体` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `策划` 先对面板化路线、参照板结构与资产连续性提供前置建议。
3. 阶段级 `projects/<项目名>/4-主体/validation-report.md` 前后若命中 `评审`，仍按 `4-主体` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的阶段 canonical 写回权。

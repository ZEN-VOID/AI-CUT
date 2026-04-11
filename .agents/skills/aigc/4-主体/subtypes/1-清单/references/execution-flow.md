# 1-清单执行流程细则

## Canonical Landing

- 根目录：`projects/<项目名>/主体/1-清单/`
- 角色：
  - `projects/<项目名>/主体/1-清单/角色清单/第N集/角色清单.json`
  - `projects/<项目名>/主体/1-清单/角色清单/第N集/role_design_bridge.json`
- 场景：
  - `projects/<项目名>/主体/1-清单/场景清单/第N集/场景清单.json`
  - `projects/<项目名>/主体/1-清单/场景清单/第N集/scene_design_bridge.json`
- 道具：
  - `projects/<项目名>/主体/1-清单/道具清单/第N集/道具清单.json`
  - `projects/<项目名>/主体/1-清单/道具清单/第N集/prop_design_bridge.json`
- 验收：`projects/<项目名>/主体/1-清单/validation-report.md`

## Mandatory Workflow

1. 读取 `.agents/skills/aigc/4-主体/SKILL.md + CONTEXT.md` 与 `projects/<项目名>/3-明细/第N集.md`。
2. 抽取角色、场景、道具候选项。
3. 做命名归一、去重、连续性合并与用途标注。
4. 为三类主体分别落盘清单 JSON 与 bridge JSON。
5. 输出 `2-设计` 的唯一推荐入口。

## Council Runtime Inheritance

`1-清单` 不单独定义顾问团运行时，而是强制继承上层 `4-主体` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `策划` 先对主体池范围、对象裁剪与资产路线提供前置建议。
3. 阶段级 `projects/<项目名>/主体/validation-report.md` 前后若命中 `评审`，仍按 `4-主体` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的阶段 canonical 写回权。

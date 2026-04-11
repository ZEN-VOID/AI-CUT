# aigc 3-明细 / 4-场景氛围 / Execution Flow

本文件承载 `aigc 3-明细 / 4-场景氛围` 的 unified root patch contract、共享运行时与完整 workflow。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].分镜明细[].场景氛围`
- 氛围裁决侧车：`projects/<项目名>/编导/evidence/4-场景氛围/氛围裁决-第N集.md`
- 母题账本：`projects/<项目名>/编导/evidence/4-场景氛围/母题账本-第N集.md`
- 本层验收：`projects/<项目名>/编导/evidence/4-场景氛围/validation-report.md`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 本叶子未被调度时不得写占位，不得参与聚合

## Input Source Priority

1. 优先读取 `writer.story` bundle，默认消费 `世界卡 / 风格卡` 作为环境语气与题材路由护栏。
2. 若 bundle 缺失，再回退读取 canonical `project_preset.json`。
3. 若两者都缺失，必须在侧车或 `validation-report.md` 中显式记录预设缺口，不得静默沿旧假设继续。

## Council Runtime Inheritance (Mandatory)

`4-场景氛围` 不单独定义顾问团运行时，而是强制继承上层 `3-明细` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `监制` 先对空间压力、环境可拍性与风格一致性提供前置建议。
3. 阶段级 `projects/<项目名>/编导/validation-report.md` 前后若命中 `评审`，仍按 `3-明细` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的统一根文件写回权。

## Mandatory Workflow

1. 读取上层 `.agents/skills/aigc/3-明细/SKILL.md + CONTEXT.md`，并完整读取当前 `第N集.json`。
2. 先确认父级 `3-明细` 已将本叶子纳入本轮 `selected_subskills[]`；若未命中，立即停止。
3. 回看 grouped source、`2-组间` handoff 与 `writer.story` 预设字段，识别戏核、题材护栏与环境缺口。
4. 为待补镜位建立叙事锚点卡，并在 `景 / 境 / 物 / 留白` 中裁决 dominant route。
5. 以字段 patch 方式把氛围判断写回 `场景氛围`；锚点卡、母题链与 QA 结论只保留在 sidecar。
6. 复检边界、密度、连读性与下一入口，不为未调度的 sibling 补空字段。

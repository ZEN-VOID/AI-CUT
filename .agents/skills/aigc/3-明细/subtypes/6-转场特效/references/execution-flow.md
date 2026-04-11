# aigc 3-明细 / 6-转场特效 / Execution Flow

本文件承载 `aigc 3-明细 / 6-转场特效` 的 unified root patch contract、共享运行时与完整 workflow。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].分镜明细[].转场特效`
- 转场设计侧车：`projects/<项目名>/编导/evidence/6-转场特效/转场设计-第N集.md`
- 执行报告：`projects/<项目名>/编导/evidence/6-转场特效/execution-report-第N集.md`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 本叶子未被调度时不得写占位，不得参与聚合

## Council Runtime Inheritance (Mandatory)

`6-转场特效` 不单独定义顾问团运行时，而是强制继承上层 `3-明细` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `监制` 先对镜间桥接、特效必要性与执行成本提供前置建议。
3. 阶段级 `projects/<项目名>/编导/validation-report.md` 前后若命中 `评审`，仍按 `3-明细` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的统一根文件写回权。

## Mandatory Workflow

1. 读取上层 `.agents/skills/aigc/3-明细/SKILL.md + CONTEXT.md` 与完整的 `projects/<项目名>/编导/第N集.json`。
2. 先确认父级 `3-明细` 已将本叶子纳入本轮 `selected_subskills[]`；若未命中，立即停止。
3. 锁定命中的分镜组与分镜明细，回查角色表现、运镜手法与组间 handoff。
4. 逐组或逐段提取桥接锚点，裁决包装层与主桥接路径。
5. 仅生成本镜级 `转场特效` 字段 patch；桥接理由、排除理由与留口进入 evidence sidecar。
6. 本叶子不创建第二份 episode 主稿或平行汇总稿，统一根文件写回由父级聚合器负责。

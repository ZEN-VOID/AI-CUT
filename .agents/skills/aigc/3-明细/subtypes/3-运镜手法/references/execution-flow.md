# aigc 3-明细 / 3-运镜手法 / Execution Flow

本文件承载 `aigc 3-明细 / 3-运镜手法` 的 unified root patch contract、共享运行时与完整 workflow。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].分镜明细[].运镜手法`
- 运镜设计侧车：`projects/<项目名>/编导/evidence/3-运镜手法/运镜设计-第N集.md`
- 执行报告：`projects/<项目名>/编导/evidence/3-运镜手法/execution-report-第N集.md`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 本叶子未被调度时不得写占位，不得参与聚合

## Council Runtime Inheritance (Mandatory)

`3-运镜手法` 不单独定义顾问团运行时，而是强制继承上层 `3-明细` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `监制` 先对镜间观看路径、执行成本与可拍性提供前置建议。
3. 阶段级 `projects/<项目名>/编导/validation-report.md` 前后若命中 `评审`，仍按 `3-明细` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的统一根文件写回权。

## Mandatory Workflow

1. 读取上层 `.agents/skills/aigc/3-明细/SKILL.md + CONTEXT.md` 与完整的 `projects/<项目名>/编导/第N集.json`。
2. 先确认父级 `3-明细` 已将本叶子纳入本轮 `selected_subskills[]`；若未命中，立即停止。
3. 锁定命中分镜组与分镜明细，提取组级/段级观看路径锚点。
4. 裁决主运镜波形，并将其拆成逐镜 `运镜手法` 字段 patch。
5. 将波形理由、排除理由与未处理留口写入 evidence sidecar 与执行报告。
6. 本叶子只返回本字段 patch，不创建第二份 episode 主稿或平行汇总稿。

# aigc 3-明细 / 5-摄影美学 / Execution Flow

本文件承载 `aigc 3-明细 / 5-摄影美学` 的 unified root patch contract、共享运行时与完整 workflow。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].分镜明细[].摄影美学`
- 父级执行报告：`projects/<项目名>/编导/evidence/5-摄影美学/execution-report-第N集.md`
- patch 记录：`projects/<项目名>/编导/evidence/5-摄影美学/patch-log-第N集.md`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 本父技能只聚合本轮实际调度到的 `光影设计 / 色彩设计 / 摄影参数`；未调度子技能与总 `json` 无关

## Council Runtime Inheritance (Mandatory)

`5-摄影美学` 不单独定义顾问团运行时，而是强制继承上层 `3-明细` 的 `Council Runtime Contract`。

执行规则：

1. 进入本父技能或其叶子技能前，先遵守 `3-明细` 根技能对项目根 `team.yaml` 的读取规则。
2. 若顾问团启用，则由 `监制` 先对摄影层增强的执行一致性、成本感与下游视频继承性给建议。
3. 本层完成后若进入阶段级 `validation-report.md`，`评审` 仍只在 `3-明细` 根级闸门介入。
4. 本父技能与其叶子技能都不夺取统一根文件写回权。

## Mandatory Workflow

1. 读取 `.agents/skills/aigc/3-明细/SKILL.md + CONTEXT.md` 与完整的 `projects/<项目名>/编导/第N集.json`。
2. 确认目标镜位已经具备上游 `分镜表现` 与必要的组间 handoff。
3. 由父级 route decision 明确本轮 `selected_subskills[]`；若只命中一个 leaf，则只执行一个，禁止为了结构完整补跑其余 leaf。
4. 进入命中的 leaf 执行；若多命中，则按 `光影设计 -> 色彩设计 -> 摄影参数` 受控串行续写。
5. 各 leaf 只返回 `摄影美学` 字段 patch，并把完整三段式过程写入各自 evidence sidecar。
6. 父技能只聚合本轮实际命中的 patch，并统一回写到 `第N集.json` 的镜级字段。
7. 将本轮裁决、覆盖镜位与未处理留口写入执行报告与 patch 记录；未命中的 leaf 不得补空字段。

# aigc 3-明细 / 2-角色表现 / Execution Flow

本文件承载 `aigc 3-明细 / 2-角色表现` 的 unified root patch contract、共享运行时与完整 workflow。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].分镜明细[].角色表现`
- 父级执行报告：`projects/<项目名>/编导/evidence/2-角色表现/execution-report-第N集.md`
- patch 记录：`projects/<项目名>/编导/evidence/2-角色表现/patch-log-第N集.md`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 本父技能只聚合本轮实际调度到的 `动作戏 / 对手戏 / 内心戏`；未调度子技能与总 `json` 无关

## Input Source Priority

1. 优先读取 `writer.performance` bundle，作为本层默认的表演口径、预设与 guard 入口。
2. 若 bundle 缺失，再回退读取 legacy `project_preset.json`。
3. 若两者都缺失，必须在执行报告中显式记录输入缺口，不得静默沿旧假设继续。

## Council Runtime Inheritance (Mandatory)

`2-角色表现` 不单独定义顾问团运行时，而是强制继承上层 `3-明细` 的 `Council Runtime Contract`。

执行规则：

1. 进入本父技能或其叶子技能前，先遵守 `3-明细` 根技能对项目根 `team.yaml` 的读取规则。
2. 若顾问团启用，则由 `监制` 先对人物层增强的可拍性、节奏压力与执行边界给建议。
3. 本层完成后若进入阶段级 `validation-report.md`，`评审` 仍只在 `3-明细` 根级闸门介入。
4. 本父技能与其叶子技能都不夺取统一根文件写回权。

## Mandatory Workflow

1. 完整读取 `projects/<项目名>/编导/第N集.json`，再读取 `writer.performance` bundle、分组容器与 `2-组间` handoff。
2. 由父级 route decision 明确本轮 `selected_subskills[]`；若只命中一个 leaf，则只执行一个，禁止为了结构完整补跑其余 leaf。
3. 判断当前场景/段落的 dominant pressure，并先锁不可变层与越权边界。
4. 进入命中的角色表现 leaf 执行；若多命中，则先执行 dominant subtype，再决定是否追加 supplemental subtype。
5. 各 leaf 只返回 `角色表现` 字段 patch，并把三段式过程写入各自 evidence sidecar。
6. 父技能只聚合本轮实际命中的 patch，并统一回写到 `第N集.json` 的镜级字段。
7. 将本轮裁决、覆盖范围与未处理留口写入执行报告与 patch 记录；未命中的 leaf 不得补空字段。

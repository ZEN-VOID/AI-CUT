# aigc 3-明细 / 1-分镜表现 / Execution Flow

本文件承载 `aigc 3-明细 / 1-分镜表现` 的 unified root patch contract、共享运行时与完整 workflow。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- patch 目标：`final_output.main_content.分镜组列表[].分镜明细[].分镜表现`
- 密度分析 sidecar：`projects/<项目名>/编导/evidence/1-分镜表现/密度分析-第N集.md`
- 构图方案 sidecar：`projects/<项目名>/编导/evidence/1-分镜表现/构图方案-第N集.md`
- 本层验收：`projects/<项目名>/编导/evidence/1-分镜表现/validation-report.md`
- 阶段验收：`projects/<项目名>/编导/validation-report.md`
- 本父技能只聚合本轮实际调度到的 `分镜密度 / 分镜构图`；未调度子技能与总 `json` 无关

## Council Runtime Inheritance (Mandatory)

`1-分镜表现` 不单独定义顾问团运行时，而是强制继承上层 `3-明细` 的 `Council Runtime Contract`。

执行规则：

1. 进入本父技能或其叶子技能前，先遵守 `3-明细` 根技能对项目根 `team.yaml` 的读取规则。
2. 若顾问团启用，则由 `监制` 先对分镜组织、镜数资源感与可拍性给建议。
3. 本层完成后若进入阶段级 `validation-report.md`，`评审` 仍只在 `3-明细` 根级闸门介入。
4. 本父技能与其叶子技能都不夺取统一根文件写回权。

## Mandatory Workflow

1. 读取上层 `.agents/skills/aigc/3-明细/SKILL.md + CONTEXT.md` 与完整的 `projects/<项目名>/编导/第N集.json`。
2. 若 `metadata.source_profile.preset_registry` 非空，先做锚点继承判定：哪些组命中 `hard_lock / soft_lock / reference_only`，哪些允许一锚多镜。
3. 先由父级 route decision 明确本轮 `selected_subskills[]`；若只命中其一，则只调度其一，不为结构完整补跑另一子技能。
4. 逐组进入 `分镜密度`，确定镜数、锚点与插入节奏；若命中 `soft_lock + single_anchor_multi_shot`，可在同一粗锚点内细分多镜。
5. 仅对已命中的结果继续进入 `分镜构图`，生成静态镜头组织方案与 `分镜表现` patch。
6. 各叶子把完整三段式过程写入各自 sidecar，只返回本层负责字段的 patch。
7. 父技能只聚合本轮已调度叶子的有效 patch，并统一回写到 `第N集.json` 的镜级字段。
8. 复检原文守恒、组内编号连续、写位边界与结构一致性；未命中的子技能不得补空字段。

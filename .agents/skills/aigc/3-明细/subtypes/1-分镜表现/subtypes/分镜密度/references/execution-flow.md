# aigc 3-明细 / 1-分镜表现 / 分镜密度 / Execution Flow

本文件承载 `分镜密度` 叶子的统一写位、sidecar 与返回 patch 规则。

## Canonical Landing

- 统一根文件：`projects/<项目名>/编导/第N集.json`
- sidecar 输出：`projects/<项目名>/编导/evidence/1-分镜表现/密度分析-第N集.md`
- 返回责任：为父级 `1-分镜表现` 提供镜数、锚点、节奏决策与 `分镜表现` patch 草案
- 本叶子未被调度时不得写占位，不得参与聚合

## Council Runtime Inheritance (Mandatory)

`分镜密度` 不单独定义顾问团运行时，而是强制继承 `3-明细` 根技能与 `1-分镜表现` 父技能的顾问团合同。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `监制` 先对镜数密度、执行资源感与可拍性提供前置建议。
3. 阶段级 `projects/<项目名>/编导/validation-report.md` 前后若命中 `评审`，仍按 `3-明细` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的统一根文件写回权。

## Leaf Workflow (Mandatory)

1. 先完整读取 `projects/<项目名>/编导/第N集.json`，再锁定当前分镜组的剧本正文、组间设计与既有镜级结构。
2. 先确认父级 `1-分镜表现` 已将本叶子纳入本轮 `selected_subskills[]`；若未命中，立即停止。
3. 先做第一层节奏裁决，锁定 `base_range`，不得跳步直接给镜数。
4. 再做第二层收窄，得到 `refined_range`，并检查 `single_panel_long_take` 是否成立。
5. 最后枚举候选整数，执行可拍性、可读性与 `Aesthetic Pressure Test`，收敛为唯一 `panel_count`。
6. 将 `panel_count`、句段锚点、功能位、`aesthetic_peak_plan` 与给父级的 patch 建议写入 sidecar，由父技能决定是否继续调度 `分镜构图` 并统一聚合。

## Gate Order (Mandatory)

- `rhythm / scene_type / group_duration / info_load` 决定 `panel_count`。
- `导演意图` 只允许在合法 `refined_range` 内偏置默认落点。
- 模板门槛、反平庸门禁与集级序列去重属于末端验收，不得前置抢答。

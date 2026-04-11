# 节奏执行流程细则

## Canonical Landing

- 阶段目录：`projects/<项目名>/规划/4-节奏/`
- canonical 主产物：`projects/<项目名>/规划/4-节奏/第N集.md`
- thinking sidecar：`projects/<项目名>/规划/4-节奏/thinking/第N集.md`
- 验收记录：`projects/<项目名>/规划/4-节奏/validation-report-第N集.md`
- 父级聚合写回：仅在 `1-规划` 显式选中 `4-节奏` 时，把节奏摘要 patch 回 `projects/<项目名>/规划/第N集.md`

## Mandatory Workflow

1. 读取 `projects/<项目名>/Init/north_star.yaml` 与 `Init/init_handoff.yaml`，确认 `original_adherence` 与顺序授权。
2. 若 `original_adherence: true`，停止本技能，返回“保留原作节奏，不独立执行 `4-节奏`”的结论。
3. 读取 `Init/episode-split-plan.json`、`规划/第N集.md` 与 `规划/3-分组/第N集.md`。
4. 锁定本集主驱动与七步缺口。
5. 生成七步节奏蓝图、峰值账本与组级节奏刀法。
6. 补齐 `下游加载提示`，明确 `2-组间/导演意图` 与 `3-明细` 继续放大的方向。
7. 先落 `thinking/第N集.md`，再落 `第N集.md` 与 `validation-report-第N集.md`。
8. 若本轮由父级 `1-规划` 显式纳入 `4-节奏`，则把 `主驱动裁决 / 峰值账本 / 节奏执行策略 / 下游加载提示` 以摘要 patch 回父级 `规划/第N集.md`；若未显式纳入，则本技能只保留本地节奏 handoff。

## Council Runtime Inheritance

`4-节奏` 不单独定义顾问团运行时，而是强制继承上层 `1-规划` 的 `Council Runtime Contract`。

执行规则：

1. 直接进入本叶子技能时，仍必须先读取 `projects/<项目名>/team.yaml` 与 `.agents/skills/aigc/_shared/council-runtime/module-spec.md`。
2. 若顾问团启用，则由 `策划` 先对节奏重排收益、结构完整性与后续可消费性提供前置建议。
3. 阶段级 `projects/<项目名>/规划/validation-report.md` 前后若命中 `评审`，仍按 `1-规划` 根技能的闸门执行。
4. 本叶子技能不夺取主代理的阶段 canonical 写回权。

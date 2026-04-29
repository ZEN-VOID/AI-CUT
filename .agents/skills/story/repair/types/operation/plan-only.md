# Operation Package: Plan Only

## Selection Signals

- 用户要求“先分析 / 看看影响 / 给计划 / 不要动文件 / 只审计”。

## Fixed Context

- 不写回 canonical 文件。
- 可以读取、定位、汇总和输出 repair plan。
- 若发现阻断风险，报告缺口和推荐授权点。

## Review Gate

- 输出必须包含 `impact_map`、`canonical_owner`、`writeback_order` 和 residual risk。
- 不得声称已完成实际修复。

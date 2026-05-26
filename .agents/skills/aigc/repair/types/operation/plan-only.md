# Operation: Plan Only

用于只生成影响范围、修复计划、豆包任务包或审计报告，不执行写回。

## Fixed Context

- 不修改 canonical 业务文件。
- 可以输出 `doubao_task_packet`、stage routes、writeback order 和 asset action 建议。
- 若用户后续授权执行，重新进入 `operation.execute`。

## Review Gate

- 报告清楚标记 `mode: repair_plan` 或 `impact_assessment`。
- 不列出不存在的 changed files。

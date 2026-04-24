# Output Template

## Output Contract Alignment

- Required output: 升级后的目标 skill 载体改动，以及包含 `upgrade_points`、`point_type`、`landing_set`、`sync_scope`、`validation_checks`、`review_gate`、`learning_writebacks`、`residual_risks` 的 absorption summary。
- Output format: 目标文件 patch、必要同步面、验证结果与中文最终摘要。
- Output path: 默认原地修改 `target_skill` 所在目录；必要同步面落在对应父级/sibling/shared/registry 路径；报告类派生产物按用户要求写入 `reports/`。
- Naming convention: 新增 Skill 2.0 文件使用 canonical 固定名；任务 ID 与脚本参数保持 ASCII 安全字符。
- Completion gate: 通过结构、引用和 `review/review-contract.md` 本地 gate；若真实 reviewer/subagent 被阻断，必须报告降级。

## Absorption Summary

```yaml
target_skill: ""
upgrade_points: []
point_type: []
landing_set: []
sync_scope: []
parity_targets: []
validation_checks: []
review_gate:
  mode: ""
  verdict: ""
learning_writebacks: []
residual_risks: []
```

## Human Summary

- 已改动：
- 验证：
- 降级或风险：

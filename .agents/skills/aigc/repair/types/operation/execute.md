# Operation: Execute

用于用户明确要求执行、改掉、同步修、写回或重做。

## Fixed Context

- 执行前必须确认写回权限和破坏性范围。
- 文本分析、润色和创意候选默认走 `doubao-seed-2.0-pro`；provider 不可用时必须显式降级。
- 写回只能进入 owning stage 合同允许的路径。

## Review Gate

- changed files、provider evidence、review verdict 和 residual risks 必须齐全。
- 对生成资产只记录失效或重建路线，不伪造结果。

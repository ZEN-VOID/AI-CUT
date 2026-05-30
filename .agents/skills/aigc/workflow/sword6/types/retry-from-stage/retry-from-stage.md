# Retry From Stage

适用于从 `3-导演`、`4-表演`、`5-摄影` 或 `6-分组` 续跑。

## Fixed Context

- `start_stage` 必须明确。
- 对每集验证 `start_stage` 所需上一阶段输入存在。
- 若上一阶段输入缺失或不可信，回到 owning stage，而不是从请求阶段硬跑。
- retry report 必须列出 reused outputs 和 regenerated outputs。

## Gate Bias

续跑不默认覆盖已有通过产物。覆盖必须来自用户明确授权或阶段 repair gate。

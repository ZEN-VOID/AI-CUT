# Retry From Stage

适用于从 `2-美学`、`3-主体`、`4-编剧`、`5-导演`、`6-分镜`、`7-摄影` 或 `8-分组` 续跑；旧 `2-编导`、`3-运动`、`4-摄影`、`5-分组` 续跑请求应先映射到当前 2-8 主链 owner。

## Fixed Context

- `start_stage` 必须明确。
- 对每集验证 `start_stage` 所需上一阶段输入存在。
- 若上一阶段输入缺失或不可信，回到 owning stage，而不是从请求阶段硬跑。
- retry report 必须列出 reused outputs 和 regenerated outputs。

## Gate Bias

续跑不默认覆盖已有通过产物。覆盖必须来自用户明确授权或阶段 repair gate。

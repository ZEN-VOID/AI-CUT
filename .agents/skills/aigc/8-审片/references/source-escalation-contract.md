# Source Escalation Contract

## High-Confidence Gate

只有同时满足以下条件，才允许把审片发现上升到源层：

1. 至少两个素材、两个变体、或跨分镜组重复出现同类问题；或单个问题已经明确来自技能合同/模板文字。
2. 能排除普通模型偶发瑕疵、下载损坏、单次 seed 漂移。
3. 能定位明确 source owner：`3-摄影`、`4-分组`、`7-视频`、`8-审片` 或对应叶子技能。
4. 有清晰修复方式，且不会破坏既有成功案例。
5. 最终报告写明 `Symptom -> Direct Cause -> Source Owner -> Rule Fix`。

## Common Source Owners

| symptom | likely owner |
| --- | --- |
| 文件名无法回推 group_id | `7-视频` 输出合同 |
| 15 秒视频总是塞入太多 beat | `4-分组` 边界/密度合同 |
| 镜头不可动、只有气氛形容 | `3-摄影` 分镜明细合同 |
| 审片无法稳定落盘 | `8-审片` landing contract |
| 多路线视频都错绑主体参照 | `7-视频` 叶子 reference binding |

## Downgrade Rule

只要证据不足，必须降级为 `review_only` 或 `rerun_only`。不得为了“看起来闭环”而污染源层。

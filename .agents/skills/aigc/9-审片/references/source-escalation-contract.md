# Source Escalation Contract

## High-Confidence Gate

只有同时满足以下条件，才允许把审片发现上升到源层：

1. 至少两个素材、两个变体、或跨分镜组重复出现同类问题；或单个问题已经明确来自技能合同/模板文字。
2. 能排除普通模型偶发瑕疵、下载损坏、单次 seed 漂移。
3. 能定位明确 source owner：`4-摄影`、`5-分组`、`8-视频`、`9-审片` 或对应叶子技能。
4. 有清晰修复方式，且不会破坏既有成功案例。
5. 最终报告写明 `Symptom -> Direct Cause -> Source Owner -> Rule Fix`。

## Common Source Owners

| symptom | likely owner |
| --- | --- |
| 文件名无法回推 group_id | `8-视频` 输出合同 |
| 15 秒视频总是塞入太多 beat | `5-分组` 边界/密度合同 |
| 镜头不可动、只有气氛形容 | `4-摄影` 分镜明细合同 |
| 审片无法稳定落盘 | `9-审片` landing contract |
| 多路线视频都错绑主体参照 | `8-视频` 叶子 reference binding |

## Downgrade Rule

只要证据不足，必须降级为 `review_only` 或 `rerun_only`。不得为了“看起来闭环”而污染源层。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 源层升级是否满足“至少两个素材/变体/跨分镜组重复”或“单个问题明确来自技能合同/模板文字”的高置信入口？ | `GATE-REVIEW-10` | `FAIL-REVIEW-SOURCE-ESCALATION` | `steps/video-review-workflow.md#N5 Landing`、本文件 `High-Confidence Gate` | 多例素材清单、变体/分镜组 refs，或直接源层文字证据 |
| 是否已排除普通模型偶发瑕疵、下载损坏、单次 seed 漂移等不应污染源层的原因？ | `GATE-REVIEW-10` / `GATE-REVIEW-05` | `FAIL-REVIEW-SOURCE-ESCALATION` | 本文件 `High-Confidence Gate`、`references/review-dimensions-contract.md#Mismatch Attribution` | 排除说明、同组变体对比、prompt 清晰度和模型问题证据 |
| 是否定位了明确 source owner，例如 `4-摄影`、`5-分组`、`8-视频`、`9-审片` 或对应叶子技能，而不是笼统写“上游问题”？ | `GATE-REVIEW-10` | `FAIL-REVIEW-SOURCE-ESCALATION` | 本文件 `Common Source Owners`、`steps/video-review-workflow.md#N5 Landing` | `source_owner`、owner path、症状到 owner 的因果说明 |
| 修复方式是否清晰、局部、可执行，且不会破坏既有成功案例？ | `GATE-REVIEW-11` | `FAIL-REVIEW-SOURCE-ESCALATION` | owning skill / source document、`steps/video-review-workflow.md#N6 Write And Verify` | 修复方案、影响范围、成功案例不破坏说明、changed_files |
| 最终报告是否写明 `Symptom -> Direct Cause -> Source Owner -> Rule Fix`，让源层变更可追溯？ | `GATE-REVIEW-12` | `FAIL-REVIEW-SOURCE-ESCALATION` | `steps/video-review-workflow.md#N6 Write And Verify`、`templates/review-report.template.md` | 报告中的源层升级链、rule fix diff 或未升级原因 |
| 证据不足时是否降级为 `review_only` 或 `rerun_only`，而不是为了闭环强行源层优化？ | `GATE-REVIEW-10` | `FAIL-REVIEW-LANDING` | 本文件 `Downgrade Rule`、`references/finding-landing-contract.md` | 降级 verdict、`landing_decision`、证据缺口说明 |

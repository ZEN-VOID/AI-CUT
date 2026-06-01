# Finding Landing Contract

## Landing Types

| landing | use when | write target |
| --- | --- | --- |
| `review_only` | 信息不足、低置信、或仅记录素材内容 | `projects/aigc/<项目名>/9-审片/第N集/` |
| `rerun_only` | 单次生成瑕疵，不需要改上游 | 审片报告 + `8-视频` rerun note |
| `group_repair` | 分镜组正文、节奏、焦点、首尾状态导致可复现偏差 | `projects/aigc/<项目名>/5-分组/第N集.md` |
| `source_escalation` | 多例复现且能定位阶段合同或技能模板 | owning skill / source document |

## Group Repair Boundary

允许修：

- 对应 `## group_id` 的正文、YAML 统计、出场/入场或新版组间连接件。
- 与该组直接相邻且必须同步的衔接画面。

禁止顺手修：

- 无关分镜组。
- 未经证据支持的剧情事实。
- 全集结构迁移。

## Report Required Fields

审片报告必须包含：

- `video_path`
- `group_id`
- `variant`
- `source_group_path`
- `observed_content`
- `expected_from_group`
- `findings`
- `landing_decision`
- `changed_files`
- `thinking_process`

## Patch Rule

`group_repair` 不是重写得更文学，而是让下一次视频生成更稳定：

- 降低同时出现的主体数量。
- 明确唯一焦点、镜头动作和停点。
- 把后续 beat 留给下一组。
- 减少可读文字、复杂近景手部和无必要角色近景。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每条 finding 是否按证据强度和置信度落到 `review_only`、`rerun_only`、`group_repair` 或 `source_escalation`，而不是为了闭环强行改上游？ | `GATE-REVIEW-10` | `FAIL-REVIEW-LANDING` | `steps/video-review-workflow.md#N5 Landing`、本文件 `Landing Types` | finding list 中的 `landing_decision`、`confidence`、降级或升级理由 |
| `group_repair` 是否只修改对应 `## group_id`、必要 YAML/首尾状态和直接相邻衔接画面，未顺手改无关分镜组或全集结构？ | `GATE-REVIEW-11` | `FAIL-REVIEW-PATCH-SCOPE` | `steps/video-review-workflow.md#N6 Write And Verify`、本文件 `Group Repair Boundary` | `changed_files`、目标 group_id、diff 摘要、相邻衔接修改原因 |
| 审片报告是否包含 `video_path`、`group_id`、`variant`、`source_group_path`、`observed_content`、`expected_from_group`、`findings`、`landing_decision`、`changed_files`、`thinking_process`？ | `GATE-REVIEW-12` | `FAIL-REVIEW-REPORT` | `templates/review-report.template.md`、`steps/video-review-workflow.md#N6 Write And Verify` | 报告字段清单或缺字段修复记录 |
| `group_repair` 是否以“让下一次视频生成更稳定”为目标，降低主体数量、明确唯一焦点/镜头动作/停点，并把后续 beat 留给下一组？ | `GATE-REVIEW-10` / `GATE-REVIEW-11` | `FAIL-REVIEW-PATCH-SCOPE` | 本文件 `Patch Rule`、`projects/aigc/<项目名>/5-分组/第N集.md` 对应组 | 修前/修后组摘要、被移走或保留的 beat、生成稳定性说明 |
| `source_escalation` 是否只在满足高置信升级门后使用，低置信或单次模型瑕疵是否降级为 `review_only` / `rerun_only`？ | `GATE-REVIEW-10` | `FAIL-REVIEW-SOURCE-ESCALATION` | `references/source-escalation-contract.md`、`steps/video-review-workflow.md#N5 Landing` | 多例证据、source owner、降级说明或源层修复链路 |

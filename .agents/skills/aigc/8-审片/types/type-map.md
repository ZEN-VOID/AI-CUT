# Type Map

## Type Profile Variables

| variable | values |
| --- | --- |
| `video_scope` | `single_video`、`group_variants`、`episode_batch` |
| `naming_state` | `canonical`、`variant`、`drifted`、`unknown` |
| `source_state` | `group_found`、`group_missing`、`ambiguous_group` |
| `evidence_state` | `video_ok`、`no_audio`、`audio_only`、`unreadable` |
| `prompt_state` | `prompt_found`、`prompt_missing`、`prompt_ambiguous`、`prompt_conflicting` |
| `example_state` | `no_examples`、`good_examples`、`bad_examples`、`paired_examples`、`batch_examples` |
| `subagents_state` | `not_requested`、`enabled`、`blocked_by_upper_policy`、`completed`、`downgraded` |
| `review_dimension` | `video_intrinsic`、`prompt_alignment`、`creative_quality`、`example_calibration` |
| `mismatch_owner` | `none`、`prompt_problem`、`model_problem`、`mixed_cause`、`evidence_gap` |
| `quality_state` | `strong_candidate`、`usable_plain`、`aesthetic_miss`、`banal`、`unusable` |
| `finding_route` | `review_only`、`rerun_only`、`group_repair`、`quality_learning`、`source_escalation` |

## Mapping Matrix

| signal | route impact | review impact |
| --- | --- | --- |
| `single_video + canonical` | 直接审片 | 标准报告 |
| `group_variants` | 对比共同问题和单变体问题 | 共同问题更可能上游可修 |
| `drifted` | 先记录命名异常 | 不阻断内容审查，但不能静默通过 |
| `group_missing` | 阻断或最小澄清 | 不写回 |
| `audio_only` | 只审音频 | 不给视频通过 verdict |
| `prompt_found` | 启用 prompt alignment pass | 必须输出 matched / partially_matched / mismatched / not_enough_prompt_evidence |
| `prompt_conflicting` | 优先排查 prompt 问题 | 不把模型判为唯一责任方 |
| `paired_examples` | 启用 example calibration pass | 必须输出靠近好示例和落入坏示例的点 |
| `subagents_state + enabled` | 启用审片监制顾问分支 | 必须按 `team.yaml` 和共享顾问合同形成 `review_advisor_packet` |
| `subagents_state + blocked_by_upper_policy` | 不得本地模拟为真实 subagents | 必须输出阻断层级、原计划路径、实际降级路径和未启动成员 |
| `creative_quality + banal` | 给出创作质量阻断或条件通过 | 不把“技术可用”等同于“创作合格” |
| `model_problem` | 默认 rerun 或换路线 | 不改分组，除非多例稳定失败 |
| `prompt_problem` | 回到 `4-分组` / `7-视频` prompt owner | 修 prompt 密度、动作可执行性或审美约束 |
| `source_escalation` | 必须读取 source escalation contract | 高置信门逐项检查 |

# Type Map

## Type Profile Variables

| variable | values |
| --- | --- |
| `input_origin` | `local_file`、`libtv_canvas_url`、`libtv_project_uuid`、`libtv_canvas_name`、`libtv_bound_project` |
| `video_scope` | `single_video`、`group_variants`、`episode_batch` |
| `libtv_state` | `not_applicable`、`project_resolved`、`project_ambiguous`、`node_resolved`、`node_missing`、`remote_video_ready`、`downloaded`、`download_failed` |
| `naming_state` | `canonical`、`variant`、`drifted`、`unknown` |
| `source_state` | `group_found`、`group_missing`、`ambiguous_group` |
| `evidence_state` | `video_ok`、`no_audio`、`audio_only`、`unreadable` |
| `prompt_state` | `prompt_found`、`prompt_missing`、`prompt_ambiguous`、`prompt_conflicting` |
| `example_state` | `no_examples`、`good_examples`、`bad_examples`、`paired_examples`、`batch_examples` |
| `顾问与复核流程_state` | `not_requested`、`enabled`、`local_checklist`、`completed` |
| `review_dimension` | `video_intrinsic`、`prompt_alignment`、`creative_quality`、`example_calibration` |
| `method_profile` | `source_fidelity_pass`、`continuity_pass`、`performance_pass`、`cinematography_pass`、`editing_rhythm_pass`、`sound_pass`、`prop_object_pass`、`ethics_safety_pass`、`aigc_artifact_forensics`、`prompt_execution_pass`、`candidate_selection_pass`、`repair_design_pass` |
| `mismatch_owner` | `none`、`prompt_problem`、`model_problem`、`mixed_cause`、`evidence_gap` |
| `quality_state` | `strong_candidate`、`usable_plain`、`aesthetic_miss`、`banal`、`unusable` |
| `finding_route` | `review_only`、`rerun_only`、`conditional_accept`、`variant_selection`、`group_repair`、`libtv_prompt_repair`、`asset_reference_repair`、`sound_policy_repair`、`quality_learning`、`source_escalation` |
| `operation_route` | `accept_as_candidate`、`conditional_accept`、`compare_variants`、`rerun_same_prompt`、`rerun_with_seed_or_model_change`、`libtv_prompt_repair_and_rerun`、`group_prompt_repair`、`shot_split_or_merge`、`asset_reference_repair`、`image_order_repair`、`sound_policy_repair`、`download_or_naming_repair`、`request_missing_evidence`、`source_escalation_candidate`、`archive_rejected_candidate` |

## Mapping Matrix

| signal | route impact | review impact |
| --- | --- | --- |
| `input_origin + libtv_canvas_url` | 先走 `references/libtv-intake-contract.md` 的 URL projectId 解析 | 必须保存 remote node query 并下载真实视频后再审片 |
| `input_origin + libtv_canvas_name` | 先用 `libtv project list --name` 唯一匹配画布 | 多命中阻断，不能猜项目 |
| `input_origin + libtv_project_uuid` | 直接用显式 project UUID 查询节点 | 报告中记录 projectUuid、nodeKey、result URL |
| `libtv_state + downloaded` | 进入标准本地视频审片 | `libtv_input` 与 evidence pack 都必须落进报告 |
| `libtv_state + project_ambiguous` | 阻断并要求最小澄清 | 不得下载或审片 |
| `libtv_state + node_missing` | 阻断并要求视频节点名或 node key | 不得凭画面猜 group |
| `libtv_state + download_failed` | 保存远端查询证据，停止最终 verdict | 报告下载失败和可恢复动作 |
| `single_video + canonical` | 直接审片 | 标准报告 |
| `group_variants` | 对比共同问题和单变体问题 | 共同问题更可能上游可修 |
| `drifted` | 先记录命名异常 | 不阻断内容审查，但不能静默通过 |
| `group_missing` | 阻断或最小澄清 | 不写回 |
| `audio_only` | 只审音频 | 不给视频通过 verdict |
| `prompt_found` | 启用 prompt alignment pass | 必须输出 matched / partially_matched / mismatched / not_enough_prompt_evidence |
| `prompt_conflicting` | 优先排查 prompt 问题 | 不把模型判为唯一责任方 |
| `paired_examples` | 启用 example calibration pass | 必须输出靠近好示例和落入坏示例的点 |
| `observed_content_summary` | 进入 method selection | 必须记录 selected / skipped methods 和理由 |
| `dialogue_or_audio_present` | 启用 `sound_pass` | 输出音频事实、同步和声音策略判断 |
| `human_performance_visible` | 启用 `performance_pass` | 检查表演动机、眼神、情绪和身体动作 |
| `camera_language_material` | 启用 `cinematography_pass` / `editing_rhythm_pass` | 判断机位、构图、运动、节奏和观众位置 |
| `key_prop_or_text_visible` | 启用 `prop_object_pass` / `aigc_artifact_forensics` | 检查关键物、伪文字、融化和状态连续 |
| `safety_or_project_boundary_signal` | 启用 `ethics_safety_pass` | 对照项目 MEMORY / north_star 判断呈现方式 |
| `group_variants + candidate_selection_pass` | 启用选片操作 | 输出 primary / backup / reject 和修复成本 |
| `顾问与复核流程_state + enabled` | 启用审片监制顾问分支 | 必须按 `team.yaml` 和共享顾问合同形成 `review_advisor_packet` |
| `顾问与复核流程_state + local_checklist` | 不得本地模拟为顾问与复核流程 | 使用本地顾问与复核流程 |
| `creative_quality + banal` | 给出创作质量阻断或条件通过 | 不把“技术可用”等同于“创作合格” |
| `model_problem` | 默认 rerun 或换路线 | 不改分组，除非多例稳定失败 |
| `prompt_problem` | 回到 `5-分组` / `8-视频` prompt owner | 修 prompt 密度、动作可执行性或审美约束 |
| `source_escalation` | 必须读取 source escalation contract | 高置信门逐项检查 |

# Output Template

## Execution Summary

```yaml
flow: subject_reference_flow
project_root: projects/aigc/<项目名>
episode: 第N集
groups:
  - group_id: x-y-z
    duration: 12
    resolution: 720p
    ratio: "16:9"
    allow_libtv_prompt_optimization: false
    prompt_optimization_opt_in: false
    generation_mode: omnireference_video
    generation_mode_label: 全能参考 / 多图主体参考生成视频
    modeType: mixed2video
    modeType_source: subject_reference_flow_default
    text2video_fallback_authorized: false
    handoff_prompt_separated_from_params_prompt: true
    params_prompt_contract: [分镜组正文, 完整YAML, 主体_at_资产引用]
    prompt_lock_natural_language_checked: true
    canvas_at_asset_mentions_checked: true
    canvas_at_asset_mentions_status: verified | at_asset_mention_unverified
    remote_params_prompt_fidelity_checked: true
    full_yaml_in_params_prompt: true
    binding_table_in_params_prompt: false
    duplicate_subject_reference_checked: true
    canonical_reference_order: yaml_roles_then_scenes_then_props
    reference_order_checked: true
    reference_mapping_checked: true
    prompt_duplication_checked: true
    duration_estimate_seconds: 14
    duration_source: yaml_duration_estimate
    registry_path: projects/aigc/<项目名>/9-视频/libTV画布流/libtv-canvas-active-registry.json
    manifest_path: projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-subject-reference-manifest.json
    submit_plan_path: projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-libtv-submit-plan.json
    queue_record_path: projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-queue-record.json
    excluded_from_libtv_images: []
    excluded_due_to_budget: []
    status: submitted | completed | blocked | placeholder
    sessionId: ""
    projectUuid: ""
    projectUrl: ""
    canvas_link: "[打开画布](https://www.liblib.tv/canvas?projectId=...)"
    downloaded: false
    local_file: ""
```

## Output Contract Alignment

- Required output: 记录 LibTV 画布流提交状态、主体绑定表使用状态、active registry、manifest、submit plan、queue record、session/canvas 信息和显式下载结果。
- Output format: 中文简报 + 可选 YAML/JSON 摘要。
- Output path: 默认不落本地视频生成物；证据工件进入 `projects/aigc/<项目名>/9-视频/libTV画布流/第N集/`，active registry 位于 `projects/aigc/<项目名>/9-视频/libTV画布流/`；显式下载时进入同集目录。
- Naming convention: 单组视频 `<分镜组ID>.mp4`；多变体 `<分镜组ID>-a.mp4`。
- Completion gate: 类型包已加载，主体绑定表、active registry、manifest、submit plan、queue record 和时长投影完成，LibTV env wrapper 已转官方脚本提交或明确阻断；默认未自动下载。

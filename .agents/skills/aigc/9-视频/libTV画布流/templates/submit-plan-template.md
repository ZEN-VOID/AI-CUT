# Submit Plan Template

```yaml
schema_version: libtv-submit-plan/v1
flow: subject_reference_flow
project_root: projects/aigc/<项目名>
episode: 第N集
group_id: x-y-z
group_source_path: projects/aigc/<项目名>/6-分组/第N集.md
group_source_heading: "## x-y-z"
projectUuid: ""
projectUrl: ""
registry_path: projects/aigc/<项目名>/9-视频/libTV画布流/libtv-canvas-active-registry.json
manifest_path: projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-subject-reference-manifest.json
queue_record_path: projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-queue-record.json
remote_prompt_template: .agents/skills/aigc/9-视频/libTV画布流/templates/libtv-remote-prompt-template.md
duration_estimate_seconds: 14
duration_source: yaml_duration_estimate
duration: 14
resolution: 720p
ratio: "16:9"
audio: 按用户或分镜组要求
allow_libtv_prompt_optimization: false
prompt_optimization_opt_in: false
generation_mode: omnireference_video
generation_mode_label: 全能参考 / 多图主体参考生成视频
modeType: mixed2video
modeType_source: subject_reference_flow_default
text2video_fallback_authorized: false
subject_binding_table_title: 主体绑定表
canonical_reference_order:
  source: yaml_subject_order
  order: [角色, 场景, 道具]
  preserve_yaml_list_order: true
  apply_to:
    - subject_bindings
    - selected_reference_bindings
    - source_node_keys
    - source_node_url_mapping
    - imageList
    - mixedList
  forbidden_order_sources:
    - upload_order
    - canvas_created_at
    - local_file_scan_order
    - Image_N
    - Portrait_N
reference_order_check: planned
reference_mapping_check: planned
handoff_message_contains:
  - canvas_instruction
  - generation_mode
  - modeType
  - duration_resolution_ratio_download
  - prompt_lock
  - selected_reference_bindings
params_prompt_contract:
  - storyboard_group_body
  - full_fenced_yaml
  - canvas_at_asset_mentions_after_bound_subjects
prompt_lock_natural_language_required: true
canvas_at_asset_mentions_required: true
canvas_at_asset_mentions_verification: required
canvas_at_asset_mentions_status: planned
remote_params_prompt_fidelity_check_required: true
full_fenced_yaml_in_params_prompt: true
subject_binding_table_in_params_prompt: false
execution_metadata_in_params_prompt: false
duplicate_subject_reference_allowed: false
dedupe_style_audio_constraints: true
libtv_images_count: 0
libtv_reference_payload_required: true
excluded_from_libtv_images: []
excluded_due_to_budget: []
forbidden_prompt_phrases:
  - 本轮不提交任何参考图 URL
  - 参考图审核失败
  - 改为纯文生视频
  - 角色与道具按原文生成
  - StyleBible_Summary
  - 其中，
  - 【执行锁】
  - 【生成参数】
  - 【本次提交的9张参照图】
  - 【主体绑定表】
download: false
status: planned
```

## Required Notes

- `prompt_body` 只引用 `6-分组` 现有组正文，不在计划中改写剧情事实。
- `allow_libtv_prompt_optimization=false` 必须同时写入 handoff message 自然语言锁定句，禁止优化、重排、摘要、压缩、改写或补镜头，并要求 `create_generation_task.params.prompt` 严格等于“分镜组正文 + 底部完整 YAML”。
- `分镜组原文` 中每个已绑定 YAML 主体首次出现处、以及底部 YAML 中对应主体名后，必须插入 LibTV 画布 `@` 资产引用 / node mention（标准名称待官方确认）；引用绑定来自 `主体绑定表` 的 `canvas_node_name / node_key / URL`，不得伪造成普通文本解释、URL 注释、`{{Portrait N}}`、`〔主体参照: ...〕` 或手写图片编号。
- 当前 CLI 纯文本消息无法单独证明 UI 级 `@` 引用已插入；提交计划必须记录验证方式，无法验证时写 `canvas_at_asset_mentions_status=at_asset_mention_unverified`。
- 本地图片路径、候选集合和视觉消歧证据只进入 manifest / submit plan，不进入 `params.prompt`。
- `allow_libtv_prompt_optimization=true` 只能在用户显式 opt-in 后出现，并同步写入 queue record 与执行报告。
- 当 `libtv_images_count > 0` 时，handoff message 必须显式请求 `全能参考 / 多图主体参考生成视频`，并逐项包含真实 `URL + node_key + yaml_name + 用途`。
- `source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 必须按 YAML 主体展示顺序的选中子集传入：`角色` 原顺序 -> `场景` 原顺序 -> `道具` 原顺序；不得按上传顺序或 `Portrait N` 排列。
- 查询后必须核对 `source_node_url_mapping` 每个 `node_key/url` 与主体绑定表的 `yaml_name/category` 一致；不得用数组第 N 项反推主体。
- `modeType` 必须使用 Seedance 2.0 标准称谓；主体参照流默认 `mixed2video`，指定类型时必须全链路一致。
- `text2video_fallback_authorized` 默认必须为 `false`；参考图审核失败时不得静默降级，除非用户当前轮显式授权。
- `本轮不提交任何参考图 URL`、`参考图审核失败`、`改为纯文生视频` 等执行诊断不得进入 `params.prompt`。
- `params.prompt` 必须包含底部完整 fenced YAML；不得用 `YAML主体清单` 或 `主体绑定表` 替代完整 YAML，也不得把绑定表复制进 `params.prompt`。
- 同一 YAML 主体默认只提交一张参照图；除非用户显式要求多视图或多版本对比，不得把 active 图和新上传图同时放入同一视频任务。
- 分镜组正文已有 StyleBible、声音、字幕、背景音乐约束时，不得在头部或尾部重复追加，也不得生成 `其中，...` 复述段。

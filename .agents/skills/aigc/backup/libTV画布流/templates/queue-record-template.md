# Queue Record Template

```yaml
schema_version: libtv-queue-record/v1
flow: subject_reference_flow
project_root: projects/aigc/<项目名>
episode: 第N集
group_id: x-y-z
status: planned | submitted | completed | blocked | needs_rework
sessionId: ""
projectUuid: ""
projectUrl: ""
submitted_at: ""
updated_at: ""
official_script: .agents/skills/cli/libTV/scripts/create_session.py
wrapper: .agents/skills/aigc/8-视频/libTV画布流/scripts/run_libtv_with_env.py
env_loaded_from: .env
allow_libtv_prompt_optimization: false
prompt_optimization_opt_in: false
generation_mode: omnireference_video
generation_mode_label: 全能参考 / 多图主体参考生成视频
modeType: mixed2video
modeType_source: subject_reference_flow_default
text2video_fallback_authorized: false
prompt_structure_checked: false
prompt_lock_natural_language_checked: false
canvas_at_asset_mentions_checked: false
canvas_at_asset_mentions_status: unverified
remote_params_prompt_fidelity_checked: false
yaml_subject_list_in_prompt: false
prompt_duplication_checked: false
download: false
downloaded_files: []
manifest_path: projects/aigc/<项目名>/8-视频/libTV画布流/第N集/x-y-z-subject-reference-manifest.json
submit_plan_path: projects/aigc/<项目名>/8-视频/libTV画布流/第N集/x-y-z-libtv-submit-plan.json
report_path: projects/aigc/<项目名>/8-视频/libTV画布流/第N集/x-y-z-执行报告.md
blocked_reason: ""
```

队列记录只保存提交和状态证据，不承载剧情改写或创作正文。

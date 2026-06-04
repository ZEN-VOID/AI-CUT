# Default Video Review Type Package

## Purpose

`default` 类型包用于所有尚未分化为独立子类型的审片任务。它只提供类型画像和固定上下文，不拥有独立审片节点、verdict、landing 或输出合同。

## Match Signals

- 用户提供本地 `.mp4`、LibTV 入口、同组变体、好/坏示例或授权修复请求。
- 没有更具体的审片类型包被用户或父技能显式命中。

## Fixed Context

- `types/type-map.md`
- `SKILL.md#Type Routing Matrix`
- `SKILL.md#Thinking-Action Node Map`

## Output To Runtime Spine

```yaml
type_profile:
  package_id: default
  input_origin: local_file | libtv_canvas_url | libtv_project_uuid | libtv_canvas_name | libtv_bound_project
  video_scope: single_video | group_variants | episode_batch
  evidence_state: video_ok | no_audio | audio_only | unreadable
  finding_route: review_only | rerun_only | conditional_accept | variant_selection | group_repair | libtv_prompt_repair | asset_reference_repair | sound_policy_repair | quality_learning | source_escalation
```

## Boundary

- 不读取视频、不抽帧、不比较 prompt、不写报告。
- 不替代 `SKILL.md` 的 `Type Routing Matrix`、`Module Trigger Matrix` 或 `Review Gate Binding`。

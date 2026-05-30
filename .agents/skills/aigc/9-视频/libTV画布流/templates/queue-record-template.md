# Queue Record Template

```yaml
schema_version: 2
project_name: ""
episode: "第N集"
group_id: "x-y-z"
status: planned | blocked | handed_off | running | complete | failed | needs_rework
created_at: ""
updated_at: ""

libtv:
  executor_skill: ".agents/skills/cli/libTV"
  cli_version: ""
  projectUuid: ""
  projectUrl: ""
  groupNodeKey: ""
  video_node_key: ""
  video_node_name: "x-y-z"
  left_input_edges:
    - image_index: 1
      placeholder: "{{Image 1}}"
      yaml_name: ""
      node_key: ""
  queried_left_input_order_verified: false

artifacts:
  manifest_path: "projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-subject-reference-manifest.json"
  submit_plan_path: "projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-libtv-submit-plan.json"
  cli_handoff_plan_path: "projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-cli-handoff-plan.md"
  report_path: "projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-执行报告.md"

commands:
  planned: []
  executed_summary: []
  left_connection_summary: ""

download:
  requested: false
  command_summary: ""
  local_path: ""

blocking:
  blocked_reason: ""
  fail_codes: []
  next_fix: ""
```

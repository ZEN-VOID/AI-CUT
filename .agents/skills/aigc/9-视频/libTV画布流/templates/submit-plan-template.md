# LibTV Submit Plan Template

## Output Contract Alignment

- Required output: per-group submit plan with source, subject binding, duration/spec, CLI handoff and review status.
- Output format: Markdown with YAML blocks.
- Output path: `projects/aigc/<项目名>/9-视频/libTV画布流/第N集/<分镜组ID>-libtv-submit-plan.json` or `.md` when human-readable.
- Naming convention: `<分镜组ID>-libtv-submit-plan`.
- Completion gate: route, prompt, binding, handoff and review fields are complete.

```yaml
schema_version: 2
project_name: ""
project_root: "projects/aigc/<项目名>"
episode: "第N集"
group_id: "x-y-z"
flow: subject_reference_flow
status: planned | blocked | handed_off | executed | needs_rework

paths:
  registry_path: "projects/aigc/<项目名>/9-视频/libTV画布流/libtv-canvas-active-registry.json"
  manifest_path: "projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-subject-reference-manifest.json"
  queue_record_path: "projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-queue-record.json"
  cli_handoff_plan_path: "projects/aigc/<项目名>/9-视频/libTV画布流/第N集/x-y-z-cli-handoff-plan.md"

source:
  group_source_path: "projects/aigc/<项目名>/6-分组/第N集.md"
  connector_skipped: true
  prompt_source: "6-分组原文 + 完整 YAML"

duration_spec:
  duration_source: yaml | storyboard_sum | fallback_default
  duration_estimate_seconds: 0
  duration_seconds: 0
  resolution: "720p"
  ratio: "16:9"

subject_bindings: []
left_input_edges: []
image_placeholder_map: []
excluded_due_to_budget: []
missing_subjects: []

prompt_policy:
  allow_libtv_prompt_optimization: false
  params_prompt_clean: true
  image_placeholders_inserted: true
  image_placeholders_source: "left_input_edges"
  preserve_scene_shot_identity: true
  forbidden_internal_diagnostics_in_prompt: true

mode:
  model: "star-video2"
  model_default_source: "LibTV Seedance 2.0 standard model; star-video2-fast requires explicit user override"
  modeType: mixed2video
  model_schema_checked: false
  model_schema_source: ""

cli_handoff:
  executor_skill: ".agents/skills/cli/libTV"
  cli_version_required: ">=1.0.1"
  auth_check_command: "libtv account info"
  projectUuid: ""
  projectUrl: ""
  group:
    name: ""
    node_key: ""
  video_node:
    name: "x-y-z"
    node_key: ""
    model: "star-video2"
    model_override_reason: ""
    left_connection_strategy: create_with_ordered_left_inputs | rebuild_existing_left_inputs | append_only_when_empty
    left_input_edges:
      - image_index: 1
        placeholder: "{{Image 1}}"
        yaml_name: ""
        node_key: ""
        connect_command: "libtv node \"x-y-z\" -p \"<projectUuid>\" -g \"<groupNodeKey>\" --left-add \"<imageNodeKey>\""
    prompt_uses_placeholders: true
  planned_commands: []
  executed_commands_summary: []

download:
  requested: false
  planned_command: ""
  output_path: ""

review:
  verdict: pending
  fail_codes: []
```

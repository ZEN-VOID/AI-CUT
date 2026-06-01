# LibTV Submit Plan Template

## Output Contract Alignment

- Required output: per-group submit plan with source, subject binding, duration/spec, CLI handoff and review status.
- Output format: Markdown with YAML blocks.
- Output path: `projects/aigc/<项目名>/8-视频/libTV画布流/第N集/<分镜组ID>-libtv-submit-plan.json` or `.md` when human-readable.
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
  registry_path: "projects/aigc/<项目名>/8-视频/libTV画布流/libtv-canvas-active-registry.json"
  stable_subject_mapping_path: "projects/aigc/<项目名>/8-视频/libTV画布流/stable-subject-mapping.json"
  manifest_path: "projects/aigc/<项目名>/8-视频/libTV画布流/第N集/x-y-z-subject-reference-manifest.json"
  queue_record_path: "projects/aigc/<项目名>/8-视频/libTV画布流/第N集/x-y-z-queue-record.json"
  cli_handoff_plan_path: "projects/aigc/<项目名>/8-视频/libTV画布流/第N集/x-y-z-cli-handoff-plan.md"

source:
  group_source_path: "projects/aigc/<项目名>/5-分组/第N集.md"
  connector_skipped: true
  prompt_source: "5-分组原文 + 完整 YAML"

duration_spec:
  duration_source: yaml | storyboard_sum | fallback_default
  duration_estimate_seconds: 0
  duration_seconds: 0
  resolution: "720p"
  ratio: "16:9"

subject_bindings: []
planned_left_input_edges: []
runtime_image_placeholder_map: []
queried_runtime_image_map_verified: false
final_remote_prompt_queried_after_last_prompt_write: false
remote_prompt_hygiene_verified: false
excluded_due_to_budget: []
missing_subjects: []

prompt_policy:
  allow_libtv_prompt_optimization: false
  params_prompt_clean: true
  image_placeholders_inserted: true
  image_placeholders_source: "runtime_image_placeholder_map"
  image_placeholder_insert_scope: "fenced_yaml_subject_entries_only"
  final_prompt_assembled_after_runtime_image_map: true
  final_prompt_must_be_queried_from_remote_node: true
  decisive_check_timing: "after final node params and prompt are written, immediately before --run"
  forbidden_remote_prompt_tokens:
    - "{{Portrait"
    - "主体绑定表"
    - "参照图绑定"
    - "planned_left_input_edges"
    - "runtime_image_placeholder_map"
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
    ordered_single_attach_default: true
    planned_left_input_edges:
      - planned_image_index: 1
        stable_subject_id: ""
        yaml_name: ""
        node_key: ""
        connect_command: "libtv node \"x-y-z\" -p \"<projectUuid>\" -g \"<groupNodeKey>\" --left-add \"<imageNodeKey>\""
    create_without_run_first: true
    draft_prompt_before_runtime_map: true
    auto_repair_before_run:
      enabled: true
      repairable_failures:
        - runtime_image_order_differs_from_plan
        - prompt_placeholder_mismatch
        - remote_prompt_pollution
        - stale_portrait_placeholder
      hard_stop_failures:
        - missing_or_ambiguous_subject_asset
        - cli_cannot_update_left_inputs_or_prompt
        - remote_prompt_rewritten_after_update
        - reference_asset_review_failed
      actions:
        - rebuild_runtime_image_placeholder_map
        - rewrite_prompt_from_runtime_map
        - clean_remote_prompt_pollution
        - rebuild_ordered_left_inputs_if_needed
    auto_repair_actions: []
    decisive_pre_run_query_required: true
    last_prompt_write_round: 0
    runtime_image_placeholder_map:
      - image_index: 1
        placeholder: "{{Image 1}}"
        stable_subject_id: ""
        yaml_name: ""
        node_key: ""
        assetId: ""
        url: ""
        verified_by: "queried data.params.imageList"
    query_before_run_required: true
    final_query_before_run_must_verify_prompt_and_imageList: true
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

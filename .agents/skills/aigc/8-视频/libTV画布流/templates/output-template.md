# Output Template: libTV画布流

## Output Contract Alignment

- Required output: LibTV plan / handoff / execution status, subject binding, artifacts and residual risks.
- Output format: concise Chinese report plus artifact paths.
- Output path: `projects/aigc/<项目名>/8-视频/libTV画布流/第N集/`.
- Naming convention: group-id prefixed artifact names.
- Completion gate: review pass or blocked reason; if executed, CLI result identifiers recorded.

```yaml
libtv_canvas_flow_report:
  project: ""
  episode: "第N集"
  route: subject_reference_flow
  status: planned | handed_off | executed | blocked | needs_rework
  libtv:
    executor_skill: ".agents/skills/cli/libTV"
    projectUuid: ""
    projectUrl: ""
    groupNodeKey: ""
    video_node_key: ""
  artifacts:
    registry_path: ""
    manifest_path: ""
    submit_plan_path: ""
    queue_record_path: ""
    cli_handoff_plan_path: ""
    report_path: ""
  prompt:
    source_group: ""
    clean_params_prompt: true
    allow_libtv_prompt_optimization: false
  subject_binding:
    active_registry_updated: false
    missing_subjects: []
    excluded_due_to_budget: []
  duration_spec:
    duration_seconds: 0
    resolution: "720p"
    ratio: "16:9"
  download:
    requested: false
    local_path: ""
  review:
    verdict: ""
    fail_codes: []
    residual_risks: []
```

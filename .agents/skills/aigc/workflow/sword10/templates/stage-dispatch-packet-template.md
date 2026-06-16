# Stage Dispatch Packet Template

## Output Contract Alignment

| Output Contract field | Template section |
| --- | --- |
| Required output | per-stage per-episode dispatch packet |
| Output format | YAML-compatible packet |
| Output path | `projects/aigc/<项目名>/workflow/sword10/<run_id>/dispatch/<stage_slug>/第N集.yaml` |
| Naming convention | `dispatch/<stage_slug>/第N集.yaml` |
| Completion gate | packet has input_path, output_path, stage_skill, completion_gate |

```yaml
run_id: sword10-YYYYMMDD-HHMMSS
project_root: projects/aigc/<项目名>/
episode_id: 第N集
stage_scope: episode
stage_slug: 4-编剧
stage_skill: .agents/skills/aigc/4-编剧/SKILL.md
stage_context: .agents/skills/aigc/4-编剧/CONTEXT.md
input_path: projects/aigc/<项目名>/1-分集/第N集.md
output_path: projects/aigc/<项目名>/4-编剧/第N集.md
extra_inputs: []
context_bundle:
  - projects/aigc/<项目名>/MEMORY.md
  - projects/aigc/<项目名>/CONTEXT/
runtime_mode: subagent
subagent_id: null
completion_gate:
  expected_output_exists: true
  stage_review_verdict: pass
status: pending
verdict: null
fail_code: null
```

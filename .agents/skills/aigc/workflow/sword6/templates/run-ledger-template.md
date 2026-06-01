# Run Ledger Template

## Output Contract Alignment

| Output Contract field | Template section |
| --- | --- |
| Required output | `run-ledger.yaml` |
| Output format | YAML-compatible ledger |
| Output path | `projects/aigc/<项目名>/workflow/sword6/<run_id>/run-ledger.yaml` |
| Naming convention | `run-ledger.yaml` |
| Completion gate | `status` and `stages[].verdict` are filled |

```yaml
run_id: sword6-YYYYMMDD-HHMMSS
project_root: projects/aigc/<项目名>/
episode_selector: []
start_stage: 2-编导
end_stage: 5-分组
runtime_mode: subagent
used_subagent_runtime: true
status: running
stages:
  - stage_slug: 2-编导
    status: pending
    verdict: null
    dispatch_dir: dispatch/2-编导/
    episodes: []
  - stage_slug: 3-运动
    status: pending
    verdict: null
    dispatch_dir: dispatch/3-运动/
    episodes: []
  - stage_slug: 4-摄影
    status: pending
    verdict: null
    dispatch_dir: dispatch/4-摄影/
    episodes: []
  - stage_slug: 5-分组
    status: pending
    verdict: null
    dispatch_dir: dispatch/5-分组/
    episodes: []
failure_routes: []
```

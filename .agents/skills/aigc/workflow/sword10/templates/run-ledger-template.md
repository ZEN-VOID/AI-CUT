# Run Ledger Template

## Output Contract Alignment

| Output Contract field | Template section |
| --- | --- |
| Required output | `run-ledger.yaml` |
| Output format | YAML-compatible ledger |
| Output path | `projects/aigc/<项目名>/workflow/sword10/<run_id>/run-ledger.yaml` |
| Naming convention | `run-ledger.yaml` |
| Completion gate | `status` and `stages[].verdict` are filled |

```yaml
run_id: sword10-YYYYMMDD-HHMMSS
project_root: projects/aigc/<项目名>/
episode_selector: []
start_stage: 2-编剧
end_stage: 10-分组
runtime_mode: subagent
used_subagent_runtime: true
status: running
stages:
  - stage_slug: 2-编剧
    status: pending
    verdict: null
    dispatch_dir: dispatch/2-编剧/
    episodes: []
  - stage_slug: 3-美学
    status: pending
    verdict: null
    dispatch_dir: dispatch/3-美学/
    episodes: []
  - stage_slug: 4-导演
    status: pending
    verdict: null
    dispatch_dir: dispatch/4-导演/
    episodes: []
  - stage_slug: 5-表演
    status: pending
    verdict: null
    dispatch_dir: dispatch/5-表演/
    episodes: []
  - stage_slug: 6-氛围
    status: pending
    verdict: null
    dispatch_dir: dispatch/6-氛围/
    episodes: []
  - stage_slug: 7-分镜
    status: pending
    verdict: null
    dispatch_dir: dispatch/7-分镜/
    episodes: []
  - stage_slug: 8-摄影
    status: pending
    verdict: null
    dispatch_dir: dispatch/8-摄影/
    episodes: []
  - stage_slug: 9-光影
    status: pending
    verdict: null
    dispatch_dir: dispatch/9-光影/
    episodes: []
  - stage_slug: 10-分组
    status: pending
    verdict: null
    dispatch_dir: dispatch/10-分组/
    episodes: []
failure_routes: []
```

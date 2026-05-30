# Sword6 Output Template

本模板定义 `sword6` 完成后的汇总报告结构。

## Output Contract Alignment

| Output Contract field | Template section |
| --- | --- |
| Required output | Run Summary、Stage Results、Final Artifacts |
| Output format | Markdown report with YAML-compatible tables |
| Output path | `projects/aigc/<项目名>/workflow/sword6/<run_id>/completion-report.md` |
| Naming convention | `completion-report.md` |
| Completion gate | Completion Verdict、Failure And Retry Routes |

## Template

```markdown
# Sword6 Completion Report

run_id: <run_id>
project_root: projects/aigc/<项目名>/
episode_selector: <episodes>
runtime_mode: subagent|degraded-subagent-unavailable
verdict: pass|partial|blocked

## Run Summary

| stage | total | passed | failed | skipped |
| --- | ---: | ---: | ---: | ---: |
| 2-编剧 | 0 | 0 | 0 | 0 |
| 3-导演 | 0 | 0 | 0 | 0 |
| 4-表演 | 0 | 0 | 0 | 0 |
| 5-摄影 | 0 | 0 | 0 | 0 |
| 6-分组 | 0 | 0 | 0 | 0 |

## Stage Results

| episode | stage | input_path | output_path | verdict | fail_code |
| --- | --- | --- | --- | --- | --- |

## Final Artifacts

- run ledger: `run-ledger.yaml`
- dispatch packets: `dispatch/`
- canonical stage outputs: listed above

## Failure And Retry Routes

| episode | failed_stage | fail_code | retry_start_stage | repair_route |
| --- | --- | --- | --- | --- |

## Completion Verdict

<short final verdict; do not paste stage正文>
```

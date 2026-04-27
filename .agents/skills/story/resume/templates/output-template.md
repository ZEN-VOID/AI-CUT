# Story Resume Output Template

## Output Contract Alignment

| field | alignment |
| --- | --- |
| Required output | 恢复裁决包：`project_root`、tracked command 或 artifact fallback 证据、current step、恢复选项、推荐选项、用户确认、已执行命令、下一 stage handoff；无法恢复时输出 blocker 和最小补充信息。 |
| Output format | 默认 Markdown 用户-facing 恢复报告；可附 YAML/JSON 结构片段，但不得写成阶段业务真源。 |
| Output path | 默认不落盘；若用户明确要求报告，写入 `projects/story/<项目名>/resume/resume-report-YYYYMMDD.md`。 |
| Naming convention | 恢复报告使用 `resume-report-YYYYMMDD.md`；恢复模式使用 ASCII-safe 值；下一入口必须是唯一 skill、命令或 runtime 路径。 |
| Completion gate | 通过 `review/resume-review-gate.md`：项目根锁定、detect/fallback 证据可复核、风险已标注、危险动作已过滤、用户确认已满足、唯一下一入口已给出。 |

## Markdown Shape

```markdown
## 恢复裁决

- project_root: `...`
- mode: `tracked_workflow_resume | artifact_fallback_resume | ...`
- tracked_command: `...`
- current_step: `...`
- risk_level: `low | medium | high | blocked`

## 证据

- workflow detect: `...`
- artifact fallback: `...`
- checked files: `...`

## 恢复选项

A. ...
B. ...
C. ...

推荐：...
需要用户确认：...

## 已执行命令

- `...`

## 下一入口

`...`

## Blocker

...
```

## YAML Shape

```yaml
story_resume:
  project_root: ""
  mode: ""
  tracked_command: ""
  current_step: ""
  evidence:
    workflow_detect: ""
    artifact_fallback: []
  normalized_recovery_options: []
  recommended_option: ""
  user_confirmed_option: ""
  commands_executed: []
  next_stage_handoff: ""
  blockers: []
```

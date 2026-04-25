# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 一个融合型主体参照包，包含当前 mode 对应 artifacts 与旧三段来源映射 |
| Output format | Markdown 合同与报告、JSON 请求对象、主体索引 JSON、manifest、submit plan、submit brief |
| Output path | 所有路径必须位于 `projects/aigc/<项目名>/6-Video/C.主体参照/<episode_id>/` |
| Naming convention | episode 保留 `第N集`；provider id 小写；技能 id 为 `aigc-video-subject-reference` |
| Completion gate | 结构 validator、上下文 audit、AIGC audit 和本地 review checklist 均不出现阻断项 |

## Runtime Summary Shape

```yaml
skill: aigc-video-subject-reference
project_name:
episode_id:
mode:
subject_scope:
source_root: projects/aigc/<项目名>/3-Detail/<episode_id>.json
output_root: projects/aigc/<项目名>/6-Video/C.主体参照/<episode_id>/
artifacts:
  distill:
    - distill/<episode_id>.json
    - distill/<episode_id>.txt
    - distill/_manifest.json
  reference_binding:
    - reference-binding/subject-index.json
    - reference-binding/subject-report.md
    - reference-binding/<episode_id>.json
    - reference-binding/_manifest.json
    - reference-binding/subject-match-report.md
  generation_handoff:
    - generation-handoff/<provider>/submit-plan.json
    - generation-handoff/<provider>/submit-brief.md
next_entry:
review_verdict:
```

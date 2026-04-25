# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 当前 mode 对应的 `distill`、`reference-binding`、`generation-handoff` artifacts，以及三段来源映射 |
| Output format | Markdown 报告、JSON request、JSON manifest、`submit-plan.json`、`submit-brief.md` |
| Output path | 所有路径必须位于 `projects/aigc/<项目名>/6-Video/B.分镜故事板参照/<episode_id>/` |
| Naming convention | episode 保留 `第N集`；provider id 小写；技能 id 为 `aigc-video-storyboard-reference` |
| Completion gate | `validate_skill_2_0.py` 通过；当前 mode 的 review verdict 为 `pass` 或 `pass_with_todo` |

## Final Response Shape

- mode:
- source_root:
- output_root:
- completed_artifacts:
- skipped_by_mode:
- validation:
- next_entry:
- residual_todo:

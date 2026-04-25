# Output Template

## Output Contract Alignment

| Output Contract field | Template binding |
| --- | --- |
| Required output | `最终结果` 必须列出本轮 mode 对应帧级 artifacts 与唯一下一入口 |
| Output format | Markdown closeout + JSON artifact paths + review verdict |
| Output path | 所有路径必须位于 `projects/aigc/<项目名>/6-Video/A.分镜画面参照/<episode_id>/` |
| Naming convention | episode 使用 `第N集`，provider 使用小写 id，旧三段目录不改名 |
| Completion gate | 写明结构验证、AIGC 审计、本地 review 或降级结果 |

## Final Response Shape

```md
最终结果:
- mode: <distill_only|bind_references|handoff_provider|full_chain|compat_migration>
- shot_scope: <shot_id|episode_frame_batch>
- output_root: projects/aigc/<项目名>/6-Video/A.分镜画面参照/<episode_id>/
- next_entry: <provider skill|manual handoff|reference-binding|3-Detail|waiting>

关键产物:
- distill: <path 或 skipped>
- reference-binding: <path 或 skipped>
- generation-handoff: <path 或 skipped>

验证:
- skill_2_0_validator: <pass/fail/not_run>
- aigc_skill_audit: <pass/fail/not_run>
- review_verdict: <pass|pass_with_todo|needs_rework|blocked>

风险 / TODO:
- <非阻断风险或 none>
```

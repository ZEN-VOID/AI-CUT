# $aigc-init Output Template

Use this template for the final user-facing response after scaffold-only `$aigc-init` completes or blocks.

## Output Contract Alignment

| marker | binding |
| --- | --- |
| Required output | current 0-14 project directory scaffold plus project `MEMORY.md` and `CONTEXT/README.md` |
| Output format | Markdown final response referencing directories, `MEMORY.md`, and `CONTEXT/` |
| Output path | `projects/aigc/<项目名>/` |
| Naming convention | stage directory names match current `.agents/skills/aigc/0-14` package names |
| Completion gate | `review/init-review-gate.md` scaffold sufficiency gate |

## Completed

```markdown
已完成 `0-初始化` scaffold。

- project_root: <projects/aigc/项目名>
- scaffold_dirs:
  - 0-初始化
  - 1-分集
  - 2-编剧
  - 3-美学
  - 4-导演
  - 5-表演
  - 6-氛围
  - 7-分镜
  - 8-摄影
  - 9-光影
  - 10-分组
  - 11-主体
  - 12-图像
  - 13-画布
  - 14-审片
- memory: <projects/aigc/项目名/MEMORY.md>
- context_root: <projects/aigc/项目名/CONTEXT/>
- memory_items_captured: <none|summary>
- skipped_removed_artifacts: north_star/init_handoff/story-source/team/STATE/CHANGELOG/source/governance
```

## Blocked

```markdown
`0-初始化` scaffold 暂停。

- block_reason: <missing project name | path outside projects/aigc | directory path conflict | memory overwrite risk | unsafe delete/reset scope | other>
- current_safe_output: <diagnostic only | partial scaffold readback>
- missing_input_or_gate: <specific missing field/gate>
- next_required_user_action: <one concrete action>
```

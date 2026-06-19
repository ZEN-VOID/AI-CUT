# $aigc-init Output Template

Use this template for the final user-facing response after scaffold-plus-memory `$aigc-init` completes or blocks.

## Output Contract Alignment

| marker | binding |
| --- | --- |
| Required output | current `1-10` project directory scaffold plus centralized project `MEMORY.md` and `CONTEXT/README.md`; no project-level `0-初始化/` |
| Output format | Markdown final response referencing directories, `MEMORY.md`, and `CONTEXT/` |
| Output path | `projects/aigc/<项目名>/` |
| Naming convention | stage directory names match current active `.agents/skills/aigc/1-10` runtime stage-root package names; the initialization skill package, leaf, satellite, backup, workflow, and shared packages are not precreated by initialization |
| Completion gate | `review/init-review-gate.md` scaffold and memory sufficiency gate |

## Completed

```markdown
已完成 AIGC project scaffold + project memory。

- project_root: <projects/aigc/项目名>
- scaffold_dirs:
  - 1-分集
  - 2-美学
  - 3-主体
  - 4-编剧
  - 5-导演
  - 6-分镜
  - 7-摄影
  - 8-分组
  - 9-图像
  - 10-画布
- memory: <projects/aigc/项目名/MEMORY.md>
- context_root: <projects/aigc/项目名/CONTEXT/>
- memory_items_captured: <none|summary of requirements/team/reference absorption/context guidance>
- deferred_context_materials: <none|paths/reason>
- skipped_removed_artifacts: north_star/init_handoff/story-source/team/STATE/CHANGELOG/source/governance
- skipped_project_init_folder: 0-初始化
- non_scaffolded_skill_packages: leaf/domain/satellite/backup/workflow/shared packages are created only by owning workflows when needed
```

## Blocked

```markdown
AIGC project scaffold + project memory 暂停。

- block_reason: <missing project name | path outside projects/aigc | directory path conflict | memory overwrite risk | supplied context cannot be summarized safely | unsafe delete/reset scope | other>
- current_safe_output: <diagnostic only | partial scaffold readback>
- missing_input_or_gate: <specific missing field/gate>
- next_required_user_action: <one concrete action>
```

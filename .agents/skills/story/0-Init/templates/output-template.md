# Output Template

本模板定义 `story-init` 输出包的渲染层。它不得改写 `SKILL.md` 的路径、命名或完成门禁。

## Output Contract Alignment

| field | alignment |
| --- | --- |
| Required output | 项目根 `team.yaml`、`STATE.json`、`MEMORY.md`、`CHANGELOG.md`、`CONTEXT/`，以及 `0-Init/north_star.yaml`、`story-source-manifest.yaml`、`init_handoff.yaml` |
| Output format | YAML/JSON/Markdown 项目工件，加一段中文闭环摘要 |
| Output path | `projects/story/<项目名>/` |
| Naming convention | 初始化阶段标识 `0-init`；命令标识 `story-init`；初始化目录固定为 `0-Init/` |
| Completion gate | team、runtime、project memory、0-Init 三件套、provenance 与 review verdict 均通过 |

## User Closeout Shape

```markdown
已完成 `projects/story/<项目名>/` 初始化。

- team 真源：`team.yaml`
- 项目状态：`STATE.json`
- 项目记忆：`MEMORY.md`
- 初始化交接：`0-Init/north_star.yaml`、`0-Init/story-source-manifest.yaml`、`0-Init/init_handoff.yaml`
- 验证结果：<pass | pass_with_followups | needs_rework | blocked>
- 下一入口：`1-Cards`
```

## Artifact Patch Shape

```yaml
artifact_patch_set:
  team_yaml: {}
  state_json: {}
  project_memory: {}
  north_star: {}
  story_source_manifest: {}
  init_handoff: {}
  review_verdict: pass
```

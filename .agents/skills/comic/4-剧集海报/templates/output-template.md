# 剧集海报输出模板

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | `comic_episode_poster_design.v1` JSON；可选 imagegen 生成图记录 |
| Output format | JSON，字段遵循 `episode-poster-design.schema.json` |
| Output path | `projects/comic/<项目名>/4-剧集海报/第N集-剧集海报.json` |
| Naming convention | 单集 `第N集-剧集海报.json`；生图资产 `第N集-剧集海报-vNN.png` 或用户指定稳定名称 |
| Completion gate | validator 通过；review gate 通过；若生图，`.agents/skills/cli/imagegen` 完成并持久化 |

## Delivery Note Shape

```text
mode: design_json | design_json_and_render | repair_existing_json
json_path: projects/comic/<项目名>/4-剧集海报/第N集-剧集海报.json
validated_by: python3 .agents/skills/comic/4-剧集海报/scripts/validate_episode_poster_json.py <json_path>
imagegen_handoff: .agents/skills/cli/imagegen
rendered_assets:
  - <path if requested>
verdict: pass | pass_with_todo | needs_rework | blocked
```

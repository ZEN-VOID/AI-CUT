# Canonical Outputs

## 1. episode 级 JSON carrier

路径：

`projects/<项目名>/4-Design/1-场景/2-设计/第N集/场景设计.json`

最小骨架：

```json
{
  "episode_id": "第N集",
  "source_scene_catalog": "projects/<项目名>/4-Design/1-场景/1-清单/第N集/第N集.json",
  "scene_designs": [
    {
      "scene_key": "scene-name--variant",
      "scene_name": "场景名",
      "scene_variant": "方位或变体",
      "source_scene_ids": ["1-1-10-1"],
      "design_direction": "",
      "reverse_taboos": [],
      "space_prototype": "",
      "architectural_reference": "",
      "structural_language": "",
      "material_palette": "",
      "set_dressing": "",
      "circulation_and_blocking": "",
      "camera_anchor": "",
      "lighting_atmosphere": "",
      "cultural_constraints": "",
      "final_scene_prompt": "",
      "panel_handoff": "",
      "design_markdown_path": "projects/<项目名>/4-Design/1-场景/2-设计/第N集/<scene_key>.md",
      "review_status": "pass|rework",
      "audit_trace": {
        "selected_roles": [],
        "review_note": "",
        "audit_report": ""
      }
    }
  ]
}
```

## 2. per-scene Markdown card

路径：

`projects/<项目名>/4-Design/1-场景/2-设计/第N集/<scene_key>.md`

真源模板：

- `templates/scene-design-card.md`

要求：

- 字段顺序固定，不得随意删栏。
- 缺证据时显式写 `待补定`，不得静默省略。
- `prompt整合` 只保留可直接给下游消费的最终汇总，不堆叠原始思维过程。

## 3. 可选 `_manifest.json`

只在显式要求追溯、审计或批量调试时写出。默认不作为必需产物。

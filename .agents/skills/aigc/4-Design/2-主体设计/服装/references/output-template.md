# Output Template

## 1. `服装设计.json`

```json
{
  "meta": {
    "project_name": "项目名",
    "episode_id": "第1集",
    "source_bridge": "projects/aigc/项目名/4-Design/服装/1-清单/第1集/costume_design_bridge.json",
    "skill_id": "aigc/4-Design/服装/2-设计",
    "generated_at": "2026-04-12T12:00:00-07:00"
  },
  "costumes": [
    {
      "costume_id": "costume-role-001-baseline",
      "role_id": "role-001",
      "canonical_label": "角色名-常服",
      "costume_state": "baseline",
      "design_thesis": {},
      "silhouette_system": {},
      "layering_system": [],
      "material_and_pattern": {},
      "accessory_system": {},
      "mobility_and_continuity": {},
      "negative_constraints": [],
      "structured_markdown_path": "projects/aigc/项目名/4-Design/服装/2-设计/第1集/costume-role-001-baseline-角色名-常服.md"
    }
  ]
}
```

## 2. `costume_design_prompt.json`

```json
{
  "meta": {},
  "costumes": [
    {
      "costume_id": "costume-role-001-baseline",
      "canonical_label": "角色名-常服",
      "prompt_cn": "",
      "render_hints": [],
      "negative_constraints": []
    }
  ]
}
```

## 3. `第N集/<costume_id>-<canonical_label>.md`

必须使用 `templates/服装设计卡.template.md`，最低包含：

1. `物语`
2. `Design Thesis`
3. `Silhouette & Layering`
4. `Material & Pattern`
5. `Accessory & Continuity`
6. `Negative Constraints`
7. `prompt整合`

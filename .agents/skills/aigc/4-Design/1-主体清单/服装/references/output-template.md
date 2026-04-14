# Output Template

## 1. `服装清单.json`

```json
{
  "meta": {
    "schema_version": "aigc/design-costume-list/v1",
    "skill_id": "aigc-design-costume-list",
    "project_name": "项目名",
    "episode_id": "第1集",
    "primary_input": "projects/aigc/项目名/4-Design/角色/1-清单/第1集/角色清单.json",
    "source_inputs": [
      "projects/aigc/项目名/4-Design/角色/1-清单/第1集/角色清单.json",
      "projects/aigc/项目名/3-Detail/第1集.json"
    ],
    "source_role_list": "projects/aigc/项目名/4-Design/角色/1-清单/第1集/角色清单.json",
    "source_episode_detail": "projects/aigc/项目名/3-Detail/第1集.json",
    "source_schema": ".agents/skills/aigc/_shared/director_episode_output.schema.json",
    "generated_at": "2026-04-12T12:00:00-07:00"
  },
  "statistics": {
    "group_count": 8,
    "shot_count": 30,
    "role_count": 5,
    "costume_count": 5,
    "group_map_count": 30
  },
  "group_costume_map": [],
  "costumes": []
}
```

## 2. `服装研究.json`

```json
{
  "meta": {},
  "costumes": [
    {
      "costume_id": "costume-role-001-baseline",
      "role_id": "role-001",
      "canonical_label": "角色名-常服",
      "evidence_ledger": [],
      "silhouette_profile": {},
      "material_profile": {},
      "accessory_profile": {},
      "continuity_profile": {},
      "display_profile": {},
      "chronicle": ""
    }
  ]
}
```

## 3. `costume_design_bridge.json`

```json
{
  "meta": {},
  "costumes": [
    {
      "costume_id": "costume-role-001-baseline",
      "role_id": "role-001",
      "canonical_label": "角色名-常服",
      "costume_state": "baseline",
      "prompt_anchor": "costume / silhouette / material / continuity",
      "silhouette_system": {},
      "layer_system": [],
      "material_palette": [],
      "accessory_system": [],
      "continuity_rules": [],
      "negative_constraints": []
    }
  ]
}
```

## Path Contract

- 默认每集独立目录：
  - `projects/aigc/<项目名>/4-Design/服装/1-清单/第N集/服装清单.json`
  - `projects/aigc/<项目名>/4-Design/服装/1-清单/第N集/服装研究.json`
  - `projects/aigc/<项目名>/4-Design/服装/1-清单/第N集/costume_design_bridge.json`
  - `projects/aigc/<项目名>/4-Design/服装/1-清单/第N集/_manifest.json`

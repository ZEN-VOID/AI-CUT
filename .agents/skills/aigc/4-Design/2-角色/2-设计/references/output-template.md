# Output Template

## 1. `character_design.json`

```json
{
  "meta": {
    "project_name": "项目名",
    "episode_id": "第1集",
    "source_role_list": "projects/项目名/4-Design/2-角色/1-清单/第1集/角色清单.json",
    "source_episode_detail": "projects/项目名/3-Detail/第1集.json",
    "skill_id": "aigc/4-Design/2-角色/2-设计",
    "generated_at": "2026-04-12T12:00:00-07:00"
  },
  "roles": [
    {
      "role_id": "role-001",
      "canonical_name": "角色名",
      "role_tier": "lead",
      "costume_state": "baseline",
      "visual_anchor": {},
      "wardrobe_profile": {},
      "makeup_profile": {},
      "personality_profile": {},
      "scene_compatibility": {},
      "prop_compatibility": {},
      "variation_rules": [],
      "negative_constraints": [],
      "evidence": [],
      "structured_markdown_path": "projects/项目名/4-Design/2-角色/2-设计/第1集/角色名.md"
    }
  ]
}
```

## 2. `第N集/[角色名].md`

必须使用 `templates/角色设计卡.template.md`，最低包含：

1. `物语`
2. `解构`
3. `Visual Anchor`
4. `Wardrobe System`
5. `Makeup & Hair`
6. `Personality & Pose`
7. `Scene / Prop Compatibility`
8. `Negative Constraints`
9. `prompt整合`

## 3. `_manifest.json`

```json
{
  "episode_id": "第1集",
  "selected_roles": [
    "role-001"
  ],
  "source_inputs": [],
  "output_files": [],
  "selected_agents": [],
  "review_status": "pass",
  "audit_status": "pass"
}
```

## Path Contract

- 默认每集独立目录：
  - `projects/<项目名>/4-Design/2-角色/2-设计/第N集/character_design.json`
  - `projects/<项目名>/4-Design/2-角色/2-设计/第N集/[角色名].md`
  - `projects/<项目名>/4-Design/2-角色/2-设计/第N集/_manifest.json`

## Hard Rules

1. `character_design.json` 必须覆盖本轮命中的所有角色，且角色顺序与 `角色清单.json` 中的选角顺序一致。
2. 逐角色 Markdown 必须与 `character_design.json.roles[]` 一一对应。
3. `evidence[]` 至少回链 `group_id + shot_id + source_file`。
4. `negative_constraints` 不能为空数组时，必须能解释它阻止的误读方向。

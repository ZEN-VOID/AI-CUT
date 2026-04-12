# Output Template

## 1. 道具设计.json

```json
{
  "meta": {
    "project_name": "项目名",
    "episode_id": "第1集",
    "skill_id": "aigc/4-Design/4-道具/2-设计",
    "source_bridge": "projects/项目名/4-Design/4-道具/1-清单/第1集/prop_design_bridge.json"
  },
  "props": [
    {
      "prop_id": "prop-001",
      "canonical_name": "令牌",
      "prop_type": "general_prop",
      "evidence": {
        "group_ids": [],
        "shot_ids": [],
        "evidence_ledger": []
      },
      "design_thesis": {
        "design_goal": "",
        "narrative_function": "",
        "silhouette_hook": "",
        "continuity_rule": ""
      },
      "structure_modules": [],
      "material_and_finish": [],
      "wear_marks": [],
      "shot_route": {},
      "physical_character": {},
      "display_profile": {},
      "style_refs": {
        "north_star_ref": "",
        "global_style_ref": "",
        "type_guide_ref": "",
        "master_method_mapping": [],
        "signature_motif": []
      },
      "negative_constraints": [],
      "render_contract": {
        "target_skill_id": "nano-banana-multiview-prop",
        "render_mode": "PROP_DESIGN_SHEET",
        "aspect_ratio": "16:9",
        "layout": "three-column"
      },
      "prompt_anchor": ""
    }
  ]
}
```

## 2. prop_design_prompt.json

```json
{
  "meta": {},
  "props": [
    {
      "prop_id": "prop-001",
      "canonical_name": "令牌",
      "target_skill_id": "nano-banana-multiview-prop",
      "prompt_cn": "",
      "negative_constraints": [],
      "render_hints": {
        "render_mode": "PROP_DESIGN_SHEET",
        "aspect_ratio": "16:9",
        "layout": "three-column"
      }
    }
  ]
}
```

## 3. _manifest.json

```json
{
  "meta": {},
  "inputs": {},
  "outputs": {},
  "selected_agents": [],
  "coverage": {
    "prop_count": 0,
    "has_design_master": true,
    "has_prompt_sidecar": true
  },
  "path_normalization": {
    "requested_output_root": "",
    "canonical_output_root": ""
  }
}
```

## Path Contract

- `projects/<项目名>/4-Design/4-道具/2-设计/第N集/道具设计.json`
- `projects/<项目名>/4-Design/4-道具/2-设计/第N集/prop_design_prompt.json`
- `projects/<项目名>/4-Design/4-道具/2-设计/第N集/_manifest.json`

# Output Template

## 1. 道具设计.json

```json
{
  "meta": {
    "schema_version": "aigc/design-prop-design/v1",
    "skill_id": "aigc-design-prop-design",
    "project_name": "项目名",
    "episode_id": "第1集",
    "primary_input": "projects/aigc/项目名/4-Design/道具/1-清单/第1集/prop_design_bridge.json",
    "source_inputs": [
      "projects/aigc/项目名/4-Design/道具/1-清单/第1集/prop_design_bridge.json",
      "projects/aigc/项目名/4-Design/道具/1-清单/第1集/道具研究.json",
      "projects/aigc/项目名/3-Detail/第1集.json",
      "projects/aigc/项目名/4-Design/道具/1-清单/第1集/道具清单.json"
    ],
    "source_bridge": "projects/aigc/项目名/4-Design/道具/1-清单/第1集/prop_design_bridge.json",
    "source_research": "projects/aigc/项目名/4-Design/道具/1-清单/第1集/道具研究.json",
    "source_detail": "projects/aigc/项目名/3-Detail/第1集.json",
    "source_catalog": "projects/aigc/项目名/4-Design/道具/1-清单/第1集/道具清单.json",
    "generated_at": "2026-04-14T10:00:00-07:00"
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
        "narrative_significance": {
          "is_special": true,
          "level": "critical",
          "story_function": "权力凭证",
          "reason": "该道具承担关键剧情识别，不能降格为普通陈设。",
          "visual_obligation": "按英雄道具处理，优先保证近景/特写可读。",
          "continuity_guard": "关键纹样、缺口和使用痕迹必须连续保留。"
        },
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
        "type_elements_ref": "",
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
  "meta": {
    "schema_version": "aigc/design-prop-design-prompt/v1",
    "skill_id": "aigc-design-prop-design",
    "project_name": "项目名",
    "episode_id": "第1集",
    "primary_input": "projects/aigc/项目名/4-Design/道具/2-设计/第1集/道具设计.json",
    "source_inputs": [
      "projects/aigc/项目名/4-Design/道具/2-设计/第1集/道具设计.json",
      "projects/aigc/项目名/4-Design/道具/1-清单/第1集/prop_design_bridge.json",
      "projects/aigc/项目名/4-Design/道具/1-清单/第1集/道具研究.json",
      "projects/aigc/项目名/3-Detail/第1集.json"
    ],
    "source_design_master": "projects/aigc/项目名/4-Design/道具/2-设计/第1集/道具设计.json",
    "generated_at": "2026-04-14T10:00:00-07:00"
  },
  "props": [
    {
      "prop_id": "prop-001",
      "canonical_name": "令牌",
      "target_skill_id": "nano-banana-multiview-prop",
      "prompt_cn": "",
      "negative_constraints": [],
      "narrative_focus": {
        "level": "critical",
        "visual_obligation": "按英雄道具处理，优先保证近景/特写可读。"
      },
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
  "status": "completed",
  "episode_id": "第1集",
  "input_file": "projects/aigc/项目名/4-Design/道具/1-清单/第1集/prop_design_bridge.json",
  "output_dir": "projects/aigc/项目名/4-Design/道具/2-设计/第1集",
  "output_files": [
    "projects/aigc/项目名/4-Design/道具/2-设计/第1集/道具设计.json",
    "projects/aigc/项目名/4-Design/道具/2-设计/第1集/prop_design_prompt.json",
    "projects/aigc/项目名/4-Design/道具/2-设计/第1集/_manifest.json"
  ],
  "source_inputs": [
    "projects/aigc/项目名/4-Design/道具/1-清单/第1集/prop_design_bridge.json",
    "projects/aigc/项目名/4-Design/道具/1-清单/第1集/道具研究.json",
    "projects/aigc/项目名/3-Detail/第1集.json"
  ],
  "selected_agents": [],
  "statistics": {
    "prop_count": 0,
    "special_narrative_prop_count": 0,
    "has_design_master": true,
    "has_prompt_sidecar": true
  },
  "path_normalization": {
    "requested_output_root": "projects/aigc/项目名/4-Design/道具/2-设计/第1集",
    "canonical_output_root": "projects/aigc/项目名/4-Design/道具/2-设计/第1集"
  },
  "notes": [
    "canonical business truth 是 `道具设计.json`；`prop_design_prompt.json` 与 `_manifest.json` 都是派生 sidecar。"
  ]
}
```

## Path Contract

- `projects/aigc/<项目名>/4-Design/道具/2-设计/第N集/道具设计.json`
- `projects/aigc/<项目名>/4-Design/道具/2-设计/第N集/prop_design_prompt.json`
- `projects/aigc/<项目名>/4-Design/道具/2-设计/第N集/_manifest.json`

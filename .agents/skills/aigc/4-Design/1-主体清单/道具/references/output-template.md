# Output Template

## 1. 道具清单.json

```json
{
  "meta": {
    "schema_version": "aigc/design-prop-list/v1",
    "skill_id": "aigc-design-prop-list",
    "project_name": "项目名",
    "episode_id": "第1集",
    "primary_input": "projects/aigc/项目名/3-Detail/第1集.json",
    "source_inputs": [
      "projects/aigc/项目名/3-Detail/第1集.json"
    ],
    "source_input": "projects/aigc/项目名/3-Detail/第1集.json",
    "source_schema": ".agents/skills/aigc/_shared/director_episode_output.schema.json",
    "generated_at": "2026-04-12T12:00:00-07:00"
  },
  "statistics": {
    "group_count": 8,
    "shot_count": 30,
    "group_map_count": 30,
    "prop_count": 5,
    "groups_without_prop_count": 0
  },
  "group_prop_map": [
    {
      "group_id": "1-1-10",
      "shot_id": "1-1-10-1",
      "scene": "长廊西端入口朝东",
      "roles": "角色A前景入画，角色B远端停住",
      "raw_prop_text": "门把轻晃，旧灯管闪烁",
      "prop_mentions": []
    }
  ],
  "props": []
}
```

## 2. 道具研究.json

```json
{
  "meta": {},
  "props": [
    {
      "prop_id": "prop-001",
      "canonical_name": "令牌",
      "evidence_ledger": [],
      "attribute_profile": {},
      "scene_usage_profile": {},
      "historical_cultural_profile": {},
      "design_bridge_profile": {},
      "display_profile": {},
      "narrative_significance": {
        "is_special": true,
        "level": "critical",
        "story_function": "权力凭证",
        "reason": "该道具直接承担身份确认与剧情推进，不能降格为普通摆件。",
        "visual_obligation": "保持英雄道具级辨识度，优先确保近景/特写一眼可读。",
        "continuity_guard": "跨镜头保持令牌纹样、边口缺损和使用痕迹的连续性。"
      },
      "chronicle": ""
    }
  ]
}
```

## 3. prop_design_bridge.json

```json
{
  "meta": {},
  "props": [
    {
      "prop_id": "prop-001",
      "canonical_name": "令牌",
      "prompt_anchor": "令牌 / material=metal / function=authority / route=macro",
      "structure_modules": [],
      "material_and_finish": [],
      "wear_marks": [],
      "shot_route": {},
      "physical_character": {},
      "narrative_significance": {
        "is_special": true,
        "level": "critical",
        "story_function": "权力凭证",
        "reason": "身份凭证型道具，承担剧情验证功能。",
        "visual_obligation": "不得被弱化成普通背景摆件。",
        "continuity_guard": "关键纹样与边口磨痕必须保持连续。"
      },
      "negative_constraints": []
    }
  ]
}
```

## Naming Contract

- `道具清单.json` 是唯一对象池真源
- `道具研究.json` 是研究层派生 sidecar
- `prop_design_bridge.json` 是桥接层派生 sidecar
- `_manifest.json` 是审计侧车

## Path Contract

- 默认每集独立目录：
  - `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/道具清单.json`
  - `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/道具研究.json`
  - `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/prop_design_bridge.json`

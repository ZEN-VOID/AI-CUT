# {{角色名称}}

source_character_list: `projects/aigc/<项目名>/4-设计/角色/1-清单/角色清单.md`
source_north_star: `projects/aigc/<项目名>/0-初始化/north_star.yaml`
source_team: `projects/aigc/<项目名>/team.yaml`

## 固定画面约束

- Format: full-body costume fitting photo
- Background: solid color background
- Scene Placement: no scene environment, no architecture, no street, no interior set, no props-heavy background
- Prompt Must Include: `full-body costume fitting photo, solid color background, no scene environment`

## 1. 名称 / 首次登场 / 原文描述

- 名称：{{复述清单中相关信息，确保来源准确}}
- 首次登场：{{复述清单中相关信息，确保来源准确}}
- 原文描述：{{复述清单中相关信息，确保来源准确}}

## 2. 研究考据

{{结合 north_star.yaml 中的世界观，思考当前角色符合叙事的文化属性和具象特征；若涉及冷门信息点且本地资料不足，可启用网络搜索并记录来源或不确定性。}}

## 3. 物语

{{结合以上内容展开散文式、诗意化的角色描述，说明身份、欲望、压力、关系、身体和服装如何共同显像。}}

## 4. 解构

## Identity & Story Pressure

Identity Hook: {{identity_hook}}
Narrative Tension: {{narrative_tension}}
Power / Relationship Axis: {{power_axis}}
Differentiation Axes: {{differentiation_axes}}

## Visual Drivers

Style Backbone: {{style_backbone}}
Character Style: {{character_style}}
Reference: {{body_reference}}
Face Signature: {{face_signature}}
Hair Signature: {{hair_signature}}
Silhouette & Build: {{body_signature}}
Costume System: {{costume_signature}}
Accessories & Continuity: {{continuity_signature}}
Design Guardrails: {{design_guardrails}}

## Detailed Character Design

Reference: {{body_reference}}
Age: {{body_age}}
Species / Ethnicity: {{body_species}}
Gender: {{body_gender}}
Occupation: {{body_occupation}}

### Face

- Makeup: {{face_makeup}}
- Face Shape: {{face_shape_cn}}
- Bone Structure: {{face_bone_cn}}
- Eyes: {{face_eyes_cn}}
- Eyelashes: {{face_eyelash_cn}}
- Brows: {{face_brow_cn}}
- Nose: {{face_nose_cn}}
- Mouth: {{face_mouth_cn}}

### Hair

- Style: {{hair_style_cn}}
- Length: {{hair_length_cn}}
- Color: {{hair_color_cn}}
- Texture: {{hair_texture_cn}}
- Hairline: {{hairline_cn}}
- Temple Hair: {{temple_hair_cn}}

### Body

- Overall Style: {{body_style_cn}}
- Height: {{body_height_cn}}
- Weight: {{body_weight_cn}}
- Build: {{body_type_cn}}
- Posture: {{body_posture_cn}}
- Proportion: {{body_ratio_cn}}
- Upper Body:
  - Arms: {{upper_arm_cn}}
  - Fingers: {{finger_cn}}
- Lower Body:
  - Legs: {{leg_cn}}
  - Feet: {{foot_cn}}

### Personality

- Constellation: {{personality_constellation}}
- Blood Type: {{personality_blood_type}}
- Spirit: {{personality_spirit}}
- Emotional Profile: {{personality_emotion}}
- Interests: {{personality_interest}}
- Inner State: {{personality_inner}}
- Identity Core: {{personality_id}}

## Detailed Costume Design

- Era: {{costume_era_cn}}
- Designer / Brand Reference: {{costume_brand_cn}}
- Styling Direction: {{costume_style_cn}}
- Cultural Elements: {{costume_culture_cn}}
- Type: {{costume_type_cn}}
- Material / Attribute: {{costume_attribute_cn}}

### Wearing Details

- Head: {{costume_head_cn}}
- Upper Body: {{costume_upper_cn}}
- Lower Body: {{costume_lower_cn}}
- Footwear: {{costume_foot_cn}}

## Cinematography

Format: full-body costume fitting photo
Shot Size: full body
Background: solid color background
Scene Placement: no scene environment
Composition: {{composition}}
Camera Setup: {{camera_setup}}
Midjourney V8 Parameters: {{midjourney_params}}

## 5. 提示词设计

- 全局风格提示词引用：{{引用 projects/aigc/<项目名>/0-初始化/north_star.yaml 中的“全局风格提示词”}}
- 服装风格引用：{{引用 projects/aigc/<项目名>/0-初始化/north_star.yaml 中的“服装风格”}}
- 固定画面约束：full-body costume fitting photo, solid color background, no scene environment

```text
{{整合 4. 解构的信息，以适用于 AIGC 生图提示词的方式蒸馏组织为自然流畅的英文提示词，2000 字符以内；必须包含 full-body costume fitting photo / solid color background / no scene environment 约束。}}
```

## Review Verdict

```yaml
verdict: pending
source_item: "{{角色清单中的名称}}"
prompt_character_count: 0
reviewer: ""
subagent_status: ""
notes: ""
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成单个角色主体的细目设计 Markdown，包含名称/首次登场/原文描述、研究考据、物语、完整角色解构字段、提示词设计。 |
| Output format | Markdown 单角色设计稿；解构字段固定为 `Identity & Story Pressure`、`Visual Drivers`、`Detailed Character Design`、`Detailed Costume Design`、`Cinematography`。 |
| Output path | Canonical 路径为 `projects/aigc/<项目名>/4-设计/角色/2-设计/<角色名>.md`。 |
| Naming convention | 默认使用 `<角色名>.md`；冲突或不安全字符时使用 `<角色名>__<首次登场ID>.md`。 |
| Completion gate | 角色来自上游清单；已消费 `north_star.yaml` 与 `team.yaml`；正文由 LLM 创作；英文 prompt 融合全局风格和服装风格且不超过 2000 字符；画面固定为纯色背景全身定妆照，不置身具体场景。 |

# {{场景名称}}

source_scene_list: `projects/aigc/<项目名>/4-设计/场景/1-清单/场景清单.md`
source_north_star: `projects/aigc/<项目名>/0-初始化/north_star.yaml`
source_team: `projects/aigc/<项目名>/team.yaml`

## 固定画面约束

- Frame Constraint: pure empty shot / empty establishing space
- Human Presence: no people, no human figures, no body parts, no silhouettes, no reflections of people
- Prompt Must Include: `empty shot, no people, no human figures`

## 1. 名称 / 首次登场 / 原文描述

- 名称：{{复述清单中相关信息，确保来源准确}}
- 首次登场：{{复述清单中相关信息，确保来源准确}}
- 原文描述：{{复述清单中相关信息，确保来源准确}}

## 2. 研究考据

{{结合 north_star.yaml 中的世界观，思考当前场景符合叙事的文化属性和具象特征；若涉及冷门信息点且本地资料不足，可启用网络搜索并记录来源或不确定性。}}

## 3. 物语

{{结合以上内容展开散文式、诗意化的场景描述，说明空间如何承载人物、事件、记忆、权力、时间或情绪。}}

## 4. 解构

## Scene Design

Style Backbone: {{style_backbone}}
Design Type: {{design_type_en}}
Master / Typology Reference: {{design_master_prompt}}
Concept Translation: {{design_concept_prompt}}
Style Detail: {{scene_style_prompt}}
Period and Region: {{period_region_en}}
Function: {{function_attribute_en}}
Spatial Layout: {{space_layout_en}}
Space Type: {{space_type_en}}
Material Detail: {{material_detail_en}}
Structural Detail: {{structural_detail_en}}
Circulation Plan: {{circulation_en}}
Color Theme: {{color_theme_en}}

### Cultural Elements

- Symbolic Design: {{symbolic_design_en}}
- Ornament Pattern: {{ornament_pattern_en}}

Lighting Design (Interior Only): {{lighting_design_en}}
Fixture Design (Interior Only): {{lamp_design_en}}
Furniture Design (Interior Only): {{furniture_design_en}}

### Decor Details (Interior Only)

- Wall Decor: {{wall_decor_en}}
- Floor Material: {{floor_material_en}}

Ecology Design (Landscape Only): {{ecology_design_en}}
Water Design (Landscape Only): {{water_design_en}}
Art Installation (Landscape Only): {{art_installation_en}}

Atmosphere: {{atmosphere_en}}
Weather: {{weather_en}}
Season and Time: {{season_time_en}}

## Cinematography

Shot Size: {{photo_shot_size_en}}
Lens Type: {{lens_type_en}}
Camera Angle: {{camera_angle_en}}
Composition Layout: {{composition_layout_en}}
Composition Method: {{composition_method_en}}
Human Presence: none, pure empty shot
Shape Sense: {{shape_sense_en}}
Line Sense: {{line_sense_en}}
Tonal Sense: {{tonal_sense_en}}
Focus Sense: {{focus_sense_en}}
Rhythm Sense: {{rhythm_sense_en}}
Texture and Surface: {{texture_sense_en}}
Momentum: {{momentum_en}}

### Lighting Setup

- Key Light: {{main_light_en}}
- Fill Light: {{fill_light_en}}
- Back Light: {{back_light_en}}
Lighting Type: {{lighting_type_en}}

### Color

- Hue: {{color_hue_en}}
- Value: {{color_value_en}}
- Saturation: {{color_saturation_en}}
- Temperature: {{color_temperature_en}}
- Color Psychology: {{color_psychology_en}}

### Camera Specifications

- Camera Body: {{camera_model_en}}
- Aperture: {{aperture_en}}
- Shutter: {{shutter_en}}
- ISO: {{iso_en}}
- Focal Length: {{focal_length_en}}
- Resolution: {{resolution_en}}

## 5. 提示词设计

- 全局风格提示词引用：{{引用 projects/aigc/<项目名>/0-初始化/north_star.yaml 中的“全局风格提示词”}}
- 建筑风格引用：{{引用 projects/aigc/<项目名>/0-初始化/north_star.yaml 中的“建筑风格”}}
- 固定画面约束：pure empty shot, no people, no human figures, no silhouettes, no reflections of people

```text
{{整合 4. 解构的信息，以适用于 AIGC 生图提示词的方式蒸馏组织为自然流畅的英文提示词，2000 字符以内；必须包含 pure empty shot / no people / no human figures 约束。}}
```

## Review Verdict

```yaml
verdict: pending
source_item: "{{场景清单中的名称}}"
prompt_character_count: 0
reviewer: ""
subagent_status: ""
notes: ""
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成单个场景主体的细目设计 Markdown，包含名称/首次登场/原文描述、研究考据、物语、完整 Scene Design + Cinematography 解构、提示词设计。 |
| Output format | Markdown 单场景设计稿；解构字段保留固定英文槽位；英文 prompt 放入 fenced text block。 |
| Output path | canonical path 为 `projects/aigc/<项目名>/4-设计/场景/2-设计/S###-<场景名>.md`。 |
| Naming convention | `S###` 来自上游清单顺序，场景名使用清单 canonical 名称并替换非法文件名字符。 |
| Completion gate | 场景来自上游清单；已消费 `north_star.yaml` 与 `team.yaml`；正文由 LLM 创作；英文 prompt 融合全局风格和建筑风格且不超过 2000 字符；画面固定为纯空镜，无人物、人体局部、剪影或人群。 |

# {{场景名称}}

source_scene_list: `projects/aigc/<项目名>/11-主体/场景/1-清单/场景清单.md`
source_north_star: `projects/aigc/<项目名>/0-初始化/north_star.yaml`
source_team_synthesis: `projects/aigc/<项目名>/team.yaml.init_synthesis`

## 固定画面约束

- Frame Constraint: pure empty shot / empty establishing space
- Human Presence: no people, no human figures, no body parts, no silhouettes, no reflections of people
- Prompt Must Include: `empty shot, no people, no human figures`

## 1. 名称 / 首次登场 / 原文描述

- 名称：{{复述清单中相关信息，确保来源准确}}
- 首次登场：{{复述清单中相关信息，确保来源准确}}
- 原文描述：{{复述清单中相关信息，确保来源准确}}

## 2. 研究考据 / Research Brief

{{由 LLM 直接完成研究判断，不得由脚本拼接。研究层必须服务可见空间设计，不写与画面无关的百科堆料；若涉及冷门信息点且本地资料不足，可启用网络搜索并记录来源或不确定性。}}

```yaml
research_brief:
  research_questions:
    - "{{会影响空间形制、材质、光线、地域、年代或仪式可信度的问题}}"
  source_posture:
    project_source:
      - "{{来自场景清单 / north_star.yaml / team.yaml.init_synthesis / MEMORY.md / CONTEXT/ 的强约束}}"
    user_source:
      - "{{用户本轮补充；无则写 none}}"
    common_knowledge:
      - "{{通用建筑 / 地理 / 摄影常识；无则写 none}}"
    scene_inference:
      - "{{基于场景名、关键词和 type_profile 的推断，必须标注为推断}}"
    web_source:
      - "{{若联网使用，记录来源名称或链接摘要；未使用写 not_used}}"
    unresolved:
      - "{{无法确认但会影响设计的点；无则写 none}}"
  evidence_matrix:
    - claim: "{{来源事实或合理推断}}"
      posture: "project_source | user_source | common_knowledge | scene_inference | web_source | unresolved"
      design_impact: "{{它如何影响空间结构、材料、光线、构图或 prompt token}}"
      confidence: "high | medium | low"
  uncertainty_register:
    - uncertainty: "{{不确定项}}"
      risk: "{{误用文化符号 / 年代错置 / 地域混淆 / 材质不可信 / 其他}}"
      handling: "{{保守处理、非特指化、替代方案或需要后续确认}}"
  visual_translation:
    - evidence_or_inference: "{{对应 evidence_matrix 的 claim}}"
      visible_design: "{{转译成可见空间结构、材质、表面、色彩、光源、陈设、地形或构图}}"
      prompt_token_target: "{{后续英文 prompt 中应出现或避免的 token 方向}}"
```

## 3. 物语

{{结合以上内容展开散文式、诗意化的场景描述，说明空间如何承载事件、记忆、权力、时间或情绪；可以讨论人物关系对空间的压力，但不得让人物、人体局部、剪影或倒影出现在画面中。}}

## 4. 解构

主体ID号：{{场景主体 ID，例如 S###；必须与 5. 提示词设计中的主体 ID 号和英文 prompt 开头完全一致}}

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

- 画面基调引用：{{引用 projects/aigc/<项目名>/3-美学/画面基调/全局风格协议.md 中的 Global Style Prompt}}
- 场景风格引用：{{优先引用 projects/aigc/<项目名>/3-美学/第N集/场景风格/场景风格协议.md 中的 Scene Style Prompt；缺失时回退 projects/aigc/<项目名>/3-美学/场景风格/场景风格协议.md，并记录 fallback}}
- 主体 ID 号：{{场景主体 ID，例如 S###；若上游清单已有 ID 则原样沿用}}
- 时间与地域引用：{{引用 research_brief / type_profile / 上游清单 / 项目资料中的时间与地域锚点；若具体信息不确定，写入有来源姿态的保守英文锚点}}
- 固定画面约束：pure empty shot, no people, no human figures, no silhouettes, no reflections of people

### Prompt Evidence Chain

| prompt token group | evidence source | visual translation | uncertainty handling |
| --- | --- | --- | --- |
| subject_id_prefix | {{上游场景清单主体 ID / 文件名前缀 S###}} | {{英文整合提示词开头必须使用的主体 ID 号}} | mandatory |
| style_anchor | {{3-美学/画面基调 / 3-美学/场景风格 / team.yaml.init_synthesis / user_source}} | {{画面基调与场景风格如何转为可见色彩、质感、构图或氛围}} | {{无 / 保守化 / 非特指化}} |
| period_region_tokens | {{research_brief.source_posture / type_profile / user_source}} | {{最终英文 prompt 中必须显式出现的时间与地域英文 token}} | {{无 / 保守化 / 非特指化}} |
| spatial_tokens | {{research_brief.evidence_matrix}} | {{空间结构、尺度、边界、动线}} | {{无 / 保守化 / 非特指化}} |
| material_tokens | {{research_brief.evidence_matrix}} | {{材质、表面、装饰、陈设}} | {{无 / 保守化 / 非特指化}} |
| light_camera_tokens | {{Cinematography}} | {{光线、镜头、构图、景深}} | {{无 / 保守化 / 非特指化}} |
| deconstruction_coverage | {{## 4. 解构 / Scene Design / Cinematography}} | {{说明 Scene Design 与 Cinematography 的全部有效槽位如何被整合进英文 prompt；若压缩、合并或剔除，写明理由}} | {{无 / 合并 / 剔除并说明}} |
| empty_shot_tokens | fixed visual constraint | empty shot, no people, no human figures | mandatory |

```text
{{英文整合提示词必须以主体 ID 号开头，格式为 "<主体ID>: ..."; 整合对象是 4. 解构的全部有效信息，而不是只拼接主体 ID、风格、时间地域和负向词；必须把 Scene Design 与 Cinematography 中的空间结构、尺度边界、材质表面、色彩陈设、动线、镜头距离、构图、光线、焦段、景深和氛围节奏蒸馏组织为自然流畅、可生成画面的英文整合提示词，2000 字符以内；必须显式包含时间 token、地域 token、建筑/空间风格 token，以及 pure empty shot / no people / no human figures 约束。}}
```

## Review Verdict

```yaml
verdict: pending
source_item: "{{场景清单中的名称}}"
prompt_character_count: 0
research_brief_status: "pending"
source_posture_status: "pending"
uncertainty_status: "pending"
prompt_evidence_chain_status: "pending"
fixed_visual_status: "pending"
reviewer: ""
review_status: ""
notes: ""
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成单个场景主体的细目设计 Markdown，包含名称/首次登场/原文描述、研究考据 / Research Brief、物语、完整 Scene Design + Cinematography 解构、提示词设计。 |
| Output format | Markdown 单场景设计稿；`## 4. 解构` 标题下方必须先写 `主体ID号：<主体ID>`，再写固定英文槽位；英文 prompt 放入 fenced text block。 |
| Output path | canonical path 为 `projects/aigc/<项目名>/11-主体/场景/2-设计/S###-<场景名>.md`。 |
| Naming convention | `S###` 来自上游清单顺序，场景名使用清单 canonical 名称并替换非法文件名字符。 |
| Completion gate | 场景来自上游清单；已消费 `3-美学/画面基调/全局风格协议.md`、当前集优先/项目级回退的 `3-美学/场景风格/场景风格协议.md`、`north_star.yaml` 与 `team.yaml.init_synthesis`；正文由 LLM 创作；研究层包含 research_brief / source_posture / uncertainty_register / visual_translation；`## 4. 解构` 下的主体 ID、`## 5. 提示词设计` 的主体 ID 和英文 prompt 开头三者一致；英文 prompt 以主体 ID 号开头，有 prompt_evidence_chain，已整合 `## 4. 解构` 的 Scene Design 与 Cinematography 全部有效信息，融合 `画面基调.Global Style Prompt + 场景风格.Scene Style Prompt`、时间与地域锚点且不超过 2000 字符；画面固定为纯空镜，无人物、人体局部、剪影或人群。 |

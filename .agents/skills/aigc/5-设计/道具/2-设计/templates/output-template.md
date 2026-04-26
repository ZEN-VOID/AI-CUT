# {{道具名称}}

source_prop_list: `projects/aigc/<项目名>/5-设计/道具/1-清单/道具清单.md`
source_north_star: `projects/aigc/<项目名>/0-初始化/north_star.yaml`
source_team: `projects/aigc/<项目名>/team.yaml`

## 固定画面约束

- Type: close-up single prop shot
- Camera Angle: 45-degree view
- Background: solid color background
- Scene Placement: no scene environment, no tabletop scene, no room set, no street, no hands holding the prop
- Prompt Must Include: `close-up prop shot, 45-degree view, solid color background, no scene environment`

## 1. 名称 / 首次登场 / 原文描述

- 名称：{{复述清单中相关信息，确保来源准确}}
- 首次登场：{{复述清单中相关信息，确保来源准确}}
- 原文描述：{{复述清单中相关信息，确保来源准确}}

## 2. 研究考据

{{结合 north_star.yaml 中的世界观，思考当前道具符合叙事的文化属性和具象特征；若涉及冷门信息点且本地资料不足，可启用网络搜索并记录来源或不确定性。}}

## 3. 物语

{{结合以上内容展开散文式、诗意化的道具描述，说明物件的功能、主人痕迹、时间沉积、象征压力和视觉记忆点。}}

## 4. 解构

## Photography

Type: close-up single prop shot
Shot Size: close-up
Camera Angle: 45-degree view
Background: solid color background
Scene Placement: no scene environment, no hands holding the prop

## Prop Design

Style Backbone: {{style_backbone}}
Prop Type: {{prop_type_en}}
Design Inspiration: {{design_inspiration_en}}
Period Attribute: {{period_attribute_en}}
Functionality: {{functionality_en}}

Shape Sense: {{shape_en}}
Line Sense: {{line_sense_en}}
Dimensional Layering: {{volume_en}}
Size: {{size_en}}

Material Detail: {{material_en}}
Texture Detail: {{texture_en}}
Decoration Detail: {{decoration_en}}
Pattern Detail: {{pattern_en}}

Art Elements: {{art_element_en}}
Cultural Elements: {{culture_en}}
Ergonomics: {{ergonomics_en}}

## 5. 提示词设计

- 全局风格提示词引用：{{引用 projects/aigc/<项目名>/0-初始化/north_star.yaml 中的“全局风格提示词”}}
- 物品风格引用：{{引用 projects/aigc/<项目名>/0-初始化/north_star.yaml 中的“物品风格”}}
- 固定画面约束：close-up prop shot, 45-degree view, solid color background, no scene environment

```text
{{整合 4. 解构的信息，以适用于 AIGC 生图提示词的方式蒸馏组织为自然流畅的英文提示词，2000 字符以内；必须包含 close-up prop shot / 45-degree view / solid color background / no scene environment 约束。}}
```

## Review Verdict

```yaml
verdict: pending
source_item: "{{道具清单中的名称}}"
prompt_character_count: 0
reviewer: ""
subagent_status: ""
notes: ""
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板生成单个道具主体的细目设计 Markdown，包含名称/首次登场/原文描述、研究考据、物语、完整 Photography + Prop Design 解构、提示词设计。 |
| Output format | Markdown 单道具设计稿；解构字段固定为 `Photography` 与 `Prop Design`；英文 prompt 放入 fenced text block。 |
| Output path | canonical path 为 `projects/aigc/<项目名>/5-设计/道具/2-设计/<安全文件名>.md`。 |
| Naming convention | 文件名优先使用清单 `名称` 的安全化结果；同名或多状态道具追加首次登场 ID 或状态。 |
| Completion gate | 道具来自上游清单；已消费 `north_star.yaml` 与 `team.yaml`；正文由 LLM 创作；英文 prompt 融合全局风格和物品风格且不超过 2000 字符；画面固定为纯色背景近景特写、45 度视角，不置身具体场景。 |

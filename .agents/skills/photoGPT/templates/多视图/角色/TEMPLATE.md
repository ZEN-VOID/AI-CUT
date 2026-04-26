# Template: 多视图 / 角色

Template ID: `photoGPT.多视图.角色.v1`

## Required Fields

- `character_id`
- `character_name`
- `desc`
- 一张或多张角色参考图

## Input Roles

- 主参考图：提供角色身份、脸、发型、体态、服装和风格。
- 辅助参考图：只补充表情、姿态、服装层次或局部细节。

## Prompt Frame

```text
### 角色ID: <character_id>
保留参考图的画面风格和角色核心形象，根据以下要求调整为专业多视图角色设计页：

【设计主体】
<desc>。全身站立像，双脚可见，中性简洁背景，角色概念设计图风格。

【画布规格】
Create one professional CHARACTER_DESIGN_SHEET on a 4096x2304 landscape canvas (16:9). Use dark gray base (#1a1a1a) with subtle grid overlay (#2A2A2A). Keep character zones clean and do not render environment scene. Rendering style should be inherited from the reference image.

【三栏布局】
LEFT COLUMN (15%): COLOR PALETTE 4x3 swatch grid; HAIR STYLE structure, length, texture and value hints.
CENTER COLUMN (50%): FULL BODY VIEWS: front view, side 3/4 view, back view. Feet bottom-aligned, stable scale, 15-20px gap.
RIGHT COLUMN (35%): OUTFIT LAYERING 2x3 flat-lay; ACCESSORIES wearables only; ACTION POSES 3 slots; FACIAL EXPRESSIONS 2x3 slots.

【强制约束】
- Output must be CHARACTER_DESIGN_SHEET, not a poster or 3x3 storyboard.
- Character identity lock across all views: same face, hair, skin tone, body proportion and costume logic.
- No scene/environment/background narrative.
- No props/weapons/hand-held objects unless user explicitly requires them.
- Must display one fixed top-left identity badge: <character_id> + <character_name>.
```

## Negative Constraints

- 不混入多个角色身份。
- 不生成完整场景叙事背景。
- 不把 layout reference 的人物身份复制过来。

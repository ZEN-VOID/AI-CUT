# Template: 多视图 / 服装

Template ID: `photoGPT.多视图.服装.v1`

## Required Fields

- `costume_id`
- `costume_name`
- `desc`
- 一张或多张服装参考图

## Input Roles

- 主参考图：提供服装整体剪裁、廓形、层次和配色。
- 辅助参考图：提供面料、纹样、配饰、穿着状态或细节工艺。

## Prompt Frame

```text
### 服装ID: <costume_id>
保留参考图中的服装核心设计语言，根据以下要求调整为专业多视图服装设计页：

【设计主体】
<desc>。展示同一套服装的正面、侧面、背面、局部细节和层次拆解；服装应自然呈现可穿着结构，但不更换服装身份。

【画布规格】
Create one professional COSTUME_DESIGN_SHEET on a 4096x2304 landscape canvas (16:9). Use neutral dark gray base with subtle grid overlay. Keep a clean production design layout with stable gutters and readable modules.

【布局模块】
LEFT COLUMN: color palette, fabric/material swatches, trim and accessory chips.
CENTER COLUMN: front view, side 3/4 view, back view of the same outfit, aligned to a shared baseline and stable scale.
RIGHT COLUMN: layering breakdown, close-ups of seams/fasteners/embroidery/wear marks, and 2-3 motion fit examples.

【强制约束】
- Output must be COSTUME_DESIGN_SHEET, not fashion poster or model lookbook.
- Same costume identity across all modules: silhouette, material, color hierarchy, closures and decoration cannot drift.
- If a body/mannequin is used, keep it neutral and secondary; do not create a new character identity.
- Must display one fixed top-left identity badge: <costume_id> + <costume_name>.
```

## Negative Constraints

- 不把服装变成不同套装。
- 不引入强人物身份、复杂场景或广告海报构图。
- 不丢失面料、剪裁、装饰和层次结构。

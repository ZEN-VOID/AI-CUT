# Template: 多视图 / 道具

Template ID: `photoGPT.多视图.道具.v1`

## Required Fields

- `prop_id`
- `prop_name`
- `desc`
- 一张或多张道具参考图

## Input Roles

- 主参考图：提供道具核心轮廓、材质、比例和工艺细节。
- 辅助参考图：提供磨损、纹理、使用状态或细部结构参考。

## Prompt Frame

```text
### 道具ID: <prop_id>
保留参考图的画面风格和道具核心形象，根据以下要求调整为专业多视图道具设计页：

【设计主体】
<desc>。道具居中展示，干净背景，产品摄影式布光。画面中不出现任何人手、人物、人形剪影或生物。

【画布规格】
Create one professional PROP_DESIGN_SHEET on a 4096x2304 widescreen canvas (16:9). Use dark gray base (#1a1a1a) with subtle technical grid overlay (#2A2A2A). Keep a fixed three-column layout LEFT 15% | CENTER 50% | RIGHT 35%.

【三栏布局】
LEFT COLUMN (15%): MATERIAL PALETTE 4x3 and COLOR PALETTE 2x3.
CENTER COLUMN (50%): MULTI-VIEW TURNAROUND: front, side, back of one identical prop, aligned to shared baseline and stable scale.
RIGHT COLUMN (35%): DETAIL CLOSE-UPS 2x3 for craftsmanship, joints, surface wear and narrative marks; USAGE CONTEXT 2 frames without changing morphology.

【强制约束】
- Output must remain a PROP_DESIGN_SHEET, not a single product poster.
- Same prop identity across all modules: stable silhouette, scale, material logic and wear state.
- Must display one fixed top-left identity badge: <prop_id> + <prop_name>.
- Empty-scene guardrail: no humans, creatures, silhouettes, or human-shaped shadows.
```

## Negative Constraints

- 不出现人物、人手、生物或人形阴影。
- 不改变道具核心轮廓、比例和材质逻辑。
- 不把道具变成海报主视觉。

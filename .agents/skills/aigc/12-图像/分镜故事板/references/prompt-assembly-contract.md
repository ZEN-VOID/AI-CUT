# Prompt Assembly Contract

本文件定义 step1 的 prompt 组装规则：直接引用 `10-分组` 对应分镜组的完整内容作为生图基础，先插入 source comprehension、可追溯的 storyboard frame-unit plan、每格 panel 描述、角色头顶名称标注、annotation plan、layout aspect decision 和 accepted spatial floor plan，并添加任务执行前缀明确黑白线稿分镜手稿、受控彩色标注系统、panel 图片比例、文字区、sheet 画布比例裁决和空间站位保真要求。

## Task Execution Prefix

每条组级 prompt 必须逐字以下列文本开头；这是启动生图任务的任务执行词，不得替换为项目全局风格词：

```text
Create a storyboard sheet in standard storyboard manuscript style: black-and-white clean line art as the image base, with only the following annotation colors added on top: red arrows for body movement, blue arrows for camera movement, green marks for framing/composition notes, orange marks for lighting direction, purple marks for emotion/sound/narrative emphasis, and black text for character name labels above each visible character, short shot notes, and panel labels. Character name labels must exactly match the character names in the grouped shot source/YAML; do not rename, abbreviate, translate, or guess names. Do not use color for rendering characters, costumes, backgrounds, lighting, atmosphere, or global style keywords. Use the complete grouped shot source below as the foundation. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Each panel must contain a locked 16:9 image box with a visible rectangular border, plus a separate storyboard description text strip directly below that image box. Use the supplied Layout Aspect Decision and Panel Geometry Blueprint: draw the sheet according to the selected grid, normalized cell coordinates, fixed 16:9 image_box coordinates, text_strip coordinates, margins, and gutters. Do not squeeze, stretch, crop, or distort any panel image box to fill a mismatched cell; leave clean whitespace inside the cell if needed. Use pagination or multiple sheets when one legal canvas cannot preserve locked 16:9 image boxes and readable text strips. Preserve the identities, silhouettes, spatial structure, and key prop shapes from the bound character, scene, and prop reference images even though the final image base is black-and-white line art. Render the final storyboard sheet at 4K resolution so every panel image, annotation, character name label, and description remains readable. Treat the Complete Group Source as evidence and source text, not as a visual style directive; upstream color, lighting, atmosphere, cinematic, lens, grain, film, rendering, or global style phrases are quarantined and must not override this black-and-white line-art style lock. Before drawing, obey the supplied Style Lock Spec, Visual Prompt Atoms, and Floor Plan To Panel Mapping; if any of those blocks are missing, stop and rework the prompt instead of generating.
```

任务执行前缀之后先进入 `Style Lock Spec`，再进入 `Source Comprehension`、`Storyboard Frame Units`、`Visual Prompt Atoms`、`Layout Aspect Decision`、`Accepted Spatial Floor Plan` 与 `Floor Plan To Panel Mapping`；最后进入 `Complete Group Source From 10-分组`。`Complete Group Source` 只作为源证据和事实边界，不得作为风格、光影、渲染或构图美化指令；不插入解释性说明、provider 参数、执行日志或额外任务指令。

## Style Lock Spec

- `Style Lock Spec` 是每条 prompt 中的硬性画风闸门，必须位于 `Source Comprehension` 之前。
- 必填字段：`base_rendering: black_white_clean_line_art`、`allowed_color_layer: annotation_only`、`forbidden_rendering_layers`、`upstream_style_quarantine`、`reference_usage_policy`、`style_drift_stop_condition`。
- `forbidden_rendering_layers` 必须至少列出：彩色电影 still、写实渲染、项目全局画风、场景参照光影氛围、服装/背景/灯光上色、胶片颗粒/镜头语言/电影美学作为画风指令。
- `upstream_style_quarantine` 必须逐项记录完整组稿中出现但不得作为生图风格的词，例如 `全局风格`、`1993年香港武侠电影美学`、`35mm胶片颗粒`、`体积光`、`光影和氛围与场景参照图保持一致` 等；这些词只能作为源文本证据留在 `Complete Group Source`，不能出现在最终可执行绘制指令中。
- 参照图只用于身份、轮廓、空间结构和道具外形；不得把参照图颜色、光影、质感或氛围继承到 storyboard sheet。
- 若 prompt 中没有 `Style Lock Spec`，或 `visual_prompt_atoms` 仍含电影风格/彩色渲染词，必须标记 `FAIL-SHEET-STYLE-LOCK` 并返工；不得用“前缀已经声明黑白线稿”作为通过理由。

## Source Comprehension

- `Source Comprehension` 是 prompt 中的源内容理解摘要，用于让模型在生成前理解现有分镜组，而不是补写新剧情。
- 必须包含：本组叙事功能、连续动作链、空间锚点、角色状态锚点、道具状态锚点、视觉转折、必须保留的源事实、禁止补写项。
- 每项必须能回指 `Complete Group Source From 10-分组`；不得写成“综合理解”“保持一致”等泛化表述。

## Storyboard Frame Units

- `Storyboard Frame Units` 是 prompt 中的轻量 panel plan，用于告诉生图模型 storyboard 格数、每格视觉节拍、每格下方文字描述、每个角色头顶名称标注和每格标注计划。
- frame unit 必须来自 `references/group-source-extraction.md` 识别结果，可回指 `group_body`，不得补写上游没有的剧情事实。
- frame unit 的编号是 `panel_no`，不是原始 `分镜N`。原始 `分镜N` 只出现在 `source_shot_labels` 中，用于追溯。
- 允许 `panel_no` 与 `source_shot_labels` 一对多、多对一或一对一；不得把 `分镜标签数 = storyboard panel 数` 作为默认规则。
- 每个 frame unit 必须包含 `panel_description`，作为该 panel 图片下方的文字内容；`panel_description` 只能由 LLM 从对应 `source_span` 和分组稿分镜描述原文保真精简整合，不得发明新动作、情绪结果或角色事实。
- `panel_description_density` 默认写 `rich_brief`：每格下方文字应是 1-2 句可读分镜说明，推荐 40-90 个中文字符，最多 120 个中文字符；同一 sheet panel 很多时可压缩到 25-60 个中文字符。内容优先级为：主体/动作/画面状态 > 景别/构图/运镜 > 情绪/声音/叙事强调 > 关键场景/道具。删除重复风格词、过长对白、执行说明和无关修饰。
- 每个 frame unit 必须记录 `panel_image_aspect_ratio`，默认值为 `16:9`；只有用户显式指定时才可改为 `9:16` 或其他比例。
- 每个 frame unit 必须记录 `character_name_labels`，用于在每个可见角色头顶放置黑色文本角色名；角色名必须与分组稿/组底 YAML `角色` 字段完全一致。
- 每个 frame unit 必须记录 `annotation_plan`。如果某类标注在该 panel 不适用，写 `none`；不得为了填满颜色系统而发明不存在的运动、机位、灯光、声音或叙事强调。
- 若 frame-unit 识别为 `partial`，必须回到完整组稿自动返工到 `ready`；无法稳定裁决时只可 failed 报告，不得以等待人工确认或 prompt-only 结束。

## Visual Prompt Atoms

- `Visual Prompt Atoms` 是传给 imagegen 的可执行绘制原子，必须由 LLM 基于 `source_span`、`panel_description`、`annotation_plan` 和 `floor_plan_to_panel_mapping` 逐 panel 写出；不得由脚本、模板、关键词替换或通用句架批量生成。
- 每个 panel 必须包含以下 atom 字段：
  - `draw_subjects`: 只列本 panel 可见主体，角色名与 YAML 一致。
  - `subject_actions`: 当前 panel 要画出的可见动作或状态，必须能回指 `source_span`。
  - `spatial_positions`: 角色/道具在平面图中的位置、朝向、相对距离和左右/前后关系。
  - `camera_framing`: 景别、视角、构图或摄影机方向；无源证据时写 `none`，不得补写。
  - `line_art_instruction`: 黑白线稿、清晰轮廓、少量灰度阴影、无彩色渲染。
  - `annotation_overlay`: 红/蓝/绿/橙/紫/黑色标注的具体落点；不适用写 `none`。
  - `text_strip`: 下方文字区内容，必须等于该 panel 的 `panel_description`。
  - `negative_prompt_atoms`: 本 panel 禁止出现的风格漂移、站位漂移和新增事实。
- `Visual Prompt Atoms` 必须比 `panel_description` 更可执行：不能只写“表现紧张气氛”“保持武侠风格”“突出动作感”等泛化句；每个 atom 至少包含一个可画对象、一个空间锚点和一个源事实边界。
- 生成 prompt 的最终绘制指令只能消费 `Style Lock Spec`、`Storyboard Frame Units`、`Visual Prompt Atoms`、`Layout Aspect Decision`、`Accepted Spatial Floor Plan`、`Floor Plan To Panel Mapping` 和 `Reference Subjects`；`Complete Group Source` 是审计证据，不是直接绘制指令。

## Prompt Body

- `prompt_body` 必须直接引用对应分镜组的完整内容，包括组正文和组底 YAML；YAML 同时用于主体参照绑定。
- 保留组内风格句、类型元素、画面风格、对白、动作画面、分镜明细、`分镜N:` 顺序和底部 YAML；默认忽略相邻组间连接件，不把连接件写入 storyboard prompt。
- 不翻译、不摘要、不改写剧情事实。
- 可在结构化侧车中记录 `shot_count`、`group_id` 和 YAML 主体，但不要把报告字段插入 prompt 正文。
- prompt 的画风要求只允许使用任务执行前缀中的“标准分镜手稿风格黑白线稿基底 + 受控彩色标注系统”；不得援引项目全局风格、north star 全局画风或场景图风格作为风格词。
- source block 中保留的上游风格句只作为完整分镜组内容证据，不得被解释为 imagegen style directive。
- prompt 必须在 `Style Lock Spec.upstream_style_quarantine` 中显式隔离 source block 里的上游画风、光影、氛围、镜头质感和电影风格句；隔离后的词不得进入 `Visual Prompt Atoms` 的 `line_art_instruction` 或最终 imagegen 绘制句。
- 绑定的角色、场景、道具参照图只用于主体身份、轮廓、空间结构和关键道具外形保真，不用于继承彩色画风、光影或氛围。
- 角色头顶名称标注属于黑色文本标注层，名称来源必须回指完整分镜组内容或组底 YAML；不得从参照图文件名、外观、正文泛称或模型猜测中改写角色名。
- 彩色标注系统只用于信息标注，不得把颜色涂进角色、服装、背景、光影或氛围。

## Layout Semantics

任务执行前缀已声明：

- 多格 storyboard；
- frame unit 基于视觉节拍识别，不强制一一对应原始 `分镜N`；
- 最终成图按 4K 分辨率生成，保障小 panel 可读性；
- 每个 panel 的图片区默认锁定为可见边框的 16:9 image box；
- 每个 panel 的图片下方必须有分镜描述文字区；
- 根据 storyboard panel 数先反推 sheet layout、整图比例、`gpt-image-2` 合法尺寸和 `panel_geometry_blueprint`；
- frame units 过多时允许分页或多 sheet 计划，并在 plan/report 中记录；
- 画面基底统一为标准黑白线稿分镜手稿，不使用全局风格词；
- 彩色只用于标注系统：红色箭头=身体运动，蓝色箭头=摄影机运动，绿色标记=取景/构图笔记，橙色标记=灯光方向，紫色标记=情绪/声音/叙事强调，黑色文本=角色头顶名称、简短镜头笔记和面板标签。

执行者不得再额外硬编码格数或整图比例，除非用户明确要求某种布局。默认必须先用 `panel_count`、目标 panel 图片比例、下方文字区和标注安全边距计算 `layout_aspect_decision`，并输出 `panel_geometry_blueprint` 来锁定每个 panel 的 cell、16:9 image box 和 text strip。

## Layout Aspect Decision

- `Layout Aspect Decision` 必须跟随 `Storyboard Frame Units`，作为 prompt 中的明确布局裁决。
- 必填字段：`panel_count`、`target_panel_image_aspect_ratio`、`effective_panel_slot_ratio`、`panel_geometry_blueprint`、`candidate_grids`、`selected_grid`、`selected_sheet_aspect_ratio`、`selected_sheet_size`、`provider_size_constraints`、`panel_image_box_ratio_error`、`pagination_or_multi_sheet_decision`、`rationale`。
- `selected_sheet_size` 必须满足 `gpt-image-2` 尺寸范围：最大边 `<=3840px`、宽高为 `16px` 倍数、长短边比例 `<=3:1`、总像素 `655360..8294400`。
- `panel_geometry_blueprint` 必须为每个 panel 记录 `cell_norm`、`image_box_norm`、`image_box_aspect_ratio: 16:9`、`text_strip_norm` 和 `ratio_error`；`image_box` 必须锁定 16:9，允许 cell 内留白，不允许拉伸填满 cell。
- 若候选布局无法让每个 panel 图片框误差 `<= 0.06`，prompt 必须声明分页或多 sheet；不得要求模型在固定画布里压缩 panel。

## Accepted Spatial Floor Plan

- `Accepted Spatial Floor Plan` 是 storyboard sheet 生成前的强制空间输入，来源于 `references/spatial-floor-plan-contract.md`。
- 必须记录 `floor_plan_id`、`top_view_diagram_path`、`acceptance_verdict: accepted`、角色站位、道具位置、摄影机位置/方向、运动路径、与上一组的空间连续性。
- 若 `acceptance_verdict` 不是 `accepted`，prompt 包只能作为内部 draft，必须自动回到 floor plan 生成/验收返工；无法恢复时 failed 报告，不得停在等待确认状态。
- storyboard sheet prompt 必须要求每个 panel 的角色站位、朝向、相对距离、道具位置和摄影机方向与 accepted floor plan 一致；不得只按画面美观重新摆位。

## Floor Plan To Panel Mapping

- `Floor Plan To Panel Mapping` 是把 accepted top-view 平面图转译到每个 storyboard panel 的硬门槛；只附平面图路径或缩略图不够。
- 必填字段：`panel_no`、`floor_plan_zone`、`characters_position_and_facing`、`props_position`、`camera_position_and_direction`、`movement_path_used`、`unchanged_anchors_from_floor_plan`、`allowed_composition_variation`、`forbidden_spatial_drift`。
- 每个 panel 的 `floor_plan_zone` 必须来自 accepted floor plan 的场景边界、角色站位或摄影机锥形视野；不得为了画面漂亮把角色挪到平面图未授权位置。
- `allowed_composition_variation` 只允许说明景别、裁切和透视转换；不得改变左右关系、内外线、前后距离、角色朝向、道具相对位置或摄影机方向。
- 若某 panel 无法从平面图找到对应区域或摄影机方向，必须回到 `spatial_floor_plan` 或 `storyboard_frame_units` 返工；不得直接 imagegen。

## Prompt Package Shape

Markdown prompt 包推荐：

```markdown
## 1-1-1

Create a storyboard sheet in standard storyboard manuscript style: black-and-white clean line art as the image base, with only the following annotation colors added on top: red arrows for body movement, blue arrows for camera movement, green marks for framing/composition notes, orange marks for lighting direction, purple marks for emotion/sound/narrative emphasis, and black text for character name labels above each visible character, short shot notes, and panel labels. Character name labels must exactly match the character names in the grouped shot source/YAML; do not rename, abbreviate, translate, or guess names. Do not use color for rendering characters, costumes, backgrounds, lighting, atmosphere, or global style keywords. Use the complete grouped shot source below as the foundation. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Each panel must contain a locked 16:9 image box with a visible rectangular border, plus a separate storyboard description text strip directly below that image box. Use the supplied Layout Aspect Decision and Panel Geometry Blueprint: draw the sheet according to the selected grid, normalized cell coordinates, fixed 16:9 image_box coordinates, text_strip coordinates, margins, and gutters. Do not squeeze, stretch, crop, or distort any panel image box to fill a mismatched cell; leave clean whitespace inside the cell if needed. Use pagination or multiple sheets when one legal canvas cannot preserve locked 16:9 image boxes and readable text strips. Preserve the identities, silhouettes, spatial structure, and key prop shapes from the bound character, scene, and prop reference images even though the final image base is black-and-white line art. Render the final storyboard sheet at 4K resolution so every panel image, annotation, character name label, and description remains readable. Treat the Complete Group Source as evidence and source text, not as a visual style directive; upstream color, lighting, atmosphere, cinematic, lens, grain, film, rendering, or global style phrases are quarantined and must not override this black-and-white line-art style lock. Before drawing, obey the supplied Style Lock Spec, Visual Prompt Atoms, and Floor Plan To Panel Mapping; if any of those blocks are missing, stop and rework the prompt instead of generating.

### Style Lock Spec

- base_rendering: black_white_clean_line_art
- allowed_color_layer: annotation_only
- forbidden_rendering_layers:
  - color_cinematic_still
  - photorealistic_rendering
  - global_style_keywords
  - scene_lighting_atmosphere
  - costume_background_lighting_color_rendering
- upstream_style_quarantine:
  - source_phrase: <源文本中的上游风格句>
    treatment: evidence_only_not_style_directive
- reference_usage_policy: identity_silhouette_spatial_structure_prop_shape_only
- style_drift_stop_condition: missing_style_lock_or_color_rendering_terms_in_visual_prompt_atoms

### Source Comprehension

- narrative_function: <本组在当前段落中的叙事功能>
- action_chain: <按源正文整理的连续动作链>
- spatial_anchors: <场景位置、入出场、相对方位等锚点>
- character_state_anchors: <角色状态和关系锚点>
- prop_state_anchors: <关键道具状态>
- visual_turning_points: <需要形成独立 panel 的视觉转折>
- must_preserve_source_facts: <必须保留的源事实>
- forbidden_inventions: <不得补写的事实边界>

### Storyboard Frame Units

1. panel_no: 1
   panel_image_aspect_ratio: 16:9
   visual_beat: <从组正文中识别出的第一个 storyboard panel 视觉节拍>
   panel_description: <rich_brief；从 source_span 和分组稿分镜描述原文保真精简为 1-2 句>
   panel_description_density: rich_brief
   character_name_labels:
     - <角色名>: above_character_head
   annotation_plan:
     red_body_movement_arrows: <身体运动方向；不适用写 none>
     blue_camera_movement_arrows: <摄影机运动方向；不适用写 none>
     green_framing_composition_marks: <取景/构图笔记；不适用写 none>
     orange_lighting_direction_marks: <灯光方向；不适用写 none>
     purple_emotion_sound_narrative_marks: <情绪/声音/叙事强调；不适用写 none>
     black_text_notes_and_panel_label: <简短镜头笔记和面板标签>
   source_shot_labels: 分镜1
   source_span: <可回指的源文本片段或摘要>

2. panel_no: 2
   panel_image_aspect_ratio: 16:9
   visual_beat: <可合并或拆分后的 storyboard panel 视觉节拍>
   panel_description: <rich_brief；从 source_span 和分组稿分镜描述原文保真精简为 1-2 句>
   panel_description_density: rich_brief
   character_name_labels:
     - <角色名>: above_character_head
   annotation_plan:
     red_body_movement_arrows: <身体运动方向；不适用写 none>
     blue_camera_movement_arrows: <摄影机运动方向；不适用写 none>
     green_framing_composition_marks: <取景/构图笔记；不适用写 none>
     orange_lighting_direction_marks: <灯光方向；不适用写 none>
     purple_emotion_sound_narrative_marks: <情绪/声音/叙事强调；不适用写 none>
     black_text_notes_and_panel_label: <简短镜头笔记和面板标签>
   source_shot_labels: 分镜1, 分镜2
   source_span: <可回指的源文本片段或摘要>

### Layout Aspect Decision

- panel_count: <storyboard_frame_units 数量>
- target_panel_image_aspect_ratio: 16:9
- effective_panel_slot_ratio: <计入下方文字区和标注安全边距后的单格槽位比例>
- panel_geometry_blueprint:
  - geometry_lock: fixed_16_9_image_boxes
  - max_panel_image_box_ratio_error: 0.06
  - outer_margin_pct: <推荐 0.035-0.05>
  - gutter_pct: <推荐 0.018-0.03>
  - text_strip_factor: <推荐 0.18-0.26>
  - image_box_policy: lock_16_9_inside_cell_leave_whitespace_if_needed
  - panels:
    - panel_no: 1
      cell_norm: { x: <0-1>, y: <0-1>, w: <0-1>, h: <0-1> }
      image_box_norm: { x: <0-1>, y: <0-1>, w: <0-1>, h: <0-1> }
      image_box_aspect_ratio: 16:9
      text_strip_norm: { x: <0-1>, y: <0-1>, w: <0-1>, h: <0-1> }
      ratio_error: <必须 <= 0.06>
- candidate_grids:
  - columns: <候选列数>
    rows: <候选行数>
    predicted_sheet_aspect_ratio: <候选整图比例>
    nearest_gpt_image_2_size: <合法 WIDTHxHEIGHT>
    panel_image_box_ratio_error: <单格图片区比例误差>
    readability_risk: <none | low | medium | high>
- selected_grid: <columns>x<rows>
- selected_sheet_aspect_ratio: <整张 sheet 比例>
- selected_sheet_size: <gpt-image-2 合法 WIDTHxHEIGHT；built-in mode 作为目标尺寸语义传入 prompt>
- pagination_or_multi_sheet_decision: <single_sheet | paginate | multiple_sheets>
- panel_image_box_ratio_error: <最终误差；必须 <= 0.06，否则分页或多 sheet>
- rationale: <为什么该比例和几何蓝图最能保持单个 panel 图片框为 16:9>

### Visual Prompt Atoms

1. panel_no: 1
   draw_subjects: <本 panel 可见主体>
   subject_actions: <源文本可回指的动作/状态>
   spatial_positions: <来自 Floor Plan To Panel Mapping 的站位、朝向、相对距离>
   camera_framing: <源文本已有景别/构图/运镜；无则 none>
   line_art_instruction: black-and-white clean storyboard line art, clear silhouettes, no color rendering
   annotation_overlay: <红/蓝/绿/橙/紫/黑标注落点；不适用写 none>
   text_strip: <等于 panel_description>
   negative_prompt_atoms:
     - no color cinematic still
     - no photorealistic lighting
     - no rewritten character positions
     - no facts outside source_span

### Accepted Spatial Floor Plan

- floor_plan_id: <分镜组ID>
- top_view_diagram_path: projects/aigc/<项目名>/12-图像/分镜故事板/第N集/floor-plans/<分镜组ID>.png
- acceptance_verdict: accepted
- scene_boundary: <场景边界、出入口、主要空间锚点>
- character_positions: <角色站位、朝向、相互距离；角色名与 YAML 一致>
- prop_positions: <关键道具位置及与角色/场景关系>
- camera_plan: <每个 panel 或视觉节拍的摄影机位置、方向、视野锥和运动路径>
- continuity_from_previous: <与上一张 accepted floor plan 相比的不变锚点、变化项和移动逻辑>

### Floor Plan To Panel Mapping

1. panel_no: 1
   floor_plan_zone: <对应平面图区域/镜头锥>
   characters_position_and_facing: <角色站位、朝向、相互距离>
   props_position: <道具位置>
   camera_position_and_direction: <摄影机位置、方向和视野锥>
   movement_path_used: <使用哪条运动路径；无则 none>
   unchanged_anchors_from_floor_plan: <保持不变的空间锚点>
   allowed_composition_variation: <仅限景别、裁切、透视转换>
   forbidden_spatial_drift: <不得改变的左右/内外/前后/朝向关系>

### Complete Group Source From 10-分组

<直接粘贴 10-分组 中该分镜组完整内容，包含组正文和底部 fenced YAML>

### Reference Subjects

Characters:
- 林寂: projects/aigc/<项目名>/11-主体/角色/3-生成/林寂-多视图.png

Scene:
- 永夜私立中学二年级A班教室: projects/aigc/<项目名>/11-主体/场景/3-生成/永夜私立中学二年级A班教室-多视图.png
  visual_anchor: spatial_structure_and_subject_identity

Props:
- 厚黑窗帘: missing
```

## Integrity Gate

通过 prompt 组装必须满足：

1. prompt 以任务执行前缀起笔。
2. `Source Comprehension` 存在且具体，能回指当前组源内容，没有补写剧情事实。
3. `Style Lock Spec` 存在，显式隔离完整组稿中的上游风格句，且 `Visual Prompt Atoms` 不含彩色电影 still、写实光影、全局画风或场景氛围渲染词。
4. `Storyboard Frame Units` 存在，且每个 panel 可回指源正文；不得默认把原始 `分镜N` 机械映射为 panel。
5. 每个 frame unit 具备 `rich_brief panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 和默认 `panel_image_aspect_ratio: 16:9`，并声明描述文字位于该 panel 图片下方。
6. `Visual Prompt Atoms` 存在，每个 panel 至少包含可画对象、动作/状态、空间锚点、线稿指令、标注覆盖、文字区和负向原子。
7. `Layout Aspect Decision` 存在，基于实际 panel 数和目标单格比例反推整图比例与 `gpt-image-2` 合法尺寸，并包含 `panel_geometry_blueprint`；每个 `image_box` 锁定 16:9，未固定画布后挤压 panel。
8. `Accepted Spatial Floor Plan` 存在，且 `acceptance_verdict: accepted`；否则不得进入 storyboard sheet imagegen。
9. `Floor Plan To Panel Mapping` 存在，逐 panel 记录平面图区域、角色站位朝向、道具位置、摄影机方向、运动路径和禁止空间漂移项。
10. 任务执行前缀明确要求 4K 出图，避免多 panel 被压缩到不可读。
11. `Complete Group Source From 10-分组` 直接来自对应分镜组完整内容，没有上游剧情改写。
12. 所有 `分镜N:` 标签按原顺序保留。
13. YAML 不得被丢弃；其主体列表进入 reference manifest，并作为完整分镜组内容的一部分保留在 source block 中。
14. prompt 不得援引全局风格作为风格词；黑白线稿也必须通过绑定参照图和平面图还原角色、场景、道具主体形象与空间站位。
15. 每个可见角色头顶必须有黑色文本角色名；角色名必须与分组稿/组底 YAML `角色` 字段一致。
16. 彩色只允许用于指定标注语义，不得用于画面渲染；每个颜色语义必须与用户声明的标注系统一致。
17. 若由于 provider 限制导致单 sheet 不可读，必须自动采用分页或多 sheet 并继续生成；不得压缩组正文、删减 frame units 或停下等待用户确认。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 任务执行前缀分行、漏句或被翻译 | 重写 prompt header |
| 组正文被摘要 | 回到 `group-source-extraction.md` 重新提取 |
| 插入了说明文字或 provider 参数 | 删除非 prompt 内容，移到 plan/report |
| 分镜顺序乱序 | 按源正文顺序恢复 |
| panel 与 `分镜N` 被默认一一对应 | 重建 `Storyboard Frame Units`，按视觉节拍识别 |
| panel 缺少描述文字、过度简略、过度冗长或默认图片比例 | 按 `rich_brief` 精简规则补齐 `panel_description` 与 `panel_image_aspect_ratio: 16:9` |
| `Source Comprehension` 空泛或缺失 | 回到完整组稿逐组重建源内容理解，不用通用模板套句 |
| `Layout Aspect Decision` 缺失、`panel_geometry_blueprint` 缺失、`selected_sheet_size` 非法或整图比例挤压 panel | 重算候选行列、16:9 image box 坐标和 `gpt-image-2` 合法尺寸；必要时分页或多 sheet |
| `Accepted Spatial Floor Plan` 缺失或未 accepted | 回到 `references/spatial-floor-plan-contract.md` 生成/验收平面图，验收通过后继续生图 |
| 角色头顶名称缺失或名称不一致 | 从组底 YAML `角色` 字段重建 `character_name_labels` |
| annotation plan 缺失或颜色语义错误 | 按标注系统补齐/修正 red/blue/green/orange/purple/black 字段 |
| prompt 援引全局风格或场景风格词 | 恢复任务执行前缀中的黑白线稿分镜手稿约束，并删除全局风格词 |
| prompt 未声明 4K | 恢复任务执行前缀中的 4K 分辨率句 |
| `Style Lock Spec` 缺失，或 `Visual Prompt Atoms` 仍包含彩色电影/写实光影/全局风格/场景氛围渲染词 | 标记 `FAIL-SHEET-STYLE-LOCK`，隔离上游风格句，重写线稿基底与负向原子 |
| `Visual Prompt Atoms` 缺失或只是泛化描述 | 标记 `FAIL-SHEET-PROMPT-ATOMS`，回到 source span 逐 panel 写可执行绘制原子 |
| `Floor Plan To Panel Mapping` 缺失，或 panel 站位无法回指 accepted floor plan | 标记 `FAIL-SHEET-FLOOR-PLAN-MAPPING`，回到 floor plan 和 frame units 建立逐 panel 映射 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每条组级 prompt 是否逐字以任务执行前缀起笔，没有漏句、翻译、分行破坏或前置说明？ | `G2-PREFIX` | `FAIL-SHEET-PROMPT` | `N4-PROMPT-DRAFT` / `references/prompt-assembly-contract.md#task-execution-prefix` | prompt markdown 中每个 `## group_id` 后首段可逐字比对任务执行前缀 |
| 任务执行前缀之后是否先写 `Style Lock Spec`，再写 `Source Comprehension`、`Storyboard Frame Units`、`Visual Prompt Atoms`、`Layout Aspect Decision`、`Accepted Spatial Floor Plan` 与 `Floor Plan To Panel Mapping`，最后进入 `Complete Group Source From 10-分组`，没有插入 provider 参数、执行日志或解释性说明？ | `G2-PREFIX` | `FAIL-SHEET-PROMPT` | `N4-PROMPT-DRAFT` / `N5B-FINAL-PAYLOAD` / `references/prompt-assembly-contract.md#task-execution-prefix` | prompt package 结构顺序为 task prefix -> style lock -> source comprehension -> frame units -> visual prompt atoms -> layout aspect decision -> accepted spatial floor plan -> floor plan to panel mapping -> complete group source -> reference subjects |
| `Source Comprehension` 是否具体理解当前组现有内容，并回指源正文/YAML，而不是通用模板套句？ | `G3A-SOURCE-COMPREHENSION` | `FAIL-SHEET-SCRIPTED-PROJECTION` | `N3A-FRAME-UNITS` / `N4-PROMPT-DRAFT` | prompt 的 source comprehension 与 `group-index.json.source_comprehension` 一致，报告抽查 source anchor |
| `Storyboard Frame Units` 是否来自 group extraction 结果，panel 编号使用 `panel_no`，没有把原始 `分镜N` 直接当 storyboard panel 编号？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `N4-PROMPT-DRAFT` | prompt 的 frame-unit plan 含 `panel_no`、`source_shot_labels`、`source_span`，并可回指 `group-index.json` |
| panel 与原始 `分镜N` 是否允许一对一、一对多、多对一，并通过 `mapping_type` 解释，而非默认一一对应？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `N4-PROMPT-DRAFT` | prompt 与 `group-index.json` 同步记录 `mapping_type`，review note 抽查 split/merge 合理性 |
| 每个 frame unit 是否包含 `rich_brief panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 和 `panel_image_aspect_ratio: 16:9` 默认值，且描述文字位于 panel 图片下方？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N3A-FRAME-UNITS` / `N4-PROMPT-DRAFT` | prompt 的 frame-unit plan、imagegen plan 和 report 同步记录 panel 描述、描述密度、角色名、标注计划与比例 |
| `Layout Aspect Decision` 是否基于实际 panel 数、目标单格比例、`panel_geometry_blueprint` 和 `gpt-image-2` 合法尺寸选择整图比例，且没有要求模型挤压 panel 适配固定画布？ | `G8A-LAYOUT-ASPECT` | `FAIL-SHEET-LAYOUT-ASPECT` | `N3B-LAYOUT-ASPECT` / `N4-PROMPT-DRAFT` | prompt、group-index 和 plan 均记录 candidate grids、selected_grid、selected_sheet_size、panel_geometry_blueprint、panel_image_box_ratio_error 和 pagination decision |
| `Accepted Spatial Floor Plan` 是否已接入 prompt，且 verdict 为 accepted？ | `G8D-FLOOR-PLAN-ACCEPTANCE` | `FAIL-SHEET-FLOOR-PLAN-GATE` | `N5A-FLOOR-PLAN` / `N5B-FINAL-PAYLOAD` | prompt、floor-plan manifest 和 plan 均记录 accepted floor plan id/path/verdict |
| `prompt_body` 是否直接采用完整分镜组内容，保留风格句、对白、动作画面、分镜明细、`分镜N:` 顺序和底部 YAML，没有翻译、摘要或改写剧情事实？ | `G4-CONTENT` | `FAIL-SHEET-PROMPT` | `N4-PROMPT-DRAFT` / `references/prompt-assembly-contract.md#prompt-body` | prompt 主体与 `group-index.json.group_full_source` diff 或抽查记录显示无剧情改写、无顺序漂移 |
| 相邻组间连接件是否没有进入 storyboard prompt 主体？ | `G4-CONTENT` | `FAIL-SHEET-PROMPT` | `N3-GROUP-INDEX` / `N4-PROMPT-DRAFT` | prompt markdown 不含 `## x-y-z~x-y-z` 连接件正文，报告记录 connector ignored |
| YAML 是否作为完整分镜组内容保留，并只通过 YAML 主体列表驱动 reference manifest / Reference Subjects？ | `G5-SUBJECTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/prompt-assembly-contract.md#prompt-body` | prompt 主体含 fenced YAML；`reference-manifest.json` 和 `Reference Subjects` 记录 YAML 主体 |
| prompt、manifest 与 plan 是否都声明参照图用于主体身份、空间结构和道具外形保真，而不是作为全局风格或场景风格锚点？ | `G7-SUBJECT-FIDELITY` | `FAIL-SHEET-REF` | `N4-PROMPT-DRAFT` / `N5-REF-BIND` | prompt 任务执行前缀、Scene slot、manifest 和 imagegen plan 均出现主体保真策略，且不出现全局风格词 |
| prompt 是否声明并正确使用彩色标注系统：红=身体运动、蓝=摄影机运动、绿=取景/构图、橙=灯光方向、紫=情绪/声音/叙事强调、黑=角色名、简短镜头笔记和面板标签？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT-DRAFT` / `references/prompt-assembly-contract.md#layout-semantics` | prompt 任务执行前缀、frame-unit `annotation_plan`、plan/report 均记录颜色语义，且没有把颜色用于渲染 |
| 每个可见角色头顶是否使用黑色文本显示角色名，且角色名与分组稿/组底 YAML `角色` 字段一致？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N3A-FRAME-UNITS` / `N4-PROMPT-DRAFT` / `N5B-FINAL-PAYLOAD` | prompt、frame-unit `character_name_labels`、plan/report 记录角色名来源与位置 |
| prompt 是否保留 4K、锁定 16:9 panel image box、图片下方描述文字、layout aspect decision、panel geometry blueprint 和 accepted floor plan 等语义，且没有额外硬编码格数或整图比例？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N4-PROMPT-DRAFT` / `references/prompt-assembly-contract.md#layout-semantics` | prompt 任务执行前缀包含 4K、locked 16:9 image box、description under image、annotation readability、layout aspect、panel geometry blueprint 和 spatial floor plan 约束；除用户明确要求外无固定行列数或固定整图比例 |
| 若 provider 限制导致单 sheet 不可读，是否自动采用分页或多 sheet 并继续生成，而不是压缩组正文、删减 frame units 或等待用户确认？ | `G12-REPORT` | `FAIL-SHEET-REPORT` | `N4-PROMPT-DRAFT` / `N7-IMAGEGEN` / `N10-CLOSE` | 执行报告记录 layout risk、受影响 `group_id`、分页/多 sheet 决策、生成图片路径或不可恢复失败原因 |
| prompt 是否包含 `Style Lock Spec`，并把完整组稿中的上游电影风格、光影、氛围、色彩和渲染词隔离为 evidence-only？ | `G2A-STYLE-LOCK` | `FAIL-SHEET-STYLE-LOCK` | `N5B-FINAL-PAYLOAD` / `references/prompt-assembly-contract.md#style-lock-spec` | prompt、plan 和 report 记录 `style_lock_spec`、`upstream_style_quarantine` 与 `forbidden_rendering_layers` |
| 每个 panel 是否包含可执行 `Visual Prompt Atoms`，而不是只给 summary / panel_description / 完整组稿让 imagegen 自行理解？ | `G3B-PROMPT-ATOMS` | `FAIL-SHEET-PROMPT-ATOMS` | `N3A-FRAME-UNITS` / `N5B-FINAL-PAYLOAD` | prompt 和 imagegen plan 逐 panel 记录 draw_subjects、subject_actions、spatial_positions、camera_framing、line_art_instruction、annotation_overlay、text_strip、negative_prompt_atoms |
| 每个 panel 是否通过 `Floor Plan To Panel Mapping` 回指 accepted floor plan 的区域、角色站位、道具位置和摄影机方向？ | `G8E-FLOOR-PLAN-MAPPING` | `FAIL-SHEET-FLOOR-PLAN-MAPPING` | `N5A-FLOOR-PLAN` / `N5B-FINAL-PAYLOAD` | prompt、floor-plan manifest 和 imagegen plan 逐 panel 记录 floor_plan_zone、characters_position_and_facing、camera_position_and_direction、forbidden_spatial_drift |

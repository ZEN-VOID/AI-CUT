# Prompt Assembly Contract

本文件定义 step1 的 prompt 组装规则：直接引用 `8-分组` 对应分镜组的完整内容作为生图基础，先插入 source comprehension、可追溯的 storyboard frame-unit plan、每格 panel 描述、角色头顶名称标注、annotation plan、layout aspect decision、visual prompt atoms 与可选 spatial handoff，再添加任务执行前缀明确黑白线稿分镜手稿、受控彩色标注系统、panel 图片比例、文字区、sheet 画布比例裁决和主体保真要求。

`分镜故事板` 不再生成、验收或维护平面图。若同一项目已有 `分镜平面图` 产物，本技能只可把它作为可选 `Spatial Handoff` 证据读取，用于增强 `spatial_positions`；缺失不阻断故事板生成。

## Task Execution Prefix

每条组级 prompt 必须逐字以下列文本开头；这是启动生图任务的任务执行词，不得替换为项目全局风格词：

```text
Create a storyboard sheet in standard storyboard manuscript style: black-and-white clean line art as the image base, with only the following annotation colors added on top: red arrows for body movement, blue arrows for camera movement, green marks for framing/composition notes, orange marks for lighting direction, purple marks for emotion/sound/narrative emphasis, and black text for character name labels above each visible character, short shot notes, and panel labels. Character name labels must exactly match the character names in the grouped shot source/YAML; do not rename, abbreviate, translate, or guess names. Do not use color for rendering characters, costumes, backgrounds, lighting, atmosphere, or global style keywords. Use the complete grouped shot source below as the foundation. Derive storyboard panels from the visual beats in the group source; do not force a one-to-one mapping from original shot labels to panels. Each panel must contain a locked 16:9 image box with a visible rectangular border, plus a separate storyboard description text strip directly below that image box. Use the supplied Layout Aspect Decision and Panel Geometry Blueprint: draw the sheet according to the selected grid, normalized cell coordinates, fixed 16:9 image_box coordinates, text_strip coordinates, margins, and gutters. Do not squeeze, stretch, crop, or distort any panel image box to fill a mismatched cell; leave clean whitespace inside the cell if needed. Use pagination or multiple sheets when one legal canvas cannot preserve locked 16:9 image boxes and readable text strips. Preserve the identities, silhouettes, spatial structure, and key prop shapes from the bound character, scene, and prop reference images even though the final image base is black-and-white line art. Render the final storyboard sheet at 4K resolution so every panel image, annotation, character name label, and description remains readable. Treat the Complete Group Source as evidence and source text, not as a visual style directive; upstream color, lighting, atmosphere, cinematic, lens, grain, film, rendering, or global style phrases are quarantined and must not override this black-and-white line-art style lock. Before drawing, obey the supplied Style Lock Spec, Source Comprehension, Storyboard Frame Units, Layout Aspect Decision, Visual Prompt Atoms, and Reference Subjects; if any required block is missing, stop and rework the prompt instead of generating.
```

任务执行前缀之后先进入 `Style Lock Spec`，再进入 `Source Comprehension`、`Storyboard Frame Units`、`Layout Aspect Decision`、`Visual Prompt Atoms`、可选 `Spatial Handoff`；最后进入 `Complete Group Source From 8-分组` 和 `Reference Subjects`。`Complete Group Source` 只作为源证据和事实边界，不得作为风格、光影、渲染或构图美化指令；不插入解释性说明、provider 参数、执行日志或额外任务指令。

## Required Blocks

- `Style Lock Spec`：隔离完整组稿中的上游电影风格、彩色、光影、氛围、镜头质感和胶片颗粒等词。
- `Source Comprehension`：记录本组叙事功能、连续动作链、空间锚点、角色状态锚点、道具状态锚点、视觉转折、必须保留的源事实、禁止补写项。
- `Storyboard Frame Units`：从视觉节拍裁决 panel，不机械等同 `分镜N`；每格有 `rich_brief panel_description`、角色头顶名称和受控标注计划。
- `Layout Aspect Decision`：根据 panel 数、16:9 单格图片区、下方文字区和标注安全边距反推整图比例、行列、合法尺寸和 `panel_geometry_blueprint`。
- `Visual Prompt Atoms`：逐 panel 记录 draw_subjects、subject_actions、spatial_positions、camera_framing、line_art_instruction、annotation_overlay、text_strip、negative_prompt_atoms。
- `Spatial Handoff`：可选块。只有已存在且已验收的 `分镜平面图` 侧车才可写 `consumed`；缺失写 `none`。不得把该块用作故事板前置门禁或画风来源。
- `Complete Group Source From 8-分组`：直接粘贴对应分镜组完整内容，包含组正文和底部 fenced YAML。
- `Reference Subjects`：只来自组底 YAML 主体和真实图片资产。

## Visual Prompt Atoms

- `spatial_positions` 必须来自 `source_span`、`panel_description`、源空间锚点和可选 `Spatial Handoff` 的综合裁决。
- 可选 `Spatial Handoff` 只能补强相对方位、站位、动线和机位理解；不得覆盖 `8-分组` 明确事实。
- 如果 sidecar 与源正文冲突，标记 `FAIL-SHEET-SPATIAL-HANDOFF`，优先回到 `Source Comprehension` 或忽略冲突侧车。
- `Visual Prompt Atoms` 必须比 `panel_description` 更可执行：不能只写“表现紧张气氛”“保持武侠风格”“突出动作感”等泛化句。

## Integrity Gate

通过 prompt 组装必须满足：

1. prompt 以任务执行前缀起笔。
2. `Source Comprehension` 存在且具体，能回指当前组源内容，没有补写剧情事实。
3. `Style Lock Spec` 存在，显式隔离完整组稿中的上游风格句，且 `Visual Prompt Atoms` 不含彩色电影 still、写实光影、全局画风或场景氛围渲染词。
4. `Storyboard Frame Units` 存在，且每个 panel 可回指源正文；不得默认把原始 `分镜N` 机械映射为 panel。
5. 每个 frame unit 具备 `rich_brief panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 和默认 `panel_image_aspect_ratio: 16:9`。
6. `Visual Prompt Atoms` 存在，每个 panel 至少包含可画对象、动作/状态、空间锚点、线稿指令、标注覆盖、文字区和负向原子。
7. `Layout Aspect Decision` 存在，基于实际 panel 数和目标单格比例反推整图比例与合法尺寸，并包含 `panel_geometry_blueprint`；每个 `image_box` 锁定 16:9，未固定画布后挤压 panel。
8. 可选 `Spatial Handoff` 若存在，必须来自 `分镜平面图` accepted 产物并只作为空间证据；缺失不得阻断生成。
9. `Complete Group Source From 8-分组` 直接来自对应分镜组完整内容，没有上游剧情改写。
10. YAML 不得被丢弃；其主体列表进入 reference manifest，并作为完整分镜组内容的一部分保留在 source block 中。
11. prompt 不得援引全局风格作为风格词；黑白线稿也必须通过绑定参照图还原角色、场景、道具主体形象。
12. 每个可见角色头顶必须有黑色文本角色名；角色名必须与分组稿/组底 YAML `角色` 字段一致。
13. 彩色只允许用于指定标注语义，不得用于画面渲染。
14. 若由于 provider 限制导致单 sheet 不可读，必须自动采用分页或多 sheet 并继续生成；不得压缩组正文、删减 frame units 或停下等待用户确认。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 任务执行前缀分行、漏句或被翻译 | 重写 prompt header |
| 组正文被摘要 | 回到 `group-source-extraction.md` 重新提取 |
| panel 与 `分镜N` 被默认一一对应 | 重建 `Storyboard Frame Units`，按视觉节拍识别 |
| panel 缺少描述文字、过度简略、过度冗长或默认图片比例 | 按 `rich_brief` 精简规则补齐 `panel_description` 与 `panel_image_aspect_ratio: 16:9` |
| `Source Comprehension` 空泛或缺失 | 回到完整组稿逐组重建源内容理解，不用通用模板套句 |
| `Layout Aspect Decision` 缺失、`panel_geometry_blueprint` 缺失、`selected_sheet_size` 非法或整图比例挤压 panel | 重算候选行列、16:9 image box 坐标和合法尺寸；必要时分页或多 sheet |
| `Spatial Handoff` 缺失 | 记录 `none`，继续故事板生成 |
| `Spatial Handoff` 被当作前置门禁、画风来源或覆盖源事实 | 标记 `FAIL-SHEET-SPATIAL-HANDOFF`，移除误用或回到 source comprehension 返工 |
| 角色头顶名称缺失或名称不一致 | 从组底 YAML `角色` 字段重建 `character_name_labels` |
| annotation plan 缺失或颜色语义错误 | 按标注系统补齐/修正 red/blue/green/orange/purple/black 字段 |
| prompt 援引全局风格或场景风格词 | 恢复任务执行前缀中的黑白线稿分镜手稿约束，并删除全局风格词 |
| `Style Lock Spec` 缺失，或 `Visual Prompt Atoms` 仍包含彩色电影/写实光影/全局风格/场景氛围渲染词 | 标记 `FAIL-SHEET-STYLE-LOCK`，隔离上游风格句，重写线稿基底与负向原子 |
| `Visual Prompt Atoms` 缺失或只是泛化描述 | 标记 `FAIL-SHEET-PROMPT-ATOMS`，回到 source span 逐 panel 写可执行绘制原子 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每条组级 prompt 是否逐字以任务执行前缀起笔，没有漏句、翻译、分行破坏或前置说明？ | `G2-PREFIX` | `FAIL-SHEET-PROMPT` | `N4-PROMPT-DRAFT` / `references/prompt-assembly-contract.md#task-execution-prefix` | prompt markdown 中每个 `## group_id` 后首段可逐字比对任务执行前缀 |
| `Source Comprehension` 是否具体理解当前组现有内容，并回指源正文/YAML，而不是通用模板套句？ | `G3A-SOURCE-COMPREHENSION` | `FAIL-SHEET-SCRIPTED-PROJECTION` | `N3A-FRAME-UNITS` / `N4-PROMPT-DRAFT` | prompt 的 source comprehension 与 `group-index.json.source_comprehension` 一致，报告抽查 source anchor |
| `Storyboard Frame Units` 是否来自 group extraction 结果，panel 编号使用 `panel_no`，没有把原始 `分镜N` 直接当 storyboard panel 编号？ | `G3-FRAME-UNITS` | `FAIL-SHEET-GROUP` | `N3A-FRAME-UNITS` / `N4-PROMPT-DRAFT` | prompt 的 frame-unit plan 含 `panel_no`、`source_shot_labels`、`source_span`，并可回指 `group-index.json` |
| 每个 frame unit 是否包含 `rich_brief panel_description`、`panel_description_density`、`character_name_labels`、`annotation_plan` 和 `panel_image_aspect_ratio: 16:9` 默认值，且描述文字位于 panel 图片下方？ | `G8-LAYOUT` | `FAIL-SHEET-IMAGEGEN` | `N3A-FRAME-UNITS` / `N4-PROMPT-DRAFT` | prompt 的 frame-unit plan、imagegen plan 和 report 同步记录 panel 描述、角色名、标注计划与比例 |
| `Layout Aspect Decision` 是否基于实际 panel 数、目标单格比例、`panel_geometry_blueprint` 和合法尺寸选择整图比例，且没有要求模型挤压 panel 适配固定画布？ | `G8A-LAYOUT-ASPECT` | `FAIL-SHEET-LAYOUT-ASPECT` | `N3B-LAYOUT-ASPECT` / `N4-PROMPT-DRAFT` | prompt、group-index 和 plan 均记录 candidate grids、selected_grid、selected_sheet_size、panel_geometry_blueprint、panel_image_box_ratio_error 和 pagination decision |
| 可选 `Spatial Handoff` 若存在，是否只作为 `visual_prompt_atoms.spatial_positions` 的空间证据使用，没有成为前置门禁、画风来源或覆盖源事实？ | `G8B-SPATIAL-HANDOFF` | `FAIL-SHEET-SPATIAL-HANDOFF` | `N5B-FINAL-PAYLOAD` | prompt、plan 和报告记录 `spatial_handoff_status`、source path/verdict、usable constraints 或 `none` |
| `prompt_body` 是否直接采用完整分镜组内容，保留风格句、对白、动作画面、分镜明细、`分镜N:` 顺序和底部 YAML，没有翻译、摘要或改写剧情事实？ | `G4-CONTENT` | `FAIL-SHEET-PROMPT` | `N4-PROMPT-DRAFT` / `references/prompt-assembly-contract.md#prompt-body` | prompt 主体与 `group-index.json.group_full_source` diff 或抽查记录显示无剧情改写、无顺序漂移 |
| prompt 是否包含 `Style Lock Spec`，并把完整组稿中的上游电影风格、光影、氛围、色彩和渲染词隔离为 evidence-only？ | `G2A-STYLE-LOCK` | `FAIL-SHEET-STYLE-LOCK` | `N5B-FINAL-PAYLOAD` / `references/prompt-assembly-contract.md#required-blocks` | prompt、plan 和 report 记录 `style_lock_spec`、`upstream_style_quarantine` 与 `forbidden_rendering_layers` |
| 每个 panel 是否包含可执行 `Visual Prompt Atoms`，而不是只给 summary / panel_description / 完整组稿让 imagegen 自行理解？ | `G3B-PROMPT-ATOMS` | `FAIL-SHEET-PROMPT-ATOMS` | `N3A-FRAME-UNITS` / `N5B-FINAL-PAYLOAD` | prompt 和 imagegen plan 逐 panel 记录 draw_subjects、subject_actions、spatial_positions、camera_framing、line_art_instruction、annotation_overlay、text_strip、negative_prompt_atoms |

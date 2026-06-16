# Reference Slot Binding Contract

本文件定义 step2：直接以每个分镜组底部 YAML 的主体信息为基准，查找角色、场景、道具生成图并绑定参照路径。

分镜故事板统一采用标准分镜手稿风格黑白线稿基底，并允许叠加受控彩色标注系统。角色、场景、道具参照图用于还原主体身份、轮廓、空间结构和关键道具外形；不得把项目全局风格、场景图风格、彩色光影或氛围当作本技能的风格词。彩色只允许用于标注语义，不得用于主体渲染。

## YAML Baseline

只消费组底 YAML 中的字段：

```yaml
角色: []
场景: []
道具: []
```

字段缺失时视为空数组并记录缺口。不得从正文、对白、分镜明细或道具描述中自动扩展主体清单。

## Search Roots

固定检查以下目录：

```text
projects/aigc/<项目名>/3-主体/角色/3-生成
projects/aigc/<项目名>/3-主体/场景/3-生成
projects/aigc/<项目名>/3-主体/道具/3-生成
```

## Image Priority

对每个主体名称：

1. 进行图片参照时，如有 `<主体名称>-多视图.png`、`.jpg`、`.jpeg`、`.webp` 可选，必须优先绑定多视图。
2. 只有多视图图片不存在时，才选择 `<主体名称>-主图.png`、`.jpg`、`.jpeg`、`.webp`。
3. 若只有 JSON 而无真实图片文件，不视为可绑定图片。
4. 若多视图与主图都不存在，槽位保持空、列入 `missing`，并从 imagegen 参照图片数组中移除。
5. 同一主体同时存在多视图与主图时，manifest、prompt slot 与 imagegen plan 的 `reference_images` 必须全部使用多视图路径，不得退回主图。

## Matching Policy

- 默认使用精确主体名匹配。
- 可使用项目内已确认的规范别名，但必须在 manifest 中记录 `matched_by: alias` 与别名来源。
- 不得对子串、泛词、类别词或推测名进行自动绑定。例如“学生”不能自动绑定到“学生群像”，除非 YAML 或用户显式确认。
- 同名多候选时进入 `ambiguous`，不得选择第一个凑数。

## Manifest Requirements

`reference-manifest.json` 至少包含：

```yaml
group_id: "1-1-1"
characters: []
scene: []
props: []
bound: []
missing: []
ambiguous: []
binding_policy:
  source: group_yaml
  priority: multi_view_then_main
visual_context_policy:
  before_builtin_imagegen: "view_image_each_bound_local_path"
style_policy:
  default: "standard_storyboard_manuscript_black_white_line_art_base_with_controlled_annotation_colors"
  forbidden: "global_style_keywords_or_scene_lighting_atmosphere_as_style"
  annotation_color_system:
    red_arrows: "body_movement"
    blue_arrows: "camera_movement"
    green_marks: "framing_composition_notes"
    orange_marks: "lighting_direction"
    purple_marks: "emotion_sound_narrative_emphasis"
    black_text: "character_name_labels_above_heads_short_shot_notes_and_panel_labels"
subject_fidelity_policy:
  when_reference_bound: "preserve_identity_silhouette_spatial_structure_prop_shape"
```

所有 `bound[].path` 必须是存在的本地图片路径。

## Bound Entry

```yaml
name: "林寂"
category: "character"
path: "projects/aigc/<项目名>/3-主体/角色/3-生成/林寂-多视图.png"
selected_variant: "multi_view"
matched_by: "exact"
context_role: "character_reference"
context_status: "pending_view_image"
fidelity_anchor: "identity_and_silhouette"
```

场景类 `bound` 条目还必须包含：

```yaml
visual_anchor: "spatial_structure_and_subject_identity"
context_role: "scene_spatial_reference"
secondary_context_role: "subject_identity_reference"
```

道具类 `bound` 条目还必须包含：

```yaml
fidelity_anchor: "prop_shape_and_key_details"
context_role: "prop_shape_reference"
```

## Gate

通过绑定必须满足：

1. 每个候选主体可追溯到该组 YAML。
2. 所有绑定路径存在且是图片文件。
3. 同一主体存在多视图时，`selected_variant` 必须是 `multi_view`，不得退回主图。
4. 缺图主体不保留空路径，不进入 imagegen reference images。
5. ambiguous 不进入生成计划；歧义主体自动记录为 `ambiguous` 并从 reference images 排除，后续用已绑定参照或纯文本 prompt 继续生图。
6. 对所有进入 imagegen reference images 的本地图片，生成前必须逐张调用 `view_image`；检视完成后 `context_status` 必须为 `visible_in_conversation_context`。
7. 只要绑定场景图，manifest、prompt slot 与 imagegen plan 必须都声明其 `visual_anchor: spatial_structure_and_subject_identity`；不得将场景图记录为风格、光影或氛围锚点。
8. manifest、prompt slot 与 imagegen plan 必须声明统一风格为 `standard_storyboard_manuscript_black_white_line_art_base_with_controlled_annotation_colors`，且参照图仅承担主体保真职责。
9. manifest、prompt slot 与 imagegen plan 必须声明彩色只用于标注系统，不用于角色、服装、背景、灯光、氛围或全局画风。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Characters / Scene / Props 候选主体是否只来自当前组底 YAML，没有从正文、对白、分镜明细、道具描述或猜测名扩展？ | `G5-SUBJECTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#yaml-baseline` | `reference-manifest.json` 记录 `binding_policy.source: group_yaml`，每个主体有 YAML source trace |
| 查找路径是否只落在角色、场景、道具三个 `3-主体/*/3-生成` 目录，没有扫描项目其他位置凑图？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#search-roots` | manifest 记录 search roots、候选路径和未越界扫描说明 |
| 同一主体存在多视图与主图时，manifest、prompt slot 和 imagegen plan 是否全部绑定多视图，只有缺多视图时才退到主图？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#image-priority` | `bound[].selected_variant`、prompt Reference Subjects、plan `reference_images` 均显示 `multi_view` 优先 |
| 只有 JSON 而无 PNG/JPG/JPEG/WebP 图片的主体是否进入 `missing`，且没有保留空路径或进入 imagegen reference images？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#image-priority` | manifest `missing[]` 记录无图原因，`bound[]` 和 plan 不含空字符串或 JSON 路径 |
| 主体匹配是否使用精确名或已确认 alias，并在 alias 情况下记录来源，没有对子串、泛词、类别词或推测名自动绑定？ | `G5-SUBJECTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#matching-policy` | `bound[].matched_by` 为 `exact` 或 `alias`；alias 条目带来源；ambiguous 记录候选而不生成 |
| 同名多候选或低置信匹配是否进入 `ambiguous` 并自动从 reference images 排除，同时继续生成而不等待确认？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `N6-REVIEW` | manifest `ambiguous[]` 记录候选、原因和排除状态；plan 排除 ambiguous 条目并继续使用可用参照或纯文本 prompt |
| 每个 `bound[].path` 是否真实存在且为图片文件，并带有 `context_role` / `context_status`？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#manifest-requirements` | manifest 中所有 `bound[]` 均有存在性检查结果、图片扩展名、`context_status` |
| 所有进入 imagegen reference images 的本地图是否在生成前逐张 `view_image`，并把状态更新为 `visible_in_conversation_context`？ | `G11-REF-INPUT` | `FAIL-SHEET-IMAGEGEN` | `N6-REVIEW` / `N7-IMAGEGEN` | manifest / plan / report 记录每个本地路径的 `view_image` 检视状态与上下文角色 |
| 绑定场景图时，manifest、prompt slot 与 imagegen plan 是否都声明 `visual_anchor: spatial_structure_and_subject_identity`，并把场景图标注为空间结构与主体身份参考？ | `G7-SUBJECT-FIDELITY` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#bound-entry` | scene bound entry 含 `visual_anchor`、`context_role: scene_spatial_reference`、`secondary_context_role: subject_identity_reference` |
| 绑定任何主体参照图时，manifest、prompt slot 与 imagegen plan 是否都声明参照图用于黑白线稿基底下的主体保真，而不是继承全局风格、场景风格或彩色光影氛围？ | `G7-SUBJECT-FIDELITY` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#manifest-requirements` | manifest 记录 `style_policy.default`、`annotation_color_system` 与 `subject_fidelity_policy`，且无全局风格词锚定 |

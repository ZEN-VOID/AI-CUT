# Reference Slot Binding Contract

本文件定义 step2：直接以每个分镜组底部 YAML 的主体信息为基准，查找角色、场景、道具生成图并绑定参照路径。

场景图承担双重职责：既是空间/环境参照，也是本组 storyboard 出图的风格、光影和氛围锚点。全局风格文字锁定不能替代场景参照图的视觉一致性要求。

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
projects/aigc/<项目名>/7-设计/角色/3-生成
projects/aigc/<项目名>/7-设计/场景/3-生成
projects/aigc/<项目名>/7-设计/道具/3-生成
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
scene_visual_policy:
  when_scene_reference_bound: "match_style_lighting_atmosphere"
```

所有 `bound[].path` 必须是存在的本地图片路径。

## Bound Entry

```yaml
name: "林寂"
category: "character"
path: "projects/aigc/<项目名>/7-设计/角色/3-生成/林寂-多视图.png"
selected_variant: "multi_view"
matched_by: "exact"
context_role: "character_reference"
context_status: "pending_view_image"
```

场景类 `bound` 条目还必须包含：

```yaml
visual_anchor: "style_lighting_atmosphere"
context_role: "scene_reference"
secondary_context_role: "style_lighting_atmosphere_reference"
```

## Gate

通过绑定必须满足：

1. 每个候选主体可追溯到该组 YAML。
2. 所有绑定路径存在且是图片文件。
3. 同一主体存在多视图时，`selected_variant` 必须是 `multi_view`，不得退回主图。
4. 缺图主体不保留空路径，不进入 imagegen reference images。
5. ambiguous 不进入生成计划，除非用户确认。
6. 对所有进入 imagegen reference images 的本地图片，生成前必须逐张调用 `view_image`；检视完成后 `context_status` 必须为 `visible_in_conversation_context`。
7. 只要绑定场景图，manifest、prompt slot 与 imagegen plan 必须都声明其 `visual_anchor: style_lighting_atmosphere`；不得只依靠全局风格文字描述锁定整体画风。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Characters / Scene / Props 候选主体是否只来自当前组底 YAML，没有从正文、对白、分镜明细、道具描述或猜测名扩展？ | `G5-SUBJECTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#yaml-baseline` | `reference-manifest.json` 记录 `binding_policy.source: group_yaml`，每个主体有 YAML source trace |
| 查找路径是否只落在角色、场景、道具三个 `7-设计/*/3-生成` 目录，没有扫描项目其他位置凑图？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#search-roots` | manifest 记录 search roots、候选路径和未越界扫描说明 |
| 同一主体存在多视图与主图时，manifest、prompt slot 和 imagegen plan 是否全部绑定多视图，只有缺多视图时才退到主图？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#image-priority` | `bound[].selected_variant`、prompt Reference Subjects、plan `reference_images` 均显示 `multi_view` 优先 |
| 只有 JSON 而无 PNG/JPG/JPEG/WebP 图片的主体是否进入 `missing`，且没有保留空路径或进入 imagegen reference images？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#image-priority` | manifest `missing[]` 记录无图原因，`bound[]` 和 plan 不含空字符串或 JSON 路径 |
| 主体匹配是否使用精确名或已确认 alias，并在 alias 情况下记录来源，没有对子串、泛词、类别词或推测名自动绑定？ | `G5-SUBJECTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#matching-policy` | `bound[].matched_by` 为 `exact` 或 `alias`；alias 条目带来源；ambiguous 记录候选而不生成 |
| 同名多候选或低置信匹配是否进入 `ambiguous`，在用户确认前不进入生成计划？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `N6-REVIEW` | manifest `ambiguous[]` 记录候选、原因、确认状态；plan 排除未确认项 |
| 每个 `bound[].path` 是否真实存在且为图片文件，并带有 `context_role` / `context_status`？ | `G6-SLOTS` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#manifest-requirements` | manifest 中所有 `bound[]` 均有存在性检查结果、图片扩展名、`context_status` |
| 所有进入 imagegen reference images 的本地图是否在生成前逐张 `view_image`，并把状态更新为 `visible_in_conversation_context`？ | `G11-REF-INPUT` | `FAIL-SHEET-IMAGEGEN` | `N6-REVIEW` / `N7-IMAGEGEN` | manifest / plan / report 记录每个本地路径的 `view_image` 检视状态与上下文角色 |
| 绑定场景图时，manifest、prompt slot 与 imagegen plan 是否都声明 `visual_anchor: style_lighting_atmosphere`，并把场景图标注为双重参考角色？ | `G7-SCENE-VISUAL` | `FAIL-SHEET-REF` | `N5-REF-BIND` / `references/reference-slot-binding.md#bound-entry` | scene bound entry 含 `visual_anchor`、`context_role: scene_reference`、`secondary_context_role: style_lighting_atmosphere_reference` |

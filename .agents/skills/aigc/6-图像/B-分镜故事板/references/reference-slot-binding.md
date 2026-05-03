# Reference Slot Binding Contract

本文件定义 step2：直接以每个分镜组底部 YAML 的主体信息为基准，查找角色、场景、道具生成图并绑定参照路径。

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
projects/aigc/<项目名>/5-设计/角色/3-生成
projects/aigc/<项目名>/5-设计/场景/3-生成
projects/aigc/<项目名>/5-设计/道具/3-生成
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
```

所有 `bound[].path` 必须是存在的本地图片路径。

## Bound Entry

```yaml
name: "林寂"
category: "character"
path: "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
selected_variant: "multi_view"
matched_by: "exact"
context_role: "character_reference"
context_status: "pending_view_image"
```

## Gate

通过绑定必须满足：

1. 每个候选主体可追溯到该组 YAML。
2. 所有绑定路径存在且是图片文件。
3. 同一主体存在多视图时，`selected_variant` 必须是 `multi_view`，不得退回主图。
4. 缺图主体不保留空路径，不进入 imagegen reference images。
5. ambiguous 不进入生成计划，除非用户确认。
6. 对所有进入 imagegen reference images 的本地图片，生成前必须逐张调用 `view_image`；检视完成后 `context_status` 必须为 `visible_in_conversation_context`。

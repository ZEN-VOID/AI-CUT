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

1. 优先选择 `<主体名称>-多视图.png`、`.jpg`、`.jpeg`、`.webp`。
2. 若多视图图片不存在，选择 `<主体名称>-主图.png`、`.jpg`、`.jpeg`、`.webp`。
3. 若只有 JSON 而无真实图片文件，不视为可绑定图片。
4. 若多视图与主图都不存在，槽位保持空、列入 `missing`，从 LibTV 图片数组中移除，并不得在主体信息后添加空 `@` 后缀。

## Matching Policy

- 默认使用精确主体名匹配。
- 可使用项目内已确认的规范别名，但必须在 manifest 中记录 `matched_by: alias` 与别名来源。
- 不得对子串、泛词、类别词或推测名进行自动绑定。例如“学生”不能自动绑定到“学生群像”，除非 YAML 或用户显式确认。
- 同名或别名命中多个候选图片时，必须先执行视觉消歧：把候选图片路径、YAML 主体名称、类别、分镜组上下文和候选来源发送到当前窗口作为可加载图像上下文，由 LLM 识图比较后选择唯一匹配项。
- 视觉消歧只能在候选集合内部选择，不得借识图扩大到 YAML 之外的新主体或未列入候选的图片。
- 视觉消歧成功时写入 `bound`，并记录 `matched_by: visual_disambiguation`、候选清单、选择理由和上下文来源。
- 视觉消歧后仍无法唯一确定时才进入 `ambiguous`，不得选择第一个凑数。

## Manifest Requirements

`reference-manifest.json` 至少包含：

```yaml
group_id: "1-1-1"
characters: []
scenes: []
props: []
bound: []
missing: []
ambiguous: []
binding_policy:
  source: group_yaml
  priority: multi_view_then_main
  disambiguation: visual_first_then_ambiguous
```

所有 `bound[].path` 必须是存在的本地图片路径。
每个已绑定主体还必须生成 `subject_inline`，格式为 `<主体名称> @<图片路径>`，用于写入 prompt 的对应角色、场景或道具信息之后。
多候选经过视觉消歧时，manifest 还必须保留 `visual_disambiguation[]` 证据，至少包含主体名称、类别、候选图片路径、是否已发送窗口上下文、最终选择和无法选择时的阻断原因。

## Bound Entry

```yaml
name: "林寂"
category: "character"
path: "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
selected_variant: "multi_view"
matched_by: "exact"
subject_inline: "林寂 @projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
```

## Visual Disambiguation Entry

```yaml
name: "林寂"
category: "character"
group_id: "1-1-1"
candidates:
  - "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
  - "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-主图.png"
context_sent_to_window: true
selected_path: "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
decision_basis: "多视图图像与组底 YAML 主体和组正文中的服装、年龄、关键外观一致。"
status: "resolved"
```

## Gate

通过绑定必须满足：

1. 每个候选主体可追溯到该组 YAML。
2. 所有绑定路径存在且是图片文件。
3. 多视图优先于主图。
4. 缺图主体不保留空路径，不进入 LibTV reference images，不生成空 `subject_inline`。
5. 多候选主体已有视觉消歧证据，或明确进入 `ambiguous`。
6. ambiguous 不进入生成计划，除非用户确认。

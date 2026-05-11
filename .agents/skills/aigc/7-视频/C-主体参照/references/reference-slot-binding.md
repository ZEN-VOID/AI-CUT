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

## Fresh Local Resolution Order

每次执行都必须先从当前本地生成目录重新解析主体图，再考虑上传缓存：

1. 读取组底 YAML 主体名。
2. 在当前 `5-设计/*/3-生成` 搜索根中枚举候选图片。
3. 按 `Image Priority` 和视觉消歧规则裁决当前 `selected_path`。
4. 记录 `resolved_from_current_generation_dir: true`、`resolution_candidates[]`、`selected_path`、`selected_variant` 和当前文件指纹。
5. 只有在 `selected_path + source_sha256 + source_size_bytes + source_mtime_ns` 与缓存条目完全一致后，才允许复用缓存 URL。

禁止顺序：

- 不得先按主体名查 `upload-cache.json`，再反推本地路径。
- 不得用缓存里已有的 OSS URL 证明主体图存在。
- 不得在当前生成目录没有对应图片时，使用历史缓存 URL 代替缺失主体图。
- 不得按文件名相似、旧阶段 manifest、旧视频任务或旧画布 URL 选择主体图。

## Image Priority

对每个主体名称：

1. 优先选择 `<主体名称>-多视图.png`、`.jpg`、`.jpeg`、`.webp`。
2. 若多视图图片不存在，选择 `<主体名称>-主图.png`、`.jpg`、`.jpeg`、`.webp`。
3. 若只有 JSON 而无真实图片文件，不视为可绑定图片。
4. 若多视图与主图都不存在，槽位保持空、列入 `missing`，从 LibTV 图片数组中移除，并不得在主体信息后添加空 `@` 后缀。

## Upload Cache Freshness Policy

- 上传缓存只能作为同一轮执行中的传输加速层，不能作为主体参照真源。
- 上传缓存的 lookup key 必须是当前已解析本地文件的 `path + source_sha256 + source_size_bytes + source_mtime_ns`，不得只用主体名、角色 ID、文件名或旧 URL 命中。
- 使用任何缓存 `uploaded_url` 前，必须先确认 `bound[].path` 当前存在、是图片文件，并且仍位于 `5-设计/角色/3-生成`、`5-设计/场景/3-生成` 或 `5-设计/道具/3-生成` 的当前生成目录下。
- 缓存条目必须记录并匹配当前本地文件指纹：`source_sha256`、`source_size_bytes`、`source_mtime_ns`。任一字段缺失或不匹配时，必须重新运行 `upload_file.py`，不得沿用缓存 URL。
- 若本地源图缺失，即使缓存中仍有 OSS URL，也必须将该主体列入 `missing / stale_cached_upload`，并阻断该 URL 进入 `images[]`、`mixedList` 和 YAML `uploaded_url`。
- 禁止为了绕过上传慢、上传失败或并发拥堵而把历史缓存 URL 当成“可用参照图”。上传失败只能写入 blocked / needs_rework，不得降级为历史图提交。

## Shared Reference Policy

- 默认一个 YAML 主体对应一个独立参照绑定；不同主体不得静默共用同一 `path` 或 `uploaded_url`。
- 若两个 YAML 主体确实应共用同一张图，例如“竹筒杯”和“冰甘蔗水”被上游明确裁决为同一物件视图，manifest 必须为所有相关条目写入 `shared_reference_group`、`shared_reference_reason` 和 `primary_subject_name`。
- 未声明共享原因的重复 `path`、重复 `uploaded_url` 或重复 `mixedList` 项，必须判定为 `reference_prompt_integrity_error`，不得提交。

## LibTV Image Budget

- 单个分镜组提交给 LibTV 的主体参照图上限为 9 张。
- 当 YAML 实际关联到的可用参照元素超过 9 张时，必须做取舍，不得把全部图片塞进 `mixedList`。
- 取舍顺序：
  1. 角色优先保留。
  2. 场景优先保留，尤其是承载空间、光影、透视和运动边界的场景。
  3. 超出上限时先排除道具；仅保留对本组动作、证据或视觉锚点最关键的道具。
  4. 若排除道具后仍超过 9 张，再考虑是否存在不必要的场景、重复场景、群像角色或可由源文本保留的次要主体。
- 被排除的主体不得进入 `images[]`、`mixedList` 或 YAML `uploaded_url`；仍应在 manifest / report 中记录为 `excluded_from_libtv_images`，并说明它们由源文本约束保留。
- 若按以上规则仍无法在不破坏角色身份或空间连续性的前提下压到 9 张以内，必须标记 `needs_rework / reference_budget_unresolved`，交由用户或上游重新裁决；不得提交超过 9 张图的 LibTV 任务。

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
  max_libtv_images_per_group: 9
```

所有 `bound[].path` 必须是存在的本地图片路径。进入 LibTV 的 `images[]` 不得超过 9 张；超过上限被排除的可用主体写入 `excluded_from_libtv_images[]`。
每个已绑定主体还必须生成 `subject_inline`，格式为 `<主体名称> @<图片路径>`，用于写入 prompt 的对应角色、场景或道具信息之后。
`bound[]`、`missing[]`、`ambiguous[]`、`excluded_from_libtv_images[]` 四类集合中的主体名必须互斥；同一主体不得同时被写成“已绑定”和“缺图 / 未进入预算”。
每个已绑定主体必须显式记录 `resolved_from_current_generation_dir: true`。若使用缓存 URL，还必须记录 `upload_cache_lookup_key` 和 `upload_cache_hit_after_fresh_resolution: true`。
多候选经过视觉消歧时，manifest 还必须保留 `visual_disambiguation[]` 证据，至少包含主体名称、类别、候选图片路径、是否已发送窗口上下文、最终选择和无法选择时的阻断原因。

## Bound Entry

```yaml
name: "林寂"
category: "character"
path: "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
resolved_from_current_generation_dir: true
resolution_candidates:
  - "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
source_sha256: "<sha256>"
source_size_bytes: 123456
source_mtime_ns: 1770000000000000000
upload_cache_lookup_key: "<path>|<sha256>|<size>|<mtime_ns>"
upload_cache_hit_after_fresh_resolution: false
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
7. `images[]` / `mixedList` 不超过 9 张；超过时已优先从道具取舍，并记录排除理由；无法合理压缩到 9 张以内时不得提交。
8. 任何使用缓存 URL 的图片都必须通过本地路径存在性和 `source_sha256 / source_size_bytes / source_mtime_ns` 指纹一致性检查；失败即视为 stale cache，不得提交。
9. 使用缓存 URL 前必须已经完成 fresh local resolution，并记录 `resolved_from_current_generation_dir: true` 与 `upload_cache_hit_after_fresh_resolution: true`；按主体名、角色 ID 或文件名直接命中缓存一律失败。
10. `bound[]` 与 `missing[] / ambiguous[] / excluded_from_libtv_images[]` 的主体名不得重叠。
11. 重复本地路径、重复 uploaded URL 或重复 mixedList URL 只有在显式声明 `shared_reference_group` 和共享理由时允许，否则不得提交。

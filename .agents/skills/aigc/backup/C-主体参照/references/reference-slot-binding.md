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

## Same-Canvas Asset Reuse Order

同一 LibTV `projectUuid/projectID` 画布内，主体图 URL 是传输层资产登记，可以按 YAML 主体名直接复用：

1. 读取组底 YAML 主体名。
2. 先锁定当前 LibTV `projectUuid/projectUrl`。
3. 在当前 `projectUuid` 的 `asset_uploads` / 项目级上传登记中查找同一 `category + yaml_name` 的 active uploaded URL。
4. 若只命中一个 active URL，且 URL 的 `/claw/<projectUuid>/` 与当前画布一致，直接复用，不要求重新解析本地生成目录或匹配本地文件指纹。
5. 若没有 active URL、同名登记有歧义、图片已调整，或用户显式要求“替换/更新/重新上传”，再按 `Image Priority` 从当前 `5-设计/*/3-生成` 搜索根解析图片并运行 `upload_file.py`，上传成功后把新 URL 标为 active。

禁止顺序：

- 不得复用其他 `projectUuid/projectID` 画布的 URL。
- 不得在同一主体名存在多个 active URL 且无 `active/latest` 标记时自行猜测。
- 不得因本地图片文件发生调整而静默沿用旧 URL；图片调整必须由用户显式触发替换或由任务输入明确声明。
- 不得把同名 URL 复用理解为生成槽位顺序；`generation_slots` 仍必须逐组重建。

## Image Priority

对每个主体名称：

1. 若同一画布已有唯一 active uploaded URL，优先复用该 URL。
2. 需要新上传或显式替换时，优先选择 `<主体名称>-多视图.png`、`.jpg`、`.jpeg`、`.webp`。
3. 若多视图图片不存在，选择 `<主体名称>-主图.png`、`.jpg`、`.jpeg`、`.webp`。
4. 若只有 JSON 而无真实图片文件，不视为可上传图片。
5. 若既没有同画布 active URL，也没有多视图/主图，槽位保持空、列入 `missing`，从 LibTV 图片数组中移除，并不得在主体信息后添加空 `@` 后缀。

## Active Asset Reuse Policy

- active `asset_uploads` 是同一 LibTV 画布内的已上传资产登记，不再要求每次按本地 `path + 指纹` 验证后才能复用。
- 默认 lookup key 是 `projectUuid + category + yaml_name`；登记中应保留 `asset_registry_lookup_key`、`reuse_policy: same_canvas_active_url` 或等价字段。
- `uploaded_url` 必须是当前画布作用域内的 LibTV `/claw/<projectUuid>/` URL；跨画布 URL 一律阻断。
- 本地 `path`、`source_sha256`、`source_size_bytes`、`source_mtime_ns` 仍可作为审计证据；字段存在时必须自洽，但字段缺失不阻断同画布 active URL 复用。
- 当图片内容已调整、更换、多候选重新裁决，或用户明确要求替换时，必须进入 `explicit_replace`：重新解析当前本地图片、上传并把新 URL 设为 active。
- 若同一 `projectUuid + category + yaml_name` 有多个候选 uploaded URL 且没有 active/latest 标记，必须标记 `needs_rework / asset_registry_ambiguous`，不得猜测。

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
- 绑定完成后必须进入注册机制，而不是只把 URL 塞进 prompt：`asset_uploads` 注册 `yaml_name -> uploaded_url`，`generation_slots` 注册 `reference_index / 图N / mixedList[n-1] -> uploaded_url -> yaml_name`。最终提交、远端 prompt 和 YAML 只消费注册表结果。
- 不得对子串、泛词、类别词或推测名进行自动绑定。例如“学生”不能自动绑定到“学生群像”，除非 YAML 或用户显式确认。
- 同名或别名命中多个候选图片时，必须先执行视觉消歧：把候选图片路径、YAML 主体名称、类别、分镜组上下文和候选来源发送到当前窗口作为可加载图像上下文，由 LLM 识图比较后选择唯一匹配项。
- 视觉消歧只能在候选集合内部选择，不得借识图扩大到 YAML 之外的新主体或未列入候选的图片。
- 视觉消歧成功时写入 `bound`，并记录 `matched_by: visual_disambiguation`、候选清单、选择理由和上下文来源。
- 视觉消歧后仍无法唯一确定时才进入 `ambiguous`，不得选择第一个凑数。

## Reference Slot Registry

每个进入 LibTV 视频生成框的参照图都必须在 `reference-manifest.json` 中注册为两层真源：

```yaml
asset_uploads:
  - name: "林寂"              # 原 YAML 主体名；别名匹配时仍写 YAML 使用名
    canonical_asset_name: "林寂"
    category: "character"
    source_path: "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
    source_sha256: "<optional_sha256>"
    source_size_bytes: 123456
    source_mtime_ns: 1770000000000000000
    uploaded_url: "https://libtv-res.liblib.art/claw/<projectUuid>/<uuid>.png"
    reuse_policy: "same_canvas_active_url"
    asset_registry_lookup_key: "<projectUuid>|character|林寂"
    active: true
    oss_upload_index: 1
generation_slots:
  - reference_index: 1
    slot: 1
    ui_slot_index: 1
    mixedList_index: 0
    portrait_token: "{{Portrait 1}}"
    image_token: "{{Image 1}}"
    uploaded_url: "https://libtv-res.liblib.art/claw/<projectUuid>/<uuid>.png"
    name: "林寂"
    category: "character"
    slot_source: "ui_thumbnail_order | post_submit_mixedList | submit_plan_expected_order"
```

注册规则：

- `asset_uploads[].name` 必须是组底 YAML 的主体名称；别名、设计稿正式名或文件名只能写入 `canonical_asset_name / alias_source / alias_reason`，不得替换 YAML 名称。
- `generation_slots[].name + uploaded_url` 必须能用 URL 反查到 `asset_uploads[]` 的同名项；若 URL 对应的 name 不同，判定为 `reference_slot_registry_mismatch`。
- `generation_slots[].reference_index` 必须从 1 连续编号，且等于最终 YAML 中对应主体项的 `reference_index`；`mixedList_index = reference_index - 1`。
- submit plan `images[]`、远端 `mixedList` 和 prompt YAML 都必须逐槽匹配 `generation_slots` 的 name 与 URL；只匹配 URL 集合不够，主体名错位也必须失败。
- 若 LibTV UI 缩略图、query 回显或用户截图显示实际槽位与本地预期不一致，必须用实际 `mixedList[n].url` 或 UI 图N 反查 `asset_uploads`，重建 `generation_slots` 后回刷 YAML 与 `libtv-submission.txt`，不得继续沿用旧 YAML 顺序。

## Manifest Requirements

`reference-manifest.json` 至少包含：

```yaml
group_id: "1-1-1"
characters: []
scenes: []
props: []
bound: []
asset_uploads: []
generation_slots: []
missing: []
ambiguous: []
binding_policy:
  source: group_yaml
  priority: multi_view_then_main
  disambiguation: visual_first_then_ambiguous
  max_libtv_images_per_group: 9
```

`bound[].path` 是可选本地审计证据；新上传或显式替换时应记录当前本地图片路径，直接复用同画布 active URL 时可以只记录 `uploaded_url + asset_registry_lookup_key`。进入 LibTV 的 `images[]` 不得超过 9 张；超过上限被排除的可用主体写入 `excluded_from_libtv_images[]`。
本地图片路径、候选集合和源图指纹只作为 manifest / submit plan 审计证据，不写入 prompt 正文；`subject_inline` 若保留，仅作为本地审计摘要，不再投影为 `@<图片路径>` 追加到角色、场景或道具行后。
`bound[]`、`missing[]`、`ambiguous[]`、`excluded_from_libtv_images[]` 四类集合中的主体名必须互斥；同一主体不得同时被写成“已绑定”和“缺图 / 未进入预算”。
每个已绑定主体必须显式记录复用或上传来源：同画布复用写 `reuse_policy: same_canvas_active_url` 与 `asset_registry_lookup_key`；显式替换重传写 `reuse_policy: explicit_replace`、本地解析证据和上传证据。旧字段 `source_sha256 / source_size_bytes / source_mtime_ns` 可以保留为审计证据，但不再是复用 URL 的硬前置条件。
final 相位必须存在 `asset_uploads[]` 与 `generation_slots[]`；`generation_slots[]` 是 YAML `reference_index`、submit plan `images[]`、远端 `mixedList` 与 LibTV UI 图N 的唯一槽位注册真源。
多候选经过视觉消歧时，manifest 还必须保留 `visual_disambiguation[]` 证据，至少包含主体名称、类别、候选图片路径、是否已发送窗口上下文、最终选择和无法选择时的阻断原因。

## Bound Entry

```yaml
name: "林寂"
category: "character"
path: "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
reuse_policy: "same_canvas_active_url"
asset_registry_lookup_key: "<projectUuid>|character|林寂"
resolved_from_current_generation_dir: false
resolution_candidates:
  - "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
source_sha256: "<optional_sha256>"
source_size_bytes: 123456
source_mtime_ns: 1770000000000000000
uploaded_url: "https://.../claw/<projectUuid>/..."
selected_variant: "multi_view"
matched_by: "exact"
subject_inline: "林寂 local_path=projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
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
8. 任何 reused uploaded URL 都必须属于当前 `projectUuid` 的 `/claw/<projectUuid>/` 作用域；跨画布 URL 不得提交。
9. 同画布 active URL 可按 YAML 主体名直接复用；若图片已调整或用户显式要求替换，必须重新上传并更新 active URL。
10. `bound[]` 与 `missing[] / ambiguous[] / excluded_from_libtv_images[]` 的主体名不得重叠。
11. 重复本地路径、重复 uploaded URL 或重复 mixedList URL 只有在显式声明 `shared_reference_group` 和共享理由时允许，否则不得提交。
12. final 相位 `generation_slots[]` 必须逐项锁定 `reference_index -> name -> uploaded_url`，且与 prompt YAML、submit plan `images[]`、远端 `mixedList` 同槽一致；任何主体名和参照图错位都必须阻断提交或触发重提。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 参照主体是否只来自组底 YAML 的 `角色 / 场景 / 道具`，没有从正文、对白、分镜明细或泛词自动扩展？ | `G3-SUBJECTS` | `FAIL-VIDSUBJ-REF` | `N5-REF-BIND` / 本文件 `YAML Baseline` | `reference-manifest.json.yaml_subjects`、YAML 原文和被排除的非 YAML 候选 |
| 搜索根是否限定在当前项目 `5-设计/*/3-生成`，且 JSON 记录没有被当作可上传图片？ | `G4-SLOTS` | `FAIL-VIDSUBJ-REF` | `N5-REF-BIND` | `resolution_candidates`、`missing[]`、真实图片路径存在性检查 |
| 同画布 active uploaded URL 是否按 `projectUuid + category + yaml_name` 复用，且 URL `/claw/<projectUuid>/` 与当前画布一致？ | `G15-SAME-CANVAS-REUSE` | `FAIL-VIDSUBJ-REFERENCE-PROJECT-SCOPE` | `N5-REF-BIND` / `N8-DISPATCH` | `asset_uploads[].reuse_policy`、`asset_registry_lookup_key`、`projectUuid`、URL scope |
| 同名多个 active URL、跨画布 URL、图片调整或用户显式替换请求是否被阻断或转入 `explicit_replace`，没有靠猜测沿用旧 URL？ | `G15-SAME-CANVAS-REUSE` | `FAIL-VIDSUBJ-ASSET-REGISTRY-AMBIGUOUS` / `FAIL-VIDSUBJ-REFERENCE-PROJECT-SCOPE` | `N5-REF-BIND` | `asset_registry_ambiguous` finding、`explicit_replace` 记录、上传或替换证据 |
| 新上传或显式替换时是否遵守多视图优先、主图次之，缺图主体不保留空路径且不进入 LibTV 图片数组？ | `G4-SLOTS` | `FAIL-VIDSUBJ-REF` | `N5-REF-BIND` | `bound[].selected_variant`、`missing[]`、图片路径和 `images[]` 对照 |
| 多候选主体是否先把候选图作为窗口图像上下文做视觉消歧，仍不能唯一确认才进入 `ambiguous`？ | `G4-SLOTS` | `FAIL-VIDSUBJ-REF` | `N5-REF-BIND` / `N6-REVIEW` | `visual_disambiguation[]`、候选清单、`context_sent_to_window`、选择理由或 unresolved 原因 |
| 单组进入 `images[] / mixedList` 的参照是否不超过 9 张，超限时按角色和场景优先、道具先排除并留存取舍理由？ | `G6-REFERENCE-BUDGET` | `FAIL-VIDSUBJ-REF-BUDGET` | `N5-REF-BIND` / `N6-REVIEW` | `reference_image_budget`、`excluded_from_libtv_images[]`、`mixedList` 数量 |
| 不同 YAML 主体是否没有静默共用同一路径、uploaded URL 或 mixedList 项；确需共享时是否声明共享组和主主体？ | `G16-REF-PROMPT-INTEGRITY` | `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` | `N5-REF-BIND` | `shared_reference_group`、`shared_reference_reason`、重复 URL 检查结果 |
| 是否建立了两层注册表：`asset_uploads: yaml_name -> uploaded_url` 与 `generation_slots: reference_index / 图N / mixedList[n-1] -> uploaded_url -> yaml_name`？ | `G16-REF-PROMPT-INTEGRITY` / `G19-REMOTE-REFERENCE-ORDER` | `FAIL-VIDSUBJ-REFERENCE-SLOT-REGISTRY` / `FAIL-VIDSUBJ-UPLOAD-LEDGER` | `N5-REF-BIND` / `N8-DISPATCH` | `reference-manifest.json.asset_uploads`、`generation_slots`、slot source |
| final 相位中 `generation_slots` 是否逐项锁定 `reference_index -> name -> uploaded_url`，并能同槽匹配 prompt YAML、submit plan `images[]` 和远端 `mixedList`？ | `G16-REF-PROMPT-INTEGRITY` / `G19-REMOTE-REFERENCE-ORDER` | `FAIL-VIDSUBJ-REFERENCE-SLOT-REGISTRY` / `FAIL-VIDSUBJ-REMOTE-REFERENCE-ORDER` | `N8-DISPATCH` | 引用一致性检查结果、YAML 按 `reference_index` 排序对照、post-submit order gate |
| `bound[] / missing[] / ambiguous[] / excluded_from_libtv_images[]` 是否互斥，同一主体没有同时被写成已绑定和缺图/未入预算？ | `G16-REF-PROMPT-INTEGRITY` | `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` | `N5-REF-BIND` / `N6-REVIEW` | manifest 四类集合互斥检查和冲突主体列表 |
| 本地路径、候选集合和指纹是否只留在 manifest / submit plan 审计证据中，没有被投影进 prompt 正文或远端提交？ | `G5-LOCAL-ASSET-EVIDENCE` | `FAIL-VIDSUBJ-PROMPT` | `N4-PROMPT` / `N5-REF-BIND` | prompt / `libtv-submission.txt` 本地路径扫描结果、manifest 审计字段 |

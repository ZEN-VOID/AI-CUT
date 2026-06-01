# Hybrid Reference Binding Contract

本文件定义故事板总参照与主体参照的查找、绑定和审查边界。

## Storyboard Total Reference

查找路径：

1. `projects/aigc/<项目名>/7-图像/B-分镜故事板/第N集/images/<group_id>.*`
2. `projects/aigc/<项目名>/7-图像/B-分镜故事板/第N集/<group_id>.*`

允许扩展名：`png`、`jpg`、`jpeg`、`webp`。

绑定规则：

- 唯一命中时写入 `storyboard_total_reference`。
- 无命中时记录 `storyboard_missing_optional`，不保留空图片槽。
- 多个同优先级命中时阻断该组，要求用户选择或先清理上游。
- 故事板总参照只能作为整组总参照，不得挂到某个主体后；进入 LibTV 时只在 final fenced YAML 的 `故事板参照.reference_index / uploaded_url / image_token` 中表达，不另起远端参照说明段。draft prompt 不提前写这些槽位字段。

## Subject References

主体来源：

- 组底 YAML 的 `角色`
- 组底 YAML 的 `场景`
- 组底 YAML 的 `道具`

设计图查找路径：

- `projects/aigc/<项目名>/6-设计/角色/3-生成/`
- `projects/aigc/<项目名>/6-设计/场景/3-生成/`
- `projects/aigc/<项目名>/6-设计/道具/3-生成/`

优先级：

1. 多视图图或 multiview 图。
2. 主图、单图、封面图。
3. 其他真实图片候选。

禁止：

- 只存在 JSON、Markdown 或 prompt 文件时，不得当作图片参照。
- 不得从正文泛词自动扩展主体列表。
- 不得用角色图替代道具图，或用场景图替代角色图。
- 不得按主体名、角色 ID、文件名或历史 URL 直接命中上传缓存；缓存只能在当前本地图片 fresh resolve 之后作为上传加速项使用。

## Fresh Local Resolution And Upload Cache

每次执行 D 路线都必须先从当前项目本地生成目录重新解析参照真源：

1. 故事板总参照从当前 `7-图像/B-分镜故事板` 目录 fresh resolve。
2. 主体参照从当前 `6-设计/角色|场景|道具/3-生成` 目录 fresh resolve。
3. 对每个进入 LibTV 的图片记录 `resolved_from_current_generation_dir: true`、`source_sha256`、`source_size_bytes`、`source_mtime_ns` 和候选集合。
4. 只有当缓存记录的 `path + source_sha256 + source_size_bytes + source_mtime_ns` 与当前 fresh resolve 文件完全匹配时，才允许复用 cached uploaded URL。
5. 本地源图缺失、指纹缺失或指纹不匹配时，该 URL 必须判定为 `stale_cached_upload`，不得进入 `mixedList`、final fenced YAML 绑定或 submit plan `images[]`。

## Manifest Shape

```json
{
  "group_id": "1-1-1",
  "storyboard_total_reference": {
    "path": "projects/aigc/<项目名>/7-图像/B-分镜故事板/第1集/images/1-1-1.png",
    "marker": "@图1",
    "role": "storyboard_total_reference",
    "resolved_from_current_generation_dir": true,
    "source_sha256": "",
    "source_size_bytes": 0,
    "source_mtime_ns": 0
  },
  "subject_references": [
    {
      "subject_type": "角色",
      "subject_name": "林夏",
      "path": "projects/aigc/<项目名>/6-设计/角色/3-生成/林夏/多视图.png",
      "marker": "uploaded_url_binding",
      "yaml_binding": {"name": "林夏", "reference_index": 1, "uploaded_url": "", "image_token": "{{Image 1}}"},
      "selected_variant": "multi_view",
      "resolved_from_current_generation_dir": true,
      "source_sha256": "",
      "source_size_bytes": 0,
      "source_mtime_ns": 0
    }
  ],
  "missing": []
}
```

## LibTV Image Budget

若图片数量超过 9 张或 LibTV 当前上限：

1. 单个分镜组真实提交给 LibTV 的 `mixedList` 最多 9 张图，故事板总参照和主体参照共同计入上限。
2. 故事板总参照优先保留。
3. 主体参照中角色和场景优先保留。
4. 超出上限时先排除道具；仅保留对本组动作、证据或视觉锚点最关键的道具。
5. 若排除道具后仍超过 9 张，再排除重复、不必要或可由源文本保留的次要主体。
6. 被排除的主体不得进入 `mixedList` 或 final fenced YAML 槽位绑定；必须记录 `reference_over_limit`、`excluded_due_to_budget`，并说明它们由源文本约束保留。
7. 若无法在不破坏故事板总参照、角色身份或空间连续性的前提下压到 9 张以内，必须标记 `needs_rework / reference_budget_unresolved`，交由用户或上游重新裁决；不得提交超过 9 张图的 LibTV 任务。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 故事板总参照是否只按当前 `7-图像/B-分镜故事板/第N集/images/<group_id>.*` 与同集根层 `<group_id>.*` 两级路径查找，且只接受真实 `png/jpg/jpeg/webp` 图片？ | `GATE-VIDHYB-REF-01` | `FAIL-VIDHYB-REF` | `N3-STORYBOARD-BIND` / `references/hybrid-reference-binding.md#Storyboard-Total-Reference` | storyboard search roots、candidate list、extension filter、selected path |
| 故事板候选是否唯一；无命中是否只记录 `storyboard_missing_optional` 并移除空图片槽，多命中是否阻断该组等待用户或上游清理？ | `GATE-VIDHYB-REF-01` | `FAIL-VIDHYB-REF` | `N3-STORYBOARD-BIND` | unique/missing/multiple verdict、blocked reason、manifest `missing[]` |
| 故事板总参照是否只作为整组总参照写入 `storyboard_total_reference`，没有被挂到某个角色、场景或道具主体后，也没有在 draft prompt 阶段预写槽位字段？ | `GATE-VIDHYB-REF-01` | `FAIL-VIDHYB-REF` | `N3-STORYBOARD-BIND` / `N5-PROMPT-ASSEMBLE` | manifest role、draft prebinding scan、final `故事板参照` diff |
| 主体清单是否只来自组底 YAML 的 `角色 / 场景 / 道具`，没有从组正文泛词、标题、旁白或历史 manifest 自动扩展主体？ | `GATE-VIDHYB-REF-02` | `FAIL-VIDHYB-REF` | `N4-SUBJECT-BIND` / `references/hybrid-reference-binding.md#Subject-References` | YAML subject list、rejected body-derived candidates、subject source trace |
| 主体图片是否只从当前 `6-设计/角色、场景、道具/3-生成` 对应类型目录解析，没有用角色图替代道具图、用场景图替代角色图或跨类型兜底？ | `GATE-VIDHYB-REF-02` | `FAIL-VIDHYB-REF` | `N4-SUBJECT-BIND` | per-type search roots、candidate type、selected image path、cross-type rejection notes |
| 参照选择是否优先多视图或 multiview，其次主图/单图/封面图，并明确拒绝 JSON、Markdown、prompt 文件或目录占位冒充图片？ | `GATE-VIDHYB-REF-02` | `FAIL-VIDHYB-REF` | `N4-SUBJECT-BIND` | selected_variant、candidate ranking、non-image rejection list |
| 每个进入 LibTV 的故事板或主体图片是否从当前本地生成目录 fresh resolve，并记录 `resolved_from_current_generation_dir: true`、`source_sha256`、`source_size_bytes`、`source_mtime_ns`？ | `GATE-VIDHYB-REF-03` | `FAIL-VIDHYB-STALE-REFERENCE-ASSET` | `N3-STORYBOARD-BIND` / `N4-SUBJECT-BIND` / `references/hybrid-reference-binding.md#Fresh-Local-Resolution-And-Upload-Cache` | fresh resolution record、fingerprint fields、source file stat |
| 上传缓存是否只在当前 fresh resolve 的 `path + source_sha256 + source_size_bytes + source_mtime_ns` 完全匹配时复用，且没有按主体名、group_id、文件名或旧 URL 直接命中？ | `GATE-VIDHYB-REF-03` | `FAIL-VIDHYB-STALE-REFERENCE-ASSET` | `N3-STORYBOARD-BIND` / `N4-SUBJECT-BIND` | cache lookup key、fingerprint comparison、stale cache rejection |
| `reference-manifest.json` 是否同时表达故事板总参照、主体参照、缺图项、`yaml_binding` 和 selected variant，且未把未上传或未入预算主体写成空 `reference_index / uploaded_url`？ | `GATE-VIDHYB-REF-02` | `FAIL-VIDHYB-REF` | `N4-SUBJECT-BIND` / `N5-PROMPT-ASSEMBLE` | manifest shape audit、bound/missing split、empty slot scan |
| 单组 LibTV 图片预算是否把故事板总参照与全部主体参照共同计数，并在真实 `mixedList` 前确认不超过 9 张？ | `GATE-VIDHYB-BUDGET-01` | `FAIL-VIDHYB-LIBTV` | `N4-SUBJECT-BIND` / `N6-PLAN-BUILD` / `references/hybrid-reference-binding.md#LibTV-Image-Budget` | reference_image_budget.max_images、pre-budget count、mixedList count |
| 超过 9 张时是否先保留故事板总参照，再优先角色和场景，先排除道具，再排除重复、不必要或可由源文本保留的次要主体，并记录 `excluded_due_to_budget`？ | `GATE-VIDHYB-BUDGET-01` | `FAIL-VIDHYB-LIBTV` | `N4-SUBJECT-BIND` / `N6-PLAN-BUILD` | exclusion order、excluded_due_to_budget list、source-text retention note |
| 若无法在不破坏故事板总参照、角色身份或空间连续性的前提下压到 9 张以内，是否标记 `needs_rework / reference_budget_unresolved` 并阻断提交？ | `GATE-VIDHYB-BUDGET-01` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `N7-REVIEW-GATE` | blocked submit plan、needs_rework reason、no sessionId evidence |
| 被排除、缺失或缓存失效的故事板/主体是否只写入 manifest、submit plan 和 report，没有进入 final fenced YAML 槽位、远端 `mixedList` 或 `*-libtv-submission.txt`？ | `GATE-VIDHYB-REMOTE-02` | `FAIL-VIDHYB-REF-PROMPT-INTEGRITY` | `N5-PROMPT-ASSEMBLE` / `N6-PLAN-BUILD` | manifest missing/excluded list、final YAML scan、submission forbidden phrase scan |

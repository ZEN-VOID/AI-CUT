# Frame Image Binding Contract

本文件定义 step2：检查 `projects/aigc/<项目名>/6-图像/A-分镜画面` 中是否存在对应四段式 `分镜ID` 的图像，并把真实路径写入 LibTV YAML。

## Source Roots

固定候选根：

```text
projects/aigc/<项目名>/6-图像/A-分镜画面/第N集/
projects/aigc/<项目名>/6-图像/A-分镜画面/第N集/images/
```

## Match Key

- 只以四段式 `shot_id` 作为默认匹配键，例如 `1-1-1-1`。
- 优先匹配 `images/<shot_id>.<ext>`。
- 次级匹配同集目录下 `<shot_id>.<ext>`。
- 允许扩展名：`png`、`jpg`、`jpeg`、`webp`。
- 不使用角色名、场景名、正文关键词或模糊语义猜测图片。

## Binding Policy

命中唯一真实文件时，写入 manifest / YAML：

```yaml
shot_id: "1-1-1-1"
reference_annotation: "1-1-1-1@projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-1.png"
reference_status: "found"
```

并加入当前 group job 的 `reference_images`：

```yaml
reference_images:
  - shot_id: "1-1-1-1"
    path: "projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-1.png"
    marker: "@图1"
    role: "storyboard_frame"
    source: "6-图像/A-分镜画面"
```

未命中时，只写 manifest：

```yaml
shot_id: "1-1-1-1"
reference_status: "missing_optional"
reference_annotation: "1-1-1-1"
```

并从 `reference_images` 中移除该镜空槽位。

## Marker Assignment

- 本地 manifest 可保留 `marker` 便于 review；`marker` 不得跳号，不得为缺图镜头预留空号。
- `prompt.md` 与远端提交的 canonical 绑定必须落在 fenced YAML 的 `分镜画面参照` 列表中；列表按组内镜头顺序、仅对存在真实图片并进入 `imageList` 的镜头写入。
- `分镜画面参照` 字段至少包含 `reference_index`、`shot_id`、`source_label`、`uploaded_url`；`reference_index` 必须等于该图进入 `imageList` 的 1-based 顺序。远端 `*-libtv-submission.txt` 不得把本地 marker 投影为脱离 YAML 的人工 `参照图N` 编号，也不得另起分镜画面参照说明段。

## LibTV Image Budget

- 单个分镜组真实提交给 LibTV 的 `imageList` 最多 9 张图。
- 当可用分镜画面图超过 9 张时，必须做预算裁决：优先保留首镜、尾镜、关键动作、转场和空间关系镜头，排除重复或不必要的相邻画面。
- 被排除的 `shot_id` 不得进入 `imageList` 或远端 URL 清单；必须在 manifest / batch / report 中记录 `excluded_due_to_budget`。
- 若无法在不破坏组内动作与空间连续性的前提下压到 9 张以内，标记 `needs_rework / reference_budget_unresolved`，不得提交超过 9 张图的 LibTV 任务。

## Review Notes

- 缺图不是失败，只是该镜头没有图像参照。
- 当前组至少有一张图时默认走 `libtv_session_with_uploaded_references`；没有任何图时走 `libtv_session_text_only`。
- 多个同优先级候选命中时，标记 `ambiguous` 并阻断该组提交，不得随机选择。
- 所有路径必须真实存在，且位于当前项目根内。
- 参照图只作为分镜画面视觉参照；不得反向改写 `4-分组` 的剧情和镜头事实。
- `imageList` 不超过 9 张；超限时必须有 `excluded_due_to_budget` 或阻断状态。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 图片候选根是否只来自当前项目 `6-图像/A-分镜画面/第N集/` 与 `images/` 子目录，且解析路径真实存在并位于项目根内？ | `GATE-FVID-REF-01` | `FAIL-FVID-REF` | `N5-REF-BIND` | reference manifest 记录 search roots、resolved path、existence check 与 project-root check |
| 图片匹配是否只以四段式 `shot_id` 为默认键，优先 `images/<shot_id>.<ext>`，其次同集目录 `<shot_id>.<ext>`，没有使用角色名、场景名、正文关键词或语义猜测？ | `GATE-FVID-REF-02` | `FAIL-FVID-REF` | `N5-REF-BIND` | candidate list 记录匹配优先级、扩展名、selected candidate reason 或 no-match reason |
| 唯一命中时是否同时写入 manifest 与当前组 `reference_images`；未命中时是否只写 `missing_optional` 并移除空槽位；同优先级多候选是否阻断而非随机选择？ | `GATE-FVID-REF-03` | `FAIL-FVID-REF` | `N5-REF-BIND` | reference manifest 的 `found / missing_optional / ambiguous` 状态、候选列表与空槽扫描结果 |
| 本地 `marker` 是否只服务 manifest/review 且不跳号，远端 canonical 绑定是否改由 final fenced YAML `分镜画面参照[]` 承载，没有人工预设脱离 YAML 的 `参照图N`？ | `GATE-FVID-REF-04` | `FAIL-FVID-SLOT-ORDER` | `N8-DISPATCH` | `generation_slots`、`imageList`、final YAML `reference_index` 与本地 marker 对照 |
| `分镜画面参照[]` 是否只列真实存在且进入 `imageList` 的镜头，并且 `reference_index` 等于该图进入 `imageList` 的 1-based 顺序？ | `GATE-FVID-REF-04` | `FAIL-FVID-SLOT-ORDER` | `N8-DISPATCH` | final YAML、LibTV plan、slot ledger 的 `reference_index -> uploaded_url -> shot_id` 对照 |
| 单个分镜组真实提交的 `imageList` 是否不超过 9 张；超限时是否按首镜、尾镜、关键动作、转场、空间关系镜头做预算裁决，并记录被排除 `shot_id`？ | `GATE-FVID-REF-05` | `FAIL-FVID-REFERENCE-BUDGET` | `N5-REF-BIND` | selected / excluded shot list、`excluded_due_to_budget`、budget rationale |
| 无法在不破坏组内动作与空间连续性的前提下压到 9 张以内时，是否标记 `needs_rework / reference_budget_unresolved` 并阻断提交，而不是静默丢图或超量提交？ | `GATE-FVID-REF-05` | `FAIL-FVID-REFERENCE-BUDGET` | `N5-REF-BIND` | batch/report 中的 blocked reason、unresolved budget note、next rework entry |
| 参照图是否只作为分镜画面视觉参照，没有反向改写 `4-分组` 的剧情、镜头事实、组正文或镜头顺序？ | `GATE-FVID-REF-06` | `FAIL-FVID-PROMPT` | `N6-YAML` | prompt package 与 group source hash 对照、reference usage note |
| 当前组至少一张图时是否走 uploaded references；没有任何图时是否走 text-only；两种路线都没有保留缺图镜头的空图片槽位？ | `GATE-FVID-LIBTV-01` | `FAIL-FVID-LIBTV` | `N6-YAML` | batch YAML 的 command type、reference image count、empty slot scan 与 skipped/missing summary |
| 执行报告是否清楚区分 `found`、`missing_optional`、`ambiguous`、`excluded_due_to_budget`、`reference_budget_unresolved`，并给出对应返工入口？ | `GATE-FVID-REPORT-01` | `FAIL-FVID-REPORT` | `N12-CLOSE` | close report 的 reference coverage、status summary、rework targets |

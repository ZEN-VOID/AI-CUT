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

# Frame Image Binding Contract

本文件定义 step2：检查 `projects/aigc/<项目名>/6-图像/A-分镜画面` 中是否存在对应四段式 `分镜ID` 的图像，并把真实路径写入 Dreamina YAML。

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

- `@图N` 按组内镜头顺序、仅对存在真实图片的镜头连续编号。
- prompt 映射必须同时保留 `@图N`、`shot_id` 与路径，例如 `@图1 = 1-1-1-1@projects/.../1-1-1-1.png`。
- `marker` 不得跳号，不得为缺图镜头预留空号。

## Review Notes

- 缺图不是失败，只是该镜头没有图像参照。
- 当前组至少有一张图时默认走 `multimodal2video`；没有任何图时走 `text2video`。
- 多个同优先级候选命中时，标记 `ambiguous` 并阻断该组提交，不得随机选择。
- 所有路径必须真实存在，且位于当前项目根内。
- 参照图只作为分镜画面视觉参照；不得反向改写 `4-分组` 的剧情和镜头事实。

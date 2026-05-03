# Storyboard Image Binding Contract

本文件定义 step2：检查 `projects/aigc/<项目名>/6-图像/B-分镜故事板` 中是否存在对应分镜组 ID 的图像，并把真实路径写入 LibTV YAML。

## Source Roots

固定候选根：

```text
projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/
projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/images/
```

## Match Key

- 只以 `group_id` 作为默认匹配键，例如 `1-1-1`。
- 优先匹配 `images/<group_id>.<ext>`。
- 次级匹配同集目录下 `<group_id>.<ext>`。
- 允许扩展名：`png`、`jpg`、`jpeg`、`webp`。
- 不使用角色名、场景名、正文关键词或模糊语义猜测图片。

## Binding Policy

- 命中唯一真实文件时，写入 YAML：

```yaml
reference_images:
  - path: "projects/aigc/<项目名>/6-图像/B-分镜故事板/第1集/images/1-1-1.png"
    role: "storyboard_sheet"
    marker: "@图1"
    source: "6-图像/B-分镜故事板"
reference_status: "found"
```

- 未命中时，写入：

```yaml
reference_images: []
reference_status: "missing_optional"
```

- 多个同优先级候选命中时，标记 `ambiguous` 并阻断该组提交，不得随机选择。
- 所有路径必须真实存在，且位于当前项目根内。
- 参照图只作为 storyboard visual reference；不得反向改写 `4-分组` 的剧情和镜头事实。

## Review Notes

- 缺图不是失败，只是该组走 `libtv_session_text_only`。
- 有图时默认走 `libtv_session_with_uploaded_references`，prompt 中必须说明 `@图1` 是分镜故事板视觉参照，不是首帧。
- 若用户显式要求“没有故事板图就跳过视频生成”，可把 `missing_optional` 改为 `skipped_by_user_policy`。

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
- B 路线真实提交给 LibTV 的 `imageList` 只允许 1 张故事板总参照，且必然不超过 9 张；若异常出现多张候选，必须唯一裁决或阻断，不得把多张候选塞入 `imageList`。
- `marker: "@图1"` 只用于 manifest / submit plan 可读映射；`prompt.md` 与远端提交的 canonical 绑定必须落在 fenced YAML 的 `故事板参照` 对象中，字段至少包含 `name: 故事板总参照`、`role: storyboard_sheet`、`uploaded_url`。
- 远端 `*-libtv-submission.txt` 不得把本地 marker 投影为人工 `参照图1` 编号，也不得另起故事板参照说明段；只能复用 source-first enriched YAML 中的 `故事板参照.uploaded_url` 绑定。

## Review Notes

- 缺图不是失败，只是该组走 `libtv_session_text_only`。
- 有图时默认走 `libtv_session_with_uploaded_references`，远端 `【直接生成请求】` 必须说明 `故事板参照.uploaded_url` 是分镜故事板视觉参照，不是首帧。
- 若用户显式要求“没有故事板图就跳过视频生成”，可把 `missing_optional` 改为 `skipped_by_user_policy`。

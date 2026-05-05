# Hybrid Prompt Assembly Contract

本文件定义 `D-主板混合参照` 的 prompt 组装规则。

## Fixed Opening

每条 D 本地审核 prompt 必须以固定参照用途说明起笔：

```text
请参考故事板总参照图作为本分镜组的整体构图、镜头顺序、角色站位、场景连续性与情绪节奏参考；不要把故事板参照当作单一首帧。后文每个主体名称后的 @参照图 用于锁定对应角色、场景或道具外观，不得互相替换。根据以下完整分镜组内容生成一条连续视频。保持分镜顺序、角色动作、镜头运动、场景与情绪连续；不生成字幕，不生成BGM，保留物理互动音效与环境音。
```

## LibTV Remote Opening

发送给 LibTV 的 `*-libtv-submission.txt` 必须以此固定开头开始，且必须位于任何 `分镜组原文`、`分镜明细` 或长正文之前：

```text
【LibTV 调用锁定】
provider: seedance2.0
taskType: video
modeType: mixed2video
mixedList: [{"url": "<uploaded_url_1>", "type": "image"}, {"url": "<uploaded_url_2>", "type": "image"}, ...]
duration: 15
ratio: 16:9
resolution: 720p
enableSound: on
```

远端提交文本只能出现 `参照图N：<uploaded_url>`、`mixedList` 调用锁和主体 / 故事板用途说明；不得包含 `@projects/...`、`/Volumes/...` 或其他本地图片路径。本地审核 prompt 可以保留本地路径用于 review gate。

若存在故事板图，固定开头之后必须提供故事板 marker 或路径映射，例如：

```text
故事板总参照：@图1 -> projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/images/1-1-1.png
```

若故事板图缺失，不得保留空 `@图1`，应写：

```text
故事板总参照：缺失，按文字分镜组生成。
```

## Subject Inline Binding

- 主体参照来自组底 YAML 的 `角色 / 场景 / 道具`。
- 有图主体必须在对应主体信息后追加 `@<图片路径>` 或 LibTV marker 映射。
- 示例：`角色：林夏 @图2（projects/aigc/<项目名>/5-设计/角色/3-生成/林夏/多视图.png）`
- 缺图主体保留主体文本，但不得追加空 marker；在 manifest 记录 `missing_optional`。

## Body Rule

固定开头与参照说明之后，直接接入 `4-分组` 的完整组正文。LLM 可以调整说明层和 provider 指令层的表达，但不得删改分镜事实、镜头顺序、动作结果或 YAML 主体。

## Marker Ordering

1. 故事板总参照优先占用第一个 marker，例如 `@图1`。
2. 主体参照按 YAML 顺序分配后续 marker。
3. 若无故事板图，主体参照从 `@图1` 开始，但必须在 prompt 中说明没有故事板总参照。
4. manifest 必须保存 marker、role、source_path、subject_name、subject_type。

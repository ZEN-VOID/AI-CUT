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
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
transport_only_projection: true
禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头。
只允许执行 transport_only 投影：上传 URL、mixedList、duration、ratio、resolution、enableSound。
```

远端提交文本只能出现 `故事板总参照：参照图N <uploaded_url>`、`主体名：参照图N <uploaded_url>`、`mixedList` 调用锁和主体 / 故事板用途说明；不得包含 `@projects/...`、`/Volumes/...` 或其他本地图片路径。本地审核 prompt 可以保留本地路径用于 review gate。
远端生成 prompt 完整体必须包含 `【混合参照说明】 + 【分镜组源文本】`；不得只把 `【分镜组源文本】` 投给 `params.prompt`，也不得只把混合参照作为 `mixedList` 的匿名图片数组。每个图片 token / 图片编号 / 参照 URL 必须邻近故事板身份或主体名称。
默认远端提交必须采用 `strict_original + transport_only`，`allow_libtv_prompt_optimization=false`。这表示只允许把本地路径投影为上传 URL、补齐 `mixed2video / mixedList / duration / ratio / resolution / enableSound` 等技术参数，不允许 LibTV 远端 Agent 对 `【分镜组源文本】` 做提示词优化、重新编排、摘要、改写或补镜头。
只有用户显式选择 `libtv_optimize` 或显式声明 `allow_libtv_prompt_optimization: true` 时，才允许远端做创作型编排；该选择必须写入 submit plan、queue 和 report。

若存在故事板图，固定开头之后必须提供故事板 marker 或路径映射，例如：

```text
故事板总参照：参照图1 <uploaded_url>；用于整体构图、镜头顺序、画面连续性和节奏。
```

若故事板图缺失，不得保留空 `@图1`，应写：

```text
故事板总参照：缺失，按文字分镜组生成。
```

## Subject Inline Binding

- 主体参照来自组底 YAML 的 `角色 / 场景 / 道具`。
- 有图主体必须在对应主体信息后追加 `@<图片路径>` 或 LibTV marker 映射。
- 示例：`角色：林夏 @图2（projects/aigc/<项目名>/5-设计/角色/3-生成/林夏/多视图.png）`
- 远端 `*-libtv-submission.txt` 中必须投影为 `主体名：参照图N <uploaded_url>`；不得只写裸 `参照图N` 或裸 URL。
- 缺图主体保留主体文本，但不得追加空 marker；在 manifest 记录 `missing_optional`。

## Direct Generation Request

远端 `*-libtv-submission.txt` 必须在 `【混合参照说明】` 后、`【分镜组源文本】` 前写入：

```text
【直接生成请求】
请基于【混合参照说明】（包含故事板总参照、主体名、主体类别、参照图编号和主体参照 URL）和下方【分镜组源文本】，按 `mixed2video + mixedList` 生成一条连续视频。请直接把【混合参照说明】中与本组相关的故事板总参照绑定关系、主体名/参照图绑定关系 + 【分镜组源文本】原文作为生成 prompt 完整体。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把混合参照简化为裸图片 token、裸图片编号或裸 URL。
```

## Body Rule

固定开头与参照说明之后，直接接入 `4-分组` 的完整组正文。LLM 可以调整说明层和 provider 指令层的表达，但不得删改分镜事实、镜头顺序、动作结果或 YAML 主体。未 opt-in `libtv_optimize` 时，任何远端优化版提示词、摘要版分镜或镜头计划都不是正常执行步骤，必须按 `prompt_fidelity_violation / libtv_optimize_without_opt_in` 返工。

## Marker Ordering

1. 故事板总参照优先占用第一个 marker，例如 `@图1`。
2. 主体参照按 YAML 顺序分配后续 marker。
3. 若无故事板图，主体参照从 `@图1` 开始，但必须在 prompt 中说明没有故事板总参照。
4. manifest 必须保存 marker、role、source_path、subject_name、subject_type。

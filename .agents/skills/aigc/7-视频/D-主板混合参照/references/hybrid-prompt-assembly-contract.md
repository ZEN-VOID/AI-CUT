# Hybrid Prompt Assembly Contract

本文件定义 `D-主板混合参照` 的 prompt 组装规则。

## Prompt Shape

每条 D 本地审核 `prompt.md` 必须采用 source-first enriched YAML：直接保留 `4-分组/第N集.md` 中对应 `## x-y-z` 分镜组原文，包含标题、正文和 fenced YAML；不得在原文前另写“固定开头”“混合参照说明”或缺图说明段。

唯一允许的机械注入位置是该组 fenced YAML：

- 故事板图唯一绑定并上传后，新增或更新 `故事板参照` 对象，写入 `name: 故事板总参照`、`role: storyboard_sheet`、`reference_index`、`uploaded_url`。
- 已绑定并上传的 YAML 主体，把原 `角色 / 场景 / 道具` 列表项扩展为对象并补入 `name`、`reference_index`、`uploaded_url`；缺图、未入预算或没有上传 URL 的主体保留原名称，不写空 URL、不写 `null`、不写缺图解释。
- `reference_index` 使用 1-based 顺序，必须与 submit plan `reference_images[]` 顺序、`mixedList` 数组顺序、LibTV 自动生成的图1/图2/图3顺序保持一致。
- 本地路径、源图指纹、缺图原因、预算取舍原因仍归 manifest、submit plan 和 report 管理；`prompt.md` 不再用 `@projects/...` 展开混合参照说明。

## LibTV Remote Opening

发送给 LibTV 的 `*-libtv-submission.txt` 必须以此固定开头开始，且必须位于任何 `分镜组原文`、`分镜明细` 或长正文之前：

```text
【LibTV 调用锁定】
provider: seedance2.0
taskType: video
modeType: mixed2video
mixedList: [{"url": "<uploaded_url_1>", "type": "image"}, {"url": "<uploaded_url_2>", "type": "image"}, ...]
mixedList 单个分镜组最多 9 张图；故事板总参照与主体参照共同计入上限。
duration: <duration_hint>
duration_rule: 从当前分镜组时长估算计算；小于等于4秒按4秒，4到15秒之间按估算值，大于等于15秒按15秒。
ratio: 16:9
resolution: 720p
enableSound: on
audio_preflight_required: true
生成前必须确认远端 create_generation_task.params.enableSound 为 on / true；不得只把声音要求写在自然语言 prompt 中。
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
transport_only_projection: true
禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头。
只允许执行 transport_only 投影：上传 URL、mixedList、duration、ratio、resolution、enableSound。
```

远端提交文本只能通过 `【分镜组源文本】` fenced YAML 的 `故事板参照.uploaded_url` 和主体列表项 `uploaded_url` 表达混合参照绑定；不得包含 `@projects/...`、`/Volumes/...` 或其他本地图片路径，也不得人工预设 `参照图1/2/N` 编号。
缺故事板、缺主体图、无缓存 URL、未进入预算或被排除主体不得写入远端 `libtv-submission.txt`，只能写入 manifest / submit plan / report；不得出现“无独立参照图 / 无缓存 URL / 未进入预算主体 / 不创建空图片槽”等说明行。
远端生成 prompt 完整体必须包含 source-first enriched YAML 形态的 `【分镜组源文本】`；不得另起 `【混合参照说明】`，不得只把混合参照作为 `mixedList` 的匿名图片数组。若系统自动生成图片 token / 图片编号，每个 token / 编号 / 参照 URL 必须邻近故事板身份或主体名称。
默认远端提交必须采用 `strict_original + transport_only`，`allow_libtv_prompt_optimization=false`。这表示只允许把本地路径投影为上传 URL、补齐 `mixed2video / mixedList / duration / ratio / resolution / enableSound` 等技术参数，不允许 LibTV 远端 Agent 对 `【分镜组源文本】` 做提示词优化、重新编排、摘要、改写或补镜头。`duration` 必须来自当前组 submit plan 的 `duration_hint`，不得固定写 15 秒。
只有用户显式选择 `libtv_optimize` 或显式声明 `allow_libtv_prompt_optimization: true` 时，才允许远端做创作型编排；该选择必须写入 submit plan、queue 和 report。

若故事板图缺失，不得保留空 `@图1`，也不得在远端提交中写“故事板总参照：缺失”。缺失原因只写入 manifest / submit plan / report；`【分镜组源文本】` 的 fenced YAML 直接不注入 `故事板参照.uploaded_url`。

## Subject Inline Binding

- 主体参照来自组底 YAML 的 `角色 / 场景 / 道具`。
- 有图主体必须在 fenced YAML 的对应主体列表项中写入 `name` 和 `uploaded_url`。
- 示例：`角色: [{name: 林夏, uploaded_url: "https://..."}]`；实际落盘使用块状 YAML，保持可读。
- 远端 `*-libtv-submission.txt` 中必须保留该 YAML 绑定；不得只写裸 URL，也不得人工预设 `参照图N` 编号。
- 缺图主体保留为原 YAML 名称，作为源文本约束；不得追加空 marker，不得写入空 `uploaded_url`；在 manifest 记录 `missing_optional`。

## Direct Generation Request

远端 `*-libtv-submission.txt` 必须在 `【分镜组源文本】` 前写入：

```text
【直接生成请求】
请基于下方【分镜组源文本】，按 `mixed2video + mixedList` 生成一条连续视频。【分镜组源文本】保留了原始分镜组正文，且其 fenced YAML 中的 `故事板参照.reference_index / uploaded_url` 和主体列表项 `reference_index / uploaded_url` 已绑定对应故事板总参照与主体参照图；reference_index=1 对应 mixedList[0] / 系统自动图1，reference_index=2 对应 mixedList[1] / 系统自动图2，依次类推。请把原始正文和 YAML 顺序绑定关系共同作为生成 prompt 完整体。生成时参考故事板总参照作为整体构图、镜头顺序、角色站位、场景连续性与情绪节奏参考，不要把故事板参照当作单一首帧；每个主体 uploaded_url 用于锁定对应角色、场景或道具外观，不得互相替换。如系统自动插入真实图片 token 或编号，必须把故事板身份或主体名和 reference_index 放在对应 token/编号旁边。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把混合参照简化为裸图片 token、裸图片编号或裸 URL。
```

## Body Rule

`【分镜组源文本】` 直接接入 `4-分组` 的完整组正文，只允许在 fenced YAML 内注入 uploaded_url 绑定。LLM 可以调整 provider 指令层的表达，但不得删改分镜事实、镜头顺序、动作结果或 YAML 主体。未 opt-in `libtv_optimize` 时，任何远端优化版提示词、摘要版分镜或镜头计划都不是正常执行步骤，必须按 `prompt_fidelity_violation / libtv_optimize_without_opt_in` 返工。

## Marker Ordering

1. 故事板总参照优先占用第一个 marker，例如 `@图1`。
2. 主体参照按 YAML 顺序分配后续 marker。
3. 若无故事板图，主体参照从 `@图1` 开始，但必须在 prompt 中说明没有故事板总参照。
4. manifest 必须保存 marker、role、source_path、subject_name、subject_type。

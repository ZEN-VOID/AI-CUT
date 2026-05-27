# Hybrid Prompt Assembly Contract

本文件定义 `D-主板混合参照` 的 prompt 组装规则。

## Prompt Shape

每条 D 本地审核 `prompt.md` 必须采用 source-first YAML 两阶段处理：draft 直接保留 `4-分组/第N集.md` 中对应 `## x-y-z` 分镜组原文，包含标题、正文和原始 fenced YAML，不提前写死 `reference_index / uploaded_url`；final 才按最终 `generation_slots` 回刷参照字段。不得在原文前另写“固定开头”“混合参照说明”或缺图说明段。

唯一允许的机械注入位置是该组 fenced YAML：

- 故事板图唯一绑定、上传并确认槽位后，新增或更新 `故事板参照` 对象，写入 `name: 故事板总参照`、`role: storyboard_sheet`、`reference_index`、真实 `uploaded_url` 和可选 `image_token`。
- 已绑定、上传并确认槽位的 YAML 主体，把原 `角色 / 场景 / 道具` 列表项扩展为对象并补入 `name`、`reference_index`、真实 `uploaded_url` 和可选 `image_token`；缺图、未入预算或没有上传 URL 的主体保留原名称，不写空 URL、不写 `null`、不写缺图解释。
- `uploaded_url` 来自 `asset_uploads` 的身份映射；`reference_index` 来自 `generation_slots` 的视频生成槽位顺序。OSS 上传顺序本身不得决定 `reference_index`；若视频生成框 UI 缩略图顺序可观测，UI 图N / `Image N` 是最终槽位真源；只有 UI 槽位不可观测时才退回用远端实际 `mixedList[n].url` 反查。`reference_index` 使用 1-based 顺序，必须与最终 UI 图N / `mixedList` 数组顺序、LibTV 自动生成的图1/图2/图3顺序保持一致。
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
audio_preflight: unverified_non_blocking_when_cli_only
若当前 CLI 无法在生成前确认远端 create_generation_task.params.enableSound，则记录 audio_preflight_unverified_non_blocking，继续提交，并以后验音频门验收。
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
transport_only_projection: true
禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头。
只允许执行 transport_only 投影：上传 URL、mixedList、duration、ratio、resolution、enableSound。
```

远端提交文本只能通过 final `【分镜组源文本】` fenced YAML 的 `故事板参照.reference_index / uploaded_url / image_token` 和主体列表项 `reference_index / uploaded_url / image_token` 表达混合参照绑定；不得包含 `@projects/...`、`/Volumes/...` 或其他本地图片路径，也不得人工预设 `参照图1/2/N` 编号。
缺故事板、缺主体图、无缓存 URL、未进入预算或被排除主体不得写入远端 `libtv-submission.txt`，只能写入 manifest / submit plan / report；不得出现“无独立参照图 / 无缓存 URL / 未进入预算主体 / 不创建空图片槽”等说明行。
远端生成 prompt 完整体必须包含 final source-first YAML 形态的 `【分镜组源文本】`；不得另起 `【混合参照说明】`，不得只把混合参照作为 `mixedList` 的匿名图片数组。若系统自动生成图片 token / 图片编号，每个 token / 编号 / 参照 URL 必须邻近故事板身份或主体名称。
若 LibTV 端实际加载 URL 或 UI 缩略图顺序可观测且与预期不同，最终 prompt 必须以 UI 图N优先；UI 不可观测时才以远端实际 `mixedList[n].url` 反查 `asset_uploads` 后生成的 `generation_slots` 为准：图1 / `mixedList[0]` 反查出的故事板或主体写 `reference_index: 1`，图2 / `mixedList[1]` 反查出的故事板或主体写 `reference_index: 2`，依次类推。不得假设 name-OSS 配对会让 LibTV 自动按 YAML 名称匹配图片。
默认远端提交必须采用 `strict_original + transport_only`，`allow_libtv_prompt_optimization=false`。这表示只允许把本地路径投影为上传 URL、补齐 `mixed2video / mixedList / duration / ratio / resolution / enableSound` 等技术参数，不允许 LibTV 远端 Agent 对 `【分镜组源文本】` 做提示词优化、重新编排、摘要、改写或补镜头。`duration` 必须来自当前组 submit plan 的 `duration_hint`，不得固定写 15 秒。
只有用户显式选择 `libtv_optimize` 或显式声明 `allow_libtv_prompt_optimization: true` 时，才允许远端做创作型编排；该选择必须写入 submit plan、queue 和 report。

若故事板图缺失，不得保留空 `@图1`，也不得在远端提交中写“故事板总参照：缺失”。缺失原因只写入 manifest / submit plan / report；`draft` 原 YAML 不预填绑定，`final` 的 fenced YAML 直接不注入 `故事板参照` 绑定字段。

## Subject Inline Binding

- 主体参照来自组底 YAML 的 `角色 / 场景 / 道具`。
- 有图主体必须在 final fenced YAML 的对应主体列表项中写入 `name`、`reference_index`、真实 `uploaded_url` 和可选 `image_token`。
- 示例：`角色: [{name: 林夏, reference_index: 2, uploaded_url: "https://...", image_token: "{{Image 2}}"}]`；实际落盘使用块状 YAML，保持可读。
- 远端 `*-libtv-submission.txt` 中必须保留该 YAML 绑定；不得只写裸 URL，也不得人工预设 `参照图N` 编号。
- 缺图主体保留为原 YAML 名称，作为源文本约束；不得追加空 marker，不得写入空 `uploaded_url`；在 manifest 记录 `missing_optional`。

## Direct Generation Request

远端 `*-libtv-submission.txt` 必须在 `【分镜组源文本】` 前写入：

```text
【直接生成请求】
请基于下方【分镜组源文本】，按 `mixed2video + mixedList` 生成一条连续视频。【分镜组源文本】保留了原始分镜组正文，且其 fenced YAML 中的 `故事板参照.reference_index / uploaded_url / image_token` 和主体列表项 `reference_index / uploaded_url / image_token` 已绑定对应故事板总参照与主体参照图；reference_index=1 对应 mixedList[0] / 系统自动图1，reference_index=2 对应 mixedList[1] / 系统自动图2，依次类推。请把原始正文和 YAML 顺序绑定关系共同作为生成 prompt 完整体。生成时参考故事板总参照作为整体构图、镜头顺序、角色站位、场景连续性与情绪节奏参考，不要把故事板参照当作单一首帧；每个主体 uploaded_url 用于锁定对应角色、场景或道具外观，不得互相替换。如系统自动插入真实图片 token 或编号，必须把故事板身份或主体名和 reference_index 放在对应 token/编号旁边。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把混合参照简化为裸图片 token、裸图片编号或裸 URL。
```

## Body Rule

`【分镜组源文本】` 直接接入 `4-分组` 的完整组正文，draft 不预填绑定字段，final 只允许在 fenced YAML 内注入 `reference_index / uploaded_url / image_token` 绑定。LLM 可以调整 provider 指令层的表达，但不得删改分镜事实、镜头顺序、动作结果或 YAML 主体。未 opt-in `libtv_optimize` 时，任何远端优化版提示词、摘要版分镜或镜头计划都不是正常执行步骤，必须按 `prompt_fidelity_violation / libtv_optimize_without_opt_in` 返工。

## Marker Ordering

1. 故事板总参照优先占用第一个 marker，例如 `@图1`。
2. 主体参照按 YAML 顺序分配后续 marker。
3. 若无故事板图，主体参照从 `@图1` 开始，但必须在 prompt 中说明没有故事板总参照。
4. manifest 必须保存 marker、role、source_path、subject_name、subject_type。
5. 以上 marker 只代表预期槽位；最终 `reference_index` 必须以 `generation_slots` 或远端实际 `mixedList` 顺序为准。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 本地 `prompt.md` 的 draft 是否直接以原 `## group_id` 组正文和原始 fenced YAML 为主体，没有在原文前另写固定开头、混合参照说明或缺图说明？ | `GATE-VIDHYB-PROMPT-01` | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` / `references/hybrid-prompt-assembly-contract.md` | draft prompt snapshot、prefix scan、source line/body hash 对照 |
| draft 阶段是否没有提前写死 `reference_index / uploaded_url / image_token`、空 URL 或占位 URL，避免后续 UI 槽位变化造成错绑？ | `GATE-VIDHYB-PROMPT-01` | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` | draft prebinding scan、empty URL scan、slot phase note |
| final 是否只在 fenced YAML 内新增或更新 `故事板参照` 对象，并写入 `name: 故事板总参照`、`role: storyboard_sheet`、真实 `reference_index / uploaded_url` 和可选 `image_token`？ | `GATE-VIDHYB-PROMPT-02` | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` / `N3-STORYBOARD-BIND` | final YAML diff、storyboard_total_reference manifest、slot ledger |
| 已绑定主体是否只把原 YAML `角色 / 场景 / 道具` 列表项扩展为对象，并写入对应 `name + reference_index + uploaded_url + image_token`；缺图、未入预算或未上传主体是否保留原名称且不写空槽？ | `GATE-VIDHYB-PROMPT-02` | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` / `N4-SUBJECT-BIND` | final YAML subject diff、manifest bound/missing subjects、empty slot scan |
| `uploaded_url` 是否只来自 `asset_uploads` 身份映射，而 `reference_index` 是否只来自 UI 图N或实际 `mixedList` 形成的 `generation_slots`？ | `GATE-VIDHYB-SLOT-01` | `FAIL-VIDHYB-UPLOAD-SLOT-CONFLATION` | `N6-PLAN-BUILD` / `references/hybrid-prompt-assembly-contract.md` | asset_uploads ledger、generation_slots ledger、URL 反查记录、final YAML slot projection |
| 若 UI 图N / `Image N` 可观测，是否优先使用 UI 槽位真源；UI 不可观测时才用远端实际 `mixedList[n].url` 反查，且没有把 OSS 上传顺序当成图N顺序？ | `GATE-VIDHYB-SLOT-01` | `FAIL-VIDHYB-UPLOAD-SLOT-CONFLATION` | `N6-PLAN-BUILD` | UI slot capture 或 mixedList query、upload order comparison、slot projection notes |
| `*-libtv-submission.txt` 是否以 `【LibTV 调用锁定】` 开头并在正文前锁定 provider、taskType、modeType、mixedList、duration、ratio、resolution、enableSound 与 fidelity 字段？ | `GATE-VIDHYB-REMOTE-01` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `references/libtv-handoff.md` | submission header snapshot、modeType、mixedList/text2video route、duration fields |
| 有任一故事板或主体参照图时是否固定 `modeType=mixed2video` 且 `mixedList` 最多 9 张；完全无图时才固定 `modeType=text2video`，没有传空图片槽？ | `GATE-VIDHYB-REMOTE-01` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` | submit plan image count、mixedList count、text2video no-image evidence、budget notes |
| 远端提交文本是否没有本地路径、`@projects/...`、`/Volumes/...`、人工 `参照图1/2/N` 编号、缺图/无缓存/未入预算说明或空槽说明？ | `GATE-VIDHYB-REMOTE-02` | `FAIL-VIDHYB-REF-PROMPT-INTEGRITY` | `N5-PROMPT-ASSEMBLE` / `N6-PLAN-BUILD` | submission text scan、本地路径 scan、forbidden phrase scan |
| `【直接生成请求】` 是否明确要求基于下方 final `【分镜组源文本】`，并把原始正文与 fenced YAML 中故事板/主体槽位绑定共同作为 prompt 完整体？ | `GATE-VIDHYB-REMOTE-02` | `FAIL-VIDHYB-REF-PROMPT-INTEGRITY` | `N5-PROMPT-ASSEMBLE` | direct request snapshot、final source-first YAML、token/name adjacency evidence |
| 远端提交是否默认声明 `strict_original + transport_only`、`allow_libtv_prompt_optimization=false`，并禁止优化、重排、摘要、改写或补镜头？ | `GATE-VIDHYB-FIDELITY-01` | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` / `N7-REVIEW-GATE` | submit plan fidelity fields、submission constraints、query prompt comparison |
| 只有用户显式选择 `libtv_optimize` 或 `allow_libtv_prompt_optimization: true` 时，是否才允许远端创作型编排，并把该 opt-in 写入 submit plan、queue 和 report？ | `GATE-VIDHYB-FIDELITY-01` | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` / `N7-REVIEW-GATE` | user opt-in evidence、submit plan、queue ledger、report fidelity note |
| `duration` 是否来自当前组 submit plan 的 `duration_hint`，没有固定写 15 秒或跨组复用时长？ | `GATE-VIDHYB-DURATION-01` | `FAIL-VIDHYB-DURATION` | `N6-PLAN-BUILD` / `references/group-source-extraction.md` | submit plan `duration_hint`、submission duration、group duration source |
| 若生成前无法验证 `create_generation_task.params.enableSound`，是否记录 `audio_preflight_unverified_non_blocking` 并继续；生成后是否仍以后验音频证据验收？ | `GATE-VIDHYB-REMOTE-01` | `FAIL-VIDHYB-AUDIO-PREFLIGHT` | `N6-PLAN-BUILD` / `references/libtv-handoff.md` | submission `enableSound=on`、audio_preflight note、query/ffprobe evidence |
| marker 顺序是否只是预期槽位辅助，最终 `reference_index` 是否以 `generation_slots` 或远端实际 `mixedList` 顺序为准，而不是以 `@图1` 文案强行决定？ | `GATE-VIDHYB-SLOT-01` | `FAIL-VIDHYB-UPLOAD-SLOT-CONFLATION` | `N6-PLAN-BUILD` / `N5-PROMPT-ASSEMBLE` | marker manifest、generation_slots ledger、final YAML reference_index audit |

# Video Prompt Assembly Contract

本文件定义 step1 之后的组级视频 prompt 组装规则。目标是把 `5-分组` 的现有组正文保真转换为 LibTV 可提交文本，而不是重新创作分镜。

## Prompt Shape

每个分镜组生成一个独立 `prompt.md`。`prompt.md` 始终必须是 source-first YAML：直接保留 `5-分组/第N集.md` 中对应 `## x-y-z` 分镜组原文，包含标题、正文和 fenced YAML；不得在原文前另写“请根据以下完整分镜组内容...”、`主体参照说明：`、`分镜组原文：` 或缺图说明段。

`prompt.md` 有两个合法相位：

- `draft`：用于提取、主体匹配、OSS 上传和 UI 槽位确认前的工作稿。它只保留原组 fenced YAML，不提前写 `reference_index`、`uploaded_url`、空 URL 或占位 URL。
- `final`：用于提交或重提 LibTV。唯一允许注入的位置是该组 fenced YAML；对已绑定并已上传的主体，把原 YAML 列表项扩展为对象并补入 `reference_index`、真实 `uploaded_url` 和可选 `portrait_token`。

`uploaded_url` 来自 `asset_uploads` 的 `name -> OSS URL` 身份映射，`reference_index` 来自 `generation_slots` 的图N槽位顺序。OSS 上传顺序本身不得决定 `reference_index`；若视频生成框 UI 缩略图顺序可观测，UI 图N / `Portrait N` 是最终槽位真源，优先级高于 YAML 文本出现顺序、OSS 上传顺序和工具层 `mixedList` 回显。`reference_index` 使用 1-based 顺序，必须与最终视频生成槽位、LibTV 自动生成的图1/图2/图3顺序保持一致。可额外写 `portrait_token` 记录 UI 槽位，但 `uploaded_url` 必须仍是真实 OSS URL。缺图、未入预算或没有上传 URL 的主体保留原名称，不写空 URL、不写 `null`、不写缺图解释。final 示例：

```text
## 1-1-1

<直接保留分镜组正文>

```yaml
字数统计: 420字
时长估算: 约12秒
角色:
  - name: 林寂
    reference_index: 1
    uploaded_url: "https://libtv-res.liblib.art/claw/<projectUuid>/linji.png"
  - 未绑定角色名
场景:
  - name: 永夜私立中学二年级A班教室
    reference_index: 2
    uploaded_url: "https://libtv-res.liblib.art/claw/<projectUuid>/classroom.png"
道具: []
```
```

本地路径、源图指纹、缺图原因、预算取舍原因仍归 `reference-manifest.json`、submit plan 和 report 管理；`prompt.md` 不再用 `@projects/...` 展开主体参照说明。发送给 LibTV 的 `*-libtv-submission.txt` 必须在运输层固定开头后复用 final source-first enriched YAML 文本，但不得包含本地路径。若 `prompt.md` 仍处于 draft 相位，不得创建最终远端提交；需要先用已确认的 `generation_slots` 回刷为 final。

## Prompt Fidelity Modes

默认提交口径是 `strict_original + transport_only`，即默认不授权 LibTV 远端提示词优化：

| mode | default | allowed | forbidden |
| --- | --- | --- | --- |
| `strict_original` | yes | 将 source-first enriched YAML 作为生成 prompt 完整体；分镜组标题、正文和非注入字段必须逐字保留，主体 URL 只写入 YAML 的 `uploaded_url` 字段 | 改写、摘要、重排、压缩、合并镜头、补镜头、把源文本改成优化版提示词、只保留裸图片 token |
| `transport_only` | yes | 从 manifest / plan 把 uploaded URL 注入 YAML，裁剪超过 provider 上限的参照图，补齐 `mixed2video / mixedList / duration / ratio / resolution / enableSound` 等技术参数 | 改动分镜内容、角色动作、对白、镜头顺序、音效、氛围事实 |
| `controlled_libtv_optimize` | no | 用户显式 opt-in 后，允许 LibTV 优化影像生成提示词、镜头衔接、动作连贯、光影氛围和物理音效表达；source-first enriched YAML 仍作为事实真源 | 未显式 opt-in 时不得启用；不得改写、删减、翻译或替换对白、旁白、音效文字、主体绑定、分镜顺序和视频参数 |
| `libtv_optimize` | no | 在用户显式 opt-in 后，允许 LibTV 重新组织提示词、压缩、合并镜头或做工作流规划 | 未显式 opt-in 时不得启用 |

字段约束：

- `prompt_fidelity_mode` 默认值为 `strict_original`。
- `allow_libtv_prompt_optimization` 默认值为 `false`；只有用户显式 opt-in `controlled_libtv_optimize` 或 `libtv_optimize` 时才允许改为 `true`。
- 默认只允许运输层投影：上传 URL、`mixedList`、时长、比例、分辨率和声音参数；画面提示词、镜头衔接、动作连贯、光影氛围等表达层优化也默认禁止。
- `strict_original` 下，final `prompt.md` 和远端生成 prompt 主体必须以当前分镜组 source-first enriched YAML 为事实真源；主体名、`reference_index` 与 uploaded URL 的绑定只通过原组 YAML 的对象化列表项表达。技术投影只能发生在远端调用锁定、YAML `reference_index / uploaded_url / portrait_token` 和 provider 参数区，不得把主体名绑定裁掉。`taskType` / `params` 等远端工具 envelope 字段不是投递文本真源，字段变体不得被单独判定为主体参照投递失败。
- 由于 LibTV / Seedance 最终可能只按图片数组顺序理解图1、图2、图3，`reference_index` 是硬绑定字段：`reference_index: 1` 对应 `mixedList[0]`，也对应远端自动图1；`reference_index: 2` 对应 `mixedList[1]`，也对应远端自动图2。禁止只校验 URL 集合一致而不校验顺序一致。
- 若远端返回内容显示其在 `create_generation_task` 前自行生成“优化版提示词 / 重新编排脚本 / 镜头计划 / 摘要版分镜”，且本地未 opt-in，必须判定为 `prompt_fidelity_violation`。

## LibTV Remote Opening

`*-libtv-submission.txt` 必须以此固定开头开始，且必须位于任何 `分镜组原文`、`分镜明细` 或长正文之前：

```text
【LibTV 调用锁定】
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
不允许优化、润色、压缩、摘要、重排或改写【分镜组源文本】中的提示词表达。
硬锁定事实：分镜组标题、正文、对白、旁白、音效文字必须逐字保留；角色名、场景名、道具名、分镜顺序、fenced YAML 中的 reference_index 与 uploaded_url、mixedList 数组顺序、duration、ratio、resolution、enableSound 不得改写、删减、翻译或替换。
禁止把【分镜组源文本】转换成优化版提示词、工作流说明或镜头计划。
必须将【分镜组源文本】中原始正文和 fenced YAML 的 reference_index + uploaded_url 主体绑定共同作为生成 prompt 的完整主体。
禁止在提交文本中脱离 YAML 手写“参照图1/2/N”人工编号；但必须遵守 YAML `reference_index` 顺序：reference_index=1 对应 mixedList[0] / 系统自动图1，reference_index=2 对应 mixedList[1] / 系统自动图2，依次类推。
禁止在生成 prompt 中只保留裸图片 token、裸图片编号或裸 URL；若系统自动生成图片 token/图片编号，每个 token/编号必须邻近对应主体名称和 reference_index。
只允许执行 transport_only 投影：上传 URL、mixedList、duration、ratio、resolution、enableSound。
禁止调用 ask_user。
禁止向用户确认、展示“请稍候”、等待下一条消息。
用户已授权立即生成。
如果需要模型参数，直接使用下方固定参数，不要查询后停顿。
无法创建生成节点时，直接返回 ERROR_NO_GENERATION_NODE。
provider: seedance2.0
taskType: video
说明：taskType / params 属于 LibTV 远端 Agent 工具调用 envelope 的观测项；投递文本只负责提供可执行生成意图、主体绑定、mixedList 和视频参数，不把远端 envelope 字段变体作为投递文本失败依据。
modeType: mixed2video
mixedList: [{"url": "<uploaded_url_1>", "type": "image"}, {"url": "<uploaded_url_2>", "type": "image"}, ...]
mixedList 单个分镜组最多 9 张图；超过时角色和场景优先，先排除道具，其次排除重复、不必要或可由源文本保留的次要主体。
duration: <duration_hint>
duration_rule: 从当前分镜组时长估算计算；小于等于4秒按4秒，4到15秒之间按估算值，大于等于15秒按15秒。
ratio: 16:9
resolution: 720p
enableSound: on
audio_preflight_required: false
若当前调用面无法在生成前验证 create_generation_task.params.enableSound，记录 `audio_preflight_unverified_non_blocking` 并继续提交；生成后仍需音频 URL、task_result.audios 或 ffprobe 音轨验收。

【视频默认规格】
硬性生成参数：这是 <duration_hint> 秒视频，不是固定 15 秒或默认 10 秒。生成前必须把画布/视频时长设置为 <duration_hint> 秒；<duration_hint> 来自当前分镜组的时长估算并按 4-15 秒范围 clamp。声音/音频开启，保留物理互动音效、环境声、对白声音和旁白声音；不生成 BGM。横屏 16:9，720P。

【给龙虾的工作流管理要求】
把全部工作流和结果都放在画布上。不要把这句话转化为确认问题或等待消息；它是执行要求。

【直接生成请求】
请在严格原文模式下，基于下方【分镜组源文本】按 `mixed2video + mixedList` 生成一条连续视频。不得优化、润色、压缩、摘要、重排或改写画面提示词、镜头衔接、动作表达、光影氛围、对白、旁白和音效文字；必须保持分镜顺序、角色动作、主体参照绑定、reference_index、uploaded_url、mixedList 顺序不变。【分镜组源文本】保留了原始分镜组正文，且其 fenced YAML 中的 `reference_index` 和 `uploaded_url` 字段已经绑定对应主体参照图；请把原始正文和 YAML 主体 `reference_index + uploaded_url` 绑定关系共同作为生成 prompt 完整体。图像顺序以 YAML `reference_index` 为准：reference_index=1 对应 mixedList[0] / 系统自动图1，reference_index=2 对应 mixedList[1] / 系统自动图2，依次类推。生成时保持身份、外观、服装、材料、体态、空间或动作关系连续性。如系统自动插入真实图片 token 或编号，必须把主体名和 reference_index 放在对应 token/编号旁边。禁止把主体参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<直接粘贴 final source-first enriched YAML 分镜组全文>
```

远端提交口径要求：

- 默认必须声明 `prompt_fidelity_mode: strict_original` 和 `allow_libtv_prompt_optimization: false`；不允许 LibTV 做提示词优化、润色、压缩、摘要、重排或改写。
- `【直接生成请求】` 不写“不生成字幕，不生成背景音乐”句；该类视频规格约束只能保留在 `【视频默认规格】`、源分镜原文或 provider 参数区，避免直接请求首段过载。
- 默认必须显式列出硬锁定事实；只有用户 opt-in `controlled_libtv_optimize` 或更强 `libtv_optimize` 时才允许远端优化，并需在 submit plan / report 中记录。
- `*-libtv-submission.txt` 不得包含 `@projects/...`、绝对本地路径或其他本地文件路径；远端只接收 source-first enriched YAML 中的 `name + uploaded_url` 绑定，不得接收人工预设的 `参照图N` 编号。
- `mixedList` 内必须直接填入上传返回的真实 URL，并使用严格 JSON 对象写法；不得写 `参照图N URL`、`<uploaded_url>` 或其他占位符后再期待远端二次解析；单个分镜组 `mixedList` 必须小于等于 9 张图。
- `mixedList`、final source-first enriched YAML 中的 `reference_index / uploaded_url / portrait_token` 和 submit plan `images[]` 必须是一组可机械互证的投影：每个进入 `mixedList` 的 URL 必须在 YAML 中邻近唯一主体名；每个 YAML `uploaded_url` 也必须存在于 `mixedList`；`reference_index` 必须等于 submit plan `images[].upload_index`，且 `mixedList[reference_index-1].url` 必须等于该 YAML `uploaded_url`；每个 uploaded URL 的 `/claw/<projectUuid>/` 必须与 submit plan 锁定的 `projectUuid` 一致。
- 若 LibTV 端实际加载顺序可观测且与预期不同，最终 prompt 必须以视频生成框 UI 缩略图槽位优先生成 `generation_slots`：UI 图1 / `Portrait 1` 对应主体写 `reference_index: 1`，UI 图2 / `Portrait 2` 对应主体写 `reference_index: 2`，依次类推；只有 UI 槽位不可观测时才退回用远端实际 `mixedList[n].url` 反查 `asset_uploads`。不得假设 name-OSS 配对会让 LibTV 自动按 YAML 名称匹配图片。
- 远端提交不再单独创建 `【已上传主体参照 URL】` 或 `【主体参照说明】` 段；主体绑定只保留在原组 YAML 的 `uploaded_url` 字段中。
- 参照连续性要求不得单独列标题；连续性句只能出现一次，并应并入首段生成请求或 `【直接生成请求】`，且必须位于 `【分镜组源文本】` 之前，使其先于源文本内“视频生成的画面风格，光影和氛围与场景参照图保持一致。”等风格约束生效。
- 缺图、无可复用 URL、未进入预算或被取舍的主体不得写入远端 `libtv-submission.txt`；不得出现“无独立参照图 / 无可复用 URL / 未进入预算主体 / 不创建空图片槽”等说明行。它们只能写入 `reference-manifest.json`、submit plan 或执行报告。
- 不得静默复用同一个 uploaded URL 表示多个主体；确需共享时，必须在 manifest / submit plan 写明 `shared_reference_group` 和 `primary_subject_name`，远端主体说明也必须写清“共用同一参照图”的关系。
- `duration` 必须使用当前组 submit plan 的 `duration_hint`，不得固定写 15 秒；`duration_hint` 由 `duration_estimate_seconds` clamp 到 4-15 秒得到。
- 远端最终 `create_generation_task.params.prompt` 必须同时包含主体名称、`reference_index` 和对应图片 token/编号/URL；只有当 LibTV 自动插入真实图片编号后，才把主体名与 `reference_index` 邻近该真实编号。不得生成只有 `{{Image 1}} {{Image 2}} ...`、`图片1 图片2 ...` 或裸 URL 列表开头的 prompt。
- 远端工具 envelope 只作为 query 后观测项：若出现明确 tool error（例如 `params is required`）、`ask_user` 等待态、长时间无生成节点或主体名绑定丢失，才记录失败；仅出现 `task_type` 或字符串型 `params`，但没有明确错误时，不得阻断或判死。投递文本层只裁决主体名+URL绑定、`mixedList`、时长、比例、分辨率、声音请求和源文本保真。
- 远端提交必须请求 `enableSound:on`；若字段缺失、为 `off/false`、只存在于 prompt 文本，或当前 provider 不支持可验证音频开关，记录 `audio_preflight_unverified_non_blocking`，不作为提交阻断。最终音频通过必须依赖音频 URL、`task_result.audios` 或下载后 `ffprobe`。
- 固定开头必须显式禁止 `ask_user`、确认、等待下一条消息和“请稍候”状态式回复；远端若不能创建生成节点，应返回 `ERROR_NO_GENERATION_NODE`，不得进入用户确认循环。
- `分镜组源文本` 是连续视频约束文本，不是图片生成任务列表；固定开头必须显式防止远端代理把它改路由为分镜图流程。
- 若某主体缺图，或因 9 图预算被取舍，只能在 manifest / submit plan / 报告中写明原因；远端提交必须直接省略该主体，不得生成空 `参照图` 槽位，不得进入 `mixedList`，不得用“无独立参照图、无可复用 URL 或未进入预算主体”列表污染 LibTV prompt。
- `【直接生成请求】` 必须出现在 `【分镜组源文本】` 前，避免远端先读到 `分镜明细` 后自动规划图片工作流。

## Provider Instruction Boundary

- 可以添加最小 provider 指令，例如横屏、连续视频、保持镜头顺序、参照图路径绑定。
- 不得重写 `group_body` 中的剧情事实、镜头顺序或角色动作。
- 不得把 YAML 主体清单写成剧情正文；只可在每个有图且已上传的主体项中注入 `uploaded_url`。
- 本地路径只留在 manifest / submit plan / report；prompt 与 LibTV 远端提交必须使用上传后的 URL 和主体名，不得把本地路径发送给远端，也不得预设 `参照图N` 人工编号。
- 远端生成 prompt 完整体必须包含 source-first enriched YAML 分镜组全文；不得只把去掉 YAML 的正文投给 `params.prompt`，也不得只把主体参照作为 `mixedList` 的匿名图片数组。
- LibTV 远端提交 prompt 必须明确锁定 `modeType=mixed2video` 和 `mixedList`；不得只用自然语言描述“全能参照”。
- 不得承诺 LibTV 不支持的参数或能力；模型、时长、分辨率以 `.agents/skills/cli/libTV` 当前约束为准。

## Reference Path Suffix Rule

- 当使用 `libtv_session_with_uploaded_references` 时，draft prompt 必须先保持 YAML 未绑定；final prompt 必须把对应 YAML 主体列表项扩展为对象并补 `reference_index`、真实 `uploaded_url` 和可选 `portrait_token`，例如 `- name: 林寂` + `reference_index: 1` + `uploaded_url: "https://..."` + `portrait_token: "{{Portrait 1}}"`。
- 缺图主体保留原名称，不得添加空 `uploaded_url`，也不得写 `uploaded_url: null` 或缺图解释。
- final YAML 中 `reference_index / uploaded_url / portrait_token` 的顺序必须与最终 `generation_slots` 和 submit plan 的 `images[]` 顺序一致；prompt 内不使用抽象占位符替代 URL。若 UI 槽位已观测，submit plan 的 `images[].upload_index` 必须表达 UI 图N槽位，原始 OSS 上传顺序另写 `oss_upload_index`。
- 对 `*-libtv-submission.txt`，YAML `reference_index / uploaded_url` 必须和 `mixedList` 真实 URL 项逐项一致；不得脱离 YAML 另造 `参照图N` 映射。
- 对远端 `create_generation_task.params.prompt`，若 LibTV 系统自动插入图片 token / 图片编号，必须与主体名和 `reference_index` 同段绑定，例如 `{{Image 1}} 任盈盈 reference_index=1` 或 `任盈盈 reference_index=1 {{Image 1}}`。只有 `{{Image 1}} {{Image 2}}` 或 `图片1 图片2` 的裸 token 序列视为主体名绑定丢失。

## Length Handling

- 默认保留完整 `group_body`。
- 若 LibTV prompt 长度或人工策略要求压缩，必须先获得用户对 `libtv_optimize` 或等价压缩策略的显式 opt-in，并在 submit plan 中记录：
  - `source_group_body_preserved: true`
  - `prompt_compression: none / reviewed_summary`
  - `source_group_body_path`
  - `compression_reason`
- 压缩只能保留事实，不得添加新剧情。

## Gate

通过 prompt gate 必须满足：

1. prompt 能回指 `source_file` 与 `group_id`。
2. `group_body` 是主要内容，且没有被剧情改写。
3. draft 相位不得伪造空 `reference_index / uploaded_url`；final 相位若存在参考图，对应 YAML 主体项有 `reference_index`、真实 `uploaded_url` 和可选 `portrait_token`，且顺序与最终 `generation_slots`、`images[]`、`mixedList` 逐项一致。
4. 若没有参考图，prompt 不包含空 `uploaded_url`、`uploaded_url: null` 或缺图解释。
5. `*-libtv-submission.txt` 以 `【LibTV 调用锁定】` 开头；有主体参照图时包含 `modeType: mixed2video` 和 `mixedList`，无图时包含 `modeType: text2video`。
6. `*-libtv-submission.txt` 不包含本地图片路径，只包含已上传 URL 和主体名绑定关系；不得预设 `参照图1/2/N` 人工编号。
7. `*-libtv-submission.txt` 在 provider 参数前包含 no-ask 约束：禁止 `ask_user`、禁止确认、禁止等待下一条消息、用户已授权立即生成。
8. 默认提交包含 `prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false` 和硬锁定事实约束；`【直接生成请求】` 不写“不生成字幕，不生成背景音乐”句。
9. 若 submit plan 未记录用户 opt-in，远端 query 中不得出现 LibTV 自行生成的优化版提示词、重新编排脚本、镜头计划、摘要版分镜或任何表达层优化。
10. 远端工具 envelope 变体（例如 `task_type` 或字符串型 `params`）只记录为 `generation_envelope_variant`；只有出现明确 tool error、`params is required`、`ask_user` 等待态、无生成节点超时或主体名绑定丢失时，才不得标记为正常 pending。
11. 远端提交文本必须请求 `enableSound:on`；若无法在生成前确认该字段，状态记录为 `audio_preflight_unverified_non_blocking`，仍可进入提交/排队；最终报告必须保留音频风险并等待生成后验收。
12. 远端 `create_generation_task.params.prompt` 必须包含主体名、`reference_index` 与图片 token/编号/URL 绑定；若只出现裸 `{{Image N}}`、裸 `图片N` 或裸 URL 序列，状态必须记录为 `subject_reference_name_stripped`。
13. 有主体参照图时，提交前 `images[]` / `mixedList` 必须小于等于 9；超过上限必须先取舍并记录，不得提交超限任务。
14. `duration` 必须等于 submit plan 中的 `duration_hint`，且 `duration_hint=clamp(duration_estimate_seconds, 4, 15)`；小于等于 4 秒用 4 秒，大于等于 15 秒用 15 秒。
15. 本地 prompt、远端 `libtv-submission.txt`、manifest 和 submit plan 必须通过引用一致性检查：draft 相位允许 prompt YAML 未绑定但不得创建最终远端提交；final 相位已绑定主体不得出现在缺图清单，YAML 按 `reference_index` 排序后的 `uploaded_url`、`mixedList` URL 和 `images[]` URL 必须逐项顺序一致，未声明共享关系时不得重复 URL，uploaded URL 的 LibTV project scope 必须与 submit plan `projectUuid` 一致。
16. 远端 `libtv-submission.txt` 不得包含缺图/无可复用 URL/未入预算主体列表；`生成时保持` 连续性句只能出现一次，必须并入 `【直接生成请求】` 或首段生成请求、位于 `【分镜组源文本】` 前，且不得单独列 `参照连续性总领` 标题。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `prompt.md` 是否采用 source-first YAML，直接保留 `5-分组` 对应 `## x-y-z` 的标题、正文和 fenced YAML，而非另写二次说明段？ | `G2-CONTENT` | `FAIL-VIDSUBJ-PROMPT` | `N4-PROMPT` | `prompt.md` 源文片段、`source_file` / `group_id` 回指 |
| draft 相位是否只保留原 YAML，未伪造空 `reference_index`、空 `uploaded_url`、占位 URL 或最终远端提交？ | `G16-REF-PROMPT-INTEGRITY` | `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` | `N4-PROMPT` / `N6-REVIEW` | `slot_binding_phase=draft`、draft YAML 扫描结果、无 `libtv-submission.txt` final 证据 |
| final 相位是否只在原 fenced YAML 的已绑定主体项中注入 `reference_index`、真实 `uploaded_url` 和可选 `portrait_token`？ | `G16-REF-PROMPT-INTEGRITY` | `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` | `N8-DISPATCH` | final YAML、`generation_slots`、`asset_uploads` 对照 |
| `reference_index` 是否来自最终 `generation_slots` 或 UI 图N槽位，而不是 YAML 文本顺序、OSS 上传顺序或旧 mixedList 回显？ | `G19-REMOTE-REFERENCE-ORDER` | `FAIL-VIDSUBJ-REFERENCE-SLOT-REGISTRY` / `FAIL-VIDSUBJ-REMOTE-REFERENCE-ORDER` | `N8-DISPATCH` | `generation_slot_source`、UI / post-submit mixedList 证据、回刷记录 |
| 默认提交是否保持 `strict_original + transport_only`，且未在用户 opt-in 前授权 LibTV 优化、摘要、重排或改写表达？ | `G2-CONTENT` / `G14-POST-SUBMIT` | `FAIL-VIDSUBJ-PROMPT` / `FAIL-VIDSUBJ-LIBTV-STALL` | `N4-PROMPT` / `N8-DISPATCH` | submit plan 的 `prompt_fidelity_mode`、`allow_libtv_prompt_optimization`、query 优化漂移检查 |
| `*-libtv-submission.txt` 是否以 `【LibTV 调用锁定】` 开头，并在源文本前声明 no-ask、严格原文、硬锁定事实和 provider 参数？ | `G7-PROVIDER-ROUTE` / `G14-POST-SUBMIT` | `FAIL-VIDSUBJ-LIBTV` / `FAIL-VIDSUBJ-LIBTV-STALL` | `N8-DISPATCH` | `libtv-submission.txt` 首段、no-ask 扫描、provider 参数区 |
| 有主体图时 `modeType=mixed2video` 和严格 JSON `mixedList` 是否存在；无图时是否是 `modeType=text2video`，且没有空图片槽？ | `G7-PROVIDER-ROUTE` | `FAIL-VIDSUBJ-LIBTV` | `N8-DISPATCH` | `libtv-submit-plan.json.command`、`mixedList`、无图 text2video 记录 |
| `mixedList`、submit plan `images[]` 和 YAML `reference_index / uploaded_url` 是否逐项同槽一致，且单组不超过 9 张？ | `G6-REFERENCE-BUDGET` / `G16-REF-PROMPT-INTEGRITY` | `FAIL-VIDSUBJ-REF-BUDGET` / `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` | `N5-REF-BIND` / `N8-DISPATCH` | 引用一致性 gate、`images[]` 数量、`excluded_due_to_budget` |
| 远端提交是否没有本地路径、`@projects/...`、人工 `参照图N` 编号、裸图片 token 序列或裸 URL 列表？ | `G5-LOCAL-ASSET-EVIDENCE` / `G9-REMOTE-NUMBERING` | `FAIL-VIDSUBJ-PROMPT` | `N4-PROMPT` / `N8-DISPATCH` | `libtv-submission.txt` 禁词扫描、远端 prompt token 邻近绑定检查 |
| 缺图、无可复用 URL、未入预算或被取舍主体是否只写入 manifest / submit plan / report，没有污染远端 `libtv-submission.txt`？ | `G16-REF-PROMPT-INTEGRITY` | `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` | `N4-PROMPT` / `N5-REF-BIND` | 远端提交缺图列表扫描、manifest `missing / excluded` |
| `duration` 是否等于 submit plan 的 `duration_hint`，且由 `duration_estimate_seconds` clamp 到 4-15 秒，不固定 15 秒？ | `G8-DURATION` | `FAIL-VIDSUBJ-DURATION` | `N3-GROUP-INDEX` / `N8-DISPATCH` | `duration_source`、`duration_estimate_seconds`、`duration_hint`、远端提交时长 |
| 远端提交是否请求 `enableSound:on`，并在不可生成前验证时只记录非阻断音频风险？ | `G17-AUDIO-PREFLIGHT` | `WARN-VIDSUBJ-AUDIO-PREFLIGHT-UNVERIFIED` | `N8-DISPATCH` / `N9-QUEUE` | submit plan / queue / report 中的 `audio_preflight_unverified_non_blocking` |
| 远端 query 是否未出现未授权优化、`ask_user` 等待态、明确 tool error、主体名绑定丢失或只有裸图片 token；出现时是否未被标为正常 pending？ | `G14-POST-SUBMIT` / `G19-REMOTE-REFERENCE-ORDER` | `FAIL-VIDSUBJ-LIBTV-STALL` / `FAIL-VIDSUBJ-PROMPT-REFERENCE-BINDING` | `N9-QUEUE` / `N8-DISPATCH` | query 摘要、stall gate、post-submit reference-order gate、`libtv-results.json.attempts[]` |
| `生成时保持` 连续性句是否最多出现一次，并入 `【直接生成请求】` 或首段请求，且位于 `【分镜组源文本】` 前？ | `G16-REF-PROMPT-INTEGRITY` | `FAIL-VIDSUBJ-REF-PROMPT-INTEGRITY` | `N4-PROMPT` | `libtv-submission.txt` 连续性句计数和段落位置 |
| `分镜组源文本` 是否被明确声明为连续视频约束，而不是图片生产清单，防止远端改路由为分镜图流程？ | `G7-PROVIDER-ROUTE` / `G14-POST-SUBMIT` | `FAIL-VIDSUBJ-LIBTV` / `FAIL-VIDSUBJ-LIBTV-STALL` | `N8-DISPATCH` | 固定 opening 文本、query 中 route drift / generation node 检查 |

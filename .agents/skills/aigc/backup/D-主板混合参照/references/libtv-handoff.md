# LibTV Handoff

本文件定义 `D-主板混合参照` 与 `.agents/skills/cli/libTV` 的交接规则。D 叶子负责把故事板总参照和主体参照绑定到同一组级任务；`$libTV` 负责上传、会话、查询和下载。

## Official Skill Dependency

- 视频生成必须调用 `.agents/skills/cli/libTV` 官方技能包完成；不得绕过其 `scripts/` 直接拼接私有 OpenAPI。
- 提交前加载 `.agents/skills/cli/libTV/SKILL.md`，并确认 `LIBTV_ACCESS_KEY` 已在当前命令环境中可用。
- 新建主板混合参照视频任务时必须先运行 `python3 .agents/skills/cli/libTV/scripts/change_project.py`，或由用户显式指定一个可继续使用的 existing `projectUuid/projectUrl`；把锁定后的 `projectUuid/projectUrl` 写入 submit plan、queue 和 report。

## Official Script Order

有故事板或主体参照图时固定顺序：

1. `change_project.py`：新建任务时必须先执行，或由用户显式指定 existing `projectUuid/projectUrl` 作为继续使用的画布锁。
2. `upload_file.py <path>`：在上述 `projectUuid` 已锁定后，上传故事板总参照和主体参照，保存返回的 OSS URL。每个 uploaded URL 的 `/claw/<projectUuid>/` 必须与 submit plan 中锁定的 `projectUuid` 一致。上传返回只建立 `asset_uploads: reference_identity -> uploaded_url` 身份映射，不承载图N顺序真源；最终图N顺序必须由视频生成 `mixedList` 形成的 `generation_slots` 决定。
3. `create_session.py "$(cat <prompt>)"`：提交远端 `*-libtv-submission.txt`，返回 `sessionId/projectUuid/projectUrl`。
4. `query_session.py <sessionId> --project-id <projectUuid>`：按官方 `$libTV` 轮询策略查询画布消息和生成结果。
5. `download_results.py <sessionId> --output-dir <episode_output_dir> --filename <group_id>.mp4`：生成完成后自动下载到本技能的集目录，并使用精确文件名避免生成 `<group_id>_01.mp4`。

无参照图时跳过 `upload_file.py`，其余顺序不变。

## Canvas Sync

- 每个任务必须同步到 LibTV 画布：远端消息、上传参照、生成节点和结果都应保留在同一 `projectUrl`。
- 有故事板或主体参照图时，上传 URL 的 `claw` project scope、submit plan `projectUuid`、queue `projectUuid` 和 `create_session.py` 返回的 `projectUuid` 必须一致；不一致时状态写成 `reference_project_scope_mismatch`，不得提交或继续等待。
- queue/result/report 必须记录 `sessionId`、`projectUuid`、`projectUrl`，用于用户在画布查看。
- 若画布未出现对应生成节点或结果 URL，不得把本地状态标为 downloaded / generated。

## Prompt Fidelity And Optimization Authorization

- 默认远端 handoff 必须采用 `strict_original + transport_only`：`prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false`，并禁止提示词优化、重新编排、摘要、改写和补镜头。
- `strict_original` 表示 `【分镜组源文本】` 中的原始分镜组正文、final fenced YAML 的 `故事板参照.reference_index / uploaded_url / image_token` 和主体列表项 `reference_index / uploaded_url / image_token` 绑定关系必须共同作为 Seedance `create_generation_task.params.prompt` 的完整主体；LibTV 远端 Agent 不得在工具调用前自行生成优化版提示词、镜头计划或摘要版分镜。
- `transport_only` 只允许上传 URL、`mixedList`、时长、比例、分辨率、声音等技术投影；不得改变分镜内容、镜头顺序、角色动作、对白、音效或氛围事实。
- 时长投影必须使用当前分镜组的 `duration_hint`，不得固定写 15 秒；`duration_hint=clamp(duration_estimate_seconds, 4, 15)`。
- 只有 submit plan 明确记录用户 opt-in `prompt_fidelity_mode=libtv_optimize` 或 `allow_libtv_prompt_optimization=true` 时，才允许 LibTV 做提示词优化、压缩、合并镜头或工作流规划。
- 若远端 query 显示 assistant 在 `create_generation_task` 之前执行“优化提示词 / 重新编排 / 摘要 / 镜头计划”且本地未 opt-in，必须判定为 `prompt_fidelity_violation / libtv_optimize_without_opt_in`；不得把该 session 标为正常 pending。

## Pre-Generation Audio Control Gate

- D 路线默认要求有声视频；远端提交文本必须声明 `enableSound: on`。
- 当前 `.agents/skills/cli/libTV/scripts/create_session.py` 只向 Agent-IM 发送消息，本地 CLI 本身没有独立 `--enable-sound` 开关。若不能在生成前验证 `create_generation_task.params.enableSound`，记录为 `audio_preflight_unverified_non_blocking`，但不得因此阻断提交。
- 可接受的生成前强证据：请求体或预执行工具调用中 `create_generation_task.params.enableSound` 明确为 `on` / `true` / 布尔真值。
- 生成前缺少强证据时，必须保留后验音频门：生成后必须通过 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 检出 audio stream；否则状态写成 `audio_missing / no_audio_stream`，不得交付。

## Command Selection

| reference state | command | rule |
| --- | --- | --- |
| `reference_images` 非空 | `libtv_session_with_uploaded_references` | 先确认 `mixedList` <= 9，逐个上传故事板图和主体图，再把 URL 按故事板身份和主体名写入 prompt，不预设 `参照图N` |
| `reference_images` 为空 | `libtv_session_text_only` | 无参照图时只发送完整组级 prompt |
| `$libTV` 脚本或凭据不可用 | blocked | 写入 `blocked`，不得伪造 `sessionId` |

## Defaults

- `requested_model`: 默认为空，表示使用 LibTV 后端默认视频路由。用户显式指定模型时，原样写入自然语言任务。
- `duration_estimate_seconds`: 默认从 `4-分组` 组底 YAML 的 `时长估算` 读取；缺失时按组内分镜秒数求和，区间取上限，仍无法确定才回退 15 秒并记录原因。
- `duration_hint`: 必须写入远端提交；按 `clamp(duration_estimate_seconds, 4, 15)` 计算，小于等于 4 秒用 4 秒，4 到 15 秒之间用估算值，大于等于 15 秒用 15 秒。
- `ratio_hint`: 默认 `16:9`，必须写入远端提交。
- `video_resolution_hint`: 默认 `720p`，即用户可见规格 720P，必须写入远端提交。
- `enableSound`: 默认 `on`，必须写入远端提交文本；若生成前无法验证真实 `create_generation_task.params.enableSound`，记录 `audio_preflight_unverified_non_blocking`，继续提交并以后验音频门验收。
- `poll_seconds`: 默认 `45`。
- 图片路径必须存在；空数组不传参照。

## Remote Handoff Contract

本地 `prompt.md` 必须采用 source-first YAML 两阶段处理：draft 直接保留 `4-分组` 中对应分镜组原文和原始 fenced YAML，不提前写死 `reference_index / uploaded_url`；final 只按最终 `generation_slots` 在 fenced YAML 内注入 `故事板参照.reference_index / uploaded_url / image_token` 和主体列表项 `reference_index / uploaded_url / image_token`。发送给 LibTV 画布的 `*-libtv-submission.txt` 是运输层包裹文本，必须复用 final source-first YAML 作为 `【分镜组源文本】`，并满足：

- 文件第一行必须是 `【LibTV 调用锁定】`。
- 第一段必须使用 `hybrid-prompt-assembly-contract.md#LibTV Remote Opening` 中的 D 专属调用锁，明确 `provider=seedance2.0`、`taskType=video`、有图时 `modeType=mixed2video` 和 `mixedList`，无图时 `modeType=text2video`。
- 源层规则：`asset_uploads` 只证明“故事板总参照或某个主体名对应哪个 OSS URL”；`generation_slots` 才证明“图N/mixedList[n-1] 对应哪个 OSS URL 和故事板/主体身份”。若视频生成框 UI 缩略图顺序可观测，以 UI 图N / `Image N` 为最终槽位真源；只有 UI 槽位不可观测时才用远端 query 的实际 `mixedList[n].url` 反查 `asset_uploads`。回刷 fenced YAML 的 `reference_index=N`、真实 `uploaded_url` 和可选 `image_token` 后重提。
- 远端提交不得包含 `@projects/...`、`/Volumes/...`、`projects/aigc/.../5-设计/...`、`projects/aigc/.../6-图像/...` 等本地图片路径；只允许通过 final `【分镜组源文本】` fenced YAML 的 `故事板参照.reference_index / uploaded_url / image_token` 和主体列表项 `reference_index / uploaded_url / image_token` 表达混合参照绑定，不得另起 `【混合参照说明】`，也不得预设 `参照图1/2/N` 人工编号。
- 缺故事板、缺主体图、无缓存 URL、未进入预算或被预算排除的主体不得写入远端提交，只能写入 manifest / submit plan / report；不得出现“无独立参照图 / 无缓存 URL / 未进入预算主体 / 不创建空图片槽”等说明行。
- `【直接生成请求】` 必须写成“基于下方【分镜组源文本】”，并明确该源文本的 fenced YAML 已包含故事板与主体 `reference_index / uploaded_url / image_token` 绑定；不得只写“基于上述参照图 URL”。
- 远端 `create_generation_task.params.prompt` 必须保留故事板身份、主体名与图片 token/编号/URL 绑定；提交文本不得人工生成 `故事板总参照 参照图1`、`林寂 参照图2` 这类编号，只有当 LibTV 自动插入真实图片编号后，才把故事板身份或主体名邻近该真实编号，例如 `林寂 {{Image 2}}`。不得把参照区压成 `{{Image 1}} {{Image 2}} ...`、`图片1 图片2 ...` 或裸 URL 列表。
- 故事板和主体 uploaded URL 必须能回指当前 fresh resolve 的本地源图及其指纹；源图缺失、指纹缺失或缓存指纹不匹配时，不得进入远端提交。
- 默认提交文本必须声明 `strict_original + transport_only`，且 `allow_libtv_prompt_optimization=false`；未显式 opt-in 时不得要求或默许 LibTV 重新组织、压缩、合并或摘要分镜组源文本。
- 不得把 D 任务拆成 B 路线和 C 路线分别提交；故事板总参照和主体参照必须在同一个 `mixed2video` 任务中生效。

## Mixed Reference Prompt Rule

发送给 LibTV 的消息必须清楚区分两类参照：

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

【直接生成请求】
请基于下方【分镜组源文本】，按 `mixed2video + mixedList` 生成一条连续视频。【分镜组源文本】保留了原始分镜组正文，且其 fenced YAML 中的 `故事板参照.reference_index / uploaded_url / image_token` 和主体列表项 `reference_index / uploaded_url / image_token` 已绑定对应故事板总参照与主体参照图；请把原始正文和 YAML 槽位绑定关系共同作为生成 prompt 完整体。生成时参考故事板总参照作为整体构图、镜头顺序、画面连续性和节奏参考，不作为唯一首帧；每个主体 uploaded_url 仅用于对应主体外观一致性，不改写剧情事实。不要自行写“参照图1/2/N”编号；如系统自动插入真实图片 token 或编号，必须把故事板身份或主体名放在对应 token/编号旁边。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把混合参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<直接粘贴 final source-first YAML 分镜组全文；若有参照图，fenced YAML 内包含 故事板参照和主体项的 reference_index / uploaded_url / image_token>
```

## Submit Plan Requirements

`第N集-libtv-submit-plan.json` 每个 task 至少记录：

- `queue_id`
- `group_id`
- `command`
- `prompt_path`
- `storyboard_reference.path`
- `storyboard_reference.uploaded_url`
- `subject_references[].path`
- `subject_references[].uploaded_url`
- `asset_uploads[]`
- `generation_slots[]`
- `reference_image_budget.max_images`
- `reference_image_budget.excluded_due_to_budget`
- `download_dir`
- `expected_output`
- `sessionId`
- `projectUuid`
- `projectUrl`
- `prompt_fidelity_mode`
- `allow_libtv_prompt_optimization`
- `transport_only_projection`
- `duration_source`
- `duration_estimate_seconds`
- `duration_hint`
- `next_action`

## Queue Ledger

| queue_id | group_id | command | sessionId | projectUuid | local_status | remote_status | reference_count | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Query And Download

- 查询使用 `python3 .agents/skills/cli/libTV/scripts/query_session.py <sessionId> --project-id <projectUuid>`。
- 按官方 `$libTV` 轮询策略查询完成后必须自动下载；下载使用 `python3 .agents/skills/cli/libTV/scripts/download_results.py <sessionId> --output-dir <episode_output_dir> --filename <group_id>.mp4`。
- 下载后必须执行音轨探测，例如 `ffprobe -v error -select_streams a -show_entries stream=index,codec_type,codec_name -of json <video>`；没有 audio stream 时状态必须写成 `audio_missing / no_audio_stream`，不得交付。若 LibTV query 中 `task_result.audios` 为空且尚未通过下载后音轨检查，不能把视频 URL 当作成功。
- 下载目录固定为：

```text
projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/
```
- 短轮询超时必须保留 `sessionId` 并用 `query_session.py` 后续查询。

## Gate

1. 提交前有 `LIBTV_ACCESS_KEY` 自检策略或实际结果。
2. 所有本地参照路径可读；上传失败必须进入 blocked 或 submit_failed。
3. prompt 使用 draft/final source-first YAML 保留完整组正文，并在 final fenced YAML 内按生成槽位绑定故事板总参照和主体 `reference_index / uploaded_url / image_token`；远端 `*-libtv-submission.txt` 首段为 `【LibTV 调用锁定】` 和正确 `modeType`。
4. 队列能用 `sessionId` 续查。
5. 有任一故事板或主体参照图时，远端调用必须为 `modeType=mixed2video` 且使用 `mixedList`，`mixedList` 不超过 9 张；不得退回 `singleImage2video`、`image2video` 或 B/C 分开提交。
6. 远端工具 prompt 保留故事板身份、主体名与图片 token/编号/URL 绑定，提交文本未预设 `参照图N` 人工编号，不存在裸图片 token 序列，也不存在单独 `【混合参照说明】` 作为第二真源。
7. 默认提交 prompt 已声明 `strict_original + transport_only`，且 submit plan 中 `allow_libtv_prompt_optimization=false`。
8. 未显式 opt-in `libtv_optimize` 时，远端 query 不得出现优化版提示词、重新编排脚本、镜头计划或摘要版分镜。
9. `duration_hint` 必须等于 `clamp(duration_estimate_seconds, 4, 15)`，远端 `duration` 与 submit plan 一致。
10. 生成前 `create_generation_task.params.enableSound` 若可验证则必须为开启；若当前 CLI 路径不可验证，记录 `audio_preflight_unverified_non_blocking` 并继续提交，但生成后必须有 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 证明视频含 audio stream。
11. 生成后必须有 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 证明视频含音频 stream；否则不得 pass。
12. 远端提交不得包含缺图/无缓存/未入预算/不创建空图片槽说明；所有未进入 `mixedList` 的故事板或主体只写入本地 manifest / submit plan / report。
13. 故事板和主体 uploaded URL 必须有当前本地源图指纹匹配证据；历史缓存 URL 无指纹或指纹不匹配时不得进入 `mixedList`。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 视频生成是否明确加载并调用 `.agents/skills/cli/libTV` 官方技能包，没有绕过其 `SKILL.md` 和 `scripts/` 直接拼接私有 OpenAPI？ | `GATE-VIDHYB-LIBTV-01` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `references/libtv-handoff.md#Official-Skill-Dependency` | libTV SKILL load note、command plan、no private API route evidence |
| 提交前是否完成 `LIBTV_ACCESS_KEY` 可用性检查；凭据或脚本不可用时是否写入 `blocked`，没有伪造 `sessionId` 或远端状态？ | `GATE-VIDHYB-LIBTV-01` | `FAIL-VIDHYB-LIBTV` | `N8-SUBMIT-OR-SKIP` / `references/libtv-handoff.md#Command-Selection` | credential check result、blocked reason、queue local_status |
| 新建任务是否先通过 `change_project.py` 锁定 `projectUuid/projectUrl`，或只在用户显式指定时沿用 existing 画布，并把锁写入 submit plan、queue 和 report？ | `GATE-VIDHYB-LIBTV-01` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `N8-SUBMIT-OR-SKIP` | project lock command、projectUuid/projectUrl fields、user existing-canvas evidence |
| 有参照图时官方脚本顺序是否严格为 project lock -> `upload_file.py` -> `create_session.py` -> `query_session.py` -> `download_results.py`，无图时才跳过 upload？ | `GATE-VIDHYB-LIBTV-02` | `FAIL-VIDHYB-LIBTV` | `N8-SUBMIT-OR-SKIP` / `N9-QUERY-DOWNLOAD` | command log、per-task queue events、upload skip reason for text-only |
| 每个 uploaded URL 的 `/claw/<projectUuid>/` scope 是否与 submit plan、queue 和 create_session 返回的 `projectUuid` 一致，不一致时是否阻断或写 `reference_project_scope_mismatch`？ | `GATE-VIDHYB-LIBTV-02` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `N8-SUBMIT-OR-SKIP` | uploaded URL scope audit、projectUuid comparison、blocked status |
| 上传返回是否只写入 `asset_uploads: reference_identity -> uploaded_url`，最终 `reference_index` 是否来自 UI 图N或实际 `mixedList` 的 `generation_slots`，而不是上传顺序？ | `GATE-VIDHYB-SLOT-01` | `FAIL-VIDHYB-UPLOAD-SLOT-CONFLATION` | `N6-PLAN-BUILD` / `references/libtv-handoff.md#Official-Script-Order` | asset_uploads ledger、generation_slots ledger、upload order comparison |
| 远端消息、上传参照、生成节点和结果是否都保留在同一 `projectUrl`；画布没有对应生成节点或结果 URL 时是否没有标为 generated/downloaded？ | `GATE-VIDHYB-LIBTV-03` | `FAIL-VIDHYB-LIBTV` | `N9-QUERY-DOWNLOAD` / `N10-CLOSEOUT` | canvas message evidence、result URL、queue remote_status |
| 远端 handoff 是否第一行就是 `【LibTV 调用锁定】`，并按有图 `mixed2video + mixedList`、无图 `text2video` 锁定 provider/taskType/modeType？ | `GATE-VIDHYB-REMOTE-01` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `references/libtv-handoff.md#Remote-Handoff-Contract` | submission header、modeType、mixedList or text2video evidence |
| 单组 `mixedList` 是否不超过 9 张，且故事板总参照与主体参照共同计入预算；超限处理是否已经在 submit plan 中明示？ | `GATE-VIDHYB-BUDGET-01` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `references/hybrid-reference-binding.md#LibTV-Image-Budget` | mixedList count、reference_image_budget、excluded_due_to_budget |
| 远端提交是否没有本地路径、`@projects/...`、`/Volumes/...`、人工 `参照图1/2/N`、缺图/无缓存/未入预算说明、裸图片 token 或裸 URL 列表？ | `GATE-VIDHYB-REMOTE-02` | `FAIL-VIDHYB-REF-PROMPT-INTEGRITY` | `N5-PROMPT-ASSEMBLE` / `N6-PLAN-BUILD` | submission text scan、本地路径 scan、forbidden phrase scan |
| `【直接生成请求】` 是否明确基于下方 final `【分镜组源文本】`，并要求故事板身份、主体名与 `reference_index / uploaded_url / image_token` 共同作为 prompt 完整体？ | `GATE-VIDHYB-REMOTE-02` | `FAIL-VIDHYB-REF-PROMPT-INTEGRITY` | `N5-PROMPT-ASSEMBLE` / `N6-PLAN-BUILD` | direct request snapshot、final source-first YAML、token/name adjacency evidence |
| 默认提交是否声明 `prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false` 与 `transport_only_projection: true`，且未 opt-in 时 query 不出现优化、摘要、重排或镜头计划？ | `GATE-VIDHYB-FIDELITY-01` | `FAIL-VIDHYB-PROMPT` | `N5-PROMPT-ASSEMBLE` / `N7-REVIEW-GATE` | submit plan fidelity fields、submission constraints、query prompt comparison |
| `duration` 是否来自当前组 `duration_hint=clamp(duration_estimate_seconds, 4, 15)`，没有固定写 15 秒或跨组复用时长？ | `GATE-VIDHYB-DURATION-01` | `FAIL-VIDHYB-DURATION` | `N2-GROUP-EXTRACT` / `N6-PLAN-BUILD` | duration_source、duration_estimate_seconds、duration_hint、submission duration |
| 远端提交文本是否声明 `enableSound: on`；如果当前 CLI 无法在生成前验证 `create_generation_task.params.enableSound`，是否只记录 `audio_preflight_unverified_non_blocking`？ | `GATE-VIDHYB-AUDIO-01` | `FAIL-VIDHYB-AUDIO-PREFLIGHT` | `N6-PLAN-BUILD` / `N7-REVIEW-GATE` | submission enableSound field、preflight verification or non-blocking note |
| 生成后是否通过 `task_result.audios`、音频 URL 或下载后 `ffprobe` 证明视频有音频；缺音频是否写为 `audio_missing / no_audio_stream` 而不是 pass？ | `GATE-VIDHYB-AUDIO-02` | `FAIL-VIDHYB-AUDIO-MISSING` | `N9-QUERY-DOWNLOAD` / `N10-CLOSEOUT` | query audio evidence、audio URL、ffprobe output、verdict |
| 故事板和主体 uploaded URL 是否都能回指当前 fresh resolve 的本地源图和指纹；源图缺失、指纹缺失或缓存指纹不匹配时是否没有进入 `mixedList`？ | `GATE-VIDHYB-REF-03` | `FAIL-VIDHYB-STALE-REFERENCE-ASSET` | `N3-STORYBOARD-BIND` / `N4-SUBJECT-BIND` / `N6-PLAN-BUILD` | source fingerprint record、cache match verdict、mixedList URL trace |
| submit plan 是否完整记录 `asset_uploads[]`、`generation_slots[]`、`reference_image_budget`、prompt fidelity、duration、project、download 与 `next_action` 等 handoff 必填字段？ | `GATE-VIDHYB-LIBTV-03` | `FAIL-VIDHYB-LIBTV` | `N6-PLAN-BUILD` / `references/libtv-handoff.md#Submit-Plan-Requirements` | submit plan field coverage、missing field findings |
| queue ledger 是否至少记录 `queue_id / group_id / command / sessionId / projectUuid / local_status / remote_status / reference_count / next_action`，并能支持后续 query/download？ | `GATE-VIDHYB-LIBTV-03` | `FAIL-VIDHYB-LIBTV` | `N8-SUBMIT-OR-SKIP` / `N9-QUERY-DOWNLOAD` | queue ledger row、sessionId/projectUuid、next_action |
| 查询和下载是否使用官方 `query_session.py <sessionId> --project-id <projectUuid>` 与 `download_results.py ... --filename <group_id>.mp4`，输出固定在本技能集目录而不是默认 `videos/` 子目录？ | `GATE-VIDHYB-LIBTV-03` | `FAIL-VIDHYB-LIBTV` | `N9-QUERY-DOWNLOAD` / `references/libtv-handoff.md#Query-And-Download` | query command、download command、output path、exact filename |
| 交付报告是否记录 submitted/queued/downloaded/skipped/failed、sessionId 或 blocked reason、音频验收、缺图/预算排除与可执行返工入口？ | `GATE-VIDHYB-REPORT-01` | `FAIL-VIDHYB-REPORT` | `N10-CLOSEOUT` / `templates/output-template.md` | execution report、review findings、queue ledger、rework targets |

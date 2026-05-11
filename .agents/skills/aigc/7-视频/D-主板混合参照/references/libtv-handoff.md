# LibTV Handoff

本文件定义 `D-主板混合参照` 与 `.agents/skills/cli/libTV` 的交接规则。D 叶子负责把故事板总参照和主体参照绑定到同一组级任务；`$libTV` 负责上传、会话、查询和下载。

## Official Skill Dependency

- 视频生成必须调用 `.agents/skills/cli/libTV` 官方技能包完成；不得绕过其 `scripts/` 直接拼接私有 OpenAPI。
- 提交前加载 `.agents/skills/cli/libTV/SKILL.md`，并确认 `LIBTV_ACCESS_KEY` 已在当前命令环境中可用。
- 如需新画布隔离当前分镜组，先运行 `python3 .agents/skills/cli/libTV/scripts/change_project.py`，并把返回的 `projectUuid/projectUrl` 写入 submit plan、queue 和 report。

## Official Script Order

有故事板或主体参照图时固定顺序：

1. `change_project.py`：仅在需要干净画布或用户要求隔离时执行。
2. `upload_file.py <path>`：逐图上传故事板总参照和主体参照，保存返回的 OSS URL。
3. `create_session.py "$(cat <prompt>)"`：提交远端 `*-libtv-submission.txt`，返回 `sessionId/projectUuid/projectUrl`。
4. `query_session.py <sessionId> --project-id <projectUuid>`：按官方 `$libTV` 轮询策略查询画布消息和生成结果。
5. `download_results.py <sessionId> --output-dir <episode_output_dir> --prefix <group_id>`：生成完成后自动下载到本技能的集目录。

无参照图时跳过 `upload_file.py`，其余顺序不变。

## Canvas Sync

- 每个任务必须同步到 LibTV 画布：远端消息、上传参照、生成节点和结果都应保留在同一 `projectUrl`。
- queue/result/report 必须记录 `sessionId`、`projectUuid`、`projectUrl`，用于用户在画布查看。
- 若画布未出现对应生成节点或结果 URL，不得把本地状态标为 downloaded / generated。

## Prompt Fidelity And Optimization Authorization

- 默认远端 handoff 必须采用 `strict_original + transport_only`：`prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false`，并禁止提示词优化、重新编排、摘要、改写和补镜头。
- `strict_original` 表示 `【分镜组源文本】` 中的原始分镜组正文、fenced YAML 的 `故事板参照.uploaded_url` 和主体列表项 `uploaded_url` 绑定关系必须共同作为 Seedance `create_generation_task.params.prompt` 的完整主体；LibTV 远端 Agent 不得在工具调用前自行生成优化版提示词、镜头计划或摘要版分镜。
- `transport_only` 只允许上传 URL、`mixedList`、时长、比例、分辨率、声音等技术投影；不得改变分镜内容、镜头顺序、角色动作、对白、音效或氛围事实。
- 时长投影必须使用当前分镜组的 `duration_hint`，不得固定写 15 秒；`duration_hint=clamp(duration_estimate_seconds, 4, 15)`。
- 只有 submit plan 明确记录用户 opt-in `prompt_fidelity_mode=libtv_optimize` 或 `allow_libtv_prompt_optimization=true` 时，才允许 LibTV 做提示词优化、压缩、合并镜头或工作流规划。
- 若远端 query 显示 assistant 在 `create_generation_task` 之前执行“优化提示词 / 重新编排 / 摘要 / 镜头计划”且本地未 opt-in，必须判定为 `prompt_fidelity_violation / libtv_optimize_without_opt_in`；不得把该 session 标为正常 pending。

## Pre-Generation Audio Control Gate

- D 路线默认要求有声视频；声音开启必须在生成前落到真实生成任务参数，而不是只写进自然语言 prompt。
- 当前 `.agents/skills/cli/libTV/scripts/create_session.py` 只向 Agent-IM 发送消息，本地 CLI 本身没有独立 `--enable-sound` 开关。若不能使用可验证的生成任务接口、远端预执行工具调用草案，或其他能在执行前设置 `create_generation_task.params.enableSound` 的控制面，则该组必须标记 `blocked_audio_control_unverified`，不得作为正式生成提交。
- 可接受的生成前证据：请求体或预执行工具调用中 `create_generation_task.params.enableSound` 明确为 `on` / `true` / 布尔真值。
- 不可接受的证据：`enableSound: on` 只出现在提交文本、prompt 中写“声音开启”、或生成后已经出现视频 URL。

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
- `enableSound`: 默认 `on`，且必须在生成前作为 `create_generation_task.params.enableSound` 可验证地开启；只写入远端提交文本不是充分证据。
- `poll_seconds`: 默认 `45`。
- 图片路径必须存在；空数组不传参照。

## Remote Handoff Contract

本地 `prompt.md` 必须采用 source-first enriched YAML，直接保留 `4-分组` 中对应分镜组原文，并只在 fenced YAML 内注入 `故事板参照.uploaded_url` 和主体列表项 `uploaded_url`。发送给 LibTV 画布的 `*-libtv-submission.txt` 是运输层包裹文本，必须复用同一个 source-first enriched YAML 作为 `【分镜组源文本】`，并满足：

- 文件第一行必须是 `【LibTV 调用锁定】`。
- 第一段必须使用 `hybrid-prompt-assembly-contract.md#LibTV Remote Opening` 中的 D 专属调用锁，明确 `provider=seedance2.0`、`taskType=video`、有图时 `modeType=mixed2video` 和 `mixedList`，无图时 `modeType=text2video`。
- 远端提交不得包含 `@projects/...`、`/Volumes/...`、`projects/aigc/.../5-设计/...`、`projects/aigc/.../6-图像/...` 等本地图片路径；只允许通过 `【分镜组源文本】` fenced YAML 的 `故事板参照.uploaded_url` 和主体列表项 `uploaded_url` 表达混合参照绑定，不得另起 `【混合参照说明】`，也不得预设 `参照图1/2/N` 人工编号。
- 缺故事板、缺主体图、无缓存 URL、未进入预算或被预算排除的主体不得写入远端提交，只能写入 manifest / submit plan / report；不得出现“无独立参照图 / 无缓存 URL / 未进入预算主体 / 不创建空图片槽”等说明行。
- `【直接生成请求】` 必须写成“基于下方【分镜组源文本】”，并明确该源文本的 fenced YAML 已包含故事板与主体 uploaded_url 绑定；不得只写“基于上述参照图 URL”。
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
audio_preflight_required: true
生成前必须确认远端 create_generation_task.params.enableSound 为 on / true；不得只把声音要求写在自然语言 prompt 中。
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
transport_only_projection: true
禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头。
只允许执行 transport_only 投影：上传 URL、mixedList、duration、ratio、resolution、enableSound。

【直接生成请求】
请基于下方【分镜组源文本】，按 `mixed2video + mixedList` 生成一条连续视频。【分镜组源文本】保留了原始分镜组正文，且其 fenced YAML 中的 `故事板参照.uploaded_url` 和主体列表项 `uploaded_url` 已绑定对应故事板总参照与主体参照图；请把原始正文和 YAML uploaded_url 绑定关系共同作为生成 prompt 完整体。生成时参考故事板总参照作为整体构图、镜头顺序、画面连续性和节奏参考，不作为唯一首帧；每个主体 uploaded_url 仅用于对应主体外观一致性，不改写剧情事实。不要自行写“参照图1/2/N”编号；如系统自动插入真实图片 token 或编号，必须把故事板身份或主体名放在对应 token/编号旁边。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把混合参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<直接粘贴 source-first enriched YAML 分镜组全文；若有参照图，fenced YAML 内包含 故事板参照.uploaded_url 和主体 uploaded_url>
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
- 按官方 `$libTV` 轮询策略查询完成后必须自动下载；下载使用 `python3 .agents/skills/cli/libTV/scripts/download_results.py <sessionId> --output-dir <episode_output_dir> --prefix <group_id>`。
- 下载后必须执行音轨探测，例如 `ffprobe -v error -select_streams a -show_entries stream=index,codec_type,codec_name -of json <video>`；没有 audio stream 时状态必须写成 `audio_missing / no_audio_stream`，不得交付。若 LibTV query 中 `task_result.audios` 为空且尚未通过下载后音轨检查，不能把视频 URL 当作成功。
- 下载目录固定为：

```text
projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/
```
- 短轮询超时必须保留 `sessionId` 并用 `query_session.py` 后续查询。

## Gate

1. 提交前有 `LIBTV_ACCESS_KEY` 自检策略或实际结果。
2. 所有本地参照路径可读；上传失败必须进入 blocked 或 submit_failed。
3. prompt 使用 source-first enriched YAML 保留完整组正文，并在 fenced YAML 内绑定故事板总参照和主体 uploaded_url；远端 `*-libtv-submission.txt` 首段为 `【LibTV 调用锁定】` 和正确 `modeType`。
4. 队列能用 `sessionId` 续查。
5. 有任一故事板或主体参照图时，远端调用必须为 `modeType=mixed2video` 且使用 `mixedList`，`mixedList` 不超过 9 张；不得退回 `singleImage2video`、`image2video` 或 B/C 分开提交。
6. 远端工具 prompt 保留故事板身份、主体名与图片 token/编号/URL 绑定，提交文本未预设 `参照图N` 人工编号，不存在裸图片 token 序列，也不存在单独 `【混合参照说明】` 作为第二真源。
7. 默认提交 prompt 已声明 `strict_original + transport_only`，且 submit plan 中 `allow_libtv_prompt_optimization=false`。
8. 未显式 opt-in `libtv_optimize` 时，远端 query 不得出现优化版提示词、重新编排脚本、镜头计划或摘要版分镜。
9. `duration_hint` 必须等于 `clamp(duration_estimate_seconds, 4, 15)`，远端 `duration` 与 submit plan 一致。
10. 生成前 `create_generation_task.params.enableSound` 必须可验证为开启；只存在于自然语言提交文本时阻断为 `blocked_audio_control_unverified / audio_preflight_missing_or_unsupported`。
11. 生成后必须有 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 证明视频含音频 stream；否则不得 pass。
12. 远端提交不得包含缺图/无缓存/未入预算/不创建空图片槽说明；所有未进入 `mixedList` 的故事板或主体只写入本地 manifest / submit plan / report。
13. 故事板和主体 uploaded URL 必须有当前本地源图指纹匹配证据；历史缓存 URL 无指纹或指纹不匹配时不得进入 `mixedList`。

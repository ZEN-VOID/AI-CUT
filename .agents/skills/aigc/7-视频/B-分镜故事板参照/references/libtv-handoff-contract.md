# LibTV Handoff Contract

本文件定义 step3：把完整分镜组内容和可选故事板参照图，交给 `.agents/skills/cli/libTV` 作为唯一视频生成运输中心。B 叶子负责故事板参照绑定和 prompt 保真；`$libTV` 负责上传、建会话、轮询和下载。

## Required LibTV Preflight

每次执行生成前必须：

1. 加载 `.agents/skills/cli/libTV/SKILL.md`。
2. 调用 `.agents/skills/cli/libTV` 官方技能包完成视频生成，不得绕过其 `scripts/` 直接拼接私有 OpenAPI。
3. 确认当前命令环境有 `LIBTV_ACCESS_KEY`；不得把 key 写入文件、模板、queue 或报告。
4. 如需新画布隔离当前分镜组，先运行 `python3 .agents/skills/cli/libTV/scripts/change_project.py`，并把返回的 `projectUuid/projectUrl` 写入 submit plan、queue 和 report。
5. 创建或打开本集 queue ledger：`第N集-libtv-queue.md`。
6. 如果存在故事板图，运行 `python3 .agents/skills/cli/libTV/scripts/upload_file.py <storyboard_path>`，把返回的 OSS URL 写入 submit plan。

## Official Script Order

有故事板图时固定顺序：

1. `change_project.py`：仅在需要干净画布或用户要求隔离时执行。
2. `upload_file.py <storyboard_path>`：上传故事板总参照图。
3. `create_session.py "$(cat <prompt>)"`：提交远端 `*-libtv-submission.txt`，返回 `sessionId/projectUuid/projectUrl`。
4. `query_session.py <sessionId> --project-id <projectUuid>`：按官方 `$libTV` 轮询策略查询画布消息和生成结果。
5. `download_results.py <sessionId> --output-dir <episode_output_dir> --prefix <group_id>`：生成完成后自动下载到本技能的集目录。

无故事板图时跳过 `upload_file.py`，其余顺序不变。

## Canvas Sync

- 每个任务必须同步到 LibTV 画布：远端消息、故事板参照、生成节点和结果都应保留在同一 `projectUrl`。
- queue/result/report 必须记录 `sessionId`、`projectUuid`、`projectUrl`，用于用户在画布查看。
- 若画布未出现对应生成节点或结果 URL，不得把本地状态标为 downloaded / generated。

## Prompt Fidelity And Optimization Authorization

- 默认远端 handoff 必须采用 `strict_original + transport_only`：`prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false`，并禁止提示词优化、重新编排、摘要、改写和补镜头。
- `strict_original` 表示 `【分镜组源文本】` 中的原始分镜组正文和 fenced YAML 里的 `故事板参照.uploaded_url` 绑定关系必须共同作为 Seedance `create_generation_task.params.prompt` 的完整主体；LibTV 远端 Agent 不得在工具调用前自行生成优化版提示词、镜头计划或摘要版分镜。
- `transport_only` 只允许上传 URL、`imageList`、时长、比例、分辨率、声音等技术投影；不得改变分镜内容、镜头顺序、角色动作、对白、音效或氛围事实。
- 时长投影必须使用当前分镜组的 `duration_hint`，不得固定写 15 秒；`duration_hint=clamp(duration_estimate_seconds, 4, 15)`。
- 只有 submit plan 明确记录用户 opt-in `prompt_fidelity_mode=libtv_optimize` 或 `allow_libtv_prompt_optimization=true` 时，才允许 LibTV 做提示词优化、压缩、合并镜头或工作流规划。
- 若远端 query 显示 assistant 在 `create_generation_task` 之前执行“优化提示词 / 重新编排 / 摘要 / 镜头计划”且本地未 opt-in，必须判定为 `prompt_fidelity_violation / libtv_optimize_without_opt_in`；不得把该 session 标为正常 pending。

## Pre-Generation Audio Control Gate

- B 路线默认要求有声视频；声音开启必须在生成前落到真实生成任务参数，而不是只写进自然语言 prompt。
- 当前 `.agents/skills/cli/libTV/scripts/create_session.py` 只向 Agent-IM 发送消息，本地 CLI 本身没有独立 `--enable-sound` 开关。若不能使用可验证的生成任务接口、远端预执行工具调用草案，或其他能在执行前设置 `create_generation_task.params.enableSound` 的控制面，则该组必须标记 `blocked_audio_control_unverified`，不得作为正式生成提交。
- 可接受的生成前证据：请求体或预执行工具调用中 `create_generation_task.params.enableSound` 明确为 `on` / `true` / 布尔真值。
- 不可接受的证据：`enableSound: on` 只出现在提交文本、prompt 中写“声音开启”、或生成后已经出现视频 URL。

## Remote Handoff Contract

本地 `prompt.md` 必须采用 source-first enriched YAML：直接保留 `4-分组/第N集.md` 中对应 `## x-y-z` 分镜组原文，包含标题、正文和 fenced YAML；唯一允许的机械注入位置是 fenced YAML 中新增或更新 `故事板参照` 对象。该对象只在故事板图唯一绑定并上传后写入 `name: 故事板总参照`、`role: storyboard_sheet`、`reference_index: 1`、`uploaded_url`；缺故事板、多候选未裁决或未上传时不写空 URL、不写缺图说明。

发送给 LibTV 画布的 `*-libtv-submission.txt` 是运输层包裹文本，必须复用同一个 source-first enriched YAML 作为 `【分镜组源文本】`，并满足：

- 文件第一行必须是 `【LibTV 调用锁定】`。
- 第一段必须明确：`provider=seedance2.0`、`taskType=video`、`modeType=singleImage2video`、`imageList=["<真实 uploaded_url_1>"]`；无故事板图时改用 `modeType=text2video` 且 `imageList=[]`。`imageList` 必须直接填入上传返回的真实 URL，不得保留 `参照图1 URL` 占位符；B 路线有图时 `imageList` 只含 1 张故事板图，且必须 <= 9。
- 远端提交不得包含 `@projects/...`、`/Volumes/...`、`projects/aigc/.../6-图像/...` 等本地图片路径；只允许通过 `【分镜组源文本】` fenced YAML 的 `故事板参照.uploaded_url` 绑定故事板总参照与 uploaded URL，不得另起 `【故事板参照说明】`，也不得预设 `参照图1/2/N` 人工编号。
- 缺故事板、多候选未裁决、被排除或未进入预算的信息不得写入远端 `libtv-submission.txt`，只能写入 manifest / batch / report；不得出现“无独立参照图 / 无缓存 URL / 未进入预算 / 不创建空图片槽”等说明行。
- `【直接生成请求】` 必须写成“基于下方【分镜组源文本】”，并明确该源文本的 fenced YAML 已包含 `故事板参照.uploaded_url`；不得只写“基于上述参照图 URL”。
- 远端 `create_generation_task.params.prompt` 必须保留故事板总参照身份与图片 token/编号/URL 绑定；提交文本不得人工生成 `故事板总参照 参照图1` 这类编号，只有当 LibTV 自动插入真实图片编号后，才把故事板总参照邻近该真实编号，例如 `故事板总参照 {{Image 1}}` 或 `{{Image 1}} 故事板总参照`。不得把参照区压成裸 `{{Image 1}}`、裸 `图片1` 或裸 URL。
- 默认提交文本必须声明 `strict_original + transport_only`，且 `allow_libtv_prompt_optimization=false`；未显式 opt-in 时不得要求或默许 LibTV 重新组织、压缩、合并或摘要分镜组源文本。
- 本路线允许使用已经上传的故事板图作为整组总参照；禁止的是远端重新做故事板、拆 panel 或把故事板图误当首帧图生视频。

## YAML Job Schema

每个分镜组一个 job：

```yaml
- group_id: "1-1-1"
  command_type: "libtv_session_with_uploaded_references"
  prompt: "<完整 LibTV prompt>"
  reference_images:
    - path: "projects/aigc/<项目名>/6-图像/B-分镜故事板/第1集/images/1-1-1.png"
      uploaded_url: "<由 upload_file.py 返回>"
      marker: "uploaded_url_binding"
      role: "storyboard_sheet"
  reference_image_budget:
    max_images: 9
    selection_rule: "B 路线只允许单张故事板总参照进入 imageList；多候选必须唯一裁决或阻断。"
    excluded_due_to_budget: []
  libtv:
    requested_model: ""
    duration_source: "group_yaml"
    duration_estimate_seconds: 12
    duration_rule: "clamp(duration_estimate_seconds, 4, 15)"
    duration_hint: 12
    ratio_hint: "16:9"
    video_resolution_hint: "720p"
    poll_seconds: 45
    prompt_fidelity_mode: "strict_original"
    allow_libtv_prompt_optimization: false
    transport_only_projection: true
  output:
    download_dir: "projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第1集"
    expected_video_path: "projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第1集/1-1-1.mp4"
```

## Command Projection

| reference state | command_type | real `$libTV` projection |
| --- | --- | --- |
| `reference_images` 非空 | `libtv_session_with_uploaded_references` | 上传故事板图后调用 `create_session.py`；远端必须调用 Seedance `modeType=singleImage2video`，`imageList` 只含故事板 URL |
| `reference_images` 为空 | `libtv_session_text_only` | 调用 `create_session.py`；远端必须调用 Seedance `modeType=text2video` |

`7-视频` 不在本地硬编码模型版本。除非用户显式要求其他规格，否则默认参数固定写入远端提交：`resolution=720p`、`ratio=16:9`、`duration=<duration_hint>`、`enableSound=on`；`duration_hint` 从当前组 `duration_estimate_seconds` clamp 到 4-15 秒得到。用户显式指定模型、时长、比例、分辨率或质量档时，原样写入发送给 LibTV 的自然语言任务；未指定模型时使用 LibTV 后端默认路由。

## Prompt Projection

有参照图时，发送给 LibTV 的消息必须包含：

```text
【LibTV 调用锁定】
provider: seedance2.0
taskType: video
modeType: singleImage2video
imageList: ["<uploaded_url_1>"]
imageList 单个分镜组最多 9 张图；B 路线有图时只允许 1 张故事板总参照。提交文本不得预设“参照图1/2/N”人工编号。
duration: <duration_hint>
duration_rule: 从当前分镜组时长估算计算；小于等于4秒按4秒，4到15秒之间按估算值，大于等于15秒按15秒。
ratio: 16:9
resolution: 720p
enableSound: on
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
transport_only_projection: true
禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头。
只允许执行 transport_only 投影：上传 URL、imageList、duration、ratio、resolution、enableSound。

【直接生成请求】
请基于下方【分镜组源文本】，按 `singleImage2video + imageList` 生成一条连续视频。【分镜组源文本】保留了原始分镜组正文，且其 fenced YAML 中的 `故事板参照.reference_index=1` 和 `uploaded_url` 已绑定该分镜组故事板总参照；reference_index=1 对应 imageList[0] / 系统自动图1。请把原始正文和 YAML 故事板顺序绑定关系共同作为生成 prompt 完整体。该图片是该分镜组的多格分镜故事板视觉参照，只用于画面连续性、镜头顺序、构图节奏和角色位置参考；不得把故事板图当作首帧，也不得覆盖以下完整分镜组内容。如系统自动插入真实图片 token 或编号，必须把故事板总参照身份和 reference_index 放在对应 token/编号旁边。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把故事板参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<直接粘贴 source-first enriched YAML 分镜组全文；若有故事板图，fenced YAML 内包含 故事板参照.uploaded_url>
```

无参照图时，远端提交直接使用 `modeType: text2video` 调用锁 + source-first 完整分镜组内容。

## Background Concurrency

- 默认 `background: true`。
- 默认 worker 数：`min(4, job_count)`；用户可显式降低或提高，但不得超过 LibTV 账号配额、上传带宽和本机 I/O 可承受范围。
- 每个 worker 只处理自己的 group job，并写入独立临时结果，例如 `.tmp/<group_id>.result.json`。
- 主流程负责单线程汇总 queue ledger、results JSON 和 `执行报告.md`。
- 任一 job 失败不应抹掉其他 job 的 `sessionId`；失败组记录 `failed` 与 rework entry。

## Queue And Download

- 每个成功创建的 LibTV job 必须记录 `sessionId`、`projectUuid` 和 `projectUrl`。
- 短轮询超时后必须标记 `querying` 或 `queued`，并写 `next_action`。
- 查询使用 `python3 .agents/skills/cli/libTV/scripts/query_session.py <sessionId> --project-id <projectUuid>`。
- 按官方 `$libTV` 轮询策略查询完成后必须自动下载；下载使用 `python3 .agents/skills/cli/libTV/scripts/download_results.py <sessionId> --output-dir <episode_output_dir> --prefix <group_id>`。
- 下载后必须执行音轨探测，例如 `ffprobe -v error -select_streams a -show_entries stream=index,codec_type,codec_name -of json <video>`；没有 audio stream 时状态必须写成 `audio_missing / no_audio_stream`，不得交付。若 LibTV query 中 `task_result.audios` 为空且尚未通过下载后音轨检查，不能把视频 URL 当作成功。
- 下载目录固定为：

```text
projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第N集/
```

- 若远端成功但下载超时，按 `$libTV` 经验清理半截文件后重试，必要时用媒体 URL 直下。

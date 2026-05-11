# LibTV Handoff Contract

本文件定义 step3：把完整分镜组内容和可选多张分镜画面参照图，交给 `.agents/skills/cli/libTV` 作为唯一视频生成运输中心。A 叶子负责 AIGC prompt 与参照裁决；`$libTV` 负责本地参照图上传、创建会话、轮询和下载。

## Required LibTV Preflight

每次执行生成前必须：

1. 加载 `.agents/skills/cli/libTV/SKILL.md`。
2. 调用 `.agents/skills/cli/libTV` 官方技能包完成视频生成，不得绕过其 `scripts/` 直接拼接私有 OpenAPI。
3. 确认当前命令环境有 `LIBTV_ACCESS_KEY`；不得把 key 写入文件、模板、queue 或报告。
4. 如需新画布隔离当前分镜组，先运行 `python3 .agents/skills/cli/libTV/scripts/change_project.py`，并把返回的 `projectUuid/projectUrl` 写入 submit plan、queue 和 report。
5. 创建或打开本集 queue ledger：`第N集-libtv-queue.md`。
6. 对每个真实本地参照图运行 `python3 .agents/skills/cli/libTV/scripts/upload_file.py <path>`，把返回的 OSS URL 写入 submit plan。

## Official Script Order

有参照图时固定顺序：

1. `change_project.py`：仅在需要干净画布或用户要求隔离时执行。
2. `upload_file.py <path>`：逐图上传分镜画面参照，保存返回的 OSS URL。
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
- `strict_original` 表示 `【分镜组源文本】` 中的原始分镜组正文和 fenced YAML 里的 `分镜画面参照[].uploaded_url` 绑定关系必须共同作为 Seedance `create_generation_task.params.prompt` 的完整主体；LibTV 远端 Agent 不得在工具调用前自行生成优化版提示词、镜头计划或摘要版分镜。
- `transport_only` 只允许上传 URL、`imageList`、时长、比例、分辨率、声音等技术投影；不得改变分镜内容、镜头顺序、角色动作、对白、音效或氛围事实。
- 时长投影必须使用当前分镜组的 `duration_hint`，不得固定写 15 秒；`duration_hint=clamp(duration_estimate_seconds, 4, 15)`。
- 只有 submit plan 明确记录用户 opt-in `prompt_fidelity_mode=libtv_optimize` 或 `allow_libtv_prompt_optimization=true` 时，才允许 LibTV 做提示词优化、压缩、合并镜头或工作流规划。
- 若远端 query 显示 assistant 在 `create_generation_task` 之前执行“优化提示词 / 重新编排 / 摘要 / 镜头计划”且本地未 opt-in，必须判定为 `prompt_fidelity_violation / libtv_optimize_without_opt_in`；不得把该 session 标为正常 pending。

## Pre-Generation Audio Control Gate

- A 路线默认要求有声视频；声音开启必须在生成前落到真实生成任务参数，而不是只写进自然语言 prompt。
- 当前 `.agents/skills/cli/libTV/scripts/create_session.py` 只向 Agent-IM 发送消息，本地 CLI 本身没有独立 `--enable-sound` 开关。若不能使用可验证的生成任务接口、远端预执行工具调用草案，或其他能在执行前设置 `create_generation_task.params.enableSound` 的控制面，则该组必须标记 `blocked_audio_control_unverified`，不得作为正式生成提交。
- 可接受的生成前证据：请求体或预执行工具调用中 `create_generation_task.params.enableSound` 明确为 `on` / `true` / 布尔真值。
- 不可接受的证据：`enableSound: on` 只出现在提交文本、prompt 中写“声音开启”、或生成后已经出现视频 URL。

## Remote Handoff Contract

本地 `prompt.md` 必须采用 source-first enriched YAML：直接保留 `4-分组/第N集.md` 中对应 `## x-y-z` 分镜组原文，包含标题、正文和 fenced YAML；唯一允许的机械注入位置是 fenced YAML 中新增或更新 `分镜画面参照` 列表。该列表只写真实进入 `imageList` 的 `reference_index / shot_id / source_label / uploaded_url`；`reference_index` 使用 1-based 顺序，必须等于 `imageList` 顺序和 LibTV 自动图1/图2/图3顺序。缺图、未入预算或被排除的镜头不写入 `prompt.md`，只写 manifest / batch / report。

发送给 LibTV 画布的 `*-libtv-submission.txt` 是运输层包裹文本，必须复用同一个 source-first enriched YAML 作为 `【分镜组源文本】`，并满足：

- 文件第一行必须是 `【LibTV 调用锁定】`。
- 默认第一段必须明确：`provider=seedance2.0`、`taskType=video`、`modeType=image2video`、`imageList=["<真实 uploaded_url_1>", "<真实 uploaded_url_2>"]`。`imageList` 必须直接填入上传返回的真实 URL，不得保留 `参照图N URL` 占位符；单组 `imageList` 最多 9 张图。
- 仅当用户显式要求首尾帧/起止帧过渡，且参照图数量为 1-2 张时，允许 `modeType=frames2video`；否则不得把 A 的多张镜级参照误锁为 `frames2video`。
- 远端提交不得包含 `@projects/...`、`/Volumes/...`、`projects/aigc/.../6-图像/...` 等本地图片路径；只允许通过 `【分镜组源文本】` fenced YAML 的 `分镜画面参照[].uploaded_url` 绑定 `shot_id / source_label` 与 uploaded URL，不得另起 `【分镜画面参照说明】`，也不得预设 `参照图1/2/N` 人工编号。
- 缺图、未进入预算、被排除或超限取舍的分镜画面不得写入远端 `libtv-submission.txt`，只能写入 manifest / batch / report；不得出现“无独立参照图 / 无缓存 URL / 未进入预算 / 不创建空图片槽”等说明行。
- 分镜画面连续性要求应使用一段总领式说明，并入 `【直接生成请求】`；不得在每个 URL 行后重复长句，避免 LibTV 自动图片 token 与分镜ID邻近关系被长文本稀释。
- `【直接生成请求】` 必须写成“基于下方【分镜组源文本】”，并明确该源文本的 fenced YAML 已包含 `分镜画面参照[].reference_index / uploaded_url`；不得只写“基于上述参照图 URL”。
- 远端 `create_generation_task.params.prompt` 必须保留分镜ID/镜头标签与图片 token/编号/URL 绑定；提交文本不得人工生成 `1-1-1-1 参照图1` 这类编号，只有当 LibTV 自动插入真实图片编号后，才把分镜ID/镜头标签邻近该真实编号，例如 `1-1-1-1 {{Image 1}}` 或 `{{Image 1}} 1-1-1-1`。不得把参照区压成 `{{Image 1}} {{Image 2}} ...`、`图片1 图片2 ...` 或裸 URL 列表。
- 默认提交文本必须声明 `strict_original + transport_only`，且 `allow_libtv_prompt_optimization=false`；未显式 opt-in 时不得要求或默许 LibTV 重新组织、压缩、合并或摘要分镜组源文本。
- 本路线允许使用已经上传的分镜画面图作为参照；禁止的是远端新做分镜图或把每张图变成独立单镜任务。

## YAML Job Schema

每个分镜组一个 job：

```yaml
- group_id: "1-1-1"
  command_type: "libtv_session_with_uploaded_references"
  prompt: "<完整 LibTV prompt>"
  reference_images:
    - shot_id: "1-1-1-1"
      path: "projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-1.png"
      uploaded_url: "<由 upload_file.py 返回>"
      marker: "uploaded_url_binding"
      role: "storyboard_frame"
  reference_image_budget:
    max_images: 9
    selection_rule: "首镜、尾镜、关键动作、转场和空间关系镜头优先；超过上限时排除重复或不必要的相邻画面。"
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
    download_dir: "projects/aigc/<项目名>/7-视频/A-分镜画面参照/第1集"
    expected_video_path: "projects/aigc/<项目名>/7-视频/A-分镜画面参照/第1集/1-1-1.mp4"
```

## Command Projection

| reference state | command_type | real `$libTV` projection |
| --- | --- | --- |
| `reference_images` 非空 | `libtv_session_with_uploaded_references` | 逐图上传后调用 `create_session.py`；远端默认调用 Seedance `modeType=image2video`，`imageList` 按 shot 顺序排列 |
| `reference_images` 为 1-2 张且用户显式要求首尾帧 | `libtv_session_with_uploaded_references` | 远端调用 Seedance `modeType=frames2video`，`imageList` 顺序为首帧、尾帧 |
| `reference_images` 为空 | `libtv_session_text_only` | 远端调用 Seedance `modeType=text2video` |
| `reference_images` 超过 9 张、用户上限或 LibTV 当前可承受范围 | `blocked` / `split_by_user_policy` | 不静默丢图；先按 9 图预算裁决，仍无法合理压缩时按用户策略阻断、分段或降级，并写入 report |

`7-视频` 不在本地硬编码模型版本。除非用户显式要求其他规格，否则默认参数固定写入远端提交：`resolution=720p`、`ratio=16:9`、`duration=<duration_hint>`、`enableSound=on`；`duration_hint` 从当前组 `duration_estimate_seconds` clamp 到 4-15 秒得到。用户显式指定模型、时长、比例、分辨率或质量档时，原样写入发送给 LibTV 的自然语言任务；未指定模型时使用 LibTV 后端默认路由。

## Prompt Projection

有参照图时，发送给 LibTV 的消息必须包含：

```text
【LibTV 调用锁定】
provider: seedance2.0
taskType: video
modeType: image2video
imageList: ["<uploaded_url_1>", "<uploaded_url_2>", ...]
imageList 单个分镜组最多 9 张图；超过时保留首镜、尾镜、关键动作、转场和空间关系镜头，排除重复或不必要的相邻画面。
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
请基于下方【分镜组源文本】，按 `image2video + imageList` 生成一条连续视频。【分镜组源文本】保留了原始分镜组正文，且其 fenced YAML 中的 `分镜画面参照[].reference_index` 和 `uploaded_url` 已绑定对应分镜画面图；reference_index=1 对应 imageList[0] / 系统自动图1，reference_index=2 对应 imageList[1] / 系统自动图2，依次类推。请把原始正文和 YAML 分镜画面顺序绑定关系共同作为生成 prompt 完整体。以上图片仅作为对应分镜ID的镜级视觉锚点，统一用于画面连续性、角色位置、构图、镜头顺序和关键动作参考；不得把任一图片当作唯一首帧，不得覆盖以下完整分镜组内容。如系统自动插入真实图片 token 或编号，必须把分镜ID/镜头标签和 reference_index 放在对应 token/编号旁边。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把分镜画面参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<直接粘贴 source-first enriched YAML 分镜组全文；若有参照图，fenced YAML 内包含 分镜画面参照[].uploaded_url>
```

无参照图时，远端提交使用 `modeType: text2video` 调用锁 + source-first 完整分镜组内容。只有用户显式“首尾帧/起止帧过渡”时，才把上述 `modeType` 改为 `frames2video`。

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
projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/
```

- 若远端成功但下载超时，按 `$libTV` 经验清理半截文件后重试，必要时用媒体 URL 直下。

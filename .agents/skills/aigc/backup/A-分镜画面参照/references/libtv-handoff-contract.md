# LibTV Handoff Contract

本文件定义 step3：把完整分镜组内容和可选多张分镜画面参照图，交给 `.agents/skills/cli/libTV` 作为唯一视频生成运输中心。A 叶子负责 AIGC prompt 与参照裁决；`$libTV` 负责本地参照图上传、创建会话、轮询和下载。

## Required LibTV Preflight

每次执行生成前必须：

1. 加载 `.agents/skills/cli/libTV/SKILL.md`。
2. 调用 `.agents/skills/cli/libTV` 官方技能包完成视频生成，不得绕过其 `scripts/` 直接拼接私有 OpenAPI。
3. 确认当前命令环境有 `LIBTV_ACCESS_KEY`；不得把 key 写入文件、模板、queue 或报告。
4. 新建分镜画面参照视频任务时必须先运行 `python3 .agents/skills/cli/libTV/scripts/change_project.py`，或由用户显式指定一个可继续使用的 existing `projectUuid/projectUrl`；把锁定后的 `projectUuid/projectUrl` 写入 submit plan、queue 和 report。
5. 创建或打开本集 queue ledger：`第N集-libtv-queue.md`。
6. 在上述 `projectUuid` 已锁定后，对每个真实本地参照图运行 `python3 .agents/skills/cli/libTV/scripts/upload_file.py <path>`，把返回的 OSS URL 写入 submit plan。每个 uploaded URL 的 `/claw/<projectUuid>/` 必须与 submit plan 中锁定的 `projectUuid` 一致。上传返回只建立 `frame_uploads: shot_id/source_label -> uploaded_url` 身份映射，不承载图N顺序真源；最终图N顺序必须由视频生成 `imageList` 形成的 `generation_slots` 决定。

## Official Script Order

有参照图时固定顺序：

1. `change_project.py`：新建任务时必须先执行，或由用户显式指定 existing `projectUuid/projectUrl` 作为继续使用的画布锁。
2. `upload_file.py <path>`：上传分镜画面参照，保存返回的 OSS URL；上传顺序不得单独作为 `reference_index` 真源。
3. `create_session.py "$(cat <prompt>)"`：提交远端 `*-libtv-submission.txt`，返回 `sessionId/projectUuid/projectUrl`。
4. `query_session.py <sessionId> --project-id <projectUuid>`：按官方 `$libTV` 轮询策略查询画布消息和生成结果。
5. `download_results.py <sessionId> --output-dir <episode_output_dir> --filename <group_id>.mp4`：生成完成后自动下载到本技能的集目录，并使用精确文件名避免生成 `<group_id>_01.mp4`。

无参照图时跳过 `upload_file.py`，其余顺序不变。

## Canvas Sync

- 每个任务必须同步到 LibTV 画布：远端消息、上传参照、生成节点和结果都应保留在同一 `projectUrl`。
- 有参照图时，上传 URL 的 `claw` project scope、submit plan `projectUuid`、queue `projectUuid` 和 `create_session.py` 返回的 `projectUuid` 必须一致；不一致时状态写成 `reference_project_scope_mismatch`，不得提交或继续等待。
- queue/result/report 必须记录 `sessionId`、`projectUuid`、`projectUrl`，用于用户在画布查看。
- 若画布未出现对应生成节点或结果 URL，不得把本地状态标为 downloaded / generated。

## Prompt Fidelity And Optimization Authorization

- 默认远端 handoff 必须采用 `strict_original + transport_only`：`prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false`，并禁止提示词优化、重新编排、摘要、改写和补镜头。
- `strict_original` 表示 `【分镜组源文本】` 中的原始分镜组正文和 final fenced YAML 里的 `分镜画面参照[].reference_index / uploaded_url / image_token` 绑定关系必须共同作为 Seedance `create_generation_task.params.prompt` 的完整主体；LibTV 远端 Agent 不得在工具调用前自行生成优化版提示词、镜头计划或摘要版分镜。
- `transport_only` 只允许上传 URL、`imageList`、时长、比例、分辨率、声音等技术投影；不得改变分镜内容、镜头顺序、角色动作、对白、音效或氛围事实。
- 时长投影必须使用当前分镜组的 `duration_hint`，不得固定写 15 秒；`duration_hint=clamp(duration_estimate_seconds, 4, 15)`。
- 只有 submit plan 明确记录用户 opt-in `prompt_fidelity_mode=libtv_optimize` 或 `allow_libtv_prompt_optimization=true` 时，才允许 LibTV 做提示词优化、压缩、合并镜头或工作流规划。
- 若远端 query 显示 assistant 在 `create_generation_task` 之前执行“优化提示词 / 重新编排 / 摘要 / 镜头计划”且本地未 opt-in，必须判定为 `prompt_fidelity_violation / libtv_optimize_without_opt_in`；不得把该 session 标为正常 pending。

## Pre-Generation Audio Control Gate

- A 路线默认要求有声视频；远端提交文本必须声明 `enableSound: on`。
- 当前 `.agents/skills/cli/libTV/scripts/create_session.py` 只向 Agent-IM 发送消息，本地 CLI 本身没有独立 `--enable-sound` 开关。若不能在生成前验证 `create_generation_task.params.enableSound`，记录为 `audio_preflight_unverified_non_blocking`，但不得因此阻断提交。
- 可接受的生成前强证据：请求体或预执行工具调用中 `create_generation_task.params.enableSound` 明确为 `on` / `true` / 布尔真值。
- 生成前缺少强证据时，必须保留后验音频门：生成后必须通过 `task_result.audios` 非空、音频 URL，或下载后 `ffprobe` 检出 audio stream；否则状态写成 `audio_missing / no_audio_stream`，不得交付。

## Remote Handoff Contract

本地 `prompt.md` 必须采用 source-first YAML 两阶段处理：draft 直接保留 `5-分组/第N集.md` 中对应 `## x-y-z` 分镜组原文，包含标题、正文和原始 fenced YAML，不提前写死 `reference_index / uploaded_url`；final 唯一允许的机械注入位置是 fenced YAML 中新增或更新 `分镜画面参照` 列表。该列表只写真实进入 `imageList` 的 `reference_index / shot_id / source_label / uploaded_url / image_token`；`uploaded_url` 来自 `frame_uploads` 的身份映射，`reference_index` 来自 `generation_slots` 的视频生成槽位顺序。`reference_index` 使用 1-based 顺序，必须等于最终 UI 图N / `imageList` 顺序和 LibTV 自动图1/图2/图3顺序。缺图、未入预算或被排除的镜头不写入 final prompt，只写 manifest / batch / report。

发送给 LibTV 画布的 `*-libtv-submission.txt` 是运输层包裹文本，必须复用已确认槽位后的 final source-first YAML 作为 `【分镜组源文本】`，并满足：

- 文件第一行必须是 `【LibTV 调用锁定】`。
- 默认第一段必须明确：`provider=seedance2.0`、`taskType=video`、`modeType=image2video`、`imageList=["<真实 uploaded_url_1>", "<真实 uploaded_url_2>"]`。`imageList` 必须直接填入上传返回的真实 URL，不得保留 `参照图N URL` 占位符；单组 `imageList` 最多 9 张图。
- 源层规则：`frame_uploads` 只证明“哪个 shot_id/source_label 对应哪个 OSS URL”；`generation_slots` 才证明“图N/imageList[n-1] 对应哪个 OSS URL 和 shot_id”。若视频生成框 UI 缩略图顺序可观测，以 UI 图N / `Image N` 为最终槽位真源；只有 UI 槽位不可观测时才用远端 query 的实际 `imageList[n]` URL 反查 `frame_uploads`。回刷 fenced YAML 的 `reference_index=N`、真实 `uploaded_url` 和可选 `image_token` 后重提。
- 仅当用户显式要求首尾帧/起止帧过渡，且参照图数量为 1-2 张时，允许 `modeType=frames2video`；否则不得把 A 的多张镜级参照误锁为 `frames2video`。
- 远端提交不得包含 `@projects/...`、`/Volumes/...`、`projects/aigc/.../7-图像/...` 等本地图片路径；只允许通过 final `【分镜组源文本】` fenced YAML 的 `分镜画面参照[].reference_index / uploaded_url / image_token` 绑定 `shot_id / source_label` 与真实生成槽位，不得另起 `【分镜画面参照说明】`，也不得预设 `参照图1/2/N` 人工编号。
- 缺图、未进入预算、被排除或超限取舍的分镜画面不得写入远端 `libtv-submission.txt`，只能写入 manifest / batch / report；不得出现“无独立参照图 / 无缓存 URL / 未进入预算 / 不创建空图片槽”等说明行。
- 分镜画面连续性要求应使用一段总领式说明，并入 `【直接生成请求】`；不得在每个 URL 行后重复长句，避免 LibTV 自动图片 token 与分镜ID邻近关系被长文本稀释。
- `【直接生成请求】` 必须写成“基于下方【分镜组源文本】”，并明确该源文本的 fenced YAML 已包含 `分镜画面参照[].reference_index / uploaded_url / image_token`；不得只写“基于上述参照图 URL”。
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
      path: "projects/aigc/<项目名>/7-图像/A-分镜画面/第1集/images/1-1-1-1.png"
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
    download_dir: "projects/aigc/<项目名>/8-视频/A-分镜画面参照/第1集"
    expected_video_path: "projects/aigc/<项目名>/8-视频/A-分镜画面参照/第1集/1-1-1.mp4"
```

## Command Projection

| reference state | command_type | real `$libTV` projection |
| --- | --- | --- |
| `reference_images` 非空 | `libtv_session_with_uploaded_references` | 逐图上传后调用 `create_session.py`；远端默认调用 Seedance `modeType=image2video`，`imageList` 按 shot 顺序排列 |
| `reference_images` 为 1-2 张且用户显式要求首尾帧 | `libtv_session_with_uploaded_references` | 远端调用 Seedance `modeType=frames2video`，`imageList` 顺序为首帧、尾帧 |
| `reference_images` 为空 | `libtv_session_text_only` | 远端调用 Seedance `modeType=text2video` |
| `reference_images` 超过 9 张、用户上限或 LibTV 当前可承受范围 | `blocked` / `split_by_user_policy` | 不静默丢图；先按 9 图预算裁决，仍无法合理压缩时按用户策略阻断、分段或降级，并写入 report |

`8-视频` 不在本地硬编码模型版本。除非用户显式要求其他规格，否则默认参数固定写入远端提交：`resolution=720p`、`ratio=16:9`、`duration=<duration_hint>`、`enableSound=on`；`duration_hint` 从当前组 `duration_estimate_seconds` clamp 到 4-15 秒得到。用户显式指定模型、时长、比例、分辨率或质量档时，原样写入发送给 LibTV 的自然语言任务；未指定模型时使用 LibTV 后端默认路由。

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
请基于下方【分镜组源文本】，按 `image2video + imageList` 生成一条连续视频。【分镜组源文本】保留了原始分镜组正文，且其 fenced YAML 中的 `分镜画面参照[].reference_index / uploaded_url / image_token` 已绑定对应分镜画面图；reference_index=1 对应 imageList[0] / 系统自动图1，reference_index=2 对应 imageList[1] / 系统自动图2，依次类推。请把原始正文和 YAML 分镜画面顺序绑定关系共同作为生成 prompt 完整体。以上图片仅作为对应分镜ID的镜级视觉锚点，统一用于画面连续性、角色位置、构图、镜头顺序和关键动作参考；不得把任一图片当作唯一首帧，不得覆盖以下完整分镜组内容。如系统自动插入真实图片 token 或编号，必须把分镜ID/镜头标签和 reference_index 放在对应 token/编号旁边。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把分镜画面参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<直接粘贴 final source-first YAML 分镜组全文；若有参照图，fenced YAML 内包含 分镜画面参照[].reference_index / uploaded_url / image_token>
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
- 按官方 `$libTV` 轮询策略查询完成后必须自动下载；下载使用 `python3 .agents/skills/cli/libTV/scripts/download_results.py <sessionId> --output-dir <episode_output_dir> --filename <group_id>.mp4`。
- 下载后必须执行音轨探测，例如 `ffprobe -v error -select_streams a -show_entries stream=index,codec_type,codec_name -of json <video>`；没有 audio stream 时状态必须写成 `audio_missing / no_audio_stream`，不得交付。若 LibTV query 中 `task_result.audios` 为空且尚未通过下载后音轨检查，不能把视频 URL 当作成功。
- 下载目录固定为：

```text
projects/aigc/<项目名>/8-视频/A-分镜画面参照/第N集/
```

- 若远端成功但下载超时，按 `$libTV` 经验清理半截文件后重试，必要时用媒体 URL 直下。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 生成前是否加载 `.agents/skills/cli/libTV/SKILL.md` 并调用官方 `$libTV` 技能/脚本，而不是绕过为私有 OpenAPI 或手写提交器？ | `GATE-FVID-LIBTV-02` | `FAIL-FVID-LIBTV` | `N8-DISPATCH` | submit plan 中的 `$libTV` skill load note、官方脚本命令清单、private API scan |
| 是否完成 `LIBTV_ACCESS_KEY` credential check，且没有把 key 写入 prompt、batch、queue、模板或报告？ | `GATE-FVID-LIBTV-03` | `FAIL-FVID-LIBTV` | `N8-DISPATCH` | credential check status、redacted env note、secret scan summary |
| 新任务是否先锁定 `projectUuid/projectUrl`，或仅在用户显式指定时复用 existing 画布，并把同一画布写入 submit plan、queue 和 report？ | `GATE-FVID-LIBTV-04` | `FAIL-FVID-LIBTV` | `N8-DISPATCH` | `projectUuid/projectUrl` lock record、`create_session.py` response、queue/report projection |
| 每个上传 URL 的 `/claw/<projectUuid>/` 是否与锁定画布一致，且上传结果只进入 `frame_uploads` 身份映射而不直接当作图N顺序？ | `GATE-FVID-LIBTV-05` | `FAIL-FVID-SLOT-ORDER` | `N8-DISPATCH` | upload ledger、project scope check、`frame_uploads` / `generation_slots` 对照 |
| 官方脚本顺序是否保持 `change_project.py -> upload_file.py -> create_session.py -> query_session.py -> download_results.py`，且无参照图时只跳过 upload？ | `GATE-FVID-LIBTV-06` | `FAIL-FVID-LIBTV` | `N8-DISPATCH` | command projection、per-job execution trace、text-only branch note |
| 画布同步是否真实可查：远端消息、上传参照、生成节点和结果都在同一 `projectUrl`，缺生成节点或结果 URL 时不标记 generated/downloaded？ | `GATE-FVID-LIBTV-07` | `FAIL-FVID-QUEUE` | `N9-QUEUE` | queue ledger、query response excerpt、remote node/result URL status |
| 有参照图、无参照图、显式首尾帧三种路线是否分别投影为 `image2video`、`text2video`、受限 `frames2video`，且没有空图片槽位？ | `GATE-FVID-LIBTV-01` | `FAIL-FVID-LIBTV` | `N6-YAML` | batch YAML 的 command type、reference count、modeType、empty slot scan |
| 单组 `imageList` 是否最多 9 张；超限时是否先做预算裁决并记录 `excluded_due_to_budget`，而不是静默丢图或超量提交？ | `GATE-FVID-REF-05` | `FAIL-FVID-REFERENCE-BUDGET` | `N5-REF-BIND` | selected / excluded shot list、budget rationale、blocked reason |
| draft/final source-first YAML 是否分相：draft 不伪造 URL，final 只在 fenced YAML 的 `分镜画面参照[]` 注入进入 `imageList` 的真实槽位绑定？ | `GATE-FVID-PROMPT-02` | `FAIL-FVID-PROMPT` | `N6-YAML` | draft/final YAML diff、`*-libtv-submission.txt` 截要、slot ledger |
| `reference_index` 是否来自最终 UI 图N或实际 `imageList` 的 `generation_slots`，而不是来自上传顺序、本地 marker 或人工 `参照图N`？ | `GATE-FVID-REF-04` | `FAIL-FVID-SLOT-ORDER` | `N8-DISPATCH` | `generation_slots`、`imageList`、final YAML `reference_index` 对照 |
| 远端 `*-libtv-submission.txt` 是否以 `【LibTV 调用锁定】` 开头，使用真实 uploaded URL，不含本地路径、占位 URL、另起 `【分镜画面参照说明】` 或缺图/未入预算说明？ | `GATE-FVID-PROMPT-02` | `FAIL-FVID-PROMPT` | `N6-YAML` | submission text excerpt、本地路径/占位符 scan、final fenced YAML 参照列表 |
| `【直接生成请求】` 是否基于下方 `【分镜组源文本】`，并让原始组正文与 final YAML 参照绑定共同作为生成 prompt 完整体，而不是裸图片 token、裸编号或裸 URL 列表？ | `GATE-FVID-PROMPT-02` | `FAIL-FVID-PROMPT` | `N6-YAML` | remote prompt excerpt、分镜ID/镜头标签与图片 token/URL 邻近绑定检查 |
| 默认提交是否保持 `strict_original + transport_only` 与 `allow_libtv_prompt_optimization=false`；未 opt-in 时 query 中是否没有优化、摘要、重排、补镜头或镜头计划？ | `GATE-FVID-PROMPT-03` | `FAIL-FVID-PROMPT` | `N6-YAML` | submit plan opt-in field、submission text fidelity block、query prompt audit |
| `duration` 是否使用当前组 `duration_hint=clamp(duration_estimate_seconds, 4, 15)`，而不是全组固定 15 秒或脱离组底时长证据？ | `GATE-FVID-DURATION-02` | `FAIL-FVID-DURATION` | `N6-YAML` | group duration evidence、batch `duration_hint`、remote submission duration |
| 远端提交是否声明 `enableSound=on`；若生成前无法验证工具参数，是否记录 `audio_preflight_unverified_non_blocking` 并继续官方提交流程？ | `GATE-FVID-AUDIO-01` | `FAIL-FVID-AUDIO` | `N8-DISPATCH` | submission audio line、preflight verification status、non-blocking note |
| 生成后是否通过 `task_result.audios`、音频 URL 或下载后 `ffprobe` 证明有 audio stream；无音轨是否写成 `audio_missing / no_audio_stream` 且不交付？ | `GATE-FVID-AUDIO-02` | `FAIL-FVID-AUDIO` | `N10-QUERY-DOWNLOAD` | query audio evidence、ffprobe JSON、`audio_missing / no_audio_stream` status if failed |
| 后台并发是否每组保留 `sessionId/projectUuid/projectUrl`、queue row 和 next_action，失败组不抹掉已提交组状态？ | `GATE-FVID-LIBTV-07` | `FAIL-FVID-QUEUE` | `N9-QUEUE` | queue ledger、tmp result、submitted/failed group status |
| 完成后是否按 `$libTV` 查询并自动下载到 `8-视频/A-分镜画面参照/第N集/`，文件名精确为 `<group_id>.mp4`，不把远端成功或半截文件误判为交付？ | `GATE-FVID-DOWNLOAD-01` | `FAIL-FVID-DOWNLOAD` | `N10-QUERY-DOWNLOAD` | download command、expected video path、file existence/size and retry note |
| close report 是否覆盖 submit plan、queue、结果、下载/跳过/失败原因、音频验收状态和可执行返工入口？ | `GATE-FVID-REPORT-01` | `FAIL-FVID-REPORT` | `N12-CLOSE` | close report 的 coverage、status summary、rework targets |

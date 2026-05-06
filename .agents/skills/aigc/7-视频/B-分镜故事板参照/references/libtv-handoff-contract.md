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
- `strict_original` 表示 `【故事板参照说明】` 中的故事板身份/参照图/URL 绑定关系与 `【分镜组源文本】` 原文必须共同作为 Seedance `create_generation_task.params.prompt` 的完整主体；LibTV 远端 Agent 不得在工具调用前自行生成优化版提示词、镜头计划或摘要版分镜。
- `transport_only` 只允许上传 URL、`imageList`、时长、比例、分辨率、声音等技术投影；不得改变分镜内容、镜头顺序、角色动作、对白、音效或氛围事实。
- 只有 submit plan 明确记录用户 opt-in `prompt_fidelity_mode=libtv_optimize` 或 `allow_libtv_prompt_optimization=true` 时，才允许 LibTV 做提示词优化、压缩、合并镜头或工作流规划。
- 若远端 query 显示 assistant 在 `create_generation_task` 之前执行“优化提示词 / 重新编排 / 摘要 / 镜头计划”且本地未 opt-in，必须判定为 `prompt_fidelity_violation / libtv_optimize_without_opt_in`；不得把该 session 标为正常 pending。

## Remote Handoff Contract

本地审核 prompt 可以保留故事板本地路径，便于 review gate 回查；发送给 LibTV 画布的 `*-libtv-submission.txt` 是另一层远端提交文本，必须满足：

- 文件第一行必须是 `【LibTV 调用锁定】`。
- 第一段必须明确：`provider=seedance2.0`、`taskType=video`、`modeType=singleImage2video`、`imageList=["<真实 uploaded_url_1>"]`；无故事板图时改用 `modeType=text2video` 且 `imageList=[]`。`imageList` 必须直接填入上传返回的真实 URL，不得保留 `参照图1 URL` 占位符。
- 远端提交不得包含 `@projects/...`、`/Volumes/...`、`projects/aigc/.../6-图像/...` 等本地图片路径；只允许出现 `故事板总参照：参照图1 <uploaded_url>` 与故事板总参照用途说明。
- `【直接生成请求】` 必须写成“基于【故事板参照说明】（包含故事板身份和参照 URL）和下方【分镜组源文本】”，不得只写“基于上述参照图 URL”。
- 远端 `create_generation_task.params.prompt` 必须保留故事板总参照身份与图片 token/编号绑定，例如 `故事板总参照 参照图1`、`故事板总参照 {{Image 1}}` 或 `{{Image 1}} 故事板总参照`；不得把参照区压成裸 `{{Image 1}}`、裸 `图片1` 或裸 URL。
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
      marker: "参照图1"
      role: "storyboard_sheet"
  libtv:
    requested_model: ""
    duration_hint: 15
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

`7-视频` 不在本地硬编码模型版本。除非用户显式要求其他规格，否则默认参数固定写入远端提交：`resolution=720p`、`ratio=16:9`、`duration=15`、`enableSound=on`；用户显式指定模型、时长、比例、分辨率或质量档时，原样写入发送给 LibTV 的自然语言任务；未指定模型时使用 LibTV 后端默认路由。

## Prompt Projection

有参照图时，发送给 LibTV 的消息必须包含：

```text
【LibTV 调用锁定】
provider: seedance2.0
taskType: video
modeType: singleImage2video
imageList: ["<uploaded_url_1>"]
duration: 15
ratio: 16:9
resolution: 720p
enableSound: on
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
transport_only_projection: true
禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头。
只允许执行 transport_only 投影：上传 URL、imageList、duration、ratio、resolution、enableSound。

【故事板参照说明】
故事板总参照：参照图1 <uploaded_url>
参照图1 是该分镜组的多格分镜故事板视觉参照，只用于画面连续性、镜头顺序、构图节奏和角色位置参考；不得把故事板图当作首帧，也不得覆盖以下完整分镜组内容。

【直接生成请求】
请基于【故事板参照说明】（包含故事板身份和参照 URL）和下方【分镜组源文本】，按 `singleImage2video + imageList` 生成一条连续视频。请直接把【故事板参照说明】中与本组相关的故事板总参照绑定关系 + 【分镜组源文本】原文作为生成 prompt 完整体。禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头；禁止把故事板参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<完整分镜组内容>
```

无参照图时，prompt 直接使用 `modeType: text2video` 固定开头加完整分镜组内容。

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
- 下载目录固定为：

```text
projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第N集/
```

- 若远端成功但下载超时，按 `$libTV` 经验清理半截文件后重试，必要时用媒体 URL 直下。

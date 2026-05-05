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

## Remote Handoff Contract

本地审核 prompt 可以保留 `shot_id@path` 或 `本地源`，便于 review gate 回查；发送给 LibTV 画布的 `*-libtv-submission.txt` 是另一层远端提交文本，必须满足：

- 文件第一行必须是 `【LibTV 调用锁定】`。
- 默认第一段必须明确：`provider=seedance2.0`、`taskType=video`、`modeType=image2video`、`imageList=["<真实 uploaded_url_1>", "<真实 uploaded_url_2>"]`。`imageList` 必须直接填入上传返回的真实 URL，不得保留 `参照图N URL` 占位符。
- 仅当用户显式要求首尾帧/起止帧过渡，且参照图数量为 1-2 张时，允许 `modeType=frames2video`；否则不得把 A 的多张镜级参照误锁为 `frames2video`。
- 远端提交不得包含 `@projects/...`、`/Volumes/...`、`projects/aigc/.../6-图像/...` 等本地图片路径；只允许出现 `参照图N：<uploaded_url>` 与必要的 `shot_id` / 分镜编号说明。
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
      marker: "参照图1"
      role: "storyboard_frame"
  libtv:
    requested_model: ""
    duration_hint: 15
    ratio_hint: "16:9"
    video_resolution_hint: "720p"
    poll_seconds: 45
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
| `reference_images` 超过用户或 LibTV 当前可承受范围 | `blocked` / `split_by_user_policy` | 不静默丢图；按用户策略阻断、分段或降级，并写入 report |

`7-视频` 不在本地硬编码模型版本。除非用户显式要求其他规格，否则默认参数固定写入远端提交：`resolution=720p`、`ratio=16:9`、`duration=15`、`enableSound=on`；用户显式指定模型、时长、比例、分辨率或质量档时，原样写入发送给 LibTV 的自然语言任务；未指定模型时使用 LibTV 后端默认路由。

## Prompt Projection

有参照图时，发送给 LibTV 的消息必须包含：

```text
【LibTV 调用锁定】
provider: seedance2.0
taskType: video
modeType: image2video
imageList: ["<uploaded_url_1>", "<uploaded_url_2>", ...]
duration: 15
ratio: 16:9
resolution: 720p
enableSound: on

以下分镜画面图仅作为镜级视觉参照，用于画面连续性、角色位置、构图、镜头顺序和关键动作参考；不得把任一图片当作唯一首帧，不得覆盖以下完整分镜组内容。
参照图1：<uploaded_url>（1-1-1-1）
参照图2：<uploaded_url>（1-1-1-2）

<直接粘贴 projects/aigc/<项目名>/4-分组/第N集.md 中该分镜组的完整现有内容>
```

无参照图时，prompt 使用 `modeType: text2video` 固定开头加完整分镜组内容。只有用户显式“首尾帧/起止帧过渡”时，才把上述 `modeType` 改为 `frames2video`。

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
projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/
```

- 若远端成功但下载超时，按 `$libTV` 经验清理半截文件后重试，必要时用媒体 URL 直下。

# LibTV Handoff Contract

本文件定义 step3：把完整分镜组内容和可选多张分镜画面参照图，交给 `.agents/skills/cli/libTV` 作为唯一视频生成运输中心。A 叶子负责 AIGC prompt 与参照裁决；`$libTV` 负责本地参照图上传、创建会话、轮询和下载。

## Required LibTV Preflight

每次执行生成前必须：

1. 加载 `.agents/skills/cli/libTV/SKILL.md + CONTEXT.md`。
2. 确认当前命令环境有 `LIBTV_ACCESS_KEY`；不得把 key 写入文件、模板、queue 或报告。
3. 创建或打开本集 queue ledger：`第N集-libtv-queue.md`。
4. 对每个真实本地参照图运行 `python3 .agents/skills/cli/libTV/scripts/upload_file.py <path>`，把返回的 OSS URL 写入 submit plan。

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
    download_dir: "projects/aigc/<项目名>/7-视频/A-分镜画面参照/第1集/videos"
    expected_video_path: "projects/aigc/<项目名>/7-视频/A-分镜画面参照/第1集/videos/1-1-1.mp4"
```

## Command Projection

| reference state | command_type | real `$libTV` projection |
| --- | --- | --- |
| `reference_images` 非空 | `libtv_session_with_uploaded_references` | 逐图调用 `upload_file.py`，再调用 `create_session.py "<prompt + 参照图N: <uploaded_url>>"` |
| `reference_images` 为空 | `libtv_session_text_only` | 调用 `create_session.py "<完整组内容 prompt>"` |
| `reference_images` 超过用户或 LibTV 当前可承受范围 | `blocked` / `split_by_user_policy` | 不静默丢图；按用户策略阻断、分段或降级，并写入 report |

`7-视频` 不在本地硬编码模型版本。除非用户显式要求其他规格，否则默认 720P、15 秒、16:9；用户显式指定模型、时长、比例、分辨率或质量档时，原样写入发送给 LibTV 的自然语言任务；未指定模型时使用 LibTV 后端默认路由。

## Prompt Projection

有参照图时，发送给 LibTV 的消息必须包含：

```text
根据以下完整分镜组内容生成一条连续视频。保持分镜顺序、角色动作、镜头运动、场景与情绪连续；不生成字幕，不生成BGM，保留物理互动音效与环境音。

以下分镜画面图仅作为镜级视觉参照，用于画面连续性、角色位置、构图、镜头顺序和关键动作参考；不得把任一图片当作唯一首帧，不得覆盖以下完整分镜组内容。
参照图1：<uploaded_url>（1-1-1-1，本地源：projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-1.png）
参照图2：<uploaded_url>（1-1-1-2，本地源：projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-2.png）

<直接粘贴 projects/aigc/<项目名>/4-分组/第N集.md 中该分镜组的完整现有内容>
```

无参照图时，prompt 直接使用固定视频约束前缀加完整分镜组内容。

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
- 下载使用 `python3 .agents/skills/cli/libTV/scripts/download_results.py <sessionId> --output-dir <videos_dir> --prefix <group_id>`。
- 下载目录固定为：

```text
projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/videos/
```

- 若远端成功但下载超时，按 `$libTV` 经验清理半截文件后重试，必要时用媒体 URL 直下。

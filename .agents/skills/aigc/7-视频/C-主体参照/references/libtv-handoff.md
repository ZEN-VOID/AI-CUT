# LibTV Handoff

本文件定义 step3：根据完整分镜组内容和主体参照，调用 `.agents/skills/cli/libTV` 完成组级视频生成。C 叶子负责主体槽位和 prompt 组装；`$libTV` 负责上传本地参照图、创建会话、查询和下载。

## Required Skill Dependency

提交或查询前必须加载：

```text
.agents/skills/cli/libTV/SKILL.md
.agents/skills/cli/libTV/CONTEXT.md
```

并确认当前命令环境存在 `LIBTV_ACCESS_KEY`。不得把 key 写入任何项目文件。

## Command Selection

| reference state | command | rule |
| --- | --- | --- |
| `bound_images` | `libtv_session_with_uploaded_references` | 一张或多张主体图片；先上传本地图片，再把 OSS URL 追加到对应主体信息后 |
| `visual_resolved` | `libtv_session_with_uploaded_references` | 多候选已通过窗口图像上下文识图消歧，按最终选中的图片上传 |
| `no_images` | `libtv_session_text_only` | 无可用主体图，使用纯文本 prompt，不传空图片 |
| `ambiguous` | blocked | 视觉消歧仍无法唯一确定，或尚未把候选图作为可加载上下文完成识图前不得提交 |
| `auth_or_script_failed` | blocked | `LIBTV_ACCESS_KEY` 或 `$libTV` 脚本不可用时只写计划和 blocked queue row |

## Default Parameters

- `requested_model`: 默认为空，表示使用 LibTV 后端默认视频路由。用户显式指定模型时，原样写入自然语言任务。
- `duration_hint`: 默认 `15` 秒，作为自然语言要求发送给 LibTV。
- `ratio_hint`: 默认 `16:9`。
- `video_resolution_hint`: 默认 `720p`，即用户可见规格 720P。
- `poll_seconds`: 默认短轮询 `45` 秒；超时后保留 `sessionId` 并进入 queue ledger。
- `parallelism`: 默认后台多线程批量并发；实际值应记录在 submit plan，建议从 `2` 到 `4` 起步，避免上传带宽不稳。

## Submit Plan Shape

`第N集-libtv-submit-plan.json` 至少包含：

```json
{
  "project_name": "诡校-测试版",
  "episode_id": "第1集",
  "output_root": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集",
  "parallelism": 3,
  "libtv_self_check": {
    "required_env": "LIBTV_ACCESS_KEY",
    "status": "pending"
  },
  "tasks": [
    {
      "queue_id": "第1集-1-1-1",
      "group_id": "1-1-1",
      "command": "libtv_session_with_uploaded_references",
      "requested_model": "",
      "duration_hint": 15,
      "ratio_hint": "16:9",
      "video_resolution_hint": "720p",
      "prompt_path": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/prompts/1-1-1.txt",
      "images": [
        {
          "upload_index": 1,
          "name": "林寂",
          "category": "character",
          "path": "projects/aigc/诡校-测试版/5-设计/角色/3-生成/林寂-多视图.png",
          "uploaded_url": "",
          "subject_inline": "林寂 参照图1"
        }
      ],
      "download_dir": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/videos",
      "expected_output": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/videos/1-1-1.mp4"
    }
  ]
}
```

## Script Rendering

有参照图：

```bash
python3 .agents/skills/cli/libTV/scripts/upload_file.py "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png"
python3 .agents/skills/cli/libTV/scripts/upload_file.py "projects/aigc/<项目名>/5-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png"
python3 .agents/skills/cli/libTV/scripts/create_session.py "$(cat projects/aigc/<项目名>/7-视频/C-主体参照/第N集/prompts/1-1-1.txt)"
```

prompt 文件中必须包含上传后的 URL，例如：

```text
林寂：参照图1 <uploaded_url>
永夜私立中学二年级A班教室：参照图2 <uploaded_url>
```

无参照图：

```bash
python3 .agents/skills/cli/libTV/scripts/create_session.py "$(cat projects/aigc/<项目名>/7-视频/C-主体参照/第N集/prompts/1-1-1.txt)"
```

## Queue Ledger

任何提交、排队或待下载任务都必须写入 `第N集-libtv-queue.md`：

| queue_id | group_id | command | sessionId | projectUuid | local_status | remote_status | last_checked_at | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

`sessionId` 缺失时该行状态只能是 `planned`、`blocked` 或 `submit_failed`。

## Concurrency Rules

- 并发只发生在 LibTV 上传、创建会话或查询层；`group-index`、`reference-manifest` 和最终 `执行报告.md` 必须串行汇流写入。
- 每个 worker 只能处理自己的 `queue_id`，不得改写其他组的 prompt 或结果。
- 若并发提交任一组失败，不影响其他组继续，但最终报告必须列出失败组和重试命令。

## Gate

通过 LibTV handoff 必须满足：

1. 提交前有 `LIBTV_ACCESS_KEY` 自检策略或实际结果。
2. 每个 runnable group 有合法命令和非空 prompt。
3. 有参照图时 `images[]` 本地路径都存在，且已记录 `uploaded_url` 或上传失败原因。
4. 无参照图时命令为 `libtv_session_text_only`，不传空图片槽。
5. 任务状态可通过 queue ledger 续查。

# Dreamina Handoff Contract

本文件定义 step3：根据完整分镜组内容和主体参照，调用 `.agents/skills/cli/dreamina-cli` 完成组级视频生成。

## Required Skill Dependency

提交或查询前必须加载：

```text
.agents/skills/cli/dreamina-cli/SKILL.md
.agents/skills/cli/dreamina-cli/CONTEXT.md
```

并执行其强制自检：

```bash
dreamina user_credit
```

## Command Selection

| reference state | Dreamina command | rule |
| --- | --- | --- |
| `bound_images` | `dreamina multimodal2video` | 一张或多张主体图片，prompt 必须在对应主体信息后追加 `@<图片路径>` |
| `no_images` | `dreamina text2video` | 无可用主体图，使用纯文本 prompt，不传空图片 |
| `ambiguous` | blocked | 参照歧义未解决前不得提交 |
| `auth_or_cli_failed` | blocked | 登录或 CLI 自检失败时只写计划和 blocked queue row |

## Default Parameters

- `model_version`: 默认 `seedance2.0`；若当前 CLI help 不支持，降级到 `seedance2.0fast` 并记录原因。
- `duration`: 默认 `15`。
- `ratio`: 默认 `16:9`。
- `video_resolution`: 默认 `720p`。
- `poll`: 默认短轮询 `45` 秒；超时后保留 submit_id 并进入 queue ledger。
- `parallelism`: 默认后台多线程批量并发；实际值应记录在 submit plan，建议从 `2` 到 `4` 起步，避免登录态或上传带宽不稳。

## Submit Plan Shape

`第N集-dreamina-submit-plan.json` 至少包含：

```json
{
  "project_name": "诡校-测试版",
  "episode_id": "第1集",
  "output_root": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集",
  "parallelism": 3,
  "tasks": [
    {
      "queue_id": "第1集-1-1-1",
      "group_id": "1-1-1",
      "command": "multimodal2video",
      "model_version": "seedance2.0",
      "duration": 15,
      "ratio": "16:9",
      "video_resolution": "720p",
      "prompt_path": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/prompts/1-1-1.txt",
      "images": [
        {
          "upload_index": 1,
          "name": "林寂",
          "category": "character",
          "path": "projects/aigc/诡校-测试版/5-设计/角色/3-生成/林寂-多视图.png",
          "subject_inline": "林寂 @projects/aigc/诡校-测试版/5-设计/角色/3-生成/林寂-多视图.png"
        }
      ],
      "download_dir": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/videos",
      "expected_output": "projects/aigc/诡校-测试版/7-视频/C-主体参照/第1集/videos/1-1-1.mp4"
    }
  ]
}
```

## CLI Command Rendering

有参照图：

```bash
dreamina multimodal2video \
  --image "projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png" \
  --image "projects/aigc/<项目名>/5-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png" \
  --prompt "$(cat projects/aigc/<项目名>/7-视频/C-主体参照/第N集/prompts/1-1-1.txt)" \
  --model_version=seedance2.0 \
  --duration=15 \
  --ratio=16:9 \
  --video_resolution=720p \
  --poll=45
```

无参照图：

```bash
dreamina text2video \
  --prompt "$(cat projects/aigc/<项目名>/7-视频/C-主体参照/第N集/prompts/1-1-1.txt)" \
  --model_version=seedance2.0 \
  --duration=15 \
  --ratio=16:9 \
  --video_resolution=720p \
  --poll=45
```

## Queue Ledger

任何提交、排队或待下载任务都必须写入 `第N集-dreamina-queue.md`：

| queue_id | group_id | command | submit_id | local_status | remote_status | last_checked_at | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |

`submit_id` 缺失时该行状态只能是 `planned`、`blocked` 或 `submit_failed`。

## Concurrency Rules

- 并发只发生在 Dreamina 提交或查询层；`group-index`、`reference-manifest` 和最终 `执行报告.md` 必须串行汇流写入。
- 每个 worker 只能处理自己的 `queue_id`，不得改写其他组的 prompt 或结果。
- 若并发提交任一组失败，不影响其他组继续，但最终报告必须列出失败组和重试命令。

## Gate

通过 Dreamina handoff 必须满足：

1. 提交前有 `dreamina user_credit` 自检策略或实际结果。
2. 每个 runnable group 有合法命令和非空 prompt。
3. 有参照图时 `images[]` 路径都存在，且 prompt 对应主体信息后有 `@<图片路径>`。
4. 无参照图时命令为 `text2video`，不传空图片槽。
5. 任务状态可通过 queue ledger 续查。

# Dreamina Handoff Contract

本文件定义 step3：把完整分镜组内容和可选多张分镜画面参照图准确转化为符合 `.agents/skills/cli/dreamina-cli` 的提交格式，并以分镜组为单位默认后台多线程批量并发执行。

## Required Dreamina Preflight

每次执行生成前必须：

1. 加载 `.agents/skills/cli/dreamina-cli/SKILL.md + CONTEXT.md`。
2. 运行 `dreamina --help` 或确认 binary 已可用。
3. 运行 `dreamina user_credit`；失败则停止提交。
4. 创建或打开本集 queue ledger：`第N集-dreamina-queue.md`。

## YAML Job Schema

每个分镜组一个 job：

```yaml
- group_id: "1-1-1"
  command_type: "multimodal2video"
  prompt: "<完整 Dreamina prompt>"
  reference_images:
    - shot_id: "1-1-1-1"
      path: "projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-1.png"
      marker: "@图1"
      role: "storyboard_frame"
  dreamina:
    model_version: "seedance2.0_vip"
    duration: 10
    ratio: "16:9"
    video_resolution: "720p"
    poll: 45
  output:
    expected_video_path: "projects/aigc/<项目名>/7-视频/A-分镜画面参照/第1集/videos/1-1-1.mp4"
```

## Command Selection

| reference state | command_type | command projection |
| --- | --- | --- |
| `reference_images` 非空 | `multimodal2video` | `dreamina multimodal2video --image <path1> --image <path2> ... --prompt "<@图N...>" --model_version=<model> --duration=<sec> --ratio=<ratio> --video_resolution=720p --poll=<sec>` |
| `reference_images` 为空 | `text2video` | `dreamina text2video --prompt "<完整组内容>" --model_version=<model> --duration=<sec> --ratio=<ratio> --video_resolution=720p --poll=<sec>` |
| `reference_images` 超过当前 CLI 上限 | `blocked` / `split_by_user_policy` | 不静默丢图；按用户策略阻断、分段或降级，并写入 report |

默认值遵循 `dreamina-cli` 当前矩阵与本视频阶段 VIP 优先规则：

- `multimodal2video`: 未显式指定模型时使用 `model_version=seedance2.0_vip`。
- `text2video`: 未显式指定模型时使用 `model_version=seedance2.0_vip`。
- 仅当用户显式指定其他模型 / fast 档 / 非 VIP 路线时，才可改用 `seedance2.0`、`seedance2.0fast` 或 `seedance2.0fast_vip`。
- 若当前 `dreamina <subcommand> -h` 未暴露 `seedance2.0_vip`，先提示更新或切换到新版 Dreamina CLI；不得静默降级。
- `duration`: 默认 10 秒，必须在 Dreamina 当前允许范围内。
- `ratio`: 默认 `16:9`，除非项目或用户指定竖屏。
- `video_resolution`: 默认 `720p`。
- `poll`: 默认 45 秒；超时不视为失败，转 queue 查询。

## Prompt Projection

有参照图时，prompt 必须包含：

```text
根据以下完整分镜组内容生成一条连续视频。保持分镜顺序、角色动作、镜头运动、场景与情绪连续；不生成字幕，不生成BGM，保留物理互动音效与环境音。

以下分镜画面图仅作为镜级视觉参照，用于画面连续性、角色位置、构图、镜头顺序和关键动作参考；不得把任一图片当作唯一首帧，不得覆盖以下完整分镜组内容：
@图1 = 1-1-1-1@projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-1.png
@图2 = 1-1-1-2@projects/aigc/<项目名>/6-图像/A-分镜画面/第1集/images/1-1-1-2.png

<直接粘贴 projects/aigc/<项目名>/4-分组/第N集.md 中该分镜组的完整现有内容>
```

无参照图时，prompt 直接使用固定视频约束前缀加完整分镜组内容。

## Background Concurrency

- 默认 `background: true`。
- 默认 worker 数：`min(4, job_count)`；用户可显式降低或提高，但不得超过 Dreamina CLI、账号配额和本机 I/O 可承受范围。
- 每个 worker 只提交自己的 group job，并写入独立临时结果，例如 `.tmp/<group_id>.result.json`。
- 主流程负责单线程汇总 queue ledger、results JSON 和 `执行报告.md`。
- 任一 job 失败不应抹掉其他 job 的 `submit_id`；失败组记录 `failed` 与 rework entry。

## Queue And Download

- 每个成功提交的 job 必须记录 `submit_id`。
- `--poll` 超时后必须标记 `querying` 或 `queued`，并写 `next_action`。
- 查询使用 `dreamina query_result --submit_id=<id>`。
- 下载目录固定为：

```text
projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/videos/
```

- 若远端成功但下载超时，按 `dreamina-cli` 经验清理半截文件后重试，必要时用媒体 URL 直下。

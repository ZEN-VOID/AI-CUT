# Dreamina Handoff Contract

本文件定义 step3：把完整分镜组内容和可选故事板参照图准确转化为符合 `.agents/skills/cli/dreamina-cli` 的提交格式，并以分镜组为单位默认后台多线程批量并发执行。

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
    - path: "projects/aigc/<项目名>/6-图像/B-分镜故事板/第1集/images/1-1-1.png"
      marker: "@图1"
      role: "storyboard_sheet"
  dreamina:
    model_version: "seedance2.0fast"
    duration: 10
    ratio: "16:9"
    video_resolution: "720p"
    poll: 45
  output:
    expected_video_path: "projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第1集/videos/1-1-1.mp4"
```

## Command Selection

| reference state | command_type | command projection |
| --- | --- | --- |
| `reference_images` 非空 | `multimodal2video` | `dreamina multimodal2video --image <path> --prompt "<@图1...>" --model_version=<model> --duration=<sec> --ratio=<ratio> --video_resolution=720p --poll=<sec>` |
| `reference_images` 为空 | `text2video` | `dreamina text2video --prompt "<完整组内容>" --model_version=<model> --duration=<sec> --ratio=<ratio> --video_resolution=720p --poll=<sec>` |

默认值遵循 `dreamina-cli` 当前矩阵：

- `multimodal2video`: `model_version=seedance2.0fast` 或用户显式指定的 `seedance2.0`。
- `text2video`: `model_version=seedance2.0fast` 或用户显式指定的 `seedance2.0`。
- `duration`: 默认 10 秒，必须在 Dreamina 当前允许范围内。
- `ratio`: 默认 `16:9`，除非项目或用户指定竖屏。
- `video_resolution`: 默认 `720p`。
- `poll`: 默认 45 秒；超时不视为失败，转 queue 查询。

## Prompt Projection

有参照图时，prompt 必须包含：

```text
@图1 是该分镜组的多格分镜故事板视觉参照，只用于画面连续性、镜头顺序、构图节奏和角色位置参考；不得把故事板图当作首帧，也不得覆盖以下完整分镜组内容。

<完整分镜组内容>
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
projects/aigc/<项目名>/7-视频/B-分镜故事板参照/第N集/videos/
```

- 若远端成功但下载超时，按 `dreamina-cli` 经验清理半截文件后重试，必要时用媒体 URL 直下。

# AIGC Image Generation Execution Contract

本文件是 AIGC 工作流内图像生成执行模式的共享真源，覆盖：

- `.agents/skills/aigc/4-Design/2-设计`
- `.agents/skills/aigc/4-Design/3-面板`
- `.agents/skills/aigc/5-Image/3-图像生成`

## Default Mode

所有可进入真实 provider 的图像生成动作，默认采用：

```json
{
  "execution_mode": "background-batch-concurrent",
  "max_concurrent": 100,
  "provider": "nano-banana/general 或已选 provider",
  "request_sidecar_required": true,
  "foreground_override": "--foreground"
}
```

含义：

1. 先写稳定 request sidecar，再提交 provider。
2. 多任务统一写成 `{ "tasks": [...] }` 批量请求。
3. 默认后台提交，不阻塞上游设计、面板或 submit-plan 写回。
4. 默认最大并发为 `100`；provider 执行层仍可按自身硬上限钳制。
5. 用户显式要求等待结果、排查失败或做最终验收时，才使用 `--foreground` 前台等待。

## Required Trace Fields

凡以后台模式提交，manifest、bridge report 或 submit-plan 至少记录：

| field | requirement |
| --- | --- |
| `execution_mode` | 固定为 `background-batch-concurrent` |
| `status` | 提交成功后写 `background_submitted`，不得伪装为图片已完成 |
| `request_batch_path` | 指向本轮 `{ "tasks": [...] }` request sidecar |
| `max_concurrent` | 默认 `100` 或用户显式覆盖值 |
| `background_pid` | 本地后台进程 pid；非本地 provider 可写 provider task id |
| `background_log` | 本地后台 stdout/stderr 日志路径 |
| `output_dir / expected_outputs` | provider 结果应回填的 canonical 输出目录或文件清单 |

## Stage Rules

| stage | request sidecar | default behavior | completion meaning |
| --- | --- | --- | --- |
| `4-Design/2-设计` | `2-设计/第N集/generated/requests/design_auto_image_batch.json` | 批量提交所有缺同 stem 图片的设计 Markdown | `background_submitted` 表示已提交；图片完成需后续按同 stem 文件复核 |
| `4-Design/3-面板` | `3-面板/第N集/generated/requests/panel_auto_generate_batch.json` | layout JSON 先落盘，再后台批量并发提交 panel 图 | `background_submitted` 表示已提交；layout/request 为当前可验收真源 |
| `5-Image/3-图像生成` | `submit-plan.json` 内的 provider request section | submit-plan 默认声明后台批量并发执行参数 | 本层完成表示 handoff 包稳定，不等于 provider 已产图 |

## Overrides

- `--foreground`：前台等待 provider 完成，用于最终验收、故障复现或必须同步拿图的人工任务。
- `--layout-only / --json-only / --request-only`：只写 layout/request/bridge report，不提交 provider。
- `--dry-run / --generation-dry-run`：构造 request 并打印或验证 payload，不真实调用 provider。
- `--max-concurrent <N>`：允许用户覆盖默认并发，但执行层必须遵守 provider 硬上限。

## Hard Gates

1. 后台提交成功只能写 `background_submitted`，不得写成 `success/generated/completed` 来暗示图片已经存在。
2. 若 request sidecar 未写出，不得启动后台 provider。
3. 若后台进程启动失败，必须返回非零或把 manifest 状态写为 `failed`。
4. 后续阶段若必须消费真实图片，必须检查本地输出文件或 provider report，而不是只看 `background_submitted`。

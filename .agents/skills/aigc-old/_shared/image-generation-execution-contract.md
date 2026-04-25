# AIGC Image Generation Execution Contract

本文件是 AIGC 工作流内图像生成执行模式的共享真源，覆盖：

- `.agents/skills/aigc/4-Design/场景`
- `.agents/skills/aigc/4-Design/角色`
- `.agents/skills/aigc/4-Design/道具`
- `.agents/skills/aigc/5-Image/3-图像生成`

## Default Mode

所有可进入真实图像生成的动作，默认采用：

```json
{
  "execution_mode": "codex-builtin-imagegen",
  "max_concurrent": 1,
  "provider_skill": "imagegen",
  "provider_mode": "built-in image_gen",
  "default_model": "GPT-IMAGE-2",
  "request_sidecar_required": true,
  "project_copy_required": true
}
```

含义：

1. 先写稳定 request sidecar，再由 Codex 会话调用内置 `image_gen` 工具。
2. 多任务仍统一写成 `{ "tasks": [...] }` 批量请求，作为逐张调用内置 `image_gen` 的执行清单。
3. 内置 `image_gen` 默认按 `GPT-IMAGE-2` 模型口径完成生成；不要求 `OPENAI_API_KEY`，不得默认改走 API / CLI provider。
4. 内置工具默认把原图保存到 `$CODEX_HOME/generated_images/...`；项目资产必须复制回 request sidecar 声明的 `output_dir/output_filename`，并保留原始生成文件。
5. API / CLI / nano-banana / anyfast 只允许作为用户显式要求的 fallback，不得作为 `4-Design/场景`、`4-Design/角色`、`4-Design/道具` 或 `5-Image/3-图像生成` 的默认生图路径。

## Required Trace Fields

凡准备或执行内置 imagegen，manifest、bridge report 或 submit-plan 至少记录：

| field | requirement |
| --- | --- |
| `execution_mode` | 固定为 `codex-builtin-imagegen` |
| `provider_skill` | 固定为 `imagegen` |
| `provider_mode` | 固定为 `built-in image_gen` |
| `default_model` | 固定为 `GPT-IMAGE-2` |
| `status` | 侧车已写但图片未复制回项目时写 `request_ready`，不得伪装为图片已完成 |
| `request_batch_path` | 指向本轮 `{ "tasks": [...] }` request sidecar |
| `generated_source_path` | 内置工具生成后的 `$CODEX_HOME/generated_images/...` 原始文件路径；未生成前可为空 |
| `output_dir / expected_outputs` | provider 结果应回填的 canonical 输出目录或文件清单 |

## Stage Rules

| stage | request sidecar | default behavior | completion meaning |
| --- | --- | --- | --- |
| `4-Design/{场景,角色,道具}` 设计图 | `4-Design/generated/requests/design_auto_image_batch.json` | 汇总所有缺同 stem 图片的设计 Markdown，逐张调用内置 `image_gen` 后复制回同目录同 stem 图片 | `request_ready` 只表示可生图；图片完成必须按同 stem 文件复核 |
| `4-Design/{场景,角色,道具}` 面板图 | `4-Design/generated/requests/panel_auto_generate_batch.json` | `[主体名].json` 面板提示词先落盘，再按 request sidecar 逐张调用内置 `image_gen` 生成 panel 图 | `request_ready` 只表示可生图；面板提示词/request 为当前可验收真源 |
| `5-Image/3-图像生成` | `submit-plan.json` 内的 provider request section | submit-plan 默认声明内置 imagegen 执行参数 | 本层完成表示 handoff 包稳定，不等于图片已复制回项目 |

## Overrides

- `--foreground`：兼容旧参数；内置 `image_gen` 本身由 Codex 会话前台调用。
- `--layout-only / --json-only / --request-only`：只写 layout/request/bridge report，不提交 provider。
- `--dry-run / --generation-dry-run`：构造 request 并打印或验证 payload，不调用内置 `image_gen`。
- `--max-concurrent <N>`：兼容旧参数；内置 `image_gen` 对多主体仍按一个资产一次调用处理。

## Hard Gates

1. request sidecar 写出但内置 `image_gen` 尚未完成时只能写 `request_ready`，不得写成 `success/generated/completed` 来暗示图片已经存在。
2. 若 request sidecar 未写出，不得调用内置 `image_gen`。
3. 若内置 `image_gen` 生成失败或无法复制回项目路径，必须把 manifest 状态写为 `failed` 并保留请求侧车。
4. 后续阶段若必须消费真实图片，必须检查本地输出文件，而不是只看 `request_ready`。
5. 除非用户显式要求 fallback，`4-Design/场景`、`4-Design/角色`、`4-Design/道具` 与 `5-Image/3-图像生成` 不得默认调用 `.agents/skills/api/anyfast/image/nano-banana/general`、`nano_banana_generate.py` 或任何需要 API key 的远端脚本。

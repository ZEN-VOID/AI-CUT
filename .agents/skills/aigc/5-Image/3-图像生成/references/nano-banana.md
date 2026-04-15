# 5-Image / 3-图像生成 / NANO-banana 模块

## 目标 provider

- handoff skill: `.agents/skills/api/image/nano-banana/SKILL.md`

## 固定输入语义

1. 图片引用最终按 `BASE64-compatible` 形态交付
2. 若 `provider_variants.nano_banana.resolution_status=pending_encode`，本层必须在 submit-plan 中显式写清“执行前编码”
3. 若已是合法 data URL / BASE64，可直接标记 `ready`

## submit-plan 最低要求

- `provider = nano_banana`
- `input_mode = base64_compatible`
- `provider_input_resolution` 写清：
  - 哪些引用已 ready
  - 哪些引用需由执行层从本地路径编码为 BASE64
- `output_dir` 写成 `projects/aigc/<项目名>/5-Image/3-图像生成/nano_banana/<source_tranche>/<第N集>/`
- `expected_outputs[]` 或执行后 `result_outputs[]` 中的本地图片路径必须与 `submit-plan.json` 同目录
- `execution` 必须继承 `.agents/skills/aigc/_shared/image-generation-execution-contract.md`：
  - `execution_mode = background-batch-concurrent`
  - `max_concurrent = 100`
  - `status_after_submit = background_submitted`
  - `foreground_override = --foreground`
  - `request_batch_path` 指向本目录内 provider-ready `{ "tasks": [...] }` sidecar 或 submit-plan 内等价 batch section
- `next_entry = .agents/skills/api/image/nano-banana/SKILL.md`

## 审计点

- 不伪造 BASE64
- 不把 `pending_encode` 误写成 ready
- 不把后台提交态误写成真实图片已完成
- 真实输出图像下载或规范化到 submit-plan 所在目录，不以 API 临时响应、远程 URL 或缓存路径作为 canonical 路径
- 下一入口唯一且明确

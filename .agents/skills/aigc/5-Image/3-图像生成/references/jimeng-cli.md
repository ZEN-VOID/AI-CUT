# 5-Image / 3-图像生成 / 即梦 CLI 模块

## 目标 provider

- handoff skill: `.agents/skills/cli/dreamina-cli/SKILL.md`

## 固定输入语义

1. 图片引用最终必须解析为本地路径
2. `image_markers[].provider_variants.jimeng_cli.resolution_status` 应为 `ready`
3. 若请求对象是 prompt-only，可不消费引用图

## submit-plan 最低要求

- `provider = jimeng_cli`
- `input_mode = local_path_direct`
- `provider_input_resolution` 写清使用哪些本地图片路径
- `output_dir` 写成 `projects/aigc/<项目名>/5-Image/3-图像生成/jimeng_cli/<source_tranche>/<第N集>/`
- `expected_outputs[]` 或执行后 `result_outputs[]` 中的本地图片路径必须与 `submit-plan.json` 同目录
- `execution` 必须继承 `.agents/skills/aigc/_shared/image-generation-execution-contract.md`：
  - `execution_mode = background-batch-concurrent`
  - `max_concurrent = 100`
  - `status_after_submit = background_submitted`
  - `foreground_override = --foreground`
  - `request_batch_path` 指向本目录内 provider-ready 批量提交 sidecar 或 submit-plan 内等价 batch section
- `next_entry = .agents/skills/cli/dreamina-cli/SKILL.md`

## 审计点

- 不出现 URL / BASE64 作为 Dreamina 最终图片输入
- 如果引用驱动，则路径真实可读
- 不把后台提交态误写成真实图片已完成
- 真实输出图像下载或规范化到 submit-plan 所在目录，不以 Dreamina 临时缓存作为 canonical 路径
- 最终下一入口唯一

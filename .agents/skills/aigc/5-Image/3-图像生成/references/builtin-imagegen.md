# 5-Image / 3-图像生成 / 内置 Image Gen 模块

## Role

本模块是 `3-图像生成` 的默认执行模块。除非用户显式要求 API / CLI / NANO-banana / 即梦 CLI fallback，本层默认锁定：

- `provider = builtin_image_gen`
- `provider_skill = imagegen`
- `provider_mode = built-in image_gen`
- `default_model = GPT-IMAGE-2`
- `execution_mode = codex-builtin-imagegen`

## Handoff Contract

1. 先写 `request-batch.json + submit-plan.json + submit-brief.md`。
2. `submit-plan.json` 中 `status` 写 `request_ready`，不得伪装为图片已生成。
3. 按 `request-batch.json.tasks[]` 逐张调用内置 `image_gen`。
4. 内置工具生成的原图保留在 `$CODEX_HOME/generated_images/...`。
5. 项目可消费图片必须复制回 `submit-plan.output_dir` 下的 `expected_outputs[]` 位置。
6. 复制回项目后，执行层回填 `result_outputs[]`，记录 `generated_source_path` 与项目输出路径。

## Reference Handling

- `prompt_only` 请求可直接进入内置 Image Gen。
- 若请求包含本地 reference image，执行前必须让引用图在当前会话中可见，或明确记录为需要人工可见引用准备；不得把裸本地路径当作内置工具已经消费的图片。
- 若需要严格路径直传或 BASE64 运输层，必须显式切到 `jimeng_cli` 或 `nano_banana` fallback。

## Output Gate

- canonical 输出目录必须是 `projects/aigc/<项目名>/5-Image/3-图像生成/builtin_image_gen/<source_tranche>/<第N集>/`。
- `$CODEX_HOME/generated_images/...` 只能作为原始生成证据，不是项目 canonical 输出。
- `Assets/` 只能接收派生副本，不得替代 submit 包同目录输出。

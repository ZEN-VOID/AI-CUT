# Provider Modules

## builtin_image_gen

- 默认 provider。
- `provider_skill = imagegen`
- `default_model = GPT-IMAGE-2`
- `execution_mode = codex-builtin-imagegen`
- `max_concurrent = 1`
- 内置工具生成的原图路径只作为生成证据，项目 canonical 图片必须复制回 `submit-plan.output_dir`。
- 若请求包含本地 reference image，执行前必须让引用图在当前会话中可见，或在 brief 中写明人工可见引用准备。

## jimeng_cli

- handoff skill: `.agents/skills/cli/dreamina-cli/SKILL.md`
- 最终图片输入只能是本地路径。
- 不得把 URL、BASE64 或占位路径写入 `resolved_input`。
- 外部 provider 执行可使用后台批量并发，submit-plan 必须区分 `background_submitted` 与真实图片完成。

## nano_banana

- handoff skill: `.agents/skills/api/anyfast/image/nano-banana/SKILL.md`
- 最终图片输入按 BASE64-compatible 形态交付。
- 若 `provider_variants.nano_banana.resolution_status=pending_encode`，submit-plan 必须写明执行前编码。
- 不得伪造 BASE64，不得把远程 URL 当作项目 canonical 图片。

## Provider Gate

provider 不唯一时只允许输出推荐主案、备选案和缺口。只有 provider 唯一时，才允许生成最终 `submit-plan.json`。

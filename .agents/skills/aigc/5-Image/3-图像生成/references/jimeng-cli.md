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
- `next_entry = .agents/skills/cli/dreamina-cli/SKILL.md`

## 审计点

- 不出现 URL / BASE64 作为 Dreamina 最终图片输入
- 如果引用驱动，则路径真实可读
- 最终下一入口唯一


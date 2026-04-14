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
- `next_entry = .agents/skills/api/image/nano-banana/SKILL.md`

## 审计点

- 不伪造 BASE64
- 不把 `pending_encode` 误写成 ready
- 下一入口唯一且明确


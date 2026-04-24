# Provider Modules

## Built-In Image Gen

- 默认模型口径：`GPT-IMAGE-2`。
- 默认执行模式：`codex-builtin-imagegen`。
- 不要求 API key。
- request ready 不等于图片已生成成功；真实图片必须复制或回填到 submit 包同目录。

## 即梦 CLI

- 只接受本地路径作为图片引用。
- 不得把 URL 或 BASE64 写入即梦 CLI handoff。
- 适合用户显式要求 CLI 提交、排队或复用本地图片路径时使用。

## NANO-banana

- 最终需要 BASE64-compatible 输入承载。
- 兼容态可写 `pending_encode`，由 provider 执行前完成编码。
- 不得提前写伪 BASE64。

## Provider-Neutral Rule

不论 provider 如何选择，`reference_images / image_markers` 的 provider-neutral 字段都不得被删除。provider-specific 信息只能写入变体或 handoff 解析说明。

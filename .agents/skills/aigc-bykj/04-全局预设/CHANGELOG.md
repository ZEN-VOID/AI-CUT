# CHANGELOG

## 2026-05-29

- 初始化 `04-全局预设` 整合型 skill。
- 增加三种主模式：指定风格、参考图解析还原、从 `02-剧本处理` 全本剧本自动解析。
- 增加 300-500 字 `global_style_prompt` 输出要求，并对齐 `.agents/skills/aigc` 的 `north_star.yaml` 全局风格口径。
- 增加 `global_style_collection`，将全局风格建模为包含组别与设计主体的总集合。
- 全量补强图片参考模式：单/多图权重、逐图证据、冲突处理、可迁移边界和 `do_not_import` 去污染审计。
- 全量补强自动解析模式：`02` 全本覆盖、组别候选、设计主体候选、置信度与证据不足退化。
- 内置参考图 12 维视觉风格解析协议。
- 固定统一 JSON schema、`visual_styles.json` 风格库、执行报告和 manifest 输出。
- 固定 canonical 输出目录为 `output/[项目名]/04-全局预设/`。

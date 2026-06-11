# Polishing Mode Map

本文件辅助 `story-polishing` 判定润色任务模式；主路由仍以根 `SKILL.md` 为准。

| mode | trigger | scope rule | gate |
| --- | --- | --- | --- |
| `chapter_polish` | 首次从 `3-初稿` 生成 `4-润色` | 默认最小局部修补 | 不改核心事实 |
| `polish_rewrite` | 用户明确要求重润、覆盖、整章重写 | 允许扩大范围，但必须保留 source anchor | 覆盖授权明确 |
| `local_repair` | 局部坏点、内置验收 finding、AI 腔或中文表达问题 | 只修 affected span 与必要上下文 | diff 可解释 |
| `acceptance_repair` | 用户显式要求分维度审计并直接优化，或终稿验收 FAIL | 验收 findings 进入 repair brief | 不允许只审不改 |
| `dry_run` | 只装配或诊断上下文 | 不写正文 | 输出缺口清单 |

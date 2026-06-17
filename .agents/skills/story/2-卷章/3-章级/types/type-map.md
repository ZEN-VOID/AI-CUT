# Type Package Map

本文件是 `story-plan-chapter-level` 的 canonical 类型包入口。执行时先读取本文件，再加载命中的固定上下文文件；章级规划类型与爽点类型分别由同目录专项包承载。

## Selection Index

| field | meaning |
| --- | --- |
| `package_id` | 稳定类型包 ID |
| `path` | 类型包入口文件或目录 |
| `match_signals` | 用户输入、产物状态、题材画像或任务模式的命中信号 |
| `load_mode` | `exclusive`、`stackable` 或 `fallback` |
| `context_files` | 执行时固定加载的文件 |
| `conflicts_with` | 互斥类型包 |
| `inherits_from` | 上层类型包 |

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `chapter-planning-core` | `types/chapter-planning-type-map.md` | 新建、修订或审查 `第N章.md`；需要形成 `task_mode / chapter_scope / output_type / review_type` | stackable | `types/chapter-planning-type-map.md` | none | none |
| `payoff-genre-profile` | `types/payoff-genre-type-map.md` | 章级爽点设计、`genre_payoff_profile`、高超对决差异轴、类型口味校准 | stackable | `types/payoff-genre-type-map.md` | none | `chapter-planning-core` |

## Default Package Rule

- 默认加载 `chapter-planning-core`。
- 当任务需要生成、修订或审查 `本章爽点设计`，或上游/用户输入包含类型画像、爽点口味、高超对决、关系/情绪/认知 payoff 时，同时加载 `payoff-genre-profile`。
- `types/` 是固定上下文加载层；`knowledge-base/` 只做按需检索，不替代本入口。

## Loading Flow

1. 读取 `types/type-map.md` 并命中 `chapter-planning-core`。
2. 按任务信号决定是否叠加 `payoff-genre-profile`。
3. 固定加载命中包的 `context_files`。
4. 由 `types/chapter-planning-type-map.md` 产出章级 `type_profile`，由 `types/payoff-genre-type-map.md` 产出 `genre_payoff_profile`。
5. 将类型画像交给 `SKILL.md` 的 `Thinking-Action Node Map` 与 `references/chapter-payoff-rules.md` 消费。
6. 交付前由 `review/review-contract.md` 检查类型分支、爽点口味和输出字段是否一致。

## Canonical Type Sources

- `types/chapter-planning-type-map.md`
- `types/payoff-genre-type-map.md`

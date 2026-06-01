# Type Package Map

本文件是 `story-plan-book-level` 的 canonical 类型包入口。执行时先读取本文件，再加载命中的固定上下文文件；业务分型细则由同目录 `book-level-type-map.md` 承载。

## Selection Index

| field | meaning |
| --- | --- |
| `package_id` | 稳定类型包 ID |
| `path` | 类型包入口文件或目录 |
| `match_signals` | 用户输入、产物状态或任务模式的命中信号 |
| `load_mode` | `exclusive`、`stackable` 或 `fallback` |
| `context_files` | 执行时固定加载的文件 |
| `conflicts_with` | 互斥类型包 |
| `inherits_from` | 上层类型包 |

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `book-level-planning-core` | `types/book-level-type-map.md` | 新建、修订、审查或修复 `整体规划.md`；需要形成 `request_type / artifact_state / input_strength / revision_scope / review_type` | stackable | `types/book-level-type-map.md` | none | none |

## Default Package Rule

- 默认加载 `book-level-planning-core`。
- 若未来拆出题材、修订范围或审查 provider 子类型包，必须先在 `Package Index` 中登记 `context_files` 后才允许被 `steps/` 消费。
- `types/` 是固定上下文加载层；`knowledge-base/` 只做按需检索，不替代本入口。

## Loading Flow

1. 读取 `types/type-map.md` 并命中 `book-level-planning-core`。
2. 固定加载 `types/book-level-type-map.md`。
3. 由 `book-level-type-map.md` 产出 `type_profile`。
4. 将 `type_profile` 交给 `steps/book-level-planning-workflow.md` 消费。
5. 交付前由 `review/review-contract.md` 检查类型分支是否与输出字段一致。

## Canonical Type Source

- `types/book-level-type-map.md`

# Type Map

每次调用本技能时，先从本入口识别 review mode，再加载专属 review 类型包。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `review_default` | `types/review-type-map.md` | checkpoint、stage acceptance、package release、repair route 聚合 | fallback | `types/review-type-map.md` | none | none |

## Default Package Rule

默认加载 `types/review-type-map.md`。review mode 必须唯一；如果用户只提供模糊质量检查请求，先锁定 checkpoint、stage 或 release scope。

## Loading Flow

1. 锁定项目根、scope_ref 和 review_mode。
2. 加载 `types/review-type-map.md` 生成 review profile。
3. 将 profile 交给 `steps/review-workflow.md` 组装 fact pack 与维度调度。
4. 交付前加载 `review/review-gate.md` 聚合 verdict 与 route。


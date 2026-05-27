# Type Map

每次调用本技能时，先从本入口识别查询类型，再加载专属查询类型包。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `query_default` | `types/query-type-map.md` | 所有项目事实、状态、产物、资产、验收、路径和制度查询 | fallback | `types/query-type-map.md` | none | none |

## Default Package Rule

默认加载 `types/query-type-map.md`。若用户同时询问状态、资产、验收和制度，先在该类型包内判定主 truth role，再按主次顺序读取证据。

## Loading Flow

1. 锁定项目根候选和用户查询目标。
2. 加载 `types/query-type-map.md` 生成 truth role。
3. 将 truth role 交给 `steps/query-workflow.md` 读取 canonical carrier。
4. 涉及完成、通过或交付时补读 `review/review-contract.md`。


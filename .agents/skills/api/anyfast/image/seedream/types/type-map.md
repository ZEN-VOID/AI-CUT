# Type Package Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `request` | `types/request/` | 默认执行、生成、提交、主流程请求 | fallback | `types/request/request.md` | none | none |
| `query` | `types/query/` | 查询、查看状态、下载、列举、解释能力 | stackable | `types/query/query.md` | none | none |
| `repair` | `types/repair/` | 报错、重试、排障、参数修复、环境修复 | stackable | `types/repair/repair.md` | none | none |

## Loading Flow

1. 根据用户输入选择 `request`、`query`、`repair` 中的一个或多个类型包。
2. 加载命中包的 `context_files` 作为固定上下文。
3. 若仍需背景经验，再从 `knowledge-base/` 按需检索。

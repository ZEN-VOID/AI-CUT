# Type Map

每次调用本技能时，先从本入口识别参考素材和阶段桥接类型，再加载专属 source 类型包。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `source_default` | `types/source-type-map.md` | 视频、截图序列、时间码描述、参考片段、阶段桥接拉片 | fallback | `types/source-type-map.md` | none | none |

## Default Package Rule

默认加载 `types/source-type-map.md`。若任务同时要求全局风格、编剧、摄影和设计桥接，可叠加输出目标，但必须保持各 owning stage 字段边界。

## Loading Flow

1. 锁定参考素材、目标项目、目标阶段和证据粒度。
2. 加载 `types/source-type-map.md` 生成 source profile 与 bridge targets。
3. 将类型画像交给 `steps/shot-by-shot-workflow.md`。
4. 输出前加载 `review/review-contract.md` 检查证据、版权和临摹边界。


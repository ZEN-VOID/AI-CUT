# Type Map

每次调用本技能时，先从本入口识别恢复类型，再加载专属恢复类型包。

## Package Index

| package_id | path | match_signals | load_mode | context_files | conflicts_with | inherits_from |
| --- | --- | --- | --- | --- | --- | --- |
| `resume_default` | `types/resume-type-map.md` | 续跑、断点恢复、治理补齐、唯一下一入口、review repair 回接 | fallback | `types/resume-type-map.md` | none | none |

## Default Package Rule

默认加载 `types/resume-type-map.md`。若请求同时包含恢复、查询、审查或修复信号，先判定是否足以给唯一下一入口；不足时转 query/review/repair 或阻断。

## Loading Flow

1. 锁定项目根和恢复意图。
2. 加载 `types/resume-type-map.md` 生成 resume profile 与 risk profile。
3. 将类型画像交给 `SKILL.md#Thinking-Action Node Map` 核对证据链。
4. 交付前加载 `review/resume-review-gate.md` 检查唯一入口和禁止动作。

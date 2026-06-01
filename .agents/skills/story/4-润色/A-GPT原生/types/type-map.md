# Type Map

本文件是 `story-polishing-gpt-native` 的类型包索引。执行时先加载本索引，再加载命中的类型包；`knowledge-base/` 只做按需检索，不替代固定类型上下文。

## Package Index

| package_id | selection_signal | context_files | loading_mode | review_gate |
| --- | --- | --- | --- | --- |
| `polishing-core` | 每次章节润色、重润、局部修复或 dry-run | `types/polishing-type-map.md` | required | `types` / `minimal_repair` |
| `guardrail-setup` | 每次执行前与写回前 | `types/guardrail-setup.md` | required | `security` / `runtime_behavior` |

## Default Package Rule

- 默认同时加载 `polishing-core` 与 `guardrail-setup`。
- 用户指定 `chapter_polish`、`polish_rewrite`、`local_repair`、`subagent_review_optimize` 或 `dry_run` 时，仍先加载 `guardrail-setup`，再让 `polishing-core` 产出 mode。
- 若用户显式要求多路线对照，本索引只负责当前 `A-GPT原生` 路线；英文序号分流由父级 `4-润色/SKILL.md` 裁决。

## Loading Flow

1. 读取 `SKILL.md + CONTEXT.md`，锁定输入、输出和 guardrails。
2. 加载本 `types/type-map.md`。
3. 加载 `types/guardrail-setup.md` 形成运行时边界。
4. 加载 `types/polishing-type-map.md` 形成 `type_profile`。
5. 将 `type_profile` 交给 `steps/chapter-polishing-workflow.md` 的 `N2-TYPE-PROFILE` 与后续节点消费。

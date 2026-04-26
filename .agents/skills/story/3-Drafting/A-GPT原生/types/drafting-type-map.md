# Drafting Type Map

本文件承载 `story-drafting-gpt-native` 的分型策略。它只负责判型和路由，不承载完整执行步骤。

## Type Variables

| variable | values | source |
| --- | --- | --- |
| `domain_type` | `story` | 固定值 |
| `artifact_type` | `markdown_chapter` | Output Contract |
| `execution_type` | `gpt_native_creative`、`dry_run` | 用户请求与 CLI 参数 |
| `topology_type` | `hybrid` | steps 拓扑 |
| `drafting_mode` | `chapter_draft`、`chapter_rewrite`、`chapter_continue`、`local_repair`、`dry_run` | 目标文件状态 + 用户意图 |
| `review_type` | `structural_validator`、`continuity_gate`、`gpt_native_evidence_gate` | review 合同 |
| `output_type` | `canonical_draft`、`context_pack`、`gpt_native_sidecar`、`repair_patch` | mode 与 gate |

## Mode Matrix

| drafting_mode | trigger | required extra input | route | review gate |
| --- | --- | --- | --- | --- |
| `chapter_draft` | 目标章不存在或用户要求起草 | 无 | `N5A-NEW-DRAFT-PROMPT` | frontmatter + heading + prose completeness |
| `chapter_rewrite` | 目标章存在且用户要求重写/大修 | 现有 `第N章.md` | `N5B-REWRITE-PROMPT` | rewritten prose still aligns with planning |
| `chapter_continue` | 目标章存在且用户要求续写/补全 | 现有 `第N章.md` 与续写边界 | `N5C-CONTINUE-PROMPT` | continuity bridge and chapter exit hook |
| `local_repair` | 用户或 review 指出局部问题 | finding / issue / rework target | `N5D-REPAIR-PROMPT` | local fix does not rewrite upstream truth |
| `dry_run` | 用户要求只装配上下文或脚本传 `--dry-run` | 无 | `N3-CONTEXT-PACK` 后停止 | context pack exists and no writeback |

## Decision Rules

1. 用户显式指定 mode 时优先遵守，但不得违反输出路径与 LLM-first 边界。
2. 若目标章不存在，默认 `chapter_draft`。
3. 若目标章存在且用户没有说明处理方式，必须先回读现稿，再按用户目标在 `chapter_rewrite` 与 `chapter_continue` 间选择；无法判断时简短追问。
4. 若输入来自 review finding，默认 `local_repair`，且不得扩大为重写整章，除非 finding 指向全章结构失效。
5. `dry_run` 不拥有正文真源写权。
6. 若用户显式要求外部 provider 生成正文，按用户意图改路由到对应 provider skill。

## Output Routing

| output_type | path | truth role |
| --- | --- | --- |
| `canonical_draft` | `projects/story/<项目名>/3-Drafting/第N卷/第N章.md` | 章节正文业务真源 |
| `context_pack` | `projects/story/<项目名>/reports/3-Drafting/gpt-native/.../*messages.json` | GPT 原生创作输入证据 |
| `gpt_native_sidecar` | `projects/story/<项目名>/reports/3-Drafting/gpt-native/.../` | GPT 原生过程证据 |
| `repair_patch` | review 或报告工件 | 辅助修复说明，不直接夺取正文真源 |

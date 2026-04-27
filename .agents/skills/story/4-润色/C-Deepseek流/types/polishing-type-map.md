# Polishing Type Map

本文件承载 `story-polishing-deepseek` 的分型策略。它只负责判型和路由，不承载完整执行步骤。

## Type Variables

| variable | values | source |
| --- | --- | --- |
| `domain_type` | `story` | 固定值 |
| `artifact_type` | `markdown_chapter` | Output Contract |
| `execution_type` | `deepseek_provider_creative`、`dry_run` | 用户请求与 CLI 参数 |
| `topology_type` | `hybrid` | steps 拓扑 |
| `polishing_mode` | `chapter_polish`、`polish_rewrite`、`local_repair`、`local_repair`、`dry_run` | 目标文件状态 + 用户意图 |
| `review_type` | `structural_validator`、`continuity_gate`、`provider_evidence_gate` | review 合同 |
| `output_type` | `canonical_draft`、`messages_pack`、`deepseek_sidecar`、`repair_patch` | mode 与 gate |

## Mode Matrix

| polishing_mode | trigger | required extra input | route | review gate |
| --- | --- | --- | --- | --- |
| `chapter_polish` | 目标章不存在或用户要求起草 | 无 | `N5A-POLISH-PROMPT` | frontmatter + heading + prose completeness |
| `polish_rewrite` | 目标章存在且用户要求重写/大修 | 现有 `第N章.md` | `N5B-REPOLISH-PROMPT` | rewritten prose still aligns with planning |
| `local_repair` | 目标章存在且用户要求续写/补全 | 现有 `第N章.md` 与续写边界 | `N5C-REPAIR-PROMPT` | continuity bridge and chapter exit hook |
| `local_repair` | 用户或 review 指出局部问题 | finding / issue / rework target | `N5D-REPAIR-PROMPT` | local fix does not rewrite upstream truth |
| `dry_run` | 用户要求只装配上下文或脚本传 `--dry-run` | 无 | `N3-CONTEXT-PACK` 后停止 | messages pack exists and no writeback |

## Decision Rules

1. 用户显式指定 mode 时优先遵守，但不得违反输出路径、provider 与 LLM-first 边界。
2. 若目标章不存在，默认 `chapter_polish`。
3. 若目标章存在且用户没有说明处理方式，必须先回读现稿，再按用户目标在 `polish_rewrite` 与 `local_repair` 间选择；无法判断时简短追问。
4. 若输入来自 review finding，默认 `local_repair`，且不得扩大为重写整章，除非 finding 指向全章结构失效。
5. `dry_run` 不拥有正文真源写权。

## Output Routing

| output_type | path | truth role |
| --- | --- | --- |
| `canonical_draft` | `projects/story/<项目名>/4-润色/第N卷/第N章.md` | 章节润色稿业务真源 |
| `messages_pack` | `projects/story/<项目名>/reports/4-润色/deepseek/.../*messages.json` | provider 输入证据 |
| `deepseek_sidecar` | `projects/story/<项目名>/reports/4-润色/deepseek/.../` | provider 过程证据 |
| `repair_patch` | review 或报告工件 | 辅助修复说明，不直接夺取正文真源 |

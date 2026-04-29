# Polishing Type Map

## 类型包加载边界

- 每次调用本技能时，必须依据本文件识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- `types/` 中命中的类型包作为固定上下文加载；`knowledge-base/` 只作为按需检索、切片或向量召回的知识库，不替代类型包。


本文件承载 `story-polishing-deepseek` 的分型策略。它只负责判型和路由，不承载完整执行步骤。

## Type Variables

| variable | values | source |
| --- | --- | --- |
| `domain_type` | `story` | 固定值 |
| `artifact_type` | `markdown_chapter` | Output Contract |
| `execution_type` | `deepseek_provider_creative`、`dry_run` | 用户请求与 CLI 参数 |
| `topology_type` | `hybrid` | steps 拓扑 |
| `polishing_mode` | `chapter_polish`、`polish_rewrite`、`local_repair`、`subagent_review_optimize`、`dry_run` | 目标文件状态 + 用户意图 |
| `review_type` | `structural_validator`、`continuity_gate`、`story_review_dimension_subagents`、`provider_evidence_gate` | review 合同 |
| `output_type` | `canonical_draft`、`messages_pack`、`deepseek_sidecar`、`repair_patch` | mode 与 gate |

## Mode Matrix

| polishing_mode | trigger | required extra input | route | review gate |
| --- | --- | --- | --- | --- |
| `chapter_polish` | 目标章不存在或用户要求生成首版修补稿 | 无 | `N5A-POLISH-PROMPT` | frontmatter + heading + minimal repair + prose completeness |
| `polish_rewrite` | 目标章存在且用户明确要求重写/大修/整章重润 | 现有 `第N章.md`、显式覆盖授权 | `N5B-REPOLISH-PROMPT` | rewritten prose is explicitly authorized and aligns with planning |
| `local_repair` | 目标章存在且用户要求续写/补全 | 现有 `第N章.md` 与续写边界 | `N5C-REPAIR-PROMPT` | continuity bridge and chapter exit hook |
| `local_repair` | 用户或 review 指出局部问题 | finding / issue / rework target | `N5D-REPAIR-PROMPT` | local fix preserves source distribution and does not rewrite upstream truth |
| `subagent_review_optimize` | 用户显式要求启用 subagents、按审计点分维度审查后直接优化 | 审计点、`story/review` registry、命中的 review 子技能 packets 或降级报告 | `N3R-REVIEW-SUBAGENT-AUDIT` -> `N5D-REPAIR-PROMPT` | dimension findings have been injected into DeepSeek messages and directly optimized |
| `dry_run` | 用户要求只装配上下文或脚本传 `--dry-run` | 无 | `N3-CONTEXT-PACK` 后停止 | messages pack exists and no writeback |

## Decision Rules

1. 用户显式指定 mode 时优先遵守，但不得违反输出路径、provider 与 LLM-first 边界。
2. 若目标章不存在，默认 `chapter_polish`，但语义是从初稿生成首版最小局部修补稿，不是凭 planning 起草新章。
3. 若目标章存在且用户没有说明处理方式，必须先回读现稿，再按用户目标在 `polish_rewrite` 与 `local_repair` 间选择；无法判断时简短追问。
4. 若输入来自 review finding，默认 `local_repair`，且不得扩大为重写整章，除非 finding 指向全章结构失效且用户确认。
5. 若用户显式要求 subagents 模式，先进入 `subagent_review_optimize`，按 `story/review` 维度子技能拆分审计点，再把 findings 作为 provider `local_repair` 的输入直接优化正文。
6. `dry_run` 不拥有正文真源写权。

## Output Routing

| output_type | path | truth role |
| --- | --- | --- |
| `canonical_draft` | `projects/story/<项目名>/4-润色/第N卷/第N章.md` | 章节修补稿业务真源 |
| `messages_pack` | 临时 provider 目录；显式 `--output-dir` 调试时才落盘 | provider 输入证据 |
| `deepseek_sidecar` | 默认不落盘；显式 `--output-dir` 调试时才生成 | provider 过程证据 |
| `repair_patch` | review 或报告工件 | 辅助修复说明，不直接夺取正文真源 |

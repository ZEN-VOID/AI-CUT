# Drafting Built-in Acceptance Contract

本文件承载 `story-drafting` 的阶段内置验收合同。它只展开 `3-初稿/SKILL.md#Built-in Acceptance Contract`，不得外包给独立 `story/review`，也不得写出父层 `review/第V卷.validation.json`。

## Acceptance Scope

| dimension | checks |
| --- | --- |
| `source_context` | 是否加载 story 根、阶段 `CONTEXT.md`、项目 MEMORY/CONTEXT、三层 planning、north_star、对象真源和监制包 |
| `structure_realization` | 本章 planning 的事件、冲突、任务、线索和伏笔是否被写成戏，而不是摘要式提到 |
| `continuity` | 同卷前文存在时是否完整承接事实、线索、关系、道具、卷目标和文气 |
| `logic_self_consistency` | 因果链、能力边界、世界规则、例外代价和 source truth 是否自洽 |
| `character_consistency` | 人物行为、动机、关系压力、成长承接、对白声口和社会身份语言是否成立 |
| `timeline` | 时间锚、事件顺序、持续时长和伏笔静默窗口是否越线 |
| `task_convergence` | 章级任务是否从属于卷级任务，支流任务是否汇聚、转挂或显式开放 |
| `prose_reader_pull` | 是否具备现场感、句群起伏、对白潜台词、心理暗流、读者牵引和章末钩子 |
| `creative_authorship` | 是否由 LLM-first 主创，脚本和模板没有生成正文 |
| `output_state` | frontmatter、标题、canonical path、验收包和状态 hook 是否正确 |

## Acceptance Packet

验收包写入 `projects/story/<项目名>/3-初稿/第N卷/第N章.acceptance.json`，至少包含：

- `acceptance_status`
- `accepted_manuscript_stage`
- `accepted_manuscript_refs`
- `dimension_results`
- `critical_issues`
- `rework_targets`
- `handoff_targets`
- `acceptance_ref`

初稿 `pass` 只授权进入 `4-润色`；`handoff_targets` 不得包含 `return`。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为当前章 candidate draft 交付，并 handoff 到 `4-润色` |
| `pass_with_followups` | 可交付，但有非阻断后续项；仍需进入 `4-润色` |
| `needs_rework` | 存在阻断问题，必须回到对应 rework target 后重新验收 |
| `blocked` | 缺少关键输入、权限或写回授权 |

## Failure Codes

| fail_code | dimension | default_rework_target |
| --- | --- | --- |
| `FAIL-DRAFT-CONTEXT` | source_context | `SKILL.md#N2-SOURCE-LOCK` / `SKILL.md#N4-SUPERVISION` |
| `FAIL-DRAFT-STRUCTURE` | structure_realization | `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-CONTINUITY` | continuity | `SKILL.md#N3-CONTINUITY` / `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-LOGIC` | logic_self_consistency | `SKILL.md#N2-SOURCE-LOCK` / `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-CHARACTER` | character_consistency | `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-TIMELINE` | timeline | `SKILL.md#N2-SOURCE-LOCK` / `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-TASK` | task_convergence | `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-PROSE-PULL` | prose_reader_pull | `SKILL.md#N5-CREATIVE-DRAFT` |
| `FAIL-DRAFT-AUTHORSHIP` | creative_authorship | `SKILL.md#LLM-First Creative Authorship Contract` |
| `FAIL-DRAFT-WRITEBACK` | output_state | `SKILL.md#N7-WRITEBACK-STATE` |

## Gate Rule

不得宣布完成：

- 缺少必需输入或未加载项目记忆/相关项目上下文。
- 缺少监制包或正式降级记录。
- planning 义务只被摘要提到，没有转成可感知的事件、关系压力或现场动作。
- 同卷前文、因果、人物、时间线或任务汇聚出现断带。
- 正文保留 planning 标题句法、执行层标签或流程术语。
- 正文缺少现场发现、读者牵引或章末钩子。
- 主要人物对白无法区分身份、关系和意图。
- 脚本以规则拼接、模板填充或启发式补写替代 LLM 主创正文。
- 输出不是 canonical path，或未同步生成 `第N章.acceptance.json`。
- 覆盖已有章节时没有授权。

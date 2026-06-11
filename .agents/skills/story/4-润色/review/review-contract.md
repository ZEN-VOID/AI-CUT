# Polishing Built-in Acceptance Contract

本文件承载 `story-polishing` 的阶段内置验收合同。它只展开 `4-润色/SKILL.md#Built-in Acceptance Contract`，不得外包给独立 `story/review`，也不得写出父层 `review/第V卷.validation.json`。

## Acceptance Scope

| dimension | checks |
| --- | --- |
| `source_anchor` | 是否读取唯一 `3-初稿` 源章、目标 `4-润色` 路径和既有目标稿状态 |
| `minimal_repair` | 是否保留初稿事实、段落骨架、句群起伏、人物声口和章末牵引 |
| `regression_structure_logic` | 润色是否损坏结构兑现、连续性、逻辑自洽、人物一致性、时间线或任务汇聚 |
| `chinese_prose` | 是否去掉明显翻译腔、说明腔、流程腔和公式化解释 |
| `genre_texture_density` | 是否保留并强化题材质感、场景密度、信息延迟、心理暗流、对白锋利度和句群节奏 |
| `anti_ai_features` | 是否定位具体 AI 腔坏点，而不是泛化洗稿 |
| `reader_pull` | 悬念、冲突压力、情绪推进、章末钩子和读者追读力是否没有弱化 |
| `creative_authorship` | 是否由 LLM-first 润色，脚本和模板没有生成正文 |
| `output_state` | frontmatter、标题、canonical path、验收包和状态 hook 是否正确 |

## Acceptance Packet

验收包写入 `projects/story/<项目名>/4-润色/第N卷/第N章.acceptance.json`，至少包含：

- `acceptance_status`
- `accepted_manuscript_stage`
- `accepted_manuscript_refs`
- `dimension_results`
- `critical_issues`
- `rework_targets`
- `handoff_targets`
- `acceptance_ref`

终稿 `pass` 必须声明 `accepted_manuscript_stage = 4-润色`，并在 `handoff_targets` 中包含 `return`。若项目显式跳过润色，则不得使用本技能伪造通过，应回到 `3-初稿` 验收包声明例外。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为当前章 accepted polished manuscript 交付，并 handoff 到 `return` |
| `pass_with_followups` | 可交付且可 handoff，但必须在验收包中记录 residual followups |
| `needs_rework` | 存在阻断问题，必须回到对应 rework target 后重新验收 |
| `blocked` | 缺少源章、权限或写回授权 |

## Failure Codes

| fail_code | dimension | default_rework_target |
| --- | --- | --- |
| `FAIL-POLISH-SOURCE` | source_anchor | `SKILL.md#P1-SOURCE-LOCK` |
| `FAIL-POLISH-SCOPE` | minimal_repair | `SKILL.md#P3-REPAIR-PLAN` |
| `FAIL-POLISH-REGRESSION` | regression_structure_logic | `SKILL.md#P3-REPAIR-PLAN` / `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-PROSE` | chinese_prose | `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-TEXTURE` | genre_texture_density | `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-AI-FEATURES` | anti_ai_features | `SKILL.md#P3-REPAIR-PLAN` / `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-READER-PULL` | reader_pull | `SKILL.md#P4-CREATIVE-POLISH` |
| `FAIL-POLISH-AUTHORSHIP` | creative_authorship | `SKILL.md#LLM-First Creative Authorship Contract` |
| `FAIL-POLISH-WRITEBACK` | output_state | `SKILL.md#P6-WRITEBACK-STATE` |

## Gate Rule

不得宣布完成：

- 缺少 `3-初稿` 源章。
- 润色改动核心事实、人物关系、因果链、时间线或章末牵引。
- 润色造成结构兑现、连续性、人物一致性或任务汇聚回退。
- 润色把初稿清洗成短句均匀、通用顺滑或摘要式文本。
- AI 腔坏点没有被具体定位，只有泛化“更自然”的洗稿口号。
- 题材质感、场景密度、信息延迟、句群节奏或追读力被磨平。
- 脚本以规则拼接、模板填充或启发式补句替代 LLM 主创正文。
- 输出不是 canonical path，或未同步生成 `第N章.acceptance.json`。
- `acceptance_status=PASS` 但 `handoff_targets` 未包含 `return`。
- 覆盖已有润色稿时没有授权。

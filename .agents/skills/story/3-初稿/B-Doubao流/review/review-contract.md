# Drafting Review Contract

本文件承载 `story-drafting-doubao` 的质量门禁和 reviewer/provider 规则。审查结论不直接改写业务真源，必须回到主技能聚合与写回规则生效。

## Review Scope

| dimension | checks |
| --- | --- |
| `context_loading` | 是否加载同目录 `CONTEXT.md`、story 根合同（`../../SKILL.md` / `../../CONTEXT.md`）、项目 `MEMORY.md` 与相关 `CONTEXT/` |
| `source_alignment` | 是否遵守三层 planning、全局卡、风格卡与 `north_star` |
| `supervision_packet` | 是否真实启动 team supervision subagents，或有上层阻断降级报告；监制包是否来自项目 `team.yaml -> roles.production.members` 或有明确补位说明；是否包含请教问题、顾问回答摘要、可执行指导；是否进入 Doubao messages |
| `continuity` | 同卷前文存在时是否完整承接事实、线索、关系、文气、卷目标完成度、任务连续性与悬疑节奏；当前卷无前序章时是否用卷规划与当前章 planning 补齐 |
| `frontmatter` | YAML 头是否只保留 `写作模型: Doubao` 与 `字数: XXX字`，未重复灌入上下文引用或摘要 |
| `prose_quality` | 正文是否是小说 prose，而非摘要、提纲、流程说明或 planning 复述 |
| `narrative_perspective` | 正文是否保持叙事内视角，未把章节编号、上一章/本章、provider、frontmatter、sidecar、supervision_packet 等执行层标签漏入小说 |
| `dialogue_voice` | 主要人物对白是否能体现角色卡声纹、身份、关系与当前意图，是否避免全员同一种说明腔 |
| `sentence_variety` | 是否避免高频重复 `不是……是……` 等解释句式；同一场戏内是否有句式、节奏和表达路径变化 |
| `provider_evidence` | 是否真实命中豆包 provider，并有 messages pack / raw output / report 证据 |
| `path_contract` | 是否写入 `projects/story/<项目名>/3-初稿/第N卷/第N章.md` |
| `script_boundary` | 脚本是否只做机械辅助，没有替代 LLM 主创正文 |
| `overwrite_safety` | 已有章节是否要求显式 mode + `--force` |
| `repair_authorship` | 返工/修复优化是否仍由 Doubao provider 执行，subagents 是否只作为 brief 与复核层 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为当前章 drafting 输出交付 |
| `pass_with_followups` | 可交付，但有非阻断后续项 |
| `needs_rework` | 存在阻断问题，必须回到对应 rework target |
| `blocked` | 缺失关键输入、provider、权限或上层策略 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: context_loading | source_alignment | supervision_packet | continuity | frontmatter | prose_quality | narrative_perspective | dialogue_voice | sentence_variety | provider_evidence | path_contract | script_boundary | review_handoff
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Default Reviewer Path

- 默认辅助 reviewer：team supervision subagents + `code-reviewer`。
- 正式写作调用默认真实启动 team supervision subagents；仓库层已将本 skill 调用视为对默认 subagent 路径的许可。
- 监制 subagents 默认按项目 `team.yaml -> roles.production.members` 调用已指定监制组成员作为资深创作顾问；每个成员必须回答面向其领域的具体请教问题，并把创意脑洞落实为可执行写作指导。
- GPT/subagents 只拥有监制、prompt 约束和返工 brief 权；正文执行层必须仍是 Doubao provider。
- 对 review 失败后的 `local_repair`、`chapter_rewrite` 或卷级返工，同样要求 Doubao provider evidence；subagent worker 直接改写正文不能通过本 lane review gate。
- 当前卷完成后默认进入 `.agents/skills/story/review` 的 `final_acceptance`，由 `code-reviewer` 与 registry mandatory 维度做卷级审计。
- 若上层 system/developer/tool policy 阻断真实 reviewer/subagent，则允许降级为本地 checklist，但最终报告必须说明：
  - 阻断来源层级
  - 原计划 provider / subagent 路径
  - 实际采用的降级路径
  - 未真实启动的 reviewer

## Gate Rule

不得在以下情况宣布完成：

- 缺少必需输入或未加载项目记忆/相关项目上下文。
- 输出不是 canonical path。
- frontmatter 缺 `写作模型: Doubao`、缺 `字数: XXX字`，重复写入 planning/cards/context 引用与 global/style/north-star 摘要，或 YAML 不可解析。
- 正文保留 planning 标题句法或流程术语。
- 正文出现 `第N章`、`上一章`、`本章`、`本轮生成`、`provider`、`frontmatter`、`sidecar`、`supervision_packet` 等破次元标签。
- 主要人物对白无法从口吻、措辞、停顿、动作和意图区分说话人。
- `不是……是……` 句式在同章中过度重复，或在同一场戏连续承担解释功能。
- 缺少 `supervision_packet` 或 subagent 降级报告。
- `supervision_packet` 不能追溯项目 `team.yaml` roster 来源、请教问题、顾问回答摘要和最终可执行指导。
- provider 证据链缺失，却宣称按当前技能完成。
- 返工或修复优化缺 Doubao repair messages/report，却继续保持 `写作模型: Doubao` 或宣称按 `B-Doubao流` 完成。
- 脚本以规则拼接或模板填充替代 LLM 主创正文。
- 覆盖已有章节时没有显式 `--force`。
- 当前卷已完成却未触发 `review/final_acceptance` 或未说明延后原因。

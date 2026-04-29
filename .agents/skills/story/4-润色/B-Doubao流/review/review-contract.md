# Polishing Review Contract

本文件承载 `story-polishing-doubao` 的质量门禁和 reviewer/provider 规则。审查结论不直接改写业务真源，必须回到主技能聚合与写回规则生效。

## Review Scope

| dimension | checks |
| --- | --- |
| `context_loading` | 是否加载同目录 `CONTEXT.md`、story 根合同（`../../SKILL.md` / `../../CONTEXT.md`）、项目 `MEMORY.md` 与相关 `CONTEXT/` |
| `source_alignment` | 是否遵守三层 planning、全局卡、风格卡与 `north_star` |
| `supervision_packet` | 是否真实启动 team supervision subagents，或有上层阻断降级报告；监制包是否进入 Doubao messages |
| `continuity` | 上一章存在时是否承接；不存在时是否用 planning 补齐 |
| `minimal_repair` | 是否保留初稿骨架、句长/段落分布和人物气口；是否避免无授权整章重排、短句化清洗和通用顺滑化 |
| `frontmatter` | YAML 头是否极简且只保留 `润色模型: Doubao`、`初稿来源` 与 `字数`，未重复灌入上下文引用或摘要 |
| `prose_quality` | 正文是否是小说 prose，且未出现无授权整章重排、短句化清洗、摘要、提纲、流程说明或 planning 复述 |
| `provider_evidence` | 是否真实命中豆包 provider，并有 messages pack / raw output / report 证据 |
| `review_subagent_packets` | 显式 subagents 模式下，是否按审计点调度 `story/review` 维度子技能，并把 findings 注入 Doubao repair brief 直接优化正文 |
| `path_contract` | 是否写入 `projects/story/<项目名>/4-润色/第N卷/第N章.md` |
| `script_boundary` | 脚本是否只做机械辅助，没有替代 LLM 主创正文 |
| `overwrite_safety` | 已有章节是否要求显式 mode + `--force` |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为当前章 polishing 输出交付 |
| `pass_with_followups` | 可交付，但有非阻断后续项 |
| `needs_rework` | 存在阻断问题，必须回到对应 rework target |
| `blocked` | 缺失关键输入、provider、权限或上层策略 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: context_loading | source_alignment | supervision_packet | continuity | frontmatter | minimal_repair | prose_quality | provider_evidence | review_subagent_packets | path_contract | script_boundary | review_handoff
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Default Reviewer Path

- 默认辅助 reviewer：team supervision subagents + `code-reviewer`。
- 正式写作调用默认真实启动 team supervision subagents；仓库层已将本 skill 调用视为对默认 subagent 路径的许可。
- GPT/subagents 只拥有监制、prompt 约束和返工 brief 权；正文执行层必须仍是 Doubao provider。
- 当前卷完成后默认进入 `.agents/skills/story/review` 的 `final_acceptance`，由 `code-reviewer` 与 registry mandatory 维度做卷级审计。
- 当用户显式要求 subagents 模式时，默认执行 `../SKILL.md` 的 `Subagent Review-Optimize Contract`：按审计点调用 `.agents/skills/story/review` 的结构兑现、连续性、逻辑自洽校验、人物一致性、时间线、任务汇聚等维度子技能；每个维度产出 packet / finding / repair brief 后，必须注入 Doubao messages，由 Doubao provider 在同轮直接优化正文。
- 显式 subagents 模式下，`story/review` 子技能只负责分维度审计与归因，不拥有本章最终 PASS/FAIL 或正文写权；本 lane 负责把审计包转译为 provider repair prompt 并写回 canonical path。
- 显式 subagents 模式不得停在“审计报告已生成”；若没有直接优化正文，verdict 至少为 `needs_rework`。
- 若上层 system/developer/tool policy 阻断真实 reviewer/subagent，则允许降级为本地 checklist，但最终报告必须说明：
  - 阻断来源层级
  - 原计划 provider / subagent 路径
  - 实际采用的降级路径
  - 未真实启动的 reviewer

## Gate Rule

不得在以下情况宣布完成：

- 缺少必需输入或未加载项目记忆/相关项目上下文。
- 输出不是 canonical path。
- frontmatter 缺 `润色模型: Doubao`、`初稿来源` 或 `字数`，重复写入 planning/cards/context 引用与 global/style/north-star 摘要，或 YAML 不可解析。
- 正文保留 planning 标题句法或流程术语。
- 无用户显式授权时进行了整章重写、短句化清洗、段落机械切分或通用顺滑化。
- 缺少 `supervision_packet` 或 subagent 降级报告。
- 显式 subagents 模式下缺少 review 维度子技能 packets、repair brief，或只有审计意见没有通过 Doubao 直接优化正文。
- provider 证据链缺失，却宣称按当前技能完成。
- 脚本以规则拼接或模板填充替代 LLM 主创正文。
- 覆盖已有章节时没有显式 `--force`。
- 当前卷已完成却未触发 `review/final_acceptance` 或未说明延后原因。

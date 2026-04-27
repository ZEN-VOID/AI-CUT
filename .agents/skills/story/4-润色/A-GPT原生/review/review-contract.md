# Polishing Review Contract

本文件承载 `story-polishing-gpt-native` 的质量门禁和 reviewer 规则。审查结论不直接改写业务真源，必须回到主技能聚合与写回规则生效。

## Review Scope

| dimension | checks |
| --- | --- |
| `context_loading` | 是否加载同目录 `CONTEXT.md`、story 根合同（`../../SKILL.md` / `../../CONTEXT.md`）、项目 `MEMORY.md` 与相关 `CONTEXT/` |
| `source_alignment` | 是否遵守三层 planning、全局卡、风格卡与 `north_star` |
| `supervision_packet` | 是否真实启动 team supervision subagents，或有上层阻断降级报告；监制包是否进入 GPT-native messages |
| `continuity` | 上一章存在时是否承接；不存在时是否用 planning 补齐 |
| `frontmatter` | YAML 头是否极简且只保留 `润色模型: GPT`，未重复灌入上下文引用或摘要 |
| `prose_quality` | 正文是否是小说 prose，而非摘要、提纲、流程说明或 planning 复述 |
| `gpt_native_evidence` | 是否有 context pack、GPT-authored draft sidecar、writeback summary 或等价证据 |
| `path_contract` | 是否写入 `projects/story/<项目名>/4-润色/第N卷/第N章.md` |
| `script_boundary` | 脚本是否只做机械辅助，没有替代 LLM 主创正文 |

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为当前章 polishing 输出交付 |
| `pass_with_followups` | 可交付，但有非阻断后续项 |
| `needs_rework` | 存在阻断问题，必须回到对应 rework target |
| `blocked` | 缺失关键输入、权限、上下文容量或上层策略 |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: context_loading | source_alignment | supervision_packet | continuity | frontmatter | prose_quality | gpt_native_evidence | path_contract | script_boundary | review_handoff
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Default Reviewer Path

- 默认辅助 reviewer：team supervision subagents + `code-reviewer`。
- 正式写作调用默认真实启动 team supervision subagents；仓库层已将本 skill 调用视为对默认 subagent 路径的许可。
- 当前卷完成后默认进入 `.agents/skills/story/review` 的 `final_acceptance`，由 `code-reviewer` 与 registry mandatory 维度做卷级审计。
- A lane 中 GPT 同时承担主写作和监制能力时，监制必须在后台隔离 subagents 中进行；不得把主写作者自评当成独立审计。
- 若上层 system/developer/tool policy 阻断真实 reviewer/subagent，则允许降级为本地 checklist，但最终报告必须说明：
  - 阻断来源层级
  - 原计划 provider / subagent 路径
  - 实际采用的降级路径
  - 未真实启动的 reviewer

## Gate Rule

不得在以下情况宣布完成：

- 缺少必需输入或未加载项目记忆/相关项目上下文。
- 输出不是 canonical path。
- frontmatter 缺 `润色模型: GPT`，或重复写入 planning/cards/context 引用与 global/style/north-star 摘要。
- 正文保留 planning 标题句法或流程术语。
- 缺少 `supervision_packet` 或 subagent 降级报告。
- 缺少 GPT 原生证据链，却宣称按当前技能完成。
- 脚本以规则拼接或模板填充替代 LLM 主创正文。
- 当前卷已完成却未触发 `review/final_acceptance` 或未说明延后原因。

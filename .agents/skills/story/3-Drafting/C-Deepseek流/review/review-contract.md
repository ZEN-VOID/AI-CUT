# Drafting Review Contract

本文件承载 `story-drafting-deepseek` 的质量门禁和 reviewer/provider 规则。审查结论不直接改写业务真源，必须回到主技能聚合与写回规则生效。

## Review Scope

| dimension | checks |
| --- | --- |
| `context_loading` | 是否加载同目录 `CONTEXT.md`、story 根合同、项目 `MEMORY.md` 与相关 `CONTEXT/` |
| `source_alignment` | 是否遵守三层 planning、全局卡、风格卡与 `north_star` |
| `continuity` | 上一章存在时是否承接；不存在时是否用 planning 补齐 |
| `frontmatter` | 必需字段、`写作模型: Deepseek`、引用路径、global/style/north-star 摘要是否齐备且非照抄 |
| `prose_quality` | 正文是否是小说 prose，而非摘要、提纲、流程说明或 planning 复述 |
| `provider_evidence` | 是否真实命中 DeepSeek provider，并有 messages pack / raw output / report 证据 |
| `path_contract` | 是否写入 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md` |
| `script_boundary` | 脚本是否只做机械辅助，没有替代 LLM 主创正文 |

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
  dimension: context_loading | source_alignment | continuity | frontmatter | prose_quality | provider_evidence | path_contract | script_boundary
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Default Reviewer Path

- 默认辅助 reviewer：`code-reviewer` 或真实 subagent。
- 若用户显式启用 subagents，且上层策略允许，应真实启动 reviewer，而不是主 agent 本地模拟。
- 若上层 system/developer/tool policy 阻断真实 reviewer/subagent，则允许降级为本地 checklist，但最终报告必须说明：
  - 阻断来源层级
  - 原计划 provider / subagent 路径
  - 实际采用的降级路径
  - 未真实启动的 reviewer

## Gate Rule

不得在以下情况宣布完成：

- 缺少必需输入或未加载项目记忆/相关项目上下文。
- 输出不是 canonical path。
- frontmatter 缺任一必需字段，或 `写作模型` 不等于 `Deepseek`。
- 正文保留 planning 标题句法或流程术语。
- provider 证据链缺失，却宣称按当前技能完成。
- 脚本以规则拼接或模板填充替代 LLM 主创正文。

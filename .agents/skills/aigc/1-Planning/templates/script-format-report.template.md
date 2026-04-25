# 1-Planning 2-格式执行报告

---
output_id: OUTPUT-SCRIPT-REPORT
owner_mode: script_format
output_path: projects/aigc/<项目名>/1-Planning/2-格式/执行报告.md
content_contract: 全部已执行 episode 的输入、业务分析、变体裁决、validator、handoff 与返工项。
template_note: 本报告是 2-格式 唯一执行报告；不得再生成 第N集-执行报告.md。
---

## 第N集

### 输入清单

- 上游逐集真源：`projects/aigc/<项目名>/1-Planning/1-分集/第N集.md`
- 上游索引：`projects/aigc/<项目名>/1-Planning/episode-split-plan.json`
- 分集报告：`projects/aigc/<项目名>/1-Planning/1-分集/执行报告.md`

### 业务分析摘要

<本集业务目标、受众、约束、风险与非目标。>

### 变体裁决

- selected_variant: `<标准剧|解说剧|compare>`
- variant_signals: `<判模证据>`
- rejected_variants: `<被拒变体与理由>`
- dialogue_policy: `<对白策略>`
- narration_policy: `<旁白策略>`
- inner_monologue_policy: `<内心独白策略>`

### 结构重排摘要

<场景数量、结构重排、保留/压缩的重点。>

### validator 结果

- validator: `validate_script_output.py`
- status: `<PASS|FAIL>`
- findings: `<warning/error 摘要>`
- actual_word_count: `<总字数>`

### 父级 handoff

- episode_id: `第N集`
- selected_variant: `<标准剧|解说剧|compare>`
- script_output_path: `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md`
- scene_count: `<场景数>`
- source_profile: `<source_profile 摘要>`
- bootstrap_output: `projects/aigc/<项目名>/2-Global/导演意图.md`

### 验收结论与返工项

<通过结论或最小返工入口。>

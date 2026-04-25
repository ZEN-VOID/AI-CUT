# 1-Planning 2-剧本执行报告

---
output_id: OUTPUT-SCRIPT-REPORT
owner_mode: script_format
output_path: projects/aigc/<项目名>/1-Planning/2-格式/执行报告.md
content_contract: 全部已执行 episode 的输入、业务分析、剧本策略、validator、handoff 与返工项。
template_note: 本报告是 2-剧本 唯一执行报告；runtime 输出路径仍为 2-格式/执行报告.md，不得再生成 第N集-执行报告.md。
---

## 第N集

### 输入清单

- 上游逐集真源：`projects/aigc/<项目名>/1-Planning/1-分集/第N集.md`
- 上游索引：`projects/aigc/<项目名>/1-Planning/episode-split-plan.json`
- 分集报告：`projects/aigc/<项目名>/1-Planning/1-分集/执行报告.md`

### 业务分析摘要

<本集业务目标、受众、约束、风险与非目标。>

### 剧本策略

- selected_variant: `标准剧`
- format_signals: `<剧本策略证据>`
- dialogue_policy: `<对白策略>`
- narration_policy: `<旁白策略>`
- inner_monologue_policy: `<内心独白策略>`
- visual_field_policy: `<动作/环境/音效/音效画面/道具/系统画面等字段分流策略；说明声画字段纯度>`

### 结构重排摘要

<场景数量、结构重排、正式影视剧本字段分流与画面剧本化改写摘要。>

### validator 结果

- validator: `validate_script_output.py`
- status: `<PASS|FAIL>`
- findings: `<warning/error 摘要>`
- actual_word_count: `<总字数>`

### 父级 handoff

- episode_id: `第N集`
- selected_variant: `标准剧`
- script_output_path: `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md`
- scene_count: `<场景数>`
- source_profile: `<source_profile 摘要>`
- bootstrap_output: `projects/aigc/<项目名>/2-Global/导演意图.md`

### 验收结论与返工项

<通过结论或最小返工入口。>

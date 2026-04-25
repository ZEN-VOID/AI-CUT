# 1-Planning 3-分组执行报告

<!--
output_id: OUTPUT-GROUPING-REPORT
owner_mode: grouping
output_path: projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md
content_contract: 组序、source_span、量化字段、quantization_trace、episode 级 handoff。
template_note: 每个分镜组都必须逐条登记 canonical 量化结果与 quantization_trace，不得只写结论。
-->

## 第1集

### 【1-1-1】 <分组名>
source_span: `<场景范围或镜号范围>`
estimated_duration_seconds: `<15秒>`
effective_text_chars: `<150>`
window_status: `<pass | pass_low_anchor | pass_high_preserve>`
judgement_basis: `<说明本组为何保留 / 拆分 / 不并组；若低于 warn_low 或高于 warn_high，必须写清拆并检查、锁定依据或独立信息落点。>`
quantization_trace: `duration=<default(15)->15 或 mapping[1-1-1](20)->20>; window=base(<duration>*10*<pace_coef>=<base_text_window>), warn_low(<base>*0.8=<warn_low>), warn_high(<base>*1.0=<warn_high>), hard(<base>*1.1=<hard_text_window>); effective_chars=<字段加权或规划估算过程>; mode=<group_section_field_weighted | planning_estimate_visible_chars | story_source_recomputed_field_weighted | story_source_recomputed_visible_chars>`

### 【1-1-2】 <分组名>
source_span: `<场景范围或镜号范围>`
estimated_duration_seconds: `<15秒>`
effective_text_chars: `<132>`
window_status: `<pass | pass_low_anchor | pass_high_preserve>`
judgement_basis: `<继续逐组填写>`
quantization_trace: `duration=<...>; window=<...>; effective_chars=<...>; mode=<...>`

## handoff 摘要

episode_id: `第1集`
group_count: `<本集分组数>`
group_order: `<1-1-1 -> 1-1-2 -> ...>`
locked_anchor_ids: `<[] 或 [已锁定 group_id]>`
duration_policy: `<默认15秒；若无显式上游时长证据则不偏离>`
pace_tier: `<慢节奏 | 中节奏 | 快节奏>`
handoff_summary: `<本集 grouped script 的 handoff 摘要>`
bootstrap_output: `projects/aigc/<项目名>/2-Global/导演意图.md`
upstream_paths:
- `projects/aigc/<项目名>/1-Planning/2-格式/第1集.md`
- `projects/aigc/<项目名>/1-Planning/episode-split-plan.json`
- `projects/aigc/<项目名>/0-Init/north_star.yaml`
- `projects/aigc/<项目名>/0-Init/init_handoff.yaml`

<!--
填写规则：
- 每个 `### 【group_id】` 区块都必须完整包含 6 个组级字段：`source_span / estimated_duration_seconds / effective_text_chars / window_status / judgement_basis / quantization_trace`。
- `quantization_trace` 必须直接复用 quantizer 的 canonical 过程串，不要手写第二套公式说明。
- 若命中 story-source 回算，`quantization_trace` 中必须保留镜号范围。
- `window_status` 不得落盘候选态 `warn_low / warn_high / error`；正式报告只能写通过态。
- `handoff 摘要` 只写 episode 级汇总，不替代组级量化证据。
-->

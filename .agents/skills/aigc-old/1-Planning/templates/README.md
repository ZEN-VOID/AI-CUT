# Templates

本目录保存 `1-Planning` 融合包的输出模板。凡本目录定义的输出内容模板，必须能回指到 `SKILL.md` 的 `Output Contract`。

`output-template.md` 是模板层对齐索引，用于结构校验；它不直接生成项目产物。

## Output Contract Alignment

| template | 对应 output_id | canonical 输出位置 | owner mode | 匹配要求 |
| --- | --- | --- | --- | --- |
| `episode-split-plan.template.json` | `OUTPUT-SPLIT-PLAN` | `projects/aigc/<项目名>/1-Planning/episode-split-plan.json` | `episode_split` | 必须包含 `source_profile`、`bootstrap_output`、coverage、边界索引与 `1-分集` 输出路径 |
| `script-format-report.template.md` | `OUTPUT-SCRIPT-REPORT` | `projects/aigc/<项目名>/1-Planning/2-格式/执行报告.md` | `script_format` / `2-剧本` | 必须包含每个已执行 episode 的剧本策略、validator 结果、handoff 与返工项；不得生成逐集报告侧车 |
| `grouping-output.template.md` | `OUTPUT-GROUPED-SCRIPT` | `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md` | `grouping` | 必须包含 grouped script 正文、三段式 `分镜组ID`、上游主稿、报告引用与可机读尾钩 |
| `grouping-report.template.md` | `OUTPUT-GROUPING-REPORT` | `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md` | `grouping` | 必须包含组序、`source_span`、量化字段、`quantization_trace` 与 episode 级 handoff |

## Non-Templated Outputs

以下输出当前不在 `templates/` 单独建模板，按对应合同直接由 LLM 主创或 review 聚合写入：

- `OUTPUT-SPLIT-SOURCE`、`OUTPUT-SPLIT-REPORT`：见 `references/episode-splitter-contract.md`。
- `OUTPUT-SCRIPT`：见 `references/script-format-contract.md`；`OUTPUT-SCRIPT-REPORT` 使用 `script-format-report.template.md`。
- `OUTPUT-VALIDATION`：见 `review/planning-review-contract.md`。

模板只提供结构骨架，不是任务完成的唯一验收标准。

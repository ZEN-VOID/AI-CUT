# 4-表演 Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-PERF-EPISODE`: `projects/aigc/<项目名>/4-表演/第N集.md`
- `OUTPUT-PERF-REPORT`: `projects/aigc/<项目名>/4-表演/执行报告.md`

### Output format

- 逐集表演稿：Markdown，完整保留 `3-导演/第N集.md` 的结构、字段、对白和顺序，只在既有字段内部嵌入表演工艺。
- 执行报告：Markdown，记录输入、目标集、review verdict、直接修复项、复审结果、`advisor_consultation_packet`、`thinking_action_node_ledger`、`psychological_reaction_evidence`、`actor_performance_control_evidence`、`protagonist_inner_voice_evidence`、`objective_action_purity_evidence`、`scene_dramatic_map`、`performance_task_map`、`blocking_power_map`、`integration_targets`、遗留风险和下游 handoff。

### Output path

```text
projects/aigc/<项目名>/4-表演/
├── 第1集.md
├── 第2集.md
└── 执行报告.md
```

### Completion gate

- 上游 `3-导演/第N集.md` 可回指，frontmatter 包含 `source_directing_path`。
- 不改写剧情事实、对白、场景标题或字段顺序。
- 阶段内 review、直接修复和复审闭环完成，未通过时不得写入 canonical 输出。

# 3-导演 Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-DIRECTOR-EPISODE`: `projects/aigc/<项目名>/3-导演/第N集.md`
- `OUTPUT-DIRECTOR-REPORT`: `projects/aigc/<项目名>/3-导演/执行报告.md`

### Output format

- 逐集导演稿：Markdown，完整保留 `2-编剧/第N集.md` 的结构、字段、对白和顺序，只在既有字段内部嵌入导演判断。
- 执行报告：Markdown，记录输入、目标集、review verdict、直接修复项、复审结果、`thinking_action_node_ledger`、`director_substance_evidence`、`peak_visual_plan`、`advisor_consultation_packet`、`controlled_enrichment_ledger`、`visual_aesthetic_evidence`、`episode_final_image_evidence`、`atmosphere_mood_evidence`、遗留风险和下游 handoff。

### Output path

```text
projects/aigc/<项目名>/3-导演/
├── 第1集.md
├── 第2集.md
└── 执行报告.md
```

### Completion gate

- 上游 `2-编剧/第N集.md` 可回指，frontmatter 包含 `source_screenplay_path`。
- 不改写剧情事实、对白、场景标题或字段顺序。
- 阶段内 review、直接修复和复审闭环完成，未通过时不得写入 canonical 输出。

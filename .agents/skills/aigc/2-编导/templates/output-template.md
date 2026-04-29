# Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-DIRECTING-EPISODE`: `projects/aigc/<项目名>/2-编导/第N集.md`
- `OUTPUT-DIRECTING-REPORT`: `projects/aigc/<项目名>/2-编导/执行报告.md`

### Output format

- 逐集编导稿：Markdown，含 YAML frontmatter、`【剧本正文】`、场景标题和字段化剧本正文。
- 执行报告：Markdown，记录输入、目标集、review verdict、直接修复项、复审结果、遗留风险和下游 handoff。

### Output path

```text
projects/aigc/<项目名>/2-编导/
├── 第1集.md
├── 第2集.md
└── 执行报告.md
```

### Naming convention

- 逐集编导稿：`第N集.md`
- 报告：`执行报告.md`

### Completion gate

- 上游 `1-分集/第N集.md` 已回指。
- 事实、顺序和对白保真。
- 声画配对、字段纯度和 slugline 稳定通过 review。
- 上游存在高潮/爽点/高光成分时，已按 `peak_visual_pass` 落入既有可拍字段，没有新增事实或对白。
- 若 review 发现阻断项，已在 `2-编导` 阶段内直接最小修复并复审通过；若无法修复，已记录阻断来源且不得推进下游。
- 执行报告记录 review verdict、repair actions、re-review verdict、残余风险和是否允许进入 `3-摄影`。

## Episode File Skeleton

See `templates/episode-script.template.md`.

# Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-DIRECTING-EPISODE`: `projects/aigc/<项目名>/2-编导/第N集.md`
- `OUTPUT-DIRECTING-REPORT`: `projects/aigc/<项目名>/2-编导/执行报告.md`

### Output format

- 逐集编导稿：Markdown，含 YAML frontmatter、`【剧本正文】`、场景标题和字段化剧本正文。
- 执行报告：Markdown，记录输入、目标集、校验结果、修复项和下游 handoff。

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
- 执行报告记录校验 verdict。

## Episode File Skeleton

See `templates/episode-script.template.md`.

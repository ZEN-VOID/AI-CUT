# Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-EPISODE-SOURCE`: `projects/aigc/<项目名>/1-分集/第N集.md`
- `OUTPUT-SPLIT-REPORT`: `projects/aigc/<项目名>/1-分集/执行报告.md`

### Output format

- 逐集文件：Markdown 原文正文。
- 执行报告：Markdown 报告。

### Output path

```text
projects/aigc/<项目名>/1-分集/
├── 第1集.md
├── 第2集.md
└── 执行报告.md
```

### Naming convention

- 逐集正文：`第N集.md`
- 报告：`执行报告.md`

### Completion gate

- 输入真源明确。
- 原生集数划分已被优先保留，或已说明无原生集标。
- 无原生集标时默认按 2500-3000 字目标窗切分。
- 输出编号连续、覆盖完整、正文未改写。

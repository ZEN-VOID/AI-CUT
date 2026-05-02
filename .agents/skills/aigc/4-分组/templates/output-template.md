# Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-GROUP-EPISODE`: `projects/aigc/<项目名>/4-分组/第N集.md`
- `OUTPUT-GROUP-REPORT`: `projects/aigc/<项目名>/4-分组/执行报告.md`

### Output format

- 逐集文件：Markdown 分镜组稿。
- 执行报告：Markdown 报告。

### Output path

```text
projects/aigc/<项目名>/4-分组/
├── 第1集.md
├── 第2集.md
└── 执行报告.md
```

### Naming convention

- 逐集分组稿：`第N集.md`
- 报告：`执行报告.md`
- 分镜组 ID：`x-y-z`

### Completion gate

- 输入摄影稿与 `north_star.yaml` 可回指。
- 每组包含三项 north_star 风格投影、正文、出场画面和 YAML 统计；其中第 1 行全局风格必须以固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。` 开头，后接原词，第 2 组起包含入场画面。
- 每组不超过 1980 字，不含 YAML。
- 组间桥接画面成对一致，每集首组不输出入场画面段。
- 正文同步 `3-摄影` 原换行且未改写。

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
- 每组包含三项 north_star 风格投影、正文和 YAML 统计；其中第 1 行全局风格必须以固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。` 开头，后接原词。
- 每组纯分镜剧本正文常规目标不超过 1680 字；1681-1980 字必须有例外理由；不含组标题、north_star、YAML 和组间连接件。
- 每对相邻组之间物理夹放 `## <上一个分镜组ID>~<下一个分镜组ID>`，标题本身作为连接件唯一分镜 ID；标题后、`连接类型` 前有三项 north_star 风格行，且第 1 行以固定全局风格前置词开头，字段含连接类型、具体连接方法描述、3-4 秒时长、变化过程、主体运动、运镜设计、透视适应和避免元素；连接方法不得只写抽象分类名，避免元素只写负面约束，不复述起点/目标端点，不输出 `分镜ID：`、`连接件提示：` 或旧版 `入场画面：` / `出场画面：`。
- 正文同步 `3-摄影` 原换行且未改写。
- 执行报告同时记录 validator error/warning 与 `boundary_review`、`bridge_review`、`faithfulness_review`、`statistics_evidence_review` 语义结论。

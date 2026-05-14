# Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-GROUP-EPISODE`: `projects/aigc/<项目名>/6-分组/第N集.md`
- `OUTPUT-GROUP-REPORT`: `projects/aigc/<项目名>/6-分组/执行报告.md`

### Output format

- 逐集文件：Markdown 分镜组稿。
- 执行报告：Markdown 报告。

### Output path

```text
projects/aigc/<项目名>/6-分组/
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
- 每组标题后先写当前场景标题行，例如 `场景1：外景 扶桑战船外舷与黑礁 - 夜`；即便未切换场景，新的分镜组也必须重复同一个场景标题；随后包含三项 north_star 风格投影、正文和 YAML 统计，其中第 1 行风格行必须以固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。需要生成现场物理互动音效、氛围感音效、环境声、自然现象声、动作声，不要生成任何字幕，不要生成背景音乐。` 开头，后接原词。
- YAML `字数统计` 必须计入分镜组标题后的场景标题行；该场景标题行不计入 `时长估算`。
- 每组以 `分镜N（约X秒）` 显式时长累计为主，优先接近 15 秒，通常约 12-18 秒可接受；单组显式时长累计不得超过 18 秒，超过 18 秒必须拆分、重组或回退 `5-摄影` 修复，不能写完整性例外理由放行；字数和对白只作辅助风险复核。
- 每对相邻组之间物理夹放 `## <上一个分镜组ID>~<下一个分镜组ID>`，标题本身作为连接件唯一分镜 ID；标题后先写场景标题行，同场景连接重复同一个场景标题，跨场景连接写成 `场景标题A ➡️ 场景标题B`；随后在 `连接类型` 前写三项 north_star 风格行，且第 1 行以固定全局风格前置词开头，字段含连接类型、具体连接方法描述、3-4 秒时长、变化过程、主体运动、运镜设计、透视适应和避免元素；连接方法不得只写抽象分类名，避免元素只写负面约束，不复述起点/目标端点，不输出 `分镜ID：`、`连接件提示：` 或旧版 `入场画面：` / `出场画面：`。
- 正文同步 `5-摄影` 原换行且未改写。
- 执行报告同时记录每组 `时长估算`、validator error/warning 与 `boundary_review`、`bridge_review`、`faithfulness_review`、`statistics_evidence_review` 语义结论。

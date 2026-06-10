# Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-GROUP-EPISODE`: `projects/aigc/<项目名>/10-分组/第N集.md`
- `OUTPUT-GROUP-REPORT`: `projects/aigc/<项目名>/10-分组/执行报告.md`

### Output format

- 逐集文件：Markdown 分镜组稿。
- 执行报告：Markdown 报告。

### Output path

```text
projects/aigc/<项目名>/10-分组/
├── 第1集.md
├── 第2集.md
└── 执行报告.md
```

### Naming convention

- 逐集分组稿：`第N集.md`
- 报告：`执行报告.md`
- 分镜组 ID：`x-y-z`

### Completion gate

- 输入光影稿或用户指定 source 与 `3-美学/画面基调/全局风格协议.md` 可回指；项目存在初始化综合时，已只读消费 `team.yaml.init_synthesis.stage_seed_summary."10-分组"`、`init_handoff.grouping_seed` 或 `north_star.yaml.创作阶段不变量.分组`，形成 `init_team_synthesis_context`，且未触发 team 身份、旧 stage profile 或伪顾问问答。用户指定非 `9-光影` source 时，执行报告必须声明 `source_override=true` 与不适用的光影稿专属检查。
- 每组标题后先写当前场景标题行，例如 `场景1：外景 扶桑战船外舷与黑礁 - 夜`；即便未切换场景，新的分镜组也必须重复同一个场景标题。场景标题行下方立即输出字段标题 `全局风格：`，字段内只保留一行内容：以固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。需要生成现场物理互动音效、氛围感音效、环境声、自然现象声、动作声，不要生成任何字幕，不要生成背景音乐。` 开头，后接根据当前分镜组从 `画面基调.Global Style Prompt` 抽取的匹配风格句，300 字以内；不得输出 `Visual Slogan`、`Design Principle`、`Visual Gene Profile` 或 `Negative Traits` 独立行。
- `全局风格：` 单行内容之后直接进入 source 分镜正文；第一行必须直接是普通 `分镜N（0-N秒）：` 或 `[0-N秒]` 时间码分镜行。首组自然整理本组开始画面，第二组起按回龙帧口径先复现上一组尾帧状态锚点，再只调整景别和镜头视角进入本组；尾帧状态锚点至少包含可见主体、动作/姿态/运动余势、关键道具/介质/环境残留、光线/烟雾/水汽/碎片/声音余波、保护线/战斗线/空间方位关系。若该画面点来自对白画面、独白画面、旁白画面或音效画面，必须同步带入对应声音内容；不得只承接情绪或空间大方向，不得直接开启新动作；不得输出 `分镜画面：`、`增补首帧：`、`回龙帧：`、来源说明或规则说明。
- YAML `字数统计` 必须计入分镜组标题后的场景标题行和分镜剧本正文；这些组头描述不计入 `时长估算`；字段标题 `全局风格：` 及其单行 `Global Style Prompt` 整理内容、YAML fenced block 本身均不计入 `字数统计`。
- 每组以连续分镜行 / 声画 atomic unit 总时长为主：裁决边界时优先累计 `分镜N（起始秒-结束秒）：` 行的时长，兼容 `[起始秒-结束秒]` 行；落盘到分镜组后，时间码必须整合为当前分镜组基准下连续递增的 `分镜N（N-N秒）：` 或 `[N-N秒]`，后一个时间段起点必须等于前一个时间段终点，YAML `时长估算` 取最终结束秒。目标约 14.5 秒，通常约 10-14.5 秒可接受；最终累计结束秒必须以 `.5` 结尾，若自然相加不是 `.5` 结尾则在组尾上调 0.5 秒；单组时长不得超过 14.5 秒，超过 14.5 秒必须拆分、重组或回退 source owner 修复，不能写完整性例外理由放行；字数和对白只作辅助风险复核。
- 不输出 `## <上一个分镜组ID>~<下一个分镜组ID>` 组间连接件，也不输出 `连接类型：`、`连接方法：`、`变化过程：`、`主体运动：`、`运镜设计：`、`透视适应：`、`避免元素：` 等连接件字段；相邻组承接只通过下一组第一个普通 `[0-N秒]` 分镜行完成。
- 正文同步 `9-光影` 或用户指定 source 原换行且未无授权改写。
- 执行报告同时记录初始化综合消费来源与采纳点、每组 `时长估算`、回龙帧尾帧状态锚点五项元素复现、镜头调整和声音承托同步检查、validator error/warning 与 `boundary_review`、`global_style_review`、`first_storyboard_continuity_review`、`connector_removal_review`、`faithfulness_review`、`statistics_evidence_review` 语义结论。

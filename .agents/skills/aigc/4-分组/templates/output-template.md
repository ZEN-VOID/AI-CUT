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
- 每组包含三项 north_star 风格投影、正文、首次锁定及变化分镜的 `站位和位移：`、出场画面和 YAML 统计；其中第 1 行全局风格必须以固定前置词 `不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。` 开头，后接原词，第 2 组起包含入场画面。
- 每条 `站位和位移：` 主语必须是明确角色名或上游已命名的稳定群体称谓，不使用 `画面主体`、`主体`、`人物`、`角色`、`主角`、代词等模糊指代；涉及多角色时必须明确前后、左右、内外、近远或动作先后的顺位关系；位移必须能由当前分镜原文、上一分镜状态或入场/出场补位画面连续推导，不能为了造句新增无证据移动；连续多个分镜站位和位移完全不变时，仅需首次固定，无需重复出现在每个分镜头。
- 每组不超过 1980 字，不含 YAML。
- 组间桥接画面成对一致，每集首组不输出入场画面段。
- 正文同步 `3-摄影` 原换行且未改写。

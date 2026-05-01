# Input / Output Contract

## Source Priority

1. 用户显式指定的小说原文资料路径。
2. `projects/aigc/<项目名>/源/`。
3. 仅当用户明确要求兼容旧项目时，才读取旧源路径或迁移中路径；读取时必须在执行报告中标明 fallback。

## Valid Source Material

- 小说正文、章节正文、含明显章节/集数标题的文本。
- `.md`、`.txt` 或可稳定抽取文本的文档。
- 多文件来源必须建立确定性排序：优先文件名数字，其次正文内章节序号，再次标题自然顺序。

## Episode Boundary Policy

### P1: Explicit Episode Boundary

若源资料含以下强信号，以原资料为准：

- `第1集`、`第一集`、`EP01`、`Episode 1`
- `第1话`、`第一话`，且上下文明显作为影视/漫画/连载单元
- 用户在指令中明确指定的集数边界或范围

不属于 P1 的信号：

- `第N章`、`第1章`、`第一章`、`Chapter 1`、卷、章、节、小节、story 项目章节文件名。
- “story 一章”不得被默认投影为 “AIGC 一集”；它只能进入 P2 候选边界。
- 章节不等于集数；章节编号不能触发 `explicit_episode_split`。

### P2: Natural Structure Boundary

没有集标时，优先借助章节、幕、小节、场面转换、叙事高潮和悬念点形成候选边界。
章节边界可作为候选，但必须再经过字数窗口、自然段闭合、戏剧断点或用户显式指令确认；不得机械执行“一章一集”。

### P3: Length Window Boundary

若 P1/P2 均不足，默认每集约 2500-3000 中文字。边界应落在自然段或情节小闭环处，避免切断一句话、对白轮次或关键动作。

## Output Path

```text
projects/aigc/<项目名>/1-分集/
├── 第1集.md
├── 第2集.md
├── ...
└── 执行报告.md
```

## Episode File Requirements

- 文件名：`第N集.md`。
- 编号：从 1 开始连续编号。
- 内容：对应集原文，允许添加最小标题和来源 frontmatter。
- 禁止：改写、扩写、删减、剧本化、分镜化、把设定说明混入正文。

## Execution Report Requirements

`执行报告.md` 至少包含：

- 输入路径与文件清单。
- 切分模式：`explicit_episode_split` 或 `length_based_split`。
- 每集来源范围、字数、边界理由。
- 覆盖状态：已覆盖、未覆盖、跳过原因。
- 返工入口：若编号、覆盖、字数或保真失败，应指向具体集数。

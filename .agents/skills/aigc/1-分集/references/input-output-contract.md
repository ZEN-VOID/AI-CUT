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

## Review Gate Mapping

本 reference 只展开分集输入、边界与输出细则；强制裁决权和返工节点由 `SKILL.md` 的 `Thinking-Action Node Map` 与 `Review Gate Binding` 持有。以下问题不是软提示，必须在 `review/review-contract.md` 中解析为可执行 gate，并能回到 `SKILL.md` 的主节点。

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否按“用户显式路径 > `projects/aigc/<项目名>/源/` > 用户明确要求的旧路径 fallback”锁定唯一小说原文真源，且未把 `MEMORY.md`、`CONTEXT/`、设定案或治理文件抬升为正文真源？ | `GATE-SPLIT-01-SOURCE-LOCK` | `FAIL-SPLIT-01` | `SKILL.md#T2-SOURCE-LOCK`；`SKILL.md#Input Contract`；本文件 `Source Priority` | 执行报告中的输入路径、fallback 说明、文件清单与真源排除说明 |
| 多文件或多章节来源是否都是可读文本，并已按文件名数字、正文内章节序号或标题自然顺序建立可复查排序？ | `GATE-SPLIT-01A-SOURCE-ORDER` | `FAIL-SPLIT-01A` | `SKILL.md#T3-SOURCE-ORDER`；本文件 `Valid Source Material` | 执行报告中的可读性判断、排序依据、输入文件顺序表 |
| 源资料存在 `第N集`、`Episode N`、`EP N` 或上下文明显为连载单元的 `第N话` 时，是否严格按原资料 P1 集标落盘，没有按字数重切？ | `GATE-SPLIT-02-P1-EPISODE-MARK` | `FAIL-SPLIT-02` | `SKILL.md#T4-MARK-SCAN`；`SKILL.md#T5-BOUNDARY-SOLVE`；本文件 `Episode Boundary Policy / P1` | 集标列表、每集原始边界、`explicit_episode_split` 模式说明 |
| `第N章`、`Chapter N`、卷、章、节、小节或 story 章节文件名是否只作为 P2 候选边界，没有被误判为原生集标或机械执行“一章一集”？ | `GATE-SPLIT-02A-CHAPTER-NOT-EPISODE` | `FAIL-SPLIT-02A` | `SKILL.md#T4-MARK-SCAN`；`SKILL.md#T5-BOUNDARY-SOLVE`；本文件 `Episode Boundary Policy / P1-P2` | 被排除的章节信号列表、P2/P3 边界裁决说明、非一章一集证据 |
| 无 P1 集标时，P2/P3 边界是否结合自然结构、戏剧断点和 2500-3000 字目标窗，且没有切断句子、对白轮次或关键动作？ | `GATE-SPLIT-03-BOUNDARY-SOLVE` | `FAIL-SPLIT-03` | `SKILL.md#T5-BOUNDARY-SOLVE`；本文件 `Episode Boundary Policy / P2-P3` | 每集字数、起止段落、边界理由、偏离目标窗的说明 |
| 逐集文件是否只写入 `projects/aigc/<项目名>/1-分集/第N集.md`，编号从 1 连续，正文保持原文，未改写、扩写、删减、剧本化、分镜化或混入设定说明？ | `GATE-SPLIT-04-EPISODE-WRITEBACK` | `FAIL-SPLIT-04` | `SKILL.md#T6-WRITEBACK`；`SKILL.md#Output Contract`；本文件 `Output Path` 与 `Episode File Requirements` | 输出文件清单、编号连续性检查、正文保真抽查或 diff 说明 |
| `执行报告.md` 是否包含输入路径、文件清单、切分模式、每集来源范围、字数、边界理由、覆盖状态、跳过原因和按具体集数定位的返工入口？ | `GATE-SPLIT-05-REPORT-COVERAGE` | `FAIL-SPLIT-05` | `SKILL.md#T7-REVIEW`；`SKILL.md#Output Contract`；本文件 `Execution Report Requirements` | 执行报告中的边界表、coverage 表、跳过原因、返工入口 |

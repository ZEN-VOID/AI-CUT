# Output Template Alignment

本模板对齐 `story-polishing` 的 Output Contract。

| field | contract |
| --- | --- |
| Required output | 当前章完整中文润色 Markdown 文件 |
| Frontmatter | `修订阶段: 润色`、`初稿来源`、`字数: XXX字` |
| Heading | `# 第N章｜章标题` |
| Body | 中文小说 prose，保留初稿事实和句群骨架 |
| Path | `projects/story/<项目名>/4-润色/第N卷/第N章.md` |
| Completion gate | 源章读取、LLM-first 润色、最小修补 gate、canonical writeback、状态 hook 记录或阻断说明 |

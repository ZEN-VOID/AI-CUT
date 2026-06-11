# Output Template Alignment

本模板对齐 `story-drafting` 的 Output Contract。

| field | contract |
| --- | --- |
| Required output | 当前章完整中文小说初稿 Markdown 文件 |
| Frontmatter | `创作阶段: 初稿`、`字数: XXX字` |
| Heading | `# 第N章｜章标题` |
| Body | 中文小说 prose |
| Path | `projects/story/<项目名>/3-初稿/第N卷/第N章.md` |
| Completion gate | 上下文加载、LLM-first 主创、质量门、canonical writeback、状态 hook 记录或阻断说明 |

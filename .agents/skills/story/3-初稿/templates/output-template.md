# Output Contract Alignment

本模板对齐 `story-drafting` 的 Output Contract。

- Required output: 当前章完整中文小说初稿 Markdown 文件，以及同章初稿验收包。
- Output format: YAML frontmatter、空行、`# 第N章｜章标题`、章节正文；frontmatter 至少包含 `创作阶段: 初稿` 与 `字数: XXX字`。
- Output path: 正文写入 `projects/story/<项目名>/3-初稿/第N卷/第N章.md`；验收包写入 `projects/story/<项目名>/3-初稿/第N卷/第N章.acceptance.json`。
- Naming convention: 卷目录使用 `第N卷`，章节文件使用 `第N章.md`，验收包使用 `第N章.acceptance.json`。
- Completion gate: 上下文加载、LLM-first 主创、命中类型化场面时 `type_package_manifest` 与 `genre_scene_route` 通过、质量门、canonical writeback、状态 hook 记录或阻断说明。

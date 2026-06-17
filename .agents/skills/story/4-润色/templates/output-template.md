# Output Contract Alignment

本模板对齐 `story-polishing` 的 Output Contract。

- Required output: 当前章完整中文最小局部修补稿 Markdown 文件，以及同章终稿验收包。
- Output format: YAML frontmatter、空行、`# 第N章｜章标题`、章节润色稿；frontmatter 至少包含 `修订阶段: 润色`、`初稿来源` 与 `字数: XXX字`。
- Output path: 正文写入 `projects/story/<项目名>/4-润色/第N卷/第N章.md`；验收包写入 `projects/story/<项目名>/4-润色/第N卷/第N章.acceptance.json`。
- Naming convention: 卷目录使用 `第N卷`，章节文件使用 `第N章.md`，验收包使用 `第N章.acceptance.json`。
- Completion gate: 源章读取、LLM-first 润色、命中类型化场面修复时 `repair_type_package_manifest` 与 `genre_scene_repair_profile` 通过、最小修补 gate、canonical writeback、状态 hook 记录或阻断说明。

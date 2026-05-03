# Scripts Boundary

本目录仅承载机械辅助脚本说明。`D-主板混合参照` 的核心 prompt 组织、故事板总参照语义、主体参照语义和视频生成策略必须由 LLM 根据 `SKILL.md` 与分区合同直接完成。

允许脚本执行：

- 读取 `4-分组` 并抽取 `group_id`、line range、YAML。
- 枚举故事板图和主体图片路径。
- 生成 JSON / Markdown / queue ledger 的机械投影。
- 查询 LibTV 状态、下载结果、校验文件存在性。

禁止脚本执行：

- 扩写或改写分镜组剧情。
- 自动决定故事板或主体图的创作语义。
- 在图片超限时静默裁剪。
- 伪造 sessionId 或生成结果。

# Scripts

本目录仅承载机械辅助脚本说明。`A-分镜画面参照` 的核心 prompt 组织、参照语义裁决和视频生成策略必须由 LLM 根据 `SKILL.md` 与分区合同直接完成。

允许的脚本职责：

- 读取 `4-分组/第N集.md` 并抽取 `## x-y-z` 边界。
- 建立 `group_id -> shot_id` 索引。
- 检查 `6-图像/A-分镜画面` 中的本地图片路径是否存在。
- 投影 JSON / YAML / queue ledger / results。
- 调用 `libtv` 命令、记录 `sessionId`、查询和下载结果。
- 机械写入默认 `prompt_fidelity_mode=strict_original`、`allow_libtv_prompt_optimization=false` 与 `transport_only_projection=true`。

禁止的脚本职责：

- 主创或扩写视频 prompt 正文。
- 改写 `4-分组` 的剧情、镜头顺序、角色关系或组边界。
- 未获用户显式 opt-in 时启用 LibTV 提示词优化、摘要、重排、补镜头或重新编排。
- 猜测不存在的图片引用或保留空图片槽位。

# Scripts Boundary

本目录仅承载机械辅助脚本说明。`D-主板混合参照` 的核心 prompt 组织、故事板总参照语义、主体参照语义和视频生成策略必须由 LLM 根据 `SKILL.md` 与分区合同直接完成。

允许脚本执行：

- 读取 `4-分组` 并抽取 `group_id`、line range、YAML。
- 枚举故事板图和主体图片路径。
- 生成 JSON / Markdown / queue ledger 的机械投影。
- 机械生成或校验 `asset_uploads` 与 `generation_slots`：前者只记录 `故事板/主体身份 -> uploaded_url`，后者记录 `UI 图N/mixedList[n-1] -> uploaded_url -> 故事板/主体身份`；若 UI 槽位可观测，必须保留 `slot_source` 并以 UI 图N 为准。
- 查询 LibTV 状态、下载结果、校验文件存在性。
- 机械写入默认 `prompt_fidelity_mode=strict_original`、`allow_libtv_prompt_optimization=false` 与 `transport_only_projection=true`。
- `build-upload-ledger.py --sync` 是 D 路线提交前的机械投影器：读取 submit plan / batch 中的故事板与主体 uploaded URL，生成 `asset_uploads` 与 `generation_slots`，并把最终槽位同步回 manifest、plan、prompt fenced YAML 的 `故事板参照` 与 `角色/场景/道具` 主体项，以及远端提交的 `mixedList`。它不生成 prompt 正文，只负责避免故事板/主体身份、URL 和 LibTV 图N 槽位错位。

禁止脚本执行：

- 扩写或改写分镜组剧情。
- 未获用户显式 opt-in 时启用 LibTV 提示词优化、摘要、重排、补镜头或重新编排。
- 自动决定故事板或主体图的创作语义。
- 在图片超限时静默裁剪。
- 把 OSS 上传顺序直接当作 `reference_index` 或图N顺序真源。
- 在 draft prompt 中伪造空 `reference_index / uploaded_url`，或在未确认槽位前生成 final 远端提交。
- 伪造 sessionId 或生成结果。

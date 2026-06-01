# Scripts

本目录仅承载机械辅助脚本说明。`A-分镜画面参照` 的核心 prompt 组织、参照语义裁决和视频生成策略必须由 LLM 根据 `SKILL.md` 与分区合同直接完成。

允许的脚本职责：

- 读取 `5-分组/第N集.md` 并抽取 `## x-y-z` 边界。
- 建立 `group_id -> shot_id` 索引。
- 检查 `7-图像/A-分镜画面` 中的本地图片路径是否存在。
- 投影 JSON / YAML / queue ledger / results。
- 机械生成或校验 `frame_uploads` 与 `generation_slots`：前者只记录 `shot_id/source_label -> uploaded_url`，后者记录 `UI 图N/imageList[n-1] -> uploaded_url -> shot_id/source_label`；若 UI 槽位可观测，必须保留 `slot_source` 并以 UI 图N 为准。
- 调用 `libtv` 命令、记录 `sessionId`、查询和下载结果。
- 机械写入默认 `prompt_fidelity_mode=strict_original`、`allow_libtv_prompt_optimization=false` 与 `transport_only_projection=true`。
- `build-upload-ledger.py --sync` 是 A 路线提交前的机械投影器：读取 submit plan / batch 中的已上传 URL，生成 `frame_uploads` 与 `generation_slots`，并把最终槽位同步回 manifest、plan、prompt fenced YAML 的 `分镜画面参照[]` 和远端提交的 `imageList`。它不生成 prompt 正文，只负责避免分镜 ID、URL 和 LibTV 图N 槽位错位。

禁止的脚本职责：

- 主创或扩写视频 prompt 正文。
- 改写 `5-分组` 的剧情、镜头顺序、角色关系或组边界。
- 未获用户显式 opt-in 时启用 LibTV 提示词优化、摘要、重排、补镜头或重新编排。
- 猜测不存在的图片引用或保留空图片槽位。
- 把 OSS 上传顺序直接当作 `reference_index` 或图N顺序真源。
- 在 draft prompt 中伪造空 `reference_index / uploaded_url`，或在未确认槽位前生成 final 远端提交。

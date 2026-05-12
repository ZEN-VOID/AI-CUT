# Scripts

本目录只承载机械辅助脚本，不承载创作主真源。

允许脚本承担：

- 读取 `4-分组/第N集.md` 并抽取 `group_id`、line range、hash。
- 检查 `6-图像/B-分镜故事板/第N集/images/<group_id>.*` 是否存在。
- 投影 `第N集-libtv-batch.yaml`、queue ledger、results JSON。
- 机械生成或校验 `storyboard_uploads` 与 `generation_slots`：前者只记录 `group_id/storyboard_sheet -> uploaded_url`，后者记录 `UI 图1/imageList[0] -> uploaded_url -> 故事板总参照`；若 UI 槽位可观测，必须保留 `slot_source` 并以 UI 图1 为准。
- 按 YAML 调用 `LIBTV_ACCESS_KEY credential check`、`create_session.py`、`upload_file.py + create_session.py`、`query_session.py`。
- 后台 worker pool、sessionId 回填、下载文件存在性校验。
- 机械写入默认 `prompt_fidelity_mode=strict_original`、`allow_libtv_prompt_optimization=false` 与 `transport_only_projection=true`。
- `build-upload-ledger.py --sync` 是 B 路线提交前的机械投影器：读取 submit plan / batch 中的故事板 uploaded URL，生成 `storyboard_uploads` 与 `generation_slots`，并把最终图1槽位同步回 manifest、plan、prompt fenced YAML 的 `故事板参照` 和远端提交的 `imageList[0]`。它不生成 prompt 正文，只负责避免故事板身份、URL 和 LibTV 图1 槽位错位。

禁止脚本承担：

- 改写、扩写或摘要分镜组正文作为 canonical video prompt。
- 未获用户显式 opt-in 时启用 LibTV 提示词优化、摘要、重排、补镜头或重新编排。
- 猜测缺失参照图。
- 把 OSS 上传动作直接当作 `reference_index` 或图1顺序真源。
- 在 draft prompt 中伪造空 `reference_index / uploaded_url`，或在未确认槽位前生成 final 远端提交。
- 在没有 queue ledger 的情况下批量提交异步视频任务。
- 让多个 worker 同时改写最终 `执行报告.md`。

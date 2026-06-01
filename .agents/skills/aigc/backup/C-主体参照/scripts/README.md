# Scripts

本目录只承载机械辅助脚本，例如解析 `5-分组`、校验图片路径、投影 LibTV submit plan、更新 queue ledger。

脚本不得承担以下职责：

- 创作或改写视频 prompt 主体。
- 从正文猜测 YAML 之外的主体。
- 选择剧情、镜头、表演或审美判断。
- 在缺少 `LIBTV_ACCESS_KEY credential check` 自检策略时伪造提交结果。

如后续新增脚本，必须提供 dry-run 模式，并把输出限定为索引、校验、计划或台账。

## Current Helpers

- `build-upload-ledger.py`：兼容旧 group package 的辅助脚本，可读取 `reference-manifest.json`、`libtv-submit-plan.json` 和旧式 `upload-XX-<name>.json` 生成或校验两层映射。compact 默认下，两层映射应并入 `reference-manifest.json.asset_uploads / generation_slots`；只有 full-trace 或旧包修复时才单独落 `upload-ledger.json`。`asset_uploads` 只记录 `yaml_name -> uploaded_url` 身份映射，不承载顺序真源；`generation_slots` 记录 `slot N / Portrait N / mixedList[n] -> uploaded_url -> yaml_name`，作为视频生成槽位顺序真源。若 submit plan 写有 `slot_source / ui_slot_source / generation_slot_source`，脚本会保留该来源；原始 OSS 上传顺序应另写 `oss_upload_index`，不得挤占生成槽位 `upload_index`。提交前必须使用 `--sync` 将 `generation_slots` 机械投影回 `reference-manifest.json`、`libtv-submit-plan.json`、`prompt.md` 的 fenced YAML 和 `libtv-submission.txt` 的 `mixedList`，避免只在校验阶段发现主体名和 URL 错位。
- `detect-libtv-stall.py`：读取 `query_session.py` 输出 JSON，机械检测 LibTV Agent-IM 是否卡在 `ask_user` / 等待用户 / 请稍候状态，并输出 post-submit gate verdict。该脚本不改写 prompt，不创建会话，不下载结果。
- `validate-reference-prompt-integrity.py`：读取单个 group package，机械校验 `reference-manifest.json`、`prompt.md`、`libtv-submit-plan.json`、`libtv-submission.txt` 的主体引用一致性、同画布 URL project scope、可选本地源图证据、重复 URL、远端本地路径泄漏和人工 `参照图N` 编号。支持 `--phase draft|final|auto`：draft 允许 prompt YAML 在 UI 槽位确认前保持未绑定；final 要求 YAML、`images[]`、`mixedList` 按 `reference_index` 顺序完全一致。该脚本只输出 verdict，不修正文案。
- `validate-post-submit-reference-order.py`：读取单个 group package 和 `query_session.py` 输出 JSON，机械校验远端 `create_generation_task.params.modeType`、`mixedList` / `imageList` 顺序是否严格等于本地最终 `generation_slots` / submit plan `images[]`，并检查远端 prompt 是否保留主体名、`reference_index` 与 URL 或系统图片 token 的邻近绑定。输出中必须包含 `expected_slots`，便于人工核对 `name -> reference_index -> Portrait N -> mixedList[n] -> uploaded_url`。未观测到生成工具调用时输出 `pending`；观测到后不一致则输出 `needs_rework`。若已有 UI 截图确认槽位，应先回刷 submit plan / prompt，再运行该脚本。

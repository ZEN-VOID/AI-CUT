# Scripts

本目录只承载机械辅助脚本，例如解析 `4-分组`、校验图片路径、投影 LibTV submit plan、更新 queue ledger。

脚本不得承担以下职责：

- 创作或改写视频 prompt 主体。
- 从正文猜测 YAML 之外的主体。
- 选择剧情、镜头、表演或审美判断。
- 在缺少 `LIBTV_ACCESS_KEY credential check` 自检策略时伪造提交结果。

如后续新增脚本，必须提供 dry-run 模式，并把输出限定为索引、校验、计划或台账。

## Current Helpers

- `detect-libtv-stall.py`：读取 `query_session.py` 输出 JSON，机械检测 LibTV Agent-IM 是否卡在 `ask_user` / 等待用户 / 请稍候状态，并输出 post-submit gate verdict。该脚本不改写 prompt，不创建会话，不下载结果。
- `validate-reference-prompt-integrity.py`：读取单个 group package，机械校验 `reference-manifest.json`、`prompt.md`、`libtv-submit-plan.json`、`libtv-submission.txt` 的主体引用一致性、上传缓存源图指纹、重复 URL、远端本地路径泄漏和人工 `参照图N` 编号。该脚本只输出 verdict，不修正文案。

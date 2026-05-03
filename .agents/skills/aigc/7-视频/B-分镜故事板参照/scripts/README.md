# Scripts

本目录只承载机械辅助脚本，不承载创作主真源。

允许脚本承担：

- 读取 `4-分组/第N集.md` 并抽取 `group_id`、line range、hash。
- 检查 `6-图像/B-分镜故事板/第N集/images/<group_id>.*` 是否存在。
- 投影 `第N集-libtv-batch.yaml`、queue ledger、results JSON。
- 按 YAML 调用 `LIBTV_ACCESS_KEY credential check`、`create_session.py`、`upload_file.py + create_session.py`、`query_session.py`。
- 后台 worker pool、sessionId 回填、下载文件存在性校验。

禁止脚本承担：

- 改写、扩写或摘要分镜组正文作为 canonical video prompt。
- 猜测缺失参照图。
- 在没有 queue ledger 的情况下批量提交异步视频任务。
- 让多个 worker 同时改写最终 `执行报告.md`。

# Scripts

本目录只承载机械辅助脚本，例如解析 `4-分组`、校验图片路径、投影 Dreamina submit plan、更新 queue ledger。

脚本不得承担以下职责：

- 创作或改写视频 prompt 主体。
- 从正文猜测 YAML 之外的主体。
- 选择剧情、镜头、表演或审美判断。
- 在缺少 `dreamina user_credit` 自检策略时伪造提交结果。

如后续新增脚本，必须提供 dry-run 模式，并把输出限定为索引、校验、计划或台账。

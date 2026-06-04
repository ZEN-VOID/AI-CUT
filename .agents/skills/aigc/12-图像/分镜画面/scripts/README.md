# Scripts Boundary

本目录仅承载机械辅助脚本说明。当前技能没有必须执行的本地脚本。

允许脚本做：

- 读取 `10-分组/第N集.md` 并切出普通 `## x-y-z` 完整组块。
- 统计组内普通 `分镜N` 数量。
- 生成 `group-index.json`、`reference-manifest.json`、`imagegen-plan.json` 的结构化投影。
- 校验本地图片路径存在性、输出路径是否会覆盖、结果数量是否等于 `shot_count`。

禁止脚本做：

- 生成或扩写 prompt 主创正文。
- 判断剧情、画面表现、角色一致性或审美质量。
- 改写 `10-分组` 正文。
- 在 provider 超过单次多图上限时静默拆组。

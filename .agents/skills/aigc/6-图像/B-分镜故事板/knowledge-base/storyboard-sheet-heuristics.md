# Storyboard Sheet Heuristics

## Stable Heuristics

- 组级 storyboard 的 prompt 越贴近 `4-分组` 原文，越容易保留镜头完整性；额外摘要反而容易丢镜头。
- 固定英文开头应保持单段原文，避免模型误把三条要求当作画面文本。
- `角色 / 场景 / 道具` 的 YAML 列表已经是上游聚合后的主体清单，默认比正文扫描更可靠。
- 多视图图片适合 storyboard 连续性；主图更适合单个主体的造型锚定。二者同时存在时，多视图优先。
- 只有 JSON 设计稿时，应把主体列为 missing，而不是把 JSON 交给 imagegen 当图片参照。

## Risk Patterns

| pattern | risk | mitigation |
| --- | --- | --- |
| 分镜数过多 | 单图网格过密，细节不可读 | 记录 `layout_risk`，必要时建议分页 |
| 缺少场景图 | 空间一致性下降 | 保留 prompt 主体，报告缺图 |
| 同名主体多候选 | 参照错绑 | 进入 ambiguous，不自动选择 |
| 批量 rerun 未锁覆盖策略 | 覆盖已有成图 | 默认跳过已有文件，除非用户要求 replace |

# Group Source Extraction Contract

本文件定义 `D-主板混合参照` 如何从 `4-分组` 提取分镜组正文与组底 YAML。

## Source

- Canonical source: `projects/aigc/<项目名>/4-分组/第N集.md`
- Group heading: Markdown 二级标题 `## x-y-z`
- Connector heading: Markdown 二级标题 `## x-y-z~x-y-z`，默认忽略
- Group body: 当前 `## x-y-z` 到下一个 `## x-y-z`、下一个 `## x-y-z~x-y-z` 或文件结尾之前的全部正文
- Subject baseline: 组尾 fenced YAML 中的 `角色 / 场景 / 道具`
- Duration baseline: 组尾 fenced YAML 中的 `时长估算`

## Extraction Rules

1. 每个目标 `group_id` 必须唯一匹配一个 `## x-y-z` 标题。
2. 提取正文时保留原分镜顺序、镜头描述、动作、音效、场景与 YAML，默认跳过 `## x-y-z~x-y-z` 连接件块。
3. 不得摘要、扩写或改写剧情事实。
4. 若 YAML 缺失，D 不能执行主体参照绑定；可生成 `blocked` 或按用户要求降级到 B 路线。
5. 同步提取组底 YAML 的 `时长估算`，形成 `duration_estimate_seconds`；若缺失则按组内 `分镜明细` 秒数求和估算，区间时长优先取上限；仍无法确定时回退 15 秒并记录 `duration_source=fallback_default`。
6. 输出 `第N集-hybrid-group-index.json` 时记录 `group_id`、source heading、line range、shot count、body hash、YAML subjects、duration source 和 duration estimate。
7. 连接件不生成 `group_id`、不绑定故事板或主体图、不创建 LibTV job、不命名 `<上组~下组>.mp4`；连接件块的 `时长` 不参与分镜组视频时长估算；未来由单独手动视频连接 skill 处理。
8. 最终提交给 LibTV 的 `duration_hint` 由 handoff 层按 `clamp(duration_estimate_seconds, 4, 15)` 生成；小于等于 4 秒用 4 秒，大于等于 15 秒用 15 秒。

## Failure Handling

| symptom | repair |
| --- | --- |
| `group_id` 不唯一 | 阻断并要求用户指定或修复上游 |
| YAML 缺失 | 标记 `missing_subject_yaml`，不得从正文猜主体 |
| 正文为空 | 阻断该组，写入 report |
| 连接件进入正文或 prompt | 按连接件标题重新切块并忽略 |
| 用户要求改剧情 | 转回上游分组修复，不在 D 内改写 |

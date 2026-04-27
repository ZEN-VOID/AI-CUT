# Group Source Extraction Contract

本文件定义 `D-主板混合参照` 如何从 `4-分组` 提取分镜组正文与组底 YAML。

## Source

- Canonical source: `projects/aigc/<项目名>/4-分组/第N集.md`
- Group heading: Markdown 二级标题 `## x-y-z`
- Group body: 当前 `## x-y-z` 到下一个 `## x-y-z` 之前的全部正文
- Subject baseline: 组尾 fenced YAML 中的 `角色 / 场景 / 道具`

## Extraction Rules

1. 每个目标 `group_id` 必须唯一匹配一个 `## x-y-z` 标题。
2. 提取正文时保留原分镜顺序、镜头描述、动作、音效、场景与 YAML。
3. 不得摘要、扩写或改写剧情事实。
4. 若 YAML 缺失，D 不能执行主体参照绑定；可生成 `blocked` 或按用户要求降级到 B 路线。
5. 输出 `第N集-hybrid-group-index.json` 时记录 `group_id`、source heading、line range、shot count、body hash、YAML subjects。

## Failure Handling

| symptom | repair |
| --- | --- |
| `group_id` 不唯一 | 阻断并要求用户指定或修复上游 |
| YAML 缺失 | 标记 `missing_subject_yaml`，不得从正文猜主体 |
| 正文为空 | 阻断该组，写入 report |
| 用户要求改剧情 | 转回上游分组修复，不在 D 内改写 |

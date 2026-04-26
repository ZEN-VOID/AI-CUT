# Query Heuristics

本文件保存 `$aigc-query` 可复用经验。强制执行规则仍以 `SKILL.md`、`references/`、`steps/`、`types/` 与 `review/` 为准。

## Heuristics

- 查询状态时先回答“项目是否可定位”，再回答“阶段跑到哪”。
- 查询阶段结果时先看当前中文阶段目录；只有 current carrier 缺失或用户点名旧路径时才读 legacy。
- 查询图像/视频时要分清阶段工件、provider 任务记录和最终媒体文件；三者不能互相替代。
- `reports/` 适合保存一次性查询报告，但不成为状态真源。
- registry/routes 与本地目录不一致时，回答应拆为“制度层声明”和“文件系统现状”两栏。

## Common Pitfalls

| pitfall | prevention |
| --- | --- |
| 搜到旧英文路径就直接回答 | 同时查 current canonical path，并标注 legacy |
| 把 `agents/openai.yaml` 当技能执行合同 | 元数据只回答入口提示，不回答业务真源 |
| 把 `CHANGELOG.md` 当当前状态 | changelog 只提供时间序线索，不替代 `STATE.json` |
| 把空目录当完成 | 空目录只证明阶段槽位存在 |

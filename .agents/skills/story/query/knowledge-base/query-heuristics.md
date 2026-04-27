# Query Heuristics

本文件保存 `$story-query` 可复用查询经验。强制执行规则仍以 `SKILL.md`、`types/`、`steps/` 和 `review/` 为准。

## Heuristics

- `query/` 的第一动作不是搜词，而是判定用户问的是哪种 truth。
- 带“原计划、安排、落在哪章”的问法，优先看三层 planning；compat MAP 只能回退。
- 带“现在、当前、默认有效”的问法，优先看 Cards `current_state`，再用 `STATE.json` 和 `index.db` 补证。
- 带“已经、实际、最终、兑现到哪”的问法，必须找 actualization sidecar、context-return artifact 和 PASS 证据。
- 角色问题里，`experience_timeline` 回答“这个人怎么一路变成这样”，planning 回答“事件按什么顺序安排”。
- `STATE.json.workflow_runtime.workflow_state` 是当前 run 兼容断点；`execution_state` 是全阶段执行真源；`task_log` 是事件证据链。
- 普通查询默认不需要加载 `tag-specification.md`；只有用户明确问标签或手动补标才读它。
- 若 query 结果需要同时引用计划与实绩，优先用“原计划 / 当前态 / 已验证实绩”三栏拆开。

## Migration Note

2026-04-27 的 Skill 2.0 升级把旧 `SKILL.md` 中的步骤、判型、输出样式和质量门禁拆到 `steps/`、`types/`、`templates/`、`review/`。后续新增细则时优先写入对应 owner，不要把入口文件重新写成大全。

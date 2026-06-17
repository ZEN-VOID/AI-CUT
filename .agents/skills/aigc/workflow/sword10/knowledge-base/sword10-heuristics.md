# Sword10 Heuristics

本文件保存 `sword10` 可检索经验。稳定且必须执行的规则应晋升到 `SKILL.md`、`references/` 或 `review/`。

## Heuristics

- 对批量集数，最有用的状态粒度是 `stage x episode`，不是按 subagent 日志逐行回放。
- 失败报告要给 `retry_start_stage`，否则用户只能重新跑全链路。
- `8-分组` 的风格上下文应来自 `2-美学/类型风格.md`、`2-美学/画面基调/全局风格协议.md` 和当前集优先/项目级回退的相关风格协议，preflight 应把这些作为额外输入检查。
- 如果同一集在上游阶段已有较新产物，续跑前应保留 reused/regenerated 标记，避免误以为全链路重跑。

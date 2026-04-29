# Scene Card Review Contract

| dimension | pass condition |
| --- | --- |
| route | `module_route` 指向 `场景卡` |
| advisor_consultation | 显式启用 subagents 时，已按项目 `team.yaml` 顾问 roster 生成 `advisor_consultation_packet`，且结论已转成场景功能、规则代价、危险或返场策略；未启用时有明确不适用说明 |
| function | 场景有叙事功能，不只是布景 |
| rules | `rule_and_risk` 与 `compatible_roles` 成立 |
| reuse | `scene_links` 与 `repeat_use_strategy` 可支撑返场 |
| trace | `loaded_references` 包含本 `SKILL.md`、`CONTEXT.md` 与本地模板 |

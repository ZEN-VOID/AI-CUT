# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `review/` 的经验层知识库，不是过程日志。
- 每次调用 `review/` 时，应与 `SKILL.md` 一起加载，用于识别最新系统中的常见脱节点：`4-Validation` intake、SQLite 持久化、`STATE.json` 摘要回写、`5-Loopback` handoff。
- 冲突优先级固定为：用户显式请求 > AGENTS.md / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| `review/` 绕过 `4-Validation` 直接起 checker | skill contract | 回到 `4-Validation` 创建新隔离团队 | 在 `review/SKILL.md` 写死 intake gate | 直接调用 `/story-review` 时仍先进入 `4-Validation` |
| 报告内容与聚合结果不一致 | aggregation | 以上游聚合结果重建报告 | 禁止在 `review/` 层主观重估分数或改写 issue | 报告中的 `issues / severity_counts / overall_score` 可追溯 |
| `anti_ai_force_check` 等新质控字段只写进文档和 JSON 示例，SQLite 实际没存 | persistence contract | 同步修 `index_manager.py`、`index_reading_mixin.py`、CLI 解析与测试 | 凡是一等趋势字段，必须“文档 + schema + save/read + tests”四处同改 | `get-recent-review-metrics` 可直接返回四个风险字段 |
| 风险字段已落库，但 `STATE.json.review_checkpoints` 与趋势报告仍看不见 | state/index observation | 给 review checkpoint 增加四个轻量风险字段，并让趋势报告直接展示风险雷达 | 一等风险字段至少要贯穿 `review_metrics`、`review_checkpoints`、趋势报告三层观察面 | resume/status/trend 都能直接看到 `anti_ai_force_check / spoiler_risk / contrivance_risk / cold_commentary_risk` |
| Step 2 参考路径仍指向旧上级目录，导致 shared reference 实际读不到 | path contract | 改为 repo-local 正确路径 | 在技能中优先使用 `${REPO_ROOT}/.agents/skills/story/...` 绝对约定 | shell 中能成功读取 shared reference |
| `review/` 试图代替 `5-Loopback` 做 gate 裁决或 actualization 决策 | stage split contract | 把 `review/` 收回到报告/持久化/升级层 | 在 `SKILL.md` 写死 `4-Validation` 判 gate、`5-Loopback` 写 truth、`review/` 只做 handoff summary | `review_handoff_summary` 不改写 `validation_status` |
| 修复后沿用旧评估结果继续推进 | workflow closure | 触发新一轮 `4-Validation` 复核 | 在 Completion Gate 写死“修复后重新隔离评估” | 修复后存在新的团队输出与报告 |
| 审查报告已经落到业务目录，但 task dir 没有形成对应的治理证据回指 | governance artifact observation | 在 `review/` 合同中把 task dir 视为治理承接层，要求报告层与证据层互相回指 | 让 `Validation/*.md` 业务报告与 `<run_id>` task artifacts 保持可追溯关系，避免出现两套互不相认的报告路径 | report、state、task dir 三处都能定位同一轮审查结论 |

## Repair Playbook

1. 先确认本轮输入是否来自新的 `4-Validation` 团队。
2. 再检查 `validation_status / routing_decision / handoff_targets` 是否完整，且未被 `review/` 私自改写。
3. 若落库字段与文档不一致，优先修 SQLite schema、save/read 逻辑和测试，不在报告模板层打补丁。
4. 若引用资料失败，优先排查 repo-local 绝对路径和 holomap/state/index 三类数据源边界。
5. 若 critical 触发修复，立即把本轮结果从“可 actualize”降为“待复核”，修后重新进入 `4-Validation`。

## Reusable Heuristics

- `review/` 的职责是“承接、落盘、升级、桥接”，不是“再做一遍判断”。
- 只要某个字段要进入趋势统计，它就必须成为 SQLite 正式列，而不是停留在示例 JSON 或 `notes`。
- `validation_status` 的所有权只在 `4-Validation`；`review/` 只能说明它、不能改写它。
- `STATE.json.review_checkpoints` 最适合保存“章节范围 + 报告路径 + 时间戳”的轻量摘要，不适合塞回完整 issue 列表。
- 轻量摘要不等于盲摘要；凡是需要被 `resume / status / trend` 快速识别的一等风险字段，应与报告路径一起回写到 `review_checkpoints`。
- 解释规划影响时，优先读 `全息地图.json`；解释运行态时，优先读 `STATE.json`；解释历史趋势时，优先读 `index.db.review_metrics`。
- 当文档已经宣称“新字段是正式字段”，第一反应应是去核对 schema / save / read / tests 四层是否真的同步，而不是只修文字。
- 正式字段若只存在数据库、却不出现在观察面，实际仍会退化成“隐形字段”；至少要让趋势报告与 state checkpoint 能看见它。
- 业务报告和治理工件都叫“report”时，最稳的区分是：`Validation/*.md` 面向书项目阅读，`<run_id>/validation_report.md` 面向三省闭环审计。

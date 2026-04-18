# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `query/` 的经验层知识库，不是过程日志。
- 每次调用 `query/` 时，应自动预加载本文件，用于 truth-role 判定、真源选路、冲突拆分与失败闭环。
- 冲突优先级固定为：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- action_policy:
  - ok: 优先更新 Type Map / Repair Playbook / Reusable Heuristics。
  - warn: 对当前技能上下文做定向压缩与结构整理。
  - critical: 先归档旧案例，再继续大规模追加。

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 查询到章节规划、任务、线索、伏笔时仍只读 `STATE.json` 或旧 `大纲/` | skill contract / data-flow doc | 把规划类问题默认入口切到 `Planning/全息地图.json` | 在 `SKILL.md` 与 `system-data-flow.md` 固定 holomap-first | 规划类查询说明明确写出 holomap 为优先数据源 |
| 把 `planned_state` 当成“已经发生的事实” | truth-role contract | 改为同时检查 `actualization + loopback artifact + validation PASS` | 在 `SKILL.md` 固定 `planned/current/validated_actual` 三分法 | 查询“已经发生了吗”时不会再拿计划冒充结果 |
| 把 `Cards.core` 当作当前默认有效状态 | cards contract | 当前态问题先看 `current_state`，再用 `history` 和 `state/index` 补证 | 在 query 合同里写死 `core != current_state` | “现在怎样了”类问题优先命中 `current_state` |
| 问角色成长历程时只给当前快照 | cross-stage semantic split | 读取 `experience_timeline + history + state_changes` | 把“事件时间”与“经历时间”分开写进查询规则 | 角色弧光查询能同时给出现在与形成过程 |
| 实绩查询忽略 `5-Loopback` 的 PASS-only gate | stage contract | 把 `actualization` 与 `第N集.loopback.json` 设为必须校验项 | 在 query 规则中写明“无 PASS 证据只能回答尚无 validated actual” | 实绩类回答会带 `validation_ref` 或明确缺口 |
| 把 XML 标签规范当成普通剧情查询主入口 | query intent routing | 降级 `tag-specification.md` 为显式手动补标场景 | 在 L2 引用策略中固定“标签查询 only on demand” | 普通角色/剧情查询不再误读标签规范 |
| 节奏、评分、风险查询仍停留在老式“Strand/紧急度”两类 | review data-flow | 补读 `review_metrics / reading_power / review_checkpoints` | 固定质量查询入口包含 `status + index review metrics` 双层 | 能回答“最近质量趋势”和“风险项” |
| 任务进度、恢复点、最近 run 查询仍只读旧独立状态文件或完全无入口 | execution truth contract | 把执行态问题切到 `STATE.json.workflow_runtime.{execution_state,task_log}` | 在共享 data-flow 文档明确 `STATE.json` 内联执行态分工 | 能回答“当前跑到哪了 / 最近哪个 stage 卡住了 / 最新恢复点在哪” |
| query 数据流文档仍把 drafting 真源写成 `Drafting/chNNNN/chapter-root.md` | drafting data-flow drift | 改回 `3-Drafting/第N集.md + 写作日志.yaml` | 在 `system-data-flow.md` 固定新 drafting 根文件与跨集连续性加载规则 | 查询解释 drafting 时不再混用旧路径 |

## Repair Playbook

1. 先识别这次问题是在问 `planned`、`current`、`validated_actual`、`quality` 还是 `manual-spec`。
2. 若答案来源混乱，先回到 truth-role 判定，而不是先继续补读更多文件。
3. 若涉及“已经发生了吗”，先检查 `MAP.actualization` 与 loopback artifact，再看 `validation_ref`。
4. 若涉及“现在怎样”，先看 `Cards.current_state`，再用 `STATE.json` 和 `index.db` 校验。
5. 若涉及“怎么变成现在”，优先给 `experience_timeline/history/state_changes` 的组合答案。
6. 若发现来源冲突，明确写出各来源说了什么、当前谁优先、谁可能过期。
7. 只有在真源合同确认无误后，才修本次具体回答。

## Reusable Heuristics

- `query/` 的第一动作不是搜词，而是先判断用户要的是哪种 truth。
- 凡是带“原计划、安排、落在哪章”的问法，优先看 `MAP planned_state`。
- 凡是带“现在、当前、默认有效”的问法，优先看 `Cards.current_state` 与 `STATE.json`。
- 凡是带“已经、实际、最终、兑现到哪”的问法，必须去找 `actualization + loopback + PASS 证据`。
- 角色问题里，`experience_timeline` 回答“这个人怎么一路变成这样”，`MAP` 回答“那些事件按什么顺序发生”。
- `STATE.json` 是快照，不是总真源；`index.db` 是证据层，不是对象设计层；`Cards` 是对象真源，不是计划真源。
- `STATE.json.workflow_runtime.workflow_state` 是当前 run 兼容断点；`STATE.json.workflow_runtime.execution_state` 是全阶段执行真源；`STATE.json.workflow_runtime.task_log` 是事件证据链。
- 普通查询默认不需要加载 `tag-specification.md`；只有当用户明确问“标签怎么写 / 手动补标怎么做”时才读它。
- 若 query 结果需要同时引用计划与实绩，优先用“原计划 / 已验证实绩 / 当前状态”三栏拆开，最不容易误导。
- 卫星拓扑发生增删时，`query/` 的 stage-position 文案与 data-flow 图也要同步缩表，不能继续挂着已下线的 peer。
- 如果 `3-Drafting` 改成了新的正文根文件路径，query 的 truth-layer 和 data-flow 文档要一起改，不然查询会默认读错 drafting 真源。

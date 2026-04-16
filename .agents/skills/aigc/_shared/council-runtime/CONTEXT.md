# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/_shared/council-runtime` 的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/_shared/council-runtime/module-spec.md` 时，应预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 后续阶段忘记读取 `team.yaml` | 共享运行时层 | 在阶段根技能强制先读项目根 `team.yaml` | 用共享 `council-runtime/module-spec.md` 作为单一真源 | 阶段执行前能判断顾问团是否启用 |
| 多个阶段各自复制一套顾问团规则 | 真源治理层 | 把共性规则上收至 `_shared/council-runtime/` | 阶段根技能只保留本阶段适配，不再平行维护通用规则 | 共性规则只在共享目录维护 |
| `评审` 过早参与前置发散 | 角色边界层 | 将 `评审` 固定到 `5-Image / 6-Video` 的阶段级 `validation-report.md` 前后 | 在共享运行时写死 `pre_and_post_validation_gate` 与对应阶段归属 | 评审不再抢前置创作职责 |
| `2-Global / 3-Detail / 4-Design` 写完 canonical 就直接结束，没有再按 `roles.supervision` 做 stage-end refine | 共享阶段末端运行时层 | 在 shared `module-spec.md` 明确“canonical 首次落盘后还要再做一次监制会审” | 让阶段根技能统一回指 shared refine 规则，而不是各自发明一套“写完后看看要不要再审”的 prose | 当前阶段的监制加强都在同一 shared runtime 下解释 |
| `roles.supervision.source_skill_refs` 被拿来直接充当 reviewer | reviewer 路由层 | 强制把 `source_skill_refs` 降级为 reviewer 匹配提示 | 在 shared runtime 写死“最终 reviewer 真源必须落在 `.agents/skills/team/**/SKILL.md`” | 阶段 skill 与 reviewer skill 不再混层 |
| 未被 `module-spec.md` 回指的提示词模板留在共享目录 | 共享模板治理层 | 删除孤立模板 | 共享运行时模板必须被 `module-spec.md` 声明为 canonical source，否则不得长期保留 | `_shared/council-runtime/` 只保留真实消费的规范载体 |

## Reusable Heuristics

- 对跨阶段顾问团机制来说，最重要的不是“顾问很多”，而是“团队真源只有一份、运行时只有一套”。
- `0-Init` 之外的共享运行时不再默认调度 `策划`；这里的前置顾问以 `监制` 为主，`评审` 只负责 `5-Image / 6-Video` 收口。
- 对跨阶段顾问运行时，最稳的分层是：`0-Init` 负责策划 kickoff，`2-Global / 3-Detail / 4-Design` 由监制前置介入并在 canonical 首次落盘后再做一次 stage-end refine，`5-Image / 6-Video` 由评审卡最终闸门。
- 共享运行时里，`roles.supervision.members` 是 stage-specific reviewer 的第一真源；`team_setup.shared_agents` 是补充池；`roles.supervision.source_skill_refs` 只负责告诉系统“这是哪个阶段域”，不该直接拿来当 reviewer。
- 只要 `runtime_policy.use_subagents_by_default == true` 且 reviewer 已稳定命中，shared runtime 的默认语义就应是真实启动 subagents，而不是主 agent 自己模拟顾问团。
- 共享运行时目录不应保留未被规范合同引用的提示词草稿；如果某模板需要长期存在，必须先在 `module-spec.md` 中声明消费方式与真源身份。

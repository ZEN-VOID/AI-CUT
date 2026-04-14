# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global` 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/2-Global/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-13

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-Global` 只有子技能，没有父级 stage 合同 | 阶段真源层 | 补父级 `SKILL.md + CONTEXT.md`，固定路由、验收与 handoff 边界 | 把 `2-Global` 视为 stage-local parent skill，而不是子技能容器目录 | 根 `aigc` 与本地阶段事实一致 |
| 用户只要求一个子技能，却被默认全量调度 | 父级路由层 | 回到父 skill 做 selective dispatch | 在父 `SKILL.md` 固化“未命中子技能不得参与聚合” | validation report 只登记本轮命中输出 |
| `0-Init` 抢占 `3-分组` 主输入地位 | 输入优先级层 | 重新锁 `1-Planning/3-分组` 为第一主输入根 | 在父 skill 和子技能共同固化 `3-分组 > 0-Init` | 子技能成稿都能回指 grouped script |
| 阶段级 validation 缺失，无法判定是否可交给 `3-Detail` | 阶段闭环层 | 写回 `projects/<项目名>/2-Global/validation-report.md` | 在父 skill Convergence Contract 中固定 validation 必写 | 阶段结束时一定有验收结论 |
| `组间设计 seed` 还没有稳定链路，却被误写成已完成 | handoff 治理层 | 明确标记为 reserved handoff / blocked readiness | 在父层合同固定“当前不可伪造 shared root 写回” | 不会再出现假 ready |
| `team.yaml` 已启用却绕过监制/评审 gate | 共享运行时层 | 回到 `council-runtime` 做前置顾问与评审判定 | 将 `2-Global` 的 council gate 固定为父层前置节点 | `validation-report.md` 有 council decision note |

## Repair Playbook

1. 先检查 `projects/<项目名>/1-Planning/3-分组/` 是否完整存在。
2. 再检查是否只是局部子技能任务，还是需要阶段级 route / validation。
3. 若 `team.yaml.enabled == true`，先跑 `council-runtime` gate，再进入子技能。
4. 汇总时只登记本轮命中子技能输出，不给未运行子技能补占位。
5. 最后明确 `3-Detail` handoff readiness 是否 ready、partial 还是 blocked。

## Reusable Heuristics

- `2-Global` 最稳的父层定位不是“再写一份总文案”，而是“统一输入、调子技能、做阶段验收、给下一阶段明确入口”。
- 子技能越多，父 skill 越要坚持 selective dispatch；否则阶段根很快会退化成“任何局部修订都全量重跑”的噪音入口。
- 对 `2-Global` 来说，`0-Init` 最适合定义长期边界，`3-分组` 最适合定义实际叙事已显现出的全局设计需求；顺序反了，输出就会漂。
- 当 `导演意图 / 组间设计 seed` 链路尚未重建时，最稳的做法是显式报告 reserved / blocked，而不是为追求“看起来闭环”去伪造 shared root。
- `validation-report.md` 是 `2-Global` 父层最关键的 stage artifact；没有它，子技能输出再好，也仍然缺阶段级闭环。 

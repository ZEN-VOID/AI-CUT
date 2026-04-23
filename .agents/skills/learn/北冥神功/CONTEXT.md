# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `北冥神功` 的经验上下文知识库，不是执行日志。
- 每次调用本技能时，必须与同目录 `SKILL.md` 一起加载。
- 冲突优先级：用户显式请求 > 仓库 `AGENTS.md` / 元规则 > `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- action_policy:
  - ok: 优先更新 Type Map / Repair Playbook / Reusable Heuristics。
  - warn: 对类型表和案例做收束，避免把本文件写成升级流水账。
  - critical: 先晋升稳定模式到 `SKILL.md` 或 `references/`，再继续追加案例。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 升级点被直接塞进目标 `SKILL.md`，但其实只是经验性启发 | 吸收落点裁决层 | 改回目标 `CONTEXT.md` 或本技能 `CONTEXT.md` | 固定先做 `point_type` 判型，再决定 landing set | 经验型内容不再污染主合同 |
| 只修目标 leaf，没有检查父级、siblings 或 shared carrier | 技能组上下文层 | 回补 group scan 与 parity scope | 把 `N3-GROUP-CONTEXT-SCAN` 设为硬门槛 | 相关 sibling / shared carrier 同步到位 |
| 升级点改变了触发语义，但 registry/routes 没更新 | 发现与路由层 | 同轮补 `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml` | 在执行硬规则中固定 discovery sync | 新技能可被发现，旧触发不漂移 |
| 共享 schema 或 runner 改了，但只修一条链 | parity 层 | 横向补齐 sibling runner / validator / template | 把 `parity_targets[]` 变为显式字段 | 同级链路都接受新口径 |
| 写了改动，却没有把经验沉淀到目标 skill 或本技能 | learning deposition 层 | 追加目标 `CONTEXT.md` / 本技能 `CONTEXT.md` / `CHANGELOG.md` | 固定 `double_learning` 闭环 | 本轮升级拥有可复用经验 |
| 升级点其实需要长细则或判型表，却硬塞在主 `SKILL.md` | 真源分层层 | 下沉到 `references/` 并从主合同回链 | 固定 skeleton-first 原则 | 主 `SKILL.md` 仍可扫描 |

## Repair Playbook

1. 先确认本轮失败属于“落点错了”“同步范围漏了”“parity 漏了”还是“学习沉淀缺失”。
2. 回看目标 skill 自己的 `SKILL.md + CONTEXT.md`，再回看其父级、siblings、shared carrier 与 registry/routes。
3. 重新做一次 `upgrade_point -> point_type -> landing_set -> sync_scope`。
4. 优先修源层载体，再修局部文案或单次输出。
5. 把局部经验写回目标 `CONTEXT.md`，把跨 skill 吸收模式写回本文件。

## Reusable Heuristics

- `skills-update` 最容易犯的错不是“不会改”，而是“改得太快，没先判型”。
- 对 skill 升级来说，`目标 skill 现状` 和 `技能组上下文` 缺一不可；只看前者会局部最优，只看后者会空泛。
- 若升级点改变的是“什么时候该触发这个 skill”，往往不止要改 `description`，还要顺带改 registry/routes。
- 若升级点改变的是“这个 skill 怎么执行”，优先检查是否应落 `SKILL.md` 骨架 + `references/`，而不只是补一段经验。
- 若升级点来源于一次真实失败，最稳的落点通常是：目标 skill 收局部修复经验，本技能收跨技能吸收策略。
- 任何牵动 shared schema、runner、validator 或 template 的升级，都要怀疑存在 sibling parity 风险。

## Case Log

> 仅记录里程碑级案例，不记录过程流水账。

### Case-001

- milestone_type: new_skill_bootstrap
- outcome: 从空目录启动 `北冥神功`，直接建立“目标 skill 现状扫描 + 技能组上下文扫描 + 升级点判型 + 落点裁决 + 双重学习沉淀”的完整吸收闭环。
- root_cause_or_design_decision: 用户需求不是要一个泛泛的“如何升级 skill”说明，而是要一个专门处理 `待升级skill + 升级点` 并能把外部知识有机吸收进技能体系的 learn 型技能。
- final_fix_or_heuristic: learn 型 skill 的核心不在“多会讲道理”，而在于把 `landing_set / sync_scope / parity_targets / learning_writebacks` 这些字段显式化。
- prevention_or_replication_checklist:
  - [x] 目标 skill 现状扫描成为硬门槛
  - [x] 技能组上下文扫描成为硬门槛
  - [x] `upgrade_point -> landing_set` 有 reference 支撑
  - [x] 同轮补 registry/routes 接入
  - [x] 建立 target + self 双重 learning deposition
- evidence_paths:
  - `.agents/skills/learn/北冥神功/SKILL.md`
  - `.agents/skills/learn/北冥神功/CONTEXT.md`
  - `.agents/skills/learn/北冥神功/references/upgrade-point-absorption-map.md`
- user_feedback_or_constraint: 用户明确要求建立一套针对 `skills-update` 的有效自学习机制，并强调必须研究目标 skill 当前配置状态与所在技能组序列整体。

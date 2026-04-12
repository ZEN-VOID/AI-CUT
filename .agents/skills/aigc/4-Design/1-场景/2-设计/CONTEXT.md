# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/1-场景/2-设计` 的经验层知识库，不是过程日志。
- 调用本子技能时，应在 `aigc -> 4-Design -> 1-场景` 根链之后加载本文件。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 绕过 `1-清单` 直接从导演 JSON 发明场景设计 | 输入真源层 | 先回到 `1-清单` 产出 scene catalog，再继续设计 | 在 `execution-flow` 固化 `scene catalog` 为首选输入 | `2-设计` 不再重建对象池 |
| subagents 各自输出平行主稿，父 skill 无法收束 | handoff 合同层 | 强制只返 `agents_plan + patch / note / report` | 在 team 合同与 agent 合同中固化 `parent writeback only` | 只有父 skill 写最终设计文件 |
| 场景设计只剩风格词堆，没有空间结构与镜头锚点 | 字段设计层 | 回到模板字段，强制补齐空间原型、结构、陈设、动线、镜头 | 在模板与 Field Master 中锁定最小字段集 | 场景卡可直接支撑下游消费 |
| reviewer / auditor 缺位，场景设计断开全局风格与导演意图 | 审计闭环层 | 补 `审景师` 与 `真源审计` 两道 gate | 在 team.md 固化 mixed tranche + veto 规则 | 设计稿可给出 review/audit trace |
| 输出仍沿用旧仓 `output/影片/...` 口径 | runtime 落点层 | 改回 `projects/<项目名>/4-Design/1-场景/2-设计/` | 在 `output-template` 与 `openai.yaml` 固化当前路径 | 产物落点符合当前仓合同 |

## Repair Playbook

1. 先检查 `1-清单/第N集.json` 是否存在且可用。
2. 再检查 `2-Global` 的全局风格 / 类型指导 / 导演意图是否齐全。
3. 然后检查 `mission_brief` 和 `scene_dispatch_plan` 是否只命中本轮需要的场景。
4. 再检查 specialist patch 是否能被父 skill 聚合进模板字段。
5. 最后检查 `审景师` 与 `真源审计` 是否留下 review / audit note。

## Reusable Heuristics

- 场景设计最稳的输入顺序是：先 scene catalog，再全局风格，再回看导演镜头证据；不要把这三层反过来。
- `设计统筹` 负责缩范围，`空间逻辑/建筑设计师/布景师` 负责补字段，`审景师/真源审计` 负责拦漂移；这三层不能混写。
- 场景卡对下游最有价值的不是辞藻，而是“空间怎么搭、镜头怎么看、哪些误读必须禁止”。
- 只要模板字段还没锁稳，就不要让 subagents 直接写整篇主稿。
- 对场景设计来说，`agents_plan` 适合承载 dispatch plan、字段补位顺序与审景返工摘要；canonical 设计稿仍只能由父 skill 聚合写回。

## Case Log

### Case-20260412-AIGC-SCENE-DESIGN-SUBAGENT-UPGRADE

- milestone_type: source_contract_change
- outcome: 把空壳的 `.agents/skills/aigc/4-Design/1-场景/2-设计` 升级为由父 skill 收束、场景设计组 subagents 分工的可执行子技能包。
- root_cause_or_design_decision: 目录先前只有空壳，没有 `SKILL.md / CONTEXT.md / CHANGELOG.md / agents/openai.yaml`，同时场景设计组角色文档也为空，导致 `1-清单` 虽然已把场景对象池交给 `2-设计`，但缺少接手合同。
- final_fix_or_heuristic: 建立父 skill、team.md、角色 agent docs、模板与 references，确保输入沿 `scene catalog -> global style -> director evidence` 收束，输出沿 `patch -> synthesis -> review/audit -> canonical writeback` 闭环。
- prevention_or_replication_checklist:
  - [x] `2-设计` 主合同已补齐
  - [x] team 与角色合同已落盘
  - [x] `CHANGELOG.md` 与 `agents/openai.yaml` 已补齐
  - [x] 场景设计卡模板已成为唯一字段真源
- evidence_paths:
  - `.agents/skills/aigc/4-Design/1-场景/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-场景/2-设计/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/1-场景/2-设计/references/chain-of-thought.md`
  - `.codex/agents/aigc/设计组/场景设计/team.md`
- user_feedback_or_constraint: 用户要求基于 `skill-subagents` 规范，结合 `brainstorming` 与 `senior-prompt-engineer`，把当前主题系统性重构为 subagents 执行思考、父 skill 统筹输入输出的结构。

### Case-20260412-AIGC-SCENE-DESIGN-AGENTS-PLAN-ALIGNMENT

- milestone_type: source_contract_change
- outcome: 将场景设计链的 subagent handoff 从 patch-only 语义升级为 `agents_plan + patch / note / report`。
- root_cause_or_design_decision: `1-Planning / 2-Global / 3-Detail` 已切到“subagents 负责思考计划、skills 负责执行闭环”的统一口径，但场景设计链仍停留在 patch-only 叙述，导致阶段间 handoff 语义不一致。
- final_fix_or_heuristic: 同步更新 `2-设计/SKILL.md`、`references/chain-of-thought.md`、team 与角色入口元数据，明确 `agents_plan` 只承载 dispatch 计划、字段补位顺序与返工摘要，不冒充 canonical 设计稿。
- prevention_or_replication_checklist:
  - [x] 父 skill 已改为 agents-plan-aware handoff
  - [x] team 与 `设计统筹` 已补 agents_plan 输出口径
  - [x] role frontmatter 已同步 `allowed_return_types`
  - [x] 经验层已登记新 handoff 语义
- evidence_paths:
  - `.agents/skills/aigc/4-Design/1-场景/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/1-场景/2-设计/references/chain-of-thought.md`
  - `.codex/agents/aigc/设计组/场景设计/team.md`
  - `.codex/agents/aigc/设计组/场景设计/设计统筹.md`
- user_feedback_or_constraint: 用户要求把 `1-Planning` 已收口的 agents-plan 口径继续推广到后续阶段，避免 stage 间 subagent 合同分裂。

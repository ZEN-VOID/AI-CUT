# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/3-服装/2-设计` 的经验层知识库，不是过程日志。
- 调用本父 skill 时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- soft_limit_cases: 16
- hard_limit_cases: 32
- status: ok
- last_checked_at: 2026-04-12

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-设计` 跳过 `1-清单` 直接发明服装设计 | 输入锚点层 | 强制回到 `costume_design_bridge.json` 锁当前服装对象池 | 在 `SKILL.md` 和 team 合同中固化“先清单、再设计” | 不再出现无对象池设计 |
| specialists 各写一整份服装稿，父 skill 无法收束 | 编排边界层 | 收回写回权到父 skill，只允许返回 `agents_plan + patch / note / report` | 在 `team.md` 与 `_shared/IO_CONTRACT.md` 固化 agents-plan-aware handoff | canonical 输出只由父 skill 写回 |
| 廓形、材质、配饰三条线互相打架 | reviewer 合同层 | 进入 `服装一致性复核`，要求指出冲突字段与返工入口 | 将跨字段一致性检查设为默认 tranche | reviewer 能给出明确 rework |
| 服装设计只剩 prompt，没有 machine-first carrier | 输出治理层 | 补回 `服装设计.json` 并让 Markdown 与其同源 | 在输出模板中固定 JSON 为 canonical | 下游面板/生图能稳定消费 JSON |
| `提示词架构师` 越权新增设计事实 | prompt 分层层 | 只允许写 `costume_design_prompt.json` patch | 在 team 合同中固定“prompt 不得倒灌 design facts” | prompt sidecar 与 design master 分层稳定 |
| 父 skill 有 team 配置，但主合同仍偏线性说明 | 思行网络层 | 把 route mode、selected_costumes、specialist 切面、review gate 和 manifest 闭环全部收回同一 `SKILL.md` | 固化“串行锁定 + specialists 并行 + review 汇流 + prompt/audit 后段”的父技能网络 | `2-设计` 能在主合同中独立解释整条执行链 |

## Repair Playbook

1. 先查 `1-清单/costume_design_bridge.json` 是否存在且服装对象池稳定。
2. 再看 `team.md` 是否仍把写回权保留在父 skill。
3. 再看 `服装设计.json` 是否与逐服装 Markdown、prompt sidecar 同源。
4. 若服装设计冲突，优先回到 `服装一致性复核` 指定的字段槽位返工。
5. 最后才调整单次 prompt 话术。

## Reusable Heuristics

- 服装设计最稳的入口不是“按角色再想一次穿搭”，而是先有服装对象池，再做结构化设计。
- 对服装链来说，`prompt sidecar` 是下游执行话术，不是服装事实真源。
- `character_design.json` 最适合做约束输入，而不是被服装类目重新覆盖。
- 对服装设计来说，`agents_plan` 最适合承载 costume dispatch、字段补位顺序与 prompt/audit 返工摘要；最终 design master 仍只能由父 skill 写回。
- 对带 subagents 的父技能做知行合一改造时，最关键的是把 team 拓扑翻译成主合同里的节点网络，而不是只在 `team.md` 里保留真实执行顺序。

## Case Log

### Case-20260412-AIGC-COSTUME-DESIGN-SKILL-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/3-服装/2-设计` 建立了父 skill、经验层、shared I/O、模板、入口元数据与服装设计组 team。
- root_cause_or_design_decision: `3-服装` 需要独立的 design synthesis，但当前仓库只有角色设计里的局部 `服装设计` specialist，没有面向独立服装真源的父 skill 和 team contract。
- final_fix_or_heuristic: 将 `2-设计` 定义为 full 父 skill，采用 `服装统筹 -> 三 specialists 并行 -> 服装一致性复核 -> 提示词架构师 -> 真源审计 -> 父 skill 写回` 的 topology，并以 `服装设计.json + 逐服装 Markdown + costume_design_prompt.json + _manifest.json` 作为 canonical 输出。
- prevention_or_replication_checklist:
  - [x] 父 skill 已建立
  - [x] `_shared/IO_CONTRACT.md` 已建立
  - [x] `agents/openai.yaml` 已建立
  - [x] 服装设计组 team 与 agent docs 已落盘
- evidence_paths:
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/服装设计/team.md`
- user_feedback_or_constraint: 用户要求参照现有 `角色 / 场景 / 道具` 家族及 subagents 配置，将 `3-服装` 补到同一治理层级。

### Case-20260412-AIGC-COSTUME-DESIGN-AGENTS-PLAN-ALIGNMENT

- milestone_type: source_contract_change
- outcome: 将服装设计链的 subagent handoff 从 patch-only 语义升级为 `agents_plan + patch / note / report`。
- root_cause_or_design_decision: `1-Planning` 已统一为“subagents 负责 agents plan、skills 负责执行闭环”，但服装设计链仍以 patch-only 描述 subagent 交接，导致阶段间 contract 漂移。
- final_fix_or_heuristic: 同步更新 shared I/O、team、planner 角色与入口元数据，明确 `agents_plan` 只承载 costume dispatch、字段补位顺序与 prompt/audit 返工摘要，不冒充 canonical design master。
- prevention_or_replication_checklist:
  - [x] shared I/O 已同步 agents-plan-aware handoff
  - [x] team 与 `服装统筹` 已补 agents_plan 输出口径
  - [x] role frontmatter 已同步 `allowed_return_types`
  - [x] 经验层已登记新 handoff 语义
- evidence_paths:
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/服装设计/team.md`
  - `.codex/agents/aigc/设计组/服装设计/服装统筹.md`
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/CONTEXT.md`
- user_feedback_or_constraint: 用户要求把 `1-Planning` 已经定下的 agents-plan 口径继续推广到服装设计子链，避免只剩 patch/note/report 的旧语义。

### Case-20260412-AIGC-COSTUME-DESIGN-ZHI-XING-NETWORK

- milestone_type: source_contract_change
- outcome: 在不改变 team、shared I/O、输入输出路径和 sidecar 分层的前提下，将 `2-设计` 重排为知行合一父技能。
- root_cause_or_design_decision: 原合同已经具备丰富机制，但主文仍更像“完整说明书 + 字段表”；team 真正的执行拓扑主要留在 team/shared I/O，而没有完全投影到父技能思行网络里。
- final_fix_or_heuristic: 将 `2-设计` 改写为 `Business Requirement Analysis -> Topology -> Thinking-Action Node Network -> Capability Detail -> Convergence -> One-Shot Output`，并把 specialists、reviewer、prompt architect、auditor 的细颗粒步骤直接写入主合同。
- prevention_or_replication_checklist:
  - [x] `_shared/IO_CONTRACT.md` 与 `team.md` 仍是支持性真源
  - [x] `agents_plan + patch / note / report` handoff 未变化
  - [x] `服装设计.json / costume_design_prompt.json / _manifest.json` 路径未变化
- evidence_paths:
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/3-服装/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/服装设计/team.md`
- user_feedback_or_constraint: 用户要求“内容和机制上全量参照现有配置，但根据知行合一的规范进行编排”，并要求每个思维·执行节点足够细致。

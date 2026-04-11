# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-明细/subtypes/5-摄影美学` 的经验层知识库，不是执行日志。
- 调用父级 `SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/3-明细/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 父级 `chain-of-thought.md` 仍停留在旧版字段表，缺少启发式快照、Gate 与可见/隐藏分层 | 思维链合同层 | 按最新 `think-think` 规范重写父级 `references/chain-of-thought.md` | 父级思维链默认包含 `模式与对象 -> 启发式工作链 -> 三轴三重 -> 工具后反思 -> Gate Summary`，同时保留 `FIELD-CINE-*` 接口 | 不暴露完整 CoT 也能完成路由、写位、真源与交接裁决 |
| 三个 leaf 已有内容，但父级没有进入判定 | 父子路由层 | 先补父级路由矩阵 | 父级显式写何时进入哪个 leaf | 父级可输出唯一主入口 |
| 同一 `[分镜N]` 出现多条 `[摄影美学]` 说明 | 写位冲突层 | 收束为单一 continuation line | 在父级固化 `[摄影美学]` 行合同 | 每镜只保留一条摄影真相 |
| 色彩与参数不回查光影，导致摄影语义打架 | 感知链顺序层 | 回到 `光影设计 -> 色彩设计 -> 摄影参数` 串行顺序 | 父级显式覆盖 `unordered` 默认并发 | 三层判断前后自洽 |
| `摄影参数` 直接改写 `焦距 / 光圈` | 边界层 | 回滚越界改动，只保留捕捉参数 | 在父级与 leaf 中固定“静态光学归 `1-分镜表现`” | 参数层不再越权 |
| 只补审美形容词，没有稳定写位 | 结构层 | 把结果收口到 `[摄影美学]` 行 | 在父级固定 continuation line 格式 | 摄影增强可持续 patch-in-place |
| 顾问团已启用，但 `5-摄影美学` 没继承 `3-明细` 的阶段顾问运行时 | 继承层 | 明确本父技能继承上层 `3-明细` 的 `Council Runtime Contract` | 子技能不再重复发明第二套顾问团规则 | 进入 `5-摄影美学` 时会先遵守项目根 `team.yaml` 判定 |

## Repair Playbook

1. 先检查父级 `5-摄影美学/SKILL.md` 是否具备唯一主入口裁决。
2. 再检查每个 `[分镜N]` 是否只存在一条 `[摄影美学]` continuation line。
3. 若多 leaf 同时命中，先锁 `光影设计`，再补 `色彩设计`，最后补 `摄影参数`。
4. 最后检查是否把越界问题留口给 `1-分镜表现`、`3-运镜手法` 或 `6-转场特效`。

## Reusable Heuristics

- 摄影美学层最容易失控的不是“不够美”，而是没有稳定写位，导致光影、色彩、参数散落在终稿各处。
- 父级 `think-think` 优先裁决的不是“写多美”，而是 `进哪个 leaf + 怎么共写一条 `[摄影美学]` 行 + 如何把未处理项交给下游`。
- 只要共享同一份集级终稿和同一条 `[摄影美学]` 行，三个 `unordered` leaf 就不该并发落笔。
- 先定光，再定色，最后定参数，能最大程度避免“参数有了但感知逻辑没立住”。
- `摄影参数` 在本层应补的是快门、ISO、白平衡、滤镜、曝光，而不是回头重做 `焦距 / 光圈`。
- 对 `5-摄影美学` 来说，顾问团机制应该继承自 `3-明细` 根级，不应在父子链里再复制一套。

## Case Log

### Case-20260409-AIGC-SCRIPT-CINEMATOGRAPHY-PARENT-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-明细/subtypes/5-摄影美学` 建立了父级合同与经验层，并把 `光影设计 / 色彩设计 / 摄影参数` 接回统一父级路由。
- root_cause_or_design_decision: 用户要求补齐 `5-摄影美学`，且明确希望包含“光影·色彩·摄影参数”；真正缺口不是单个 leaf，而是空目录没有父级写位合同，无法承接终稿共写模式。
- final_fix_or_heuristic: 先补父级 `SKILL.md + CONTEXT.md`，再把三个 leaf 都挂到“单任务唯一进入；多命中时按 `光影设计 -> 色彩设计 -> 摄影参数` 受控串行”的冲突解决规则上。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已补齐
  - [x] 父级 `CONTEXT.md` 已建立
  - [x] 三个 leaf 都已纳入同一父级矩阵
  - [x] `[摄影美学]` continuation line 已固定
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/光影设计/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/色彩设计/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/subtypes/摄影参数/SKILL.md`
- user_feedback_or_constraint: 用户明确要求完善 `5-摄影美学`，并指定应包含 `光影·色彩·摄影参数`，同时要求整个 `3-明细` 系列统一服从“基于上游分组原文的层层加权扩写”前提。

### Case-20260409-AIGC-SCRIPT-CINEMATOGRAPHY-CHAIN-UPGRADE

- milestone_type: source_contract_change
- outcome: 将父级 `references/chain-of-thought.md` 从旧版字段表合同升级为最新 `think-think` 规范的可见思维快照合同。
- root_cause_or_design_decision: 旧版父级思维链只有 `Field Master / Thought Pass Map / Pass Table`，缺少 `模式与对象`、`启发式工作链`、`三轴三重`、`工具后反思` 与 `Gate Summary`，无法和最新元技能规范对齐。
- final_fix_or_heuristic: 保留现有 `FIELD-CINE-*` 接口不变，在父级思维链中补齐 `模式与对象 -> Think-Think Design Snapshot -> 工具后反思与 Gate Summary -> Validation Matrix` 的新版骨架。
- prevention_or_replication_checklist:
  - [x] 父级 `chain-of-thought.md` 已升级为最新规范
  - [x] `FIELD-CINE-*` 字段编号保持兼容
  - [x] 已补可见 / 隐藏分层与 Gate Summary Contract
  - [x] 已把升级经验写回父级 `CONTEXT.md`
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/5-摄影美学/CONTEXT.md`
  - `/Users/vincentlee/.codex/skills/meta/解构/思维/think-think/SKILL.md`
- user_feedback_or_constraint: 用户要求“按照最新的思维链设计规范”优化父级 `chain-of-thought.md`，目标是升级设计合同，而不是重做 leaf 内容本身。

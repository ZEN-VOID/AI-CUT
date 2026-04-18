---
name: story-validate
description: Use when `story2026` 进入第 4 阶段，需要以隔离上下文的后台多智能体团队对章节或历史章节做客观检验评估，并把结果回流到修复闭环或 `5-Loopback` 的 validated actualization。
governance_tier: lite
---

# 4-Validation

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只沉淀验证层经验与聚合启发，不得覆盖本 `SKILL.md` 的 checker roster、fact pack gate 与 handoff 判定。
- 当前仓库没有单独维护 `.codex/agents/story*` agent 文档树；validation roster 的单一真源固定为根级 `references/validation-team-contract.md`。

## Scope

- `4-Validation` 是**阶段级调度层**，不是直接执行型 checker 或人工审查器。
- 它的职责是创建一次新的、后台运行的、多智能体评估团队，并把检验任务分发给 [`../references/validation-team-contract.md`](../references/validation-team-contract.md) 中登记的白名单角色。
- 它负责路由、团队生命周期、结果汇总入口与回流决策；具体审查判断由被调度的 subagents 完成。
- `validation-team-contract.md` 中的 checker roster 始终是本阶段的**基础框架**，不可被替换。
- 若 `TEAM.toml["评审"]` 已指派 AGENTS，它只是在基础框架之外额外创建“评审专家组”子通道，让阶段治理团队参与最终评审裁决与落盘。

## 调度对象（唯一白名单）

- `context-agent`：补充评估所需上下文，不负责给最终质量结论。
- `consistency-checker`
- `continuity-checker`
- `ooc-checker`
- `reader-pull-checker`
- `high-point-checker`
- `pacing-checker`
- `spoiler-checker`
- `immersion-voice-checker`

禁止事项：
- 不得绕过上述 agent 由主流程直接内联“自审结论”。
- 不得把 `4-Validation` 写成新的 checker。
- 不得调用未登记在 `validation-team-contract.md` 的临时评估角色替代正式 checker。
- 不得用 `TEAM.toml["评审"]` 的外部 AGENTS 替代正式 checker 白名单；评审专家组是治理加层，不是 checker 替身。

## 执行模式（硬规则）

### 新后台团队模式

- 每次进入 `4-Validation`，**必须新建**一组后台多智能体团队执行本轮检验。
- 默认并行调度；若用户显式要求或上游合同存在硬依赖，再做串行收束。
- 同一轮评估内允许共享“输入包”，但不共享既有对话历史。

### 上下文隔离

- 每个 checker 都必须在**新上下文**中启动，不复用主线程、既有 checker 线程或上一轮评估线程。
- 禁止把写作主流程中的隐含偏好、上次审查措辞、未验证判断直接带入本轮评估。
- 目标是降低上下文污染，优先保证客观性、可复核性与交叉校验价值。

### TEAM 阶段治理（Mandatory）

- 执行 `4-Validation` 前，必须读取项目根 `TEAM.toml`，并把 `["评审"]` 视为本阶段的唯一团队治理入口。
- `TEAM.toml["评审"]` 的作用是给既有 validation 基础框架做**增量加层**，不是覆盖 `validation-team-contract.md` 中定义的 checker 体系。
- 若满足以下任一条件，即视为评审专家组已激活：
  - `TEAM.toml["评审"].智能顾问团 = true`
  - `TEAM.toml["评审"].成员` 非空
- 评审专家组已激活时：
  - 基础 checker 白名单团队仍必须完整运行。
  - 必须在 checker 白名单团队之外，再创建一组后台评审 subagents。
  - 这组 subagents 负责对 checker 聚合结果做二次裁决、风险定级与回流建议，不替代正式 checker 的证据采样。
  - 主流程必须把评审专家组意见写入本轮 validation 聚合结果，形成可追溯的阶段评审决议。
- `TEAM.toml["评审"].管辖` 是 stage-route sanity check；若未覆盖 `4-Validation`，必须报告团队治理配置漂移。
- 若 `TEAM.toml["评审"]` 未激活，则维持当前默认 checker 团队模式，但仍要在执行说明中明确“本轮无评审专家组介入”。

## 输入合同

最小输入：
- `project_root`
- `chapter` 或 `chapter_range`
- 实际章节文件路径
- 当前模式：`normal_review` 或 `historical_recheck`
- `TEAM.toml`
- `validation_fact_pack`
  - 必含：`promise_slice`
  - 必含：`chapter_board`
  - 必含：`cards_state_history_slice`
  - 必含：`foreshadow_silence_slice`
  - 必含：`style_gate`

可选输入：
- 来自 `3-Drafting` 的执行合同 / Context Contract
- 用户额外关注项
- 上轮审查报告路径（仅用于历史复审，不作为事实真源）

## Shared References（按需）

- `../references/validation-fact-pack-spec.md`
  - 用途：校验五类强制 slice 是否齐全。
- `../references/checker-output-schema.md`
  - 用途：统一 checker 输出、validation 聚合与 review sink 字段。
- `../references/validation-team-contract.md`
  - 用途：统一 checker 白名单、职责边界与调度规则。
- `../references/context-contract-v2.md`
  - 用途：确认 `validation_fact_pack` 来源于当前章节级上下文合同，而不是孤立拼装。

## 工作流

1. 先判定本轮属于 `normal_review` 还是 `historical_recheck`。
2. 读取 `TEAM.toml`，判定 `["评审"]` 是否激活；若激活，先生成本轮评审专家组简报。
3. 构造单轮评估输入包，只注入本轮必须事实，不注入主线程长历史。
   - `context-agent` 在 validation 模式下必须先组装 `validation_fact_pack`，缺任一强制 slice 视为 `FAIL-COVENANT`
4. 创建新的后台多智能体团队。
5. 将输入包分发给 `validation-team-contract.md` 中的 checker：
   - 核心 checker 默认必开：`consistency-checker`、`continuity-checker`、`ooc-checker`、`immersion-voice-checker`
   - 条件 checker 按章节类型、规划标签、用户要求增开：`reader-pull-checker`、`high-point-checker`、`pacing-checker`、`spoiler-checker`
   - 若 `validation_fact_pack.foreshadow_silence_slice.has_active_foreshadowing=true`，则 `spoiler-checker` 默认必开
   - 若 `validation_fact_pack.style_gate.anti_ai_required=true` 或 `style_gate.no_poison_required=true`，则 `immersion-voice-checker` 不得关闭
6. 若 `TEAM.toml["评审"]` 已激活，再将同一输入包分发给评审专家组 subagents，作为基础 checker 框架之外的增量治理裁决。
7. 等 checker 与评审专家组返回结构化结果后，统一汇总为阶段评估结果；若未激活评审专家组，则仅汇总基础 checker 框架结果。
8. 将结果回流到下游：
   - 若 `validation_status=PASS`：把正式记录与评分交给 `review/`，并把 validated result handoff 到 `5-Loopback`
   - 若属于表达层、节奏层、人物层问题：回流 `3-Drafting` Step 4
   - 若暴露规则、路径、合同或恢复类问题：转入 `5-Loopback` 的 satellite routing（`query / resume / learn`）
   - 任何非 `PASS` 结果都不得进入 `5-Loopback` 的 actualization 写回主流程

## 输出合同

`4-Validation` 自身必须至少产出以下结构化对象，供下游消费：

- `validation_status`
- `validation_mode`
- `selected_agents`
- `review_council_agents`
- `review_council_summary`
- `issues`
- `severity_counts`
- `critical_issues`
- `overall_score`
- `dimension_scores`
- `anti_ai_force_check`
- `spoiler_risk`
- `contrivance_risk`
- `cold_commentary_risk`
- `routing_decision`
- `handoff_targets`

输出解释：
- `issues / severity_counts / critical_issues` 必须与 checker 聚合结果一致，供 `3-Drafting` Step 4 直接消费。
- `review_council_agents / review_council_summary` 记录 `TEAM.toml["评审"]` 触发的阶段评审专家组与其最终裁决摘要；它们是基础 checker 聚合之上的增量字段，未激活时允许为空。
- `dimension_scores` 必须可被 `review/` 直接写入 `review_metrics`。
- `anti_ai_force_check / spoiler_risk / contrivance_risk / cold_commentary_risk` 必须作为一等字段进入 `review_metrics`，不得仅压入 `notes`。
- `anti_ai_force_check` 在 Step 3 聚合时允许为 `pending`；一旦 Step 4 完成全文终检，必须回写为 `pass` 或 `fail`。
- `validation_status` 只能是：`PASS` / `FAIL-QUALITY` / `FAIL-COVENANT` / `FAIL-RUNTIME`
- `routing_decision` 只能是：`back_to_drafting_step_4` / `handoff_to_review_and_loopback` / `handoff_to_loopback_support`
- `handoff_targets` 记录被转交的 skill 或阶段入口；当 `validation_status=PASS` 时，必须显式包含 `review/` 与 `5-Loopback`。

## Shadow Governance Artifact Chain

当 `4-Validation` 跑在 tracked workflow 里时，必须承认当前 `<run_id>` 的任务工件目录会作为门下省证据层存在：

- `artifact_manifest.json`
- `validation_report.md`
- `learning_record.md`
- 失败时的 `root_cause_trace.md`

约束：

- `4-Validation` 仍然拥有 `validation_status / routing_decision / handoff_targets` 判定权。
- task dir 中的 `validation_report.md` 是对阶段结论的持久化承接，不是第二个评估入口。
- 若 checker 聚合失败，失败闭环应优先落到同一 `<run_id>` 的 trace 工件，而不是只停留在对话上下文。

## Root-Cause 执行合同

- 若评估结果失真、缺失或相互矛盾，必须按 `Symptom -> Direct Cause -> Rule Source -> Meta Rule Source` 上溯。
- 本 skill 的 `Rule Source` 默认优先检查：
  - 当前 `4-Validation/SKILL.md`
  - `../references/validation-team-contract.md`
  - `review/SKILL.md`
  - `3-Drafting/references/step-3-review-gate/appendix-review-gate.md`
- `Meta Rule Source` 默认上溯到仓库 `AGENTS.md` 与相关 meta skill。
- 修复顺序必须是：先修调度合同/agent 合同/聚合契约，再决定是否修本次章节内容。

## Lite Tier Field Mapping（Combined）

| field_id | step_id | intent | required_output | fail_code | rework_entry |
|---|---|---|---|---|---|
| FIELD-VAL-ROUTING-01 | Step 1 | 判定评估模式与回流方向 | `validation_mode`、`routing_decision` | FAIL-VAL-ROUTING-01 | 回到模式判定，重新核对 normal vs historical |
| FIELD-VAL-FACTPACK-02 | Step 2-3 | 组装 validation 必载事实包并判定 `TEAM.toml["评审"]` 是否激活 | `validation_fact_pack`、`review_council_agents` | FAIL-VAL-FACTPACK-02 | 回到 `context-agent` 补齐 `promise_slice / chapter_board / cards_state_history_slice / foreshadow_silence_slice / style_gate`，并重新读取 `TEAM.toml` |
| FIELD-VAL-TEAM-03 | Step 4-6 | 以新后台团队完成隔离评估，并在激活时附带评审专家组增量加层 | `selected_agents`、团队创建说明、`review_council_summary` | FAIL-VAL-TEAM-03 | 重新创建团队，禁止复用旧线程 |
| FIELD-VAL-AGG-04 | Step 7 | 汇总 checker 与评审专家组结论供下游消费 | `issues`、`severity_counts`、`critical_issues`、`overall_score`、`dimension_scores`、`anti_ai_force_check`、`spoiler_risk`、`contrivance_risk`、`cold_commentary_risk` | FAIL-VAL-AGG-04 | 回到聚合层，补齐 schema 并重汇总 |
| FIELD-VAL-HANDOFF-05 | Step 8 | 把结果正确交给修复/报告/actualization 闭环 | `validation_status`、`handoff_targets` | FAIL-VAL-HANDOFF-05 | 按 PASS / FAIL 重新路由到 Drafting / review / Loopback |

## Completion Gate

- 已创建新的后台多智能体团队，而非复用旧上下文。
- `validation_fact_pack` 已包含强制五个 slice。
- 评估 agent 全部来自 `validation-team-contract.md` 白名单。
- 若 `TEAM.toml["评审"]` 已激活，评审专家组已作为基础 checker 框架之外的增量加层一并运行，且其结论进入正式聚合结果。
- 已产出可被下游直接消费的聚合结构。
- `anti_ai_force_check / spoiler_risk / contrivance_risk / cold_commentary_risk` 已作为正式字段进入聚合结果。
- 已明确 `PASS` 是否进入 `review/ + 5-Loopback`，以及非 PASS 是否回流 `3-Drafting` 或 `5-Loopback` satellite support。

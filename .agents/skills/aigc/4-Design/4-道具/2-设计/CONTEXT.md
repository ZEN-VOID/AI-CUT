# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `.agents/skills/aigc/4-Design/4-道具/2-设计` 的经验层知识库，不是过程日志。
- 调用本叶子技能时，应自动预加载本文件。

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
| 只有 bridge，没有 design master | 父 skill 合同层 | 建立 `道具设计.json` 作为 canonical truth | 固定 `bridge -> design master -> prompt sidecar` 的顺序 | 下游不再直接拼接 bridge |
| prompt sidecar 抢走业务真源 | 输出治理层 | 把 prompt 文案全部下放 `prop_design_prompt.json` | 固化“canonical truth 与 prompt sidecar 分层” | design master 中不再出现长 prompt |
| 路径错写成 `4-Design/2-角色/4-道具` | 路径归一层 | 在父 skill 与 runner 中统一规范化到 `4-Design/4-道具/2-设计/第N集/` | 将 path normalization 记入 manifest 与 shared I/O | 输出目录稳定一致 |
| team 存在但没有明确后台执行规则 | subagent 编排层 | 在父 skill 与 team 文档同时补写后台执行规则 | 把 team 和父 skill 一起作为 validator 的检查对象 | 调用层不再误解成交互式前台流程 |
| prompt 架构师脱离 canonical truth 自创事实 | prompt handoff 层 | 强制 prompt 只消费 `道具设计.json` | 固化“prompt 不改业务事实”禁令 | prompt 内容能回链 design master |

## Repair Playbook

1. 先看 `prop_design_bridge.json` 是否已经存在且字段完整。
2. 再看 `道具设计.json` 是否真的只保留设计事实，而不是长 prompt。
3. 若问题出在 prompt 漂移，先修 `prop_design_prompt.json` 与 `提示词架构师.md`，不要回写 canonical truth。
4. 若问题出在事实漂移，先修结构/材质/痕迹 patch 与 team 拓扑。
5. 最后检查 `_manifest.json` 是否记录了路径归一、coverage 和 drift 结论。

## Reusable Heuristics

- 对道具设计来说，最值钱的不是“某次 prompt 写得很华丽”，而是“结构、材质、痕迹这些字段能被多次复用”。
- 让 `模型师 + 材质工艺师 + 痕迹叙事师` 并行，通常比单角色串行更稳，因为这三类 patch 的写入槽位天然分离。
- prompt 架构师应晚于 canonical synthesis；否则 prompt 很容易反过来绑架业务事实。
- 用户给错路径时，不要把错路径写成新的真源；要在 manifest 里记录一次 path normalization，然后统一落到 canonical 目录。
- 对道具设计来说，`agents_plan` 最适合承载 bridge 消费顺序、字段补位顺序与 audit 返工摘要；最终三件套真源仍只能由父 skill 写回。

## Case Log

### Case-20260412-AIGC-PROP-DESIGN-SUBA-BOOTSTRAP

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-Design/4-道具/2-设计` 建立了父 skill、shared I/O、team、prompt sidecar 和最小 runner。
- root_cause_or_design_decision: 原目录为空，且 `.codex/agents/aigc/设计组/道具设计/模型师.md` 也是空文件，导致道具设计既没有父层真源，也没有真实 agent team。
- final_fix_or_heuristic: 建立以 `道具设计.json` 为 canonical truth、`prop_design_prompt.json` 为 prompt sidecar、`_manifest.json` 为审计侧车的三件套，并用五角色 subagents 承担结构、材质、痕迹、prompt 与审计 patch。
- prevention_or_replication_checklist:
  - [x] 父 skill 已建立
  - [x] team 与角色合同已建立
  - [x] runner 与输出模板已建立
  - [x] 路径归一规则已写入 shared I/O
- evidence_paths:
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/道具设计/team.md`
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/scripts/run_prop_design_pipeline.py`
- user_feedback_or_constraint: 用户明确要求以 `skill-subagents + brainstorming + senior-prompt-engineer` 为基础，让 subagents 负责专业思考和 plan 统筹输入输出。

### Case-20260412-AIGC-PROP-DESIGN-AGENTS-PLAN-ALIGNMENT

- milestone_type: source_contract_change
- outcome: 将道具设计链的 subagent handoff 从 patch-only 语义升级为 `agents_plan + patch / note / report`。
- root_cause_or_design_decision: `1-Planning` 已经把 subagent 职责收口到“agents plan + skill execution”，但道具设计链仍在使用 patch-only 叙述，导致父 skill 与设计组 team 的 handoff 语义滞后。
- final_fix_or_heuristic: 同步更新父 skill、shared I/O、team 与角色入口元数据，明确 `agents_plan` 只承载 bridge 消费顺序、字段补位顺序与 audit 返工摘要，不冒充 design master 或 prompt sidecar。
- prevention_or_replication_checklist:
  - [x] 父 skill 已改为 agents-plan-aware handoff
  - [x] shared I/O 已同步 handoff 新口径
  - [x] team 与角色入口元数据已同步 `allowed_return_types`
  - [x] 经验层已登记新 handoff 语义
- evidence_paths:
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-Design/4-道具/2-设计/_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/设计组/道具设计/team.md`
  - `.codex/agents/aigc/设计组/道具设计/模型师.md`
- user_feedback_or_constraint: 用户要求把 `1-Planning` 已切换的 agents-plan 口径继续推广到道具设计链，统一 subagent 的思考与执行边界。

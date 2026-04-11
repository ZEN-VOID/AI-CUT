# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-主体/subtypes/3-审计` 的经验层知识库，不是执行日志。
- 调用本子技能时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 上层 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 审计只剩主观好坏评价 | 审计合同层 | 回到失败维度表重写 | 在 `Field Master` 固定结构化失败维度 | 审计报告可直接返工 |
| 审计无法回链上游约束 | 证据链层 | 补 `1-清单 / 3-明细 / 2-组间` 回查 | 把“证据链可追溯”写成强制输入 | 每条问题都能说明来源 |
| 审计完没有下一入口 | 闭环层 | 补写回 `2-设计` 或进入 `4-面板` 的裁决 | 把下一入口写成固定交付字段 | 执行链不再卡在审计之后 |

## Repair Playbook

1. 先检查 `2-设计` 输入与上游证据是否齐。
2. 再看报告里是否出现结构化失败维度。
3. 最后检查是否给出了回写建议和唯一下一入口。

## Reusable Heuristics

- 主体审计最常见的失败不是“没发现问题”，而是“发现了问题但说不成可执行返工”。
- 如果一条审计意见不能说明它违反了哪一条上游约束，那它通常还不够稳定。
- 审计是为了让链路继续向前，而不是为了在中途停成一份评论稿。
- 对审计型 leaf，主合同越短越好，把失败维度、workflow、路由与输出结构收束到 `references/` 更不容易失真。
- 对审计型 thought contract 来说，最该先暴露的不是“怎么看”，而是“依据哪条证据链判错、错在哪个结构维度、返工从哪一步开始”。

## Case Log

### Case-20260409-AIGC-SUBJECT-AUDIT-BASELINE

- milestone_type: source_contract_change
- outcome: 为 `4-主体/subtypes/3-审计` 建立了结构化失败维度、返工建议与下一入口合同。
- root_cause_or_design_decision: 参考仓 `3-审计` 的高价值部分是“把偏差收束成修复路线”，当前仓因此保留审计闭环，而不直接复制其工具脚本和 API 绑定。
- final_fix_or_heuristic: 审计阶段必须至少交付“失败维度 + 修订建议 + 下一入口”三件套，才能真正服务 `2-设计` 与 `4-面板`。
- prevention_or_replication_checklist:
  - [x] 失败维度结构化
  - [x] 修订建议固定交付
  - [x] 下一入口固定交付
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/3-设定/3-审计/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 `ZEN-VOID` 的设定审计层，但当前仓优先补阶段合同与治理闭环，不直接绑定远端生图修复脚本。

### Case-20260409-AIGC-SUBJECT-AUDIT-REFERENCES

- milestone_type: source_contract_change
- outcome: 将 `3-审计` 重构为“主合同 + references 四模块”结构，保留失败维度、返工建议与下一入口三件套不变。
- root_cause_or_design_decision: 旧版单文件合同虽完整，但审计输入、失败维度、workflow 与输出契约混写在主合同里，不利于继续按最新规范做真源维护。
- final_fix_or_heuristic: 主 `SKILL.md` 只保留边界、Visual Maps、摘要与 Root-Cause 闭环；详细 field map、workflow、域路由与输出契约拆到 `references/*.md`。
- prevention_or_replication_checklist:
  - [x] 已建立 `references/` 四件套
  - [x] 审计三件套保持不变
  - [x] 上游证据链要求继续保留
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/references/execution-flow.md`
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/references/type-strategies.md`
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/references/output-template.md`
- user_feedback_or_constraint: 用户要求在不改变内容基础的前提下按最新规范重构 `4-主体` 全目录。

### Case-20260409-AIGC-SUBJECT-AUDIT-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `3-审计/references/chain-of-thought.md` 升级为最新 `think-think` 规范，补入模式声明、证据导向启发式、工具后反思、Gate Summary 与验证矩阵。
- root_cause_or_design_decision: 旧版 `3-审计` 说明了“要有失败维度和修订建议”，但没显式压出“先锁证据链、再定失败维度、最后决定回写/放行入口”的判断顺序，容易退回主观评论。
- final_fix_or_heuristic: 保留 `FIELD-SAUD-01` 到 `FIELD-SAUD-04` 不变，把审计层核心思考显式压到 `证据链 -> 失败维度 -> 修订建议 -> 下一入口`，并要求关键节点后二次判断。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与对象`
  - [x] 已补审计层 `启发式工作链`
  - [x] 已补 `Gate Summary` 与 `Validation Matrix`
  - [x] 已补 `可见 / 隐藏分层`
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求按最新思维链设计规范优化 `4-主体` 全目录的 thought contract。

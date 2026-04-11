# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-主体/subtypes/4-面板` 的经验层知识库，不是执行日志。
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
| 面板开始二次设计主体 | 真源边界层 | 回到 `2-设计` 或 `3-审计` 先收束设计 | 在本技能写死“面板只布局，不二次发明设计” | 面板与设计卡口径一致 |
| 缺少 layout sidecar | 结构输出层 | 补齐 layout JSON | 固定“主文件 + layout”双产物 | 下游能直接消费 |
| 审计未通过就做面板 | 阶段顺序层 | 先回到 `3-审计` 或 `2-设计` | 在本技能固化“关键失败项未关闭不得进面板” | 面板不再放大缺陷版本 |

## Repair Playbook

1. 先看 `2-设计` 是否稳定，若有审计结果再看是否已通过。
2. 再看面板是否同时生成主文件与 layout sidecar。
3. 最后检查面板是否明确给出下游参照入口。

## Reusable Heuristics

- 面板阶段最怕“看起来更完整，实际上把上游设计又偷偷改了一遍”。
- 对面板来说，双产物的意义比文案华丽更重要：没有 layout，面板就很难真正服务下游。
- 若审计里还有关键失败项，先修设计，比急着做漂亮面板更稳。
- 对布局型内容输出技能，主合同适合保留边界、流程图和摘要，把双产物硬规则、真源判定与 handoff 细则下沉到 `references/`。
- 面板层的 thought contract 要先锁“继承哪一版稳定设计”，再谈主文件和 layout 如何展开；否则布局层很容易滑成第二次设计。

## Case Log

### Case-20260409-AIGC-SUBJECT-PANEL-BASELINE

- milestone_type: source_contract_change
- outcome: 为 `4-主体/subtypes/4-面板` 建立了面板主文件、layout sidecar 与下游参照交接合同。
- root_cause_or_design_decision: 参考仓 `4-面板` 的关键价值在于“把稳定设计变成布局化参照面”，当前仓因此保留 layout 语义，但不把本层写成单纯 API 生图桥。
- final_fix_or_heuristic: 面板层优先固化“主文件 + layout + 下游交接”三件套，再由后续专门执行层决定是否做图像生成。
- prevention_or_replication_checklist:
  - [x] 主文件固定交付
  - [x] layout sidecar 固定交付
  - [x] 审计前置条件已写入合同
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/3-设定/4-面板/SKILL.md`
- user_feedback_or_constraint: 用户要求参考 `ZEN-VOID` 的设定面板层，但当前仓优先补主体面板真源，不直接复制批量生图执行脚本。

### Case-20260409-AIGC-SUBJECT-PANEL-REFERENCES

- milestone_type: source_contract_change
- outcome: 将 `4-面板` 重构为“主合同 + references 四模块”结构，保留面板主文件、layout sidecar 与下游参照交接不变。
- root_cause_or_design_decision: 旧版 `4-面板` 把真源判定、workflow、field map 与输出硬规则都压在单一 `SKILL.md` 里，继续维护时容易重新混淆“布局化”与“二次设计”。
- final_fix_or_heuristic: 主 `SKILL.md` 只保留边界、Visual Maps、摘要与 Root-Cause 闭环；详细 field map、workflow、域路由与输出契约拆到 `references/*.md`。
- prevention_or_replication_checklist:
  - [x] 已建立 `references/` 四件套
  - [x] 双产物交付保持不变
  - [x] “面板不二次设计”继续固定
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/references/execution-flow.md`
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/references/type-strategies.md`
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/references/output-template.md`
- user_feedback_or_constraint: 用户要求在不改变内容基础的前提下按最新规范重构 `4-主体` 全目录。

### Case-20260409-AIGC-SUBJECT-PANEL-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `4-面板/references/chain-of-thought.md` 升级为最新 `think-think` 合同，补入模式声明、对象专属启发式、工具后反思、可见/隐藏分层与验证矩阵。
- root_cause_or_design_decision: 旧版 `4-面板` 只说明了双产物和 handoff 要存在，但没显式压出“先确认继承关系与真源稳定度、再布局化、最后唯一交接”的判断顺序，容易变成二次设计。
- final_fix_or_heuristic: 保留 `FIELD-SPNL-01` 到 `FIELD-SPNL-04` 不变，把面板层核心思考显式压到 `继承稳定设计 -> 主文件/layout 同轴 -> 下游交接`，并补 `Gate Summary` 与工具后二次判断。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与对象`
  - [x] 已补面板层 `启发式工作链`
  - [x] 已补 `工具后反思`
  - [x] 已补 `Validation Matrix`
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求按最新思维链设计规范优化 `4-主体` 全目录的 thought contract。

# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-主体/subtypes/2-设计` 的经验层知识库，不是执行日志。
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
| 设计卡与 JSON 只有一侧存在 | 交付层 | 补齐双产物 | 把“人读卡 + 机读侧车”写成固定交付 | 下游不再只靠单一格式 |
| 设计完全脱离 `1-清单` bridge | 输入真源层 | 回到 bridge 重做设计裁决 | 在父技能写死“bridge 优先于临时猜测” | 设计能回查清单依据 |
| 没有 thinking sidecar | 设计解释层 | 补一份解释层 sidecar | 把 thinking 视为必交，而非附录 | 设计决策可追因 |

## Repair Playbook

1. 先看 `1-清单` 输入是否齐。
2. 再看是否同时生成了设计卡与设计 JSON。
3. 最后检查是否有 thinking sidecar 和下一步交接说明。

## Reusable Heuristics

- 主体设计最容易塌成“文案好看但不可继续消费”，所以双产物必须同时成立。
- thinking sidecar 的价值不是解释给用户听，而是给后续审计、面板和分镜提供决策证据。
- 只要 `1-清单` 没有统一好，`2-设计` 的输出就会很快漂移成多个版本。
- 对稳定内容输出技能，主合同最好只保留边界、摘要和 Mermaid，总细则沉到 `references/` 才更利于保持单一真源。
- `2-设计` 的新版 thought contract 要先确保“设计卡与 JSON 同轴成立”，再允许扩写 `thinking sidecar`；否则很容易产出一份会说话但不可消费的设计稿。

## Case Log

### Case-20260409-AIGC-SUBJECT-DESIGN-BASELINE

- milestone_type: source_contract_change
- outcome: 为 `4-主体/subtypes/2-设计` 建立了设计卡、机读侧车与 thinking sidecar 的三件套合同。
- root_cause_or_design_decision: 参考仓 `2-设计` 的核心价值是“把 bridge 变成设计真源”，当前仓因此保留其主链语义，但收敛为当前 `projects/<项目名>/主体/2-设计/` 的统一交付面。
- final_fix_or_heuristic: 对每个主体域固定“设计卡 + JSON + thinking sidecar”三件套，比只复刻上游脚本更适合当前仓的技能真源模式。
- prevention_or_replication_checklist:
  - [x] 双产物已固定
  - [x] thinking sidecar 已固定
  - [x] bridge 优先关系已写入合同
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/3-设定/2-设计/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 `ZEN-VOID` 的 `2-设计`，但当前仓应保持 `aigc` 技能树的阶段合同写法，不直接照搬自动出图脚本型入口。

### Case-20260409-AIGC-SUBJECT-DESIGN-REFERENCES

- milestone_type: source_contract_change
- outcome: 将 `2-设计` 重构为“主合同 + references 四模块”结构，保留设计卡、设计 JSON、thinking sidecar 的三件套交付不变。
- root_cause_or_design_decision: 旧版 `2-设计` 的三件套、workflow、field map 与 fallback 全堆在主合同里，继续升级时容易把边界说明与执行细则反复混写。
- final_fix_or_heuristic: 保留三件套语义、路径和主链顺序不变，只调整承载位置，把 field map、workflow、域路由与输出契约拆到 `references/*.md`。
- prevention_or_replication_checklist:
  - [x] 已建立 `references/` 四件套
  - [x] 三件套交付保持不变
  - [x] bridge 优先关系继续固定
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/references/execution-flow.md`
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/references/type-strategies.md`
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/references/output-template.md`
- user_feedback_or_constraint: 用户要求在不改变内容基础的前提下按最新规范重构 `4-主体` 全目录。

### Case-20260409-AIGC-SUBJECT-DESIGN-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `2-设计/references/chain-of-thought.md` 升级为最新 `think-think` 合同，补入模式声明、对象专属启发式、工具后反思、可见/隐藏分层与验证矩阵。
- root_cause_or_design_decision: 旧版 `2-设计` 只描述了“三件套要交付什么”，却没有显式说明“为何先锁设计卡/JSON 同轴、何时才允许补 thinking sidecar、怎样决定下一入口”，reasoning 模型容易生成单侧成品。
- final_fix_or_heuristic: 保留 `FIELD-SDES-01` 到 `FIELD-SDES-04` 不变，把设计层思考显式压到 `继承 bridge -> 卡/JSON 对齐 -> 设计理由 -> 下一入口`，同时加入 `Gate Summary` 与工具后二次判断。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与对象`
  - [x] 已补设计层 `启发式工作链`
  - [x] 已补 `工具后反思`
  - [x] 已补 `Validation Matrix`
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求按最新思维链设计规范优化 `4-主体` 全目录的 thought contract。

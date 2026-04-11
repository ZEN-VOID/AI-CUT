# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-主体/subtypes/1-清单` 的经验层知识库，不是执行日志。
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
| 三类主体被混成一张总表 | 输出合同层 | 回到分域落盘策略 | 在 `Canonical Landing` 固定三条独立产物线 | 下游能分别消费角色/场景/道具 |
| 清单只有名字，没有桥接字段 | 下游消费层 | 补齐 bridge JSON | 把 `bridge sidecar` 设为固定交付 | `2-设计` 不再重做解释层 |
| 同一主体多种写法未归一 | 命名层 | 做别名合并与变体说明 | 在 `命名归一` 字段中保留规范名 + 别名 | 同一主体不再重复出稿 |

## Repair Playbook

1. 先看主体是否已按角色/场景/道具分域。
2. 再看每个域是否都有 bridge sidecar。
3. 最后看命名归一与连续性说明是否足够支撑下游。

## Reusable Heuristics

- `1-清单` 的关键不是“列得全”，而是“列完以后下游不用再猜”。
- 若 `2-设计` 还得自己解释主体功能，说明 `1-清单` 的桥接层还没成立。
- 同名主体的处理要优先守住连续性，而不是急着拆成多个平行卡。
- 对这类稳定 leaf，主合同尽量只保留边界和回指，把分域判定、workflow 与交付硬规则沉到 `references/`。
- 清单层的新版 thought contract 应先压 `分域 -> bridge -> 命名归一 -> handoff`，而不是先把 `FIELD-*` 逐项展开成流水账步骤。

## Case Log

### Case-20260409-AIGC-SUBJECT-INVENTORY-BASELINE

- milestone_type: source_contract_change
- outcome: 为 `4-主体/subtypes/1-清单` 建立了主体抽取、分域落盘与 bridge 交接合同。
- root_cause_or_design_decision: 参考仓的 `1-清单` 强项不在脚本本身，而在“为设计阶段准备稳定 bridge”；当前仓因此收敛为统一清单技能，而不是继续拆成未治理 leaf。
- final_fix_or_heuristic: 先固定三类主体分域落盘，再固定每类都必须有 bridge JSON，确保 `2-设计` 有单一输入面。
- prevention_or_replication_checklist:
  - [x] 三类主体分域
  - [x] 每域都有 bridge sidecar
  - [x] 命名归一显式写入合同
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/3-设定/1-清单/角色清单/SKILL.md`
- user_feedback_or_constraint: 用户要求参考 `ZEN-VOID` 的设定清单能力，但当前仓先以统一父技能形态落地，不额外新建第二层未治理子目录。

### Case-20260409-AIGC-SUBJECT-INVENTORY-REFERENCES

- milestone_type: source_contract_change
- outcome: 将 `1-清单` 重构为“主合同 + references 四模块”结构，保留分域清单、bridge sidecar 与交接语义不变。
- root_cause_or_design_decision: 旧版 `1-清单` 把 field map、workflow、域路由与输出硬规则都写在单一 `SKILL.md` 中，后续继续维护时容易把细则与边界重新混在一起。
- final_fix_or_heuristic: 主 `SKILL.md` 只保留边界、Visual Maps、摘要和 Root-Cause 闭环；详细 field map、workflow、域路由与输出契约迁到 `references/*.md`。
- prevention_or_replication_checklist:
  - [x] 已建立 `references/` 四件套
  - [x] 分域落盘与 bridge sidecar 语义保持不变
  - [x] 主合同已收束为摘要型入口
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/references/execution-flow.md`
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/references/type-strategies.md`
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/references/output-template.md`
- user_feedback_or_constraint: 用户要求在不改变内容基础的前提下按最新规范重构 `4-主体` 全目录。

### Case-20260409-AIGC-SUBJECT-INVENTORY-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `1-清单/references/chain-of-thought.md` 升级为最新 `think-think` 规范，补入模式声明、对象专属启发式、工具后反思、Gate Summary 与验证矩阵。
- root_cause_or_design_decision: 旧版 `1-清单` 只有字段表和 pass table，虽然说明了输出要求，却没有显式逼出“先分域、再补 bridge、再做命名归一”的判断压力，容易让模型回退为简单摘抄。
- final_fix_or_heuristic: 保留 `FIELD-SINV-01` 到 `FIELD-SINV-04` 不变，把清单层的核心思考显式压到 `主体归域 -> bridge 充实 -> 命名归一 -> handoff 闭环`，并要求关键读取节点后做二次判断。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与对象`
  - [x] 已补清单层 `启发式工作链`
  - [x] 已补 `Gate Summary` 与 `Validation Matrix`
  - [x] 已补 `可见 / 隐藏分层`
- evidence_paths:
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求按最新思维链设计规范优化 `4-主体` 全目录的 thought contract。

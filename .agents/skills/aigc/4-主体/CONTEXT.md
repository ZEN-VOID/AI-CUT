# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-主体` 的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/4-主体/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 四个子目录存在但没有阶段入口 | 父级路由层 | 先补 `4-主体/SKILL.md + CONTEXT.md` | 把 `1-清单 -> 2-设计` 主链与 `3-4` 可选链写成父级真源 | 模糊请求能稳定落到单一子路径 |
| `3-审计` 或 `4-面板` 被误当成默认必经阶段 | 阶段语义层 | 回到父级重申主链优先 | 在父级 `子路径路由矩阵` 固化可选语义 | “继续 4-主体” 不再默认跳去审计/面板 |
| `2-设计` 绕过 `1-清单` 直接发明主体设定 | 真源边界层 | 退回 `1-清单` 先做主体归一与桥接 | 在父级与 `2-设计` 合同都写死“清单先于设计” | 下游设计均可回查清单证据 |
| 子技能已补齐，但 `aigc` 根入口仍写“待补合同” | 元路由层 | 同步更新 `.agents/skills/aigc/SKILL.md` 与根 `CONTEXT.md` | 把阶段状态同步视为阶段补建收尾动作 | 根入口能正确把请求路由到 `4-主体` |
| 项目已启用顾问团，但主体阶段未读取 `team.yaml` | 共享运行时层 | 执行前先读项目根 `team.yaml` 与 `_shared/council-runtime/module-spec.md` | 在 `4-主体` 根技能固化 `策划前置 + 评审闸门` 合同 | 主体任务进入前能判断是否要启用顾问团 |

## Repair Playbook

1. 先检查 `4-主体` 父级是否具备主链、可选链和阶段落点合同。
2. 再判断当前请求属于清单、设计、审计还是面板。
3. 若主链未完成，优先回到 `1-清单` 或 `2-设计`，不直接做扩展链。
4. 若子路径已补齐，还要同步检查根入口状态是否已更新。

## Reusable Heuristics

- 对主体阶段来说，最容易漂移的不是“角色/场景/道具谁更重要”，而是把 `审计`、`面板` 误当成默认必经链。
- `1-清单` 的价值不只是收集主体名，而是给 `2-设计` 提供统一的解释层和连续性边界。
- 当阶段从空骨架升级为可执行入口时，父级合同与根入口状态同步必须在同一轮完成。
- 对 `4-主体` 来说，顾问团最稳的节奏是“策划先校对象池和资产路线，评审最后卡 validation gate”，不要让评审代替设计判断。
- 对稳定阶段技能做规范升级时，优先把 field map、workflow、路由与输出硬规则迁到 `references/`，主合同只保留边界、摘要与回指。
- 对阶段级 `chain-of-thought` 来说，第一优先不是补字段表，而是先把“主链/扩展链/唯一下一入口”的路由压力显式化；否则 reasoning 模型仍会在父级层迷路。
- 对 `4-主体` 来说，技能阶段名可以保留编号，但项目 runtime 目录应优先服从 `_shared/project-runtime-layout.md` 的 `主体/` 映射，而不是直接照抄 `4-主体/`。

## Case Log

### Case-20260409-AIGC-SUBJECT-STAGE-BASELINE

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/4-主体` 建立了父级阶段合同与经验层，并把四个子路径纳入统一路由。
- root_cause_or_design_decision: 目录层已经存在 `1-清单 / 2-设计 / 3-审计 / 4-面板`，但父级与子级都没有实质合同，导致 `4-主体` 仍停留在“结构存在、不可执行”的状态。
- final_fix_or_heuristic: 先补父级 `SKILL.md + CONTEXT.md`，显式固定 `1-清单 -> 2-设计` 主链、`3-审计 / 4-面板` 可选链，再分别补四个子技能合同。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已补齐
  - [x] 父级 `CONTEXT.md` 已建立
  - [x] 四个子路径已纳入统一矩阵
  - [x] 根入口状态已计划同步
- evidence_paths:
  - `.agents/skills/aigc/4-主体/SKILL.md`
  - `.agents/skills/aigc/4-主体/CONTEXT.md`
  - `.agents/skills/aigc/4-主体/subtypes/1-清单/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/2-设计/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/3-审计/SKILL.md`
  - `.agents/skills/aigc/4-主体/subtypes/4-面板/SKILL.md`
- user_feedback_or_constraint: 用户明确要求参照 `AIGC-ZEN-VOID` 的设定阶段，完善当前仓 `4-主体` 下四个子技能，但必须改写为当前 `aigc` 技能树的父子合同风格。

### Case-20260409-AIGC-SUBJECT-COUNCIL-RUNTIME

- milestone_type: source_contract_change
- outcome: 为 `4-主体` 根技能接入了基于项目根 `team.yaml` 的顾问团运行时，默认执行 `策划前置 -> 主代理草案 -> 评审闸门`。
- root_cause_or_design_decision: 用户要求 `4-主体` 根技能及其叶子技能进入时都先判断顾问团是否启用，并落实 `策划 / 评审` 职责；若主体阶段继续只依赖上游文档而不读取项目团队真源，顾问角色就无法稳定介入。
- final_fix_or_heuristic: 主体阶段的顾问团运行时不应由四个子技能各自重写，而应由 `4-主体` 根技能读取项目根 `team.yaml` 并统一执行，子技能只继承阶段合同。
- prevention_or_replication_checklist:
  - [x] `4-主体/SKILL.md` 已新增 `Council Runtime Contract`
  - [x] 已固定 `策划前置 + 评审 validation gate`
  - [x] 子技能继续只承接内容合同
- evidence_paths:
  - `.agents/skills/aigc/4-主体/SKILL.md`
  - `.agents/skills/aigc/4-主体/CONTEXT.md`
  - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- user_feedback_or_constraint: 用户明确要求 `4-主体` 及其叶子技能进入时都先读取 `projects/<项目名>/team.yaml`，并默认启用 `策划 / 评审` 职责。

### Case-20260409-AIGC-SUBJECT-REFERENCES-REFRACTOR

- milestone_type: source_contract_change
- outcome: 将 `4-主体` 根技能重构为“主合同 + references 四模块”结构，保留阶段语义、路径、顾问团运行时与主链边界不变。
- root_cause_or_design_decision: 旧版根合同虽然信息完整，但 field map、workflow、路由矩阵与输出硬规则都堆在主文件内，不利于继续按最新规范维护单一真源。
- final_fix_or_heuristic: 主 `SKILL.md` 只保留边界、Visual Maps、摘要与 Root-Cause 闭环；详细 field map、workflow、VSM 路由与输出契约拆到 `references/*.md`。
- prevention_or_replication_checklist:
  - [x] 已建立根级 `references/` 四件套
  - [x] 主 `SKILL.md` 已收束为摘要型主合同
  - [x] 阶段路径、主链、顾问团运行时保持不变
- evidence_paths:
  - `.agents/skills/aigc/4-主体/SKILL.md`
  - `.agents/skills/aigc/4-主体/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/references/execution-flow.md`
  - `.agents/skills/aigc/4-主体/references/type-strategies.md`
  - `.agents/skills/aigc/4-主体/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求“加载最新的规范，重构 `.agents/skills/aigc/4-主体`，不改变内容基础”。

### Case-20260409-AIGC-SUBJECT-THINK-THINK-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `4-主体/references/chain-of-thought.md` 从旧式“字段表 + pass table”升级为最新 `think-think` 合同，补入模式声明、启发式工作链、可见/隐藏分层、工具后反思与 Gate Summary。
- root_cause_or_design_decision: 父级字段接口虽然存在，但旧版 thought contract 仍缺少“为什么先判主链、如何压制扩展链误入、何时给唯一下一入口”的显式判断压力，reasoning 模型容易退回成目录式摘要。
- final_fix_or_heuristic: 保留 `FIELD-SUBJECT-01` 到 `FIELD-SUBJECT-04` 不变，把真正的裁决压力压到 `主链优先 -> 唯一路由 -> canonical landing -> 阶段闭环`，并显式加入 `Gate Summary` 与工具后二次判断。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与对象`
  - [x] 已补根层专属 `启发式工作链`
  - [x] 已补 `可见 / 隐藏分层`
  - [x] 已补 `工具后反思` 与 `Validation Matrix`
- evidence_paths:
  - `.agents/skills/aigc/4-主体/references/chain-of-thought.md`
  - `.agents/skills/aigc/4-主体/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求按最新思维链设计规范优化 `4-主体` 与四个子路径的 `chain-of-thought.md`。

### Case-20260410-AIGC-SUBJECT-RUNTIME-DIR-RENAME

- milestone_type: source_contract_change
- outcome: 将主体阶段的 project runtime canonical landing 从带号目录收敛为 `projects/<项目名>/主体/`。
- root_cause_or_design_decision: 先前主体阶段默认把技能阶段号直接投影到项目路径，和用户要求的无序号 runtime 目录发生冲突。
- final_fix_or_heuristic: `4-主体` 应继续作为技能阶段名存在，但所有项目级路径、模板、执行流和 gate artifact 都必须写到 `projects/<项目名>/主体/`。
- prevention_or_replication_checklist:
  - [x] `4-主体/SKILL.md` 与 `references/*.md` 已切到 `projects/<项目名>/主体/`
  - [x] `team.yaml` gate artifact 已同步到 `projects/晴深不渝/主体/validation-report.md`
  - [x] 项目 runtime 目录已物理重命名为 `主体/`
- evidence_paths:
  - `.agents/skills/aigc/4-主体/SKILL.md`
  - `.agents/skills/aigc/4-主体/CONTEXT.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`
  - `projects/晴深不渝/team.yaml`
- user_feedback_or_constraint: 用户明确要求 `projects/晴深不渝/4-主体` 不要序号。

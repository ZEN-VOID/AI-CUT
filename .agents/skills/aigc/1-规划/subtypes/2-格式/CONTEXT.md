# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-规划/subtypes/2-格式` 的经验层知识库，不是过程日志。
- 进入 `2-格式` 时，应在父级 `1-规划/CONTEXT.md` 之后预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/SKILL.md` > 父级 `SKILL.md` > 本 `SKILL.md` > 父级 `CONTEXT.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 主 `SKILL.md` 同时承载流程、模板、判模细节，开始变成第二真源 | 真源治理层 | 把执行流、VSM、模板拆到 `references/` | 固化“主合同 + references 模块层”结构 | 主 `SKILL.md` 不再重复整套细则 |
| 只有 `标准剧/解说剧` 空目录，没有父级变体路由 | 父子路由层 | 先补 `2-格式` 父级合同与路由矩阵 | 固化“父级裁决变体，子级细写合同” | 从父级能唯一进入某个变体 |
| 直接复制参考仓的“正文改写技能”，导致规划阶段越权 | 阶段边界层 | 收回为“格式合同 + 样例 + 验证报告” | 在父子技能中显式声明“不直接代写整集正文” | 产物是规划合同，而不是成片正文 |
| `标准剧` 成了默认却没写清原因 | 判模层 | 在父级写明默认分支逻辑 | 固化“未显式解说则默认标准剧” | 未给出解说信号时不会误入旁白主导 |
| 无序 sibling 被误解为可以正式双开 | 调度语义层 | 在父级显式声明“分析可并行，正式落盘只取唯一主变体” | 将该规则写成父级硬门槛 | 不再同时产出两套正式主格式 |
| 样例只讲概念，不给下游可直接照抄的骨架 | 交接层 | 增补最小格式样例 | 固化“合同 + 样例”双轨输出 | 下游能直接按样例续跑 |
| 顾问团已启用，但 `2-格式` 没继承 `1-规划` 的阶段顾问运行时 | 继承层 | 明确本父技能继承上层 `1-规划` 的 `Council Runtime Contract` | 子技能不再重复发明第二套顾问团规则 | 进入 `2-格式` 时会先遵守项目根 `team.yaml` 判定 |

## Repair Playbook

1. 先检查父级 `1-规划` 是否已把任务正确路由到 `2-格式`。
2. 再在 `标准剧 / 解说剧` 间做唯一主变体裁决。
3. 先写变体合同，再写样例，不要反过来。
4. 正式落盘前补父级 `validation-report.md`，解释为何采用该变体。
5. 若参考仓内容与当前规划阶段职责冲突，以当前阶段边界为真源。

## Reusable Heuristics

- `2-格式` 最容易犯的错不是“写得太少”，而是把下游正文创作职责提前带进规划层。
- 对格式规划来说，父级最重要的价值是做“唯一变体裁决”；子级最重要的价值是把该变体写成可消费合同。
- 如果用户没明确说要旁白主导，先走 `标准剧`，通常比默认提升旁白密度更稳。
- 只给格式原则不够；必须同时给出最小样例，下游才能真正复用。
- 对 `2-格式` 来说，顾问团机制应该继承自 `1-规划` 根级，不应在父变体层再复制一套独立运行时。
- 对已进入稳定维护的技能来说，`references/` 最适合承接流程图、VSM 四件套与模板骨架；主 `SKILL.md` 只保留判定门槛与回链。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。

## Case Log

### Case-20260409-AIGC-PLAN-FORMAT-REFERENCE-REFACTOR

- milestone_type: source_contract_change
- outcome: 将 `2-格式` 父技能重构为“主合同 + references 模块层”，把思维链、执行流、VSM 四件套与输出模板从主 `SKILL.md` 下沉到 `references/`。
- root_cause_or_design_decision: 随着 `2-格式` 父技能不断补细则，主 `SKILL.md` 已开始同时承担流程、判模、模板三类说明，存在演化成隐藏第二真源的风险。
- final_fix_or_heuristic: 保留父级 `SKILL.md` 的边界、路由、字段门禁与闭环，把 `chain-of-thought / execution-flow / type-strategies / output-template` 作为唯一细则承载层。
- prevention_or_replication_checklist:
  - [x] 父级 `references/` 已建立 4 个核心模块
  - [x] 主 `SKILL.md` 已回链到模块真源
  - [x] VSM 四件套已迁入 `references/type-strategies.md`
  - [x] 输出模板已迁入 `references/output-template.md`
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/chain-of-thought.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/references/output-template.md`
- user_feedback_or_constraint: 用户明确要求“加载最新规范”并重构 `.agents/skills/aigc/1-规划/subtypes/2-格式`。

### Case-20260409-AIGC-PLAN-FORMAT-PARENT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/1-规划/subtypes/2-格式` 建立了父级格式规划合同，并把 `标准剧 / 解说剧` 两个空壳目录接回到可路由的父级入口。
- root_cause_or_design_decision: 用户要求完善 `标准剧`、`解说剧` 两个子目录，但直接技术阻塞是 `2-格式` 父级合同缺失，导致两个变体即使补齐也仍是孤岛。
- final_fix_or_heuristic: 先补 `2-格式/SKILL.md + CONTEXT.md`，再让父级显式承担变体裁决、验证汇总和下游交接；子技能只承接各自变体的格式合同与样例。
- prevention_or_replication_checklist:
  - [x] 父级变体路由矩阵已建立
  - [x] 已明确 `标准剧` 为默认分支
  - [x] 已明确“分析可并行、正式落盘只取唯一主变体”
  - [x] 已建立父级 `validation-report.md` 输出合同
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/标准剧/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/解说剧/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 `AIGC-ZEN-VOID` 的 `2-对白·独白·旁白` 双变体结构，同时补齐当前 `1-规划` 下的源层路由。

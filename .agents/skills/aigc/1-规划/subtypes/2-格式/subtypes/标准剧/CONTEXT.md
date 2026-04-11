# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-规划/subtypes/2-格式/subtypes/标准剧` 的经验层知识库，不是过程日志。
- 进入 `标准剧` 变体时，应在父级 `2-格式/CONTEXT.md` 之后预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 上层 `SKILL.md` > 本 `SKILL.md` > 上层 `CONTEXT.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 主 `SKILL.md` 一边讲规则一边塞模板，细则和主合同混成一层 | 真源治理层 | 把模板、流程、类型策略拆到 `references/` | 固化“子技能主合同 + references”结构 | 主 `SKILL.md` 不再重复整块模板 |
| 标准剧合同被写成高旁白密度 | 体裁边界层 | 收回到“表演优先、旁白从严” | 把“允许整场景零旁白”写成硬规则 | 样例中不再默认堆旁白 |
| 样例只有对白，没有动作画面承载 | 字段合同层 | 补 `动作画面` 为默认可用字段 | 固化“动作画面承载无台词推进” | 样例能体现无台词推进 |
| 直接照搬参考仓的正文改写规则 | 阶段边界层 | 重写为规划层合同和样例 | 显式声明本技能不代写整集正文 | 产物落为 `格式合同.md` 与 `格式样例.md` |
| 旁白主体口径漂移 | 字段一致性层 | 若启用旁白，统一规划为 `讲述者` | 在合同中固定主体口径 | 合同与样例口径一致 |

## Repair Playbook

1. 先确认父级已把任务裁决到 `标准剧`。
2. 先锁“表演优先、旁白从严”，再写字段。
3. 样例至少覆盖 `动作画面 + 对白 + 对白画面`，必要时再加独白。
4. 若样例里已经能靠表演表达，就不要额外补旁白。
5. 若参考仓细节超出规划层职责，只保留其高价值格式原则。

## Reusable Heuristics

- `标准剧` 的规划核心不是“字段越多越好”，而是“默认让表演和动作画面工作”。
- 对规划层来说，最稳的旁白规则不是“禁止旁白”，而是“只有必要时才允许启用旁白”。
- 如果一份标准剧样例读起来像讲解稿，通常不是文笔问题，而是变体判模已经跑偏了。
- 对 `标准剧` 这类叶子技能，模板、局部流程和变量策略很适合下沉到 `references/`；主 `SKILL.md` 只要守住变体边界与质量门槛。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。

## Case Log

### Case-20260409-AIGC-PLAN-FORMAT-STANDARD-REFERENCE-REFACTOR

- milestone_type: source_contract_change
- outcome: 将 `标准剧` 子技能重构为“主合同 + references 模块层”，并把局部流程、VSM 四件套与模板拆出主 `SKILL.md`。
- root_cause_or_design_decision: `标准剧` 已同时承载变体边界、详细模板与执行步骤，若继续堆叠会让局部模板与主合同发生双真源漂移。
- final_fix_or_heuristic: 主 `SKILL.md` 只保留变体边界、字段主表、硬门槛与回链；详细模板和类型策略以下沉的 `references/` 为真源。
- prevention_or_replication_checklist:
  - [x] `references/` 已建立 4 个核心模块
  - [x] 输出模板已迁入 `references/output-template.md`
  - [x] VSM 四件套已迁入 `references/type-strategies.md`
  - [x] 主 `SKILL.md` 已保留边界与字段主表
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/chain-of-thought.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/references/output-template.md`
- user_feedback_or_constraint: 用户要求按最新 `skill-内容输出型` 规范重构整个 `2-格式` 子树。

### Case-20260409-AIGC-PLAN-FORMAT-STANDARD

- milestone_type: source_contract_change
- outcome: 为 `1-规划/2-格式/subtypes/标准剧` 建立了规划层格式合同与经验层，并把参考仓的“标准剧”能力改写为当前仓可消费的规划真源。
- root_cause_or_design_decision: 用户指定参考 `AIGC-ZEN-VOID` 的 `标准剧`，但当前仓所需不是正文改写技能，而是先为后续脚本阶段规划标准剧格式边界。
- final_fix_or_heuristic: 继承参考仓的核心边界，包括“表演优先、旁白从严、同命题配对、动作剥离”，同时把产物改写为 `格式合同.md + 格式样例.md + validation-report.md`。
- prevention_or_replication_checklist:
  - [x] 已明确标准剧为默认变体
  - [x] 已写明允许整场景零旁白
  - [x] 已把动作画面保留为核心字段
  - [x] 已显式声明规划层不直接代写正文
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/标准剧/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/标准剧/SKILL.md`
- user_feedback_or_constraint: 用户要求参照 `AIGC-ZEN-VOID` 的 `标准剧`，同时当前仓默认交互与合同表达使用中文。

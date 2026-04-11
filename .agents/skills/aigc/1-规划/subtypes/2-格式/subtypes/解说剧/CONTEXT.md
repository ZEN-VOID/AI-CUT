# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/1-规划/subtypes/2-格式/subtypes/解说剧` 的经验层知识库，不是过程日志。
- 进入 `解说剧` 变体时，应在父级 `2-格式/CONTEXT.md` 之后预加载本文件。
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
| 主 `SKILL.md` 同时塞满模板、流程、边界，导致子技能正文过重 | 真源治理层 | 把模板、流程、类型策略拆到 `references/` | 固化“子技能主合同 + references”结构 | 主 `SKILL.md` 只保留边界与主表 |
| 没有解说信号却误入解说剧 | 变体判模层 | 回退到父级重新裁决，优先考虑标准剧 | 把“必须存在解说信号”写成进入门槛 | 非解说项目不再默认旁白主导 |
| 旁白主体出现多个称呼 | 字段一致性层 | 统一回写为 `讲述者` | 在合同中固定主体口径 | 样例与合同口径一致 |
| 为了旁白主导而吞掉原始对白 | 对白边界层 | 重申“对白保真，非对白旁白化” | 在合同中显式拆开两者职责 | 解说剧仍保留对白层 |
| 内心独白默认开启，导致层级膨胀 | 变体约束层 | 把内心独白改回默认关闭 | 固化“仅用户显式要求时启用” | 样例中不再默认出现独白层 |

## Repair Playbook

1. 先确认父级已把任务裁决到 `解说剧`，且存在明确解说信号。
2. 先锁“旁白主导、对白保真”，再写字段。
3. 样例至少覆盖 `旁白 + 旁白画面 + 动作画面 + 对白` 四件套。
4. 旁白主体统一为 `讲述者`，不要在合同中平行造词。
5. 若没有额外要求，不默认加 `内心独白`。

## Reusable Heuristics

- `解说剧` 的规划核心不是“旁白越多越好”，而是“旁白成为非对白信息的稳定主通道”。
- 解说剧最容易出的问题是把对白也一并解释化；一旦这样做，变体就失去了戏剧支点。
- 如果一份解说剧合同说不清“谁在讲”，那它通常还不具备真正可消费的下游格式价值。
- 对 `解说剧` 这类叶子技能，最容易漂移的是“旁白规则 + 模板示例”混写；拆出 `references/` 后更容易稳住主从关系。
- 对长期维护的可执行技能目录，除 `SKILL.md + CONTEXT.md` 外，还应补齐 `agents/openai.yaml`，这样 Codex / OpenAI 侧的展示名、摘要和默认提示才有稳定入口。

## Case Log

### Case-20260409-AIGC-PLAN-FORMAT-EXPLAINER-REFERENCE-REFACTOR

- milestone_type: source_contract_change
- outcome: 将 `解说剧` 子技能重构为“主合同 + references 模块层”，把局部流程、VSM 四件套与模板从主 `SKILL.md` 下沉。
- root_cause_or_design_decision: `解说剧` 的模板与边界若继续共写在主文，会使“旁白主导”“对白保真”“主体统一”三类规则难以保持单点真源。
- final_fix_or_heuristic: 主 `SKILL.md` 只保留进入条件、边界、字段主表与门槛；模板、执行流与变量策略改由 `references/` 承载。
- prevention_or_replication_checklist:
  - [x] `references/` 已建立 4 个核心模块
  - [x] 输出模板已迁入 `references/output-template.md`
  - [x] VSM 四件套已迁入 `references/type-strategies.md`
  - [x] 主 `SKILL.md` 已保留进入条件与字段主表
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/references/chain-of-thought.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/references/execution-flow.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/references/type-strategies.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/references/output-template.md`
- user_feedback_or_constraint: 用户要求按最新 `skill-内容输出型` 规范重构整个 `2-格式` 子树。

### Case-20260409-AIGC-PLAN-FORMAT-EXPLAINER

- milestone_type: source_contract_change
- outcome: 为 `1-规划/2-格式/subtypes/解说剧` 建立了规划层格式合同与经验层，并把参考仓的“解说剧”能力改写为当前仓可消费的规划真源。
- root_cause_or_design_decision: 用户要求参照 `AIGC-ZEN-VOID` 的 `解说剧`，但当前仓真正需要的是先把“旁白主导、对白保真、主体统一”的格式边界规划清楚，而不是直接重写整集正文。
- final_fix_or_heuristic: 继承参考仓的核心边界，包括“非对白旁白化、旁白主体统一为讲述者、对白保真、内心独白默认关闭”，同时把产物改写为规划层的 `格式合同.md + 格式样例.md + validation-report.md`。
- prevention_or_replication_checklist:
  - [x] 已把进入条件限定为显式解说信号
  - [x] 已统一旁白主体为 `讲述者`
  - [x] 已明确“对白保真，非对白旁白化”
  - [x] 已把内心独白设为默认关闭
- evidence_paths:
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/SKILL.md`
  - `.agents/skills/aigc/1-规划/subtypes/2-格式/subtypes/解说剧/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白/解说剧/SKILL.md`
- user_feedback_or_constraint: 用户要求当前仓的 `标准剧/解说剧` 结构参照 `AIGC-ZEN-VOID`，但需落到 `1-规划/2-格式` 的规划语境中。

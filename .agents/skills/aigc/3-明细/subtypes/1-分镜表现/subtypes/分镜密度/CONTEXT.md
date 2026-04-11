# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `1-分镜表现/分镜密度` 的经验层知识库，不是执行日志。
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
| 分镜数靠直觉平均分配 | 裁决链层 | 回到“三层密度裁决” | 固化 `rhythm -> refined_range -> discrete count` | 每组镜数有可追溯依据 |
| `1帧` 被误用 | 特例层 | 重新检查 `single_panel_long_take` 证据并剔除 `1` | 在真源中固化“`1帧` 是特权 + 无证据回退到 `2`” | `1帧` 仅出现在低能留白且有明确导演证据的场景 |
| 多镜但没有句段锚点 | 输出层 | 同步补句段锚点表 | 把锚点作为强制输出字段 | 每镜可定位 |
| 高爆发段仍被压低镜数 | tie-break 层 | 在候选值中向上取势 | 固化“多个值都成立时取较高值” | 爆发段镜数不再保守塌缩 |
| `refined_range` 无交集却假装精确命中 | 回退层 | 显式记录“按节奏优先保守回退” | 在 type strategy 固化冲突回退文案 | 输出里能追到回退说明 |
| 镜数虽合法但承载不出视觉峰值 | 审美势能层 | 对候选值执行 `Aesthetic Pressure Test` 并优先上调一帧 | 把 `aesthetic_peak_plan` 与 `FAIL-COMPOSITION-FLATLINE` 写入字段合同 | 至少存在一帧峰值机会 |
| 高镜数退化为平均快切或低镜数退化为空洞模板 | 模板门控层 | 依据 `panel_count -> template_id` 重查景别/角度/滑窗/功能位约束 | 把模板级反平庸门控写入 `output-template` 真源，并在 thought pass 挂返工入口 | 模板门控判定为 `pass` |

## Repair Playbook

1. 先判节奏，再判场景类型与信息负载。
2. 再用时长提示与表达负载把区间收窄到 `refined_range`。
3. 再从候选整数里做可拍性、可读性和 `Aesthetic Pressure Test`，收敛到唯一值。
4. 再为每镜分配句段锚点、功能位与峰值机会。
5. 最后把结果交给 `分镜构图`。

## Reusable Heuristics

- 密度最稳的判法不是“看上去该几镜”，而是先回答“这组戏的呼吸是什么”。
- 当多个候选镜数都成立时，默认向更有势能的较高值取，不然很容易写成保守平镜。
- 密度输出如果没有锚点表，后续插入阶段就等于没法执行。
- `1帧` 成立的关键不是“区间里允许 1”，而是“零切换比两次切换更有力量”有无明确证据。
- 镜数裁决不是只保信息完整，还要保住至少一帧构图审美峰值的承载空间。
- 同一个 `panel_count` 不是天然成立，必须再问一句：这组镜数有没有能力长成不平庸的模板，而不是平均快切或固定正反打。

## Case Log

### Case-20260409-AIGC-SCRIPT-STORYBOARD-DENSITY

- milestone_type: source_contract_change
- outcome: 为 `分镜密度` 建立了面向脚本阶段的镜数裁决合同，使其只负责 `panel_count + 句段锚点 + 功能位`。
- root_cause_or_design_decision: 用户要求分镜数量由“分镜密度的分析和决断”来控制，因此必须把“几镜”从父级和构图子技能里抽离出来，形成单独真源。
- final_fix_or_heuristic: 从 ZEN-VOID 的导演阶段密度方法中提炼出适用于脚本内联阶段的三层裁决链，同时显式加入锚点表输出，避免只有镜数没有插入落点。
- prevention_or_replication_checklist:
  - [x] 已固定三层密度裁决
  - [x] 已把 `1帧` 收为特例
  - [x] 已要求输出句段锚点表
  - [x] 已把功能位纳入输出
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/5-分镜构图/SKILL.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/2-导演/5-分镜构图/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求“分镜数量取决于子技能：分镜密度的分析和决断”。

### Case-20260409-AIGC-SCRIPT-STORYBOARD-DENSITY-B

- milestone_type: source_contract_change
- outcome: 将 `分镜密度` 的镜数域、三级渐进裁决、长镜头特例门槛与审美势能测试分配进主合同与四个 reference 真源，避免旧版区间与粗放规则继续并存。
- root_cause_or_design_decision: 用户提供了更新后的 `1-15` 强裁决规范；原技能已有三层框架，但基础区间、场景收窄、`1帧` 证据门槛、无交集回退和构图峰值约束仍不够精确，若只大段插入正文会形成并列真源。
- final_fix_or_heuristic: 将“区间与回退”落到 `type-strategies`，将“字段与失败码”落到 `chain-of-thought`，将“写位与必填解释”落到 `output-template`，将“执行顺序与门禁先后”落到 `execution-flow`，主 `SKILL.md` 仅保留摘要级回指。
- prevention_or_replication_checklist:
  - [x] 已把基础区间改为 `1-2 / 2-4 / 5-7 / 8-12 / 13-15`
  - [x] 已固化 `single_panel_long_take` 证据门槛
  - [x] 已加入 `Aesthetic Pressure Test`
  - [x] 已加入 `FAIL-COMPOSITION-FLATLINE`
  - [x] 已加入“无交集，按节奏优先保守回退”
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/references/type-strategies.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/references/execution-flow.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“如已有相关内容不必赘述，仅作缺失补全”，因此采用按真源职责分配的融合式补全，而非整段粗插。

### Case-20260409-AIGC-SCRIPT-STORYBOARD-DENSITY-C

- milestone_type: source_contract_change
- outcome: 为 `分镜密度` 增加了按 `panel_count` 派生的模板级反平庸门控，使镜数裁决不只“合法”，还要具备可被设计成不平庸分镜组的能力。
- root_cause_or_design_decision: 用户追加的是模板级属性约束，不是新的一级裁决器；如果直接并入第一轮镜数决定，会与既有三级渐进裁决发生夺权冲突。
- final_fix_or_heuristic: 把完整门控矩阵落到 `output-template` 作为验收真源，把返工入口挂到 `chain-of-thought` 与 `execution-flow`，继续保持“先定镜数、后验模板”的职责边界。
- prevention_or_replication_checklist:
  - [x] 已建立 `panel_count -> template_id` 映射门控
  - [x] 已加入 `FAIL-SBD-TEMPLATE-GATE`
  - [x] 已要求模板门控失败时优先回到 `S6`，必要时回到 `S3`
  - [x] 已保持模板门控不抢第一轮裁决权
- evidence_paths:
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/references/execution-flow.md`
  - `.agents/skills/aigc/3-明细/subtypes/1-分镜表现/subtypes/分镜密度/CONTEXT.md`
- user_feedback_or_constraint: 用户明确以“反平庸门控（Mandatory）”追加模板矩阵，要求继续采用融合式分配，而不是粗糙拼接。

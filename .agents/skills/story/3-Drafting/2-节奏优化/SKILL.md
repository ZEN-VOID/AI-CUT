---
name: story-drafting-pacing
description: Use when `3-Drafting` needs the governed child skill that realizes planning-locked chapter rhythm into readable pulse, paragraph breathing, and chapter momentum on top of the current episode draft.
governance_tier: lite
---

# 3-Drafting / 2-节奏优化

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读父层 `3-Drafting/SKILL.md` 与 `../_shared/drafting-child-output-contract.md`。
- 必须同时读取 `../_shared/drafting-instant-validation-contract.md`，把本 child 放回父层的 `start-step -> complete-step -> inline validation -> pass or block` 正式链位中理解。
- 若当前 step 要引用本集 chapter board，必须先读取 `../_shared/chapter-board-locating-contract.md`，禁止靠数组顺序猜本集 board。
- 必须同时读取 `../../_shared/core-constraints.md`，把 shared 章节硬约束投影到当前 pacing pass，而不是只做局部字面调快。
- 必须同时读取 `../../_shared/chapter-rhythm-handoff-contract.md` 与 `references/chapter-rhythm-engine.md`，把 planning 已声明的章级 handoff 装进本 step，并只在正文兑现层做动作。
- 正式处理前，必须读取 Step 1 已写回后的当前 `第N集.md`。

## Parent Positioning

本 child 负责：

- 消费 planning 已锁定的节奏 handoff
- 建立本集 `pulse_ladder`
- 修正段落脉冲、推进间距、reaction bridge、中段发展和章末钩子密度
- 在不破坏 planning 义务与设定物理的前提下，把已锁 mode 兑现成正文体感
- 让章节读起来不是“记账式平推”

它不负责：

- 重起剧情骨架
- 重定义 `selected_pack / selected_mode / 七步职责映射`
- 发明新的 chapter board 功能债、主事件或世界规则
- 专门补景物描写
- 专门补角色细节
- 专门做对白声口与终修

## Canonical Sources

- `../SKILL.md`
- `../CONTEXT.md`
- `../_shared/chapter-board-locating-contract.md`
- `../_shared/drafting-child-output-contract.md`
- `../_shared/drafting-instant-validation-contract.md`
- `../../_shared/context-loading-contract.md`
- `../../_shared/chapter-rhythm-handoff-contract.md`
- `../../_shared/core-constraints.md`
- `references/chapter-rhythm-engine.md`

## Constraint Projection Contract

| constraint_family | pacing projection | current gate |
| --- | --- | --- |
| `规划真源即法律` | 节奏重排只能重分布段落脉冲、兑现间距与段尾牵引，不得擅自改 chapter board 功能、删掉本章应回应的承诺。 | 若删改后本章功能债或上章承接失效，必须回退重排。 |
| `设定即物理` | 不得靠发明新招式、新道具、新规则制造“更有劲”的节奏。 | 若节奏提升依赖新增设定，判定为无效优化。 |
| `发明需识别` | 若确需突出新实体，名称、作用和辨识线索必须明确，不得用模糊代称硬推高潮。 | 模糊新实体不得进入正式正文。 |
| `Hard` | 本章必须仍然可读、有推进、能回应上章承诺、无占位正文。 | 任一项失效都视为 pacing rewrite 失败。 |
| `Soft` | 优先压缩长铺垫、重分配脉冲、强化章末期待，不追求机械字数阈值。 | 若只是整体裁字但局面变化仍稀薄，视为无效。 |
| `Style` | 用动作反应、带意图对白、未闭合期待支撑节奏，而不是靠说明句堆推进。 | 连续解释段未被切开时不得宣布通过。 |

## Root-Cause Execution Contract

当本 step 出现“越改越快但越空”“删断因果”“章末失钩”“靠新设定硬加速”等问题时，必须先上溯源层而不是只补一两句：

`Symptom/Failure -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

1. `../../_shared/core-constraints.md` 是否未被真正装配进当前 step。
2. 当前 `Thinking-Action Network` 是否缺少“规划/承诺/设定”门禁节点。
3. `Lite Field Contract` 是否只检查“快了没有”，而没检查“法律和物理还在不在”。

用户闭环必须至少说明：

- 根因位置
- 立即修复
- 系统预防修复

## Business Requirement Analysis Contract

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 让 planning 已锁好的章级节奏在正文里真正可感，而不是停留在 chapter board 上。 |
| `business_object` | Step 1 后的当前正文、当前 `第V卷.写作日志.yaml`、`2-Planning/整体规划.md`、当前卷 `卷规划.md`、当前章 `第N章.md` 的本章义务、shared core constraints，以及当前项目的 `类型卡 / 题材走廊`。 |
| `constraint_profile` | 不改 planning 义务、`selected_pack / selected_mode` 与世界规则，但允许在合法边界内重排场面密度、reveals、反应位与局部顺序；必须继续遵守规划真源、设定边界、推进下限、上章承诺回应与章末期待约束。 |
| `success_criteria` | 读者能明显感知推进、停顿、加压和章末牵引，同时章节仍能回答“发生了什么/为什么现在这样”。 |
| `non_goals` | 不重写 chapter board、设定系统、世界规则或终修文风；但可对本章主事件的显影顺序、段位收放、反应/兑现落点做有限重排。 |
| `complexity_source` | 复杂度来自“节奏变形”很容易伤到因果承接、上章回应、章末牵引和设定物理。 |
| `topology_fit` | `root reread -> planning handoff projection -> pulse ladder -> drag/skip diagnosis -> pacing rewrite -> compliance audit` |
| `step_strategy` | 先锁本章不可破坏的法律、物理和 planning handoff，再把已锁定的节奏义务编排成章内 `pulse_ladder`，并在合法边界内对 reveal、reaction、并段/拆段、局部前后次序做重排与重写。 |

## Total Input Contract

- 必需输入：
  - 当前 `第N集.md`
  - `第V卷.写作日志.yaml`
  - `2-Planning/整体规划.md`
  - 当前卷 `2-Planning/第V卷/卷规划.md`
  - 当前章 `2-Planning/第V卷/第N章.md`
  - `../../_shared/core-constraints.md`
- 硬规则：
  - 必须先保住 Step 1 的事件逻辑，再谈节奏优化。
  - “保住 Step 1 的事件逻辑”指保住因果、义务、承接与设定边界，不等于冻结 Step 1 的段位顺序、reveals 时机或中段收放。
  - 节奏优化不得靠删掉必要信息制造“快感”。
  - 若上章有明确承诺，本 step 不得把回应段删成失忆式略过。
  - 不得用新能力、新道具、新规则制造假高潮。
  - 允许的合法动作包括：并段、拆段、前移有效脉冲、后置解释、补 reaction bridge、交换局部场面先后、把 promised collision 前的拖沓段改写成 `发展 / 升级`。
  - 整章至少保留一项清晰推进；若 rewrite 后仍“整章无收获”，视为失败。

### Soft / Style Projection

- 优先把长铺垫切成“信息 + 动作/反应 + 局面变化”。
- 开头若迟迟不进冲突、风险或强情绪，应优先前移有效脉冲。
- 第一屏或前两段必须尽快交代“现在为什么值得读下去”，避免把 hook 全拖到中后段。
- 本章必须尽早让读者知道“这章到底要兑现什么问题/欲望/压力”，避免只有氛围没有交易。
- 不得连续堆两个以上高压钩子却没有任何局部兑现，否则会把章节读感写成纯拉扯。
- 章末若平收，应优先补未闭合期待、代价余波或下一步压力，而不是只加一个问号句。
- 尾钩不必总是爆炸式 cliffhanger；`reveal / decision / threat / pressure transfer / quiet unease` 都可以，但必须自然长在本章正文里。

## Planning Handoff Consumption Contract

本 step 必须从 planning 读取，而不是自己重新定义：

- `selected_pack`
- `selected_mode`
- 七步职责映射
- `entry_promise`
- `conflict_axis`
- `micro_payoff`
- `exit_hook`
- `义务段位`
- `建议写法`

硬规则：

- `selected_pack / selected_mode` 只可消费，不可在本 step 重定义。
- `entry_promise` 和 `exit_hook` 必须被正文感知，但其具体段落长度和字面顺序可以重排。
- `micro_payoff` 不要求每章大高潮，但要求每章至少有一次“局面真的变了”。
- `建议写法` 可以调整；`义务段位` 不得静默删失。

## Output Contract

- `manuscript_patch`
  - 节奏重排后的正文
  - 本 step 是正文 frontmatter 中 `rhythm_type` 的 owning step；必须使用英文字段名 `rhythm_type` 写回当前集节奏类型
  - `rhythm_type` 的合法值固定为 `势能式` 或 `动能式`，依据 planning 已锁定的 `selected_mode / selected_mode_label` 判定
  - `process_log_entry`
  - `step_id: 2`
  - `focus_dimension: pacing_matrix`
  - 必须记录本轮如何投影 `core-constraints`，尤其是：
    - planning 已锁 handoff 如何被安放并编排成 `pulse_ladder`
    - 保留了哪些本章规划义务
    - 修复了哪些空转段/跳切段
    - 章末期待如何被保留或增强
    - 若存在明确 `类型卡`，本轮采用了哪些题材节奏偏置与硬约束
- owned manuscript dimension：
  - 段落脉冲
  - 推进节奏
  - 章内收放

## Immediate Validation Hook Contract

- 本 child 在正式 runtime 中只占据 `start-step -> complete-step -> inline validation` 这一个 step 区段；整条链由父层按 `start-task -> start-step -> complete-step -> inline validation -> pass or block` 驱动。
- 当前 step 写回后，父层必须立刻按 `../../4-Validation/_shared/validation-dimension-registry.yaml` 触发当前 step 登记的 inline validators。
- 只有当前 gate 明确 `pass`，Step 3 的 `start-step` 才成立。
- 若 hook 失败且 `rework_target_step == Step 2`，必须留在 Step 2 重写并重跑 gate。
- 若 hook 指向更早受影响 drafting step 或上游 `source_layer_owner`，必须按 shared contract 回卷或停止 drafting 转 source fix；不得把 block 态伪装成“已自然进入 Step 3”。

## Visual Map

```mermaid
flowchart TD
    A["N1 回读正文 / 日志 / planning handoff"] --> B["N2 投影法律 / 物理 / planning obligations"]
    B --> C["N3 解码已锁 handoff"]
    C --> D["N4 建立 pulse ladder"]
    D --> E["N5 补 reaction bridge / middle build"]
    E --> F["N6 识别拖沓 / 跳切 / 弱兑现"]
    F --> G["N7 节奏重写"]
    G --> H["N8 合规审计 + hook gate"]
```

```mermaid
flowchart LR
    A["planning handoff"] --> B["selected_pack / selected_mode"]
    A --> C["七步职责映射"]
    A --> D["entry_promise / conflict_axis"]
    A --> E["micro_payoff / exit_hook"]
    A --> F["义务段位 / 建议写法"]
    B --> G["Step 2 只做正文兑现"]
    C --> G
    D --> G
    E --> G
    F --> G
```

```mermaid
flowchart LR
    A["合法 rewrite"] --> B["并段 / 拆段"]
    A --> C["前移有效脉冲 / 后置解释"]
    A --> D["reaction bridge / middle build"]
    A --> E["段尾牵引 / 章末续推"]
    B --> F["都必须服从 planning handoff"]
    C --> F
    D --> F
    E --> F
```

```mermaid
stateDiagram-v2
    [*] --> RereadCurrent
    RereadCurrent --> ConstraintProjected
    ConstraintProjected --> HandoffDecoded
    HandoffDecoded --> PulseMapped
    PulseMapped --> MiddleBuilt
    MiddleBuilt --> Diagnosed
    Diagnosed --> Rewriting
    Rewriting --> ComplianceAudited
    ComplianceAudited --> Passed
    ComplianceAudited --> ReworkCurrentStep
```

## Thinking-Action Network

| node_id | field_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N1-ROOT-REREAD` | `FIELD-DR2-01` | 回读当前正文、日志与 planning handoff，锁当前 step 的真实输入面 | Step 1 正文、`第V卷.写作日志.yaml`、chapter board、planning handoff、reader signal | 读取 Step 1 结果、最近 hook 摘要、当前集 planning handoff 与上一章承诺承接位 | `input_note` | pass -> `N2`；正文/handoff 缺失 -> 留在 `N1` | 只有正文、日志和 planning handoff 同时可读时才允许继续 |
| `N2-CONSTRAINT-PROJECTION` | `FIELD-DR2-02` | 把法律、物理、上章承诺与 planning 义务同时投影进本 step | `N1` 输入、`core-constraints`、planning 义务 | 对齐 chapter board、上章承诺、设定边界、Hard/Soft/Style 约束，并锁“哪些是义务、哪些只是建议写法” | `constraint_note` | pass -> `N3`；法律/handoff 任一不清 -> 回 `N2` | 只有“规划没丢、设定没破、handoff 已锁”三者同时成立时才可进入正文兑现 |
| `N3-HANDOFF-DECODE` | `FIELD-DR2-03` | 解码 planning 已锁 handoff，而不是在本 step 重新定义骨架 | `N2` 约束、`selected_pack / selected_mode / 七步职责映射 / 规划义务` | 逐一确认当前章必须兑现的 promise、冲突、payoff、尾钩与 mode 体感 | `handoff_note` | pass -> `N4`；handoff 仍需二次猜测 -> 回 `N3` | Step 2 必须消费 planning，而不是自己发明第二套章级结构 |
| `N4-PULSE-LADDER` | `FIELD-DR2-04` | 把 planning handoff 编排成可感的章内脉冲梯子 | `N3` handoff、正文当前版本 | 标出推进点、改向点、陷深点、峰值点与尾钩区，形成初版 `pulse_ladder` | `pulse_note` | pass -> `N5`；义务存在但读感无起伏 -> 回 `N4` | 章内必须出现清晰的读感起伏，而不是把 planning 提纲直接翻写 |
| `N5-MIDDLE-BUILD` | `FIELD-DR2-05` | 补足 reaction bridge 与中段发展，让 mode 真正落地 | `N4` pulse ladder、中段正文 | 检查转折后是否有持续纠葛、继续陷深或再升压，并补足 reaction / entanglement / escalation | `middle_note` | pass -> `N6`；中段空转或直接跳高潮 -> 回 `N5` | 中段必须既能承接 planning 义务，也能提供正文呼吸 |
| `N6-DRAG-DIAGNOSIS` | `FIELD-DR2-06` | 识别本集真正的节奏故障，而不是泛泛说“还不够快” | `N5` 中段结构、正文问题段 | 定位平推、跳切、弱兑现、只拉不收、高潮无积累等问题 | `diagnosis_note` | pass -> `N7`；问题定位太笼统 -> 回 `N6` | 必须能回答“哪一段坏、坏在哪一层、该回哪一类动作修” |
| `N7-PACING-REWRITE` | `FIELD-DR2-07` | 在不破法律/物理与 planning handoff 的前提下完成节奏重写 | `N6` 诊断、planning handoff、pulse ladder | 调整段落长度、顺序、留白、补反应桥、强化中段和高潮、兑现 `micro_payoff / exit_hook` | `rewrite_note` | pass -> `N8`；靠删空因果或改写 planning 义务提速 -> 回 `N7` | rewrite 后必须既守 planning，又让章级 handoff 真正落进正文 |
| `N8-COMPLIANCE-AUDIT` | `FIELD-DR2-08` | 做当前 step 的最终汇流审计，并为 inline hook 提供证据 | `N7` 节奏版正文、当前 gate 要求 | 检查规划义务、设定物理、推进下限、本章兑现、mode 一致性、尾钩与占位禁令 | `compliance_note` | pass -> done；Step 2 自修 -> 回 `N7`；更早 step/source fix -> 回卷 | 只有“快而不空、mode 不漂、hook 可过”时才允许进入 Step 3 |

## Lite Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-DR2-01` | 当前正文与日志 | 已回读 Step 1 正文、日志与最近 hook 摘要 | `FAIL-DR2-01` | `N1` |
| `FIELD-DR2-02` | 约束投影 | 已锁定规划义务、设定边界、Hard/Soft/Style 门禁与“义务 vs 建议写法”边界 | `FAIL-DR2-02` | `N2` |
| `FIELD-DR2-03` | planning handoff decode | `selected_pack / selected_mode / 七步职责映射 / 四个节奏义务` 已被明确消费，无需本 step 二次猜测 | `FAIL-DR2-03` | `N3` |
| `FIELD-DR2-04` | pulse ladder | 已有章内节奏梯子，且标出峰值点与章末期待区 | `FAIL-DR2-04` | `N4` |
| `FIELD-DR2-05` | middle build | 中段已有持续纠葛、陷深或再升压，不再发空 | `FAIL-DR2-05` | `N5` |
| `FIELD-DR2-06` | 节奏问题表 | 拖沓/跳切/平推/弱钩子/只拉不收问题已定位 | `FAIL-DR2-06` | `N6` |
| `FIELD-DR2-07` | 节奏版正文 | 推进与收放明显改善，且已安放 `micro_payoff / exit_hook`，未靠删空因果或硬造新设定提速 | `FAIL-DR2-07` | `N7` |
| `FIELD-DR2-08` | 合规审计摘要 | 章节仍可读、有推进、回应承诺、mode 一致、完成至少一处局部兑现、无占位、章末保有期待 | `FAIL-DR2-08` | `N8` |

## Completion Contract

- 当前正文已具备可感知的章内脉冲。
- 当前正文已把 planning 已锁的章级 handoff 兑现成有效 `pulse_ladder`。
- 当前正文的 `势能式 / 动能式` mode 已与 planning 声明保持一致。
- 当前正文 frontmatter 中的 `rhythm_type` 已与本轮 mode 判定一致，并已写回 `势能式` 或 `动能式`。
- 当前正文仍满足 `core-constraints` 的三大定律与章节 Hard 约束。
- `process_log_entry` 已说明本次节奏调整聚焦了哪些问题，以及如何守住规划义务、设定边界与章末期待。

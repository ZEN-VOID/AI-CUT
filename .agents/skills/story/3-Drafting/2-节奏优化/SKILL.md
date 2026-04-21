---
name: story-drafting-pacing
description: Use when `3-Drafting` needs the governed child skill that rebuilds pulse, pacing matrix, and chapter momentum on top of the current episode draft.
governance_tier: lite
---

# 3-Drafting / 2-节奏优化

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读父层 `3-Drafting/SKILL.md` 与 `../_shared/drafting-child-output-contract.md`。
- 必须同时读取 `../_shared/drafting-instant-validation-contract.md`，把本 child 放回父层的 `start-step -> complete-step -> inline validation -> pass or block` 正式链位中理解。
- 若当前 step 要引用本集 chapter board，必须先读取 `../_shared/chapter-board-locating-contract.md`，禁止靠数组顺序猜本集 board。
- 必须同时读取 `../../_shared/core-constraints.md`，把 shared 章节硬约束投影到当前 pacing pass，而不是只做局部字面调快。
- 必须同时读取 `references/chapter-rhythm-engine.md`，把“单章节奏七段发动机”装进本 step，而不是只靠经验裁字。
- 正式处理前，必须读取 Step 1 已写回后的当前 `第N集.md`。

## Parent Positioning

本 child 负责：

- 建立本集节奏矩阵
- 修正段落脉冲、推进间距、转折位置和章末钩子密度
- 让章节读起来不是“记账式平推”

它不负责：

- 重起剧情骨架
- 专门补景物描写
- 专门补角色细节
- 专门做对白声口与终修

## Canonical Sources

- `../SKILL.md`
- `../CONTEXT.md`
- `../_shared/chapter-board-locating-contract.md`
- `../_shared/drafting-child-output-contract.md`
- `../_shared/drafting-instant-validation-contract.md`
- `../../_shared/type-pack-loading-contract.md`
- `../../_shared/context-loading-contract.md`
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
| `business_goal` | 让章节具备推进节奏、呼吸感和章内脉冲，而不是只把事情按时间顺序摆出来。 |
| `business_object` | Step 1 后的当前正文、当前 `写作日志.yaml`、`2-Planning/全息地图.json` 的本章义务、shared core constraints，以及当前项目的 `type-pack drafting projection`。 |
| `constraint_profile` | 不换故事骨架，只重排密度和脉冲；必须继续遵守规划真源、设定边界、推进下限、上章承诺回应与章末期待约束。 |
| `success_criteria` | 读者能明显感知推进、停顿、加压和章末牵引，同时章节仍能回答“发生了什么/为什么现在这样”。 |
| `non_goals` | 不重写 chapter board、本章主事件序列、设定系统、世界规则或终修文风。 |
| `complexity_source` | 复杂度来自“节奏变形”很容易伤到因果承接、上章回应、章末牵引和设定物理。 |
| `topology_fit` | `root reread -> chapter promise / constraint projection -> seven-slot rhythm engine -> drag/skip diagnosis -> pacing rewrite -> compliance audit` |
| `step_strategy` | 先锁本章不可破坏的法律与物理，再锁“开头钩子 / 本章承诺 / 冲突轴 / 转向 / 反应决策 / 微兑现 / 尾钩”七段发动机，最后把它们编排成章内脉冲梯子并做有限重排与重写。 |

## Total Input Contract

- 必需输入：
  - 当前 `第N集.md`
  - `写作日志.yaml`
  - `2-Planning/全息地图.json`
  - `../../_shared/core-constraints.md`
- 硬规则：
  - 必须先保住 Step 1 的事件逻辑，再谈节奏优化。
  - 节奏优化不得靠删掉必要信息制造“快感”。
  - 若上章有明确承诺，本 step 不得把回应段删成失忆式略过。
  - 不得用新能力、新道具、新规则制造假高潮。
  - 整章至少保留一项清晰推进；若 rewrite 后仍“整章无收获”，视为失败。

### Soft / Style Projection

- 优先把长铺垫切成“信息 + 动作/反应 + 局面变化”。
- 开头若迟迟不进冲突、风险或强情绪，应优先前移有效脉冲。
- 第一屏或前两段必须尽快交代“现在为什么值得读下去”，避免把 hook 全拖到中后段。
- 本章必须尽早让读者知道“这章到底要兑现什么问题/欲望/压力”，避免只有氛围没有交易。
- 不得连续堆两个以上高压钩子却没有任何局部兑现，否则会把章节读感写成纯拉扯。
- 章末若平收，应优先补未闭合期待、代价余波或下一步压力，而不是只加一个问号句。
- 尾钩不必总是爆炸式 cliffhanger；`reveal / decision / threat / pressure transfer / quiet unease` 都可以，但必须自然长在本章正文里。

## Episode Rhythm Engine Contract

| slot | core_question | required_move | common_failure |
| --- | --- | --- | --- |
| `entry_hook` | 为什么这章一开始就值得读？ | 在第一屏内给出变化、压力、异常、强情绪或局面失衡 | 先讲背景，再等读者自己找兴趣点 |
| `chapter_promise` | 这章会交付什么？ | 尽早明确本章要回答的核心问题、欲望、任务或风险 | 全章只是在走流程，没有明确交易 |
| `conflict_axis` | 这一章真正的阻力是什么？ | 明确“谁想做什么，被什么阻碍，失败代价是什么” | 只有事件推进，没有对抗与代价 |
| `turn_or_reversal` | 局势在何处改写？ | 至少出现一次价值变化、局势改向、误判翻面或压力升级 | 全章一直同方向推进，没有改向感 |
| `reaction_decision` | 冲突后人物如何消化并作出下一步？ | 保留反应、两难和决策，给后续推进合法因果 | 只剩动作噪音，没有人物吸收与决定 |
| `micro_payoff` | 本章至少兑现什么？ | 至少交付一个局部收获：信息、关系、能力、资源、情绪或局面变化 | 全章只铺不收，像下一章的预告片 |
| `exit_hook` | 为什么读者会点下一章？ | 用 reveal / decision / threat / pressure transfer / quiet unease 留下未闭合期待 | 结尾平收，或生硬硬切 cliffhanger |

硬规则：

- `entry_hook` 和 `exit_hook` 不能互相替代；开头负责拉入，尾部负责续推。
- `chapter_promise` 必须在正文前段被感知到，而不是作者心里知道、读者读完全章才知道。
- `conflict_axis` 必须可回答“此刻不顺着人物意愿发展的力量是什么”，否则不算真正起章。
- `turn_or_reversal` 不要求每章都大反转，但要求每章至少一次局势改写；关键章必须有强转向或 `false victory / false defeat`。
- `reaction_decision` 不得被纯动作推进吞没；若没有消化与决定，下一步目标通常会发虚。
- `micro_payoff` 不要求每章大高潮，但要求每章至少有一次“局面真的变了”。
- 七段发动机锁定后，仍必须把它们编排成有起伏的 `pulse_ladder`，而不是七个标签顺排。

## Output Contract

- `manuscript_patch`
  - 节奏重排后的正文
- `process_log_entry`
  - `step_id: 2`
  - `focus_dimension: pacing_matrix`
  - 必须记录本轮如何投影 `core-constraints`，尤其是：
    - 七段发动机如何被安放并编排成 `pulse_ladder`
    - 保留了哪些本章规划义务
    - 修复了哪些空转段/跳切段
    - 章末期待如何被保留或增强
    - 若启用 `type-pack`，本轮采用了哪些 `required_hooks / hard_fail_signals`
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
    A["回读 Step 1 正文 + 写作日志"] --> B["投影规划义务与 core constraints"]
    B --> C["锁七段发动机前五段"]
    C --> D["锁 micro payoff + exit hook"]
    D --> E["建立 pulse ladder"]
    E --> F["识别拖沓/跳切/弱钩子"]
    F --> G["做有限节奏重排 + micro payoff / exit hook"]
    G --> H["跑法律/物理/推进审计"]
```

```mermaid
flowchart LR
    A["发现问题段"] --> B{{"问题类型"}}
    B -->|"长铺垫空转"| C["压缩解释\n前移变化"]
    B -->|"跳切因果断"| D["补回动作-反应-结果链"]
    B -->|"章末平收"| E["补未闭合期待/代价余波"]
    B -->|"靠新设定硬提速"| F["撤销新增设定\n回到既有法律/物理"]
    C --> G["进入合规审计"]
    D --> G
    E --> G
    F --> G
```

```mermaid
stateDiagram-v2
    [*] --> RereadCurrent
    RereadCurrent --> ConstraintProjected
    ConstraintProjected --> PulseMapped
    PulseMapped --> Diagnosed
    Diagnosed --> Rewriting
    Rewriting --> ComplianceAudited
    ComplianceAudited --> Passed
    ComplianceAudited --> ReworkCurrentStep
```

## Thinking-Action Network

| node_id | field_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-ROOT-REREAD` | `FIELD-DR2-01` | 回读当前正文与日志 | 读取 Step 1 结果、上一步 hook 摘要、reader signal | `input_note` | -> `N2` | 正文最新 |
| `N2-PROMISE-CONSTRAINT-PROJECTION` | `FIELD-DR2-02` | 锁当前 step 不可破坏的法律、物理与本章交易 | 对齐 chapter board、上章承诺、设定边界、Hard/Soft/Style 约束，并锁 `chapter_promise` | `constraint_note` | -> `N3` | 约束和本章承诺清楚 |
| `N3-HOOK-AND-PROMISE-LOCK` | `FIELD-DR2-03` | 锁开头钩子与前段吸力 | 判断第一屏是否存在 `entry_hook`，并确认前段能感知 `chapter_promise` | `hook_note` | -> `N4` | 开头能拉人，且本章交易可见 |
| `N4-CONFLICT-REVERSAL-LOCK` | `FIELD-DR2-04` | 锁冲突轴与局势改写点 | 明确 `goal / obstruction / stakes`，并标出 `turn_or_reversal` 与关键代价 | `conflict_note` | -> `N5` | 本章不是平推，且中段有改向 |
| `N5-REACTION-DECISION-LOCK` | `FIELD-DR2-05` | 锁反应与下一步决定 | 标出冲突后人物的反应、两难和决策，确保后续推进有因果 | `reaction_note` | -> `N6` | 人物吸收成立，不是纯噪音推进 |
| `N6-PULSE-LADDER` | `FIELD-DR2-06` | 用七段发动机建立章内节奏梯子 | 标出推进点、冲突点、转向点、决策点、微兑现点与章末期待区 | `pulse_note` | -> `N7` | 七段已被编排成有起伏的读感 |
| `N7-DRAG-DIAGNOSIS` | `FIELD-DR2-07` | 识别节奏问题 | 找出平推、跳切、稀薄段、弱钩子、解释堆积段与“只拉不收”段 | `diagnosis_note` | -> `N8` | 问题具体 |
| `N8-PACING-REWRITE` | `FIELD-DR2-08` | 重写节奏 | 调整段落长度、顺序、压缩/留白、补反应桥、安装 `micro_payoff / exit_hook` | `rewrite_note` | -> `N9` | 节奏可感且有交易 |
| `N9-COMPLIANCE-AUDIT` | `FIELD-DR2-09` | 做最终合规审计 | 检查规划义务、设定物理、推进下限、本章兑现、章末期待、占位禁令 | `compliance_note` | done | 快而不空，且未越界 |

## Lite Field Contract

| field_id | output_slot | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `FIELD-DR2-01` | 当前正文与日志 | 已回读 Step 1 正文、日志与最近 hook 摘要 | `FAIL-DR2-01` | `N1` |
| `FIELD-DR2-02` | 约束投影 | 已锁定规划义务、设定边界、Hard/Soft/Style 门禁与 `chapter_promise` | `FAIL-DR2-02` | `N2` |
| `FIELD-DR2-03` | hook/promise lock | 开头可感知 `entry_hook`，且前段已显出本章交易 | `FAIL-DR2-03` | `N3` |
| `FIELD-DR2-04` | conflict/reversal lock | 已明确冲突轴、阻碍、代价与至少一次局势改写 | `FAIL-DR2-04` | `N4` |
| `FIELD-DR2-05` | reaction/decision lock | 冲突后有可感知反应、两难与决定 | `FAIL-DR2-05` | `N5` |
| `FIELD-DR2-06` | pulse ladder | 已有章内节奏梯子，且标出微兑现区与章末期待区 | `FAIL-DR2-06` | `N6` |
| `FIELD-DR2-07` | 节奏问题表 | 拖沓/跳切/平推/弱钩子/只拉不收问题已定位 | `FAIL-DR2-07` | `N7` |
| `FIELD-DR2-08` | 节奏版正文 | 推进与收放明显改善，且已安放 `micro_payoff / exit_hook`，未靠删空因果或硬造新设定提速 | `FAIL-DR2-08` | `N8` |
| `FIELD-DR2-09` | 合规审计摘要 | 章节仍可读、有推进、回应承诺、冲突成立、完成至少一处局部兑现、无占位、章末保有期待 | `FAIL-DR2-09` | `N9` |

## Completion Contract

- 当前正文已具备可感知的章内脉冲。
- 当前正文已具备 `entry_hook -> chapter_promise -> conflict_axis -> turn_or_reversal -> reaction_decision -> micro_payoff -> exit_hook` 的七段发动机，并已被编排成有效 `pulse_ladder`。
- 当前正文仍满足 `core-constraints` 的三大定律与章节 Hard 约束。
- `process_log_entry` 已说明本次节奏调整聚焦了哪些问题，以及如何守住规划义务、设定边界与章末期待。

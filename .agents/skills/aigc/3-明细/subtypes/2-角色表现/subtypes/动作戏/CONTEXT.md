# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `动作戏` 的经验层知识库，不是执行日志。
- 调用 `动作戏/SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > 父级 `SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 动作很热闹但没有因果链 | 动作结构层 | 回补 `触发 -> 动作 -> 结果` | 在字段主表固定因果受力链 | 每个爆点都能回查结果 |
| 动作只有抽象强度词，没有具体节拍 | 表达层 | 把“狠/快/乱”改写为节拍链 | 在步骤表先拆节拍再修辞 | 不再只剩形容词 |
| 环境与道具没有参与动作 | 空间层 | 为动作补障碍、借力点、碰撞物 | 在字段主表固定环境参与 | 动作发生地点可拍可分镜 |
| 爆点后无余波，动作像断片 | 节奏回收层 | 补喘息、受伤、停顿或局面变化 | 在 `FIELD-ACT-REC-05` 固化回收门禁 | 爆点后不悬空 |
| 为了动作感直接写成镜头脚本 | 阶段边界层 | 删除镜头化指令，只保留行为真源 | 复杂镜头问题交接给后续 sibling | 不再越权到运镜/分镜 |
| 兵器近战写成同一种“你来我往” | 兵器类型层 | 先判兵器子类型，再选交换链和落点 | 在类型策略中补 `WT-01` 到 `WT-08` 速查 | 刀、棍、枪、擒拿不再同壳 |
| 动作很炫，但没有完整交换回合 | 节拍结构层 | 回补 `逼近 -> 接触 -> 改线 -> 脱离 -> 结果` | 在字段主表固定完整回合门禁 | 不再只有零散爆点 |
| 超物理动作只剩飞来飞去 | 合法链层 | 补 `起点 -> 触发 -> 迁移 -> 落点 -> 余势` | 在类型策略固定超物理合法链 | 强化动作仍然可回放 |

## Repair Playbook

1. 先看动作目标与结果是否清楚。
2. 再拆节拍链，不要先堆强度词。
3. 再补因果受力与环境参与。
4. 最后看余波与后续留口。

## Reusable Heuristics

- 一条动作句至少要让读者看到“谁动了、动到了哪、局面变了什么”。
- 环境不是背景板，最好把门、桌、墙、栏杆、坡道、台阶变成第三个对手。
- 动作越猛，回收越重要；没有余波，镜头和情绪都接不住。
- 如果动作只剩“很快很猛”，说明还没拆到可拍节拍。
- 动作戏先判“这一下为了什么”，再判“这一下怎么打”；没有目标卡，再华丽也会空。
- 真正让动作变清楚的不是招式名，而是切入线、接触点和失衡方向。
- 兵器戏要先分清试探性碰击和真正杀伤接触，前者是测线，后者才是破口。
- 一个完整且清楚的交换回合，通常比五个模糊概括句更有冲击力。
- 动作戏和角色戏不是两条线。一个人怎么发力、被打后先护哪里，本身就在暴露人物。

## Case Log

### Case-20260409-AIGC-SCRIPT-ACTION-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `动作戏` 建立了适配当前 `3-明细` 终稿模式的 leaf 合同与经验层。
- root_cause_or_design_decision: 用户要求参照 `AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/8-动作戏` 完善当前路径，但当前仓更需要的是“终稿共写模式”下的动作增强合同，而不是复制旧仓的 writer 阶段载体。
- final_fix_or_heuristic: 保留旧仓中“节拍链、因果受力、环境参与、余波回收”的高价值能力，同时把输出载体重写为共享终稿。
- prevention_or_replication_checklist:
  - [x] 已固定共享终稿落点
  - [x] 已建立动作节拍链字段
  - [x] 已建立因果受力与余波门禁
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/动作戏/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/动作戏/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/8-动作戏/SKILL.md`
- user_feedback_or_constraint: 用户明确要求参照 `8-动作戏`，并将其并入当前 `3-明细` 的层层加权扩写链。

### Case-20260409-AIGC-SCRIPT-ACTION-PHYSICS-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `动作戏` 从“节拍链 + 因果受力”的基础合同升级为带兵器子类型、港式武指可回放标准、反空泛门禁与完整交换回合要求的动作物理合同。
- root_cause_or_design_decision: 旧版 leaf 合同已经能避免抽象动词堆砌，但仍缺少兵器差异、失衡补偿、再逼近链和超物理动作的合法链，容易把“更细”写成“更散”。
- final_fix_or_heuristic: 在 `references/type-strategies.md` 下沉物理锚点合同与 `WT-01` 到 `WT-08` 速查，在 `references/chain-of-thought.md` 把完整交换回合、兵器证据与余势回收接进字段系统，再在 `SKILL.md` 与 `CONTEXT.md` 对齐边界和经验层。
- prevention_or_replication_checklist:
  - [x] 已补 5-of-7 物理锚点门禁
  - [x] 已补兵器子类型速查
  - [x] 已补反空泛动作门禁
  - [x] 已补完整交换回合要求
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/动作戏/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/动作戏/references/type-strategies.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/动作戏/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/动作戏/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求吸收“动作戏（武打编排与物理受力细化）”部分，并禁止粗暴整段贴入。

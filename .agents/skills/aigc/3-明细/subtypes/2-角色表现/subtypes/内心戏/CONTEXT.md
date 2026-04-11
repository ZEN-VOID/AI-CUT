# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `内心戏` 的经验层知识库，不是执行日志。
- 调用 `内心戏/SKILL.md` 时，应自动预加载本文件。
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
| 只有抽象心理词，没有可见承载 | 表达层 | 改写为静默/物象/感官/记忆等可见载体 | 在字段主表固定主观承载方式 | 主观层不再空泛 |
| 内心戏无触发点，像凭空抒情 | 触发层 | 先补触发卡再落主观段 | 在 `FIELD-INN-TRIGGER-02` 固化触发门禁 | 每段内层增强都能回查触发 |
| 一段里堆太多主观手法 | 聚焦层 | 收敛为唯一主承载方式，必要时只留 `1 主 + 1 辅` | 在 `FIELD-INN-BLEND-04` 固化第二价值门禁 | 不再五花八门一起上 |
| 主观段写完回不来现实层 | 结构层 | 补动作/关系/决定回钩 | 在 `FIELD-INN-RECOVERY-06` 固化回收门禁 | 主观层能回到当下 |
| 为了“高级”直接写成超现实设定 | 阶段边界层 | 删除越界设定，只保留角色主观层 | 在核心约束中固定不新增世界规则 | 不再把内心戏写成世界观追加 |
| 正文出现 `回忆画面：` 等标签前缀 | 表达层 | 去标签，改成现实触发物带出的自然句 | 在 `FIELD-INN-LANDING-05` 固化自然融写门禁 | 标签命中数为 0 |
| 主类型是内心OS，但句子只有心理判断没有镜头可见锚点 | 机制层 | 按 `IOS-Visual` 改写为动作 + 物象 + 空间/现实回钩 | 在 `FIELD-INN-TYPE-03` 固化 `os_variant` 判定 | OS 段至少含一个可见锚点 |
| 音乐或音效明显存在，却没有被吸收到联想层 | 触发层 | 补建 `audio_cue` 证据并重判主辅类型 | 在 `FIELD-INN-TRIGGER-02` 固化音频 cue 检查 | 声音触发段可回查 cue |
| 辅类型与主类型重复、冲突或没有第二价值 | 组合层 | 删掉辅类型或更换为真正补值的辅类型 | 在 `FIELD-INN-BLEND-04` 固化组合矩阵与禁止组合 | 主辅类型 distinct value 明确 |
| 非现实段跨句、跨段漂移，吞掉当前场景 | 连续性层 | 重排为 `same-sentence` 或 `adjacent-sentence`，并补回收钩子 | 在 `FIELD-INN-GUARD-07` 固化密度与连续性门禁 | 主观段在同段闭合 |
| 改动触碰对白/独白/旁白原文 | 契约层 | 回滚到上游逐字文本，再只补旁侧可视化层 | 在 `FIELD-INN-GUARD-07` 固化逐字不可变检查 | 三类文本一致率 100% |

## Repair Playbook

1. 先判这段主观层承担的是“情绪临界、认知翻转还是主题显影”。
2. 再补 `情绪轴 + 剧情节点 + 题材风格 + 音频 cue` 的触发证据。
3. 先选主类型；只有单主类型不足时，才判辅类型是否提供第二价值。
4. 若主类型是 `内心OS`，强制进入 `IOS-Visual`，把压力写成可见动作、物象或空间变化。
5. 再把主观层落为自然句，并用现实动作/声响/对白语境回钩。
6. 最后复核密度、连续性、逐字不可变与 sibling handoff。

## Reusable Heuristics

- 情绪越重，主观段往往越该短，而不是越长。
- 一个物件、一个声响、一道光，比三句抽象心理词更能托住内心戏。
- 内心戏不是离场独白，它必须和当前场面、当前人、当前决定绑在一起。
- 如果不确定该不该写非现实化，先试静默、物象或感官错位，通常更稳。
- 先判主观任务，再判类型名；没有 `trigger / landing / recovery`，再华丽的类型名也只是空标签。
- `内心OS` 最有价值的瞬间通常发生在“做/不做、说/不说”之前的半秒，优先盯临界动作而不是心理解释。
- 辅类型只在补足第二叙事价值时成立；如果只是换个名字重复一遍，宁可删掉。
- `音乐联想` 要先让读者听见，再让记忆或情绪渗出来；反过来容易写成作者说明。
- `Q版` 只能做喜剧叠加层，不应替代主类型承担戏核。
- 梦境、闪回、闪进都必须就地回收；没有醒回锚点或现实回钩，就会误伤主叙事。

## Case Log

### Case-20260409-AIGC-SCRIPT-INNER-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `内心戏` 建立了适配当前 `3-明细` 终稿模式的 leaf 合同与经验层。
- root_cause_or_design_decision: 用户要求参照 `AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/5-非现实画面`，但当前路径更需要的是“内心戏”而不是广义非现实画面本体，因此要把其高价值能力压缩为主观触发、承载方式与回收钩子的合同。
- final_fix_or_heuristic: 保留旧仓中“触发先行、单主类型、自然融写、回收钩子”的核心经验，并改写成当前 `3-明细` 的内心戏 leaf。
- prevention_or_replication_checklist:
  - [x] 已建立触发卡
  - [x] 已建立单主承载方式规则
  - [x] 已建立回收钩子门禁
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/内心戏/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/内心戏/CONTEXT.md`
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/5-非现实画面/SKILL.md`
- user_feedback_or_constraint: 用户明确要求 `内心戏` 参照 `5-非现实画面`，但当前命名与落地语境应以 `3-明细/2-角色表现` 为准。

### Case-20260409-AIGC-SCRIPT-INNER-NRVM-IOS

- milestone_type: source_contract_change
- outcome: 将非现实裁决、内心OS画面化与双类型落盘规则融合进 `内心戏` 的现有 anatomy，而不是平移复制旧仓规范。
- root_cause_or_design_decision: 现有 `内心戏` 已有“触发-承载-回收”的基础闭环，但缺少 `NRVM-3D`、`IOS-Visual`、辅类型第二价值门禁、结构化追溯字段与密度/连续性硬门槛，导致后续执行容易回到抽象心理句或技法堆叠。
- final_fix_or_heuristic: 把类型裁决与组合矩阵沉到 `references/type-strategies.md`，把字段与返工入口沉到 `references/chain-of-thought.md`，把结构化追溯键沉到 `.agents/skills/aigc/3-明细/references/output-template.md`，并在主合同与经验层只保留必要的硬约束与可复用 heuristics。
- prevention_or_replication_checklist:
  - [x] 主合同已补自然融写、不可变层、密度与连续性硬门槛
  - [x] 类型策略已补 `NRVM-3D`、`IOS-Visual`、Dual-Type 落盘机制
  - [x] 字段系统已补主辅类型、落盘模式、回收钩子与门禁校验
  - [x] CONTEXT 已补失败类型与复用经验
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/内心戏/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/内心戏/references/type-strategies.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/内心戏/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/内心戏/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“只补缺、不堆砌、要按位置与关系消化吸收”，因此本次采用主合同摘要 + 模块细则 + 经验层沉淀的分配式写法。

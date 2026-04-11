# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/3-明细/subtypes/2-角色表现` 的经验层知识库，不是执行日志。
- 调用父级 `SKILL.md` 时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `.agents/skills/aigc/3-明细/SKILL.md` > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 三个 leaf 已有内容，但父级没有进入判定 | 父子路由层 | 先补父级路由矩阵 | 父级显式写何时进入哪个 leaf | 父级可输出唯一主入口 |
| `动作戏 / 对手戏 / 内心戏` 同集并行改写同一文件 | 写集冲突层 | 收紧为 dominant-first 受控串行 | 在父级显式覆盖 `unordered` 默认并发 | 同集多命中不再并行写 |
| 角色表现只读正文，不读分组与组间 handoff | 输入契约层 | 补齐分组容器与 `2-组间` handoff | 在父级输入链写成强制步骤 | 角色表现增强可回查编导来源 |
| 父级把角色表现理解成“堆细节” | 方法合同层 | 改写为“先判戏核，再选 leaf” | 在父级固化表现压力中心判断 | 每轮执行前都有 dominant subtype |
| 只修 leaf，不同步 `3-明细` 与 `aigc` 上层状态 | 元路由层 | 同步回写上级状态与阶段说明 | 把父子闭环与上层同步视为一体任务 | 上层状态与当前父子合同一致 |
| 顾问团已启用，但 `2-角色表现` 没继承 `3-明细` 的阶段顾问运行时 | 继承层 | 明确本父技能继承上层 `3-明细` 的 `Council Runtime Contract` | 子技能不再重复发明第二套顾问团规则 | 进入 `2-角色表现` 时会先遵守项目根 `team.yaml` 判定 |
| 情绪只剩抽象判断，没有落到可见动作 | 表演外化层 | 把情绪绑定到面部/目光/姿态/手部/呼吸/交互中的至少一项 | 在父级固化 MPEA 共享锚点池 | 关键节拍不再只剩“很痛苦/很紧张” |
| 每个角色都演成同一种紧张 | 角色口径层 | 先锁角色口径与节拍任务，再选表演手法 | 在父级类型策略里补角色原型动作特质 | 不同人物的外化方式可区分 |
| 节拍补得很多，但机械感更强 | 微观策略层 | 收回为 `1主 + 1辅`，保留节拍异质性 | 在经验层固定“锚点先于动作、互动必须成对” | 相邻节拍不再同壳复写 |
| 执行报告缺少证据与 guard，回查困难 | 交付闭环层 | 统一补 `trigger_evidence / type_decision / guard_summary` | 在输出模板中把三件套写成最低要求 | 报告可回查本轮为何这样补写 |

## Repair Playbook

1. 先检查父级 `2-角色表现/SKILL.md` 是否具备唯一主入口裁决。
2. 再检查同一集是否触发了多 leaf 写集冲突。
3. 若冲突存在，先锁 dominant subtype，再决定是否追加补充 leaf。
4. 最后检查是否已经把执行留口写入父级报告与 `CHANGELOG.md`。

## Reusable Heuristics

- 对角色表现来说，真正的父级价值不是“把三个 leaf 列出来”，而是先判这场戏最缺哪一种表现压力。
- 目录名无序不等于执行就能并行；只要共享同一终稿写集，就必须把并发改成受控串行。
- `动作戏 / 对手戏 / 内心戏` 的最佳切分标准不是题材名，而是“身体、语言、主观”三种表现压力中心。
- 只要 leaf 的内容会改变终稿节奏或人物关系，就必须回查 `2-组间` handoff，不能只凭正文局部判断。
- 对 `2-角色表现` 来说，顾问团机制应该继承自 `3-明细` 根级，不应在父子链里再复制一套。
- 对共享同一终稿写集的父级路由层来说，思维链必须先服务 `dominant subtype + 写集安全 + sibling 交接`，而不是追求把每个 leaf 的潜在机会都写进同一轮可见合同。
- 表演增强不是加形容词，而是给情绪找一个观众能看到的出口。
- 锚点先于动作：先判节拍任务、人物目标和外化准心，再决定眼神、手部还是姿态。
- 单节拍保留 `1主 + 1辅` 最稳；策略一多，人物就容易只剩同一种壳。
- 安静也可以是表演。一个呼吸停顿、一次视线回收，常常比塞满动作更有压强。
- 互动必须成对。A 的逼近、退让或挑衅，最好都能在 B 或环境上收到反作用。
- `writer.performance` 应作为当前 `2-角色表现` 层的默认消费入口；legacy `project_preset.json` 仅用于兼容。
- `trigger_evidence / type_decision / guard_summary` 写不清时，通常说明这轮补写还停留在感觉驱动。
- 机械感往往不是写得少，而是每个节拍都用了同一种增强手法。

## Case Log

### Case-20260409-AIGC-SCRIPT-CHARACTER-PARENT-CONTRACT

- milestone_type: source_contract_change
- outcome: 为 `.agents/skills/aigc/3-明细/subtypes/2-角色表现` 建立了父级合同与经验层，并把 `动作戏 / 对手戏 / 内心戏` 接回统一父级路由。
- root_cause_or_design_decision: 用户要求先补三个角色表现子技能，再补根级；直接技术阻塞是父级 `2-角色表现` 为空，导致三个 leaf 即使建立后仍没有统一入口与写集冲突规则。
- final_fix_or_heuristic: 先补父级 `SKILL.md + CONTEXT.md`，再把三个 leaf 都挂到“dominant subtype -> supplemental subtype”的父级冲突解决规则上。
- prevention_or_replication_checklist:
  - [x] 父级 `SKILL.md` 已补齐
  - [x] 父级 `CONTEXT.md` 已建立
  - [x] 三个 leaf 都已纳入同一父级矩阵
  - [x] 同集多命中不再默认并行写集
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/CONTEXT.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/动作戏/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/对手戏/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/subtypes/内心戏/SKILL.md`
- user_feedback_or_constraint: 用户明确要求三个 leaf 先补齐，再回补 `2-角色表现` 根级，并将 `对手戏` 主要理解为对话戏。

### Case-20260409-AIGC-SCRIPT-CHARACTER-PARENT-COT-UPGRADE

- milestone_type: source_contract_change
- outcome: 将 `.agents/skills/aigc/3-明细/subtypes/2-角色表现/references/chain-of-thought.md` 从“字段台账 + 简版裁决表”升级到最新 `think-think` 规范。
- root_cause_or_design_decision: 旧版 contract 虽有 `Think-Think Design Snapshot` 标题，但仍缺少 `模式与对象`、对象专属 `启发式工作链`、`可见 / 隐藏分层`、`工具后反思` 与 `Gate Summary`，导致父级路由层的可见判断链不完整，也不利于 reasoning 模型采用高层裁决方式。
- final_fix_or_heuristic: 保留 `FIELD-CPR-*` 六字段接口不变，在 reference 顶部补入模式声明、父级专属启发式工作链、三轴三重裁决、可见/隐藏分层、工具后反思、`Gate Summary Contract` 与 `Validation Matrix`，把判断核心压到 `dominant subtype + shared draft safety + sibling handoff`。
- prevention_or_replication_checklist:
  - [x] 已补 `模式与对象`
  - [x] 已补对象专属 `启发式工作链`
  - [x] 已补 `工具后反思` 与 `Gate Summary`
  - [x] 已补 `Validation Matrix`
  - [x] 已保持 `FIELD-CPR-*` 接口稳定
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/references/chain-of-thought.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求“按照最新的思维链设计规范”优化 `.agents/skills/aigc/3-明细/subtypes/2-角色表现/references/chain-of-thought.md`。

### Case-20260409-AIGC-SCRIPT-CHARACTER-PERFORMANCE-MPEA-INTEGRATION

- milestone_type: source_contract_change
- outcome: 将 `2-角色表现` 的共享风格基线、不可变层、MPEA、`writer.performance` 默认入口与执行备注三件套补进父级真源，并把跨 leaf 的微表演语料压到 `references/type-strategies.md`。
- root_cause_or_design_decision: 现有父级合同更擅长“判路”，但缺少“怎么写得像一场可拍的表演”的共享门禁；同时 `writer.performance`、执行备注与角色原型没有在输入源、输出模板和类型策略之间成套对齐。
- final_fix_or_heuristic: 父级 `SKILL.md` 只补共享硬门禁，`references/execution-flow.md` 对齐输入优先级，`.agents/skills/aigc/3-明细/references/output-template.md` 固化写感与报告三件套，`references/type-strategies.md` 承接微表演锚点池、角色原型与权力动态。
- prevention_or_replication_checklist:
  - [x] 已补共享不可变层
  - [x] 已补 MPEA 共享锚点池
  - [x] 已补 `writer.performance` 默认入口
  - [x] 已补执行备注三件套
- evidence_paths:
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/SKILL.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/references/execution-flow.md`
  - `.agents/skills/aigc/3-明细/references/output-template.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/references/type-strategies.md`
  - `.agents/skills/aigc/3-明细/subtypes/2-角色表现/CONTEXT.md`
- user_feedback_or_constraint: 用户要求“按指定位置和关系指定”补全，不允许把精华内容粗暴整块插入单一文件。

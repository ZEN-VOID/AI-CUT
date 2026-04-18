# Item Card Module Spec

## Module Identity

- module_type: `governed-reference`
- canonical_reference_path: `references/item-card-module/module-spec.md`
- canonical_context_path: `references/item-card-module/CONTEXT.md`
- canonical_module_route: `story-cards > references/item-card-module/module-spec.md`
- shared_template_source: `/Users/vincentlee/.codex/skills/meta/references-update/templates/reference-module-spec-template.md`

## 1. 适用场景

- 上层 SKILL 语境：本模块服务 [`1-Cards/SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/SKILL.md) 的物品对象路由，是 `角色 / 场景 / 物品` 三兄弟模块中的载体与剧情杠杆分支。
- 当前模块负责对象/范围：武器、线索物、重要叙事物、遗物、专属物、使用规则、代价、归属链，以及物品桶 coverage 返工。
- 模块归属类型：多子类型之一；当父技能判定当前对象为 `item`，或 mixed 请求在角色/场景约束明确后需要补载体与杠杆时进入本模块。
- 进入触发信号：用户提武器、线索、道具、遗物、专属物、使用规则、代价、归属；或 `cards-check` 指向“重要物空心”“专属物模板化”“线索物与叙事物混桶”。
- 不负责项：角色成长弧裁决、场景规则裁决、父技能任务模式判定、全局 coverage gate 汇总。
- 与兄弟模块边界：角色模块先提供人物欲望与 `exclusive_item_hooks`，场景模块提供世界规则与空间限制，物品模块负责把这些约束落成可消费的载体与剧情杠杆。

## 2. 预加载上下文

- 上层必读：
  - [`SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/SKILL.md)
  - [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/CONTEXT.md)
- 本层必读：
  - 当前 [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/item-card-module/module-spec.md)
  - 当前 [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/item-card-module/CONTEXT.md)
- 加载顺序：
  1. 根 `SKILL.md`
  2. 根 `CONTEXT.md`
  3. 当前 `module-spec.md`
  4. 当前 `CONTEXT.md`
  5. [`templates/item-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/item-card.json)
  6. `Init/north_star_contract.json`、`Init/初始化简报.json`、角色卡切片、既有 `Cards/4-物品卡/**/*.json`
- 冲突优先级：用户显式请求 > `AGENTS.md` / 父 `SKILL.md` > 当前 `module-spec.md` > 当前 `CONTEXT.md`
- 默认不并入的上下文：若角色模块尚未稳定输出 `exclusive_item_hooks`，不得在本模块擅自发明角色专属逻辑；若场景规则未锁定，不得绕过世界规则先写炫酷设定。
- 共享输入切片：
  - `north_star_contract.story_kernel / reader_promise / aesthetic_axes / cards`
  - `cards_seed.item_seed`
  - `unknowns.deferred_to_cards`
  - `templates/worldbuilding/power-systems.md`
  - `templates/worldbuilding/world-rules.md`
  - 角色卡切片

## 3. 思维链

### Think-Think Design Snapshot

- mode: `思维链优化设计`
- task_essence: 把 `道具/武器诉求` 从“设定上的东西”推进为“有剧情杠杆、有归属链、有代价且能体现角色痕迹的正式物品卡决策”。
- baseline_symptom: 旧版文档已经知道物品该看归属与代价，但没有把“先判剧情职能、再封闭归属与限制、最后做专属信号优选”写成可执行的阶段合同。

### 优化模式事实 / 推断分层

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | 当前文档已经有 `剧情杠杆对齐 / 归属与代价闭合 / 专属信号收益比` 三轴，也保留了 `Phase 1-4` 与正式模板落点 | 当前 `module-spec.md`、父 `SKILL.md`、`templates/item-card.json` | 保留既有任务本质、Phase 编排和模板落点 |
| `Inferred Gaps` | 旧版快照缺 `驱动/判废/对比` 字段拆分，也没有 `轴权归属检查 / 近邻替换压测 / 落盘扰动测试`，导致物品模块虽然有三轴，但仍可能滑回“有名字的道具” | 用户反馈 + 当前快照只到三轴/三重 | 重建字段层、验证层与落盘扰动说明 |
| `Protected Constraints` | 不破坏 `FIELD-CD-STR-01 / MAT-03 / CTX-01 / CST-01`、既有 Phase 1-4、物品模板结构、角色接口与世界规则输入责任 | 根 `SKILL.md` 字段主表与当前模板/脚本约束 | 只加固思维链，不改父技能路由与正式 schema 契约 |
| `Proposed Rewrite` | 把物品模块从“有三轴的摘要卡”升级为“有字段锋利度、验证层和落盘扰动证据的思维链合同” | `think-think` 优化模式合同 | 增补向字段展开、分重关键向字段矩阵、方向评估与增强验证 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 漂移风险 | 为什么不是别的轴名 | 直接落点 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `剧情杠杆对齐` | 当前物品到底推动什么变化，是线索、局势转折，还是角色行动的延长体 | 漂移成“设定更酷”或“名词更大” | 因为物品模块首先要回答“这件东西改变什么”，不是先回答“这件东西多有质感” | `适用场景`、`Phase 1`、`quality standard` |
| `成立轴` | `归属与代价闭合` | 持有者、使用规则、限制、代价、世界规则适配是否闭合 | 漂移成第二条“剧情价值高”判断 | 因为这一轴负责判定“有没有成立”，不是再说一次物品的重要性 | `预加载上下文`、`Phase 2`、`Phase 3` |
| `优选轴` | `专属信号收益比` | 多个成立物品里，哪个更像角色本人、剧情撬动力更强且不模板化 | 漂移成“更有质感”“更稀有”的赞美轴 | 因为这里需要的是成立解之间的可比收益尺，而不是材质赞美 | `Phase 3`、`交付`、`验收机制` |

### 向字段展开（驱动 / 判废 / 对比）

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 主裁决层 |
| --- | --- | --- | --- | --- |
| `剧情杠杆对齐` | `narrative_functions / group / owner_type` | `无法解释剧情作用 / 问题本质不属于物品模块 / 只剩设定名词没有变化杠杆` | `当前卷推进力 / 角色延长体强度 / 局势改写幅度` | `粗裁决 / Base Range` |
| `归属与代价闭合` | `ownership_links / usage_rules.activation / limits / costs / exclusive_fit.preferred_owners` | `无归属 / 无启用规则 / 无代价 / 与世界规则冲突 / 专属适配空洞` | `归属链清晰度 / 代价可执行性 / 角色接口吸收度` | `细裁决 / Range Narrowing` |
| `专属信号收益比` | `exclusive_fit.style_match / active_plot_load` | `角色痕迹只停留在外观词 / 与现有物品模板化重合 / 需要靠额外说明才能显得专属` | `首识别成本 / 剧情撬动力 / 模板化风险` | `离散裁决 / Final Selection` |

### 三重

| 裁决层 | 本层关键问题 | 关键向字段 | 唯一主轴 | 本模块产物 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | 这是物品问题吗，属于哪一类物品桶，承担什么剧情职能 | `narrative_functions / group / owner_type` | `剧情杠杆对齐` | 物品模块命中结论、物品桶归属、剧情作用 |
| `细裁决 / Range Narrowing` | 当前候选物品是否具备 `ownership_links / usage_rules / limits / costs / exclusive_fit` | `ownership_links / usage_rules.activation / limits / costs / exclusive_fit.preferred_owners` | `归属与代价闭合` | 正式物品 schema、归属链与代价骨架 |
| `离散裁决 / Final Selection` | 多个成立物品里，哪个更能体现角色痕迹并承担更强剧情杠杆 | `exclusive_fit.style_match / active_plot_load / 模板化风险` | `专属信号收益比` | 专属适配理由、剧情负载、去模板化选择 |

### 方向评估矩阵

| 字段 | 定向性 | 区分性 | 约束性 | 落盘性 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `narrative_functions` | 直接决定物品往哪类剧情杠杆收敛 | 能区分线索物、重要叙事物、角色延长体 | 功能说不清时不应进入正式写回 | 对应 `FIELD-CD-STR-01 -> content.module_route` | PASS |
| `ownership_links` | 决定物品是否进入“归属成立”候选 | 能区分正式物品与无主道具 | 无归属会直接判废 | 对应 `FIELD-CD-MAT-03 -> content.card_groups.*` | PASS |
| `usage_rules` | 决定物品是否有可执行的启用与代价结构 | 能区分能推动剧情的物品与只是摆设的物件 | 缺 `activation / costs` 会直接判废 | 对应 `FIELD-CD-MAT-03` | PASS |
| `exclusive_fit.style_match` | 不改变候选范围，但决定成立解中的最终取舍 | 能区分真正像角色本人和只是换皮的专属物 | 不能单独 veto，只做离散比较 | 对应 `FIELD-CD-CTX-01 -> execution_notes.design_rationale` | PASS |

### 快照落点说明

- 思维链如何作用于执行流程：`Phase 1` 先锁剧情作用与桶位，`Phase 2` 再补归属/代价闭合，`Phase 3` 才做专属信号与模板映射优选。
- 思维链如何作用于交付：正式交付必须同时写出 `ownership_links`、`usage_rules`、`exclusive_item_hooks`、`exclusive_fit` 与 trace 字段，不能只交一个“设定酷物”。
- 思维链如何作用于验收：只要出现“无归属、无代价、无角色痕迹、混桶”任一情况，就直接返工。

### 字段落盘映射

| 裁决层 | 关键向字段 | field_id / 决策槽位 | 具体落点 | 说明 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `narrative_functions / group / owner_type` | `FIELD-CD-STR-01` | `content.module_route` + 路由记录 | 先判清是不是物品问题，否则下游归属与代价字段没有意义 |
| `细裁决 / Range Narrowing` | `ownership_links / usage_rules / costs / exclusive_fit.preferred_owners` | `FIELD-CD-MAT-03` | `content.card_groups.*` / `content.card_schema.item_card` | 物品成立条件必须进入正式 schema，不接受只写设定说明 |
| `离散裁决 / Final Selection` | `exclusive_fit.style_match / active_plot_load / 模板化风险` | `FIELD-CD-CTX-01` | `content.loaded_references` + `execution_notes.design_rationale` | 用于解释“为什么是这件物品，不是更泛化的替代物” |
| `Gate` | `无归属 / 无代价 / 无角色痕迹 / 混桶` | `FIELD-CD-CST-01` | `gate_summary.status` | 这些是 veto，不归 `优选轴` 越权处理 |

### 有效性验证

| 验证项 | 结论 | 证据/说明 | 若失败的返工入口 |
| --- | --- | --- | --- |
| `事实/推断分离` | PASS | 已把既有 Phase/模板合同与本轮推断缺口拆开，避免想象式重写 | 回到本节“优化模式事实 / 推断分层” |
| `遮轴名快检` | PASS | 遮掉轴名后仍可读出 `narrative_functions / ownership_links + usage_rules / style_match + active_plot_load` 三组不同字段 | 回到“向字段展开” |
| `轴权归属检查` | PASS | `exclusive_fit.preferred_owners` 主归 `归属与代价闭合`，`style_match` 才归 `专属信号收益比`，防止一个字段跨轴双主导 | 回到“三重”重写唯一主轴 |
| `近邻替换压测` | PASS | 若把 `剧情杠杆对齐` 替换成 `设定酷感强度`，会立刻失去对物品剧情职能和分桶的裁决力 | 回到“三轴”与“方向评估矩阵” |
| `字段落盘追踪` | PASS | 三层都能追到 `FIELD-CD-STR-01 / MAT-03 / CTX-01 / CST-01` | 回到“字段落盘映射” |
| `落盘扰动测试` | PASS | 移除 `usage_rules.costs` 会直接让重要物空心，并削弱 `FIELD-CD-MAT-03` 的成立性；移除 `style_match` 会让 `FIELD-CD-CTX-01` 无法解释专属优选 | 回到 `Phase 2-3` 与对应 field 落点 |

## 4. 执行流程

### Phase 1 物品路由与剧情作用确认

- 目标：确认当前任务是否应进入物品模块，并锁定物品的剧情作用与桶位。
- 输入：父 `SKILL.md` 路由段、用户诉求、`cards-check` finding、角色卡切片、既有物品索引。
- 动作：
  - 判定是否属于武器、线索、重要叙事物、文物、点缀物问题。
  - 明确物品服务的是“打开认知”“改变局势”还是“成为角色延长体”。
  - Mixed 请求下确认角色模块与场景模块是否已提供必要约束。
- 产出：物品模块命中结论、目标桶、需要读取的角色/场景约束切片。
- 失败信号 / 返工入口：若无法回答“这件东西改变什么、属于谁、为什么现在要改它”，退回父 `SKILL.md` 重新做对象路由。

### Phase 2 归属与代价闭合

- 目标：把物品从“设定存在”推进到“归属、规则、限制、代价成立”。
- 输入：`north_star_contract.cards`、角色卡 `exclusive_item_hooks`、`world-rules.md`、既有物品卡。
- 动作：
  - 先补 `ownership_links / narrative_functions / usage_rules`，再写外观与质感。
  - 显式写出 `limits / costs / activation`，避免重要物空心。
  - 校验 `exclusive_fit` 是否真正吸收角色欲望、行动方式与世界规则限制。
- 产出：可落盘的物品规则骨架、归属链、代价结构、专属适配。
- 失败信号 / 返工入口：若重要物没有归属与代价、专属物看不出角色痕迹、线索物与叙事物混桶，回本阶段重做。

### Phase 3 专属信号优选与模板映射

- 目标：在成立物品里选择更像角色本人、剧情撬动力更强的表达，并映射到正式模板。
- 输入：Phase 2 通过的物品候选、[`item-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/item-card.json)、角色卡与既有物品分布。
- 动作：
  - 比较 `style_match / active_plot_load / 模板化风险`。
  - 记录为何选择当前物品表达而不是更泛化的通用道具。
  - 写入 `content.module_route / loaded_references / writeback_plan` 等 trace 槽位。
- 产出：正式物品卡 payload、专属适配理由、trace 字段。
- 失败信号 / 返工入口：若物品仍像通用设定名词，或与既有物品剧情作用重叠严重，回到 Phase 1-2 重做剧情职能与代价闭合。

### Phase 4 写回与 gate 回接

- 目标：把物品模块结果回接到正式写卡链路与 coverage gate。
- 输入：Phase 3 payload、`cards-write` / `cards-check` 约束、父技能回写边界。
- 动作：
  - 将正式产物落到 `Cards/4-物品卡/**/*.json`。
  - Mixed 场景下显式记录本物品消费了哪些角色/场景约束。
  - 回跑物品桶 coverage 检查，确认物品卡真正可消费。
- 产出：正式物品卡、可追溯 trace、物品模块 gate 结论。
- 失败信号 / 返工入口：若写回后仍出现“空心重要物”“模板化专属物”“混桶”，回到对应阶段修复。

## 5. 交付

- 类型：`内容输出型`
- 模式：以当前 `module-spec.md` 约束物品判断逻辑，以当前 `CONTEXT.md` 提供局部返工启发，以 `templates/item-card.json` 作为正式 schema 骨架。
- 正式落点：
  - `Cards/4-物品卡/**/*.json`
  - coverage trace 中的 `content.module_route / loaded_references / writeback_plan`
- 上层消费方式：父 `SKILL.md` 在物品请求、mixed 串行收尾、物品桶 coverage 返工时进入本模块；根技能把本模块产出的归属链与代价结构并入最终 gate。
- 输出模板/字段骨架：
  - `core / current_state / history`
  - `ownership_links`
  - `exclusive_item_hooks`
  - `usage_rules`
  - `exclusive_fit`

## 6. 验收机制

- quality standard：
  - 每张正式物品卡都能回答“为什么这件东西非它不可、属于谁、怎样启用、要付什么代价、为何像这个角色本人”。
  - 专属物必须吸收角色卡与世界规则的共同约束，而不是只改外观词。
  - 线索物与重要叙事物按剧情作用分桶，不能再混成“大事物”一桶。
- acceptance checklist：
  - [ ] 父技能能明确说明何时进入物品模块
  - [ ] 已读取根 `SKILL.md`、根 `CONTEXT.md`、当前 `module-spec.md`、当前 `CONTEXT.md`
  - [ ] 物品桶归属明确，且无兄弟模块职责串位
  - [ ] `ownership_links + usage_rules + exclusive_fit + exclusive_item_hooks` 均已成立
  - [ ] 正式 payload 已映射到 `templates/item-card.json`
  - [ ] 写回后 coverage gate 无物品模块 blocking finding
- fail signal：
  - 重要物没有持有者、功能和代价
  - 专属物看不出角色痕迹
  - 线索物与重要叙事物混桶
  - 物品绕开世界规则或角色接口自说自话
- rework entry：
  - 路由错误 -> 回父 `SKILL.md` Section 9
  - 桶位与剧情作用问题 -> 回 Phase 1
  - 归属/代价/规则问题 -> 回 Phase 2
  - 专属信号与 trace 问题 -> 回 Phase 3
  - coverage gate 问题 -> 回 Phase 4 并联动根 `CONTEXT.md`

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是，物品相关请求与 mixed 串行收尾都显式进入本模块。
- 若为多模块场景，是否已有统一路由段落：是，父技能已有条件加载矩阵；本轮会补强默认顺序、模块关系与 `module CONTEXT` 的读取顺序。
- 父 `SKILL.md` 中的模块关系：角色/场景/物品按对象类型互斥；mixed 与全量建卡按 `角色 -> 场景 -> 物品` 串行；coverage repair 仅按需加载命中模块。

# Scene Card Module Spec

## Module Identity

- module_type: `governed-reference`
- canonical_reference_path: `references/scene-card-module/module-spec.md`
- canonical_context_path: `references/scene-card-module/CONTEXT.md`
- canonical_module_route: `story-cards > references/scene-card-module/module-spec.md`
- shared_template_source: `/Users/vincentlee/.codex/skills/meta/references-update/templates/reference-module-spec-template.md`

## 1. 适用场景

- 上层 SKILL 语境：本模块服务 [`1-Cards/SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/SKILL.md) 的场景对象路由，是 `角色 / 场景 / 物品` 三兄弟模块中的空间与规则分支。
- 当前模块负责对象/范围：地点、空间、环境、世界规则接口、氛围、危险、出入条件、复用策略，以及场景桶 coverage 返工。
- 模块归属类型：多子类型之一；当父技能判定当前对象为 `scene`，或 mixed 请求在角色模块之后需要补空间承载时进入本模块。
- 进入触发信号：用户提地点、环境、空间规则、氛围、危险、常驻据点、反复出场场景；或 `cards-check` 指向“像布景板”“超现实失控”“复用策略缺失”。
- 不负责项：人物成长判断、物品归属/代价设计、父技能任务模式判定、全局 coverage gate 汇总。
- 与兄弟模块边界：角色模块先提供进入者与关系压力，场景模块负责把这些压力安放到可写戏空间，物品模块只在场景和人物规则已稳定后处理局部载体。

## 2. 预加载上下文

- 上层必读：
  - [`SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/SKILL.md)
  - [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/CONTEXT.md)
- 本层必读：
  - 当前 [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/scene-card-module/module-spec.md)
  - 当前 [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/scene-card-module/CONTEXT.md)
- 加载顺序：
  1. 根 `SKILL.md`
  2. 根 `CONTEXT.md`
  3. 当前 `module-spec.md`
  4. 当前 `CONTEXT.md`
  5. [`templates/scene-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/scene-card.json)
  6. `Init/north_star_contract.json`、`Init/初始化简报.json`、既有 `Cards/3-场景卡/**/*.json`
- 冲突优先级：用户显式请求 > `AGENTS.md` / 父 `SKILL.md` > 当前 `module-spec.md` > 当前 `CONTEXT.md`
- 默认不并入的上下文：角色私有成长细节与物品私有代价不直接复制进场景卡；场景只接收影响其功能、规则与进入条件的上游约束。
- 共享输入切片：
  - `north_star_contract.story_kernel / reader_promise / aesthetic_axes / cards`
  - `cards_seed.global_seed`
  - `unknowns.deferred_to_cards`
  - `templates/worldbuilding/faction-systems.md`
  - `templates/worldbuilding/world-rules.md`

## 3. 思维链

### Think-Think Design Snapshot

- mode: `思维链优化设计`
- task_essence: 把 `地点/空间诉求` 从“可描述场景”推进为“可写戏、可复用、受规则约束并能正式落盘的场景卡决策”。
- baseline_symptom: 旧版文档已经知道场景要看功能与规则，但没有把“先做空间职责判断、再压实规则风险、最后做复用优选”写成显式阶段式合同。

### 优化模式事实 / 推断分层

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | 当前文档已经有 `可写戏功能对齐 / 规则与风险闭合 / 复用回报比` 三轴，也保留了 `Phase 1-4` 与正式模板落点 | 当前 `module-spec.md`、父 `SKILL.md`、`templates/scene-card.json` | 保留既有任务本质、Phase 编排和模板落点 |
| `Inferred Gaps` | 旧版快照缺 `驱动/判废/对比` 字段拆分，也没有 `轴权归属检查 / 近邻替换压测 / 落盘扰动测试`，导致场景模块虽然有三轴，但仍可能滑回“布景板”语言 | 用户反馈 + 当前快照只到三轴/三重 | 重建字段层、验证层与落盘扰动说明 |
| `Protected Constraints` | 不破坏 `FIELD-CD-STR-01 / MAT-02 / CTX-01 / CST-01`、既有 Phase 1-4、场景模板结构、`scene_links` 的上游消费关系 | 根 `SKILL.md` 字段主表与当前模板/脚本约束 | 只加固思维链，不改父技能路由与正式 schema 契约 |
| `Proposed Rewrite` | 把场景模块从“有三轴的摘要卡”升级为“有字段锋利度、验证层和落盘扰动证据的思维链合同” | `think-think` 优化模式合同 | 增补向字段展开、分重关键向字段矩阵、方向评估与增强验证 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 漂移风险 | 为什么不是别的轴名 | 直接落点 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `可写戏功能对齐` | 该场景到底服务哪类戏剧用途，是否值得占用一个正式场景桶位 | 漂移成“画面更漂亮”或“世界观更大” | 因为场景模块首先要回答“这里能发生什么戏”，不是先回答“这里看起来多壮观” | `适用场景`、`Phase 1`、`quality standard` |
| `成立轴` | `规则与风险闭合` | 场景规则、危险、代价、进入条件、适配角色是否闭合 | 漂移成第二条“场景很有氛围”判断 | 因为这一轴负责判定“这个空间是否真的成立”，不是再说一次视觉价值 | `预加载上下文`、`Phase 2`、`Phase 3` |
| `优选轴` | `复用回报比` | 两个都成立的场景方案里，哪个更适合重复出场、复用成本更低 | 漂移成“更奇观”“更梦幻”的赞美轴 | 因为这里需要的是返场收益与复用成本比较，不是风格赞美 | `Phase 3`、`交付`、`验收机制` |

### 向字段展开（驱动 / 判废 / 对比）

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 主裁决层 |
| --- | --- | --- | --- | --- |
| `可写戏功能对齐` | `narrative_functions / compatible_roles / 场景桶归属` | `无法解释谁会来 / 不能支撑当前戏剧压力 / 问题本质不属于场景模块` | `当前卷返场频率 / 主冲突承载力 / 空间切换成本` | `粗裁决 / Base Range` |
| `规则与风险闭合` | `rule_and_risk.scene_rules / hazards / costs / access_level / scene_links` | `无规则约束 / 无危险代价 / 进入条件空缺 / 无法与世界规则对齐` | `规则清晰度 / 风险可执行性 / 角色适配稳定度` | `细裁决 / Range Narrowing` |
| `复用回报比` | `current_focus.repeat_use_strategy / sensory_anchors` | `返场策略为空 / 只能一次性消耗 / 需要靠旁白解释场景差异` | `复用回报 / 感官辨识度 / 与现有场景重合度` | `离散裁决 / Final Selection` |

### 三重

| 裁决层 | 本层关键问题 | 关键向字段 | 唯一主轴 | 本模块产物 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | 这是场景问题吗，属于哪一类场景桶，是否需要承担常驻或关键戏剧空间 | `narrative_functions / compatible_roles / 场景桶归属` | `可写戏功能对齐` | 场景模块命中结论、场景桶归属、功能目标 |
| `细裁决 / Range Narrowing` | 当前候选场景是否具备 `rule_and_risk / compatible_roles / access_level / costs` | `rule_and_risk.scene_rules / hazards / costs / access_level / scene_links` | `规则与风险闭合` | 正式场景 schema、规则与风险骨架 |
| `离散裁决 / Final Selection` | 多个成立场景里，哪个更能长期返场且不与现有场景重合 | `repeat_use_strategy / sensory_anchors / 与现有场景重合度` | `复用回报比` | 复用策略、感官锚点、差异化理由 |

### 方向评估矩阵

| 字段 | 定向性 | 区分性 | 约束性 | 落盘性 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `narrative_functions` | 直接决定场景是否服务当前戏剧压力 | 能区分常驻戏剧空间与装饰性地点 | 若功能说不清，场景不应进入正式落盘 | 对应 `FIELD-CD-STR-01 -> content.module_route` | PASS |
| `rule_and_risk.scene_rules` | 决定场景是否进入“规则成立”候选 | 能区分强规则场景与浮空奇观 | 缺规则就直接判废 | 对应 `FIELD-CD-MAT-02 -> content.card_groups.*` | PASS |
| `scene_links` | 决定场景是否可复用而非一次性消耗 | 能区分可连续返场与只会新增地点的方案 | 无链接会削弱复用稳定性 | 对应 `FIELD-CD-MAT-02` | PASS |
| `repeat_use_strategy` | 不改变候选范围，但决定成立解中的最终选择 | 能区分两个都成立但返场收益不同的场景方案 | 不能单独 veto，只做离散比较 | 对应 `FIELD-CD-CTX-01 -> execution_notes.design_rationale` | PASS |

### 快照落点说明

- 思维链如何作用于执行流程：`Phase 1` 先判断空间功能与桶位，`Phase 2` 再封闭规则和风险，`Phase 3` 才决定返场策略与感官表达。
- 思维链如何作用于交付：正式交付必须同时写出 `scene_links`、`rule_and_risk`、`compatible_roles` 与 `repeat_use_strategy`，不能只交漂亮描述。
- 思维链如何作用于验收：只要出现“无功能、无规则、无复用策略”的场景，即使画面感很强也直接返工。

### 字段落盘映射

| 裁决层 | 关键向字段 | field_id / 决策槽位 | 具体落点 | 说明 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `narrative_functions / compatible_roles / 场景桶归属` | `FIELD-CD-STR-01` | `content.module_route` + 路由记录 | 先判清是不是场景问题，否则下游规则字段无意义 |
| `细裁决 / Range Narrowing` | `rule_and_risk / access_level / scene_links` | `FIELD-CD-MAT-02` | `content.card_groups.*` / `content.card_schema.scene_card` | 场景成立条件必须进入正式 schema，不接受只写氛围说明 |
| `离散裁决 / Final Selection` | `repeat_use_strategy / sensory_anchors / 与现有场景重合度` | `FIELD-CD-CTX-01` | `content.loaded_references` + `execution_notes.design_rationale` | 用于解释“为什么选这个返场方案” |
| `Gate` | `无功能 / 无规则 / 无复用策略` | `FIELD-CD-CST-01` | `gate_summary.status` | 这些是 veto，不归 `优选轴` 越权处理 |

### 有效性验证

| 验证项 | 结论 | 证据/说明 | 若失败的返工入口 |
| --- | --- | --- | --- |
| `事实/推断分离` | PASS | 已把既有 Phase/模板合同与本轮推断缺口拆开，避免想象式重写 | 回到本节“优化模式事实 / 推断分层” |
| `遮轴名快检` | PASS | 遮掉轴名后仍可读出 `narrative_functions / rule_and_risk / repeat_use_strategy` 三组不同字段 | 回到“向字段展开” |
| `轴权归属检查` | PASS | `scene_links` 主归 `规则与风险闭合`，不再被 `优选轴` 偷拿来解释成“更方便复用” | 回到“三重”重写唯一主轴 |
| `近邻替换压测` | PASS | 若把 `可写戏功能对齐` 替换成 `场景氛围强度`，会失去对 `谁来做什么` 的裁决力 | 回到“三轴”与“方向评估矩阵” |
| `字段落盘追踪` | PASS | 三层都能追到 `FIELD-CD-STR-01 / MAT-02 / CTX-01 / CST-01` | 回到“字段落盘映射” |
| `落盘扰动测试` | PASS | 移除 `repeat_use_strategy` 会让两个都成立的场景方案无法完成最终取舍，也会直接削弱 `FIELD-CD-CTX-01` 的说明力 | 回到 `Phase 3` 与 `FIELD-CD-CTX-01` 落点 |

## 4. 执行流程

### Phase 1 场景路由与功能确认

- 目标：确认当前任务是否应进入场景模块，并锁定场景承担的戏剧功能与桶位。
- 输入：父 `SKILL.md` 路由段、用户诉求、`cards-check` finding、既有场景索引。
- 动作：
  - 判定是否属于地点/规则/危险/环境/复用策略问题。
  - 锁定 `室内 / 室外 / 自然 / 超现实` 场景桶。
  - Mixed 请求下确认角色模块是否已提供必要的进入者与冲突压力。
- 产出：场景模块命中结论、目标桶、需要读取的场景切片。
- 失败信号 / 返工入口：若无法回答“谁会来、来做什么、为何非这个场景不可”，退回父 `SKILL.md` 重新做对象路由。

### Phase 2 规则与风险闭合

- 目标：把场景从“有画面”推进到“规则、危险、代价、进入条件成立”。
- 输入：`north_star_contract.cards`、`world-rules.md`、`faction-systems.md`、既有场景卡。
- 动作：
  - 先补 `narrative_functions / compatible_roles`，再写感官与氛围。
  - 对超现实与强规则场景显式写出 `scene_rules / hazards / costs / access_level`。
  - 建立 `scene_links`，避免每个问题都新增一次性地点。
- 产出：可落盘的场景规则骨架、风险设计、适配角色与场景链接。
- 失败信号 / 返工入口：若超现实场景没有代价与限制、常驻场景没有复用策略、场景无法回答“谁适合来”，回本阶段重做。

### Phase 3 复用优选与模板映射

- 目标：在成立场景里选择更适合返场、复用、长期承担戏剧压力的方案，并映射到正式模板。
- 输入：Phase 2 通过的场景候选、[`scene-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/scene-card.json)、既有场景分布。
- 动作：
  - 比较 `repeat_use_strategy / sensory_anchors / 与现有场景重合度`。
  - 记录当前场景为何比替代场景更值得占用正式桶位。
  - 写入 `content.module_route / loaded_references / writeback_plan` 等 trace 槽位。
- 产出：正式场景卡 payload、返场理由、trace 字段。
- 失败信号 / 返工入口：若场景仍像一次性布景板，或多个场景互相争抢同一戏剧职责，回到 Phase 1-2 重分功能与规则。

### Phase 4 写回与 gate 回接

- 目标：把场景模块结果回接到正式写卡链路与 coverage gate。
- 输入：Phase 3 payload、`cards-write` / `cards-check` 约束、父技能回写边界。
- 动作：
  - 将正式产物落到 `Cards/3-场景卡/**/*.json`。
  - Mixed 场景下把已确认的空间规则回送给物品模块与根技能 gate。
  - 回跑场景桶 coverage 检查，确认场景卡真正可消费。
- 产出：正式场景卡、可追溯 trace、场景模块 gate 结论。
- 失败信号 / 返工入口：若写回后仍出现“只有画面没有戏”“规则缺席”“复用策略为空”，回到对应阶段修复。

## 5. 交付

- 类型：`内容输出型`
- 模式：以当前 `module-spec.md` 约束场景判断逻辑，以当前 `CONTEXT.md` 提供局部返工启发，以 `templates/scene-card.json` 作为正式 schema 骨架。
- 正式落点：
  - `Cards/3-场景卡/**/*.json`
  - coverage trace 中的 `content.module_route / loaded_references / writeback_plan`
- 上层消费方式：父 `SKILL.md` 在场景请求、mixed 串行中段、场景桶 coverage 返工时进入本模块；根技能把本模块产出的空间规则并入最终 gate。
- 输出模板/字段骨架：
  - `core / current_state / history`
  - `scene_links`
  - `current_focus.repeat_use_strategy`
  - `rule_and_risk`
  - `compatible_roles`

## 6. 验收机制

- quality standard：
  - 每张正式场景卡都能回答“允许什么戏发生、谁适合进入、进入的代价是什么、为何值得反复使用”。
  - 强规则场景必须显示世界规则接口，不能只靠氛围词支撑。
  - 场景模块应减少一次性奇观，优先建立可反复消费的戏剧空间。
- acceptance checklist：
  - [ ] 父技能能明确说明何时进入场景模块
  - [ ] 已读取根 `SKILL.md`、根 `CONTEXT.md`、当前 `module-spec.md`、当前 `CONTEXT.md`
  - [ ] 场景桶归属明确，且无兄弟模块职责串位
  - [ ] `rule_and_risk + compatible_roles + scene_links + repeat_use_strategy` 均已成立
  - [ ] 正式 payload 已映射到 `templates/scene-card.json`
  - [ ] 写回后 coverage gate 无场景模块 blocking finding
- fail signal：
  - 场景只有美术描述、没有叙事功能
  - 超现实场景没有规则与代价
  - 场景无法回答“谁适合来、来做什么”
  - 场景复用策略为空或与既有场景严重重合
- rework entry：
  - 路由错误 -> 回父 `SKILL.md` Section 9
  - 功能与桶位问题 -> 回 Phase 1
  - 规则/风险问题 -> 回 Phase 2
  - 复用与 trace 问题 -> 回 Phase 3
  - coverage gate 问题 -> 回 Phase 4 并联动根 `CONTEXT.md`

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是，场景相关请求与 mixed 中段都显式进入本模块。
- 若为多模块场景，是否已有统一路由段落：是，父技能已有条件加载矩阵；本轮会补强默认顺序、模块关系与 `module CONTEXT` 的读取顺序。
- 父 `SKILL.md` 中的模块关系：角色/场景/物品按对象类型互斥；mixed 与全量建卡按 `角色 -> 场景 -> 物品` 串行；coverage repair 仅按需加载命中模块。

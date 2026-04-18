# Character Card Module Spec

## Module Identity

- module_type: `governed-reference`
- canonical_reference_path: `references/character-card-module/module-spec.md`
- canonical_context_path: `references/character-card-module/CONTEXT.md`
- canonical_module_route: `story-cards > references/character-card-module/module-spec.md`
- shared_template_source: `/Users/vincentlee/.codex/skills/meta/references-update/templates/reference-module-spec-template.md`

## 1. 适用场景

- 上层 SKILL 语境：本模块服务 [`1-Cards/SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/SKILL.md) 的角色对象路由，是 `角色 / 场景 / 物品` 三兄弟模块中的角色分支。
- 当前模块负责对象/范围：人物、关系、弧光、服装、声口、成长时间线、专属物接口，以及角色桶覆盖率返工。
- 模块归属类型：多子类型之一；当父技能判定当前对象为 `character`，或在 mixed 请求里需要按 `角色 -> 场景 -> 物品` 串行起手时进入本模块。
- 进入触发信号：用户提人物、关系、角色成长、身份层级、专属物、服装辨识、时间线锚点；或 `cards-check` 指向角色桶稀薄、关系边断裂、角色撞位。
- 不负责项：场景规则设计、物品代价设计、父技能任务模式判定、全局 coverage gate 汇总。
- 与兄弟模块边界：角色模块先输出可消费的人物真源与 `exclusive_item_hooks`；场景模块承接空间/规则；物品模块只能在角色接口已稳定后吸收角色约束。

## 2. 预加载上下文

- 上层必读：
  - [`SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/SKILL.md)
  - [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/CONTEXT.md)
- 本层必读：
  - 当前 [`module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/character-card-module/module-spec.md)
  - 当前 [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/character-card-module/CONTEXT.md)
- 加载顺序：
  1. 根 `SKILL.md`
  2. 根 `CONTEXT.md`
  3. 当前 `module-spec.md`
  4. 当前 `CONTEXT.md`
  5. [`templates/character-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/character-card.json)
  6. `Init/north_star_contract.json`、`Init/初始化简报.json`、既有 `Cards/2-角色卡/**/*.json`
- 冲突优先级：用户显式请求 > `AGENTS.md` / 父 `SKILL.md` > 当前 `module-spec.md` > 当前 `CONTEXT.md`
- 默认不并入的上下文：`2-Planning` 的 MAP 事件明细不直接并入角色卡正文；需要事件时间时只回指 `Planning/8-全息地图.json`，不复制事件流水。
- 共享输入切片：
  - `north_star_contract.story_kernel / reader_promise / aesthetic_axes / cards`
  - `cards_seed.character_seed`
  - `unknowns.deferred_to_cards`
  - `templates/worldbuilding/character-design.md`

## 3. 思维链

### Think-Think Design Snapshot

- mode: `思维链优化设计`
- task_essence: 把 `人物相关诉求` 从“泛人物设定”推进为“可区分、可成长、可挂专属物接口并可正式落盘的角色卡决策”。
- baseline_symptom: 旧版文档更像字段摘要卡，能告诉执行者“要看哪些字段”，却不能稳定指导“何时进入角色模块、怎样做成立裁决、何时把问题退回父技能重路由”。

### 优化模式事实 / 推断分层

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | 当前文档已经有 `角色戏份职责对齐 / 成长与关系闭合 / 辨识收益比` 三轴，也保留了 `Phase 1-4` 与正式模板落点 | 当前 `module-spec.md`、父 `SKILL.md`、`templates/character-card.json` | 保留既有任务本质、Phase 编排和模板落点 |
| `Inferred Gaps` | 旧版快照缺 `驱动/判废/对比` 字段拆分，也没有 `轴权归属检查 / 近邻替换压测 / 落盘扰动测试`，导致三轴看起来成立，但字段锋利度不足 | 用户反馈“思维链执行不到位” + 当前快照只到三轴/三重 | 重建字段层、验证层与落盘扰动说明 |
| `Protected Constraints` | 不破坏 `FIELD-CD-STR-01 / MAT-01 / CTX-01 / CST-01`、既有 Phase 1-4、角色模板结构、`exclusive_item_hooks` 的下游接口责任 | 根 `SKILL.md` 字段主表与当前模板/脚本约束 | 只加固思维链，不改父技能路由与正式 schema 契约 |
| `Proposed Rewrite` | 把角色模块从“有三轴的摘要卡”升级为“有字段锋利度、验证层和落盘扰动证据的思维链合同” | `think-think` 优化模式合同 | 增补向字段展开、分重关键向字段矩阵、方向评估与增强验证 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 漂移风险 | 为什么不是别的轴名 | 直接落点 |
| --- | --- | --- | --- | --- | --- |
| `方向轴` | `角色戏份职责对齐` | 当前候选角色到底承担哪类戏、落在哪个角色桶、是否值得成为正式人物真源 | 漂移成“设定更满”或“标签更多” | 因为角色模块首先要回答“这个人负责推进什么戏”，不是先回答“这个人有多少设定” | `适用场景`、`Phase 1`、`质量标准` |
| `成立轴` | `成长与关系闭合` | 角色弧光、关系边、时间锚点、专属物接口是否闭合，而不是只剩标签堆叠 | 漂移成第二条“角色很重要”判断 | 因为这一轴负责判定“过线不过线”，不是再说一次角色价值 | `预加载上下文`、`Phase 2`、`Phase 3` |
| `优选轴` | `辨识收益比` | 多个成立方案里，哪个更不撞位、更好记、后续消费成本更低 | 漂移成“更酷”“更有味道”的赞美轴 | 因为这里需要的是成立解之间的可比收益尺，而不是审美口号 | `Phase 3`、`交付`、`验收机制` |

### 向字段展开（驱动 / 判废 / 对比）

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 主裁决层 |
| --- | --- | --- | --- | --- |
| `角色戏份职责对齐` | `角色桶归属 / narrative_function / relationship_network_position` | `戏份职责空缺 / 与现有主角色职责重叠 / 无法解释为什么当前问题应进入角色模块` | `当前卷聚焦度 / 与主线压力咬合度 / 群像负载成本` | `粗裁决 / Base Range` |
| `成长与关系闭合` | `experience_timeline / current_state.timeline_anchor / relationship_edges / exclusive_item_hooks` | `时间线流水账 / 关系边虚连 / 专属物接口缺失 / 当前状态无法挂到时间锚点` | `成长转折清晰度 / 关系闭合度 / 下游物品可消费性` | `细裁决 / Range Narrowing` |
| `辨识收益比` | `speech_texture / gesture_habits / outfit_view` | `辨识信号全靠标签词 / 角色声口与兄弟角色重复 / 只能靠旁白解释人物差异` | `首识别成本 / 记忆黏性 / 变体扩展成本 / 撞位风险` | `离散裁决 / Final Selection` |

### 三重

| 裁决层 | 本层关键问题 | 关键向字段 | 唯一主轴 | 本模块产物 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | 这是角色问题吗，属于哪一桶人物，是否应该先于场景/物品进入 | `角色桶归属 / narrative_function / relationship_network_position` | `角色戏份职责对齐` | 角色模块命中结论、角色桶归属、进入信号 |
| `细裁决 / Range Narrowing` | 当前候选角色是否具备 `experience_timeline / timeline_anchor / relationship_edges / exclusive_item_hooks` | `experience_timeline / current_state.timeline_anchor / relationship_edges / exclusive_item_hooks` | `成长与关系闭合` | 正式角色 schema、关系边与时间线骨架 |
| `离散裁决 / Final Selection` | 两个都成立的角色方案里，哪个更有辨识度且更利于后续物品/剧情消费 | `speech_texture / gesture_habits / outfit_view / 撞位风险` | `辨识收益比` | 设计理由、辨识信号、减撞位选择 |

### 方向评估矩阵

| 字段 | 定向性 | 区分性 | 约束性 | 落盘性 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `角色桶归属` | 直接决定先往哪类人物簇收敛 | 能区分主角色、反派、次要、群像 | 若桶位说不清，当前请求不应进入正式角色写回 | 对应 `FIELD-CD-STR-01 -> content.module_route` | PASS |
| `experience_timeline` | 决定角色是否进入“成长成立”候选 | 能区分成长型角色与标签型角色 | 流水账时间线会直接判废 | 对应 `FIELD-CD-MAT-01 -> content.card_groups.*` | PASS |
| `exclusive_item_hooks` | 决定角色是否能被下游物品模块消费 | 能区分“有后续接口”的角色与纯装饰角色 | 缺失接口时物品专属适配直接失真 | 对应 `FIELD-CD-MAT-01 / item module input` | PASS |
| `撞位风险` | 不改变候选范围，但决定成立解中的最终取舍 | 能区分两个都成立但记忆成本不同的角色方案 | 不能单独 veto，只能做离散比较 | 对应 `FIELD-CD-CTX-01 -> execution_notes.design_rationale` | PASS |

### 快照落点说明

- 思维链如何作用于执行流程：`Phase 1` 先裁角色桶与进入资格，`Phase 2` 再压实成长/关系闭合，`Phase 3` 才做辨识度优选和模板落盘映射。
- 思维链如何作用于交付：正式交付必须同时带出 `relationship_edges`、`experience_timeline`、`exclusive_item_hooks` 和 trace 字段，避免只交一张好看的人设卡。
- 思维链如何作用于验收：只要出现“角色很多但分工不清”“有经历没成长含义”“专属物接口缺失”，直接判定返工，不接受以细节描写掩盖结构失败。

### 字段落盘映射

| 裁决层 | 关键向字段 | field_id / 决策槽位 | 具体落点 | 说明 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `角色桶归属 / narrative_function` | `FIELD-CD-STR-01` | `content.module_route` + 路由记录 | 角色问题若未先命中角色模块，后续字段全部失效 |
| `细裁决 / Range Narrowing` | `experience_timeline / timeline_anchor / relationship_edges / exclusive_item_hooks` | `FIELD-CD-MAT-01` | `content.card_groups.*` / `content.card_schema.character_card` | 角色成立条件必须写入正式 schema，不接受只留说明文本 |
| `离散裁决 / Final Selection` | `speech_texture / gesture_habits / outfit_view / 撞位风险` | `FIELD-CD-CTX-01` | `content.loaded_references` + `execution_notes.design_rationale` | 用于解释“为什么选这个角色表达而不是另一个” |
| `Gate` | `角色撞位 / 时间线流水账 / 接口缺失` | `FIELD-CD-CST-01` | `gate_summary.status` | 这些是 veto，不归 `优选轴` 越权处理 |

### 有效性验证

| 验证项 | 结论 | 证据/说明 | 若失败的返工入口 |
| --- | --- | --- | --- |
| `事实/推断分离` | PASS | 已把保留合同与本轮推断缺口拆开，避免凭印象重写 | 回到本节“优化模式事实 / 推断分层” |
| `遮轴名快检` | PASS | 遮掉轴名后仍可读出 `角色桶归属 / experience_timeline / 撞位风险` 三组不同字段 | 回到“向字段展开” |
| `轴权归属检查` | PASS | `exclusive_item_hooks` 主归 `成长与关系闭合`，不再被 `优选轴` 解释权污染 | 回到“三重”重写唯一主轴 |
| `近邻替换压测` | PASS | 若把 `角色戏份职责对齐` 替换成 `人设浓度`，会立刻失去对角色桶和戏份职责的约束力 | 回到“三轴”与“方向评估矩阵” |
| `字段落盘追踪` | PASS | 三层都能追到 `FIELD-CD-STR-01 / MAT-01 / CTX-01 / CST-01` | 回到“字段落盘映射” |
| `落盘扰动测试` | PASS | 移除 `exclusive_item_hooks` 会直接让 `FIELD-CD-MAT-01` 不完整，并切断 item module 的消费链 | 回到 `Phase 2` 与 `FIELD-CD-MAT-01` 落点 |

## 4. 执行流程

### Phase 1 路由与角色桶确认

- 目标：确认当前任务是否应进入角色模块，并锁定角色桶与角色问题边界。
- 输入：父 `SKILL.md` 路由段、用户诉求、`cards-check` finding、既有角色卡索引。
- 动作：
  - 判定是否属于人物/关系/弧光/专属物接口问题。
  - 若是 mixed 请求，固定先进入角色模块，再决定是否串到场景或物品模块。
  - 锁定 `主要角色 / 反派角色 / 次要角色 / 群像角色` 中的目标桶位。
- 产出：角色模块命中结论、目标桶、需要读取的角色卡切片。
- 失败信号 / 返工入口：若一句话无法说明“这是谁、负责哪类戏、为何现在要改他”，退回父 `SKILL.md` 的对象路由重新判定。

### Phase 2 角色成立裁决

- 目标：把角色从“设定存在”推进到“成长、关系、时间锚点成立”。
- 输入：`north_star_contract.cards`、`cards_seed.character_seed`、既有角色卡、模块 `CONTEXT.md` 的局部故障模式。
- 动作：
  - 先补 `narrative_function` 与 `relationship_edges`，再写人物细节。
  - 把经历沉到 `experience_timeline`，把当前有效状态压到 `current_state.timeline_anchor`。
  - 为后续物品模块预留 `exclusive_item_hooks`。
- 产出：可落盘的角色卡 schema 决策、关系边、时间锚点、专属物接口。
- 失败信号 / 返工入口：若时间线只是事件流水、关系边无法支撑戏份、专属物接口缺失，回到本阶段重做，不进入模板映射。

### Phase 3 角色表达优选与模板映射

- 目标：在成立角色中选择最有辨识度且不撞位的表达，并映射到正式模板。
- 输入：Phase 2 通过的角色候选、[`character-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/character-card.json)、既有角色群像分布。
- 动作：
  - 比较 `speech_texture / gesture_habits / outfit_view / 撞位风险`。
  - 记录为何选择当前表达而非替代方案。
  - 补齐 `content.module_route / loaded_references / writeback_plan` 等 trace 槽位。
- 产出：正式角色卡 payload、辨识理由、trace 字段。
- 失败信号 / 返工入口：若多个角色仍互相撞位，或模板里只剩设定词没有戏份职责，回到 Phase 1-2 重分桶或重做成长/关系闭合。

### Phase 4 写回与 gate 回接

- 目标：把角色模块结果回接到正式写卡链路与 coverage gate。
- 输入：Phase 3 payload、`cards-write` / `cards-check` 调用约束、父技能回写边界。
- 动作：
  - 将正式产物落到 `Cards/2-角色卡/**/*.json`。
  - Mixed 场景下把角色约束显式交给场景/物品模块。
  - 回跑角色桶 coverage 检查，确认 gate 可消费。
- 产出：正式角色卡、可追溯 trace、角色模块 gate 结论。
- 失败信号 / 返工入口：若写回后 `cards-check` 仍提示撞位、缺成长、缺接口，回到对应阶段修复，不允许用手工说明替代正式产物。

## 5. 交付

- 类型：`内容输出型`
- 模式：以当前 `module-spec.md` 约束角色判断逻辑，以当前 `CONTEXT.md` 提供局部返工启发，以 `templates/character-card.json` 作为正式 schema 骨架。
- 正式落点：
  - `Cards/2-角色卡/**/*.json`
  - coverage trace 中的 `content.module_route / loaded_references / writeback_plan`
- 上层消费方式：父 `SKILL.md` 在角色请求、mixed 串行起手、角色桶 coverage 返工时进入本模块；物品模块消费本模块产出的 `exclusive_item_hooks`。
- 输出模板/字段骨架：
  - `core / current_state / history`
  - `relationship_edges`
  - `exclusive_item_hooks`
  - `experience_timeline`
  - `current_state.timeline_anchor`

## 6. 验收机制

- quality standard：
  - 每张正式角色卡都能回答“负责哪类戏、与谁形成关系、经历如何改变了他、为何能绑定某类专属物”。
  - 角色辨识度依赖职责、关系和行为方式，不依赖单纯外观堆砌。
  - Mixed 请求进入角色模块后，能为兄弟模块输出稳定接口，而不是把问题留给下游猜。
- acceptance checklist：
  - [ ] 父技能能明确说明何时进入角色模块
  - [ ] 已读取根 `SKILL.md`、根 `CONTEXT.md`、当前 `module-spec.md`、当前 `CONTEXT.md`
  - [ ] 角色桶归属明确，且无兄弟模块职责串位
  - [ ] `experience_timeline + timeline_anchor + relationship_edges + exclusive_item_hooks` 均已成立
  - [ ] 正式 payload 已映射到 `templates/character-card.json`
  - [ ] 写回后 coverage gate 无角色模块 blocking finding
- fail signal：
  - 角色很多但撞位
  - 角色只有标签、没有行为与弧光
  - 时间线是事件流水账
  - 专属物接口缺失或无法被下游消费
- rework entry：
  - 路由错误 -> 回父 `SKILL.md` Section 9
  - 角色桶/关系边问题 -> 回 Phase 1-2
  - 成长/时间锚点问题 -> 回 Phase 2
  - 辨识度或 trace 问题 -> 回 Phase 3
  - coverage gate 问题 -> 回 Phase 4 并联动根 `CONTEXT.md`

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是，角色相关请求与 mixed 串行起手都显式进入本模块。
- 若为多模块场景，是否已有统一路由段落：是，父技能的 `References 模块与触发细则` 已提供统一矩阵；本轮会进一步强化默认顺序、互斥与按需规则。
- 父 `SKILL.md` 中的模块关系：角色/场景/物品按对象类型互斥；mixed 与全量建卡按 `角色 -> 场景 -> 物品` 串行；coverage repair 仅按需加载命中模块。

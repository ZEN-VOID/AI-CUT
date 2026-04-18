# Creative Seed Routing Module Spec

## 1. 适用场景

- 上层 SKILL 语境：`story2026/0-Init` 已完成模式锁定，但 `project_contract.creative_mandate`、`planning_seed`、商业定位或反套路约束仍存在真实缺口。
- 当前模块负责对象/范围：治理 `0-Init` 内所有创意相关 leaf references 的统一路由，包括约束包、卖点、复合题材、灵感救援、平台定位、反套路映射与趋势校准。
- 模块归属类型：多种情况触发之一。
- 进入触发信号：
  - `规划模块卡` 缺少故事引擎、开篇钩子、约束包、反套路或卖点。
  - `商业与风格模块卡` 缺少平台语义、目标读者、风格走廊或禁飞区校准。
  - 用户选择复合题材，需要 A+B 融合规则。
  - 用户卡在创意阶段，需要候选卖点、钩子或约束提示。
  - 用户显式要求“参考当下趋势”或“按当前平台风向校准”。
- 不负责项：
  - 不重新定义三种 `init_mode` 的选择与执行。
  - 不替代 `templates/genres/` 与 `templates/worldbuilding/` 的共享真源角色。
  - 不把 `2-Planning` 的 canonical 编排真源提前拍死。
- 与兄弟模块边界：
  - `advisor-council-mode / fast-mode / autonomous-mode` 决定执行形态。
  - 本模块只负责创意相关资料的最小读取与槽位回写，不决定模式本身。

## 2. 预加载上下文

- 上层必读：
  - 根 `SKILL.md`
  - 根 `CONTEXT.md`
- 本层必读：
  - 当前 `module-spec.md`
  - 当前 `CONTEXT.md`
- 加载顺序：
  1. 根 `SKILL.md`
  2. 根 `CONTEXT.md`
  3. 当前 `module-spec.md`
  4. 当前 `CONTEXT.md`
- 冲突优先级：用户显式请求 > 仓库 `AGENTS.md` / 元规则 > 根 `SKILL.md` > 当前 `module-spec.md` > 根 `CONTEXT.md` > 当前 `CONTEXT.md`
- 默认不并入的上下文：
  - 未命中的 mode-playbook `CONTEXT.md`
  - 不相关题材与 worldbuilding 叶子资料
  - `market-trends-2026.md`，除非命中趋势校准闸门

## 3. 思维链

### Think-Think Design Snapshot

#### Meta

- mode: `chain-optimization`
- target_object: `0-Init/references/creative-seed-routing/module-spec.md`
- trigger: 用户明确指出“思维链执行不到位”，要求按 `think-think` 强化
- baseline_source:
  - 当前文件既有 `Think-Think Design Snapshot`
  - `think-think/references/chain-optimization.md`
  - `think-think/templates/think-quadrant-template.md`
- downstream_consumers:
  - `0-Init/SKILL.md` 的 `Reference Loading Guide`
  - 三个 mode-playbook 的 `Shared Dependency Contract`
  - `project_contract.creative_mandate / planning_seed / unknowns`

#### 优化模式事实 / 推断分层

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | 当前版本虽然已有三轴三重，但只有“核心判断/本层关键问题”级表述，没有 `保留/修正/重建矩阵`、`每轴驱动/判废/对比字段`、`验证矩阵`、`落盘映射` | 当前文件既有思维链段落 | 保留已有轴名方向，补全优化模式缺失结构 |
| `Observed Facts` | 当前交付段只写了落点列表，未把“哪一重落到哪个槽位”拆开 | 当前文件 `## 5. 交付` | 新增按三重拆开的字段/步骤/槽位映射 |
| `Inferred Gaps` | 上一版更接近 `references-update` 的模块快照，而不是 `think-think` 的完整优化执行；因此可读但不够可验证 | 用户反馈 + `think-think` 的可见化执行合同 | 把思维链升级为显式优化模式工作台投影 |
| `Protected Constraints` | 不改变本模块的职责边界、leaf reference 目录、上层消费接口和 L3 趋势双闸门 | 当前文件既有 scope / phases / delivery | 只强化思维链与验证，不改业务路由真义 |
| `Proposed Rewrite` | 保留 `缺口驱动路由 / 可写回承诺成立 / 最小读取最大差异化` 三轴命名，但补齐任务本质、字段矩阵、增强验证、Gate Summary 对应落点 | 本轮 `think-think` 优化目标 | 在当前文件原位增补，不另起平行体系 |

#### 任务本质与优化边界

- 任务终局句：
  - 本模块真正要把 `创意相关缺口` 从 `散点参考读取` 推到 `可判型、可最小读取、可回写到初始化槽位的统一路由`
- 当前思维链症状：
  - 轴已经有了，但“向”还不够硬，读者难以判断每层究竟依赖哪些关键字段。
  - 有三重，但缺少前后对照、字段压测和落盘追踪，导致更像说明而非可验证合同。
  - 有交付落点，但没有明确说明每一重怎样影响上层槽位与返工入口。
- 保留 / 修正 / 重建矩阵：

| 组件 | 当前状态 | 动作 |
| --- | --- | --- |
| 任务本质 | 隐含存在，但未显式终局化 | 重写 |
| 轴角色 | 命名有效、边界基本成立 | 保留 + 修正 |
| 分重字段 | 有问题，但还未压到驱动/判废/对比层 | 重建 |
| 验证机制 | 只有验收清单，缺 `think-think` 增强验证 | 重建 |
| 落盘映射 | 有总体落点，缺分重追踪 | 修正 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | `缺口驱动路由` | 当前真正阻塞的是约束包、卖点、商业定位、复合题材、反套路还是趋势校准 | `Phase 1`、触发矩阵 |
| `成立轴` | `可写回承诺成立` | 读取到的创意资料是否能压缩成 `creative_mandate / planning_seed / unknowns`，而不是留成资料墙 | `Phase 3`、交付 |
| `优选轴` | `最小读取最大差异化` | 在多个可用 leaf references 中，哪组最小资料组合既能补齐缺口，又不把初始化层读得过重或过时 | `Phase 2`、验收机制 |

### 每条轴常看的关键向字段

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 说明 |
| --- | --- | --- | --- | --- |
| 方向轴 | `缺口类型`、`当前阻塞槽位`、`用户显式请求` | 把对象层/worldbuilding 缺口误认成创意缺口；没有真实缺口却想全读 | `约束包优先级`、`商业定位优先级`、`趋势校准必要性` | 决定“先走哪条创意路由” |
| 成立轴 | `槽位可写回性`、`来源分层可追溯性`、`deferred_to_planning 边界` | 输出仍是资料墙；把 `2-Planning` canonical 提前拍死；来源混写 | `creative_mandate` 与 `planning_seed` 的承接稳定度 | 决定“读到的材料能不能真正进入 handoff” |
| 优选轴 | `读取成本`、`差异化收益`、`时效风险` | 一次加载过多 leaf references；未授权就拉趋势资料；多份资料收益重叠 | 同一缺口下哪组最小资料更划算 | 决定“在成立解里选最小而不失效的组合” |

### 三重

| 裁决层 | 本层关键向字段 | 这些字段分别服务哪条轴角色 | 典型问题 | 候选边界 | 排除逻辑 | 下一层仍允许什么 | 有效性检查 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `缺口类型`、`阻塞槽位`、`显式趋势请求` | `方向轴 / 优选轴` | 该不该进入本模块、先走哪种创意子路由 | 只允许 `约束包 / 卖点 / 商业定位 / 复合题材 / 灵感救援 / 反套路 / 趋势校准` 七类缺口 | 对象层、worldbuilding、纯执行模式问题直接排出 | 保留 1-2 个最相关子路由进入下一层 | 遮掉轴名后仍能看见是“判缺口类型”，不是泛泛“先想清楚” |
| `细裁决 / Range Narrowing` | `最小读取清单`、`题材到反套路映射`、`趋势双闸门` | `优选轴 / 方向轴 / 成立轴` | 同一缺口下到底读哪几份 leaf references 才够 | 只在上一层保留的子路由内选择最小资料集 | 4 份以上 leaf references 同时命中、未授权趋势读取、题材映射错位直接排出 | 保留 1 组可成立的最小资料集进入回写 | 改成相邻泛词后无法维持“最小读取”约束，说明字段够锋利 |
| `离散裁决 / Final Selection` | `creative_mandate_update`、`planning_seed_update`、`unknowns_update`、`sources_breakdown` | `成立轴 / 优选轴` | 哪些候选该正式写回，哪些该延后给 `2-Planning` | 只比较已成立且来源可追溯的候选写回方案 | 资料摘要、无 provenance 的脑补、越权拍死 planning canonical 的写法全部淘汰 | 输出最终结构化槽位更新 | 调整字段后若 handoff 槽位不变，则当前“向”是假落盘 |

### 层内自省

#### 粗裁决 / Base Range

- 为什么是这个结果：
  - 方向轴判断：先确定是否真是创意缺口，避免本模块吞掉非创意问题。
  - 成立轴判断：只有能指向 `creative_mandate / planning_seed / unknowns` 的缺口才值得进入本模块。
  - 优选轴判断：不先缩小缺口类型，后续一定会读多。
- 如果不是这个结果，会不会有更好的答案：
  - 方向轴判断：若把题材细节或世界规则误归本模块，只会把边界重新弄脏。
  - 成立轴判断：若没有真实阻塞槽位，模块读取不会产生合法写回。
  - 优选轴判断：粗裁决不收窄，后面“最小读取”无法成立。

#### 细裁决 / Range Narrowing

- 为什么是这个结果：
  - 方向轴判断：不同缺口只能通向对应 leaf references，不能靠感觉多读。
  - 成立轴判断：趋势资料必须保留双闸门，否则时效资产会越权。
  - 优选轴判断：最优不是“读得最多”，而是“读最少仍然够写回”。
- 如果不是这个结果，会不会有更好的答案：
  - 方向轴判断：若不维护 genre -> anti-trope 映射，本模块仍会把题材判断外溢给上层。
  - 成立轴判断：若 leaf references 太多，回写会重新退化成资料墙。
  - 优选轴判断：同类资料收益重叠时，必须优先保留更靠近当前阻塞槽位的那组。

#### 离散裁决 / Final Selection

- 为什么是这个结果：
  - 方向轴判断：最终只选能直接推进初始化 handoff 的结构化写回。
  - 成立轴判断：来源必须可追溯，且不能越权拍死 `2-Planning`。
  - 优选轴判断：优先选择能最短路径推进下游消费的写回方案。
- 如果不是这个结果，会不会有更好的答案：
  - 方向轴判断：若还保留资料摘要，就说明本模块没有完成路由职责。
  - 成立轴判断：若 provenance 不清，`0-Init` 下游就无法区分用户承诺和助手推断。
  - 优选轴判断：若 `unknowns` 能承接更安全，就不该硬写成 `planning_seed`。

### 快照落点说明

- 思维链如何作用于执行流程：先判缺口类型，再读最小 leaf references，最后只回写结构化槽位。
- 思维链如何作用于交付：所有输出都必须落到 `project_contract.creative_mandate / planning_seed / unknowns`，而不是把参考文档内容原样搬进 handoff。
- 思维链如何作用于验收：若父 `SKILL.md` 或 mode-playbook 继续直接点名 leaf references，或趋势资料在未授权时被读取，视为模块失效。

## 4. 执行流程

### Phase 1 缺口判型

- 目标：识别当前到底需要哪一类创意路由，而不是把整个目录全读一遍。
- 输入：
  - 当前模式
  - 已确认题材、平台、目标读者、故事一句话、核心冲突
  - `planning_seed` / `creative_mandate` / `unknowns` 当前缺口
- 动作：
  - 先判断是 `约束包 / 卖点 / 商业定位 / 复合题材 / 灵感救援 / 反套路 / 趋势校准` 哪一类或哪几类。
  - 若缺口属于对象层或 worldbuilding，立即回退到共享 `templates/worldbuilding/` 或下游 `1-Cards` 路由，不在本模块硬补。
- 产出：
  - 当前回合的 `creative_route_plan`
  - 是否需要进入趋势 L3 的闸门判定
- 失败信号 / 返工入口：
  - 若只是“想显得充分”而没有真实缺口，停止加载并回到上层流程。

### Phase 2 最小读取与叶子路由

- 目标：为每类缺口只选择最小足够的本地 leaf references。
- 输入：
  - `creative_route_plan`
  - 已选题材、平台、商业目标、用户是否显式授权趋势参考
- 动作：
  - 按下表选择 leaf references：

| 场景 | 最小读取 | 主写回槽位 |
| --- | --- | --- |
| 规划模块卡默认缺约束包 | `creativity-constraints.md` + `category-constraint-packs.md` + `selling-points.md` | `planning_seed.hard_constraints / anti_trope / opening_hook` |
| 商业与风格模块卡缺平台语义 | `market-positioning.md` | `project_contract.target_reader / platform / creative_mandate` |
| 用户选择复合题材 | `creative-combination.md` | `planning_seed.story_engine / creative_mandate.one_liner` |
| 用户卡顿，需要候选刺激 | `inspiration-collection.md`，必要时补 `selling-points.md` | `creative_mandate.core_selling_points / opening_hook / unknowns` |
| 需要 genre-specific 反套路 | 按题材映射读取对应 `anti-trope-*.md` | `planning_seed.anti_trope / hard_constraints` |
| 用户显式要求当下趋势 | `market-trends-2026.md` + `WebSearch/WebFetch` | `creative_mandate / unknowns.risk_notes` |

  - 题材到反套路映射固定为：
    - 修仙 / 玄幻 / 高武 / 西幻 -> `anti-trope-xianxia.md`
    - 都市 / 历史 / 职场 / 娱乐圈 -> `anti-trope-urban.md`
    - 游戏 / 科幻 / 末世 / 电竞 -> `anti-trope-game.md`
    - 规则怪谈 / 悬疑 / 灵异 / 克苏鲁 -> `anti-trope-rules-mystery.md`
- 产出：
  - `loaded_leaf_references`
  - 当前回合的结构化候选
- 失败信号 / 返工入口：
  - 若一次性命中 4 份以上 leaf references，先回到 Phase 1 重新压缩缺口定义。

### Phase 3 槽位回写与来源分层

- 目标：把参考结果压缩成初始化可消费的结构化字段。
- 输入：
  - `loaded_leaf_references`
  - 用户原始表达
  - 当前模式下的来源策略
- 动作：
  - 只输出 `project_contract.creative_mandate / planning_seed / unknowns` 所需字段。
  - 显式区分 `user_confirmed / assistant_inferred / council_advised`。
  - 若某项只适合 `2-Planning` 再细化，则写入 `unknowns.deferred_to_planning`。
- 产出：
  - `creative_mandate_update`
  - `planning_seed_update`
  - `unknowns_update`
- 失败信号 / 返工入口：
  - 若输出仍是参考摘要或资料清单，而不是槽位更新，退回 Phase 2。

### Phase 4 路由验收与回接

- 目标：确认上层入口、mode-playbook 与本模块已形成单一真源链路。
- 输入：
  - 更新后的父 `SKILL.md`
  - 三个 mode-playbook 的共享依赖段
  - 当前模块 `CONTEXT.md`
- 动作：
  - 验证父 `SKILL.md` 已显式写明何时进入本模块。
  - 验证 mode-playbook 不再直连本模块内部 leaf references。
  - 验证趋势资料仍受用户显式请求闸门约束。
- 产出：
  - `routing_gate_summary`
- 失败信号 / 返工入口：
  - 若任一上层文件仍散点维护 leaf reference 入口，回到 Phase 4 修路由。

## 5. 交付

- 类型：非内容输出型
- 模式：为 `0-Init` 的创意相关缺口提供统一的 leaf reference 路由与结构化写回。
- 正式落点：
  - `project_contract.creative_mandate`
  - `project_contract.target_reader / platform`
  - `planning_seed.anti_trope / hard_constraints / story_engine / opening_hook`
  - `unknowns.deferred_to_planning / risk_notes`
- 上层消费方式：
  - 父 `SKILL.md` 把本模块视为唯一创意 references 入口。
  - mode-playbook 只声明依赖本模块，不再点名内部 leaf docs。
- 若为内容输出型，输出模板/字段骨架：N/A
- 若为非内容输出型，执行模式/状态推进方式：
  - `判型 -> 最小读取 -> 槽位回写 -> 路由验收`
  - 趋势资料始终保持 `用户显式请求 + WebSearch/WebFetch` 双闸门

### 分重字段落盘映射

| 裁决层 | 服务字段 / 决策槽 | 具体落盘位置 | 采用理由 | 被排除候选为何不成立 | 失败返工入口 |
| --- | --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `creative_route_plan` / `loaded_references` | 当前模块执行记录、父 `SKILL.md` 的 `Reference Loading Guide` | 先决定是否命中本模块以及命中哪类子路由 | 非创意缺口、本不该进入本模块的问题不成立 | 回到 `Phase 1` |
| `细裁决 / Range Narrowing` | `loaded_leaf_references` / `anti_trope_mapping` / `trend_gate` | 当前模块 `Phase 2`、三个 mode-playbook 的 `Shared Dependency Contract` | 保证上层只看统一入口，但本模块内部能追踪最小读取 | 读取过多、映射错位、未授权趋势引用不成立 | 回到 `Phase 2` |
| `离散裁决 / Final Selection` | `creative_mandate_update` / `planning_seed_update` / `unknowns_update` / `sources_breakdown` | `Init/初始化简报.json`、`Init/north_star_contract.json` 的上游输入槽位 | 让创意参考真正进入 handoff，而不是停在解释层 | 仍是资料墙、来源不清或越权拍死 planning canonical 不成立 | 回到 `Phase 3` |

### 验证矩阵

> 证据优先级：`落盘扰动测试 / 字段落盘追踪 / 前后行为差异` > `近邻替换压测 / 轴权归属检查` > `遮轴名快检 / 命名解释`

| 验证维度 | 检查问题 | 证据 | 状态 | fail_code | rework_entry |
| --- | --- | --- | --- | --- | --- |
| 事实/推断分离 | 是否明确区分了观察事实、推断缺口、受保护合同和建议改写 | 本模块新增 `优化模式事实 / 推断分层` 表 | PASS |  |  |
| 模式适配性 | 当前是否真的是 `chain-optimization` 而非原生设计 | 旧版已存在三轴三重雏形，本轮是基于真实基线补硬化 | PASS |  |  |
| 遮轴名快检 | 遮掉轴名后是否仍能看到 `缺口类型 / 最小读取清单 / 槽位更新` | 三重现已直接写出关键字段，不再只剩抽象问题句 | PASS |  |  |
| 轴权归属检查 | 关键字段是否各有唯一主轴与主裁决层 | `缺口类型` 属粗裁决+方向轴，`最小读取清单` 属细裁决+优选轴，`sources_breakdown` 属离散裁决+成立轴 | PASS |  |  |
| 近邻替换压测 | 把 `最小读取清单` 换成“参考选择”、`槽位可写回性` 换成“结果合理”后是否明显变钝 | 会失去可计数、可判废和可返工的锐度 | PASS |  |  |
| 分重差异 | 三重是否分别在做判型、缩读和写回，而不是换句话说同一件事 | `判缺口`、`选叶子`、`落槽位` 已明确分层 | PASS |  |  |
| 字段落盘追踪 | 每一重是否至少能追到一个字段、步骤或槽位 | 已补 `分重字段落盘映射` 表 | PASS |  |  |
| 落盘扰动测试 | 若移除 `sources_breakdown` 或 `trend_gate`，下游是否会真实变化 | 会直接损伤 provenance 与 L3 趋势门禁 | PASS |  |  |
| 下游有效性 | 是否能指导父 `SKILL.md`、mode-playbook 与 handoff 槽位一起收敛 | 上层入口、mode 依赖、handoff 槽位三处都能回指本模块 | PASS |  |  |

### Gate Summary

- status: PASS
- fail_codes: []
- repair_entry: 若未来出现读多、乱映射或假落盘，按 `Phase 1 -> Phase 2 -> Phase 3 -> Phase 4` 返工
- unknowns:
  - 未来若 leaf references 继续增多，可能需要把叶子再拆成受治理的子参考模块
- confidence: 0.88
- smallest_safe_patch: 维持当前三轴命名不变，仅继续在新增 leaf reference 时回写 `Phase 2` 场景矩阵与验证矩阵

## 6. 验收机制

- quality standard：
  - 创意引用入口收口为单一 module route。
  - 每种创意缺口都能映射到最小读取清单与明确写回槽位。
  - 趋势资料仍是 L3 资料，不会被默认加载。
- acceptance checklist：
  - [ ] 父 `SKILL.md` 已显式声明何时进入本模块。
  - [ ] 三个 mode-playbook 都只依赖本模块入口，不再散点点名 leaf references。
  - [ ] `planning_seed / creative_mandate / unknowns` 的写回位点明确。
  - [ ] 题材到反套路映射只在本模块维护。
  - [ ] 全仓不再出现活跃 `references/creativity/` 直连路径。
- fail signal：
  - 父技能与 mode-playbook 继续各自维护 leaf reference 触发规则。
  - 趋势校准在未获用户授权时被默认读取。
  - leaf references 被当成正文资料墙写回 handoff。
- rework entry：
  - 路由问题回到 Phase 4
  - 触发判型问题回到 Phase 1
  - 叶子读取过重回到 Phase 2
  - 槽位落盘失真回到 Phase 3

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是
- 若为多模块场景，是否已有统一路由段落：是，父技能新增 `Reference Loading Guide`
- 父 `SKILL.md` 中的模块关系：三种 mode-playbook 互斥；`creative-seed-routing` 与题材/worldbuilding 为按需串行

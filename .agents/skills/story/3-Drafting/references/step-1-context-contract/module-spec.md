# Step 1 Context Contract Module Spec

## 1. 适用场景

- 上层 SKILL 语境：`3-Drafting/SKILL.md` 的 Step 1 Context Agent
- 当前模块负责对象/范围：把上游真源压缩为可直接驱动 Step 2A 的章节级执行包，并裁决开头/钩子/节奏等差异化字段
- 模块归属类型：多步骤之一
- 进入触发信号：
  - 进入 Step 1
  - Step 1 输出仍像资料罗列，没有形成 Layer A-E + 任务书 + Context Contract
  - 需要为开头类型、钩子类型、情绪节奏、信息密度做差异化判定
- 不负责项：
  - 不直接写正文
  - 不做审查或润色
  - 不替代 `Planning/8-全息地图.json`、`Cards/**`、`.webnovel/state.json`
- 与兄弟模块边界：
  - 只定义 Step 1 的执行包与差异化路由
  - 需要 craft 增强时串到 `references/writing-craft-catalog/module-spec.md`
  - 不越权改写 Step 2B / 3 / 4 / 5 的职责

## 2. 预加载上下文

- 上层必读：
  - 根 `SKILL.md`
  - 根 `CONTEXT.md`
- 本层必读：
  - 当前 `module-spec.md`
  - 当前 `CONTEXT.md`
- 模块附属 appendix：
  - `references/step-1-context-contract/appendix-context-contract.md`
  - `references/step-1-context-contract/appendix-style-variants.md`
- 条件依赖：
  - `references/writing-craft-catalog/module-spec.md`
  - `../../references/reading-power-taxonomy.md`
  - `../../references/genre-profiles.md`
- 加载顺序：根 `SKILL.md` -> 根 `CONTEXT.md` -> 当前 `module-spec.md` -> 当前 `CONTEXT.md` -> 条件命中时再读 appendix / craft 模块
- 冲突优先级：用户显式请求 > `AGENTS.md` / 元规则 > 根 `SKILL.md` > 当前 `module-spec.md` > 当前 `CONTEXT.md` > appendix
- 默认不并入的上下文：不整包回读 `0-Init` 问卷、全量 `Cards/**`、全量 planning 证据层

## 3. 思维链

### Think-Think Design Snapshot

- mode: `思维链优化设计`
- task_essence:
  - 本模块真正要把 `上游分层真源` 从 `材料集合` 推到 `Step 2A 可直接消费的章节执行包`
- baseline_symptom:
  - 仅写了“三轴/三重”标题，但没有把 Step 1 真实裁决字段压到 `执行包骨架 / 冲突优先级 / 差异化路由`

### 观察到的事实 / 推断出的缺口

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | Step 1 必须输出 Layer A-E、7 板块任务书、Context Contract 与直写提示词 | 根 `SKILL.md` Step 1 合同 | 把这些提升为粗裁决的候选边界字段 |
| `Observed Facts` | 差异化只允许在真源压缩完成后发生 | 根 `SKILL.md` 与本模块 Phase 3 | 把差异化路由下沉到离散裁决 |
| `Inferred Gaps` | 之前的“执行包成形对齐”仍偏轴名，缺少驱动/判废/对比字段 | 旧快照没有字段矩阵 | 补字段矩阵与唯一轴权 |
| `Protected Constraints` | 不能让 variation / craft 反客为主改写章节真源 | 根 `SKILL.md` 与 `AGENTS.md` | 把它写入成立轴判废字段 |
| `Proposed Rewrite` | 用“执行包骨架 -> 真源优先级 -> 差异化路由”三层字段重写 | think-think 优化模式 | 已写入本模块矩阵与验证表 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | `执行包成形对齐` | Step 1 输出是否真正服务 Step 2A 直写，而不是停留在资料清单 | Layer A-E、7 板块任务书、Context Contract |
| `成立轴` | `真源压缩成立` | 上游约束、章节编排、运行态与对象切片是否彼此一致且无越权篡改 | 冲突优先级、差异化检查、题材命中路由 |
| `优选轴` | `差异化收益比` | 在都成立的执行包里，哪种开头/钩子/节奏选择更能避重和提高追读力 | `references/step-1-context-contract/appendix-style-variants.md` 与题材 hook 路由 |

### 轴角色字段化

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 唯一主轴说明 |
| --- | --- | --- | --- | --- |
| `执行包成形对齐` | `Layer A-E 完整度`、`7 板块任务书齐全度`、`Context Contract 字段覆盖` | 输出仍是原文摘抄、缺少直写提示词、缺失本章功能字段 | 执行包压缩比、Step 2A 直写可用度 | 只由方向轴决定“这是不是合格执行包” |
| `真源压缩成立` | `holomap 章节板块绑定`、`state 承接闭合`、`对象切片相关性` | 用全量问卷/全量 cards 冒充执行包、差异化覆盖真源、过渡章按字数判定 | 真源冲突数量、指导项与硬约束分离度 | 只由成立轴拥有“过线不过线”解释权 |
| `差异化收益比` | `开头类型重复风险`、`钩子类型重复风险`、`题材 hook 命中收益` | 为求花样而改写剧情、进入 craft 无明确症状、重复风险未审查 | 追读力增益、避重收益、加载成本 | 只由优选轴比较“哪种差异化更值” |

### 三重

| 裁决层 | 本层关键问题 | 本模块产物 |
| --- | --- | --- |
| `粗裁决 / Base Range` | 当前章先需要哪些 Layer A-E 与任务书字段才能开写 | 章节级执行包骨架 |
| `细裁决 / Range Narrowing` | 哪些字段来自真源、哪些只是指导项，冲突时谁优先 | Context Contract 与冲突处理规则 |
| `离散裁决 / Final Selection` | 开头/钩子/节奏/题材 hook 如何在可行方案里做差异化选择 | variation 路由与 craft 升级入口 |

### 分重关键向字段矩阵

| 裁决层 | 驱动字段 | 判废字段 | 对比字段 | 为什么这些才是“向” |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `layer_bundle_presence`、`task_brief_presence`、`context_contract_presence` | `missing_layer_block`、`missing_task_brief`、`missing_context_contract` | `draft_readiness` | 直接改变“当前能不能进入起草”的候选范围 |
| `细裁决 / Range Narrowing` | `source_priority_order`、`board_to_state_alignment`、`slice_relevance` | `truth_source_override`、`transition_by_wordcount`、`full_dump_leak` | `constraint_clarity` | 负责把“看似完整但不成立”的执行包筛掉 |
| `离散裁决 / Final Selection` | `opening_repeat_risk`、`hook_repeat_risk`、`genre_hint_match` | `style_variation_without_reason`、`craft_overload` | `reader_pull_gain` | 只在成立执行包里比较哪种差异化最划算 |

### 字段落盘映射

| 裁决层 | 服务槽位 / 步骤 | 具体落点 | 采用理由 | 失败返工入口 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | Step 1 输出骨架 | `Layer A-E + 7 板块任务书 + Context Contract + 直写提示词` | 让 Step 2A 拿到单一执行包而非散料 | 回到 Phase 1 |
| `细裁决 / Range Narrowing` | `Context Contract` 与冲突处理 | 目标/阻力/代价/过渡章判定/追读力设计 | 让真源与指导项的优先级真正落盘 | 回到 Phase 2 |
| `离散裁决 / Final Selection` | `loaded_references` / `variation note` | Step 1 的差异化路由记录 | 让“为什么进入 craft”可追溯 | 回到 Phase 3 |

### 验证矩阵

| 验证项 | 结论标准 | 当前落点 | 失败返工入口 |
| --- | --- | --- | --- |
| `遮轴名快检` | 遮掉轴名后仍能看出“执行包骨架 / 真源优先级 / 差异化路由”三层字段 | Step 1 输出结构与路由记录 | 回到字段矩阵 |
| `轴权归属检查` | `过线/不过线` 只由成立轴解释，优选轴不越权 veto | `source_priority_order` / `truth_source_override` | 回到轴角色字段化 |
| `近邻替换压测` | 若把 `opening_repeat_risk` 替换成泛词“更有新意”，裁决力明显下降 | variation 判定 | 回到离散裁决 |
| `落盘扰动测试` | 移除 `Context Contract` 或 `loaded_references` 时，Step 2A / craft 路由立即失稳 | Step 1 直写包与路由记录 | 回到落盘映射 |

### 快照落点说明

- 思维链如何作用于执行流程：先锁执行包骨架，再做差异化判定，最后才按需调用 craft 模块
- 思维链如何作用于交付：交付物必须是 Step 2A 可消费的执行包，而不是单独的参考笔记
- 思维链如何作用于验收：若输出缺少 Layer A-E、任务书或 Context Contract 任一块，直接判失败

## 4. 执行流程

### Phase 1 真源收束

- 目标：把 Layer A-E 与 7 板块任务书的必填槽位收齐
- 输入：`Planning/8-全息地图.json`、`.webnovel/state.json`、最近摘要、相关对象切片
- 动作：按根 `SKILL.md` 的五层加载矩阵压缩上游材料
- 产出：章节级执行包初稿
- 失败信号 / 返工入口：仍出现“全库罗列”或缺少本章功能字段，返工到 Step 1 上游输入裁剪

### Phase 2 合同定稿

- 目标：把执行包定稿为 Step 2A 可消费的 Context Contract
- 输入：章节级执行包初稿、`references/step-1-context-contract/appendix-context-contract.md`
- 动作：补齐目标/阻力/代价/本章变化/未闭合问题/开头类型/情绪节奏/信息密度/过渡章判定/追读力设计
- 产出：Context Contract + 直写提示词
- 失败信号 / 返工入口：字段缺失、过渡章判定偷用字数阈值、直写提示词无法直接驱动 Step 2A

### Phase 3 差异化路由

- 目标：只在必要时做开头/钩子/题材 craft 强化
- 输入：`references/step-1-context-contract/appendix-style-variants.md`、条件命中的题材 / craft 信号
- 动作：先做重复风险检查，再按需进入 `references/writing-craft-catalog/module-spec.md`
- 产出：差异化后的执行包与所用 craft 路由记录
- 失败信号 / 返工入口：为了追差异化而改写剧情真源，或根本没说明为何进入 craft 模块

## 5. 交付

- 类型：非内容输出型
- 模式：生成 Step 2A 可直接消费的章节级执行包
- 正式落点：Step 1 输出、`.webnovel/workflow_state` 的当前 step 产物、必要时 review routing note
- 上层消费方式：Step 2A 直接读取执行包，不再拆额外中间步骤
- 若为内容输出型，输出模板/字段骨架：N/A
- 若为非内容输出型，执行模式/状态推进方式：记录本轮是否进入 variation / craft catalog，以及理由

## 6. 验收机制

- quality standard：
  - 输出同时具备 Layer A-E、7 板块任务书、Context Contract、直写提示词
  - 差异化选择有据可查，不靠拍脑袋
  - 题材或 craft 命中时，路由记录能说明为何进入 `writing-craft-catalog`
- acceptance checklist：
  - [ ] 没有整包灌入 Init/Cards/Planning 原文
  - [ ] 执行包可直接驱动 Step 2A
  - [ ] 开头/钩子/节奏的差异化已做重复风险检查
  - [ ] 过渡章判定遵循规划节点而非字数阈值
- fail signal：执行包仍停留在资料堆砌、缺少 Context Contract 字段、或差异化判断与真源冲突
- rework entry：回到 Step 1 的输入裁剪与合同定稿

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是
- 若为多模块场景，是否已有统一路由段落：是，见根 `SKILL.md` 的 `Reference Loading Guide`
- 父 `SKILL.md` 中的模块关系：Step 型串行；`writing-craft-catalog` 为按需二级路由

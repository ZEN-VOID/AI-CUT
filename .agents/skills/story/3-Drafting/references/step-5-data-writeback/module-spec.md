# Step 5 Data Writeback Module Spec

## 1. 适用场景

- 上层 SKILL 语境：`3-Drafting/SKILL.md` 的 Step 5 Data Agent
- 当前模块负责对象/范围：在章节正文与审查分数已经就绪后，完成状态、索引、摘要、scene 与可选债务利息的正式写回
- 模块归属类型：多步骤之一
- 进入触发信号：
  - 进入 Step 5
  - 需要把 `state.json`、`index.db`、`summaries/` 与观测日志闭环
  - 需要决定是否执行债务利息
- 不负责项：
  - 不回滚 Step 1-4
  - 不重写正文
  - 不替代 Data Agent 的核心 A-H 子步骤
- 与兄弟模块边界：
  - 只消费 Step 4 结果
  - 通过最小失败隔离保护前序步骤

## 2. 预加载上下文

- 上层必读：
  - 根 `SKILL.md`
  - 根 `CONTEXT.md`
- 本层必读：
  - 当前 `module-spec.md`
  - 当前 `CONTEXT.md`
- 模块附属 appendix：
  - `references/step-5-data-writeback/appendix-debt-switch.md`
- 条件依赖：
  - `data-agent` 默认子步骤合同
- 加载顺序：根 `SKILL.md` -> 根 `CONTEXT.md` -> 当前 `module-spec.md` -> 当前 `CONTEXT.md` -> appendix
- 冲突优先级：用户显式请求 > `AGENTS.md` / 元规则 > 根 `SKILL.md` > 当前 `module-spec.md` > 当前 `CONTEXT.md` > appendix
- 默认不并入的上下文：不把 Step 5 的子步骤失败扩散为整条写作链重跑

## 3. 思维链

### Think-Think Design Snapshot

- mode: `思维链优化设计`
- task_essence:
  - 本模块真正要把 `已完成正文 + 审查结果` 从 `单次产物` 推到 `可被后续章节与检索系统消费的正式状态`
- baseline_symptom:
  - 旧快照能讲“写回 / 隔离 / 副作用”，但没有把“哪些是硬写回、哪些是可选副作用、哪些失败只能局部补跑”压到独立字段

### 观察到的事实 / 推断出的缺口

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | `state.json`、`index.db`、summary 是最小白名单 | 根 `SKILL.md` Step 5 | 升成粗裁决字段 |
| `Observed Facts` | G/H/I 子步骤失败不应拖整链回滚 | 根 `SKILL.md` 失败隔离规则 | 升成成立轴判废字段 |
| `Inferred Gaps` | 债务利息、style extract、RAG 之前只是“可选动作”，没有明确收益边界 | 旧快照只写“可选副作用” | 补优选轴字段 |
| `Protected Constraints` | Step 5 不能回流改写 Step 1-4 | 工作流顺序 | 写入判废字段 |
| `Proposed Rewrite` | 用“硬写回对象 -> 失败隔离 -> 可选副作用开关”三层字段重写 | think-think 优化模式 | 已写入矩阵与验证表 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | `正式写回闭环对齐` | 当前是不是在完成状态与索引写回，而不是继续创作 | A-E 核心写回与验证 |
| `成立轴` | `写回完整性成立` | state/index/summary/scene/观测日志是否闭环，失败是否被正确隔离 | 最小白名单与失败隔离规则 |
| `优选轴` | `可选副作用收益比` | 债务利息、style extract、RAG 子步骤何时值得开启 | I/H/G 的条件执行 |

### 轴角色字段化

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 唯一主轴说明 |
| --- | --- | --- | --- | --- |
| `正式写回闭环对齐` | `state_write_needed`、`index_write_needed`、`summary_write_needed` | `writeback_skipped`、`artifacts_missing` | `core_completion_ratio` | 只由方向轴决定“哪些产物必须写” |
| `写回完整性成立` | `artifact_whitelist_pass`、`scene_fallback_available`、`substep_isolation_rule` | `core_write_fail`、`full_chain_rerun`、`invalid_scene_payload` | `recovery_locality` | 只由成立轴决定“失败是否被正确隔离” |
| `可选副作用收益比` | `rag_value`、`style_extract_value`、`debt_interest_value` | `default_side_effect_on`、`side_effect_without_signal` | `benefit_vs_cost` | 只由优选轴决定“哪些副作用值得开” |

### 三重

| 裁决层 | 本层关键问题 | 本模块产物 |
| --- | --- | --- |
| `粗裁决 / Base Range` | 本轮 Step 5 的硬写回对象有哪些 | state/index/summary 白名单 |
| `细裁决 / Range Narrowing` | 哪些失败只该局部重跑 | 失败隔离规则 |
| `离散裁决 / Final Selection` | 哪些可选副作用该执行、哪些保持关闭 | debt switch / style extract / RAG 路由 |

### 分重关键向字段矩阵

| 裁决层 | 驱动字段 | 判废字段 | 对比字段 | 为什么这些才是“向” |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `state_write_needed`、`index_write_needed`、`summary_write_needed` | `artifact_missing` | `writeback_scope` | 先决定这轮有哪些正式产物必须生成 |
| `细裁决 / Range Narrowing` | `artifact_whitelist_pass`、`scene_fallback_available`、`substep_isolation_rule` | `core_write_fail`、`rerun_whole_chain` | `repair_locality` | 负责把“看似完成但恢复策略错误”的方案筛掉 |
| `离散裁决 / Final Selection` | `rag_value`、`style_extract_value`、`debt_interest_value` | `default_side_effect_on`、`unjustified_side_effect` | `benefit_vs_cost` | 真正决定哪些副作用执行、哪些保持关闭 |

### 字段落盘映射

| 裁决层 | 服务槽位 / 步骤 | 具体落点 | 采用理由 | 失败返工入口 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | Step 5 白名单检查 | `state.json`、`index.db`、summary | 让硬写回对象可验证 | 回到 Phase 1 |
| `细裁决 / Range Narrowing` | 失败隔离日志 / scene fallback | Step 5 子步骤判定 | 让局部补跑而非整链回滚 | 回到 Phase 2 |
| `离散裁决 / Final Selection` | `debt_interest` / `style extract` / `rag index` 状态 | Step 5 执行摘要 | 让可选副作用有正式开关记录 | 回到 Phase 2 |

### 验证矩阵

| 验证项 | 结论标准 | 当前落点 | 失败返工入口 |
| --- | --- | --- | --- |
| `遮轴名快检` | 去掉轴名后仍能看出“必须写什么 / 出错怎么局部补 / 哪些副作用值得开” | 白名单、隔离、执行摘要 | 回到字段矩阵 |
| `轴权归属检查` | 债务利息是否开启只能由优选轴比较，不得由成立轴偷开 | `debt_interest_value` | 回到轴角色字段化 |
| `近邻替换压测` | 把 `benefit_vs_cost` 换成泛词“顺便做了”后，副作用选择明显失真 | 离散裁决对比字段 | 回到优选轴 |
| `落盘扰动测试` | 去掉白名单或隔离规则时，Step 5 立即失去可验收性 | 核心写回与隔离日志 | 回到落盘映射 |

### 快照落点说明

- 思维链如何作用于执行流程：先做核心写回，再处理可选副作用，最后验收
- 思维链如何作用于交付：输出的是可被后续章节消费的 state/index/summaries，而不是“处理完了”的口头声明
- 思维链如何作用于验收：若白名单产物缺失，不得结束流程

## 4. 执行流程

### Phase 1 核心写回

- 目标：完成 A-E 核心写回与最小白名单校验
- 输入：章节文件、`overall_score`、project_root、state/index 当前状态
- 动作：写入 state/index/summary
- 产出：最新 `.webnovel/state.json`、`.webnovel/index.db`、`.webnovel/summaries/ch{chapter_padded}.md`
- 失败信号 / 返工入口：核心白名单缺失或不可读

### Phase 2 可选副作用判定

- 目标：决定 scenes、RAG、style extract、debt interest 是否执行
- 输入：scene 数据、review score、`references/step-5-data-writeback/appendix-debt-switch.md`
- 动作：按条件执行 G/H/I，并记录跳过原因
- 产出：scene 索引、向量索引、style sample、`debt_interest` 状态
- 失败信号 / 返工入口：把可选子步骤失败误判成整链失败

### Phase 3 验收与观测

- 目标：读取 timing 日志并给出 Step 5 放行结论
- 输入：`data_agent_timing.jsonl`、call trace、白名单产物
- 动作：校验性能与产物完整性
- 产出：Step 5 验收结论
- 失败信号 / 返工入口：白名单缺失、scene 为空但未做退化处理、观测结论缺失

## 5. 交付

- 类型：非内容输出型
- 模式：状态推进与正式写回
- 正式落点：`.webnovel/state.json`、`.webnovel/index.db`、`.webnovel/summaries/`、观测日志、可选 debt note
- 上层消费方式：下一章 Context Agent 与 query/review/loopback 读取这些正式产物
- 若为内容输出型，输出模板/字段骨架：N/A
- 若为非内容输出型，执行模式/状态推进方式：记录哪些子步骤执行、哪些跳过、为什么

## 6. 验收机制

- quality standard：
  - 最小白名单存在且内容可读
  - 可选子步骤的执行/跳过均有理由
  - Step 5 失败不会误伤前序步骤
- acceptance checklist：
  - [ ] `state.json`、`index.db`、summary 文件齐全
  - [ ] performance / timing 结论已输出
  - [ ] debt switch 判定明确
  - [ ] scene 缺失时已做合法退化
- fail signal：核心写回缺失、债务利息默认被误开、或可选子步骤失败导致整链回滚
- rework entry：回到对应子步骤局部补跑

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是
- 若为多模块场景，是否已有统一路由段落：是
- 父 `SKILL.md` 中的模块关系：Step 5 专属，串行位于 Step 4 之后

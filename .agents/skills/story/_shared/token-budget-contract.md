# Token Budget Management Contract

本文件是 `story2026` 的上下文加载 Token 预算管理合同。它定义了三级加载模式及其预算上限，确保在超长篇小说创作（数十卷、数百章）中，关键信息的上下文加载既有优先级、又不超出 token 窗口。

本文件不拥有正文写权，不是独立阶段。预算策略供所有创作阶段的 `Context Loading Contract` 引用。

## Core Principle

上下文窗口是有限资源。Token 预算管理的核心不是"加载更多"，而是"用更少的 token 承载更多的有效信息"。原则：

1. **结构化摘要 > 原文全文**：planning 摘要、验收包、人物状态快照优先于原文加载
2. **增量追加 > 全量加载**：只加载变化部分，不重复加载历史稳定数据
3. **按需加载 > 预加载**：只在触发条件满足时加载扩展层/参考层
4. **话题缓存 > 重复加载**：同一话题/对象在同一 session 中只加载一次

## Three-Tier Loading Model

```
第一层：核心层（CORE）
├── 必加载，每次任务
├── 预算上限：项目总量的 40%
└── 内容：planning 摘要 + north_star + 当前章/卷关键数据 + MEMORY/CONTEXT

第二层：扩展层（EXTENDED）
├── 按需加载，触发条件满足时
├── 预算上限：项目总量的 30%
└── 内容：对象卡 + 关系图谱 + 共享合同 + 上一章/卷完整验收包

第三层：参考层（REFERENCE）
├── 仅在触发条件满足时加载
├── 预算上限：项目总量的 20%
└── 内容：题材包 + 知识库 + 经验层 + CHANGELOG + 非当前卷数据

保留：10% 余量用于上下文波动和对话交互
```

## Budget Allocation by Stage

### 3-初稿（每章）

| 层级 | 预算 | 内容 | 触发条件 |
|------|------|------|----------|
| 核心层 | ≤8K tokens | `3-初稿/CONTEXT.md`、项目 `MEMORY.md`、项目 `CONTEXT/`（相关性过滤）、`north_star.yaml`、本章 planning、前章 acceptance 摘要、`_shared/context-loading-contract.md` | 每次 |
| 扩展层 | ≤5K tokens | 出场人物角色卡摘要（非全文）、`character-continuity-contract.md` 出场人物部分、`_shared/chapter-rhythm-handoff-contract.md`（节奏义务段位）、前章完整验收包 | 前章验收有薄弱维度 或 人物反应/类型化场面命中 |
| 参考层 | ≤3K tokens | 当前卷跨卷追踪数据、题材包（按 north_star.genre_contract 路由）、`_shared/ai-feature-detection-checklist.md`（验收时）、`knowledge-base/creative-draft-heuristics.md` | 触发对应 module 时 |
| **合计上限** | **≤16K tokens** | | |

### 4-润色（每章）

| 层级 | 预算 | 内容 | 触发条件 |
|------|------|------|----------|
| 核心层 | ≤8K tokens | `4-润色/CONTEXT.md`、`3-初稿` 源章（完整）、项目 `MEMORY.md`、`north_star.yaml`、本章 planning 摘要、前章润色验收摘要、`_shared/context-loading-contract.md` | 每次 |
| 扩展层 | ≤5K tokens | 出场人物角色卡摘要、`_shared/ai-feature-detection-checklist.md`、`_shared/genre-scene-strengthening-contract.md`（命中类型化场面时）、出场人物追踪数据 | 命中对应修复类型 |
| 参考层 | ≤3K tokens | 题材包、`knowledge-base/polishing-heuristics.md`、`types/` 对应修复类型文件、跨卷追踪数据（卷首章） | 触发对应 module 时 |
| **合计上限** | **≤16K tokens** | | |

### 2-卷章/3-章级

| 层级 | 预算 | 内容 |
|------|------|------|
| 核心层 | ≤10K tokens | 项目 CONTEXT/、卷规划、卷内已规划章摘要、`_shared/chapter-rhythm-handoff-contract.md` |
| 扩展层 | ≤6K tokens | 出场人物/场景/物品卡摘要、前卷规划摘要 |
| 参考层 | ≤4K tokens | 题材包、知识库 |
| **合计上限** | **≤20K tokens** | |

### return

| 层级 | 预算 | 内容 |
|------|------|------|
| 核心层 | ≤6K tokens | 当前卷验收聚合数据、项目 MEMORY.md |
| 扩展层 | ≤4K tokens | 跨卷追踪数据（增量写入） |
| 参考层 | ≤2K tokens | 不适用时 N/A |
| **合计上限** | **≤12K tokens** | |

## Budget Enforcement Rules

### 1. 摘要化规则

以下内容在加载时必须摘要化，不得全文加载：

| 原始内容 | 摘要化方式 | 摘要预算 |
|----------|-----------|----------|
| 人物角色卡 | 提取当前卷出场角色的核心字段（姓名/身份/关系/当前状态/关键能力） | ≤200 tokens/角色 |
| 场景卡 | 提取当前卷涉及场景的核心字段（名称/功能/位置/当前状态） | ≤100 tokens/场景 |
| 物品卡 | 提取当前卷涉及物品的核心字段（名称/归属/当前状态/能力） | ≤80 tokens/物品 |
| 前章验收包 | 提取 `dimension_scores` + `critical_issues` + `rework_targets` | ≤300 tokens/章 |
| 卷规划 | 提取卷级义务、Strand 分布、关键节点 | ≤500 tokens/卷 |
| 跨卷追踪 | 提取当前卷相关的人物状态快照 + 未兑现伏笔 | ≤400 tokens/卷 |
| 题材包 | 提取当前章命中的题材特化规则 | ≤300 tokens |

### 2. 优先级裁剪规则

当核心层预估超出预算上限时，按以下优先级裁剪：

1. **不可裁剪**：north_star.yaml、当前任务入口文件（SKILL.md/CONTEXT.md）、本章 planning
2. **高优先（优先保留）**：项目 MEMORY.md、前章验收摘要、出场人物摘要
3. **中优先（可裁到摘要）**：项目 CONTEXT/（取最近 3 条关键决策）、共享合同（只取触发部分）
4. **低优先（可跳过）**：CHANGELOG.md、非当前卷历史数据、知识库

### 3. 重复加载防护

同一 session 中：
- 同一文件只加载一次，后续引用使用缓存摘要
- north_star.yaml 只加载一次，后续使用内存引用
- 项目 MEMORY.md 和 CONTEXT/ 只加载一次
- 共享合同按需增量加载（只加载新触发的部分）

### 4. 预算溢出处理

| 溢出情况 | 处理方式 |
|----------|----------|
| 核心层超预算 ≤20% | 执行任务，但记录超预算警告 |
| 核心层超预算 >20% | 启动裁剪流程，回收至预算上限内 |
| 核心+扩展层合计超预算 | 裁剪扩展层，只保留核心层 |
| 核心层经最大化裁剪后仍超预算 | 阻断任务，报告需要人工缩减输入 |

## Integration with Context Loading Contract

`_shared/context-loading-contract.md` 中的三级加载模式（`full` / `incremental` / `minimal`）与本合同的关系：

| Context Loading Mode | Token Budget 层级 | 说明 |
|---------------------|-------------------|------|
| `full` | 核心层 + 扩展层 + 参考层 | 卷首章、新卷第一工作时 |
| `incremental` | 核心层 + 扩展层（按需） | 同卷内后续章，已有上下文缓存 |
| `minimal` | 核心层（摘要化） | 卫星技能调用、dry_run、query |

## Stage Integration

| 阶段 | 加载位置 | 预算检查点 |
|------|----------|-----------|
| 0-初始化 | Context Loading Contract | 输入检查 |
| 1-设定 | Context Loading Contract | 对象生成前 |
| 2-卷章/1-部级 | Context Loading Contract | 规划前 |
| 2-卷章/2-卷级 | Context Loading Contract | 规划前 |
| 2-卷章/3-章级 | Context Loading Contract | 规划前 |
| 3-初稿 | N2-CONTEXT-PACK 节点 | 上下文加载后、正文创作前 |
| 4-润色 | P2-CONTEXT-PACK 节点 | 上下文加载后、润色前 |
| query | Context Loading Contract | 查询执行前 |
| resume | Context Loading Contract | 续写前 |
| return | Context Loading Contract | 回流前 |
| repair | Context Loading Contract | 诊断前 |

## Monitoring

每个阶段的执行报告中应包含 token 预算使用记录：

```yaml
token_budget:
  total_limit: 16000
  core_used: 7200
  extended_used: 3800
  reference_used: 1200
  total_used: 12200
  overflow: false
  warnings: []
  cuts:  # 裁剪记录
    - item: "人物角色卡-配角C"
      reason: "配角C 本章无出场"
      tokens_saved: 180
```

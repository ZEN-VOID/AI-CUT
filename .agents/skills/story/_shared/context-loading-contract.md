# Context Loading Contract

跨阶段共享的上下文加载合同。

## Canonical Rules

- `story` 体系不再依赖根级 `references/` 目录。
- 跨阶段共享合同优先落在根级 `_shared/`。
- 阶段专属共享合同优先落在各阶段自己的 `_shared/`。
- `SKILL.md + CONTEXT.md + 选中的 types/ 类型包` 是每个阶段的默认入口；`_shared/*.md` 只承载跨阶段复用的稳定合同。

## Loading Order

1. 根 `AGENTS.md`
2. 根 `story/SKILL.md + CONTEXT.md`
3. 识别并加载根 `types/` 中选中的类型包（单选或多选）
4. 当前阶段 `SKILL.md + CONTEXT.md`
5. 识别并加载当前阶段 `types/` 中选中的类型包（单选或多选）
6. 命中的根级 `_shared/` 合同
7. 命中的阶段 `_shared/` 合同
8. 当前阶段私有 `references/` / `templates/` / `scripts/`

## Cross-Volume Loading Strategy

当项目已有多卷完成时，遵循以下跨卷上下文加载策略：

1. **卷首章**（新卷首章起草/续写）：必须加载所有已完成卷的 `CONTEXT/volume-状态摘要/第V卷-状态.md`，仅消费每个摘要中的"伏笔变动"和"人物状态变化"段，不加载完整文件。
2. **卷中章**（卷内第2章起）：沿用当前卷前序章连续性桥接，可选加载本卷状态摘要。
3. **上下文控制**：跨卷状态摘要总字数控制在 5000-15000 字以内（10卷长篇）。超出时按卷号倒序优先加载最近2-3卷。
4. `return` 阶段在 actualization 完成后，按 `cross-volume-continuity-contract.md` 自动生成当前卷的状态摘要。

## Token Budget Integration

所有阶段的上下文加载必须遵守 `_shared/token-budget-contract.md` 的三级加载模式和预算上限：

### 加载模式选择

| 场景 | 预算模式 | 层级 |
|------|----------|------|
| 卷首章（新卷第一章） | `full` | 核心层 + 扩展层 + 参考层 |
| 卷中章（同卷后续章） | `incremental` | 核心层 + 扩展层（按需） |
| 卫星技能（query/resume/repair） | `minimal` | 核心层（摘要化） |
| return 回流 | `minimal` | 核心层（摘要化） |

### 摘要化要求

加载以下内容时必须使用结构化摘要，不允许全文加载：
- 人物角色卡 → 出场角色核心字段摘要
- 前章验收包 → `dimension_scores` + `critical_issues`
- 跨卷追踪数据 → 当前卷相关的人物状态快照

### 预算溢出防护

当核心层预估超出 `token-budget-contract.md` 规定的上限时：
1. 启动优先级裁剪（north_star/planning 不可裁，MEMORY/CONTEXT 优先保留，CHANGELOG/知识库可跳过）
2. 若最大化裁剪后仍超预算，阻断并报告需要人工缩减输入
5. 跨卷追踪的具体维度和格式见 `_shared/cross-volume-continuity-contract.md`。

## Loading Modes

根据任务类型选择加载模式，以控制 token 消耗：

| mode | 适用场景 | planning 加载 | 对象卡加载 | 前文加载 | 题材包加载 |
| --- | --- | --- | --- | --- | --- |
| `standard` | 正式起草/续写/重写 | 三层全部 | 全部 | 当前卷前序+跨卷状态摘要 | 按需全量 |
| `light` | 局部修复/dry_run/诊断 | 卷级+章级 | 当前出场人物 | 上一章+跨卷状态摘要 | 按需精简 |
| `emergency` | 查询/状态检查/续跑 | 仅整体规划 | 仅摘要 | 跨卷状态摘要（最近3卷） | 不加载 |

各阶段 SKILL.md 的 Context Loading Contract 应声明支持的模式。

## Hard Gates

- 不得把阶段私有 `references/` 冒充成跨阶段共享真源。
- 不得把 `knowledge-base/` 当作每次固定加载的类型包；题材、阶段、任务模式等固定上下文必须落在 `types/` 并由 `type-map` 或 route profile 选择。
- 若某 shared contract 被 2 个以上阶段复用，应优先提升到 `_shared/` 而不是复制到兄弟目录。
- legacy `story2026` 路径只允许作为兼容 fallback，不再是 canonical source。
- 跨卷状态摘要不得替代角色卡/planning 作为真源；它是对已完成卷的事实总结，不是创作指令。

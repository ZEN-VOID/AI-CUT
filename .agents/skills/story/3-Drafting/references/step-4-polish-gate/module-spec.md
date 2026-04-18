# Step 4 Polish Gate Module Spec

## 1. 适用场景

- 上层 SKILL 语境：`3-Drafting/SKILL.md` 的 Step 4 正式润色位
- 当前模块负责对象/范围：根据审查问题包修正文稿，并完成 Anti-AI、No-Poison 与移动端排版终检
- 模块归属类型：多步骤之一
- 进入触发信号：
  - 进入 Step 4
  - 已取得 Step 3 聚合结果
  - 需要修复 `critical/high`、输出 deviation、完成 `anti_ai_force_check`
- 不负责项：
  - 不直接改规划真源
  - 不把 Step 4 用成剧情重写入口
  - 不吞掉 Step 5 的写回责任
- 与兄弟模块边界：
  - 上游依赖 `step-3-review-gate`
  - 下游交给 `step-5-data-writeback`
  - craft 专项与排版辅助通过 `writing-craft-catalog` 进入

## 2. 预加载上下文

- 上层必读：
  - 根 `SKILL.md`
  - 根 `CONTEXT.md`
- 本层必读：
  - 当前 `module-spec.md`
  - 当前 `CONTEXT.md`
- 模块附属 appendix：
  - `references/step-4-polish-gate/appendix-polish-guide.md`
- 条件依赖：
  - `references/writing-craft-catalog/module-spec.md`
- 加载顺序：根 `SKILL.md` -> 根 `CONTEXT.md` -> 当前 `module-spec.md` -> 当前 `CONTEXT.md` -> appendix -> craft 模块
- 冲突优先级：用户显式请求 > `AGENTS.md` / 元规则 > 根 `SKILL.md` > 当前 `module-spec.md` > 当前 `CONTEXT.md` > appendix / craft notes
- 默认不并入的上下文：不在本模块中重新裁决章节规划或世界规则

## 3. 思维链

### Think-Think Design Snapshot

- mode: `思维链优化设计`
- task_essence:
  - 本模块真正要把 `审查问题包 + 章节正文` 从 `待修状态` 推到 `可放行给 Step 5 的终稿`
- baseline_symptom:
  - 旧快照能说“按 severity 修”，但还没有把“什么属于问题修复、什么属于越权重写、什么构成放行”压到硬字段

### 观察到的事实 / 推断出的缺口

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | Step 4 只能修问题，不能重写规划真源 | 根 `SKILL.md` 与 `appendix-polish-guide.md` | 提升为成立轴判废字段 |
| `Observed Facts` | `anti_ai_force_check=pass` 是进入 Step 5 的硬门槛 | 根 `SKILL.md` | 提升为离散裁决放行字段 |
| `Inferred Gaps` | 之前没有明确把 craft / typesetting 放在“终检辅助”而不是“主修复逻辑” | 旧快照只提到 craft 可进入 | 收缩优选轴权限 |
| `Protected Constraints` | `critical` 必修、`high` 不修需 deviation | appendix 与根合同 | 写入方向轴和落盘映射 |
| `Proposed Rewrite` | 用“问题优先级 -> 合法修法 -> 放行终检”三层字段重写 | think-think 优化模式 | 已写入矩阵与验证表 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | `问题修复优先级对齐` | 当前修的是审查问题，而不是另起一轮改写冲动 | `critical/high` 修复顺序 |
| `成立轴` | `终检闸门成立` | Anti-AI、No-Poison、排版终检是否真正过线 | `anti_ai_force_check`、deviation、typesetting |
| `优选轴` | `最小必要改动收益比` | 在多种修法里，哪种最能修问题且最少损伤原文已有优点 | 最小必要修改策略 |

### 轴角色字段化

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 唯一主轴说明 |
| --- | --- | --- | --- | --- |
| `问题修复优先级对齐` | `critical_issue_count`、`high_issue_count`、`issue_type_cluster` | `severity_ignored`、`rewrite_from_blank` | `repair_order_efficiency` | 只由方向轴决定“先修什么” |
| `终检闸门成立` | `anti_ai_force_check`、`deviation_recorded`、`fact_layer_conflict_count` | `critical_unfixed`、`anti_ai_fail`、`truth_source_conflict` | `step5_entry_readiness` | 只由成立轴决定“能不能放行” |
| `最小必要改动收益比` | `retained_strengths`、`repair_cost`、`craft_support_gain` | `over_editing`、`style_overreach` | `repair_gain_per_change` | 只由优选轴比较哪种修法更值 |

### 三重

| 裁决层 | 本层关键问题 | 本模块产物 |
| --- | --- | --- |
| `粗裁决 / Base Range` | 当前有哪些问题必须修、哪些可择优 | 修复优先级清单 |
| `细裁决 / Range Narrowing` | 哪种修法能过线且不越权改剧情 | 修复动作与 deviation |
| `离散裁决 / Final Selection` | 终稿是否足够进入 Step 5 | 润色后正文、变更摘要、`anti_ai_force_check` |

### 分重关键向字段矩阵

| 裁决层 | 驱动字段 | 判废字段 | 对比字段 | 为什么这些才是“向” |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `critical_issue_count`、`high_issue_count`、`issue_cluster` | `severity_skipped` | `repair_scope` | 先改变“当前修复范围”的候选空间 |
| `细裁决 / Range Narrowing` | `repair_action_type`、`deviation_recorded`、`fact_layer_conflict_count` | `plot_rewrite`、`new_setting_conflict`、`anti_ai_fail_pending` | `damage_control_score` | 把“看似修了但越权”的方案筛掉 |
| `离散裁决 / Final Selection` | `anti_ai_force_check`、`typesetting_pass`、`step5_entry_readiness` | `critical_unfixed`、`gate_fail` | `final_release_confidence` | 真正决定能否进入 Step 5 |

### 字段落盘映射

| 裁决层 | 服务槽位 / 步骤 | 具体落点 | 采用理由 | 失败返工入口 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | 修复任务清单 | Step 4 修复顺序 | 让 severity 优先级可执行 | 回到 Phase 1 |
| `细裁决 / Range Narrowing` | deviation / 修复项说明 | 变更摘要 | 让“没修/不能修”有正式落点 | 回到 Phase 2 |
| `离散裁决 / Final Selection` | `anti_ai_force_check` / 终稿正文 | Step 4 放行结论 | 让 Step 5 基于正式 gate 继续 | 回到 Phase 3 |

### 验证矩阵

| 验证项 | 结论标准 | 当前落点 | 失败返工入口 |
| --- | --- | --- | --- |
| `遮轴名快检` | 去掉轴名后仍能看出“先修什么 / 怎样才算合法修 / 何时放行” | 修复任务清单、deviation、gate | 回到字段矩阵 |
| `轴权归属检查` | `anti_ai_force_check` 与事实层冲突只能由成立轴判废，优选轴不能越权美化 | gate 字段 | 回到轴角色字段化 |
| `近邻替换压测` | 把 `repair_gain_per_change` 换成泛词“更顺”后，修法选择明显失焦 | 优选轴对比字段 | 回到优选轴 |
| `落盘扰动测试` | 删掉 deviation 或 `anti_ai_force_check` 时，Step 5 放行链立即断裂 | 变更摘要与 gate | 回到落盘映射 |

### 快照落点说明

- 思维链如何作用于执行流程：先按 severity 排序，再做最小必要修复，最后执行终检
- 思维链如何作用于交付：输出必须可直接进入 Step 5，而不是还停在“待改”
- 思维链如何作用于验收：`anti_ai_force_check=fail` 时不得放行

## 4. 执行流程

### Phase 1 问题分级

- 目标：把 Step 3 的问题包转换为修复序列
- 输入：`overall_score`、`issues`、`severity_counts`、`references/step-4-polish-gate/appendix-polish-guide.md`
- 动作：先处理 `critical/high`，再决定 `medium/low` 的收益优先级
- 产出：修复任务清单
- 失败信号 / 返工入口：一上来就全文重写，或无视 severity

### Phase 2 最小必要修复

- 目标：修掉必须修的问题，同时保留原稿有效亮点
- 输入：修复任务清单、章节正文
- 动作：按问题类型做定向修复；无法修复时记录 deviation
- 产出：修复后的正文与修复项说明
- 失败信号 / 返工入口：修复引入新设定冲突，或把 Step 4 用成大改剧情入口

### Phase 3 终检放行

- 目标：完成 Anti-AI、No-Poison 与排版终检
- 输入：修复后的正文、`writing-craft-catalog` 中命中的 leaf notes（如 `typesetting.md`）
- 动作：执行全文检查，输出 `anti_ai_force_check: pass/fail`
- 产出：最终正文、变更摘要、deviation、放行结论
- 失败信号 / 返工入口：`anti_ai_force_check=fail` 或排版终检未过

## 5. 交付

- 类型：内容输出型
- 模式：覆盖章节正文，并输出变更摘要
- 正式落点：章节正文文件、Step 4 变更摘要、`anti_ai_force_check`
- 上层消费方式：Step 5 读取润色后正文与 `overall_score`
- 若为内容输出型，输出模板/字段骨架：`润色后正文 + 变更摘要（修复项 / 保留项 / deviation / anti_ai_force_check）`
- 若为非内容输出型，执行模式/状态推进方式：N/A

## 6. 验收机制

- quality standard：
  - 全部 `critical` 已处理
  - 未处理的 `high` 有 deviation
  - `anti_ai_force_check=pass`
  - 排版终检至少完成移动端可读性检查
- acceptance checklist：
  - [ ] 已按 severity 顺序修复
  - [ ] 未越权改剧情真源
  - [ ] 终检结果明确
  - [ ] 若进入 craft 模块，进入理由与收益可追溯
- fail signal：`critical` 未清零、`anti_ai_force_check=fail`、或修复引入设定冲突
- rework entry：回到 Phase 1 重新分级或回到更上游合同修复事实层问题

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是
- 若为多模块场景，是否已有统一路由段落：是
- 父 `SKILL.md` 中的模块关系：Step 4 专属；可按需串 `writing-craft-catalog`

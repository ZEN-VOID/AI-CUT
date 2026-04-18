# Writing Craft Catalog Module Spec

## 1. 适用场景

- 上层 SKILL 语境：`3-Drafting/SKILL.md` 的 Step 1 / Step 2B / Step 4 条件加读模块
- 当前模块负责对象/范围：根据题材或 craft 症状，从 `references/writing-craft-catalog/leaf-notes/*.md` 里选择最小必要的 leaf note，并避免基础对白指南与高阶声口指南同时充当平行真源
- 模块归属类型：多子类型之一
- 进入触发信号：
  - Step 1 需要题材 hook、开头差异化或章节引导强化
  - Step 2B / 4 命中对白、情绪、战斗、场景、氛围、节奏、欲望、排版等局部 craft 症状
- 不负责项：
  - 不单独拥有工作流入口
  - 不替代 step 模块
  - 不改上游真源职责
- 与兄弟模块边界：
  - 由 step 模块调用
  - 只解决局部 craft 问题

## 2. 预加载上下文

- 上层必读：
  - 根 `SKILL.md`
  - 根 `CONTEXT.md`
  - 调用它的 step `module-spec.md`
- 本层必读：
  - 当前 `module-spec.md`
  - 当前 `CONTEXT.md`
- leaf notes：
  - `references/writing-craft-catalog/leaf-notes/combat-scenes.md`
  - `references/writing-craft-catalog/leaf-notes/dialogue-writing.md`（基础对白体检：说明腔、信息宣讲、节奏失衡）
  - `references/writing-craft-catalog/leaf-notes/voice-register-and-duel.md`（高阶对白主入口：角色声口、对手戏攻防、关系位移）
  - `references/writing-craft-catalog/leaf-notes/emotion-psychology.md`
  - `references/writing-craft-catalog/leaf-notes/scene-description.md`
  - `references/writing-craft-catalog/leaf-notes/atmosphere-and-jingjie.md`
  - `references/writing-craft-catalog/leaf-notes/narrative-rhythm.md`
  - `references/writing-craft-catalog/leaf-notes/desire-description.md`
  - `references/writing-craft-catalog/leaf-notes/typesetting.md`
  - `references/writing-craft-catalog/leaf-notes/genre-hook-payoff-library.md`
- 加载顺序：根 `SKILL.md` / 调用 step 模块 -> 当前 `module-spec.md` -> 当前 `CONTEXT.md` -> 命中的最小 leaf notes
- 冲突优先级：用户显式请求 > `AGENTS.md` / 元规则 > 根 `SKILL.md` > 调用 step 模块 > 当前 `module-spec.md` > 当前 `CONTEXT.md` > leaf notes
- 默认不并入的上下文：不因为一个症状就整包读取所有 craft notes

## 3. 思维链

### Think-Think Design Snapshot

- mode: `思维链优化设计`
- task_essence:
  - 本模块真正要把 `模糊 craft 不足` 从 `泛化不够好看` 推到 `能定位到 1-2 个最必要 leaf notes 的最小加读决策`
- baseline_symptom:
  - 旧快照虽然说明了“症状 -> leaf note”，但还没有把症状归类、越权风险、最小必要原则压成可验证字段

### 观察到的事实 / 推断出的缺口

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | `writing-craft-catalog` 只能由 Step 1 / 2B / 4 按需调用 | 根 `SKILL.md` 路由矩阵 | 写入方向轴判废字段 |
| `Observed Facts` | leaf notes 的职责各不相同，有题材 hook、排版、基础对白体检与高阶声口对手戏等分工 | `references/writing-craft-catalog/leaf-notes/*.md` | 写入粗裁决症状分类字段 |
| `Inferred Gaps` | “最小加读”之前没有明确说出哪些字段决定是否过度加载 | 旧快照只有原则没有字段 | 补 `symptom_specificity` / `load_budget` 等字段 |
| `Protected Constraints` | craft note 不能覆盖 step 模块的真源与闸门 | 根 `SKILL.md` 与上层模块边界 | 强化成立轴判废字段 |
| `Proposed Rewrite` | 用“症状分类 -> 最小匹配 -> 回接收益”三层字段重写 | think-think 优化模式 | 已写入矩阵与验证表 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | `症状命中对齐` | 当前到底是哪类 craft 症状需要加读 | leaf note 选择 |
| `成立轴` | `局部强化成立` | 选中的 leaf note 是否真能解决该症状，而不是越权改真源 | 最小加读策略 |
| `优选轴` | `检索收益比` | 在多个可能 leaf note 中，哪个最少、最直接、最有收益 | 单次 1-2 个 leaf notes |

### 轴角色字段化

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 唯一主轴说明 |
| --- | --- | --- | --- | --- |
| `症状命中对齐` | `craft_symptom_type`、`trigger_step`、`genre_signal` | `no_step_owner`、`symptom_unspecified` | `symptom_specificity` | 只由方向轴决定“当前到底缺哪类 craft” |
| `局部强化成立` | `leaf_note_scope_fit`、`truth_source_respect`、`load_budget` | `leaf_note_overreach`、`full_bundle_load`、`truth_source_override` | `locality_score` | 只由成立轴决定“这个加读是否合法且不过量” |
| `检索收益比` | `expected_gain`、`loading_cost`、`step_fit` | `tiny_gain_high_cost`、`duplicate_leaf_overlap` | `gain_per_note` | 只由优选轴比较“读哪 1-2 个最值” |

### 三重

| 裁决层 | 本层关键问题 | 本模块产物 |
| --- | --- | --- |
| `粗裁决 / Base Range` | 当前是哪类 craft 症状 | 症状分类 |
| `细裁决 / Range Narrowing` | 哪些 leaf note 真与当前症状匹配 | 最小加读清单 |
| `离散裁决 / Final Selection` | 本轮到底读哪 1-2 个最划算 | 实际 loaded references |

### 分重关键向字段矩阵

| 裁决层 | 驱动字段 | 判废字段 | 对比字段 | 为什么这些才是“向” |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `craft_symptom_type`、`trigger_step`、`genre_signal` | `symptom_unspecified` | `symptom_specificity` | 先决定当前到底是哪类 craft 问题 |
| `细裁决 / Range Narrowing` | `leaf_note_scope_fit`、`load_budget`、`truth_source_respect` | `full_bundle_load`、`leaf_note_overreach` | `locality_score` | 把“知道问题但读太多/读错文档”的方案筛掉 |
| `离散裁决 / Final Selection` | `expected_gain`、`loading_cost`、`step_fit` | `duplicate_leaf_overlap` | `gain_per_note` | 真正决定哪 1-2 个 leaf notes 最值 |

### 字段落盘映射

| 裁决层 | 服务槽位 / 步骤 | 具体落点 | 采用理由 | 失败返工入口 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `craft_symptom` 归类 | 调用 step 的加读触发说明 | 让“为什么进 craft”可追溯 | 回到 Phase 1 |
| `细裁决 / Range Narrowing` | `loaded_references` 上限与理由 | 实际加载清单 | 让最小必要原则可检查 | 回到 Phase 2 |
| `离散裁决 / Final Selection` | craft 加读摘要 | 回接 Step 1 / 2B / 4 的执行建议 | 让 leaf notes 真正服务上游 step | 回到 Phase 3 |

### 验证矩阵

| 验证项 | 结论标准 | 当前落点 | 失败返工入口 |
| --- | --- | --- | --- |
| `遮轴名快检` | 去掉轴名后仍能看出“缺什么 craft / 该读哪些 / 为什么只读这些” | 症状归类、loaded_references、摘要 | 回到字段矩阵 |
| `轴权归属检查` | 是否过量加载只能由成立轴否决，不允许优选轴以“更稳”为由整包全读 | `load_budget` | 回到轴角色字段化 |
| `近邻替换压测` | 把 `gain_per_note` 换成泛词“多读一点更保险”后，最小加读原则立即失稳 | 优选轴对比字段 | 回到优选轴 |
| `落盘扰动测试` | 去掉 `loaded_references` 或摘要时，调用 step 无法追踪 craft 收益 | 加载清单与摘要 | 回到落盘映射 |

### 快照落点说明

- 思维链如何作用于执行流程：先分症状，再缩小到 1-2 个 leaf notes
- 思维链如何作用于交付：交付的是“本轮该读哪些 craft notes”，不是一锅端的大杂烩
- 思维链如何作用于验收：若 loaded references 超出必要范围，说明本模块失控

## 4. 执行流程

### Phase 1 症状识别

- 目标：确认当前 craft 问题是什么
- 输入：step 模块给出的症状、题材、审查问题包
- 动作：把问题归到战斗 / 基础对白问题 / 高阶声口问题 / 情绪 / 场景 / 氛围 / 节奏 / 欲望 / 排版 / 题材 hook
- 产出：症状分类
- 失败信号 / 返工入口：症状模糊，导致 leaf note 乱读
  - 基础对白问题：信息宣讲、对白太平、节奏拖、缺潜台词入口，优先进入 `dialogue-writing.md`
  - 高阶声口问题：角色同声同气、对手戏无位移、关系攻防发虚，优先进入 `voice-register-and-duel.md`

### Phase 2 最小加读

- 目标：选择 1-2 个最必要的 leaf notes
- 输入：症状分类、leaf notes 清单
- 动作：按最小必要原则挑选 leaf notes
- 产出：loaded references
- 失败信号 / 返工入口：为了求稳把整包 craft notes 全读一遍

### Phase 3 回接 step 模块

- 目标：把 craft notes 的收益回流到调用 step
- 输入：loaded references、step 当前任务
- 动作：生成仅服务当前 step 的执行建议
- 产出：craft 加读摘要
- 失败信号 / 返工入口：leaf note 反客为主覆盖 step 主任务

## 5. 交付

- 类型：非内容输出型
- 模式：叶子文档检索与最小加读
- 正式落点：`loaded_references`、执行建议摘要、调用 step 的附加说明
- 上层消费方式：被 Step 1 / 2B / 4 继续消费
- 若为内容输出型，输出模板/字段骨架：N/A
- 若为非内容输出型，执行模式/状态推进方式：记录实际命中的 leaf note 与症状映射

## 6. 验收机制

- quality standard：
  - 只读最必要 leaf notes
  - 叶子文档与症状一一对应
  - craft 加读不越权覆盖上层真源
- acceptance checklist：
  - [ ] 已说明症状
  - [ ] `loaded_references` 不超过最小必要范围
  - [ ] 进入 craft 的理由与收益清晰
- fail signal：整包全读、无症状映射、或 leaf note 反客为主
- rework entry：回到 Phase 1 重新收缩症状

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是
- 若为多模块场景，是否已有统一路由段落：是
- 父 `SKILL.md` 中的模块关系：二级按需模块，由 Step 1 / 2B / 4 调用

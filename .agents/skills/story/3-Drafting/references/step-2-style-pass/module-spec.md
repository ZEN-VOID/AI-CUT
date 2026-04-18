# Step 2 Style Pass Module Spec

## 1. 适用场景

- 上层 SKILL 语境：`3-Drafting/SKILL.md` 的 Step 2B 风格适配
- 当前模块负责对象/范围：把 Step 2A 草稿转译为更稳的网文表达，但不改剧情事实与事件顺序
- 模块归属类型：多步骤之一
- 进入触发信号：
  - 进入 Step 2B
  - 草稿出现模板腔、说明腔、机械腔
  - 需要做句式拆分、抽象转具体、网文口感增强
- 不负责项：
  - 不修审查问题
  - 不重写剧情
  - 不替代 Step 4 的 Anti-AI / No-Poison 终检
- 与兄弟模块边界：
  - 与 `step-4-polish-gate` 互斥职责最强，前者改表达，后者修问题
  - 需要专项 craft 支持时串到 `writing-craft-catalog`

## 2. 预加载上下文

- 上层必读：
  - 根 `SKILL.md`
  - 根 `CONTEXT.md`
- 本层必读：
  - 当前 `module-spec.md`
  - 当前 `CONTEXT.md`
- 模块附属 appendix：
  - `references/step-2-style-pass/appendix-style-adapter.md`
- 条件依赖：
  - `references/writing-craft-catalog/module-spec.md`
- 加载顺序：根 `SKILL.md` -> 根 `CONTEXT.md` -> 当前 `module-spec.md` -> 当前 `CONTEXT.md` -> appendix / craft 模块
- 冲突优先级：用户显式请求 > `AGENTS.md` / 元规则 > 根 `SKILL.md` > 当前 `module-spec.md` > 当前 `CONTEXT.md` > appendix
- 默认不并入的上下文：不在本模块里引入 Step 3 的问题清单来偷跑润色

## 3. 思维链

### Think-Think Design Snapshot

- mode: `思维链优化设计`
- task_essence:
  - 本模块真正要把 `可读但粗糙的草稿` 从 `事实正确` 推到 `表达更顺但仍不越权的待审正文`
- baseline_symptom:
  - 原有快照写了“表达转译 / 事实边界 / 可读性收益”，但没有把“哪些字段驱动改写、哪些字段一碰就坏”压成裁决字段

### 观察到的事实 / 推断出的缺口

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | Step 2B 只能改表达，不能改剧情事实、事件顺序、角色结果、设定规则 | 根 `SKILL.md` 与 `appendix-style-adapter.md` | 升成成立轴判废字段 |
| `Observed Facts` | Step 2B 与 Step 4 必须严格分工 | 根 `SKILL.md` 的职责边界 | 把“问题修复”排除出本模块范围 |
| `Inferred Gaps` | 之前没有明确“什么症状值得进入 craft、什么只是普通转译” | 旧快照缺少症状级字段 | 补最小加读触发字段 |
| `Protected Constraints` | 转译后正文必须还能被 Step 3 稳定审查 | 工作流顺序 | 把待审性写入离散裁决 |
| `Proposed Rewrite` | 用“改写白名单 -> 表达症状 -> craft 最小加读”三层字段重写 | think-think 优化模式 | 已写入矩阵与验证表 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | `表达转译对齐` | 这轮改写是否只服务网文表达提升，而不是重写剧情 | 长句拆分、抽象转具体、口感增强 |
| `成立轴` | `事实边界成立` | 改写过程中是否守住剧情走向、事件顺序、设定规则与角色结果 | 红线与禁改项 |
| `优选轴` | `可读性收益比` | 在多种表达方案里，哪种更顺滑、更有网文口感且最少引入新风险 | 软建议、题材加权、craft 升级入口 |

### 轴角色字段化

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 唯一主轴说明 |
| --- | --- | --- | --- | --- |
| `表达转译对齐` | `long_sentence_density`、`abstract_judgment_density`、`summary_narration_density` | 改写目标不清、正文没有推进点、把所有问题都扔给 Step 4 | 转译收益、段落流速改善度 | 只由方向轴决定“要不要做表达转译” |
| `事实边界成立` | `immutable_plot_points`、`event_order_lock`、`character_result_lock`、`setting_lock` | 任何剧情改写、结果逆转、设定越界 | 风险暴露数、禁改项碰撞数 | 只由成立轴决定“这次改写是否合法” |
| `可读性收益比` | `dialogue_intent_gain`、`rhythm_smoothness_gain`、`genre_fit_gain` | 为了花哨而降低清晰度、进入 craft 无症状 | 审查前可读性、成本收益比 | 只由优选轴决定“哪种表达更值” |

### 三重

| 裁决层 | 本层关键问题 | 本模块产物 |
| --- | --- | --- |
| `粗裁决 / Base Range` | 这段草稿需不需要进入风格转译 | 风格改写任务范围 |
| `细裁决 / Range Narrowing` | 哪些能改，哪些绝不能改 | 禁改项与硬约束 |
| `离散裁决 / Final Selection` | 在成立的表达方案里选哪种最顺 | 转译后的正文与改写日志 |

### 分重关键向字段矩阵

| 裁决层 | 驱动字段 | 判废字段 | 对比字段 | 为什么这些才是“向” |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `style_transfer_needed`、`sentence_pressure`、`exposition_weight` | `no_transfer_target`、`already_review_issue_mode` | `rewrite_scope` | 决定这章是否值得进入 Step 2B |
| `细裁决 / Range Narrowing` | `immutable_plot_points`、`event_order_lock`、`result_lock` | `plot_drift`、`result_change`、`setting_change` | `risk_exposure` | 负责把“写得顺但越权”的方案筛掉 |
| `离散裁决 / Final Selection` | `dialogue_gain`、`rhythm_gain`、`craft_trigger` | `craft_overreach`、`clarity_drop` | `review_readiness` | 负责在合法改写里挑最适合待审的版本 |

### 字段落盘映射

| 裁决层 | 服务槽位 / 步骤 | 具体落点 | 采用理由 | 失败返工入口 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | Step 2B 改写范围 | 改写日志中的任务范围与目标症状 | 让“为何进入 Step 2B”可追溯 | 回到 Phase 1 |
| `细裁决 / Range Narrowing` | 改写白名单 / 黑名单 | `appendix-style-adapter` 执行前的红线锁定 | 让事实边界真实可执行 | 回到 Phase 1 |
| `离散裁决 / Final Selection` | 章节正文 + 改写日志 | 风格化正文、craft 加读摘要 | 让 Step 3 读取的是稳定待审文本 | 回到 Phase 3 |

### 验证矩阵

| 验证项 | 结论标准 | 当前落点 | 失败返工入口 |
| --- | --- | --- | --- |
| `遮轴名快检` | 去掉轴名后仍能看出“要不要改 / 能改什么 / 选哪种改法” | 改写日志与红线清单 | 回到字段矩阵 |
| `轴权归属检查` | 任何事实漂移都只能由成立轴判废，不允许优选轴“好看所以放行” | `immutable_plot_points` 等锁字段 | 回到轴角色字段化 |
| `近邻替换压测` | 把 `dialogue_gain` 换成泛词“更自然”后，裁决明显变弱 | 离散裁决对比字段 | 回到优选轴 |
| `落盘扰动测试` | 拿掉改写日志或白名单后，Step 3 无法追溯转译边界 | 改写日志 / 正文 | 回到落盘映射 |

### 快照落点说明

- 思维链如何作用于执行流程：先锁红线，再做表达转译，最后才按需叠 craft 专项
- 思维链如何作用于交付：正文可被 Step 3 审查，不掺杂问题修复逻辑
- 思维链如何作用于验收：若改写触动剧情真源或角色行为结果，直接失败

## 4. 执行流程

### Phase 1 红线锁定

- 目标：标出不可改事实层
- 输入：Step 2A 草稿、章节执行包、`references/step-2-style-pass/appendix-style-adapter.md`
- 动作：锁定剧情走向、事件顺序、角色行为结果、设定规则
- 产出：改写白名单 / 黑名单
- 失败信号 / 返工入口：先改写后补红线，导致事实层漂移

### Phase 2 表达转译

- 目标：对说明腔、模板腔、机械腔做表达层修正
- 输入：改写白名单 / 黑名单、草稿正文
- 动作：拆长句、抽象转具体、删总结式旁白、保留至少 1 个明确推进点
- 产出：风格化正文
- 失败信号 / 返工入口：改写后字数、节奏或推进点明显退化

### Phase 3 Craft 加读与验证

- 目标：只在必要时调用专项 craft notes
- 输入：dialogue / rhythm / atmosphere / desire 等症状
- 动作：进入 `writing-craft-catalog` 选择最小必要 leaf note，再回到正文验证
- 产出：改写日志与最终正文
- 失败信号 / 返工入口：为了加 craft 而过度重写，或没有说明为何进入 craft 路由

## 5. 交付

- 类型：内容输出型
- 模式：在不改事实层的前提下覆盖章节正文
- 正式落点：章节正文文件与改写日志
- 上层消费方式：Step 3 把它当作正式待审正文
- 若为内容输出型，输出模板/字段骨架：`风格化正文 + 改写日志`
- 若为非内容输出型，执行模式/状态推进方式：N/A

## 6. 验收机制

- quality standard：
  - 未触碰禁改项
  - 模板腔、说明腔、机械腔明显下降
  - 改写后正文仍保留推进点与章内钩子
- acceptance checklist：
  - [ ] 事实层未变
  - [ ] 长句比例、解释段密度、对白意图至少一项得到改善
  - [ ] 若进入 craft 模块，已记录进入原因与收益
- fail signal：剧情走向漂移、角色结果改变、写成提前润色版 Step 4
- rework entry：回到 Phase 1 重新锁红线

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是
- 若为多模块场景，是否已有统一路由段落：是
- 父 `SKILL.md` 中的模块关系：Step 2B 专属；可按需串 `writing-craft-catalog`

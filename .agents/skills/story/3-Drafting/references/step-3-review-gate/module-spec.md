# Step 3 Review Gate Module Spec

## 1. 适用场景

- 上层 SKILL 语境：`3-Drafting/SKILL.md` 的 Step 3 审查阶段
- 当前模块负责对象/范围：把待审章节通过 `4-Validation` 路由到新的隔离评估团队，聚合审查结果并完成落库闸门
- 模块归属类型：多步骤之一
- 进入触发信号：
  - 进入 Step 3
  - 需要根据执行包、正文信号与章节标签自动选择 checker
  - 需要生成 `review_metrics` 并判定是否能进入 Step 4
- 不负责项：
  - 不直接修正文
  - 不伪造自审结论
  - 不跳过 `4-Validation`
- 与兄弟模块边界：
  - 为 `step-4-polish-gate` 提供问题包与硬闸门
  - 不吸收 Step 4 的修复动作

## 2. 预加载上下文

- 上层必读：
  - 根 `SKILL.md`
  - 根 `CONTEXT.md`
- 本层必读：
  - 当前 `module-spec.md`
  - 当前 `CONTEXT.md`
- 模块附属 appendix：
  - `references/step-3-review-gate/appendix-review-gate.md`
- 条件依赖：
  - `../../4-Validation/SKILL.md`
  - `.agents/skills/story/references/checker-output-schema.md`
- 加载顺序：根 `SKILL.md` -> 根 `CONTEXT.md` -> 当前 `module-spec.md` -> 当前 `CONTEXT.md` -> `4-Validation` / appendix
- 冲突优先级：用户显式请求 > `AGENTS.md` / 元规则 > 根 `SKILL.md` > 当前 `module-spec.md` > 当前 `CONTEXT.md` > appendix
- 默认不并入的上下文：不直接读取旧 checker 线程或过去的旧团队结果充数

## 3. 思维链

### Think-Think Design Snapshot

- mode: `思维链优化设计`
- task_essence:
  - 本模块真正要把 `待审章节` 从 `可被主观评价` 推到 `通过隔离团队产出可落库问题包与放行闸门`
- baseline_symptom:
  - 旧快照能说清要建队和落库，但还没有把“建队 / 选 checker / 放行”压到独立关键字段，验证颗粒度不够

### 观察到的事实 / 推断出的缺口

| 类型 | 内容 | 证据路径/依据 | 本轮动作 |
| --- | --- | --- | --- |
| `Observed Facts` | Step 3 必须经 `4-Validation` 建新团队，不得自审 | 根 `SKILL.md` 与 appendix | 变成方向轴判废字段 |
| `Observed Facts` | `review_metrics` 的字段形态和 timeline gate 是硬门槛 | appendix 与根 `SKILL.md` | 变成成立轴核心字段 |
| `Inferred Gaps` | `auto` 路由和放行判断仍偏说明文，缺少唯一轴权 | 旧快照只说“auto 路由收益比” | 补 route / gate 字段与轴权 |
| `Protected Constraints` | `overall_score` 只能来自新的隔离团队 | 审查合同 | 强化落盘映射 |
| `Proposed Rewrite` | 用“团队来源 -> 路由范围 -> 放行闸门”三层字段重写 | think-think 优化模式 | 已写入矩阵与验证表 |

### 三轴

| 轴角色 | 当前模块轴名 | 核心判断 | 直接落点 |
| --- | --- | --- | --- |
| `方向轴` | `隔离验证路由对齐` | 这轮审查是否真正通过新的隔离团队完成 | `4-Validation` 路由与 selected_agents |
| `成立轴` | `闸门字段成立` | 聚合结果、落库字段、时间线闸门是否齐全且可消费 | `review_metrics` 与 timeline gate |
| `优选轴` | `auto 路由收益比` | 在非 minimal 模式下，该启用哪些条件 checker 才最划算 | checker auto 路由 |

### 轴角色字段化

| 主轴 | 驱动字段 | 判废字段 | 对比字段 | 唯一主轴说明 |
| --- | --- | --- | --- | --- |
| `隔离验证路由对齐` | `new_team_created`、`validation_mode`、`chapter_scope` | `reuse_old_thread`、`inline_self_review`、`skip_validation` | `selected_agent_coverage` | 只由方向轴决定“这轮审查是否是真隔离审查” |
| `闸门字段成立` | `overall_score_present`、`review_metrics_shape`、`timeline_gate_state` | `missing_overall_score`、`invalid_notes_shape`、`timeline_block_ignored` | `handoff_readiness` | 只由成立轴决定“能不能放行” |
| `auto 路由收益比` | `reader_pull_trigger`、`high_point_trigger`、`pacing_trigger` | `over_review`、`under_review` | `signal_to_checker_fit` | 只由优选轴比较“启用哪些条件 checker 更值” |

### 三重

| 裁决层 | 本层关键问题 | 本模块产物 |
| --- | --- | --- |
| `粗裁决 / Base Range` | 这轮是 minimal、fast 还是标准 auto 审查 | checker 范围 |
| `细裁决 / Range Narrowing` | 哪些 checker 必跑，哪些由信号触发 | selected_agents 与 routing_decision |
| `离散裁决 / Final Selection` | 结果是否足够进入 Step 4 | 聚合结果、落库状态、timeline gate |

### 分重关键向字段矩阵

| 裁决层 | 驱动字段 | 判废字段 | 对比字段 | 为什么这些才是“向” |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `validation_mode`、`new_team_created`、`chapter_scope` | `self_review_mode`、`stale_team_reuse` | `checker_span` | 先决定这轮到底是不是合格的审查任务 |
| `细裁决 / Range Narrowing` | `selected_agents`、`routing_decision`、`review_metrics_shape` | `missing_core_checker`、`missing_required_field` | `coverage_vs_cost` | 把“有审查但不成立”的方案筛掉 |
| `离散裁决 / Final Selection` | `timeline_gate_state`、`overall_score_present`、`handoff_targets` | `timeline_high_issue_unblocked`、`metrics_not_saved` | `step4_entry_readiness` | 真正决定能否进入 Step 4 |

### 字段落盘映射

| 裁决层 | 服务槽位 / 步骤 | 具体落点 | 采用理由 | 失败返工入口 |
| --- | --- | --- | --- | --- |
| `粗裁决 / Base Range` | `validation_mode` / 新团队上下文 | `4-Validation` 调度入口 | 先证明是合法审查路径 | 回到 Phase 1 |
| `细裁决 / Range Narrowing` | `selected_agents` / `routing_decision` / `review_metrics.json` | 审查聚合与落库 | 让 Step 4 读到稳定问题包 | 回到 Phase 2 |
| `离散裁决 / Final Selection` | `timeline_gate` / `handoff_targets` | Step 4 放行判定 | 让“可进/不可进”不是口头判断 | 回到 Phase 3 |

### 验证矩阵

| 验证项 | 结论标准 | 当前落点 | 失败返工入口 |
| --- | --- | --- | --- |
| `遮轴名快检` | 去掉轴名后仍能看出“是否隔离建队 / 路由哪些 checker / 能否放行” | 新团队、selected_agents、timeline gate | 回到字段矩阵 |
| `轴权归属检查` | “能否进入 Step 4” 只能由成立轴解释，优选轴不得越权 | `timeline_gate_state` | 回到轴角色字段化 |
| `近邻替换压测` | 把 `signal_to_checker_fit` 换成泛词“更全面”后，route 解释明显变差 | auto 路由对比字段 | 回到优选轴 |
| `落盘扰动测试` | 删掉 `review_metrics_shape` 或 `timeline_gate` 时，Step 4 无法稳定接手 | 落库文件与 handoff | 回到落盘映射 |

### 快照落点说明

- 思维链如何作用于执行流程：先建隔离团队，再决定 route，最后完成聚合与闸门
- 思维链如何作用于交付：交付的是审查问题包与正式指标，不是口头“看起来没问题”
- 思维链如何作用于验收：若 `overall_score`、`review_metrics` 或 timeline gate 缺失，直接失败

## 4. 执行流程

### Phase 1 路由建队

- 目标：通过 `4-Validation` 建立新的隔离审查团队
- 输入：chapter、chapter_file、project_root、mode
- 动作：根据 mode 选择核心 checker 与 auto 条件 checker
- 产出：selected_agents、routing_decision、新团队上下文
- 失败信号 / 返工入口：复用旧线程、主流程内联自审、未说明为何启用/跳过 checker

### Phase 2 聚合与落库

- 目标：生成可供 Step 4 消费的审查问题包，并完成 `review_metrics` 落库
- 输入：checker 返回值、`.agents/skills/story/references/checker-output-schema.md`
- 动作：聚合 `issues / severity / overall_score / dimension_scores / risk fields`，执行 `save-review-metrics`
- 产出：聚合结果 + `review_metrics.json`
- 失败信号 / 返工入口：`overall_score` 缺失、字段落库不齐、`notes` 不是单字符串

### Phase 3 闸门交接

- 目标：明确这章是否能进入 Step 4
- 输入：聚合结果、timeline issues
- 动作：执行 timeline gate 与 Step 4 handoff 检查
- 产出：可进入 / 阻断判定
- 失败信号 / 返工入口：存在高严重度 `TIMELINE_ISSUE` 却仍继续放行

## 5. 交付

- 类型：非内容输出型
- 模式：输出聚合结果、落库文件与 Step 4 handoff
- 正式落点：`.webnovel/tmp/review_metrics.json`、index review metrics、新团队聚合结果
- 上层消费方式：Step 4 直接读取 `issues`、`severity_counts`、`overall_score`
- 若为内容输出型，输出模板/字段骨架：N/A
- 若为非内容输出型，执行模式/状态推进方式：写明 selected_agents、validation_mode、timeline gate 结果

## 6. 验收机制

- quality standard：
  - `overall_score` 来自新的隔离团队
  - 核心字段可落库
  - timeline gate 正确阻断严重时间线问题
- acceptance checklist：
  - [ ] 已通过 `4-Validation`
  - [ ] `review_metrics` 成功落库
  - [ ] `overall_score`、`issues`、`severity_counts`、风险字段齐全
  - [ ] 若存在高严重度 timeline issue，已阻断 Step 4
- fail signal：无隔离团队、无落库、无闸门、伪造结论
- rework entry：回到 Phase 1 重新建队与路由

## Parent SKILL 回写检查

- 父 `SKILL.md` 是否已写明当前模块触发机制：是
- 若为多模块场景，是否已有统一路由段落：是
- 父 `SKILL.md` 中的模块关系：Step 3 专属，上游无并行替代

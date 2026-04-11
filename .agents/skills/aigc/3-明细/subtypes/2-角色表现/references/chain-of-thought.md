# aigc 3-明细 / 2-角色表现 / Chain Of Thought

本文件承载 `aigc 3-明细 / 2-角色表现` 的字段主表、可见思维快照、工具后反思与返工入口真源。

## 模式与对象

| 项目 | 当前合同 |
| --- | --- |
| 默认模式 | `思维链优化设计`；若父级合同被整体重构，可短暂借用 `原生思维链设计`，但最终仍回到本文件接口 |
| 目标对象 | `2-角色表现` 父级路由层，服务 `projects/<项目名>/编导/第N集.json`、父级执行报告与 evidence sidecar |
| 默认模型策略 | 若调用模型具备 reasoning / thinking 能力，优先使用高层判断 + 可见快照 + Gate；仅在普通模型下使用少量显式步骤支架 |
| 可见性边界 | 只保留可审计、可回写、可返工的父级裁决快照；不要求外显完整内部推理 |
| 工具 / 证据依赖 | 强依赖当前集终稿、分组容器、`2-组间` handoff，以及必要时某个 leaf 的已执行结果 |
| 受保护接口 | 不破坏 `FIELD-CPR-ROOT-01` 到 `FIELD-CPR-HANDOFF-06`；不越权把父级写成 leaf 正文合集、摄影层替身或第二终稿 |

## Think-Think Design Snapshot

### 启发式工作链

- `不可删性`: 删掉这轮父级判断后，下游会失去哪一种“先判 dominant subtype、再控写集冲突、再给 sibling 留口”的关键协调能力？
- `最先推动`: 默认先推动 `FIELD-CPR-ROUTE-03` 与 `FIELD-CPR-WEIGHT-04`；若唯一主入口和表现压力中心没锁住，禁止提前细化 leaf 风格。
- `先砍什么`: 先砍“三个 leaf 平均分配”“只凭正文局部开写”“读到一点动作/对白/心理就全命中”“为求完整而并行改同一终稿”的伪方案。
- `真正比较尺`: 比较的不是哪种写法更热闹，而是哪一种 dominant subtype 最能提升可演性、最少压坏共享写集、最便于后续 sibling 继承。
- `立场纠偏`: 当前判断默认站在共享终稿消费者和后续 sibling 的立场，而不是站在单个 leaf 想扩大职责边界的立场。
- `工具后反思`: 读取上游真源或某个 leaf 的执行结果后，先重问 dominant subtype 是否变化、是否仍需 supplemental leaf、是否该回退重判，再继续推进。
- `落盘门`: 每条保留判断都必须落到 `FIELD-CPR-*`、`Gate Summary`、`Fail Code` 或 `Rework Entry` 之一；落不到就删。

### 三轴三重裁决

| 裁决角色 | 在 `2-角色表现` 的具体问题 | 主要落点 |
| --- | --- | --- |
| `方向轴` | 当前段落最该优先解决的是身体外化、语言攻防，还是主观内层，以及父级究竟该把谁定为唯一主入口 | `FIELD-CPR-ROUTE-03`、`FIELD-CPR-WEIGHT-04` |
| `成立轴` | 这次父级裁决是否被当前终稿、分组容器、`2-组间` handoff 与现有戏核共同支撑，而不是只凭局部句子猜测 | `FIELD-CPR-INPUT-02`、`FIELD-CPR-WEIGHT-04` |
| `优选轴` | 在成立的候选里，哪一种 dominant subtype 最能增强可演性、减少重复改写，并给后续 sibling 留出最清晰的入口 | `FIELD-CPR-ROUTE-03`、`FIELD-CPR-HANDOFF-06` |
| `硬门禁轴` | 是否出现 leaf 并发写集、忽略上游 handoff、平均摊派三路径、另起平行稿或父级越权下沉等强制否决条件 | `FAIL-CPR-ROOT-01` 到 `FAIL-CPR-HANDOFF-06` |

| 收敛层 | 本层先裁什么 | 服务 `field_id` | 本层收窄了什么 | 正确产物 |
| --- | --- | --- | --- | --- |
| `粗裁决` | 当前任务是否真的属于 `2-角色表现` 父级协调层，以及是否需要先判唯一主入口 | `FIELD-CPR-ROOT-01`、`FIELD-CPR-INPUT-02` | 收窄掉越权到镜头/摄影/分镜的误入，以及“不看上游就先改正文”的伪起步 | 父级边界 + 输入链 |
| `细裁决` | 当前场景最主要的表现压力中心是什么，哪一个 leaf 应成为 dominant subtype | `FIELD-CPR-ROUTE-03`、`FIELD-CPR-WEIGHT-04` | 收窄掉三个 leaf 平均分配、题材名式粗暴分类、未判戏核先补字数的假路由 | 唯一主入口 + 表现压力中心 |
| `离散裁决` | 如何把 dominant / supplemental 的执行顺序、安全写位与后续留口落到真源 | `FIELD-CPR-LAND-05`、`FIELD-CPR-HANDOFF-06` | 收窄掉另起平行稿、边写边改路由、做完父级却不给 sibling 明确入口的半闭环 | 共享写位约束 + 交接说明 |

### 可见 / 隐藏分层

| 层级 | 保留内容 | 去向 |
| --- | --- | --- |
| `可见快照层` | 父级边界、输入链、唯一主入口、表现压力中心、共享写位约束、后续留口 | 进入字段表、执行报告与真源说明 |
| `Gate Summary 层` | 当前阻塞、主导失败码、返工入口、confidence、unknowns、下一入口 | 进入验收记录或 sidecar |
| `隐藏推理层` | 被淘汰的 leaf 组合、未采用的 dominant 判断比较、局部修辞层面的试写过程 | 仅留在内部推理，不进可见合同 |

## 工具后反思与 Gate Summary

### 工具后反思

| 触发节点 | 必问反思 | 继续条件 | 不满足时回退 |
| --- | --- | --- | --- |
| 读取当前终稿、分组容器与 `2-组间` handoff 后 | 上游三者是否共同指向同一个戏核；是否已经足够支撑 dominant subtype 裁决 | 能明确回答“这场戏最缺哪种表现压力” | 回 `S2` 补输入或暂停 |
| 完成 dominant subtype 初判后 | 当前主入口是否真的唯一；是否只是因为局部元素显眼而误判 | 至少能排除另外两个 leaf 中的一个错误主入口 | 回 `S3-S4` 重判 |
| 某个 leaf 执行结果返回后 | 原先父级裁决是否仍成立；是否需要追加 supplemental leaf，还是应停止扩写避免过写 | shared draft 仍保持单一真源，且新增补强不会压坏后续 sibling | 回 `S4-S6` 重收束 |
| 准备写执行报告与留口前 | 是否已经说明覆盖范围、未处理项、唯一下一入口，而不是只写“已完成” | 后续 sibling 可以直接接手，不必重猜 dominant subtype | 回 `S6` 重写交接 |

### Gate Summary Contract

| 项目 | 必须回答 |
| --- | --- |
| `status` | `green / yellow / red` 三选一，不能省略 |
| `dominant_fail_code` | 当前最主要的失败码或 `none` |
| `rework_entry` | 若失败，必须指回 `S1` 到 `S6` |
| `confidence` | `0-1` 浮点值，说明当前父级路由判断稳定度 |
| `unknowns` | 尚未被上游真源或 leaf 执行解决的缺口，最多 3 条 |
| `next_entry` | 当前建议进入的后续 leaf 或 sibling；若无需继续，写 `none` |

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-CPR-ROOT-01 | 父级定位 | 明确 `2-角色表现` 是第二层人物表现增强站，负责父级路由与协调，而不是 leaf 正文合集或镜头层替身 | S1 | 边界清晰度 | FAIL-CPR-ROOT-01 |
| FIELD-CPR-INPUT-02 | 上游输入卡 | 明确当前终稿、分组容器、`2-组间` handoff 与必要执行结果的输入链，并说明缺口 | S2 | 输入完备性 | FAIL-CPR-INPUT-02 |
| FIELD-CPR-ROUTE-03 | 子路径路由矩阵 | 锁定 `动作戏 / 对手戏 / 内心戏` 的进入条件、唯一主入口与多命中时的 dominant-first 规则 | S3 | 路由准确性 | FAIL-CPR-ROUTE-03 |
| FIELD-CPR-WEIGHT-04 | 表现压力中心 | 写明当前场景到底缺身体、语言还是主观层，并解释为何不是另一个 dominant subtype | S4 | 戏核判断准确度 | FAIL-CPR-WEIGHT-04 |
| FIELD-CPR-LAND-05 | 终稿落点 | 所有改动只 patch 同一份 `第N集.json`，并保持执行报告与 evidence sidecar 只做证据辅助，不竞争主真源 | S5 | 真源单一性 | FAIL-CPR-LAND-05 |
| FIELD-CPR-HANDOFF-06 | 父级交接 | 给后续 sibling 留出未处理项、下一入口、是否需要 supplemental leaf 与停止条件 | S6 | 交接可执行性 | FAIL-CPR-HANDOFF-06 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-CPR-ROOT-01 | 父级到底负责什么，不负责什么 | 锁定父级职责与非职责 | 把父级写成 leaf 内容合集，或越权写成镜头/摄影说明 |
| S2 | FIELD-CPR-INPUT-02 | 当前要读哪些证据，以及哪些缺口会直接影响 dominant 裁决 | 固定终稿 / 分组 / 编导输入链并记录缺口 | 只盯当前正文，不看上游 |
| S3 | FIELD-CPR-ROUTE-03 | 当前进哪个 leaf，若多命中时如何保证共享写集安全 | 输出唯一主入口、放弃其他路径的理由与 dominant-first 规则 | 三个 leaf 一起开，或只说“都需要” |
| S4 | FIELD-CPR-WEIGHT-04 | 场景最缺哪种表现层，为什么不是别的 dominant subtype | 写表现压力中心与 dominant subtype | 没判戏核就开始补，或只按题材名分类 |
| S5 | FIELD-CPR-LAND-05 | 改动最终落到哪份真源，怎样避免产生第二正文 | 锁定同一份 `第N集.json` 与辅助 evidence 写位 | 另起平行成稿，或让报告与正文竞争真源 |
| S6 | FIELD-CPR-HANDOFF-06 | 如何交给后续 sibling，哪些项不该在本层继续硬写 | 写执行报告、留口、唯一下一入口与停止条件 | 本轮做完但后面接不上，或把所有问题都硬塞在本层 |

## Validation Matrix

| 检查项 | 通过标准 | 失败信号 |
| --- | --- | --- |
| 前置输入链检查 | 已读取当前终稿、分组容器与 `2-组间` handoff，并说明是否缺件 | 缺任一关键上游仍继续定 dominant subtype |
| dominant subtype 压测 | 能清楚说出“最缺身体 / 语言 / 主观”的唯一主判断，并至少排除一个错误主入口 | 三个 leaf 看起来都一样合理 |
| 共享写集安全检查 | 同一集只允许沿共享终稿 patch-in-place；多命中时采用 dominant-first 受控串行 | 另起平行稿或并行改同一文件 |
| 可见 / 隐藏分层检查 | 可见层只保留父级裁决快照，不把被淘汰方案和长篇比较塞进合同 | 文档充满未采用思路的自述 |
| 工具后反思检查 | 关键上游读取或 leaf 结果返回后，都发生过“是否继续 / 是否回退 / 是否改 dominant”的二次判断 | 工具结果一回来就机械继续 |
| sibling handoff 测试 | 后续 sibling 可直接接手，不必重猜表现压力中心与下一入口 | 交接只有“继续优化”之类空话 |
| 反越权检查 | 父级停留在协调、路由与留口层，不自然滑成 leaf 正文或镜头层执行文档 | 稍微细化就直接开始写 leaf 大段正文 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-CPR-ROOT-01 | 父级边界清晰，不越权到镜头 / 摄影 / 分镜，也不替代 leaf 正文 | FAIL-CPR-ROOT-01 | S1 |
| FIELD-CPR-INPUT-02 | 输入链覆盖终稿、分组、组间 handoff 与必要缺口说明 | FAIL-CPR-INPUT-02 | S2 |
| FIELD-CPR-ROUTE-03 | 三个 leaf 的进入条件、唯一主入口与冲突规则完整 | FAIL-CPR-ROUTE-03 | S3 |
| FIELD-CPR-WEIGHT-04 | 当前表现压力中心判断清楚，并解释为何不是其他主入口 | FAIL-CPR-WEIGHT-04 | S4 |
| FIELD-CPR-LAND-05 | 所有改动都回写同一终稿，辅助输出不竞争真源 | FAIL-CPR-LAND-05 | S5 |
| FIELD-CPR-HANDOFF-06 | 有执行报告、留口、唯一下一入口与停止条件 | FAIL-CPR-HANDOFF-06 | S6 |

# Impact Scope Contract

本文件定义 `story-repair` 在局部修改前必须锁定的“全身”范围。

## Impact Surface

| surface | required question | canonical examples |
| --- | --- | --- |
| project memory | 该改动是否属于长期偏好、禁区、特殊元素或稳定口径 | `projects/story/<项目名>/MEMORY.md` |
| project context | 项目共享事实、运行期补充材料是否需要同步 | `projects/story/<项目名>/CONTEXT/` |
| init source | 题材方向盘、global/style/genre 是否是错误源 | `0-初始化/north_star.yaml`、`init_handoff.yaml` |
| cards source | 角色、场景、物品、技能对象状态是否受影响 | `1-设定/**` |
| planning source | 整书、卷、章规划中的线索/任务/伏笔是否受影响 | `2-卷章/整体规划.md`、`第N卷/卷规划.md`、`第N章.md` |
| same-layer predecessor | 同层前列是否已经埋过相反事实 | 同卷前序章、上一章、同线索首次埋点 |
| current locality | 用户指定的局部本身 | 当前章节、段落、finding、对象字段 |
| produced downstream | 已产出的后续章、润色稿、sidecar 是否要同步 | `3-初稿/`、`4-润色/`、执行报告 |
| future constraints | 后续未产出但 planning/handoff 已预设的内容是否要改 | 后续章规划、卷末兑现、下一卷 handoff |
| acceptance and actualization | 已 PASS 或已回流的事实是否要失效或重验 | stage acceptance packets、`return/`、`STATE.json` |

## Universal Type Matrix

本矩阵是规则层通用标准，不写项目特例。项目特有的“某个线索牵动哪些具体章节/对象”只能追加到 `projects/story/<项目名>/CONTEXT/` 或本次 repair report，不得改写本通用矩阵。

| 当修改对象是 | 必查上游 | 必查同层/前列 | 必查下游/未来 | 必查验收 |
| --- | --- | --- | --- | --- |
| 线索 / 伏笔 / 证据链 | `2-卷章/整体规划.md`、卷规划、章规划、相关对象卡、项目 CONTEXT 中的线索索引 | 首次埋点、最近推进、当前章上一章、同线索误导点 | 后续兑现章、卷末兑现、下一卷 handoff、provider prompt/messages | 线索起承转合连续；旧口径无正向残留；新口径进入后续生成约束 |
| 角色动机 / 关系 / 状态 | 角色卡、关系字段、人物历史、相关场景/物品卡、章级人物任务 | 角色最近出场章、关系转折章、上一章情绪余波 | 后续互动章、阵营变化、润色稿、人物一致性验收维度 | 声纹、动机、关系动作和状态历史一致 |
| 物品 / 技能 / 规则机制 | 物品卡、技能卡、世界规则、north_star 边界、章级任务 | 首次出现、规则解释点、最近使用点 | 后续使用/兑现章、战斗/解谜/交易场景、卷末机制 payoff | 机制不变成外挂；代价、限制、持有人和证据链一致 |
| 场景 / 地点 / 空间动线 | 场景卡、地图/路线、章级场景义务、历史地理边界 | 上一次到达/离开、当前章前一场、空间封锁或入口点 | 后续移动、追逃、战场/旅程节点、时间线验收维度 | 人物位置、路线耗时、空间关系成立 |
| 章节事件 / 情节事实 | 章规划、卷规划、整体规划、上一章结尾、相关对象卡 | 事件因果前置、同卷前序章、冲突触发点 | 后续承接章、章节钩子、stage acceptance packet、return actualization | 事件因果、时间线、任务兑现和章末牵引一致 |
| 时间线 / 年代 / 历史边界 | north_star、整体规划、时间线索引、历史边界说明、项目 CONTEXT | 之前日期、季节、行军/旅程耗时、历史人物已出场事实 | 后续战争/政治/年龄/节气引用、review 时间线维度 | 年代不穿帮；真实历史边界不被主角线覆盖 |
| 世界观 / 题材 / 价值口径 | `0-初始化/north_star.yaml`、MEMORY、风格卡、题材承诺 | 同卷已产出文本分布、已有禁区、类型承诺第一次兑现 | provider prompt、后续章规划、润色稿、读者承诺 payoff | 新口径不和 north_star 冲突；旧口径不会在下一轮生成回流 |
| 叙事结构 / 卷章拓扑 | 整体规划、卷规划、章级规划、STATE、handoff、stage acceptance packet | 前后章任务分配、卷内节奏、已完成章节窗口 | 后续章节编号、卷末兑现、return carryover、下一卷起点 | 章节数、卷标签、任务分配和 validated actual 不漂移 |
| 已 PASS 终稿事实 / accepted actual | stage acceptance packet、return actualization、accepted manuscript refs、STATE | 被验收卷内的相关章节、终稿引用链 | 项目 CONTEXT carryover、下一卷 handoff、后续正文/润色稿 | 必须重验、失效化或明确保留旧验收；不得静默覆盖 |
| 局部语体 / 风格 / 表达分布 | MEMORY、north_star.style_contract、风格卡、阶段根技能合同 | 同章前后句群、同卷气口、角色声纹表 | 执行报告、润色稿、AI 检测风险上下文 | 不破坏事实；不把局部润色扩大成整章重写；LLM-first authorship 保持 |

## Project-Specific Extension Rule

- 通用矩阵属于 `story-repair` 规则层真源。
- 项目层只能补充具体名称、章节、对象和禁区，例如“某项目的 A 线索牵动第 2/5/9 章与某角色卡”。
- 项目层补充默认落在 `projects/story/<项目名>/CONTEXT/`；若是长期偏好、禁区或用户明确要求“以后记住”，才写入 `MEMORY.md`。
- 本次任务的实际检查结果写入 repair report 或对话，不因一次任务自动晋升为项目规则。
- 若项目补充与通用矩阵冲突，必须报告冲突；不得让项目上下文降低通用必查范围。

## Minimum Impact Map

每次 repair 至少输出：

```yaml
impact_map:
  upstream_truth:
    - path: ""
      status: affected | unaffected | unknown
      reason: ""
  same_layer_predecessors:
    - path: ""
      reason: ""
  current_locality:
    path: ""
    repair_intent: ""
  downstream_existing:
    - path: ""
      action: inspect | rewrite | invalidate | unchanged
  future_constraints:
    - path: ""
      action: update | preserve | add_guardrail
  acceptance_actualization:
    - path: ""
      gate_action: rerun | invalidate | preserve
```

## Scope Rules

1. 若旧口径在上游真源命中，默认先改上游，除非用户明确要求只做实验性局部稿。
2. 若旧口径只在正文层命中，进入 owning stage 的局部修复，不反向改写规划。
3. 若改动会改变已经 PASS 的终稿事实，必须把 stage acceptance packet 和 return actualization 纳入修复。
4. 若改动只影响表达风格而不影响事实，仍需检查 `MEMORY.md`、风格卡和阶段根技能上下文是否会把旧风格带回。
5. 若影响范围无法证明收敛，输出 repair plan 而不是直接写回。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 本次 repair 是否输出了覆盖 upstream truth、same-layer predecessor、current locality、downstream existing、future constraints、acceptance/actualization 的 impact map？ | `impact_scope` | `FAIL-REPAIR-SCOPE` | `steps/repair-workflow.md#N2-IMPACT-MAP` | repair packet 中的 `impact_map` 六类 surface 与路径/状态/理由 |
| 修改对象是否按 Universal Type Matrix 判型，并加载了命中的 `types/scope/*` 包？ | `type_matrix` | `FAIL-REPAIR-TYPE-MATRIX` | `types/type-map.md`、`steps/repair-workflow.md#N2-IMPACT-MAP` | `scope_packages_loaded`、命中矩阵行、typed package 列表 |
| 旧口径在上游真源命中时，是否先进入源层修复，而不是只改正文或润色稿？ | `source_priority` | `FAIL-REPAIR-OWNER` | `references/source-truth-ledger.md`、`steps/repair-workflow.md#N3-OWNER-ROUTE` | `canonical_owner`、`writeback_order`、旧/新口径检索证据 |
| 已 PASS 或 return actualized 的事实被改动时，是否处理 stage acceptance packet、return actualization 与 STATE？ | `accepted_truth` | `FAIL-REPAIR-AUDIT` | `steps/repair-workflow.md#N6-DOWNSTREAM-SYNC`、`steps/repair-workflow.md#N8-REVIEW-GATE` | acceptance/return/state action、重验/失效/保留理由 |
| 影响范围无法证明收敛时，是否停止写回并交付 repair plan？ | `convergence` | `FAIL-REPAIR-CONVERGENCE` | `SKILL.md#Mode Selection`、`steps/repair-workflow.md#N9-CLOSE` | verdict、阻断项、residual risks、下一步约束 |

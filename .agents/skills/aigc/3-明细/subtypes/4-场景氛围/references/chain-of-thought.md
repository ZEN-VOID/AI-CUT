# aigc 3-明细 / 4-场景氛围 / Chain Of Thought

本文件承载 `aigc 3-明细 / 4-场景氛围` 的字段主表、可见思维快照、工具后反思与返工入口真源。

## 模块定位

- 本文件是 `4-场景氛围` 按最新 `think-think` 规范升级后的标准思维链模块。
- 主 `SKILL.md` 继续保留边界、门禁、上溯钩子与模块回链；本文件负责把本层判断压实成 `运行模式 + 启发式工作链 + 三轴三重 + 可见快照 + Gate Summary`。
- 本模块默认只暴露可审计、可回写、可返工的环境裁决快照，不要求外显完整内部推理全文。
- 所有判断最终必须回到共享终稿字段、氛围裁决侧车、母题账本或本层 `validation-report.md`，不得漂成第二正文。

## 设计立场与运行模式

### 设计立场

1. `隐藏推理层`：允许模型在内部比较 `景 / 境 / 物 / 留白` 候选，但不把完整比较过程当成交付物。
2. `可见快照层`：对外只保留能支撑审计、补写、交接与返工的关键判断。
3. `字段落盘层`：每个关键判断都要落回 `FIELD-SAT-*`、共享终稿写位或 `Gate Summary`。
4. `边界守恒层`：本层只处理环境压力、空间温度、物件回声与留白，不越权到运镜、摄影、转场。

### 运行模式判定

| 模式 | 触发条件 | 外显策略 | 禁止误用 |
| --- | --- | --- | --- |
| `推理优先模式` | 使用原生 reasoning / thinking 模型执行本层补写 | 先用启发式工作链收窄环境任务与主路线，再输出可见快照与字段落点 | 把 `S1-S7` 写成僵硬逐字脚本 |
| `支架回退模式` | 普通模型、上下文噪声高、或上游材料较弱 | 保留 `S1-S7` 显式支架，但每步只保留高价值判断 | 把流程描述写得比氛围补写本身更长 |
| `工具反思增强模式` | 需要依赖 grouped source、当前 `第N集.json`、组间 handoff 或验证结果反复校正 | 每次关键材料读取或验收返回后先做二次判断，再继续写回 | 读取完证据就机械继续，不重判路线与写位 |

硬规则：

1. 默认优先 `推理优先模式`，`S1-S7` 是可见支架，不是内部推理全文脚本。
2. 任一模式都不得要求模型外显完整 CoT。
3. 若新证据改变 `环境任务 / dominant route / 写位 / 下一入口`，必须返回对应步骤重判，不得只在局部补丁式前进。

## Think-Think Design Snapshot

### 启发式工作链

- `不可删性`：删掉这轮判断，下游会在哪一处重新猜 `环境任务`、`dominant route`、`patch 位点` 或 `下一入口`？
- `最先推动`：当前最先该推动的是 `FIELD-SAT-ANCHOR-03`、`FIELD-SAT-ROUTE-04`，还是 `FIELD-SAT-PATCH-05`，而不是直接堆形容词？
- `先戏核后天气`：先回答这段环境在推进、对照、回收还是留白，再决定该是雨、雾、走廊、旧物还是静默。
- `先砍什么`：先砍摄影术语、镜头术语、标签式提示、脱离戏核的美句，以及 `景 / 境 / 物` 全开式炫技。
- `真正比较尺`：多个方案都能成立时，最终拿什么比？默认比 `戏核增压度`、`边界守恒`、`连读性`、`母题可回收性`。
- `预设护栏`：题材与环境语气先看 `writer.story` bundle 的 `世界卡 / 风格卡`，再看正文证据，不跳过结构化预设直接凭直觉选美学路线。
- `景境回收`：不要只盯物件母题；同一扇窗的光、同一条走廊的回声、同一片雨幕的强弱，也可能比道具更稳。
- `感官降维`：如果要用通感，必须把它落成声、味、温度、湿度、触感等可下游消费的物理信号，不能停在抽象抒情。
- `立场纠偏`：当前判断默认站在共享终稿与后续 sibling 消费者立场，而不是站在文案作者自我抒情的立场。
- `工具后反思`：读取 grouped source、当前终稿、组间 handoff 或验收结果后，先问哪一层判断被新证据改变，再决定是否继续。
- `落盘门`：这轮判断若落不到 `FIELD-SAT-*`、共享终稿写位、侧车、母题账本或 `Gate Summary`，就不应作为显式合同保留。

### 三轴三重裁决

| 裁决角色 | 在 `4-场景氛围` 的具体问题 | 主要落点 |
| --- | --- | --- |
| `方向轴` | 当前段落真正缺的是 `推进 / 对照 / 回收 / 留白` 中哪一种环境任务，主路线该由谁承担 | `FIELD-SAT-ANCHOR-03`、`FIELD-SAT-ROUTE-04` |
| `成立轴` | 该判断是否被 grouped source、当前终稿动作/情绪、组间 handoff 与 sibling 边界共同支撑 | `FIELD-SAT-INPUT-02`、`FIELD-SAT-ANCHOR-03`、`FIELD-SAT-PATCH-05` |
| `优选轴` | 在成立候选里，哪种氛围补写最能增压戏核、符合题材预设、最少返工、且最利于后续摄影/转场继续消费 | `FIELD-SAT-ROUTE-04`、`FIELD-SAT-MOTIF-06`、`FIELD-SAT-HANDOFF-07` |
| `硬门禁轴` | 是否命中无合法输入、锚点不足、路线过载、标签式写法、越权到 sibling、留白被写满等强制否决条件 | `FAIL-SAT-*`、`Gate Summary` |

| 收敛层 | 本层先裁什么 | 服务 `field_id` | 本层收窄了什么 | 正确产物 |
| --- | --- | --- | --- | --- |
| `粗裁决` | 当前段落到底要用环境完成什么任务 | `FIELD-SAT-ROOT-01`、`FIELD-SAT-ANCHOR-03` | 收窄掉“先美化再找用途”、无任务抒情、错把摄影效果当氛围任务 | 唯一 `环境任务 + 边界结论` |
| `细裁决` | 应走哪条 dominant route，是否需要一条 support route | `FIELD-SAT-ROUTE-04` | 收窄掉 `景 / 境 / 物 / 留白` 全开、无证据物件、题材失配、留白场堆句 | `dominant route + optional support route` |
| `离散裁决` | 最终该把句子补到哪里、如何留母题与下一入口 | `FIELD-SAT-PATCH-05`、`FIELD-SAT-MOTIF-06`、`FIELD-SAT-HANDOFF-07` | 收窄掉另起说明段、平行正文、不可回收母题、无下一入口的收尾 | `patch-in-place 写位 + 母题链 + handoff` |

### 层内自省

每次完成 `S2-S6` 后，至少要回答：

1. 为什么是这个环境任务/路线，而不是相邻任务或另一条路线？
2. 如果不是这个结果，会不会得到更强的戏核承压、更自然的连读性或更低的 sibling 返工？
3. 删掉当前保留项，下游会失去哪一个明确判断能力？
4. 如果把这一步改写成普通流程脚本，它为什么会比当前启发式合同更差？

若第 2 问答案为“会”，必须返回当前层重选，不得把旧结论直接带进下一层。

### 可见 / 隐藏分层

| 层级 | 保留内容 | 去向 |
| --- | --- | --- |
| `可见快照层` | 输入链、环境任务、主路线决议、补写位点、母题链、下一入口 | 进入侧车、共享终稿字段、母题账本 |
| `Gate Summary 层` | `status`、`dominant_fail_code`、`rework_entry`、`confidence`、`unknowns` | 进入 `projects/<项目名>/编导/evidence/4-场景氛围/validation-report.md` |
| `隐藏推理层` | 被淘汰路线的完整比较、被删掉的美句、内部取舍过程全文 | 仅留在内部推理，不进可见合同 |

## 标准思维链主链

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 必留可见快照 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-SAT-ROOT-01` | 当前任务是否真的属于 `4-场景氛围`，本层该守什么边界 | 锁定环境增强边界、排除运镜/摄影/转场越权 | `projects/<项目名>/编导/evidence/4-场景氛围/validation-report.md / 阶段边界检查` |
| `S2` | `FIELD-SAT-INPUT-02` | 当前哪些证据是合法真源，哪些只可作为弱信号 | 读取 grouped source、当前终稿、组间 handoff 与 `writer.story` 预设，形成输入链 | `projects/<项目名>/编导/evidence/4-场景氛围/氛围裁决-第N集.md / 输入链` |
| `S3` | `FIELD-SAT-ANCHOR-03` | 这段环境到底要完成什么任务，锚点是否足够 | 生成叙事锚点卡，先锁 `推进 / 对照 / 回收 / 留白`，不先挑天气 | `projects/<项目名>/编导/evidence/4-场景氛围/氛围裁决-第N集.md / 叙事锚点卡` |
| `S4` | `FIELD-SAT-ROUTE-04` | 哪条 dominant route 最成立，是否需要 support route | 从 `景 / 境 / 物 / 留白` 中做唯一主裁决，并用题材相容与排除理由收束 | `projects/<项目名>/编导/evidence/4-场景氛围/氛围裁决-第N集.md / 路由决议` |
| `S5` | `FIELD-SAT-PATCH-05` | 该补到哪个镜级字段附近，怎样 patch 才自然且不破坏原层 | 以 `patch-in-place` 方式回写共享终稿字段，并标记邻接写位 | `projects/<项目名>/编导/第N集.json / 场景氛围字段` |
| `S6` | `FIELD-SAT-MOTIF-06` | 哪些物件或环境信号值得形成最小母题链 | 记录 `首次 -> 变体 -> 回收`，允许景/境信号与物件共同承担回收，或显式放弃母题 | `projects/<项目名>/编导/evidence/4-场景氛围/母题账本-第N集.md / 母题链` |
| `S7` | `FIELD-SAT-HANDOFF-07` | 如何把本层结果交给 `5-摄影美学` 或 `6-转场特效`，并形成验收闭环 | 写下一入口、留口、风险与 Gate Summary | `projects/<项目名>/编导/evidence/4-场景氛围/validation-report.md / 交接与 Gate Summary` |

## 工具后反思与 Gate Summary

### 工具后反思

| 触发节点 | 必问反思 | 继续条件 | 不满足时回退 |
| --- | --- | --- | --- |
| 读取 grouped source、当前 `第N集.json`、组间 handoff 后 | 输入链是否足够支撑本层；哪些内容是真源，哪些只是风格暗示 | 能说清本层只补什么、不补什么 | 回 `S1-S2` 重锁边界或补输入 |
| 完成锚点卡后 | 环境任务是否唯一；留白需求是否高于风格化补写冲动 | 能明确回答这段环境要推进什么 | 回 `S3` 重判锚点与任务 |
| 完成 dominant route 初判后 | 是否出现路线过载、越权术语、无来源物件、连读断裂 | 主路线唯一，support route 仍克制且可解释 | 回 `S4-S5` 收窄路线或重置写位 |
| 写完母题链与 handoff 前 | 母题是否可回收；下一入口是否唯一；验收是否可判 PASS/FAIL | 下游可继续消费，不需要再猜本层结论 | 回 `S6-S7` 收束或改写交接 |

### Gate Summary 最低合同

| 项目 | 必须回答 |
| --- | --- |
| `status` | `green / yellow / red` 三选一，不能省略 |
| `dominant_fail_code` | 当前主导失败码或 `none` |
| `rework_entry` | 若失败，必须指回 `S1-S7` 之一 |
| `confidence` | `0-1` 浮点值，说明当前氛围裁决稳定度 |
| `unknowns` | 尚未被上游真源解决的缺口，最多 3 条 |

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SAT-ROOT-01 | `projects/<项目名>/编导/evidence/4-场景氛围/validation-report.md`.`阶段边界检查` | 明确 `4-场景氛围` 是第四层环境增强站，只负责环境增压、空间温度、母题回声与留白裁决 | S1 | 边界清晰度 | FAIL-SAT-ROOT-01 |
| FIELD-SAT-INPUT-02 | `projects/<项目名>/编导/evidence/4-场景氛围/氛围裁决-第N集.md`.`输入链` | 明确 grouped source、当前终稿、`writer.story` 预设、组间 handoff 与必要 sibling 证据的输入链与可信度 | S2 | 输入完备性 | FAIL-SAT-INPUT-02 |
| FIELD-SAT-ANCHOR-03 | `projects/<项目名>/编导/evidence/4-场景氛围/氛围裁决-第N集.md`.`叙事锚点卡` | 先锁场次功能、关系温差、情绪走向与环境任务，再决定是否允许风格化增强 | S3 | 戏核对齐度 | FAIL-SAT-ANCHOR-03 |
| FIELD-SAT-ROUTE-04 | `projects/<项目名>/编导/evidence/4-场景氛围/氛围裁决-第N集.md`.`路由决议` | 明确 `景 / 境 / 物 / 留白` 的 dominant route、support route、题材相容与排除理由 | S4 | 路由准确性 | FAIL-SAT-ROUTE-04 |
| FIELD-SAT-PATCH-05 | `projects/<项目名>/编导/第N集.json`.`场景氛围` | 氛围判断只回写同一份共享终稿字段，且必须自然贴合命中镜位 | S5 | 落笔可读性 | FAIL-SAT-PATCH-05 |
| FIELD-SAT-MOTIF-06 | `projects/<项目名>/编导/evidence/4-场景氛围/母题账本-第N集.md`.`母题链` | 记录物件或景/境环境信号的最小可追溯链路，或明确说明为何不立母题 | S6 | 可追溯性 | FAIL-SAT-MOTIF-06 |
| FIELD-SAT-HANDOFF-07 | `projects/<项目名>/编导/evidence/4-场景氛围/validation-report.md`.`交接与下一入口` | 给 `5-摄影美学` 或 `6-转场特效` 留唯一下一入口，并说明未覆盖问题与交接边界 | S7 | 交接可执行性 | FAIL-SAT-HANDOFF-07 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SAT-ROOT-01 | 本层到底负责什么，不负责什么 | 锁定环境增强边界与反越权门槛 | 把本层写成摄影、运镜或转场说明 |
| S2 | FIELD-SAT-INPUT-02 | 当前该读哪些证据，哪些证据不够硬 | 固定输入链与可信度层级 | 只凭局部句子或抽象印象补氛围 |
| S3 | FIELD-SAT-ANCHOR-03 | 这段环境任务到底是什么 | 生成锚点卡并收窄为唯一主任务 | 没判戏核就开始抒情，或锚点不足仍强写 |
| S4 | FIELD-SAT-ROUTE-04 | 当前走哪条主路线最成立 | 选 dominant route，并解释为何不选其他路线 | `景 / 境 / 物` 同时乱开，或留白场被写满 |
| S5 | FIELD-SAT-PATCH-05 | 应补到哪句附近，怎样补才不破层 | 执行自然融写并确认邻接写位 | 另起功能段、标签段，或破坏对白/分镜/角色层 |
| S6 | FIELD-SAT-MOTIF-06 | 哪些环境信号值得追踪，哪些该放弃 | 写母题链或写明放弃理由 | 好看但不可回收，或凭空引入新物件 |
| S7 | FIELD-SAT-HANDOFF-07 | 如何交给后续 sibling，并形成闭环 | 写留口、下一入口、风险与 Gate Summary | 做完本层仍接不上下一层，或验收无失败码 |

## Validation Matrix

| 检查项 | 通过标准 | 失败信号 |
| --- | --- | --- |
| 边界检查 | 文本只保留环境语义，不越权到运镜/摄影/转场 | 出现焦距、布光、镜头运动、特效主导语句 |
| 锚点成立检查 | 每段补写前都有足够锚点支撑环境任务 | 锚点不足仍强行追求氛围感 |
| 题材相容检查 | dominant route 与 `writer.story` 预设或 legacy preset 不冲突 | 明明是题材失配，仍硬追求漂亮路线 |
| 主路线唯一性检查 | dominant route 唯一，support route 仍克制 | `景 / 境 / 物 / 留白` 混开成噪声 |
| patch 连读检查 | 新句与前后文自然衔接，不破坏原段节拍 | 一读就像外挂说明或功能标签 |
| 留白门检查 | 高留白场新增不超过 1 条，且仍保有余波 | 静场被写满，余韵消失 |
| 时间刻度检查 | 物镜成立时，物件状态变化能承担时间流逝或关系变质 | 物件只有情调，没有时间刻度 |
| 母题可回收检查 | 母题链可追溯到已有物件或环境信号 | 物件凭空出现，后续无回收可能 |
| 工具后反思检查 | 关键读取与验收节点后都发生过二次判断 | 证据回来后直接机械继续 |
| Gate Summary 检查 | 有状态、失败码、返工入口、confidence、unknowns | 只写“完成”或“通过”，没有闭环信息 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-SAT-ROOT-01 | 边界清晰，不越权到运镜/摄影/转场 | FAIL-SAT-ROOT-01 | S1 |
| FIELD-SAT-INPUT-02 | 输入链覆盖 grouped source、终稿、组间 handoff，且可信度清楚 | FAIL-SAT-INPUT-02 | S2 |
| FIELD-SAT-ANCHOR-03 | 锚点卡足以支撑环境任务判断，且主任务唯一 | FAIL-SAT-ANCHOR-03 | S3 |
| FIELD-SAT-ROUTE-04 | 主路线与辅路线判断清楚，且无路线过载 | FAIL-SAT-ROUTE-04 | S4 |
| FIELD-SAT-PATCH-05 | 终稿回写自然、克制、可连读，且只在邻接位补写 | FAIL-SAT-PATCH-05 | S5 |
| FIELD-SAT-MOTIF-06 | 母题链最小可追溯，或放弃理由成立 | FAIL-SAT-MOTIF-06 | S6 |
| FIELD-SAT-HANDOFF-07 | 有留口、下一入口唯一、Gate Summary 可执行 | FAIL-SAT-HANDOFF-07 | S7 |

## 使用边界

1. 若问题是“环境任务与路线怎么判”，先看本文件与 [type-strategies.md](/Volumes/AIGC/AIGC-FILM/.agents/skills/aigc/3-明细/subtypes/4-场景氛围/references/type-strategies.md)。
2. 若问题是“往哪里写、辅助产物怎么落”，看 [output-template.md](/Volumes/AIGC/AIGC-FILM/.agents/skills/aigc/3-明细/references/output-template.md)。
3. 若问题是“执行顺序、共享运行时、交接流程”，看 [execution-flow.md](/Volumes/AIGC/AIGC-FILM/.agents/skills/aigc/3-明细/subtypes/4-场景氛围/references/execution-flow.md)。

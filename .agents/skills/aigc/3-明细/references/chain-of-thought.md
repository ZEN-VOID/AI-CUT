# aigc 3-明细 / Chain Of Thought

本文件承载 `aigc 3-明细` 的最新思维链合同真源，负责把阶段级判断从“老式字段表”升级为 `模式判定 -> 启发式工作链 -> 三轴三重 -> 可见快照 -> 字段落盘 -> Gate Summary` 的可执行链路。

## 模式与任务对象

| 模式 | 触发条件 | 在 `3-明细` 的默认用法 | 主要消费者 |
| --- | --- | --- | --- |
| `思维链优化设计` | 现有父级思维链只剩字段表、步骤表，无法承载真实裁决压力 | 默认模式；优先修父级阶段判断、唯一路由与落盘合同 | `3-明细` 根技能、各子路径、阶段验收者 |
| `原生思维链设计` | 某个新阶段或新父技能还没有稳定的阶段级思维链真源 | 用于从零建立阶段级裁决骨架 | 新建父技能或新阶段模块 |
| `推理模型适配设计` | 执行主体迁移到 reasoning / adaptive thinking 模型后，旧链条明显过度脚本化 | 把“先做什么”改写为“先裁什么、看什么证据、何时停手” | 使用推理模型执行 `3-明细` 的代理 |

硬规则：

1. 父级 `3-明细` 的默认模式是 `思维链优化设计`，除非该模块完全缺失。
2. 父级思维链必须优先服务“阶段路由 + 单一主文件 + patch-in-place + 下一入口”四个总判断，而不是直接下沉到某个 leaf 的局部写法。
3. 若当前任务无法回答“为什么是这个子路径、为什么不是其他子路径”，视为父级思维链未成立。

## Think-Think Design Snapshot

### 启发式工作链

- `不可删性`：删掉父级思维链后，执行者会失去“先锁 grouped source、再判唯一子路径、最后回写单一主文件”的总判断能力。
- `最先推动`：本轮最先要推动的不是华丽扩写，而是当前 `projects/<项目名>/编导/第N集.json` 应该由哪一层继续发酵。
- `先砍什么`：先砍掉“另起一份整稿”“多层混写一轮完成”“只做局部润色不看上游”和“所有子路径都值得一起进”的冲动。
- `真正比较尺`：比较候选子路径时，以“哪一层最能提升当前主文件的下一步可执行性、且最少越权重写”为主尺，而不是以“哪一层最有表现欲”为主尺。
- `立场纠偏`：父级思维链必须站在阶段 orchestrator 和下游消费者立场，而不是站在单次写作者的临场发挥立场。
- `工具后反思`：读取 grouped source、现有 `第N集.json`、`team.yaml`、侧车和已有验收报告后，必须先反思“证据是否支持继续当前层”，再决定继续、回退还是改路由。
- `落盘门`：如果某个判断不能落到 `唯一路由裁决 / 单一写位 / 侧车更新 / validation-report / 下一入口` 之一，它就不该留在父级思维链里。

### 三向三重自省流

| 裁决角色 | 在 `3-明细` 的具体问题 | 主要落点 |
| --- | --- | --- |
| `方向轴` | 当前最先服务的是阶段级哪一个判断：锁输入真源、判唯一路由、还是补阶段闭环 | `FIELD-SCRIPT-IDN-02`、`FIELD-SCRIPT-ROUTE-04` |
| `成立轴` | grouped source、现有主文件、组间 handoff、子路径状态、顾问团反馈是否足以支撑当前路由 | `FIELD-SCRIPT-IDN-02`、`FIELD-SCRIPT-REFL-07` |
| `优选轴` | 在多个候选都可行时，哪条子路径最稳、最少返工、最符合默认发酵顺序 | `FIELD-SCRIPT-ROUTE-04`、`FIELD-SCRIPT-GATE-08` |
| `硬门禁轴` | 是否存在上游未锁、主文件漂移、sibling 越权、顾问团阻断或验收缺口 | `FIELD-SCRIPT-LAND-05`、`FIELD-SCRIPT-GATE-08` |

| 收敛层 | 本层先裁什么 | 绝不带进下一层什么 | 正确产物 |
| --- | --- | --- | --- |
| `粗裁决 / Objective Framing` | 当前这轮要解决的是哪一个阶段级问题，服务哪个下游消费者 | “先写了再说”的扩写冲动 | 阶段终局句、输入边界、主要未知项 |
| `细裁决 / Candidate Narrowing` | 哪个子路径应成为本轮唯一主入口，哪些 sibling 应被排除 | “所有层都可以一起补”的混写冲动 | 唯一路由裁决、排除理由、默认顺序偏离说明 |
| `离散裁决 / Visible Landing` | 哪些内容进入可见快照，哪些进入侧车，哪些进入 Gate Summary 与返工入口 | 没有落盘位置的抽象判断 | 主文件写位、侧车更新、验收状态、下一入口 |

层内自省问题：

- `为什么是这个子路径，不是相邻层？`
- `如果回到默认顺序更稳，当前是否有足够证据跳层？`
- `删掉这轮保留项，下游会失去哪一种可续跑能力？`
- `如果把当前判断写成流程脚本，为什么会比启发式裁决更差？`

## 工具后反思与 Gate Summary

### 工具后反思

当父级判断依赖外部检索、文件读回、顾问团反馈或项目运行时状态时，必须执行以下反思顺序：

1. 先判断 grouped source、`第N集.json`、子路径侧车和 `validation-report.md` 是否彼此一致。
2. 再判断 `team.yaml` / 顾问团反馈是否改变当前路由或验收门槛。
3. 若证据显示主文件尚未具备进入当前层的前提，立即回退到更前一层，而不是继续硬写。
4. 若证据显示当前层已完成，但下一入口未唯一化，优先补 `Gate Summary` 与下一入口，而不是继续增加正文。

### Gate Summary Contract

| gate_state | 触发条件 | 动作 |
| --- | --- | --- |
| `PASS` | grouped source 已锁定、唯一路由明确、主文件单一、侧车与验收闭环完整 | 允许进入命中子路径或给出唯一下一入口 |
| `WARN` | 主文件单一但路由证据不足，或顾问团/验收反馈要求补一轮核对 | 先补证据或缩小任务，再进入下游 |
| `FAIL` | 上游未锁、平行稿增殖、越权混层、无写位、无返工入口 | 立即停止下游扩写，先修父级阶段合同 |

推荐评测动作：

- `唯一路由快检`：不看子路径名，只看证据是否能推出“只能先做这一层”。
- `单一真源追踪`：所有判断能否回到同一份 `projects/<项目名>/编导/第N集.json`。
- `反混层检查`：删掉本轮 route decision 后，是否会重新退回多层混写。
- `顾问团反思检查`：启用 `team.yaml` 时，是否真的在关键节点发生了二次裁决。

## 统一字段主表

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SCRIPT-MOD-01 | 模块.模式与任务对象 | 明确当前属于优化/原生/推理适配中的哪一种，以及父级消费者是谁 | S0 | 模式适配性 | FAIL-SCRIPT-MOD-01 |
| FIELD-SCRIPT-IDN-02 | 模块.阶段终局与边界 | 说明本轮首先服务哪个阶段级判断、锁哪些输入、不允许越权到哪里 | S1-S2 | 终局聚焦 | FAIL-SCRIPT-IDN-02 |
| FIELD-SCRIPT-STR-03 | 模块.启发式工作链 | 给出能真实推动路由与落盘裁决的启发式 | S3 | 启发式有效性 | FAIL-SCRIPT-STR-03 |
| FIELD-SCRIPT-ROUTE-04 | 阶段裁决.唯一路由 | 说明本轮唯一主子路径、排除 sibling 的理由、是否偏离默认顺序 | S4 | 路由稳定性 | FAIL-SCRIPT-ROUTE-04 |
| FIELD-SCRIPT-LAND-05 | 阶段裁决.Canonical Landing | 固定单一主文件、允许改动的写位和禁止平行稿规则 | S5 | 真源单一性 | FAIL-SCRIPT-LAND-05 |
| FIELD-SCRIPT-SIDE-06 | 阶段裁决.侧车与验收闭环 | 明确子路径证据目录、`validation-report.md` 与阶段级留口 | S5-S6 | 闭环完整性 | FAIL-SCRIPT-SIDE-06 |
| FIELD-SCRIPT-REFL-07 | 模块.工具后反思 | 说明读取文件、顾问团反馈或验收结果后如何决定继续/回退/改路由 | S6 | 反思闭环 | FAIL-SCRIPT-REFL-07 |
| FIELD-SCRIPT-GATE-08 | 模块.Gate Summary | 给出 PASS/WARN/FAIL 状态、unknowns、confidence 与返工入口 | S7 | 验收可执行性 | FAIL-SCRIPT-GATE-08 |
| FIELD-SCRIPT-WBK-09 | 父级回写可见性 | 确保 `SKILL.md`、`references/`、`CONTEXT.md` 和报告能相互回链 | S8 | 回写可见性 | FAIL-SCRIPT-WBK-09 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S0 | FIELD-SCRIPT-MOD-01 | 这轮是在优化旧链、补新链，还是做推理模型适配 | 判定模式并记录理由 | 默认跳过模式判定 |
| S1 | FIELD-SCRIPT-IDN-02 | 本轮真正服务哪一个阶段级判断 | 写阶段终局句、消费者、保护约束 | 只剩“继续扩写”口号 |
| S2 | FIELD-SCRIPT-IDN-02 | 当前输入链是否足够支撑阶段裁决 | 锁 grouped source、主文件、组间 handoff、子路径状态、顾问团状态 | 没读证据就判路由 |
| S3 | FIELD-SCRIPT-STR-03 | 哪些启发式真的能推动父级裁决 | 写启发式工作链并删掉空泛流程词 | 仍是“先做 A 再做 B”式脚本 |
| S4 | FIELD-SCRIPT-ROUTE-04 | 当前为什么进这个子路径，而不是其他层 | 形成唯一路由裁决与排除理由 | 多个 sibling 同时成立却不收窄 |
| S5 | FIELD-SCRIPT-LAND-05, FIELD-SCRIPT-SIDE-06 | 当前判断如何落到单一主文件、侧车与验收位 | 固定写位、侧车目录、阶段验收与禁止项 | 又长出平行稿或无证据落点 |
| S6 | FIELD-SCRIPT-REFL-07 | 新证据回来后是继续、回退还是改路由 | 写工具后反思与顾问团反思条件 | 证据变化后仍机械推进 |
| S7 | FIELD-SCRIPT-GATE-08 | 本轮如何验收、失败时回到哪里 | 输出 Gate Summary、unknowns、confidence、rework entry | 没有 PASS/WARN/FAIL 与返工入口 |
| S8 | FIELD-SCRIPT-WBK-09 | 本轮升级是否被父级可见吸收 | 回写 `references/`、必要的 `CONTEXT.md` 和设计报告 | 文档改了但经验层与报告失联 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-SCRIPT-MOD-01 | 模式明确，且与当前父级任务对象匹配 | FAIL-SCRIPT-MOD-01 | S0 |
| FIELD-SCRIPT-IDN-02 | 阶段终局、输入边界与反越权范围清晰 | FAIL-SCRIPT-IDN-02 | S1-S2 |
| FIELD-SCRIPT-STR-03 | 启发式可直接推动 `保留 / 删除 / 收窄 / 落盘 / 返工` 裁决 | FAIL-SCRIPT-STR-03 | S3 |
| FIELD-SCRIPT-ROUTE-04 | 唯一路由明确，排除 sibling 有证据支撑 | FAIL-SCRIPT-ROUTE-04 | S4 |
| FIELD-SCRIPT-LAND-05 | 所有判断回到单一主文件与允许写位 | FAIL-SCRIPT-LAND-05 | S5 |
| FIELD-SCRIPT-SIDE-06 | 侧车目录、验收位与下一入口清楚可追 | FAIL-SCRIPT-SIDE-06 | S5-S6 |
| FIELD-SCRIPT-REFL-07 | 文件/顾问团/验收结果返回后发生真实二次裁决 | FAIL-SCRIPT-REFL-07 | S6 |
| FIELD-SCRIPT-GATE-08 | Gate Summary 完整，含状态、未知项、置信度与返工入口 | FAIL-SCRIPT-GATE-08 | S7 |
| FIELD-SCRIPT-WBK-09 | 主合同、模块细则、经验层与报告之间回链完整 | FAIL-SCRIPT-WBK-09 | S8 |

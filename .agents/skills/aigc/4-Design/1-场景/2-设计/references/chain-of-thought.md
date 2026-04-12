# Field Master

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| FIELD-SCN-DES-01 | 技能包.输入真源 | 锁定 `1-清单`、`2-Global`、`3-Detail`、`Init` 的读取顺序与回退规则 | scene catalog、全局风格、导演证据、初始化预设 | S1 | 真源一致性 | FAIL-SCN-DES-01 |
| FIELD-SCN-DES-02 | 技能包.拓扑合同 | 明确 `设计统筹 -> specialist 并行 -> review/audit -> 父 skill 写回` 的 mixed tranche | team.md、角色合同、任务依赖 | S2 | 编排可执行性 | FAIL-SCN-DES-02 |
| FIELD-SCN-DES-03 | 技能包.交接合同 | 定义 `mission_brief / context_packet / agents_plan / patch / note / report` 命名与父子边界 | 父 skill、team.md、templates | S3 | 交接清晰度 | FAIL-SCN-DES-03 |
| FIELD-SCN-DES-04 | 技能包.场景设计卡字段 | 锁定设计之向、反向禁忌、空间原型、建筑/布景/动线/镜头与 prompt handoff | template、specialist patch、scene evidence | S4 | 设计可消费性 | FAIL-SCN-DES-04 |
| FIELD-SCN-DES-05 | 技能包.收束写回 | 定义 per-scene `.md` 与 episode 级 `场景设计.json` 的单一真源写回 | output-template、父 skill synthesis | S5 | 真源收束性 | FAIL-SCN-DES-05 |
| FIELD-SCN-DES-06 | 技能包.审景与审计 | 定义 reviewer / auditor veto、trace 与返工入口 | 审景师、真源审计、CONTEXT | S6 | 闭环完整性 | FAIL-SCN-DES-06 |
| FIELD-SCN-DES-07 | 技能包.面板接续 | 定义未来 `3-面板` / `5-Image` 消费的最小 handoff 字段 | panel_handoff、final_scene_prompt | S7 | 下游可接续性 | FAIL-SCN-DES-07 |

# Thought Pass Map

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SCN-DES-01 | 读取顺序是否先 scene catalog 再其他证据 | 锁定主输入与回退输入 | 直接绕过 `1-清单` |
| S2 | FIELD-SCN-DES-02 | subagents 到底如何串并行和后台执行 | 写出 tranche、precedence、veto | 只说“多角色协作” |
| S3 | FIELD-SCN-DES-03 | 父子之间如何交接 | 固化 brief/patch/note/report | 输出名称混乱或越权 |
| S4 | FIELD-SCN-DES-04 | 哪些字段必须由谁补齐 | 绑定模板字段与角色 owned fields | 设计卡缺关键空间字段 |
| S5 | FIELD-SCN-DES-05 | 谁写最终文件 | 定义父 skill synthesis 与落盘 | subagents 直接写主稿 |
| S6 | FIELD-SCN-DES-06 | 如何复核与追因 | 定义 review / audit gate | 没有 veto 或 trace |
| S7 | FIELD-SCN-DES-07 | 怎样保证可给下游消费 | 固定 panel_handoff / final_scene_prompt | 下游还要重新猜字段 |

# Pass Table

| field_id | 质量维度 | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- | --- |
| FIELD-SCN-DES-01 | 真源一致性 | 读取顺序明确，`1-清单` 是首选输入 | FAIL-SCN-DES-01 | S1 |
| FIELD-SCN-DES-02 | 编排可执行性 | mixed tranche、后台 subagents、veto 规则明确 | FAIL-SCN-DES-02 | S2 |
| FIELD-SCN-DES-03 | 交接清晰度 | brief/patch/note/report 与 handoff target 明确 | FAIL-SCN-DES-03 | S3 |
| FIELD-SCN-DES-04 | 设计可消费性 | 场景设计卡字段齐全且角色边界清楚 | FAIL-SCN-DES-04 | S4 |
| FIELD-SCN-DES-05 | 真源收束性 | 只有父 skill 写 `场景设计.json` 与 `<scene_key>.md` | FAIL-SCN-DES-05 | S5 |
| FIELD-SCN-DES-06 | 闭环完整性 | review / audit 可否决并给 trace | FAIL-SCN-DES-06 | S6 |
| FIELD-SCN-DES-07 | 下游可接续性 | 已保留 panel / image 可用 handoff 字段 | FAIL-SCN-DES-07 | S7 |

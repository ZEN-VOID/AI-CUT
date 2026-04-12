# Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SCN-PANEL-01 | 阶段定位 | 明确 `3-面板` 消费 `2-设计`，只输出 panel carrier，不越权出图 | S1 | 边界清晰度 | FAIL-SCN-PANEL-01 |
| FIELD-SCN-PANEL-02 | 输入锚点 | 锁定 `场景设计.json + 逐场景设计卡 + 模板` | S2 | 输入完备性 | FAIL-SCN-PANEL-02 |
| FIELD-SCN-PANEL-03 | prompt 收束 | 形成 `identity_badge + panel_prompt + negative_prompt` | S3 | prompt 可执行性 | FAIL-SCN-PANEL-03 |
| FIELD-SCN-PANEL-04 | 布局合同 | 固定 `16:9 + 3x3 + 9 panel` | S4 | 布局一致性 | FAIL-SCN-PANEL-04 |
| FIELD-SCN-PANEL-05 | canonical carrier | `场景面板.json + <scene_key>-layout.json` 同源且可回链 | S5 | 输出完整性 | FAIL-SCN-PANEL-05 |
| FIELD-SCN-PANEL-06 | handoff 闭环 | 指向 `5-Image / 人工审阅` 的下一入口与 triad closure | S6 | 交接可执行性 | FAIL-SCN-PANEL-06 |

# Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SCN-PANEL-01 | 当前是不是 `3-面板` 问题 | 锁定阶段边界和不拥有内容 | 开始补场景设计或直接出图 |
| S2 | FIELD-SCN-PANEL-02 | 输入是否足以做面板 | 核对 `scene_designs[]`、模板和路径 | 缺 `scene_key` 或缺设计 carrier 仍继续 |
| S3 | FIELD-SCN-PANEL-03 | prompt 是否来自设计真源并带禁区 | 生成 `panel_prompt` 与 `negative_prompt` | 把上游大段原文照抄或丢负面约束 |
| S4 | FIELD-SCN-PANEL-04 | 九宫格布局是否稳定 | 固定 aspect ratio、grid、panel count | 输出结构漂移为任意布局 |
| S5 | FIELD-SCN-PANEL-05 | episode 与 per-scene carrier 是否同源 | 写 `场景面板.json` 与逐场景 layout | 只有单文件或多文件互不回链 |
| S6 | FIELD-SCN-PANEL-06 | 如何证明本轮完成或阻塞 | 输出 manifest、triad closure 与下一入口 | 没有下游 handoff 或 closure |

# Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-SCN-PANEL-01 | 阶段边界、上下游职责与输出真源明确 | FAIL-SCN-PANEL-01 | S1 |
| FIELD-SCN-PANEL-02 | 输入根、模板与 scene selection 合法 | FAIL-SCN-PANEL-02 | S2 |
| FIELD-SCN-PANEL-03 | prompt/negative prompt 可执行且不漏禁区 | FAIL-SCN-PANEL-03 | S3 |
| FIELD-SCN-PANEL-04 | 16:9 九宫格合同稳定 | FAIL-SCN-PANEL-04 | S4 |
| FIELD-SCN-PANEL-05 | JSON carrier 同源、命名稳定、可回链 | FAIL-SCN-PANEL-05 | S5 |
| FIELD-SCN-PANEL-06 | triad closure 与下一入口明确 | FAIL-SCN-PANEL-06 | S6 |

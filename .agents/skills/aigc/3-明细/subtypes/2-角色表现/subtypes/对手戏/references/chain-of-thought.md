# aigc 3-明细 / 2-角色表现 / 对手戏 / Chain Of Thought

本文件承载 `aigc 3-明细 / 2-角色表现 / 对手戏` 的字段主表、思维链与返工入口真源。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-RVL-SRC-01 | 执行报告.来源卡 | 锁定场次、组别、冲突对象与 handoff | S1 | 来源可追溯性 | FAIL-RVL-SRC-01 |
| FIELD-RVL-CONFLICT-02 | 执行报告.冲突卡 | 写清双方目标、底牌、阻力与关系温差 | S2 | 冲突清晰度 | FAIL-RVL-CONFLICT-02 |
| FIELD-RVL-TURN-03 | 终稿.回合梯度 | 让对话有轮次推进与攻防升级 | S3 | 轮次推进力 | FAIL-RVL-TURN-03 |
| FIELD-RVL-SUBTEXT-04 | 终稿.潜台词与停顿 | 补停顿、打断、回避、反问与潜台词 | S4 | 潜台词密度 | FAIL-RVL-SUBTEXT-04 |
| FIELD-RVL-VISUAL-05 | 终稿.对位反应与背景锚 | 为关键回合补主位、反位与背景差异 | S5 | 可拍对位性 | FAIL-RVL-VISUAL-05 |
| FIELD-RVL-OUTCOME-06 | 执行报告.回合结算与留口 | 说明关系变化、场景结算与后续交接 | S6-S7 | 闭环可执行性 | FAIL-RVL-OUTCOME-06 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-RVL-SRC-01 | 这场对手戏从哪来 | 锁定场次/组别/hand off | 没有来源就开始改对白 |
| S2 | FIELD-RVL-CONFLICT-02 | 双方到底在争什么 | 写目标、底牌、阻力 | 只有台词，没有冲突卡 |
| S3 | FIELD-RVL-TURN-03 | 回合是否在推进 | 重排回合梯度 | 每轮都一样重 |
| S4 | FIELD-RVL-SUBTEXT-04 | 潜台词如何显形 | 补停顿、打断、回避、反问 | 对话全是直给信息 |
| S5 | FIELD-RVL-VISUAL-05 | 画面如何支撑正反打理解 | 补主位、反位与背景锚 | 对话只有嘴，没有场 |
| S6 | FIELD-RVL-OUTCOME-06 | 关系温度怎么变了 | 写回合结算 | 说了很多，关系没变 |
| S7 | FIELD-RVL-OUTCOME-06 | 后续谁来接 | 写留给空间/镜头层的问题 | 所有问题都硬留在本层 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-RVL-SRC-01 | 来源明确，可回查上游证据 | FAIL-RVL-SRC-01 | S1 |
| FIELD-RVL-CONFLICT-02 | 双方目标/底牌/阻力清楚 | FAIL-RVL-CONFLICT-02 | S2 |
| FIELD-RVL-TURN-03 | 回合有推进，不平铺 | FAIL-RVL-TURN-03 | S3 |
| FIELD-RVL-SUBTEXT-04 | 潜台词、停顿与打断有效 | FAIL-RVL-SUBTEXT-04 | S4 |
| FIELD-RVL-VISUAL-05 | 主位/反位/背景锚可支撑对位 | FAIL-RVL-VISUAL-05 | S5 |
| FIELD-RVL-OUTCOME-06 | 关系结算与留口清楚 | FAIL-RVL-OUTCOME-06 | S6-S7 |

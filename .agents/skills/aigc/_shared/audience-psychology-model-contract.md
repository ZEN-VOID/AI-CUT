# Audience Psychology Model Contract

## Purpose

定义观众心理模型：在每个关键叙事 beat，系统回答"观众此刻知道什么、期待什么、害怕什么、渴望什么"。本合同为全链路（编剧→导演→表演→摄影）提供统一的观众心理参照层，让每个创作决策都不只是"角色在做什么"，而是"观众此刻会如何感受"。

## Ownership

- 本文件拥有观众心理状态定义、信息状态矩阵、期待管理策略、冲突遗产传递和跨阶段消费规则。
- 各阶段消费 `audience_psychology_map` 作为创作判断的参照层。

---

## Audience State Matrix

每个关键 beat 必须回答以下五轴：

| axis | 创作问题 | 证据 |
| --- | --- | --- |
| `audience_knowledge` | 观众此刻知道什么信息？ | 已释放信息清单、信息来源标注 |
| `audience_expectation` | 观众此刻期待什么发生？ | 承诺-兑现追踪：被承诺了什么、兑现了多少 |
| `audience_fear` | 观众此刻害怕什么发生？ | 风险锚点：什么威胁被建立、什么代价被暗示 |
| `audience_desire` | 观众此刻渴望什么被满足？ | 情感欠账：什么关系等待修复、什么正义等待伸张 |
| `audience_surprise_potential` | 什么信息/事件会让观众意外？ | 信息差地图：哪些观众以为自己知道但可能是错的 |

### 使用规则

- **不要求每场都填满五轴**。低信息过场只需回答 `audience_knowledge`（观众此刻的信息基线不被破坏即可）。
- **关键场景（高潮、转折、揭示）必须五轴全填**，且 `audience_expectation` 和 `audience_surprise_potential` 必须有明确的创作决策。
- **"观众已经知道了"是最常被忽略的判断**。编剧和导演容易重复释放观众已知信息，浪费银幕时间。

---

## Conflict Legacy Transfer

跨集冲突遗产传递机制，确保各阶段使用统一的冲突词汇：

| field | description |
| --- | --- |
| `active_conflicts` | 当前集中活跃的冲突清单（人物 vs 人物 / 人物 vs 规则 / 人物 vs 自我） |
| `resolved_conflicts` | 本集解决的冲突（及其解决方式：胜负/妥协/和解/代价） |
| `newly_introduced_conflicts` | 本集新增的冲突 |
| `inherited_conflicts` | 从上游集继承、本集未解决的冲突 |
| `conflict_state_at_exit` | 本集结束时各冲突的状态（升级/冻结/缓解/转向） |

### 使用规则

- **2-编剧** 在 N4-FIELD 阶段标记冲突继承状态，不做新增或解决
- **3-导演** 在 N3-DIR-SUBSTANCE 阶段消费并深化冲突压力设计，在 N8-DIR-FINAL-IMAGE 阶段标记冲突遗产
- **4-表演** 在 N5-PERF-SCENE-CRAFT 阶段消费冲突状态决定表演张力层级
- **5-摄影** 在 N5.5-PEAK-SHOT 阶段消费冲突状态决定高点策略

---

## Per-Stage Consumption Nodes

| stage | node | consumption_action |
| --- | --- | --- |
| 2-编剧 | N4-FIELD | 在字段分流时标记观众此刻的知识基线；标注信息差类型（观众知道角色不知道 / 角色知道观众不知道 / 双方都不知道） |
| 2-编剧 | N4.2-NOVEL-TRANSFORM | 确保小说转译不消除信息差：不把"观众应该不知道"的信息提前泄露 |
| 2-编剧 | N6-SCRIPT-REVIEW | 检查：关键场景是否有观众心理标注 |
| 3-导演 | N3-DIR-SUBSTANCE | 建立 `audience_psychology_map`：每个关键 beat 的观众知识、期待、恐惧、渴望 |
| 3-导演 | N4-DIR-PEAK | 消费 audience_expectation 决定满足/延迟/反高潮策略 |
| 3-导演 | N10-DIR-REVIEW | 检查：高潮画面是否回应了观众期待或有意颠覆 |
| 4-表演 | N5-PERF-SCENE-CRAFT | 消费 audience_expectation 决定表演的"知情"层级：角色是否应该表现出比观众更多的知道/更少的知道 |
| 5-摄影 | N5.5-PEAK-SHOT | 消费 audience_fear 和 audience_desire 决定高点画面的注意力引导方向 |
| 5-摄影 | N6.4-FUNCTIONAL-PROJECTION | 消费 audience_surprise_potential 决定镜头的揭示/隐藏/误导策略 |

---

## Failure Modes

| symptom | root_cause | fix |
| --- | --- | --- |
| 观众在高潮时刻没有感受到满足 | audience_expectation 没有被建立 | 回到上游场景补承诺/期待建立 |
| 观众觉得无聊/已经知道结果 | audience_knowledge 超前于剧情推进 | 削减已知信息重复、增加新信息层 |
| 观众没有被惊到 | audience_surprise_potential 过低 | 增加信息差层级：让观众以为自己知道但可能错了 |
| 观众对角色命运不关心 | audience_desire 没有被建立 | 补充情感欠账：什么关系/正义/渴望在等待 |
| 观众觉得威胁不够真实 | audience_fear 没有被持续锚定 | 补充风险锚点：让威胁定期回到观众注意力中 |

---

## Reusable Heuristics

- 好的影视每时每刻都在管理观众心理，不只是讲故事。编剧的职责是设计"观众什么时候知道什么"，不只是"发生了什么"。
- suspense（观众知道危险但角色不知道）和 mystery（观众不知道真相）是两种完全不同的创作策略，不能混用。
- 观众的期待是最宝贵的货币。轻易兑现=浪费，永远不兑现=失信，延迟兑现后才兑现=最高价值。
- 冲突遗产必须跨集传递。一集结束时，未解决的冲突比已解决的冲突更有续集价值。
- "观众已经知道了"是最高频的创作浪费。不要重复释放信息，要释放新的信息层。

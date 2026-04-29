# Scope Package: Character State

## Selection Signals

- 角色动机、人物关系、阵营、身份、创伤、声纹、人物弧、当前状态、角色选择。

## When X Then Check X

| when | must check |
| --- | --- |
| 改角色动机 | 角色卡、人物历史、章级人物任务、最近选择场景 |
| 改关系转折 | 双方角色卡、关系字段、最近互动章、后续互动章 |
| 改阵营/身份 | 角色卡、组织/势力设定、已披露身份章、后续知情边界 |
| 改声纹/表达 | 声纹表、同卷该角色对白分布、provider prompt、润色稿 |

## Required Impact Additions

- `character_card_refs`
- `relationship_refs`
- `recent_appearance_refs`
- `future_interaction_refs`
- `voiceprint_guardrail`

## Review Gate

- 人物动机、关系动作、知情边界和状态历史一致。
- 声纹变化不把角色写成同一种解释腔。
- 后续章节不再消费旧人物状态。

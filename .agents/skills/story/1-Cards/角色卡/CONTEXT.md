# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 角色很多但撞位 | role bucket | 先修 `narrative_function`，再补设定 | 角色职责先于人设浓度 | 主角色能说明自己推进哪类戏 |
| 成长时间线变成事件流水账 | timeline contract | 改写为成长阶段与认知转折 | 固定 `experience_timeline + timeline_anchor` 双锚点 | 时间线能回答“角色因此变成什么” |
| 专属物接口空心 | downstream interface | 回补 `exclusive_item_hooks` | 角色卡先留接口，物品卡再做适配 | 专属物能一眼看出角色归属 |

## Repair Playbook

1. 先判分桶，再判关系，再判成长，再判专属物接口。
2. 若无法一句话说明“为什么是角色问题”，先退回父技能。
3. 先修结构，再补风格表达。

## Reusable Heuristics

- 角色卡最值钱的是职责、关系和成长，不是设定名词数量。
- `exclusive_item_hooks` 越早稳定，物品卡越不容易模板化。

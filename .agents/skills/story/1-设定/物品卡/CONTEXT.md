# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 重要物没有归属也没有代价 | item closure | 回补 `ownership_links + usage_rules.costs` | 重要物最小三元组固定为“归属 + 功能 + 代价” | 物品能回答属于谁、做什么、付什么 |
| 专属物模板化 | upstream interface | 回读角色接口与场景限制，再补 `exclusive_fit` | 物品卡默认把角色/场景当硬输入 | 专属物像角色本人，不像通用装备 |
| 线索物与重要叙事物混桶 | bucket contract | 按剧情作用重分桶 | 线索负责发现，叙事物负责改局 | 两类物品的剧情用途清晰分离 |
| 长篇项目物品总数踩到 profile 下限以下 | coverage gate | 补一件能改变局面的线索物或叙事物，不用装饰物凑数 | 物品收束后必须回跑 coverage validator，看 `total_count` 是否过线 | `FAIL-CARDS-ITEM-TOTAL` 消失 |

## Repair Playbook

1. 先判剧情杠杆，再判归属与代价，再判专属适配。
2. 若不清楚为何是物品问题，先回父技能。
3. 先修结构，再补材质与风格。

## Reusable Heuristics

- 物品卡最值钱的是“为什么非它不可”，不是名词密度。
- 专属物是否成立，取决于欲望、行动方式和代价结构，不只取决于外观。
- 若项目是长篇高密度结构，优先补“证据链起点物”或“权力流程物”，它们比纯兵器更能稳住 planning 和 drafting。

# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 风格卡只剩题材卖点和禁区 | style projection gap | 先把上游 `reader_promise / aesthetic_axes / style_system` 投射成 `总体基调 + 叙事/对白/画面/语言/场面风格` | 固定“风格卡输出写法合同，而不是 pitch 摘要” | 风格卡能回答“这本书该怎么写” |
| 风格卡只有抽象形容词，没有写法抓手 | writing-style closure | 回补 `narrative_style / dialogue_style / visual_style / prose_style / scene_style` | 风格卡至少要覆盖总体基调、叙事风格、对白风格、画面风格 | Drafting 能直接引用风格卡落笔 |
| 角色边界或世界规则混进风格卡 | boundary layering | 把人物底线退回角色卡，把规则体系退回全局卡 | 固定“风格卡只持有写法，不兜底人物规则和世界机制” | 风格卡不再承担角色/全局真源 |
| 下游无法引用风格契约 | downstream ref | 回补 `style_contract_refs` 与索引路径 | 固定风格卡索引必须保存正式契约引用 | 下游能用单一 ref 找到风格卡 |

## Repair Playbook

1. 先判是不是风格问题，再判是“总体基调”还是“写法骨架”失真。
2. 若上游真源不足，先回 `north_star.json`，不在风格卡里即兴补世界观。
3. 先修 `style_identity / experience_contract`，再修叙事、对白、画面、语言、场面风格。

## Reusable Heuristics

- 风格卡最值钱的是“如何写出这本书”，不是“列出几个好看的形容词”。
- `reader_promise / aesthetic_axes / style_system` 是风格卡的上游种子，不是风格卡最终字段本体。
- 对小说来说，“总体基调、叙事风格、对白风格、画面风格”应该是风格卡主骨架，而不是补充备注。

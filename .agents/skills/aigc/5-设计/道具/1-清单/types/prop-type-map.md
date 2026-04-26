# Prop Type Map

## Type Variables

| type_id | signal | merge_strategy | filter_strategy |
| --- | --- | --- | --- |
| `PROP-NARRATIVE` | 推动行动、承载线索、被角色争夺或使用 | 同一功能优先归并 | 保留 |
| `PROP-RULE` | 与禁忌、仪式、能力、系统规则相关 | 状态变化通常归并，规则变化可拆分 | 保留 |
| `PROP-VISUAL-HOOK` | 被特写、重复出现、颜色或形态强烈 | 别名归并到最稳定称呼 | 保留 |
| `PROP-GEN-LOCK` | 后续图像/视频需保持一致 | 按设计一致性归并 | 保留 |
| `PROP-BACKGROUND` | 普通陈设、空间构件、无特写杂物 | 不进入主体清单 | 默认过滤 |
| `PROP-ALIAS` | 代称、短称、持有者称呼、状态称呼 | 回查同组正文后归并 | 不单独列项 |

## Routing

- `PROP-NARRATIVE`、`PROP-RULE`、`PROP-VISUAL-HOOK`、`PROP-GEN-LOCK` 进入清单。
- `PROP-ALIAS` 进入归并裁决，不直接输出。
- `PROP-BACKGROUND` 仅在用户明确要求或存在生成锁定理由时保留，并在报告说明。

## Naming Policy

canonical `名称` 应短、稳定、可复用。避免把一次性状态、持有者动作或长句描述写进名称；这些信息应压入 `原文描述（关键词式）`。

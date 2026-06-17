# Character List Heuristics

## Practical Heuristics

- 先保留原始称呼，后做归并；过早改名会丢失别名证据。
- 首次登场以归并后的主体为准，不以最终显示名称第一次出现为准。
- 群体角色要问“后续是否需要设计资产”；如果只是气氛背景，不应污染角色清单。
- 同一角色的少年期、老年期、战斗态、战损态、受伤态、礼服、制服、伪装等应先问“是不是同一叙事主体的资产变体”，默认不要拆成新角色。
- 关键词描述要能帮助下一阶段识别人物，不要提前替下一阶段设计人物。
- 遇到 YAML 与正文不一致，优先记录风险，不在本阶段私自修复上游。

## Repair Hints

- 清单重复时，先检查 `名称` 单元是否可吸收别名，而不是新增列。
- 清单漏项时，回到 registry `subjects.characters` 和 source anchors 扫描，不要从剧情记忆补项。
- 首次登场错误时，按 `episode_file -> group_id -> YAML order` 重新排序候选证据。
- 描述过长时，删掉推断句，保留可复查关键词。
- 设计阶段需要多状态资产时，清单保持三列，在描述中加短标签或在 `design-manifest.yaml.character_variants` 中补 sidecar，不新增清单列。

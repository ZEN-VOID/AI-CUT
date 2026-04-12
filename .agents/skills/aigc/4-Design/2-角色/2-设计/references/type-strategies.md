# Type Strategies

## Role Tier Strategy

| role_tier | 设计深度 | 默认 specialist | 说明 |
| --- | --- | --- | --- |
| `lead` | full | 全部 | 主角必须完整输出全部槽位 |
| `support` | high | 全部 | 配角可精简辅助字段，但视觉锚点与穿搭系统不能缺 |
| `featured-crowd` | medium | `形象建模 + 服装设计 + 个性塑造` | 有辨识要求的群像角色可以弱化妆容颗粒度 |
| `crowd` | lite | `设计统筹 + 形象建模 + 服装设计` | 纯群演只保留识别锚点、阶层穿搭与禁区 |

## World Mode Strategy

| world_mode | 重点 | 约束 |
| --- | --- | --- |
| `historical` | 制式、材质、阶层、文化痕迹 | 禁止现代时装语言偷渡 |
| `modern` | 职业、生活方式、现实可穿性 | 避免过度奇观化 |
| `fantasy` | 世界观符号、辨识度、视觉夸张度 | 仍需保留角色 identity 与 evidence anchor |
| `stylized` | 轮廓、色块、角色气场 | 避免只剩空泛风格词 |

## Conflict Tie-Break

1. `角色清单.json` 的 canonical identity 优先。
2. `2-Global` 的项目级风格与类型指导高于单次镜头修辞。
3. `3-Detail/第N集.json` 的镜头证据高于设计组臆测。
4. 若两条证据冲突，优先保守设计，并在 `report` 说明。

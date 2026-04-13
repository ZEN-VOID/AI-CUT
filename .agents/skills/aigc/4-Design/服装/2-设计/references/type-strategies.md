# Type Strategies

## Costume Scope Strategy

| scope | 设计深度 | 默认 agents | 说明 |
| --- | --- | --- | --- |
| `hero-costume` | full | 全部 | 主视觉服装必须完整输出全部槽位 |
| `support-costume` | high | 全部 | 配角服装可精简部分 panel 话术，但设计主稿不能缺 |
| `variant-costume` | high | `廓形层次设计师 + 配饰连续性设计师 + 提示词架构师` | 同角色状态变体优先保证 continuity |
| `background-costume` | lite | `服装统筹 + 廓形层次设计师 + 材质纹样设计师` | 群像服装保留阶层穿搭与禁区即可 |

## World Mode Strategy

| world_mode | 重点 | 约束 |
| --- | --- | --- |
| `historical` | 制式、织造、阶层、礼制 | 禁止现代剪裁和时尚词偷渡 |
| `modern` | 职业、实穿性、场景功能 | 避免过度奇观化 |
| `fantasy` | 世界观符号、层次夸张、仪式感 | 仍需保留角色 identity 与时代锚点 |
| `stylized` | 廓形、色块、图案节奏 | 避免只剩空泛风格词 |

# Payoff Genre Type Map

本文件承载章级爽点设计的类型画像。它用于避免不同类型小说被写成同一种爽法；执行时先形成 `genre_payoff_profile`，再进入 `references/chapter-payoff-rules.md` 与 `steps/N4-CHAPTER-PAYOFF`。

## Loading Boundary

- 本文件只负责类型画像和口味校准，不替代 `references/chapter-payoff-rules.md` 的爽点合同。
- 若项目根、整体规划或卷规划已经声明主类型，以项目/上游声明优先。
- 若上游没有声明，章级只能根据已有设定做临时 `genre_payoff_profile`，并在输出中标注为 planning inference。

## Type Variables

| variable | allowed values | meaning |
| --- | --- | --- |
| `genre_payoff_profile` | `xuanhuan_fantasy`, `wuxia_xianxia`, `urban_power`, `mystery_suspense`, `romance`, `comedy_slice`, `political_strategy`, `horror_weird`, `hybrid`, `custom` | 当前章爽点的类型画像 |
| `subgenre_modifier` | free text | 项目或本章的子类型修饰，如学院、末世、修仙、甜宠、赛博、群像、克苏鲁等 |
| `payoff_taste` | free text | 本类型下读者期待的爽法口味 |
| `payoff_taboo` | free text | 本类型下容易串味、破坏承诺或削弱读者满足的做法 |
| `payoff_variation_axis` | free text | 所有高潮点在多章中的差异轴，用于避免同类爽点重复 |
| `duel_variation_axis` | free text | 高超对决在多章中的差异轴，用于避免同质化 |

## Genre Matrix

| genre_payoff_profile | reader expectation | likely payoff modes | avoid |
| --- | --- | --- | --- |
| `xuanhuan_fantasy` | 境界、法则、资源、奇观、命运和强者秩序被改写 | 高超对决、法则碰撞、境界压制、禁忌显影、奇境体验 | 把高能章写成普通打架，或把力量体系写得没有规则 |
| `wuxia_xianxia` | 招式、身法、心法、侠义、师承、江湖因果 | 招式拆解、剑意对撞、侠义抉择、心魔、江湖烟火 | 只有数值碾压，没有技艺与心气 |
| `urban_power` | 身份、资源、阶层、反制、现实场景翻盘 | 打脸反制、身份亮明、商业/职场行动、暧昧拉扯 | 爽点脱离现实规则，或角色忽然玄幻化 |
| `mystery_suspense` | 线索、误判、证据、心理压力和真相逼近 | 谜面推进、追捕反制、证据争夺、认知震荡 | 过早揭底，或用无因奇观破坏推理承诺 |
| `romance` | 关系变化、情绪确认、亲密距离和误会压力 | 保护行动、暧昧升温、吃醋、告白前压力、陪伴照顾 | 用外部大场面盖过关系变化 |
| `comedy_slice` | 轻松、趣味、反差、生活质感和小满足 | 小比赛、小反击、手艺展示、误会升级、治愈日常 | 突然高压破坏轻盈口味 |
| `political_strategy` | 棋局、权力、筹码、阵营、忠诚和背叛 | 棋局落子、谈判交锋、局部清算、忠诚测试 | 只写热血行动，不写筹码和后果 |
| `horror_weird` | 异常、污染、禁忌、逃生和认知不稳 | 逃生反制、禁忌显影、精神污染、安全屋喘息 | 把怪异解释得太干净，或把恐惧写成普通战斗 |
| `hybrid` | 主类型和副类型的混合期待 | 先锁主类型，再允许副类型补味 | 主副类型互相抢主导，导致爽点口味混乱 |
| `custom` | 用户或项目自定义期待 | 按项目 `MEMORY.md`、整体规划或卷规划裁决 | 临时套用通用类型清单 |

## Review Gate

- `本章爽点设计` 必须写出 `genre_payoff_profile`。
- `payoff_mode` 必须适配 `genre_payoff_profile`；若反类型写法是有意为之，必须在 `exaggeration_logic` 或 `aftertaste_hook` 中说明它如何服务项目承诺。
- 每个高潮点必须写出 `payoff_variation_axis`；若近邻章节使用同类 `payoff_mode`，至少说明两个差异轴。
- 高超对决不是所有类型都等于武斗；在权谋中可以是谈判/棋局，在悬疑中可以是追捕/推理，在日常中可以是手艺/小比赛。
- 当 `payoff_mode` 包含高超对决时，必须写出 `duel_variation_axis`，并说明它与近邻章节至少两个维度不同：对手类型、对决场域、胜负目标、胜法、代价或情绪色彩。

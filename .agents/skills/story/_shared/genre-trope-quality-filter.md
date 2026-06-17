# Genre Trope Quality Filter

本文件是 story 起草阶段加载题材类型包时的质量过滤层。类型包提供题材原料、读者期待和常见桥段，不拥有压过 `north_star.genre_contract`、项目风格卡、角色卡、关系线、场景真实性和当前章 planning 的命令权。

## Hard Rules

1. 类型包中的桥段、爽点、节奏密度和示例句只作为可选素材，不得机械套用。
2. 禁止把固定频率公式写成硬门槛，例如“每 2000 字必须一个爽点”；真正的节奏由当前章冲突、人物代价、场景压力和章末牵引决定。
3. 禁止把“收美女”、性别占有、群众震惊、脸色大变、反派降智、纸片配角、纯碾压杀戮或无代价升级当作默认奖励。
4. 任何爽点必须至少绑定一项：人物欲望、人物缺陷、代价、关系压力、世界规则、局势后果、伏笔兑现或读者长期期待。
5. 若题材包示例与项目 `MEMORY.md`、`north_star.style_contract`、角色动机或场景真实性冲突，以项目真源优先。
6. 类型包不得把正文变成套路展示清单；所有题材元素必须进入人物行动、对白潜台词、现场发现和章末牵引。
7. 类型化场面强化必须先判 `project_genre_axis + scene_function_axis`，不得把动作/武侠当作默认强化，也不得把言情、玄幻、恐怖、悬疑、现实等题材压成同一种“更刺激”写法。

## Preferred Conversion

| 低级套法 | 高级转译 |
| --- | --- |
| 主角装逼，众人震惊 | 主角用有代价的选择改变局势，旁人反应暴露社会规则或利益裂缝 |
| 反派突然降智挑衅 | 反派基于身份、恐惧、利益和错误信息做出可理解的误判 |
| 收美女 | 关系线阶段性推进：信任、误读、试探、债务、共同风险或价值观冲突 |
| 每隔固定字数一个爽点 | 由场景压力、信息揭示、行动代价和章末牵引自然形成节奏 |
| 脸色大变/倒吸冷气 | 动作停顿、物件误触、呼吸变化、视线偏移、退半步或话语断裂 |
| 所有高潮都写成打斗 | 按场景功能转译：关系拉扯、规则显影、威胁遮蔽、线索揭示、制度压力或动作对抗 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 类型包是否被机械套用为正文公式？ | trope quality gate | `FAIL-TROPE-01` | `3-初稿/types/type-map.md` + 当前 lane prompt | offending excerpt、type_package_ref |
| 爽点是否绑定人物、代价、关系或局势后果？ | payoff quality gate | `FAIL-TROPE-02` | `7-追读力强化` / `3-场景和氛围渲染` | payoff note、missing consequence |
| 关系线是否被写成占有式奖励？ | relationship dignity gate | `FAIL-TROPE-03` | `5-对白优化` / `6-心理活动描写` | relationship excerpt |
| 是否出现群众震惊、脸色模板和纸片配角堆叠？ | prose dignity gate | `FAIL-TROPE-04` | `8-润色` / `4-角色形象刻画` | trope markers |
| 类型化场面是否被压成单一武侠/动作模板，或无视项目题材契约？ | genre-scene quality gate | `FAIL-TROPE-05` | `3-初稿/references/genre-scene-drafting-contract.md` / `4-润色/types/genre-scene-repair.md` | `genre_scene_route`、offending excerpt |

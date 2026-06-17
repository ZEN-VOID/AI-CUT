# Character Presence Contract

本文件把旧影视“表演强化”的可取部分迁移为小说初稿的“人物在场反应”规则。它只服务 `3-初稿/SKILL.md#N5-CREATIVE-DRAFT`，不得成为独立阶段、平行正文真源或整章二次表演层。

## Core Principle

人物不是在“表演情绪”，而是在当前压力、欲望、关系和身份限制下做出可读反应。正文只写读者能从行动、对白、停顿、物件接触、视线、呼吸、身体姿态和空间退让中读出的结果。

## Presence Checks

每个关键人物反应至少经过以下内部判断，按当前段落需要选择进入正文：

| check | requirement |
| --- | --- |
| `pressure_anchor` | 反应必须回指当前事件压力、关系压力、任务压力或信息压力。 |
| `desire_or_fear` | 人物反应要能看出此刻想要、回避、试探、控制或失守的东西。 |
| `status_and_relationship` | 对白和动作应符合身份、地位、亲疏、亏欠、敌意或依赖关系。 |
| `visible_behavior` | 情绪优先落到手部、呼吸、视线、站位、物件误触、话语断裂、沉默或空间退让。 |
| `voice_subtext` | 对白不能只讲信息；应带有遮掩、试探、反击、退让、命令或求证。 |
| `consequence` | 反应必须推动信息揭示、关系变化、下一步行动或章末牵引。 |

## Prohibitions

- 不写“为了表演而表演”的微表情堆叠。
- 不给每个情绪点机械补齐动作、呼吸、眼神、声音、生理反应。
- 不把小说正文写成演员调度说明、舞台提示或镜头表演批注。
- 不用“他很震惊、她很痛苦、空气凝固”替代具体反应。
- 不让次要人物抢走当前段落的主要戏剧压力。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 关键人物反应是否由当前压力、欲望、关系和身份驱动，而不是机械加表演？ | `character_presence` | `FAIL-DRAFT-PRESENCE-TEXTURE` | `N5-CREATIVE-DRAFT` | `character_presence_profile` |
| 情绪是否落到可读行为、对白潜台词或空间反应，而非脸色捷径和抽象标签？ | `prose_reader_pull` | `FAIL-DRAFT-PROSE-PULL` | `N5-CREATIVE-DRAFT` | offending excerpt |

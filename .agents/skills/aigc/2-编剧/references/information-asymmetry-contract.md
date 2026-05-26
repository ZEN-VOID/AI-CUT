# Information Asymmetry Contract

## Purpose

定义信息差设计：谁在什么时刻知道什么，是悬念、紧张和反转的底层结构。信息差是影视叙事的核心引擎——观众的每一次紧张、满足和意外，都建立在"谁此刻知道什么"的精确设计之上。

## Ownership

- 本合同拥有信息差的定义、分类、逐场景标注规则和跨阶段消费关系。
- 2-编剧 在 N4-FIELD 阶段建立 `information_asymmetry_map`。
- 3-导演 在 N3-DIR-SUBSTANCE 阶段消费并深化为 `audience_psychology_map`。
- 信息差设计不改变剧情事实，只改变信息的释放时机和揭示方式。

---

## Information Categories

| category | 创作含义 | 观众体验 | 典型手法 |
| --- | --- | --- | --- |
| `audience_only` | 只有观众知道，角色不知道（dramatic irony） | 紧张、担忧、焦急——"小心啊！" | 画面揭示角色看不到的危险 |
| `character_only` | 只有某个角色知道，观众和其他角色不知道 | 好奇、猜测——"他为什么这样做？" | 角色的隐秘行动、秘密对话 |
| `shared_known` | 角色和观众都知道 | 期待——"什么时候会爆发？" | 共同面对的威胁、公开的秘密 |
| `hidden_from_all` | 所有人都不知道（mystery） | 悬念——"到底发生了什么？" | 未解之谜、意外发现 |

---

## Per-Scene Information Map

每个关键场景必须标注以下字段：

| field | 创作问题 | 输出 |
| --- | --- | --- |
| `info_state_at_entry` | 进入场景时各角色各自知道什么？ | 角色A知道X不知道Y；角色B知道Y不知道X；观众知道Z |
| `info_revealed_in_scene` | 本场景释放什么新信息给观众或角色？ | 新信息清单 + 谁接收到了 |
| `info_withheld` | 本场景故意隐藏什么信息？ | 被隐藏的信息 + 隐藏方式（不提/转移/误导） |
| `audience_pov_alignment` | 观众此刻与哪个角色的信息状态对齐？ | 与角色A对齐（观众知道A知道的一切）/ 与全知对齐 / 独立于所有角色 |
| `suspense_mechanism` | 本场景使用什么悬念机制？ | suspense / mystery / dramatic_irony / anticipation |

### suspense_mechanism 详解

| mechanism | 定义 | 观众状态 | 创作任务 |
| --- | --- | --- | --- |
| `suspense` | 观众知道危险，角色不知道 | "小心！别开门！" | 建立危险 + 展示角色无知 |
| `mystery` | 观众和角色都不知道真相 | "到底是谁？" | 释放线索 + 保持疑问 |
| `dramatic_irony` | 观众知道真相，角色被蒙在鼓里 | "他不知道对方是凶手..." | 建立错觉 + 暗示真相 |
| `anticipation` | 观众知道会发生什么，期待看到过程 | "我知道他会赢，但怎么赢？" | 铺垫 + 延迟 + 交付 |

---

## Information Asymmetry Escalation Strategy

信息差不是静态的，必须在场景间逐步升级：

### 5级信息差升级模型

| level | 状态 | 创作动作 |
| --- | --- | --- |
| L1-Seed | 种子：一个暗示、一个细节 | 画面中埋一个观众暂时不会注意的信息 |
| L2-Aware | 觉察：观众开始怀疑 | 重复暗示、角色行为不一致 |
| L3-Confirm | 确认：观众确认了某个角色不知道的事 | dramatic irony 建立完成 |
| L4-Tension | 紧张：信息差即将被打破 | 角色接近发现真相、对话逼近边缘 |
| L5-Reveal | 揭示：信息差被打破 | 真相浮出，角色知道观众已知的事 |

### 升级规则

- 不允许从 L1 直接跳到 L5（缺少中间层级会让揭示显得突兀）
- 一个集中至少有一个信息差完成 L2→L4 的升级（否则悬念缺乏推进）
- 信息差揭示后必须产生后果（关系变化/新的信息差/代价），否则揭示是空的

---

## Classic Information Asymmetry Techniques

| technique | 描述 | 使用场景 |
| --- | --- | --- |
| `foreshadowing` | 预兆：在揭示前埋入暗示 | 前期场景的细节、道具、对白中的伏笔 |
| `red_herring` | 烟雾弹：引导观众走向错误结论 | 误导性线索、可疑但无辜的角色 |
| `unreliable_narrator` | 不可靠叙述者：观众看到的不一定是真相 | 主角的内心独白可能有误判 |
| `dramatic_irony` | 戏剧反讽：观众比角色知道得多 | 观众已知角色身份但角色自己不知道 |
| `twist_reveal` | 反转揭示：颠覆观众已有认知 | 打破观众以为自己知道的信息 |
| `slow_burn_disclosure` | 慢烧揭露：极缓慢地释放信息 | 每集释放一小片拼图 |

---

## Consumption Nodes

| stage | node | action |
| --- | --- | --- |
| 2-编剧 | N4-FIELD | 标记每段信息的类别；建立 per-scene information map |
| 2-编剧 | N4.2-NOVEL-TRANSFORM | 确保小说转译不提前泄露 info_withheld |
| 2-编剧 | N5-SCRIPT-DRAFT | 信息差体现在字段的释放顺序中 |
| 2-编剧 | N6-SCRIPT-REVIEW | 检查关键场景是否有信息差标注 |
| 3-导演 | N3-DIR-SUBSTANCE | 消费 info_state 做观众位置判断和戏剧问题设计 |
| 3-导演 | N4-DIR-PEAK | 消费 suspense_mechanism 决定高潮画面的揭示策略 |
| 4-表演 | N5-PERF-SCENE-CRAFT | 消费 audience_pov_alignment 决定角色表演的"知情"层级 |
| 5-摄影 | N6.4-FUNCTIONAL-PROJECTION | 消费 suspense_mechanism 决定镜头的揭示/隐藏/误导策略 |

---

## Failure Modes

| symptom | root_cause | fix |
| --- | --- | --- |
| 观众太早猜到结局 | 信息差升级过快或 foreshadowing 过于明显 | 增加 red_herring 或降低 L2-Aware 的明显程度 |
| 观众在揭示时没有反应 | 信息差没有被 L2-L4 逐步建立 | 补充中间层级的升级步骤 |
| 观众觉得无聊/已经知道所有信息 | audience_pov_alignment 长期与全知对齐 | 切换到 character_only 让观众发现角色有秘密 |
| 信息差揭示后没有后果 | reveal 后缺少关系变化或新冲突 | 补充揭示的代价和后果 |
| 信息过早泄露 | info_withheld 在小说转译中被意外释放 | N4.2-NOVEL-TRANSFORM 必须检查 info_withheld 的保密性 |

---

## Reusable Heuristics

- 信息差是影视悬念的底层代码。谁在什么时刻知道什么，决定了观众的紧张、满足和意外。
- suspense（观众知道危险）和 mystery（观众不知道真相）是两种完全不同的引擎，不能在同一场景混用。
- 观众的期待是最宝贵的货币。轻易揭示=浪费，永远不揭示=失信，延迟揭示后才揭示=最高价值。
- "观众已经知道了"是最高频的创作浪费。不要重复释放信息，要释放新的信息层。
- 最好的反转不是"加一个新信息"，而是"重新解读观众已经知道的信息"。
- dramatic irony 的力量在于：观众看着角色走向危险，想喊但喊不出来。

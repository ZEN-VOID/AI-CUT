# CHANGELOG

## 2026-05-27 (Long Dialogue Delivery Chain)

- 新增长对白表演交付规则：`4-表演` 消费上游 `long_dialogue_beat_map`，形成 `long_dialogue_delivery_map`，逐 beat 标注气口/连续气息、停顿、重音、尾音、身体联动和对手反应。
- 新增 `GATE-PERF-14` / `FAIL-LONG-DIALOGUE-DELIVERY`，阻断把长对白演成同一口气、同一状态、同一反应链的输出。
- 同步更新 `SKILL.md`、actor performance control、workflow、review、模板和经验层；明确本阶段不重新断句、不改写引号内台词。

## 2026-05-22

- 承接 `2-编剧` 新增的正式 `表情特写` 字段：上游已有面部 beat 时必须保留字段并精修，不得吞回泛化 `心理反应`。
- 吸收演技学习视频中“情绪切换瞬间”口径：`actor-performance-control-contract.md` 新增 Emotion Transition Moment Rule，要求关键表演抓触发、裂开、压回和身体联动，而不是持续挂模板表情。
- 收紧环境声承托：声音必须来自场景身份和空间材质，不用泛化 BGM 标签替代表演压力。
- 吸收“角色活人感行为动机”学习：新增单人 `micro_activity/subconscious_response/emotional_landing` 检查和多人 `action_driver/reaction_receiver` 分工，防止角色空闲摆拍、只展示脸部细节或多人同强度抢戏。
- 新增共享合同 `../_shared/lived-in-character-behavior-contract.md`，并同步 `SKILL.md`、表演细则、review 与经验层；该合同只抽象方法，不硬编码示例。
- 新增人物动作链与空间可达性源层：关键表演 beat 必须能交代人物姿态、位置、朝向、动作向量、可达对象和退出状态。
- 新增情绪动作经济规则：强情绪默认收敛为最有效的少数外显动作，不用低信息动作堆叠或无互动环境/道具反应填充表演。
- 新增道具互动准入规则：无互动普通道具不得被硬写成倒影、涟漪、碰撞声或阴影压物等表演承托，除非有角色互动、关键信息/规则/证据/危险源或必要环境交代。
- 同步更新 `SKILL.md`、`CONTEXT.md`、`performance-and-scene-craft-contract.md` 与 review gate，新增 `FIELD-PERF-15` / `GATE-PERF-04` / `FAIL-PERF-15`。
- 将“每段对白必须写清语气情绪、气口、断句等台词表演信息”晋升为 `4-表演` 源层规则。
- 同步更新 `performance-and-scene-craft-contract.md` 的 Dialogue Performance Rule、`actor-performance-control-contract.md` 的 Dialogue Delivery Control、workflow、types、review、模板和机械校验入口。

## 2026-05-13

- 从旧合并阶段拆分初始化 `4-表演` 技能包。
- 承接心理反应可感知化、演员演技控制、场景戏剧功能、潜台词行为化、场面调度和沉默余波。
- 搬入 references：psychological-reaction-contract、performance-and-scene-craft-contract、actor-performance-control-contract。

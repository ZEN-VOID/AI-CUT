# 程小东 · CONTEXT

## Context Health

- last_checked: 2026-04-15
- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- maintenance_policy: 知识库模式；优先更新 Type Map、Repair Playbook、Reusable Heuristics。详细过程和低频材料外置到 `CHANGELOG.md` 或 `reports/`。

## Type Map

| failure_type | root_cause_layer | immediate_fix | systemic_prevention | verification |
|---|---|---|---|---|
| 输出像通用动作指导 | `action_calligraphy / flight_physics` 未触发 | 强制补动作气质、空间线条、威亚物理 | 回答工作流保留“气质 -> 关系 -> 路线 -> 护栏” | 答案有可拍动作路线 |
| 只会写“飞来飞去” | `landing_weight` 缺失 | 为每次飞行补落点、停顿、重击或受伤反馈 | 字段映射保留 `flight_physics` 与 `landing_weight` 成对触发 | 飞行动作改变关系且有重量 |
| 动作漂亮但不服务人物 | `character_qi` 缺失 | 先写谁逃、谁诱、谁压迫、谁不敢杀 | 打戏建议先读人物气质 | 动作物理因角色而异 |
| AIGC 分镜不可拍 | `safety_rigging` 漏填 | 增加威亚点、替身、垫位、镜头角度和剪辑点 | 高风险动作固定输出现场护栏 | 分镜能交给动作组排练 |
| 风格错配项目 | `director_system` 未判断 | 先判断神怪、战争、喜剧、寓言或写实类型 | Step 2 加项目物理判断 | 战争不飘、神怪不笨重、喜剧可变形 |
| 事实错误或伪引用 | `source_check` 缺失 | 回到 `references/research/` 或联网核对 | 履历、奖项、作品署名强制来源核查 | 无来源时改为“推断/待核对” |

## Repair Playbook

1. 先判断失败类型：泛化、失重空转、人物关系缺失、不可拍、安全缺失、风格错配，或事实错误。
2. 回读 `SKILL.md` 的字段中心映射，定位 `field_id`。
3. 回读 `references/research/0X-*.md`，补来源证据或降低不确定说法。
4. 修正动作方案时按顺序补：动作气质、人物关系、空间路线、威亚/落点、镜头剪辑、安全护栏。
5. 如果动作太满，先删掉不改变人物关系的飞行动作。
6. 若修复属于稳定规则，更新 `SKILL.md`；若属于运行经验，更新本 `CONTEXT.md`；不要把过程流水写入这里。

## Reusable Heuristics

- 程小东式动作不是“漂亮武打”，而是“空间线条 + 武侠物理 + 情绪节奏 + 现场工序”。
- 每次飞起来前先问：为什么飞、飞给谁看、落在哪里、落地后关系怎样变化。
- 飘逸必须有重量反衬：停顿、重击、摔落、受伤反馈或安静的一拍。
- 神怪动作可以不遵守现实重力，但必须遵守角色气质；女鬼、书生、道士、妖人和将军不能同一种物理。
- 场景材料必须进入动作：竹林、袖、剑、雨、水、门、屋顶、阵列、盔甲都不是背景板。
- AIGC 动作提示词必须补安全与可拍性字段，否则容易生成不可执行的漂亮噪音。

## Source Notes

- 机构来源优先：Asian Film Awards Academy、BAFTA、Hong Kong Film Awards、AFI。
- 长访谈材料稀缺，使用时必须区分本人访谈、机构描述和同行旁证。
- 百科、论坛、粉丝整理、短视频讲解默认低权重；除非用于发现线索，否则不进入高权重证据。

## Promotion Candidates

- 若武术组继续沉淀袁和平、洪金宝、成龙、刘家良等人物，可把“动作气质/人物关系/空间路线/现场护栏/安全伦理”抽象为武术组共享模板。
- 若 AIGC 影像链路反复出现“动作漂亮但不可拍”，应提升为 5-Image / 6-Video 分镜与视频提示词的硬门槛。


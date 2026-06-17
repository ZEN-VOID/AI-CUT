# Wuxia Blade-Qi Repair

本 repair 包用于 `4-润色` 阶段修复已有源章中的武侠白刃气流坏点。它只处理 source anchor 内已经存在或已被项目真源明确允许的刀剑风压、剑气、刀气、兵器碰撞和材质破坏表达，不从零新造战斗结果。

## Trigger Signals

- 源章、用户 finding、team brief 或任务请求明确出现：白刃剑气流、剑气、刀气、剑风、刀剑风压、内力余波、兵器风压、港式武侠打斗、徐克导演视角、程小东武指视角、动作是人物关系、动作空间书法、飞之前定落点。
- 项目 `MEMORY.md`、`team.yaml` 或 `north_star.genre_contract` 已声明 90 年代港式武侠、徐克/程小东式高飞剑侠、白刃气流、刀剑风压、材质爆点、金属火星或类似审美。
- 源章打斗已经有兵器交锋，但只写成“强、快、凌厉、气劲纵横”，缺少出刃路径、实体接触、材质响应、人物代价或余波留痕。

## Repair Scope

允许修：

- 把泛化动作句改成有方向、距离、触点、材质响应和代价的句群。
- 补足源章已经暗示的石阶、树木、湿泥、尘土、水汽、木屑、碎石、金属火星等现场回应。
- 把“剑气/刀气”收束到兵器锋芒、内力、身法、风雾水汽和碰撞余波。

禁止修：

- 改胜负、改伤亡、改关系结果、改能力规则、改章末牵引。
- 新增源章没有承托的天气、光源、现代特效、法术体系、无源爆炸或额外敌人。
- 把润色稿写成分镜、摄影说明、动作设计文档或视频 prompt。

## Research-Grounded Repair Axes

这些轴来自 90 年代香港新浪潮武侠资料检索，但在润色阶段只能作为局部修复判断，不得扩写成影评、分镜或动作设计说明。

| axis | bad symptom | repair move | hard boundary |
| --- | --- | --- | --- |
| `fast_graceful` | 只把动作改得更快、更猛 | 在源句动作内补一处优美轨迹和一处受力代价，如袖带牵风后瓦片碎响 | 不新增源章没有的长段追逐 |
| `action_drama_unity` | 打斗漂亮但和人物选择无关 | 把一招改成留手、护人、试探、误判、逼退或暴露身份的证据 | 不改胜负、伤亡、关系结果 |
| `kinetic_zen_balance` | 全段都在堆高速词 | 在出手前补一个短静止或听觉压低，再让原动作爆发 | 不新增玄学顿悟或作者讲解 |
| `practical_fx_material` | 剑气像干净光束或现代特效 | 改成火星、木屑、石粉、水花、泥线、裂痕等有撞击源的材质反应 | 无撞击源不写爆点 |
| `light_immaterial_anchor` | “气”完全脱离兵器和身体 | 回锚到刃口、转腕、步法、换气、水汽、衣料和反震 | 不把武侠改成修仙法术 |
| `jian_dao_temperament` | 刀剑气质混用，兵器只剩名词 | 剑写线、收束、克制；刀写重量、劈裂、粗粝和肉身代价 | 不为了华丽把刀写成剑舞 |
| `flesh_blood_limit` | 过度清洁或过度血腥 | 按项目 tone 调节：清洁稿保留震痛/擦伤，黑暗稿可保留血、骨震、握柄滑 | 不越过源章暴力等级 |

## Team-Lens Repair Overlay: 徐克 x 程小东

当源章、用户 finding、项目 `team.yaml` 或项目记忆明确要求结合 `.agents/skills/team/aigc/导演组/徐克` 与 `.agents/skills/team/aigc/武术组/程小东` 时，润色阶段只把二者作为 affected span 的局部诊断工具，不扩写成整章重拍式动作设计。

| team lens | detects | local repair |
| --- | --- | --- |
| 徐克 `genre_engine` | 白刃战像普通打斗，没有类型发动机 | 在源句范围内补“这招服务复仇、护人、逃生、试探、身份暴露或侠义代价”的动作后果。 |
| 徐克 `character_choice` | 奇观很满，但角色选择没变化 | 把一个爆点改成角色留手、误判、舍弃退路、暴露立场或失去保护对象。 |
| 徐克 `action_relation` | 招式清楚但关系不清 | 补谁压迫、谁撤退、谁诱敌、谁护人、谁不敢下杀手。 |
| 徐克 `overload_check` | 火星、碎石、飞身、气流全部堆上 | 删掉不改变人物选择或空间关系的奇观，只保留主爆点和必要余波。 |
| 程小东 `action_calligraphy` | 动作只有“快/猛/凌厉”，没有空间线条 | 补起线、折线、停顿、落线，用刃线、袖带、水汽、尘线或身法轨迹承接。 |
| 程小东 `flight_physics` | 人物突然飞身折返，没有起落逻辑 | 补起点、借力点、最高停顿、落点和落后关系变化。 |
| 程小东 `character_qi` | 所有人同一种速度、重心和身体规则 | 按角色身份和欲望区分侠客、刺客、妖人、将军、残者的动作物理。 |
| 程小东 `scene_material` | 场景材料只是摆设 | 让竹、雨、水、袖、门、屋顶、灯、盔甲中的 1-3 个改变路线或节奏。 |
| 程小东 `landing_weight` | 飞得美但没有重量和危险 | 补瓦碎、腕震、旧伤牵动、兵器崩口、脚下打滑或呼吸断拍。 |

## Repair Pattern

按 affected span 做最小 patch：

1. 锁定源句中的兵器、动作和承力对象。
2. 判断主 subtype：`blade_qi_line_cut`、`weapon_wind_pressure`、`impact_spark_collision`、`material_fracture_burst`、`body_method_airflow`、`aftershock_trace`、`stillness_before_burst`、`wire_flight_vector`、`rhythmic_action_drama`、`jian_dao_temperament_shift`、`practical_fx_burst`、`genre_engine_choice`、`action_calligraphy_landing` 或 `material_relation_switch`。
3. 增加 1-3 个 prose 证据：出刃路径、实体接触、材质响应、人物反震/判断、余波留痕。
4. 对照源章确认结果不变：谁占上风、谁受伤、谁逃脱、谁被保护、信息是否揭示，都不得被改写。

## Failure-To-Repair Map

| source failure | local diagnosis | repair target |
| --- | --- | --- |
| `generic_qi_glow` | “剑气大盛/刀气纵横”没有路径、触点和代价 | 补出刃方向、第一接触点、材质响应和人物反震 |
| `clean_vfx_beam` | 气流像激光、能量波或现代 CG | 改成刃口、风压、水汽、尘线、火星、木屑或裂痕 |
| `action_without_drama` | 动作华丽但不推进人物关系或局势 | 让动作承担留手、护人、试探、误判、逼退、暴露身份或失去退路 |
| `jian_dao_blur` | 刀剑只剩武器名，气质相同 | 按源章武器选择 `jian_line` 或 `dao_weight`，修正动词和材质 |
| `wire_without_anchor` | 人物突然飞身折返，没有借力点 | 补檐角、墙面、树梢、桌案、水面、瓦片或落脚代价 |
| `overloaded_burst` | 一句里同时爆石、断树、火星、水花、血雾 | 只保留 1 个主爆点和 1 个余波，删掉无源装饰 |
| `empty_spectacle` | 场面漂亮但删掉后人物选择不变 | 改成选择、失去、留手、护人失败、暴露身份或退路变化 |
| `weightless_flight` | 飞身很美但没有停顿、落点和重量 | 补起点、最高停顿、落点、落地声音或受力反馈 |
| `same_body_physics` | 不同角色动作物理相同 | 按角色气质重写速度、重心、刃线、留白和受力方式 |
| `background_only_material` | 竹、水、门、屋顶等只当背景 | 让材料改变路线、遮挡、节奏或关系 |

## Before/After Check

修复后 `genre_scene_repair_profile` 必须记录：

- `source_anchor`
- `affected_span`
- `loaded_type_packages`: 至少包含 `types/wuxia-blade-qi-repair.md`；若回看初稿类型包，应列 `.agents/skills/story/3-初稿/types/网文/武侠/白刃剑气流.md`
- `subtype`
- `research_axis`: 若本轮命中 90 年代港式新派武侠、徐克/程小东、刀剑气质或旧港片爆点，应记录采用的 research axis
- `team_lens_manifest`: 若本轮加载徐克/程小东 team lens，应记录 source paths、applied_fields 和 source facts preservation note
- `fact_preservation_note`
- `no_vfx_boundary_note`

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 是否由项目记忆、north_star、用户 finding 或源章白刃气流信号触发，而非无源加料？ | `genre_scene_route` | `FAIL-POLISH-GENRE-SCENE` | `P2-CONTEXT-PACK` / `P3-REPAIR-PLAN` | `genre_scene_repair_profile` |
| 是否只在 affected span 内增强出刃路径、材质响应、人物代价和余波，不改事实结果？ | `genre_scene_integrity` | `FAIL-POLISH-GENRE-SCENE` | `P4-CREATIVE-POLISH` | before/after evidence |
| 是否避免修仙法术、激光光效、现代 CG 感和分镜/prompt 化表达？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` / `FAIL-POLISH-GENRE-SCENE` | `P4-CREATIVE-POLISH` | boundary check |

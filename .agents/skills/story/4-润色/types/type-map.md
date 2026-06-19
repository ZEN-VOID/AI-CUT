# Polishing Type Map

本文件辅助 `story-polishing` 判定任务模式；主路由仍以 `SKILL.md` 的 Type Routing Matrix 为准。

## Package Index

| package | path | trigger | owner_gate |
| --- | --- | --- | --- |
| `polishing_type_map` | `types/polishing-type-map.md` | 需要展开润色模式、AI 腔或题材质感坏点时 | `P2-CONTEXT-PACK` |
| `guardrail_setup` | `types/guardrail-setup.md` | 覆盖、整章重润或复杂外部输入时 | `P3-REPAIR-PLAN` |
| `character_reaction_repair` | `types/character-reaction-repair.md` | 人物反应虚、对白说明腔、表演腔、脸色捷径或人物气口被磨平 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `prose_texture_repair` | `types/prose-texture-repair.md` | 场景空、题材味被磨平、句群规整或感官颗粒处理失衡 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `visual_readability_repair` | `types/visual-readability-repair.md` | 站位、方向、动作、明暗或信息落点不清 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `genre_scene_repair` | `types/genre-scene-repair.md` | 类型化场面弱、乱、读不清、题材味被磨平或被误写成单一模板 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `action_choreography_repair` | `types/action-choreography-repair.md` | 动作设计弱、打斗像流水账、攻防无判断、受力无代价、追逐路线不清、动作细节扩写 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `interiority_repair` | `types/interiority-repair.md` | 内心戏浅、心理暗流不足、认知偏差/欲望压抑/创伤回声不足、心理转折突兀、第一人称内在节奏弱 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `atmosphere_pressure_repair` | `types/atmosphere-pressure-repair.md` | 氛围淡、压迫感弱、现场感空、感官颗粒没有服务当前戏、场景压力不足 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `sci_fi_tech_repair` | `types/sci-fi-tech-repair.md` | 科幻、机甲、星际、AI、算法、能源、未来技术表现太泛，科技边界/代价/反馈不足 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `cyberpunk_texture_repair` | `types/cyberpunk-texture-repair.md` | 赛博朋克、义体、公司监控、黑客、霓虹城市、高科技低生活、科技压迫感不足 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `xuanhuan_power_repair` | `types/xuanhuan-power-repair.md` | 玄幻、修仙、高武、异能、系统能力只有光效爽点，规则触发/边界/资源代价不足 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `romance_tension_repair` | `types/romance-tension-repair.md` | 言情拉扯、暧昧、甜虐、替身、破镜、关系边界模板化，欲望/回避/潜台词不足 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |
| `wuxia_blade_qi_repair` | `types/wuxia-blade-qi-repair.md` | 源章或项目记忆命中白刃剑气流、剑气、刀气、刀剑风压、港式武侠破坏感、90 年代香港新浪潮武侠、徐克/程小东式高飞剑侠、徐克导演视角、程小东武指视角、动作是人物关系、动作空间书法、飞之前定落点、旧港片实物爆点或刀剑气质区分，且需要最小局部修清动作颗粒 | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` |

## Default Package Rule

- 默认只加载 `types/type-map.md`；具体 repair package 必须由源章坏点、用户 finding、验收 finding 或 `north_star.genre_contract` 触发。
- 未命中的 repair package 不参与本轮聚合，不补空字段、不写占位块、不形成平行润色稿。
- 类型化场面修复优先走根共享合同和 `types/genre-scene-repair.md`，不得由题材包直接改事实、胜负、关系结果或能力规则。
- 题材化细节扩写不是新阶段；动作、内心戏、氛围、科技、赛博、玄幻和言情是候选焦点，不是全题材必查清单。只有某个焦点被当前题材、场景功能、源章坏点、用户 finding 或验收 finding 命中时，才锁定 `source_anchor` 与 `affected_span` 并选择对应专项 repair package。
- 命中具体 subtype repair 时，必须记录 `repair_type_package_manifest`，列出 `matched_signal`、`loaded_paths`、`affected_span`、`subtype` 和未加载包的 `skipped_reason`；未命中但被候选池列出的包必须以 N/A 说明，不参与质量扣分。
- `wuxia_blade_qi_repair` 只在白刃气流、剑气/刀气、刀剑风压、港式武侠破坏感、90 年代香港新浪潮武侠、徐克/程小东式高飞剑侠、徐克导演视角、程小东武指视角、动作是人物关系、动作空间书法、飞之前定落点、旧港片实物爆点、刀剑气质区分或项目记忆明确要求时触发；普通动作可读性问题仍走 `visual_readability_repair` + `genre_scene_repair`。

## Loading Flow

1. 先由 `SKILL.md#Type Routing Matrix` 判定 `chapter_polish / polish_rewrite / local_repair / acceptance_repair / dry_run`。
2. 再按 source anchor、affected span、项目 `MEMORY.md`、`north_star.genre_contract`、场景功能、用户 finding 和验收 finding 判断每个候选 repair package 是否适用；只选择适用包。
3. 生成 `repair_type_package_manifest`：

   ```yaml
   repair_type_package_manifest:
     matched_signal:
     selected_packages: []
     loaded_paths: []
     affected_span:
     subtype:
     detail_expansion_focus:
     no_new_fact_boundary:
     skipped_packages: []
     skipped_reason:
     n_a_focus:
   ```

4. 最后回到 `P3-REPAIR-PLAN` 与 `P4-CREATIVE-POLISH` 统一修补，不产生平行润色稿。

## Mode Map

| mode | trigger | required_context | gate |
| --- | --- | --- | --- |
| `chapter_polish` | 目标润色稿不存在 | 源初稿、planning、north_star、MEMORY/CONTEXT | 生成第一版最小修补稿 |
| `polish_rewrite` | 用户明确要求重润/覆盖/整章重写 | 源初稿、既有润色稿、覆盖授权 | 扩大改写范围有明确理由 |
| `local_repair` | 用户或内置验收指定局部坏点 | finding、affected span、源初稿 | 只修问题及必要上下文 |
| `acceptance_repair` | 用户显式要求多维审计后直接优化，或终稿验收 FAIL | 验收维度 findings、repair brief、源初稿 | 验收 findings 必须进入正文修补 |
| `dry_run` | 只检查或装配上下文 | 源初稿和上游校准资料 | 不写正文 |

## Repair Type Packages

| repair_type | trigger | required_context | gate |
| --- | --- | --- | --- |
| `character_reaction_repair` | 人物反应虚、对白说明腔、表演腔、脸色捷径或人物气口被磨平 | source anchor、人物关系、当前压力、源章 affected span | 不新增人物动机或剧情结果 |
| `prose_texture_repair` | 场景空、题材味被磨平、句群过度规整、感官颗粒被误删或新增装饰氛围 | source anchor、场景压力、north_star、源章 affected span | 不做五感补全或无源氛围新增 |
| `visual_readability_repair` | 站位、方向、动作、明暗或信息落点不清 | source anchor、空间关系、动作链、源章 affected span | 不输出摄影、灯位或视频 prompt |
| `genre_scene_repair` | 动作/关系/能力/恐怖/悬疑/现实等类型化场面弱、乱、读不清、题材味被磨平或被误写成单一模板 | `.agents/skills/story/_shared/genre-scene-strengthening-contract.md`、source anchor、affected span、north_star.genre_contract、当前 finding | 不改事实、胜负、关系结果、能力规则或章末牵引 |
| `action_choreography_repair` | 已有动作场面不精彩、攻防无判断、动作路径/受力/代价/余波不清 | source anchor、动作链、人物选择、空间/材质锚点、源章 affected span | 不从零设计新战斗，不改胜负、伤亡、能力规则 |
| `interiority_repair` | 内心戏浅、心理转折突兀、欲望/恐惧/创伤回声缺承托 | source anchor、当前事件压力、人物关系/状态、视角距离、源章 affected span | 不新增动机、创伤、关系结果或心理报告段 |
| `atmosphere_pressure_repair` | 氛围淡、场景空、压迫感弱或感官颗粒不服务当前戏 | source anchor、场景压力、物件/空间/声音/沉默锚点、源章 affected span | 不新增无源天气、光源、气味、人群或独立氛围段 |
| `sci_fi_tech_repair` | 科技感弱、技术像标签、缺边界/代价/反馈/伦理后果 | source anchor、已有技术名和用途、规则边界、项目科幻题材轴、源章 affected span | 不新造科技体系、参数表、百科说明或万能技术 |
| `cyberpunk_texture_repair` | 赛博只剩霓虹标签，高科技低生活和公司/监控/义体压迫不足 | source anchor、已有赛博元素、身体/债务/权限/监控/公司权力锚点 | 不新增公司、帮派、义体等级、黑客能力或视觉装饰清单 |
| `xuanhuan_power_repair` | 能力只有光效爽点，缺规则触发、资源代价、边界和反馈 | source anchor、能力真源、境界/资源/技能约束、源章 affected span | 不新增境界、功法、技能、系统奖励或改突破/胜负结果 |
| `romance_tension_repair` | 言情拉扯模板化，欲望/回避/边界/潜台词不足 | source anchor、当前关系状态、误会/债务/承诺、源章 affected span | 不新增告白、亲吻、和解、分手、掉马或关系定性 |
| `wuxia_blade_qi_repair` | 白刃剑气流、剑气、刀气、剑风、刀剑风压、港式武侠破坏感、90 年代港式新派武侠质感写得泛、空、CG 化或缺少材质承托 | `types/genre-scene-repair.md`、`types/wuxia-blade-qi-repair.md`、source anchor、affected span、项目 MEMORY/north_star、武器/场景材质锚点 | 不新造战斗结果，不把白刃气流写成修仙法术、激光光效、现代 CG 或无源爆破 |

## Subtype Repair Routing

| source_signal | primary_repair | companion_packages | gate |
| --- | --- | --- | --- |
| 普通武戏站位不清 | `visual_readability_repair` | `genre_scene_repair` | 动作方向、距离、受力和后果清楚 |
| 动作设计弱、打斗像流水账、追逐缺路径或代价 | `action_choreography_repair` | `visual_readability_repair`, `genre_scene_repair` | 动作 beat、方向距离、受力代价和人物选择清楚，且不改胜负 |
| 武侠打斗缺招路、拆招和代价 | `genre_scene_repair` | 可回看 `.agents/skills/story/3-初稿/types/网文/武侠/武侠之战斗设计.md` | 不改胜负，只补动作因果 |
| 白刃剑气流、剑气/刀气、刀剑风压、港式武侠爆点、90 年代香港新浪潮武侠、徐克/程小东式高飞剑侠、徐克导演视角、程小东武指视角、动作是人物关系、动作空间书法、飞之前定落点、旧港片实物爆点、刀剑气质区分 | `wuxia_blade_qi_repair` | `genre_scene_repair`；必要时回看 `.agents/skills/story/3-初稿/types/网文/武侠/白刃剑气流.md` | 绑定实体兵器、身法、内力、材质响应、人物代价、刀剑气质、动作戏剧功能、空间线条和落点重量 |
| 内心戏浅、心理暗流弱、第一人称内在节奏不足 | `interiority_repair` | `character_reaction_repair`, `prose_texture_repair` | 心理补丁推动选择、对白、关系或章末牵引，不新增动机 |
| 氛围淡、压迫感弱、现场空 | `atmosphere_pressure_repair` | `prose_texture_repair`, `genre_scene_repair` | 场景颗粒服务冲突、信息、关系、空间限制或章末牵引 |
| 科幻/机甲/AI/星际技术表现太泛 | `sci_fi_tech_repair` | `genre_scene_repair`；必要时回看 `.agents/skills/story/3-初稿/types/网文/科幻/科幻.md` | 技术有边界、代价、反馈和后果，不新造体系 |
| 赛博朋克只有霓虹标签，高科技低生活不成立 | `cyberpunk_texture_repair` | `sci_fi_tech_repair`, `genre_scene_repair` | 赛博元素落到身体、债务、权限、监控或公司权力，不新增世界观 |
| 玄幻/修仙/高武/异能能力只有光效爽点 | `xuanhuan_power_repair` | `genre_scene_repair`；必要时回看 `.agents/skills/story/3-初稿/types/网文/玄幻剧/power-systems.md` | 能力有触发、边界、资源代价和反馈，不新造能力 |
| 言情拉扯、暧昧、甜虐或替身关系模板化 | `romance_tension_repair` | `interiority_repair`, `genre_scene_repair` | 欲望/回避、边界、潜台词和选择代价清楚，不新增关系结果 |

## Execution Environment Notes

用户给出执行环境偏好时，不改变 `mode`，只追加执行备注。

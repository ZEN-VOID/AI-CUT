# Genre Scene Repair Type

本类型包用于 `4-润色` 中修复已有 `3-初稿` 源章里的类型化场面坏点。它不从零设计场面，不改剧情结果，不生成第三正文真源。

必须先加载 `.agents/skills/story/_shared/genre-scene-strengthening-contract.md` 建立 `genre_scene_route`，再按 `types/type-map.md` 选择具体 repair package，并把修复限制在 `affected_span` 及必要上下文。

## Trigger Signals

- 动作、追逐、武戏或搏斗段读不清站位、距离、方向、受力、代价或余波。
- 言情关系段只有情绪标签、脸红模板、占有奖励或纯糖/纯虐清单，缺少欲望、回避、边界和选择。
- 玄幻/修仙/异能段只有光效或爽点，缺少规则、能力边界、资源代价和环境反馈。
- 恐怖/灵异/惊悚段只喊“恐怖、诡异、压抑”，缺少遮蔽、信息延迟、逃生路径和感官选择。
- 悬疑/侦探/谍战段线索不可复盘，伏笔和线索混用，揭晓靠作者解释。
- 现实/职场/家庭/年代段压力被写成无后果爽点，缺少制度、关系、证据和后果链。
- 用户明确指出“不要等分镜/AIGC 再补”“按当前小说类型增强场面”“不要写成武侠模板”。
- 源章或项目记忆命中白刃剑气流、剑气、刀气、剑风、刀剑风压、内力余波或港式武侠破坏感，但正文只有泛化光效、气势词或不清楚的动作。

## Repair Method

1. 锁定 `source_anchor`：源初稿的段落、句群或相邻上下文。
2. 建立 `genre_scene_route`：项目题材轴来自 `north_star.genre_contract`，场景功能轴来自源章坏点和当前 finding。
3. 标注 `affected_span` 和 `allowed_change_scope`：只修坏点及必要承接句。
4. 选择 1 个 primary scene function；secondary functions 不超过 2 个；若命中 subtype，生成 `repair_type_package_manifest` 并列真实加载路径。
5. 按场景功能修复：
   - `action_combat`：补清方向、距离、受力、材质响应和代价，不改胜负。
   - `romance_relationship`：补清欲望/回避、亲密边界、潜台词和关系选择，不新增关系结果。
   - `xuanhuan_power`：补清规则触发、能力边界、资源代价和反馈，不新造体系。
   - `horror_suspense`：补清遮蔽、信息延迟、逃生路径和感官焦点，不解释未知。
   - `mystery_clue`：补清线索可见性、误导公平性和证据状态，不提前剧透。
   - `realism_pressure`：补清制度/社会后果、物件证据和沉默成本，不无代价爽化。
6. 修后检查是否保持源章事实、段落骨架、人物气口和章末牵引。

## Subtype Repair Handling

| subtype_signal | required_package | repair_focus | boundary |
| --- | --- | --- | --- |
| 普通武侠打斗、比武、围杀、兵器追逐 | 可回看 `.agents/skills/story/3-初稿/types/网文/武侠/武侠之战斗设计.md` | 招路、拆招、方向、距离、代价、胜负余波 | 不把非武侠类型默认武侠化 |
| 白刃剑气流、剑气、刀气、剑风、刀剑风压、港式武侠破坏感 | `types/wuxia-blade-qi-repair.md`；必要时回看 `.agents/skills/story/3-初稿/types/网文/武侠/白刃剑气流.md` | 出刃路径、实体接触、材质响应、人物反震、余波留痕 | 不改胜负，不写修仙法术、激光光效、现代 CG、无源爆破 |
| 言情关系拉扯 subtype | 仍以 source anchor 和关系结果为边界 | 欲望/回避、边界、潜台词、关系选择 | 不新增关系结果 |
| 玄幻/修仙能力 subtype | 以既有能力规则为边界 | 规则触发、资源代价、环境反馈 | 不新造能力体系 |

## Prohibitions

- 不把局部类型场面修复扩大成整章重写。
- 不把所有类型场面修成武侠动作段。
- 不新增源章没有的天气、光源、爆炸、证据、关系转折、能力规则、胜负结果或死亡结果。
- 不输出分镜、摄影、视频 prompt、动作设计说明书或点评。
- 不把题材包例句直接改写成正文。

## Review Gate Mapping

| review_question | gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| 是否锁定 source anchor、affected span 和项目题材轴 + 场景功能轴？ | `genre_scene_route` | `FAIL-POLISH-GENRE-SCENE` | `P2-CONTEXT-PACK` / `P3-REPAIR-PLAN` | `genre_scene_repair_profile` |
| 修复是否只增强当前场面功能，没有改事实、改胜负、改关系结果或新造规则？ | `genre_scene_integrity` | `FAIL-POLISH-GENRE-SCENE` | `P3-REPAIR-PLAN` / `P4-CREATIVE-POLISH` | before/after evidence |
| 修复是否避免武侠化默认、机械题材套用和独立加料层？ | `genre_texture_density` | `FAIL-POLISH-TEXTURE` / `FAIL-POLISH-GENRE-SCENE` | `P4-CREATIVE-POLISH` | boundary check |
| 命中 subtype repair 时是否加载真实 package 并写入 `repair_type_package_manifest`？ | `genre_scene_subtype_package` | `FAIL-POLISH-GENRE-SCENE` | `P3-REPAIR-PLAN` | `repair_type_package_manifest` |

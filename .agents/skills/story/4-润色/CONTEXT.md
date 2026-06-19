# CONTEXT.md

本文件是 `story2026 / 4-润色` 的经验层知识库。它用于沉淀从 `3-初稿` 到 `4-润色` 的最小局部修补、中文表达局部优化、题材质感校准、AI 腔坏点定位和单根技能包运行经验，不再维护旧分支经验。

## Context Health

```yaml
monitor_version: 2
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-single-root-polishing-context
last_checked_at: 2026-06-10
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-POLISH-01` | 润色稿像重新写章，初稿事实丢失 | source anchoring | 回到 `3-初稿` 源章逐段锚定，只改表达坏点 | `P1-SOURCE-LOCK` 和 `P3-REPAIR-PLAN` 固定源章锚定 | 润色稿核心事实可追溯源初稿 |
| `TM-POLISH-02` | 用户只说润色，却被分流到旧子目录 | topology drift | 直接进入 `.agents/skills/story/4-润色/SKILL.md` | 根技能声明单一阶段入口 | `rg` 不再出现旧分支子路径主路由 |
| `TM-POLISH-03` | frontmatter 继续写 `润色模型` 并按该字段返工 | metadata drift | 新产物改用 `修订阶段: 润色`、`初稿来源`、`字数`；旧字段只作 legacy 读取 | Output Contract 固定阶段字段，不把旧 metadata 作为路由真源 | 新模板不含 `润色模型` |
| `TM-POLISH-04` | 语言变顺但题材味被磨平 | genre texture loss | 回读 `north_star.yaml.genre_contract`，只在必要处加场景压力、对白锋利度和心理节奏 | Base Polishing Rules 固定题材质感保护 | 文本更顺但不通用顺滑 |
| `TM-POLISH-05` | AI 腔只被泛化处理，结果更像规整优化稿 | anti-ai underspecification | 拆成连接词、段落均匀、主谓完整、情绪标签、解释插入语、总结句或角色混声 | `P3-REPAIR-PLAN` 要求具体坏点清单 | repair plan 有可定位坏点 |
| `TM-POLISH-06` | local repair 扩大成整章重写 | repair scope creep | 标注 affected span，只修问题区域和必要上下文 | 默认最小局部修补，整章重润需用户授权 | diff 范围可解释 |
| `TM-POLISH-07` | 场景密度被当成冗余删掉 | density compression | 恢复承载空间、物件、身体反应、关系压力或悬念延迟的颗粒 | Base Polishing Rules 固定密度节奏保护 | 场景仍可感知 |
| `TM-POLISH-08` | 旧润色稿被静默覆盖 | writeback safety | 回读既有稿并要求显式覆盖授权 | `P1-SOURCE-LOCK` 固定覆盖门 | 覆盖证据可追溯 |
| `TM-POLISH-09` | 多维验收或审计只有意见没有优化正文 | acceptance-repair gap | 先按本技能内置验收维度拆审，再把 findings 回灌到 `acceptance_repair` / `local_repair` | `P2A-ACCEPTANCE-BRIEF` 不允许只审不改后宣称完成 | 最终润色稿体现 findings 修复，验收包同步更新 |
| `TM-POLISH-10` | 从旧表演/氛围/光影迁入的修复再次变成整章加料 | texture-repair overreach | 按 `character-reaction-repair`、`prose-texture-repair`、`visual-readability-repair` 先锁 affected span 和 source anchor，只做最小 patch | `SKILL.md` 固定三类 repair types 的禁止项和 `FAIL-POLISH-TEXTURE` 验收 | diff 只影响坏点附近，且没有新增无源实体或装饰段 |
| `TM-POLISH-11` | 类型化场面修复把局部坏点扩成整章重写、武侠化默认或题材模板套用 | genre-scene repair overreach | 先锁 source anchor、affected span、项目题材轴和场景功能轴，再用 `genre-scene-repair.md` 做最小 patch | `SKILL.md` 固定 `genre_scene_integrity` gate 和 `FAIL-POLISH-GENRE-SCENE`，禁止第三正文真源 | before/after evidence 不改事实、胜负、关系结果、能力规则或章末牵引 |
| `TM-POLISH-12` | `types/` repair 包存在但无法证明具体包被加载 | repair package under-routing | 通过 `types/type-map.md` 解析真实 repair package，并生成 `repair_type_package_manifest` | `SKILL.md` 固定命中类型场面或 subtype repair 时加载 type-map 并记录真实 paths | `repair_type_package_manifest.loaded_paths` 或 `skipped_reason` 可审计 |
| `TM-POLISH-13` | 白刃剑气流被泛化修成“动作更清楚”，仍缺剑气/刀气/刀剑风压的材质承托 | wuxia blade-qi repair under-specification | 加载 `types/wuxia-blade-qi-repair.md`，只在 affected span 内补出刃路径、实体接触、材质响应、人物代价和余波 | `genre-scene-repair.md` 和 type-map 固定 `wuxia_blade_qi_repair` subtype | before/after evidence 保持胜负、伤亡、关系结果和能力规则不变 |
| `TM-POLISH-14` | 90 年代香港新浪潮武侠只被润成“更电影感”，文本出现镜头/特效/吊威亚味 | research-to-prose repair drift | 用 `wuxia-blade-qi-repair.md` 的 research axes 只修 affected span：静止预压、实物爆点、刀剑气质、动作戏剧功能和物理锚点 | type-map 把 90 年代港式新派武侠、徐克/程小东、旧港片实物爆点纳入 `wuxia_blade_qi_repair` 触发词 | 润色稿不出现分镜/prompt 化词，且事实、胜负、暴力等级不漂移 |
| `TM-POLISH-15` | 点名徐克/程小东后，润色只加“电影感/飘逸感”，仍未修人物选择、空间线条和落地重量 | team-lens repair under-integration | 用 `wuxia-blade-qi-repair.md` 的 Team-Lens Repair Overlay，只在 affected span 内补动作关系、类型发动机、空间书法、起落物理和过量删减 | repair package 固定徐克/程小东字段映射，禁止把 team lens 写成影评或整章重写许可 | `team_lens_manifest` 可追踪 source paths 和 applied_fields，before/after 不改事实结果 |
| `TM-POLISH-16` | 用户要求“细节扩写”，执行者只做泛化润色或整章加料 | detail expansion under-routing | 先锁 source anchor 与 affected span，再按动作、内心戏、氛围压力、科技、赛博、玄幻或言情信号加载专项 repair 包 | `SKILL.md`、`types/type-map.md` 和 review gate 固定 `detail_expansion_profile` 与 no-new-fact boundary | `repair_type_package_manifest.loaded_paths` 包含真实专项包，before/after 不改事实 |
| `TM-POLISH-17` | 科幻/赛博章节只加术语和霓虹装饰，科技或公司压迫仍不成立 | sci-fi cyber texture drift | 科幻走 `sci-fi-tech-repair.md`，赛博走 `cyberpunk-texture-repair.md`，只补已有技术的边界、代价、反馈、身体/债务/权限/监控压力 | type-map 固定 sci-fi/cyberpunk repair package，禁止新造科技体系或世界观 | 技术不万能，赛博不是装饰清单，人物选择受到可见约束 |
| `TM-POLISH-18` | 执行者把动作、内心戏、氛围、科技、赛博、玄幻、言情等候选焦点当成所有章节都必须检查和强化的通用清单 | detail focus universalization | 回到 `P3-REPAIR-PLAN`，只保留由项目题材、场景功能、源章坏点或 finding 命中的 selected packages，其余写 N/A | `SKILL.md`、`types/type-map.md` 和 review gate 固定候选焦点不是必修项 | `detail_expansion_profile.n_a_focus` 或 `skipped_reason` 说明未命中焦点，未产生无关加料 |

## Repair Playbook

1. 先检查当前章 `3-初稿/第N卷/第N章.md` 是否存在；缺失时硬失败，不用 planning 补写。
2. 若用户给出执行环境偏好或当前会话润色，不新增分支入口；只在执行报告中记录。
3. 若目标 `4-润色` 已存在，先回读既有润色稿；正式覆盖必须有显式确认。
4. 若润色稿改动核心剧情，回到源初稿事实锚点，要求“只改表达，不改事件”。
5. 若用户只说“AI 味重”，先定位具体文本特征，不直接触发整章重写。
6. 若润色后场景变空，优先恢复源初稿中承载压力的物件、身体反应、空间距离和信息延迟。
7. 若多维验收或审计只完成意见汇总而没有改稿，回到 `P2A -> P3 -> P4 -> P5`，让 findings 进入正文修补并重新生成验收包。
8. 若脚本或模板产出润色正文，把该产物废弃，回到 LLM-first 润色节点。
9. 若用户要求“更有表现力/氛围/画面感”，先拆成具体坏点：人物反应虚、场景压力空、视觉可读性差或中文表达坏；不要直接触发整章重润。
10. 若用户要求武戏、文戏、言情拉扯、玄幻能力兑现、恐怖悬疑或现实压力优化，先判断是否已有 `3-初稿` 源章；有源章则进入 `genre_scene_repair`，无源章回到 `3-初稿` 首写，不用润色凭 planning 从零生成。
11. 若用户质疑某个 repair type 是否会真的加载，检查 `types/type-map.md` 的 package 行和本轮 `repair_type_package_manifest`，不能只写“按需处理”。
12. 若源章或项目记忆命中白刃剑气流，先判断是否属于源章已有表达的局部坏点；是则走 `wuxia_blade_qi_repair`，否则回到 `3-初稿` 或 `repair` 判定是否需要重写上游。
13. 若用户或项目记忆指定 90 年代香港新浪潮武侠、徐克/程小东、旧港片实物爆点或刀剑气质区分，润色阶段只把这些资料锚点压成局部动作、材质、声音、人物代价和戏剧功能，不新增影评式说明或电影制作词。
14. 若用户点名徐克和程小东两位 team lens，润色先问 affected span 是否缺“选择、关系、线条、材料、落点、删减”中的哪一项；只修缺项，不把整段改成动作设计说明。
15. 若用户要求“题材化细节扩写”，先拆成候选 repair focus：动作设计、内心戏、氛围压力、科技元素、赛博质感、玄幻能力或言情拉扯；只有被项目题材、场景功能、源章坏点或 finding 命中的 focus 才需要 source anchor、affected span 和 no-new-fact boundary，未命中 focus 写 N/A。
16. 若用户要求科技/赛博质感，先判断是通用科幻技术边界问题，还是赛博朋克的身体/债务/权限/监控/公司权力压迫问题；前者走 `sci-fi-tech-repair`，后者叠加 `cyberpunk-texture-repair`。

## Reusable Heuristics

- 润色的第一真源是 `3-初稿` 正文，不是 planning。
- “更像中文”不是堆成语，也不是口语化变浅，而是减少解释性连接词，让动作、感官、停顿和对白潜台词承担信息。
- 好的二改会让人物更像在现场反应，而不是让文本更像规范答案。
- AI 检测友好的润色通常不是更顺，而是少动：保留初稿句群骨架、长短不齐、局部粗粝和人工式不均匀，只修坏处。
- 人物、场景和视觉可读性修复的共同边界是 source anchor：源章没有的光源、天气、烟雾、气味、关系转折和剧情结果，润色阶段不新增。
- 类型化场面修复的共同边界也是 source anchor：动作不改胜负，言情不改关系结果，玄幻不改规则体系，恐怖不解释未知，悬疑不提前揭晓，现实不消除后果。
- subtype repair 不是更大范围的加料许可；它只让已命中的类型坏点更具体、更可读、更符合项目题材边界。
- 细节扩写不是“写更多”，而是让已有局部更有功能：动作更可读，心理更有压力，氛围更能承托冲突，技术更有边界，赛博更有社会压迫，玄幻能力更有代价，言情拉扯更有潜台词。
- 选择多个细节扩写包时，先定 primary focus；同一 affected span 最多 1 个 primary package + 2 个 companion packages，避免把局部修补变成全场景重写。
- 动作不精彩、内心戏浅、氛围淡、科技感弱、赛博味不足、玄幻能力表现弱、言情拉扯弱是“可能存在的问题族”，不是每种题材都必须证明不存在的质量维度。
- 白刃剑气流润色的重点是把源章已有的剑气/刀气/刀剑风压绑定到实体兵器、身法、内力、现场材质和人物代价，不把 prose 改成视频特效描述。
- 港式新派武侠润色的判断顺序是：源章事实不动 -> 刀/剑/长兵器气质明确 -> 出刃路径清楚 -> 爆点有物理源 -> 动作服务人物戏 -> 没有镜头、CG、吊威亚或 prompt 词。
- team lens 参与润色时，徐克负责删掉不改变人物选择的奇观，程小东负责给保留动作补起落、停顿、材料和重量；二者都不能授权改胜负、改伤亡或改关系结果。

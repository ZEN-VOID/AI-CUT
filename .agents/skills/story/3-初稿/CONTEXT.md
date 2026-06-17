# CONTEXT.md

本文件是 `story2026 / 3-初稿` 的经验层知识库。它记录章节初稿的上下文加载、正文真源、防漂移、最小写回和单根技能包运行经验，不再维护旧分支经验。

## Context Health

```yaml
monitor_version: 2
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-single-root-drafting-context
last_checked_at: 2026-06-10
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 普通写章请求仍被分流到旧子目录 | topology drift | 直接进入 `.agents/skills/story/3-初稿/SKILL.md` | 根技能声明单一阶段入口 | `rg` 不再出现旧分支子路径主路由 |
| 初稿正文头部继续写 `写作模型` 并按该字段返工 | metadata drift | 新产物改用 `创作阶段: 初稿` 与 `字数`；旧字段只作 legacy 读取 | Output Contract 固定阶段字段，不把旧 metadata 作为路由真源 | 新模板不含 `写作模型` |
| 正文看起来像 planning 摘要而不是小说 | prose conversion gap | 回到 `N5-CREATIVE-DRAFT`，逐条把任务义务转成现场动作、物件、对白和章末牵引 | `references/chapter-drafting-contract.md` 固定 prose conversion 与现场发现门 | 正文无 planning 标题句法 |
| 新章只接最近上一章，漏掉同卷早前伏笔和线索 | continuity underload | 加载当前卷全部已存在前序章，最近前章只负责开章姿态 | Context Loading Contract 与 `N3-CONTINUITY` 固定全部前序章清单 | `continuity_bridge.previous_chapter_refs` 覆盖同卷前文 |
| 监制意见泛泛，没有进入正文创作约束 | supervision packet gap | 回读 `_shared/supervised-drafting-review-loop-contract.md`，按项目 `team.yaml` 请教具体问题 | `N4-SUPERVISION` 要求 packet 或降级说明 | 报告可追溯 roster、问题、摘要和可执行指导 |
| 执行环境提示被误当成技能分流 | execution environment confusion | 仍进入本技能，只记录执行备注 | 根合同禁止创建分支入口 | 输出路径仍是 `3-初稿/第N卷/第N章.md` |
| 情绪表达反复落在脸色颜色变化 | emotion shorthand loop | 改用动作、呼吸、手部、视线、物件误触、话语断裂或空间退让 | Core Gates 和 review gate 固定脸色捷径门禁 | 抽查关键情绪段不靠脸色颜色词承载 |
| 章节编号、sidecar 等执行层标签进入正文 | narrative perspective leak | 改写为角色可感知的事件、地点、物件或伤亡称呼 | Core Gates 固定叙事内视角完整性 | 正文无 `上一章/本章/frontmatter` 等词 |
| 旧“表演/氛围”能力迁入小说后又变成加料层 | presence-texture overreach | 回到 `references/character-presence-contract.md` 与 `references/scene-pressure-texture-contract.md`，只让人物反应和场景颗粒服务当前戏 | `SKILL.md` 固定 `presence_texture` gate，禁止独立表演层和氛围层 | `character_presence_profile` 与 `scene_pressure_texture_profile` 能回指正文功能 |
| 类型化场面首写被写成武侠专用或题材模板套用 | genre-scene route collapse | 建立 `project_genre_axis + scene_function_axis`，按当前章义务选 primary scene function | `SKILL.md` 和 `references/genre-scene-drafting-contract.md` 固定 `genre_scene_route` 与 `FAIL-DRAFT-GENRE-SCENE` | `genre_scene_profile` 能回指正文场面功能，且无第三正文层 |
| `types/` 有目录但未能证明具体题材包被加载 | type package under-routing | 通过 `types/type-map.md` 解析真实文件路径，并生成 `type_package_manifest` | `SKILL.md` 固定命中类型信号时加载 `types/type-map.md`，subtype 命中时记录真实 loaded paths | `type_package_manifest.loaded_paths` 或 `skipped_reason` 可审计 |
| 武侠打斗只停在泛化动作强化，白刃剑气流颗粒不足 | wuxia subtype under-specification | 加载 `武侠之战斗设计.md` 与 `白刃剑气流.md`，把剑气/刀气/剑风落成出刃路径、实体接触、材质响应、人物代价和余波留痕 | `types/type-map.md` 和共享合同固定 `wuxia_blade_qi_flow` subtype，不让 AIGC 分镜阶段一次性补“精彩打斗” | 正文证据不出现修仙法术、激光光效、现代 CG 或无源爆破 |
| 90 年代香港新浪潮武侠被当成风格标签，未进入动作设计 | research-to-prose gap | 用 `白刃剑气流.md` 的 research axes 把徐克/程小东、胡金铨余韵、旧港片实物爆点、刀剑气质差异翻译成动作节拍、材质证据和人物戏 | subtype package 固定资料锚点只服务 prose conversion，不允许正文出现摄影、吊威亚、CG、prompt 或影评词 | `type_package_manifest` 记录 `wuxia_blade_qi_flow`，正文能看到 weapon temperament、material evidence、dramatic function |
| 点名徐克/程小东后仍只得到泛化“港式武侠感” | team-lens under-integration | 读取 team 子技能，把徐克的 `genre_engine/character_choice/action_relation/overload_check` 与程小东的 `action_calligraphy/flight_physics/scene_material/landing_weight` 合成 `team_lens_manifest` | `白刃剑气流.md` 固定“导演发动机 + 武指物理”写前自检，不让 team lens 变成正文标签或影评段 | `type_package_manifest` / `team_lens_manifest` 能列出加载路径和 applied_fields，正文有选择、关系、线条、材料、落点 |

## Repair Playbook

1. 若写章入口仍指向旧分支子目录，先修 registry、story 根路由和阶段 `SKILL.md`，再处理正文。
2. 若用户给出执行环境偏好或当前会话写作，不新增分支入口；只在执行报告中记录。
3. 若正文像提纲，回到源层检查 context pack 是否直接泄漏 planning 标题，再让 LLM 重新做小说化转译。
4. 若同卷连续性断裂，先看是否加载了当前卷所有前序章；不要只补一句“承接上一章”。
5. 若目标章已存在，必须先回读并确认是续写、重写还是局部修复；默认不静默覆盖。
6. 若 review 返工涉及创作性改写，回到本根技能的 `local_repair / chapter_rewrite`，不再追溯旧分支。
7. 若脚本或模板产出正文内容，把该产物废弃，回到 LLM-first 主创节点。
8. 若人物反应或场景颗粒显得用力，先问它服务什么压力、信息、关系或章末牵引；答不出来就删，不要继续补感官或微表情。
9. 若用户要求武戏、文戏、言情拉扯、玄幻能力兑现、恐怖悬疑或现实压力强化，先判 owner 是否仍是初稿首写；若是，加载共享合同和 drafting 合同，在 `N5` 写进 prose，而不是新增中间阶段。
10. 若用户质疑 `types/` 是否真的加载，先检查 `types/type-map.md` 是否有真实路径映射，再要求本轮报告给出 `type_package_manifest`；不能只回答“会按需加载”。
11. 若项目记忆或用户要求白刃剑气流，先加载白刃专项包；普通武侠战斗包只解决招路，不能替代剑气/刀气/刀剑风压的材质破坏和港式武侠边界。
12. 若用户指定 90 年代香港新浪潮武侠、徐克/程小东、旧港片实物爆点或刀/剑气质差异，必须把资料锚点翻译成小说内的动作、材质、声音、人物代价和戏剧功能；不要在正文里写导演、镜头、剪辑、吊威亚或 CG。
13. 若用户点名 `.agents/skills/team/aigc/导演组/徐克` 与 `.agents/skills/team/aigc/武术组/程小东`，先把二者合成为内部工作台：徐克问“旧类型发动机、人物选择、动作关系、过量删减”，程小东问“动作气质、空间线条、起落物理、落地重量”；最后只输出小说 prose。

## Reusable Heuristics

- `3-初稿` 的核心是把 planning 义务变成有现场、有动作、有声口、有牵引的章节 prose。
- 初稿 frontmatter 越极简越稳；上下文证据放报告或 sidecar，不要挤进正文头。
- 同卷前文是写作连续性的底盘；最近上一章解决入场姿态，早前章节解决事实、伏笔、道具和卷目标进度。
- 章节正文里的读者感受来自场景中发生的发现、误触、沉默和反作用，而不是从 planning 字段翻译出的说明。
- 好的人物在场不是“更多表演”，而是当前压力下更具体的选择、回避、停顿、误触、退让或反击。
- 好的场景压力不是“更有氛围”，而是空间、物件、声音、沉默和环境反应让冲突更难逃开。
- 好的类型化场面不是“更像某题材模板”，而是当前题材承诺下的场景功能更清楚：动作有代价，关系有边界，能力有规则，恐怖有遮蔽，悬疑有可复盘线索，现实有后果。
- 类型包加载要可审计：题材目录、具体文件、subtype package、未加载原因都应落入 manifest，而不是停在自然语言“参考了题材”。
- 白刃剑气流的小说原文价值在于先把动作因果和材质反应写清楚，让后续 AIGC 分镜自然继承；不要把它拖到视频阶段再用镜头和特效一次性补足。
- 90 年代港式新派武侠的可复用转译公式是：静止预压 + 快而优美的身法轨迹 + 实物爆点 + 刀剑气质差异 + 动作服务人物戏。
- 徐克 x 程小东的 story 转译公式是：类型发动机逼出人物选择，动作关系决定空间线条，场景材料改变路线，飞身必须有落点和重量，奇观只保留会改变人物关系的部分。

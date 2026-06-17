# Genre Scene Drafting Contract

本文件展开 `story-drafting` 在初稿首写、续写、重写和局部创作修复中的类型化场面强化规则。入口、路由、正文写权和验收真源仍归 `3-初稿/SKILL.md`。

本文件必须与 `.agents/skills/story/_shared/genre-scene-strengthening-contract.md` 配合使用；共享合同负责双轴路由，本文件只负责把路由结果写进章节 prose。

## Drafting Position

- 当前阶段拥有 `projects/story/<项目名>/3-初稿/第N卷/第N章.md` 的初稿写权。
- 类型化场面强化只发生在 `N5-CREATIVE-DRAFT` 内，不能成为独立 `3.5` 阶段。
- 类型化场面强化必须服务当前章 planning、人物压力、信息推进、读者牵引和章末余波。

## Drafting Requirements

### Route Before Prose

在写入关键场面前，先建立：

- `project_genre_axis`：来自 `north_star.yaml.genre_contract` 的项目题材承诺、禁区和风格走廊。
- `scene_function_axis`：来自当前章 planning、人物冲突、场景压力和用户要求的场面功能。
- `scene_subtype_axis`：来自 `types/type-map.md`、项目 `MEMORY.md`、用户显式要求或验收 finding 的细分类型包选择；无 subtype 时写明 N/A。
- `genre_scene_route.owner_stage = 3-初稿`。
- `type_package_manifest`：记录实际加载的题材/场面/subtype 路径，禁止只写“已参考类型包”。

### Function To Prose

| scene_function | drafting focus | prose landing |
| --- | --- | --- |
| `action_combat` | 攻防节拍、距离、方向、力量来源、受击材质、动作代价 | 动作链、站位变化、物件/场地反应、短促余波 |
| `romance_relationship` | 欲望/回避、亲密边界、误读、试探、共同风险 | 对白潜台词、停顿、距离、物件误触、关系选择 |
| `xuanhuan_power` | 规则显影、能力边界、资源代价、升级收益 | 规则触发、身体/环境反馈、旁人认知变化、代价留痕 |
| `horror_suspense` | 威胁遮蔽、信息延迟、逃生路径、感官选择 | 不完整可见物、声音断点、空间退路、污染余波 |
| `mystery_clue` | 线索可见性、公平误导、视角限制、揭晓节奏 | 证据状态、目击角度、遗漏动作、读者可复盘细节 |
| `realism_pressure` | 制度/关系压力、社会后果、物件证据、身份语言 | 手续、文件、称谓、沉默成本、后续代价 |
| `strategy_intrigue` | 信息差、表面话、筹码、后手、礼制/规则破坏 | 双层对白、物件位置、旁观者反应、局势转向 |
| `comedy_timing` | 认知错位、节奏停顿、反应递进、关系缓冲 | 停顿、误触、反差动作、短句回弹 |
| `survival_disaster` | 路线、资源消耗、环境损坏、群体秩序 | 可走/不可走空间、身体负担、资源减少、秩序裂口 |
| `generic_scene_pressure` | 当前戏的冲突、信息、选择和牵引 | 现场发现、人物选择、空间压力、章末问题 |

### Action Combat Subtype To Prose

`action_combat` 只是场景功能，不等于“所有动作都写成武侠”。若项目题材轴或项目记忆命中武侠、港式武侠、高武武侠，再按下表选择 subtype package。

| subtype | required_package | drafting focus | prose landing |
| --- | --- | --- | --- |
| `wuxia_combat_design` | `types/网文/武侠/武侠之战斗设计.md` | 起手、拆招、变招、代价、胜负余波 | 招路有路径，攻防有判断，胜负来自细小破局 |
| `wuxia_blade_qi_flow` | `types/网文/武侠/白刃剑气流.md` | 剑气/刀气/剑风、刀剑风压、兵器碰撞、材质破坏、港式武侠爆点 | 出刃路径 -> 实体接触 -> 材质响应 -> 人物代价 -> 余波留痕 |
| `non_wuxia_action` | N/A 或按其他题材目录选择 | 追逐、搏斗、逃生、枪战、灾难动作等非武侠功能 | 只写当前题材支持的动作物理与空间压力，不套武侠剑气 |

白刃剑气流命中时，正文必须把气流落回实体武器、身法、内力、风雾水汽和现场碰撞；可以写石阶、大石、树木、树枝、湿泥、尘土、木屑、水汽、金属火星等破坏与余波，但不能写成修仙法术、激光能量、现代 CG 光效或无源爆炸。

## Quantified Drafting Gate

- 每个正式章节至少对 1 个关键场面判断是否需要 `genre_scene_route`；若当前章没有强类型场面，可记录 `N/A: no high-impact genre scene`.
- 每个被强化的关键场面必须有 1 个 primary scene function；secondary functions 不超过 2 个。
- 命中 subtype 时必须在 `type_package_manifest.loaded_paths` 记录真实文件路径；如果没有加载，必须写 `skipped_reason`，不能默认为“模型知道该题材”。
- 高影响场面建议写出 3-7 个可读 beat：入场压力、触发动作/对白、反应或抵抗、代价/信息、余波/转挂。少于 3 个或超过 7 个需在报告中说明。
- 正文中不得出现 `genre_scene_route`、`scene_function`、`beat_map` 等执行标签。

## Prohibitions

- 不把武侠动作当作所有类型场面的默认写法。
- 不把言情写成占有奖励、脸红模板或纯糖/纯虐清单。
- 不把玄幻写成无代价升级或新造规则。
- 不把恐怖写成形容词堆叠或一次性解释未知。
- 不把悬疑写成作者提前讲解。
- 不把现实题材写成无后果爽点。
- 不为类型化强化新增无源剧情结果、能力规则、天气、光源、爆炸、证据或关系转折。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 初稿是否建立项目题材轴和场景功能轴，而不是单题材模板套用？ | `genre_scene_route` | `FAIL-DRAFT-GENRE-SCENE` | `N2-SOURCE-LOCK` / `N5-CREATIVE-DRAFT` | `genre_scene_route` |
| 关键场面是否以人物行动、对白、空间、物件、感官选择和后果落到 prose？ | `genre_scene_fit` | `FAIL-DRAFT-GENRE-SCENE` | `N5-CREATIVE-DRAFT` | `genre_scene_profile`、正文证据 |
| 类型化强化是否没有新增第三正文真源、无源事实或题材越界？ | `genre_scene_boundary` | `FAIL-DRAFT-GENRE-SCENE` | `N5-CREATIVE-DRAFT` | boundary check |
| 命中 subtype 时是否加载真实 package，并把白刃剑气流等细分类型落成动作路径、材质响应和人物代价？ | `genre_scene_subtype_package` | `FAIL-DRAFT-GENRE-SCENE` | `N2-SOURCE-LOCK` / `N5-CREATIVE-DRAFT` | `type_package_manifest`、`genre_scene_subtype_profile` |

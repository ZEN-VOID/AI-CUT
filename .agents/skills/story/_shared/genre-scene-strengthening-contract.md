# Genre Scene Strengthening Contract

本文件是 `story2026` 的跨阶段类型化场面强化合同。它用于把武侠、言情、玄幻、恐怖、悬疑、现实等题材差异，转成章节内具体场面功能的创作约束。

本文件不拥有正文写权，不是独立阶段，不生成平行主稿。正式首写归 `3-初稿`，基于源章的最小局部修复归 `4-润色`，跨设定/规划/正文/验收/return 的连锁修改归 `repair`。

## Core Principle

类型化强化不是“把某个题材模板套进正文”，而是先判断当前项目的题材承诺，再判断当前场景要完成的功能，最后只把必要的场面能力投影到人物行动、对白潜台词、空间限制、物件状态、感官选择、信息节奏和章末牵引。

## Two-Axis Route

每次触发类型化场面强化时，必须同时建立两条轴：

```yaml
genre_scene_route:
  project_genre_axis:
    source: "0-初始化/north_star.yaml.genre_contract"
    primary_genre:
    secondary_genres: []
    promise_or_corridor:
    forbidden_defaults: []
  scene_function_axis:
    primary_scene_function:
    secondary_scene_functions: []
    scene_obligation:
    pressure_source:
    source_anchor:
  scene_subtype_axis:
    primary_scene_subtype:
    subtype_package_refs: []
    style_memory_refs: []
    material_anchor_set: []
    n_a_reason:
  routing_evidence:
    user_signal:
    planning_signal:
    north_star_signal:
    character_or_relationship_signal:
    space_or_object_signal:
    previous_text_signal:
  boundary_profile:
    owner_stage: "3-初稿 | 4-润色 | repair"
    allowed_change_scope:
    forbidden_expansion:
    fallback_reason:
```

### Supported Scene Functions

| scene_function | applies_when | strengthen_targets | forbidden_defaults |
| --- | --- | --- | --- |
| `action_combat` | 武戏、追逐、搏斗、巷战、战斗、肢体冲突、兵器或能力交锋 | 攻防节拍、站位距离、力量来源、受击材质、动作代价、余波承接 | 不把所有类型写成武侠；不无源爆破、无代价炫技或镜头参数化 |
| `romance_relationship` | 言情、亲密关系、误读、试探、告白、拉扯、破镜、替身、甜宠或虐恋 | 欲望与回避、边界感、对白潜台词、身体距离、共同风险、信任/债务变化 | 不把关系写成占有奖励、脸红模板或纯糖/纯虐清单 |
| `xuanhuan_power` | 玄幻、修仙、奇幻、高武、异能、规则或能力兑现 | 规则显影、能力边界、资源代价、升级收益、环境反馈、见证者认知变化 | 不无代价升级、不新造规则、不让光效替代力量因果 |
| `horror_suspense` | 恐怖、灵异、克苏鲁、规则怪谈、惊悚逃亡 | 威胁遮蔽、信息延迟、感官选择、逃生路径、污染余波、不可直视边界 | 不靠形容词喊恐怖；不把未知一次性解释清楚 |
| `mystery_clue` | 悬疑、侦探、推理、谍战、案件调查、信息博弈 | 线索可见性、公平误导、视角限制、揭晓节奏、证据状态、读者复盘点 | 不把伏笔和线索混用；不靠作者口吻提前解释 |
| `realism_pressure` | 现实、职场、家庭、制度、年代、社会关系、权力压迫 | 制度压力、社会后果、物件证据、身份语言、沉默成本、可见代价 | 不用夸张爽点覆盖现实约束；不让人物无代价胜利 |
| `strategy_intrigue` | 权谋、宫斗、宅斗、商战、政治/组织博弈 | 信息差、礼制/规则破坏、表面话与真实意图、筹码交换、后手代价 | 不让角色集体降智；不把计谋写成事后解释 |
| `comedy_timing` | 喜剧、轻松日常、反差、社死、吐槽、误会连锁 | 节奏停顿、认知错位、反应递进、物件误触、关系缓冲 | 不让笑点破坏人物尊严或主线压力 |
| `survival_disaster` | 末世、灾难、逃生、战争废墟、资源危机 | 空间路线、资源消耗、身体负担、环境损坏、群体秩序变化 | 不把灾难写成背景板；不无视物理和资源约束 |
| `generic_scene_pressure` | 类型证据不足或混合类型无法安全裁决 | 当前冲突、现场发现、人物选择、信息推进、章末牵引 | 不强行激活题材包 |

### Scene Subtype Package Routing

`scene_function` 只解决“这场戏是什么功能”，不能直接替代更细的题材包选择。命中强类型场面时，必须继续判断是否需要 `scene_subtype_axis`；不需要 subtype 时写明 `n_a_reason`。

| scene_function | subtype_signal | subtype_package_refs | strengthen_focus | boundary |
| --- | --- | --- | --- | --- |
| `action_combat` | 武侠打斗、兵器交锋、比武、围杀、追逐 | `.agents/skills/story/3-初稿/types/网文/武侠/武侠之战斗设计.md` | 招路、拆招、距离、变招、动作代价、胜负余波 | 不把非武侠动作默认武侠化 |
| `action_combat` | 白刃剑气流、剑气、刀气、剑风、刀剑风压、港式武侠破坏感 | `.agents/skills/story/3-初稿/types/网文/武侠/白刃剑气流.md`; `.agents/skills/story/4-润色/types/wuxia-blade-qi-repair.md` | 出刃路径、实体接触、材质破坏、人物反震、余波留痕 | 不写修仙法术、激光光束、现代 CG 光效、无源爆破 |
| `romance_relationship` | 狗血言情、替身、破镜、误会、甜虐 | `.agents/skills/story/3-初稿/types/网文/狗血言情/romance-tropes.md`; `.agents/skills/story/3-初稿/types/网文/狗血言情/emotional-tension.md` | 欲望/回避、边界、潜台词、关系选择 | 不写占有奖励、脸红模板 |
| `xuanhuan_power` | 玄幻、修仙、高武、异能规则兑现 | `.agents/skills/story/3-初稿/types/网文/玄幻剧/power-systems.md`; `.agents/skills/story/3-初稿/types/网文/修仙/修仙.md`; `.agents/skills/story/3-初稿/types/网文/高武/高武.md` | 规则触发、能力边界、资源代价、见证者认知 | 不新造无代价能力 |
| `horror_suspense` | 克苏鲁、灵异、规则怪谈、惊悚逃生 | `.agents/skills/story/3-初稿/types/网文/克苏鲁/克苏鲁.md`; `.agents/skills/story/3-初稿/types/网文/悬疑灵异/悬疑灵异.md`; `.agents/skills/story/3-初稿/types/网文/规则怪谈/规则怪谈.md` | 遮蔽、信息延迟、逃生路径、污染余波 | 不一次性解释未知 |
| `mystery_clue` | 侦探、推理、谍战、案件调查 | `.agents/skills/story/3-初稿/types/网文/侦探剧/clue-design.md`; `.agents/skills/story/3-初稿/types/网文/侦探剧/trick-design.md` | 线索可见性、公平误导、证据状态 | 不靠作者提前讲解 |
| `realism_pressure` | 现实、职场、家庭、年代、社会压力 | `.agents/skills/story/3-初稿/types/网文/现实题材/reality-anchoring.md`; `.agents/skills/story/3-初稿/types/网文/现实题材/dialogue-authenticity.md` | 制度后果、身份语言、物件证据、沉默成本 | 不写无后果爽点 |

## Routing Rules

1. 项目题材轴只能来自 `north_star.yaml.genre_contract`、用户显式长期偏好、项目 `MEMORY.md` 或已 validated 的 planning handoff；不能由单个关键词反推。
2. 场景功能轴优先来自当前章 planning、源章 affected span、用户 finding 或已写正文中的真实场景需求。
3. 同一关键场面默认只有 1 个 `primary_scene_function`；最多允许 2 个 secondary functions，并必须说明主次。
4. 若存在强 subtype 信号，必须继续建立 `scene_subtype_axis`，并把真实加载路径写入 owning stage 的 `type_package_manifest` 或 `repair_type_package_manifest`。
5. 高影响场面建议保留 3-7 个可读 beat；少于 3 个 beat 通常承托不足，超过 7 个 beat 必须说明为什么不会拖慢主线。
6. 类型包和题材 profile 只提供素材与风险提醒；正文仍由 owning stage 的 LLM-first 节点创作或修补。
7. 类型化强化不新增无源实体、剧情结果、关系转折、能力规则、天气、光源、灾害或证据。
8. 若类型证据不足，回退 `generic_scene_pressure`，只强化当前戏的压力、信息、空间和人物选择。

## Owner Routing

| task_shape | owner | output |
| --- | --- | --- |
| 新章起草、整章重写、续写中要求把题材场面写进正文 | `3-初稿` | `genre_scene_route`、`genre_scene_profile`、当前章初稿 |
| 已有初稿中某类场面弱、乱、读不清或题材味被磨平 | `4-润色` | `genre_scene_repair_profile`、affected-span patch、润色稿 |
| 修改会牵动设定、规划、前后章节、return actualization 或多阶段验收 | `repair` | impact map、owner-safe stage routes |
| 只想新增独立强化阶段 | 阻断 | 回到 owning stage，不生成第三份正文真源 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否同时建立项目题材轴和场景功能轴，而不是把武侠/动作当默认题材？ | `genre_scene_route` | `FAIL-GENRE-SCENE-ROUTE` | owner `SOURCE/CONTEXT` 节点 | `genre_scene_route` |
| 场面强化是否服务当前章义务、人物压力、信息推进或章末牵引？ | `genre_scene_function` | `FAIL-GENRE-SCENE-FUNCTION` | owner creative node | `scene_obligation`、正文证据 |
| 是否避免题材包机械套用、无源加料、剧情结果越权或新增第三正文真源？ | `genre_scene_boundary` | `FAIL-GENRE-SCENE-BOUNDARY` | owner repair/draft plan | `boundary_profile`、diff 或 draft evidence |
| 高影响场面是否有可读 beat、代价/后果和主次，而不是堆形容词或镜头词？ | `genre_scene_readability` | `FAIL-GENRE-SCENE-READABILITY` | owner creative node | `beat_map`、offending excerpt |
| 命中 subtype 时，是否加载真实 subtype package 并把路径写入 manifest，而不是只凭泛化题材词执行？ | `genre_scene_subtype_package` | `FAIL-GENRE-SCENE-ROUTE` | owner `SOURCE/CONTEXT` 节点 | `type_package_manifest` 或 `repair_type_package_manifest` |

# Screenwriter Style Analysis Contract

`编剧风格解析.md` 是 `shot-by-shot` 输出给 `2-编导` 的编剧/戏剧风格 side context。它只提炼戏剧问题、人物压力、场面调度、潜台词行为、叙事节奏和可拍承托，不写机位、景别、焦段、运镜或分镜编号。

落点：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/编剧风格解析.md`。

## Required Fields

| field | requirement | fail code |
| --- | --- | --- |
| `dramatic_question_seed` | 这一段逼角色面对什么选择、代价或不可回避的问题 | `FAIL-SCREEN-DRAMATIC-Q` |
| `audience_position_seed` | 观众知道、误解、等待、担心或被延迟满足的内容 | `FAIL-SCREEN-AUDIENCE-POS` |
| `character_pressure_seed` | 角色目标、阻碍、隐藏信息、外显策略和关系压力 | `FAIL-SCREEN-CHAR-PRESSURE` |
| `performance_task_seed` | 可执行身体动作、停顿、视线、呼吸、道具动作 | `FAIL-SCREEN-PERF-TASK` |
| `blocking_power_seed` | 人物站坐、高低、远近、入口、障碍物、权力位置等空间调度 | `FAIL-SCREEN-BLOCKING` |
| `dialogue_strategy_seed` | 对白密度、沉默、反问、威胁、信息释放或潜台词节奏 | `FAIL-SCREEN-DIALOGUE` |
| `subtext_layer_seed` | 表面对话背后的真实意图、角色隐藏信息层与潜台词弧线 | `FAIL-SCREEN-SUBTEXT` |
| `emotion_pulse_seed` | 每场的情绪心跳：压抑/爆发/余震/过渡，识别情绪脉冲节奏模式 | `FAIL-SCREEN-EMOTION-PULSE` |
| `scene_state_delta` | 场景开始与结束时，人物关系、信息权力或局势如何改变 | `FAIL-SCREEN-SCENE-DELTA` |
| `controlled_enrichment_seed` | 不新增剧情的环境反应、群体反应、声音、道具余波和可拍承托 | `FAIL-SCREEN-ENRICHMENT` |
| `subplot_weave_seed` | 次要情节如何渗透主线、伏笔如何埋与收、副线对主线的压力输送 | `FAIL-SCREEN-SUBPLOT` |
| `sound_narrative_seed` | 音乐主题、环境音叙事、静默的情绪功能，声音作为叙事工具 | `FAIL-SCREEN-SOUND` |
| `do_not_import` | 不得导入参考片台词、剧情、角色关系、标志性动作和具体画面表达 | `FAIL-SCREEN-DO-NOT` |

## Markdown Shape

`编剧风格解析.md` 至少包含：

1. `## 使用边界`
2. `## 戏剧结构摘要`
3. `## 编剧风格 Seeds`
4. `## 潜台词与情感脉冲`
5. `## 声音叙事接口`
6. `## 次要情节编织`
7. `## 场面调度与表演承托`
8. `## 禁用摄影越权`
9. `## Do Not Import`

## New Field Definitions

### subtext_layer_seed: 潜台词层

| subfield | requirement |
| --- | --- |
| `surface_dialogue_content` | 表层台词说了什么（信息/指令/掩饰） |
| `true_intent_beneath` | 没说出口的真实意图是什么 |
| `hidden_info_layer` | 角色隐藏的信息：秘密、误解、欲望、恐惧 |
| `subtext_arc_design` | 潜台词如何随场景推进而演变：逐渐揭示 / 突然崩塌 / 保持沉默 |
| `audience_vs_character_knowledge` | 观众和角色对真相的认知落差如何制造张力 |

### emotion_pulse_seed: 情绪脉冲

| subfield | requirement |
| --- | --- |
| `pulse_type` | 本场情绪脉冲类型：压迫累积 / 爆发释放 / 余震延续 / 平静过渡 |
| `emotion_accumulation` | 情绪如何在一场内积累，积累的速度和阻力来源 |
| `release_trigger` | 情绪爆发的触发点是什么，爆发形式：爆发式 / 渐进崩溃式 / 突然中断式 |
| `post_release_residual` | 爆发后的情绪余震如何处理，对下一场的情绪遗留 |
| `shared_audience_empathy` | 本场情绪如何建立观众与角色的共情连接 |

### subplot_weave_seed: 次要情节编织

| subfield | requirement |
| --- | --- |
| `subplot_identity` | 次要情节的核心议题是什么，与主线主题的呼应关系 |
| `main_line_pressure` | 副线如何对主线施加压力：延迟 / 揭示 / 干扰 / 加速 |
| `foreshadow_plant_pattern` | 伏笔的埋设节奏：早期暗示 / 中段回收 / 高潮爆发 |
| `subplot_resolution_type` | 副线收束方式：独立闭环 / 汇入主线 / 与主线同频共振 |
| `hidden_connective_tissue` | 次要情节与主线之间是否存在隐藏的因果连接 |

### sound_narrative_seed: 声音叙事接口

| subfield | requirement |
| --- | --- |
| `music_thematic_identity` | 主音乐主题是否对应角色/主题/情感，主题如何随叙事变化 |
| `diegetic_sound_function` | 环境音如何承担叙事功能：场景定位 / 情绪暗示 / 信息载体 |
| `silence_as_narrative` | 静默在何时出现、以何种方式出现，其情绪功能是什么 |
| `sound_early_or_late` | 声音是否提前于画面建立期待，或滞后于画面形成余韵 |
| `audio_visual_counterpoint` | 声音与画面是否形成对位：同步强化 / 反讽 / 延迟揭示 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `编剧风格解析.md` 是否只作为 `2-编导` side context，不改写编导 canonical 正文？ | `GATE-SBS-ADAPT-01` | `FAIL-SBS-ADAPT-SIDE-CONTEXT` | `N5-BRIDGE` | 使用边界、owner handoff 与未改写证明 |
| 戏剧问题、观众位置、角色压力和场景状态差是否完整且有参考证据回指？ | `GATE-SBS-SCREEN-01` | `FAIL-SCREEN-DRAMATIC-Q` | `N5-BRIDGE` | dramatic_question / audience_position / character_pressure / scene_state_delta |
| 观众知道、误解、等待、担心或被延迟满足的内容是否被明确建模？ | `GATE-SBS-SCREEN-01A` | `FAIL-SCREEN-AUDIENCE-POS` | `N5-BRIDGE` | audience_position_seed 与 source_shot_refs |
| 角色目标、阻碍、隐藏信息、外显策略和关系压力是否清楚？ | `GATE-SBS-SCREEN-01B` | `FAIL-SCREEN-CHAR-PRESSURE` | `N5-BRIDGE` | character_pressure_seed |
| 表演任务是否可执行，落在身体动作、停顿、视线、呼吸或道具动作？ | `GATE-SBS-SCREEN-02` | `FAIL-SCREEN-PERF-TASK` | `N5-BRIDGE` | performance_task_seed |
| 场面调度是否说明站坐、高低、远近、入口、障碍物和权力位置，不写摄影机位？ | `GATE-SBS-SCREEN-02A` | `FAIL-SCREEN-BLOCKING` | `N5-BRIDGE` | blocking_power_seed 与禁用摄影越权检查 |
| 对白策略、潜台词层和情绪脉冲是否可拍、可听、可表演？ | `GATE-SBS-SCREEN-03` | `FAIL-SCREEN-SUBTEXT` | `N5-BRIDGE` | dialogue_strategy / subtext_layer / emotion_pulse |
| 对白策略是否说明密度、沉默、反问、威胁、信息释放或潜台词节奏？ | `GATE-SBS-SCREEN-03A` | `FAIL-SCREEN-DIALOGUE` | `N5-BRIDGE` | dialogue_strategy_seed |
| controlled enrichment、次要情节和声音叙事是否只承托主线，不新增剧情事实？ | `GATE-SBS-SCREEN-04` | `FAIL-SCREEN-ENRICHMENT` | `N5-BRIDGE` | controlled_enrichment / subplot / sound_narrative |
| 次要情节是否说明对主线的压力输送、伏笔埋收和收束方式？ | `GATE-SBS-SCREEN-04A` | `FAIL-SCREEN-SUBPLOT` | `N5-BRIDGE` | subplot_weave_seed |
| 声音叙事是否说明音乐主题、环境音、静默、提前/滞后和声画对位？ | `GATE-SBS-SCREEN-04B` | `FAIL-SCREEN-SOUND` | `N5-BRIDGE` | sound_narrative_seed |
| 是否明确禁止机位、景别、焦段、运镜、分镜编号、参考片台词/剧情/角色关系/标志性动作复制？ | `GATE-SBS-SCREEN-05` | `FAIL-SCREEN-DO-NOT` | `N5-BRIDGE` / `N4-PRINCIPLE` | 禁用摄影越权与 Do Not Import 清单 |

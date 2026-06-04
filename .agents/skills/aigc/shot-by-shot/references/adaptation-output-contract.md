# AIGC Adaptation Output Contract

本文件定义 `shot-by-shot` 如何把参考片逐镜分析转成非美学 stage side context：`2-编剧`、`4-导演`、`5-表演`、`7-分镜`、`8-摄影`、`9-光影`、`11-主体` 与 `分镜脚本.md`。风格解析已经收束到 `references/aesthetic-style-analysis-contract.md`，并对齐 `.agents/skills/aigc/3-美学` 六个子技能。

## Bridge Principle

`shot-by-shot` 的桥接输出是 side context，不是 canonical rewrite。

- `2-编剧` 拥有剧本化投影、对白、声画字段和可拍承托主真源。
- `4-导演` 拥有导演批注、导演意图、声画配对和画面化选择主真源。
- `5-表演` 拥有微表情、台词语气、内心外显和演员可执行表演稿主真源。
- `7-分镜` 拥有画面点下方分镜拆分、分镜节奏、动作路径和跨画面连续性主真源。
- `8-摄影` 拥有运镜手法、镜头角度变化、镜头类型、速度和焦点行为主真源。
- `9-光影` 拥有逐分镜光源、色温、空气介质、材质反射和电影光影美学主真源。
- `11-主体` 的角色、场景、道具设计子技能拥有正式设计稿、研究到提示词证据链和画面合同主真源。
- `3-美学` 六子技能拥有正式美学协议主真源；本文件不定义风格解析主合同。
- `shot-by-shot` 只提供临摹原则、参考证据和转换建议，统一落点为 `projects/aigc/<项目名>/shot-by-shot/<reference_slug>/`。

## Non-Aesthetic Canonical Side Context Files

| file | downstream owner | purpose | forbidden |
| --- | --- | --- | --- |
| `编剧风格解析.md` | `2-编剧` | 戏剧问题、人物压力、对白策略、声画字段和可拍承托 | 导演批注、表演稿、机位、景别、焦段、运镜、分镜编号、具体台词复制 |
| `导演风格解析.md` | `4-导演` | 导演意图、场面调度、声画配对、画面化选择和批注方向 | 改写剧本正文、输出表演稿、写摄影参数或分镜编号 |
| `表演风格解析.md` | `5-表演` | 微表情、动作停顿、台词语气、潜台词行为和演员可执行任务 | 改写剧情事实、生成导演批注、写摄影分镜或 prompt |
| `分镜组织解析.md` | `7-分镜` | 参考系、主体起点、动作路径、终点状态、上一画面最终位置承接和分镜节奏 | 凭风格印象补动作、复制参考片动作顺序、改写上游剧本 |
| `摄影解析.md` | `8-摄影` | 可转成摄影阶段 side context 的运镜、视点、构图锚点、焦点行为和注意力交接 | 固定参考片镜头数量、改写上游正文、复制镜头顺序 |
| `光影解析.md` | `9-光影` | 光源叙事、光色母题、空气介质、明暗关系和材质反射 | 改写摄影稿、写灯位图、复制参考片具体光位或专属视觉符号 |
| `主体设计参考解析.md` | `11-主体` | 角色/场景/道具正式设计阶段可二次吸收的参考原则 | 直接生成正式角色、场景、道具提示词终稿 |
| `分镜脚本.md` | 分镜生产 | 标准表格式分镜脚本 | 改变 Numbers 示例 19 列字段或顺序 |

`摄影风格解析.md` 在当前主合同中优先服务 `3-美学/摄影风格`；若用户明确要给生产阶段使用，应输出 `摄影解析.md` 并标明 `side_context_for: 8-摄影`，不得混淆为正式美学协议。

## Screenwriter Compatible Packet

输出文件：`编剧风格解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `dramatic_question_seed` | 从参考片提炼“这一场戏逼角色选择什么” |
| `audience_position_seed` | 观众知道、误解、等待或担心什么 |
| `character_pressure_seed` | 角色目标、阻碍、隐藏信息和外显策略 |
| `performance_task_seed` | 可执行身体动作、停顿、视线、呼吸、道具动作 |
| `blocking_power_seed` | 人物站坐、高低、远近、门口/桌边/光源等空间关系 |
| `dialogue_strategy_seed` | 对白密度、沉默、反问、威胁、信息释放或潜台词节奏 |
| `subtext_layer_seed` | 表面对话背后的真实意图、隐藏信息层与潜台词弧线 |
| `emotion_pulse_seed` | 场内情绪心跳：压抑、爆发、余震或过渡 |
| `scene_state_delta` | 场景开始和结束的权力、信息或情绪状态差 |
| `sound_narrative_seed` | 音乐主题、环境音叙事、静默和声画对位 |
| `do_not_import` | 不得导入参考片台词、剧情、镜头、构图和具体表演 |

## Director Compatible Packet

输出文件：`导演风格解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `directorial_intent_seed` | 参考片如何把场面选择转成可见/可听的导演意图 |
| `audio_visual_pairing_seed` | 声音、沉默、动作、空间反应如何与画面点就近配对 |
| `blocking_choice_seed` | 人物进退、站位、遮挡、视线和空间权力如何服务导演批注 |
| `visible_action_support` | 抽象心理或主题如何落成可拍的动作、环境反应或节奏承托 |
| `annotation_boundary` | 只给导演批注素材，不改写 `2-编剧` 正文或生成 `5-表演` 成稿 |
| `do_not_import` | 不得导入参考片剧情、镜头顺序、台词、构图或具体调度复制 |

## Performance Compatible Packet

输出文件：`表演风格解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `micro_expression_seed` | 可执行微表情、眼神、呼吸、停顿、吞咽、手部动作或步态变化 |
| `line_delivery_seed` | 台词语气、重音、吞吐、沉默和节奏变化的可表演原则 |
| `subtext_behavior_seed` | 潜台词如何通过身体、距离、道具和反应外显 |
| `physiology_reaction_seed` | 紧张、疼痛、疲惫、压迫或释然如何转成生理反应 |
| `performance_boundary` | 只给 `5-表演` 融合改写参考，不新增剧情事实、不写摄影分镜 |
| `do_not_import` | 不得复制参考演员具体表演、口头禅、标志性动作或角色关系 |

## Storyboard Continuity Packet

输出文件：`分镜组织解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `reference_frame_seed` | 可迁移参考系，例如桌沿、门框、走廊中线、角色站位、镜头内固定物 |
| `motion_origin_seed` | 主体运动起点与身体/道具初态 |
| `motion_path_seed` | 主体或道具从起点到终点的可观察路径、方向、相位和遮挡关系 |
| `motion_destination_seed` | 运动终点、停顿姿态、落点、接触面和下一画面可承接状态 |
| `previous_state_carryover_seed` | 上一画面最终位置或状态如何约束当前画面动作 |
| `downstream_cinematography_note` | 给 `8-摄影` 的连续性提醒，不写成镜头参数终稿 |
| `do_not_import` | 不得导入参考片专属动作编排、打斗招式、构图复刻或角色姿势复制 |

## Cinematography Stage Compatible Packet

输出文件：`摄影解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `visual_unit_function` | 该类画面在目标项目中的观看任务 |
| `beat_map_seed` | 注意力、动作相位、信息揭示、情绪转折或空间关系的换镜理由 |
| `rhythm_profile_seed` | 收敛、标准展开、发散强化或断裂停顿的节奏建议 |
| `continuity_seed` | 轴线、运动方向、光色母题、景别梯度和交出点 |
| `camera_grammar_plan_seed` | 景别、视角、景深、焦点、镜头类型、构图、光色、运镜的迁移策略 |
| `functional_projection_payload` | 主体、动作、运镜、构图锚点、光色材质、空间接口、交出点 |
| `shot_detail_style_seed` | 可转成 `8-摄影` 自然中文运镜注入的写法参考 |
| `do_not_import` | 不得固定照抄参考片镜头数量和镜头顺序 |

## Lighting Stage Compatible Packet

输出文件：`光影解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `light_source_semantic_seed` | 主光、辅光、可见光源或不可见光源如何服务叙事语义 |
| `color_temperature_motif_seed` | 冷暖、色温变化和光色母题如何承托情绪或空间 |
| `air_medium_seed` | 烟雾、尘埃、雾气、水汽、反光介质如何让光影可见 |
| `material_reflection_seed` | 皮肤、金属、玻璃、布料、地面等材质如何接收或反射光 |
| `shadow_relation_seed` | 明暗比例、遮挡、投影、压迫或隐藏关系如何服务画面点 |
| `lighting_boundary` | 只给 `9-光影` 逐分镜光影注入参考，不改写 `8-摄影` 或写灯位图 |
| `do_not_import` | 不得复制参考片具体光位、专属色彩组合、构图或标志性画面 |

## Subject Design Reference Packet

输出文件：`主体设计参考解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `character_reference_seed` | 面向角色正式设计阶段的身份压力、体态、服装结构、材质原则 |
| `scene_reference_seed` | 面向场景正式设计阶段的空镜空间秩序、环境压力、装置关系 |
| `prop_reference_seed` | 面向道具正式设计阶段的完整道具主体、功能压力和细节层级 |
| `fixed_image_contract_note` | 角色全身试装照、场景空镜、道具纯色背景 45 度完整近摄的边界提醒 |
| `do_not_import` | 不得复制人物脸、服装纹样、空间构图、道具纹章或地图文字 |

## Storyboard Script Packet

主细则：`references/storyboard-script-contract.md`。

输出文件：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/分镜脚本.md`。

字段必须完全参照 `input/苍穹裂缝·战神降维.numbers` 的 19 列与顺序：

```text
镜号 | 时长 | 画面描述 | 角色1 | 角色描述1 | 角色图1 | 角色2 | 角色描述2 | 角色图2 | 参考 | 景别 | 角色动作 | 情绪 | 场景标签 | 光影氛围 | 音效 | 对白 | 分镜提示词 | 视频运动提示词
```

## Fusion Output Shape

```yaml
imitation_unit:
  source_shot_refs: ["S001"]
  transferable_principle: ""
  project_fit: ""
  screenwriter_bridge: {}
  director_bridge: {}
  performance_bridge: {}
  storyboard_continuity_bridge: {}
  cinematography_bridge: {}
  lighting_bridge: {}
  subject_design_reference: {}
  storyboard_script_row_ref: ""
  forbidden_copy:
    - ""
  risk_check:
    copyright_expression_copy: false
    stage_boundary_violation: false
    aigc_infeasible: false
```

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 桥接输出是否只作为 side context，不改写 `2-编剧`、`4-导演`、`5-表演`、`7-分镜`、`8-摄影`、`9-光影`、`11-主体` canonical 文件？ | `GATE-SBS-ADAPT-01` | `FAIL-SBS-ADAPT-SIDE-CONTEXT` | `N5B-STAGE-BRIDGE` | owner boundary note 与未写 canonical 路径清单 |
| 输出落点是否统一为 `projects/aigc/<项目名>/shot-by-shot/<reference_slug>/`？ | `GATE-SBS-ADAPT-02` | `FAIL-SBS-ADAPT-PATH` | `N7-WRITE-PACKAGE` | output paths 与执行报告落点 |
| `编剧风格解析.md` 是否只给戏剧、表演、调度、潜台词、声音叙事和可拍承托，无摄影越权？ | `GATE-SBS-ADAPT-05` | `FAIL-SBS-ADAPT-SCREEN-PACKET` | `N5B-STAGE-BRIDGE` | screenwriter bridge 字段表与禁用摄影越权检查 |
| `导演风格解析.md` 是否只给导演批注和声画配对参考，不改写剧本或表演稿？ | `GATE-SBS-ADAPT-DIRECTOR` | `FAIL-SBS-ADAPT-DIRECTOR-PACKET` | `N5B-STAGE-BRIDGE` | director bridge 字段表 |
| `表演风格解析.md` 是否只给 `5-表演` 可执行表演参考，不新增剧情事实或摄影分镜？ | `GATE-SBS-ADAPT-PERFORMANCE` | `FAIL-SBS-ADAPT-PERFORMANCE-PACKET` | `N5B-STAGE-BRIDGE` | performance bridge 字段表 |
| `分镜组织解析.md` 是否包含参考系、起点、路径、终点和上一画面承接？ | `GATE-SBS-ADAPT-STORYBOARD` | `FAIL-SBS-ADAPT-STORYBOARD-PACKET` | `N5B-STAGE-BRIDGE` | storyboard continuity bridge 字段表 |
| `摄影解析.md` side context 是否能被 `8-摄影` 消费，且不改写上游正文？ | `GATE-SBS-ADAPT-CINE-STAGE` | `FAIL-SBS-ADAPT-CINE-PACKET` | `N5B-STAGE-BRIDGE` | cinematography stage payload |
| `光影解析.md` side context 是否能被 `9-光影` 消费，且不改写 `8-摄影` 或写灯位图？ | `GATE-SBS-ADAPT-LIGHTING` | `FAIL-SBS-ADAPT-LIGHTING-PACKET` | `N5B-STAGE-BRIDGE` | lighting bridge 字段表 |
| `分镜脚本.md` 是否继承 Numbers 示例 19 列和内容编排，而不复制示例具体表达？ | `GATE-SBS-ADAPT-08` | `FAIL-SBS-ADAPT-STORYBOARD-SCRIPT` | `N5B-STAGE-BRIDGE` | table header、row mapping、example-copy check |

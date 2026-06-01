# AIGC Adaptation Output Contract

本文件定义 `shot-by-shot` 如何把参考片逐镜分析转成 `0-初始化`、`2-编导`、`3-运动`、`4-摄影`、`6-设计` 与分镜生产可消费的项目解析文档。

## Bridge Principle

`shot-by-shot` 的桥接输出是 side context，不是 canonical rewrite。

- `2-编导` 拥有剧本化投影、表演任务、场面调度和声画字段主真源。
- `3-运动` 拥有角色运动的起点、路径、终点、参照系与跨画面连续性主真源。
- `4-摄影` 拥有 `分镜明细：` 注入、镜头节拍、摄影语法和下游 payload 主真源。
- `6-设计` 的角色、场景、道具 `2-设计` 子技能拥有正式设计稿、研究到提示词证据链和画面合同主真源。
- `0-初始化` 拥有 `north_star.yaml` 中 `全局风格 / 细分风格 / 类型元素` 的长期项目真源。
- `shot-by-shot` 只提供临摹原则、参考证据和转换建议，落点是 `shot-by-shot/<reference_slug>/` 目录下的 `全局风格解析.md`、`编剧风格解析.md`、`运动风格解析.md`、`摄影风格解析.md`、`设计风格解析.md`、`分镜脚本.md`。
- 统一输出路径：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/`，不再写入 `CONTEXT/shot-by-shot/<reference_slug>/`。
- canonical 解析文件名为：`全局风格解析.md`、`编剧风格解析.md`、`运动风格解析.md`、`摄影风格解析.md`、`设计风格解析.md`、`分镜脚本.md`。
- 旧文件名 `画面风格解析.md`、`编导解析.md`、`摄影解析.md`、`设计解析.md` 仅可作为 legacy mirror，不再作为主输出合同。

## Global Style Compatible Packet

主细则：`references/global-style-analysis-contract.md`。

输出文件：`全局风格解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `narrative_research` | TL;DR、主题三联、世界三联、时代/地域/叙事类型/节奏倾向 |
| `genre_promise` | 类型核心契约、高光时刻类型、承诺兑现节奏、子类型混合 |
| `visual_motif_seed` | 重复视觉符号、色调节点、标志性视觉承诺、母题语法 |
| `temporal_texture` | 年代质感来源、信号密度、当代干扰处理、时间感构建 |
| `emotion_curve_profile` | 情绪曲线结构、幕情绪档位、高潮情绪类型、情绪余震设计 |
| `route_decision` | `R1/R2/R3/R4` 之一及其证据 |
| `style_foundation` | 媒介属性、2-3 个渲染技术栈、美学范式和叙事服务理由 |
| `pacing_anchor` | 慢/中/快节奏、判断依据、拍摄段落执行字窗 |
| `pollution_audit` | 默认去污染审计；`R4` 时原文保真审计 |
| `style_prompt_candidate` | 默认 200 字以内纯中文无污染全局风格提示词候选 |
| `do_not_import` | 不得导入的参考片具体构图、人物脸、地图文字、道具纹章、镜头顺序、对象细节 |

禁止字段：

- 直接改写 `projects/aigc/<项目名>/0-初始化/north_star.yaml`。
- 直接生成或覆盖 `style_contract.json`。
- 默认模式下把颜色、材质、构图、焦段、光圈、运镜、角色、场景、道具等下游对象细节写入全局风格提示词。
- 把参考片专属构图、纹章、地图字样或镜头顺序写入全局风格底座。

## Screenwriter Compatible Packet

主细则：`references/screenwriter-style-analysis-contract.md`。

输出文件：`编剧风格解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `dramatic_question_seed` | 从参考片提炼"这一场戏逼角色选择什么" |
| `audience_position_seed` | 观众知道、误解、等待或担心什么 |
| `character_pressure_seed` | 角色目标、阻碍、隐藏信息和外显策略 |
| `performance_task_seed` | 可执行身体动作、停顿、视线、呼吸、道具动作 |
| `blocking_power_seed` | 人物站坐、高低、远近、门口/桌边/光源等空间关系 |
| `dialogue_strategy_seed` | 对白密度、沉默、反问、威胁、信息释放或潜台词节奏 |
| `subtext_layer_seed` | 表面对话背后的真实意图、角色隐藏信息层与潜台词弧线 |
| `emotion_pulse_seed` | 每场的情绪心跳：压抑/爆发/余震/过渡，识别情绪脉冲节奏模式 |
| `scene_state_delta` | 场景开始和结束的权力、信息或情绪状态差 |
| `controlled_enrichment_seed` | 不新增剧情的环境、群体反应、声音、道具和余波承托 |
| `subplot_weave_seed` | 次要情节如何渗透主线、伏笔如何埋与收、副线对主线的压力输送 |
| `sound_narrative_seed` | 音乐主题、环境音叙事、静默的情绪功能，声音作为叙事工具 |
| `do_not_import` | 不得导入参考片台词、剧情、镜头、构图和具体表演 |

禁止字段：

- 机位、景别、焦段、镜头运动、`分镜N`、`分镜明细：`、`分镜提示词`
- 参考片具体台词、角色关系、剧情事件、标志性画面复制

## Motion Compatible Packet

输出文件：`运动风格解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `reference_frame_seed` | 可迁移参考系，例如桌沿、门框、走廊中线、角色站位、镜头内固定物 |
| `motion_origin_seed` | 主体运动起点与身体/道具初态 |
| `motion_path_seed` | 主体或道具从起点到终点的可观察路径、方向、相位和遮挡关系 |
| `motion_destination_seed` | 运动终点、停顿姿态、落点、接触面和下一画面可承接状态 |
| `previous_state_carryover_seed` | 上一画面最终位置或状态如何约束当前画面动作 |
| `downstream_cinematography_note` | 给 `4-摄影` 的连续性提醒，不写成镜头参数终稿 |
| `do_not_import` | 不得导入参考片专属动作编排、打斗招式、构图复刻或角色姿势复制 |

禁止字段：

- 直接改写项目 `3-运动` 正文。
- 不看上一画面状态，凭风格印象编造动作路径。
- 把参考片专属动作顺序、姿势组合或运动节奏逐镜复制到目标项目。

## Cinematography Compatible Packet

主细则：`references/cinematography-style-analysis-contract.md`。

输出文件：`摄影风格解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `visual_unit_function` | 该类画面在目标项目中的观看任务 |
| `beat_map_seed` | 注意力、动作相位、信息揭示、情绪转折或空间关系的换镜理由 |
| `rhythm_profile_seed` | 收敛、标准展开、发散强化或断裂停顿的节奏建议 |
| `continuity_seed` | 轴线、运动方向、光色母题、景别梯度和交出点 |
| `point_of_view_profile` | 视点归属：谁的眼睛、视点切换逻辑、主观vs客观边界 |
| `depth_of_field_semantic` | 焦深本身作为叙事工具：前景/后景/清晰/虚化的叙事语义 |
| `light_source_semantic` | 光源方向作为权力隐喻、自然光vs人工光的叙事含义、冷暖光色情绪功能 |
| `cut_grammar_seed` | 切点类型与叙事同步：匹配/跳切/fade/dissolve 及情绪同步逻辑 |
| `camera_movement_taxonomy` | 运动类型系统：推/拉/摇/移/跟/手持/斯坦尼康/无人机及各自叙事语义 |
| `long_take_structure_seed` | 长镜头内部相位组织：焦点转移、调度节奏、运动层级 |
| `format_grammar_seed` | 画幅比与构图比例如何服务叙事节奏，格式选择背后的叙事逻辑 |
| `camera_grammar_plan_seed` | 景别/视角/景深/焦点/镜头类型/构图/光色/运镜的迁移策略 |
| `functional_projection_payload` | 主体、动作、运镜、构图锚点、光色材质、空间接口、交出点 |
| `shot_detail_style_seed` | 可转成自然中文 `分镜明细：` 的写法参考 |

禁止字段：

- 改写项目 `2-编导` 正文。
- 固定照抄参考片镜头数量和镜头顺序。
- 使用无法被 AIGC 图像/视频阶段消费的空泛词。

## Design Compatible Packet

主细则：`references/design-style-analysis-contract.md`。

输出文件：`设计风格解析.md`。

允许字段：

| field | requirement |
| --- | --- |
| `role_design_seed` | 面向 `角色/2-设计`，提炼身份压力、身体姿态、服装结构、材质和颜色策略 |
| `scene_design_seed` | 面向 `场景/2-设计`，提炼空镜空间秩序、材质、光色、道具残留和无人画面约束 |
| `prop_design_seed` | 面向 `道具/2-设计`，提炼完整道具主体、材质细节、功能压力和纯色背景近摄约束 |
| `character_color_material_grammar` | 角色专属色彩系统、色相/饱和度/明度标识身份、服装材质词汇、磨损纹理叙事 |
| `space_narrative_grammar` | 场景空间如何作为角色关系隐喻、装置承载信息、空镜设计语法 |
| `prop_functional_hierarchy` | 道具功能分级：叙事核心道具/场景氛围道具/转场触发物/象征性道具系统 |
| `world_visual_grammar` | 世界观统一视觉规则：符号系统/色彩规则/材质体系/文化视觉标记 |
| `visual_translation_seed` | 把参考片具体美术表达转译成目标项目自有设定 |
| `prompt_boundary` | 明确不得复制的人脸、服装纹样、场景构图、道具纹章、地图文字或专属符号 |

固定画面合同：

- 角色解析必须服务全身服装试装照、纯色背景、无场景环境。
- 场景解析必须服务空镜、无人、无人物剪影。
- 道具解析必须服务纯色背景、45 度视角、完整道具近摄、无人物手、无场景环境。

禁止字段：

- 直接生成角色、场景或道具正式提示词终稿。
- 复制参考片具体人物脸、服装纹样、空间构图、道具纹章或地图标记。
- 混淆三类设计画面合同，例如角色图带场景、场景图带人物、道具图带人物手。

## Storyboard Script Packet

主细则：`references/storyboard-script-contract.md`。

输出文件：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/分镜脚本.md`。

字段必须完全参照 `input/苍穹裂缝·战神降维.numbers` 的 19 列与顺序：

```text
镜号 | 时长 | 画面描述 | 角色1 | 角色描述1 | 角色图1 | 角色2 | 角色描述2 | 角色图2 | 参考 | 景别 | 角色动作 | 情绪 | 场景标签 | 光影氛围 | 音效 | 对白 | 分镜提示词 | 视频运动提示词
```

编排要求：

- 每行对应一个镜头。
- `角色描述1/2` 使用 `[角色名: 描述]`。
- `对白` 无对白时写 `无`。
- `分镜提示词` 使用方括号功能块组织画面构图、主体/人物空间、环境元素、光影与大气、视觉风格/质感、技术参数。
- `视频运动提示词` 以 `[摄影机运镜：...]` 开头，并以 `[时长：<秒数>s]` 收束。
- 可学习示例的信息密度和列编排，不得照搬示例的具体角色、剧情、台词、场景或视觉表达。

## Fusion Output Shape

解析文档中的每条可用建议都应采用：

```yaml
imitation_unit:
  source_shot_refs: ["S001", "S002"]
  transferable_principle: ""
  project_fit: ""
  global_style_bridge:
    narrative_research: {}
    genre_promise: {}
    visual_motif_seed: {}
    temporal_texture: {}
    emotion_curve_profile: {}
    route_decision: {}
    style_foundation: {}
    pacing_anchor: {}
    style_prompt_candidate: ""
  directing_bridge:
    dramatic_question_seed: ""
    audience_position_seed: ""
    performance_task_seed: ""
    blocking_power_seed: ""
    subtext_layer_seed: {}
    emotion_pulse_seed: {}
    subplot_weave_seed: {}
    sound_narrative_seed: {}
  motion_bridge:
    reference_frame_seed: []
    motion_origin_seed: []
    motion_path_seed: []
    motion_destination_seed: []
    previous_state_carryover_seed: []
    downstream_cinematography_note: []
  cinematography_bridge:
    visual_unit_function: ""
    beat_map_seed: []
    point_of_view_profile: {}
    depth_of_field_semantic: {}
    light_source_semantic: {}
    camera_movement_taxonomy: {}
    cut_grammar_seed: {}
    long_take_structure_seed: {}
    format_grammar_seed: {}
    camera_grammar_plan_seed: ""
    functional_projection_payload: []
  design_bridge:
    role_design_seed: []
    scene_design_seed: []
    prop_design_seed: []
    character_color_material_grammar: {}
    space_narrative_grammar: {}
    prop_functional_hierarchy: {}
    world_visual_grammar: {}
    prompt_boundary: []
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
| 桥接输出是否只作为 side context，不改写 `north_star.yaml`、`style_contract.json` 或 `2/3/5` canonical 文件？ | `GATE-SBS-ADAPT-01` | `FAIL-SBS-ADAPT-SIDE-CONTEXT` | `N5-BRIDGE` | 输出包中的 owner boundary note 与未写 canonical 路径清单 |
| 输出落点是否统一为 `projects/aigc/<项目名>/shot-by-shot/<reference_slug>/`？ | `GATE-SBS-ADAPT-02` | `FAIL-SBS-ADAPT-PATH` | `N7-WRITE` | output paths 与执行报告落点 |
| canonical 文件名是否为 `全局风格解析.md`、`编剧风格解析.md`、`摄影风格解析.md`、`设计风格解析.md`、`分镜脚本.md`？ | `GATE-SBS-ADAPT-02` | `FAIL-SBS-ADAPT-PATH` | `N7-WRITE` | 文件清单与 legacy mirror 标注 |
| 旧文件名是否只作为 legacy mirror，不作为主输出合同？ | `GATE-SBS-ADAPT-03` | `FAIL-SBS-ADAPT-LEGACY-NAME` | `N7-WRITE` | legacy mirror note 与 canonical mapping |
| `全局风格解析.md` 是否只给叙事/类型/母题/媒介/节奏/去污染和提示词候选，不导入角色、场景、道具或摄影细节？ | `GATE-SBS-ADAPT-04` | `FAIL-SBS-ADAPT-GLOBAL-PACKET` | `N5-BRIDGE` | global style packet 字段覆盖与 pollution audit |
| `编剧风格解析.md` 是否只给戏剧、表演、调度、潜台词、声音叙事和可拍承托，无机位/景别/运镜/分镜编号？ | `GATE-SBS-ADAPT-05` | `FAIL-SBS-ADAPT-SCREEN-PACKET` | `N5-BRIDGE` | screenwriter bridge 字段表与禁用摄影越权检查 |
| `摄影风格解析.md` 是否给 `visual_unit`、`beat_map`、`camera_grammar_plan`、payload 和可改写 `分镜明细：` 的语法，不改编导正文？ | `GATE-SBS-ADAPT-06` | `FAIL-SBS-ADAPT-CINE-PACKET` | `N5-BRIDGE` | cinematography bridge payload 与编导正文未改写证据 |
| `设计风格解析.md` 是否按角色/场景/道具拆分可迁移资产原则，并保留三类画面合同？ | `GATE-SBS-ADAPT-07` | `FAIL-SBS-ADAPT-DESIGN-PACKET` | `N5-BRIDGE` | design bridge section coverage 与 fixed image contracts |
| `分镜脚本.md` 是否继承 Numbers 示例 19 列和内容编排，而不复制示例具体表达？ | `GATE-SBS-ADAPT-08` | `FAIL-SBS-ADAPT-STORYBOARD-PACKET` | `N5-BRIDGE` | table header、row mapping、example-copy check |
| 每条 `imitation_unit` 是否回指 source shots、迁移原则、项目适配、阶段桥接、禁止照搬和风险检查？ | `GATE-SBS-ADAPT-09` | `FAIL-SBS-ADAPT-FUSION-SHAPE` | `N5-BRIDGE` | `imitation_unit` YAML / report evidence chain |
| 所有阶段桥接建议是否保留 source evidence，而不是变成无来源的风格口号？ | `GATE-SBS-01` | `FAIL-SBS-EVIDENCE` | `N1-INTAKE` / `N5-BRIDGE` | source_shot_refs、timecode/still anchors、evidence grade |
| 是否有任何参考片具体台词、角色、剧情、构图、纹章、地图文字、镜头顺序或对象细节进入桥接输出？ | `GATE-SBS-RIGHTS-03` | `FAIL-RIGHTS-COPY` | `N4-PRINCIPLE` | forbidden-copy ledger 与 pollution audit |

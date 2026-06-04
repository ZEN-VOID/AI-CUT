# Cinematography Style Analysis Contract

`摄影风格解析.md` 是 `shot-by-shot` 输出给 `3-美学/摄影风格` 的摄影语法 side context；生产阶段若需要摄影桥接，应输出 `摄影解析.md` 给 `8-摄影`，光影桥接应输出 `光影解析.md` 给 `9-光影`。它可以讨论景别、视角、焦点、运镜、构图、光影和节奏，但不得改写 `2-编剧`、`4-导演`、`5-表演`、`7-分镜` 或 `8-摄影` canonical 正文，也不得固定照抄参考片镜头数量或顺序。

落点：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/摄影风格解析.md`。

## Required Fields

| field | requirement | fail code |
| --- | --- | --- |
| `visual_unit_function` | 该类画面在目标项目中的观看任务 | `FAIL-CINE-VISUAL-UNIT` |
| `beat_map_seed` | 注意力、动作相位、信息揭示、情绪转折或空间关系的换镜理由 | `FAIL-CINE-BEAT-MAP` |
| `rhythm_profile_seed` | 收敛、标准展开、发散强化或断裂停顿的节奏建议 | `FAIL-CINE-RHYTHM` |
| `continuity_seed` | 轴线、运动方向、光影母题、景别梯度和交出点 | `FAIL-CINE-CONTINUITY` |
| `point_of_view_profile` | 视点归属：谁的眼睛、视点切换逻辑、主观vs客观边界 | `FAIL-CINE-POV` |
| `depth_of_field_semantic` | 焦深本身作为叙事工具：前景/后景/清晰/虚化的叙事语义 | `FAIL-CINE-DOF-SEMANTIC` |
| `light_source_semantic` | 光源作为叙事语义：主光方向如何映射权力关系、自然光vs人工光的叙事含义 | `FAIL-CINE-LIGHT-SEMANTIC` |
| `cut_grammar_seed` | 切点类型与叙事同步：匹配/跳切/fade/dissolve 及情绪同步逻辑 | `FAIL-CINE-CUT-GRAMMAR` |
| `camera_movement_taxonomy` | 运动类型系统：推/拉/摇/移/跟/手持/斯坦尼康/无人机及各自叙事语义 | `FAIL-CINE-MOVE-TYPE` |
| `long_take_structure_seed` | 长镜头内部相位组织：焦点转移、调度节奏、运动层级 | `FAIL-CINE-LONG-TAKE` |
| `format_grammar_seed` | 画幅比与构图比例如何服务叙事节奏，格式选择背后的叙事逻辑 | `FAIL-CINE-FORMAT` |
| `camera_grammar_plan_seed` | 景别、视角、景深、焦点、镜头类型、构图、光影、运镜的迁移策略 | `FAIL-CINE-GRAMMAR-PLAN` |
| `functional_projection_payload` | 主体、动作、运镜、构图锚点、光影、空间接口、交出点 | `FAIL-CINE-PAYLOAD` |
| `shot_detail_style_seed` | 可转成自然中文 `分镜明细：` 的写法参考 | `FAIL-CINE-SHOT-DETAIL` |
| `do_not_import` | 不得导入参考片具体构图、镜头顺序、标志性画面或专属视觉符号 | `FAIL-CINE-DO-NOT` |

## Markdown Shape

`摄影风格解析.md` 或生产阶段 `摄影解析.md` 至少包含：

1. `## 使用边界`
2. `## 摄影语法摘要`
3. `## 视点与焦深语义`
4. `## 光源叙事语法`
5. `## 运动与切点语法`
6. `## 长镜头结构`
7. `## 摄影风格 Seeds`
8. `## 分镜明细写法参考`
9. `## AIGC 可执行性`
10. `## Do Not Import`

## New Field Definitions

### point_of_view_profile: 视点轮廓

| subfield | requirement |
| --- | --- |
| `pov_ownership` | 本场视点归属于谁：单一角色 / 交替 / 全知 / 物体视角 |
| `pov_switch_logic` | 视点切换的触发条件：注意力接力 / 情绪同步 / 信息揭示 / 权力转移 |
| `subjective_vs_objective_boundary` | 主观镜头与客观镜头之间的边界如何划定与切换 |
| `pov_as_narrative_tool` | 视点如何作为叙事工具：限制观众信息 / 建立共情 / 制造误解 / 终极揭示 |

### depth_of_field_semantic: 焦深语义

| subfield | requirement |
| --- | --- |
| `dof_narrative_mode` | 焦深叙事模式：选择性焦点 / 全焦 / 浅焦叙事 / 动态焦点转移 |
| `foreground_semantic` | 前景虚化作为叙事层：前景承载什么信息/情绪，角色如何利用前景 |
| `background_semantic` | 后景清晰/虚化如何参与叙事：后景是威胁/希望/秘密/余波 |
| `rack_focus_trigger` | 焦点切换的触发条件：信息揭示 / 情绪转折 / 权力变化 / 空间切换 |

### light_source_semantic: 光源叙事语义

| subfield | requirement |
| --- | --- |
| `main_light_direction_as_power` | 主光方向如何映射空间权力：顶光压迫 / 底光恐怖 / 侧光分裂 |
| `natural_vs_artificial_narrative` | 自然光 vs 人工光的叙事含义区分 |
| `light_color_temperature_narrative` | 冷暖光源如何承载情绪/时间/空间叙事功能 |
| `light_source_visibility` | 光源是否可见：可见光源制造真实感 / 不可见光源制造氛围感 |

### cut_grammar_seed: 切点语法

| subfield | requirement |
| --- | --- |
| `cut_type_inventory` | 本片使用的切点类型清单：硬切 / 匹配 / jump cut / fade / dissolve / wipe |
| `cut_type_emotion_sync` | 切点类型与情绪的同步规则：硬切强化张力 / dissolve 释放情绪 / fade 延长时间感 |
| `cut_timing_rhythm` | 切点时机与呼吸节奏的关系：提前切制造焦虑 / 延迟切制造压迫 |
| `reaction_shot_pattern` | 反应镜头的使用模式：何时用反应镜头、如何用、频率与节奏 |
| `overlap_cut_usage` | 重叠切点（在同一动作中切到下一镜头）的使用频率与叙事功能 |

### camera_movement_taxonomy: 运动类型系统

| subfield | requirement |
| --- | --- |
| `movement_type_inventory` | 运动类型清单：推/拉/摇/移/跟/手持/斯坦尼康/无人机/升降，各类型的出现频率 |
| `movement_semantic_meaning` | 各运动类型的叙事语义：推进揭示 / 拉出释然 / 摇动搜索 / 跟焦追踪 / 手持制造紧张 |
| `movement_transition_logic` | 不同运动类型之间如何切换，切换的叙事意义 |
| `handheld_narrative_usage` | 手持摄影的使用场景与叙事功能：真实感 / 紧张感 / 观察者视角 / 心理混乱 |
| `movement_speed_rhythm` | 运镜速度如何参与节奏：加速制造紧迫 / 减速制造压迫 / 匀速制造观察感 |

### long_take_structure_seed: 长镜头结构

| subfield | requirement |
| --- | --- |
| `long_take_threshold` | 多长的镜头被视为"长镜头"，参考片对长镜头的定义标准 |
| `phase_organization` | 长镜头内部 phase 如何组织：调度转移 / 焦点转移 / 景别变化 / 情绪递进 |
| `camera_movement_within_take` | 长镜头内部的摄影机运动层级：静止→运动 / 运动→静止 / 纯运动 |
| `spatial_revelation_in_take` | 长镜头如何在单一镜头内完成空间揭示：从封闭到开放 / 从局部到全貌 |
| `long_take_emotion_function` | 长镜头的情绪功能：压抑积累 / 实时压迫 / 观察距离感 / 命运不可逃避感 |

### format_grammar_seed: 格式语法

| subfield | requirement |
| --- | --- |
| `aspect_ratio_choice` | 画幅比选择：16:9 / 2.39:1 / 1.85:1 / 4:3 / 1.33:1 及其叙事功能 |
| `ratio_change_usage` | 画幅比是否在片中发生变化，变化的触发条件和叙事意义 |
| `framing_proportion_logic` | 构图比例如何服务叙事：留白制造孤独 / 满框制造压迫 / 黄金分割制造和谐 |
| `format_downstream_note` | 该画幅比对 AIGC 图像/视频生成的技术约束和提示词影响 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `摄影风格解析.md` 是否只作为 `3-美学/摄影风格` side context，或 `摄影解析.md` 是否只作为 `8-摄影` side context，不改写上游 canonical 正文？ | `GATE-SBS-ADAPT-01` | `FAIL-SBS-ADAPT-SIDE-CONTEXT` | `N5-BRIDGE` | 使用边界与未改写上游正文证据 |
| 视觉单元功能、beat map 和 rhythm profile 是否定义观看任务、换镜理由和节奏画像，而非参数堆叠？ | `GATE-SBS-CINE-01` | `FAIL-CINE-VISUAL-UNIT` | `N5-BRIDGE` | visual_unit_function、beat_map_seed、rhythm_profile_seed |
| `beat_map_seed` 是否说明注意力、动作相位、信息揭示、情绪转折或空间关系的换镜理由？ | `GATE-SBS-CINE-01A` | `FAIL-CINE-BEAT-MAP` | `N5-BRIDGE` | beat_map_seed 与 source_shot_refs |
| `rhythm_profile_seed` 是否给出收敛、标准展开、发散强化或断裂停顿的节奏建议？ | `GATE-SBS-CINE-01B` | `FAIL-CINE-RHYTHM` | `N5-BRIDGE` | rhythm_profile_seed |
| 连续性、视点、焦深和光源语义是否服务叙事与注意力交接？ | `GATE-SBS-CINE-02` | `FAIL-CINE-CONTINUITY` | `N5-BRIDGE` | continuity_seed、point_of_view_profile、depth/light semantic |
| 视点归属、切换逻辑和主客观边界是否清楚？ | `GATE-SBS-CINE-02A` | `FAIL-CINE-POV` | `N5-BRIDGE` | point_of_view_profile |
| 焦深和光源语义是否说明前/后景、清晰/虚化、拉焦触发、光源方向和冷暖功能？ | `GATE-SBS-CINE-02B` | `FAIL-CINE-DOF-SEMANTIC` | `N5-BRIDGE` | depth_of_field_semantic 与 light_source_semantic |
| 切点、运动类型、长镜头 phase 和画幅语法是否从参考证据抽象，而非照抄镜头顺序？ | `GATE-SBS-CINE-03` | `FAIL-CINE-CUT-GRAMMAR` | `N5-BRIDGE` | cut_grammar、movement taxonomy、long_take、format grammar |
| 运动类型系统是否说明运动清单、语义、切换逻辑、手持使用和速度节奏？ | `GATE-SBS-CINE-03A` | `FAIL-CINE-MOVE-TYPE` | `N5-BRIDGE` | camera_movement_taxonomy |
| 长镜头结构是否说明阈值、phase、机位运动层级、空间揭示和情绪功能，不伪造剪辑点？ | `GATE-SBS-CINE-03B` | `FAIL-CINE-LONG-TAKE` | `N5-BRIDGE` | long_take_structure_seed 与 phase map |
| 画幅和构图比例是否说明叙事功能、比例变化和下游 AIGC 约束？ | `GATE-SBS-CINE-03C` | `FAIL-CINE-FORMAT` | `N5-BRIDGE` | format_grammar_seed |
| `camera_grammar_plan_seed`、`functional_projection_payload` 和 `shot_detail_style_seed` 是否能被 `8-摄影` 消费并转成自然中文运镜注入？ | `GATE-SBS-CINE-04` | `FAIL-CINE-PAYLOAD` | `N5-BRIDGE` | camera plan、payload、shot detail style seed |
| 摄影语法计划是否包含景别、视角、景深、焦点、镜头类型、构图、光影和运镜迁移策略？ | `GATE-SBS-CINE-04A` | `FAIL-CINE-GRAMMAR-PLAN` | `N5-BRIDGE` | camera_grammar_plan_seed |
| 是否避免改写编导正文、固定照抄参考片镜头数量/顺序或使用 AIGC 不可消费空泛词？ | `GATE-SBS-CINE-05` | `FAIL-CINE-DO-NOT` | `N5-BRIDGE` / `N4-PRINCIPLE` | Do Not Import、AIGC 可执行性、rights ledger |

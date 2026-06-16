# Design Style Analysis Contract

`设计风格解析.md` 是 `shot-by-shot` 输出给 `3-主体` 的角色、场景、道具 side context。它只提炼可迁移设计原则，不直接生成正式角色设定、场景设定、道具设定或提示词终稿。

落点：`projects/aigc/<项目名>/shot-by-shot/<reference_slug>/设计风格解析.md`。

## Required Sections

| section | downstream | requirement | fail code |
| --- | --- | --- | --- |
| `## 角色解析` | `3-主体/角色/2-设计` | 身份压力、体态、服装结构、可迁移材质/纹理策略、画面合同边界 | `FAIL-DESIGN-ROLE` |
| `## 场景解析` | `3-主体/场景/2-设计` | 空镜空间秩序、环境压力、可迁移装置关系、无人画面约束 | `FAIL-DESIGN-SCENE` |
| `## 道具解析` | `3-主体/道具/2-设计` | 完整道具主体、功能压力、细节层级、纯色背景 45 度完整近摄约束 | `FAIL-DESIGN-PROP` |
| `## 角色色调与材质语法` | `3-主体/角色/2-设计` | 角色专属色彩系统、色相/饱和度/明度如何标识身份、服装材质词汇 | `FAIL-DESIGN-CHAR-COLOR` |
| `## 空间叙事语法` | `3-主体/场景/2-设计` | 场景空间如何作为角色关系的隐喻、装置如何承载信息 | `FAIL-DESIGN-SPACE` |
| `## 道具功能层级` | `3-主体/道具/2-设计` | 道具功能分级：叙事核心道具/场景氛围道具/转场触发物 | `FAIL-DESIGN-PROP-HIERARCHY` |
| `## 世界观视觉语法` | all design | 世界观统一的视觉规则：符号系统/色彩规则/材质体系 | `FAIL-DESIGN-WORLD` |
| `## 视觉转译原则` | all design | 把参考片具体美术表达转译为目标项目自有设定 | `FAIL-DESIGN-TRANSLATION` |
| `## Do Not Import` | all design | 不得复制人物脸、服装纹样、场景构图、道具纹章、地图文字或专属符号 | `FAIL-DESIGN-DO-NOT` |

## Markdown Shape

`设计风格解析.md` 至少包含：

1. `## 使用边界`
2. `## 角色解析`
3. `## 场景解析`
4. `## 道具解析`
5. `## 角色色调与材质语法`
6. `## 空间叙事语法`
7. `## 道具功能层级`
8. `## 世界观视觉语法`
9. `## 视觉转译原则`
10. `## Do Not Import`

## Fixed Image Contracts

- 角色解析服务纯色背景全身服装试装照，无场景环境。
- 场景解析服务空镜、无人、无人物剪影。
- 道具解析服务纯色背景、45 度视角、完整道具近摄、无人物手、无场景环境。

## New Section Definitions

### 角色色调与材质语法

| subfield | requirement |
| --- | --- |
| `color_identity_system` | 角色专属色相/饱和度/明度，识别哪些色彩承担身份标识功能 |
| `color_emotion_mapping` | 色彩如何承载角色情绪和心理状态，色相变化与角色弧线的关系 |
| `color_contrast_with_environment` | 角色色彩与场景色彩的关系：融合/对立/互补/压倒 |
| `material_vocabulary` | 角色服装材质来源：天然纤维/金属/塑料/皮革/丝绸及叙事密度 |
| `wear_and_texture_narrative` | 磨损、褶皱、光泽、纹理如何承载角色历史和叙事压力 |
| `costume_detail_hierarchy` | 服装细节层级：主角标识性细节/类型群像统一材质/时代信号细节 |

### 空间叙事语法

| subfield | requirement |
| --- | --- |
| `space_as_character_metaphor` | 空间如何作为角色关系的隐喻：密闭=压迫 / 开放=自由 / 多门=选择 |
| `environmental_power_mapping` | 环境元素（门/窗/桌/椅/楼梯/障碍物）如何映射空间权力结构 |
| `object_residue_narrative` | 场景中的残留物件（照片/痕迹/遗留物）如何承载叙事信息和历史感 |
| `empty_scene_design_grammar` | 空镜的设计语法：空间秩序/材质/光色/装置关系，无人时场景如何"说话" |
| `spatial_tier_separation` | 空间层级区分：地面层/中层/高层/地下，不同层级承载什么叙事功能 |
| `world_geography_signal` | 场景如何标识世界观地理/文化/时代，地理信号的出现密度 |

### 道具功能层级

| subfield | requirement |
| --- | --- |
| `narrative_core_prop` | 叙事核心道具：贯穿全片、承载核心主题、驱动关键决策的道具 |
| `scene_atmosphere_prop` | 场景氛围道具：定义场景时代/地域/文化的道具，提供空间信息但不驱动叙事 |
| `transition_trigger_prop` | 转场触发道具：用于镜头转场、视觉接力的道具 |
| `symbolic_prop_system` | 象征性道具系统：该片中道具如何被赋予超出物理功能的象征意义 |
| `prop_detail_level_hierarchy` | 道具细节层级：远景可见轮廓/中景可见结构/近景可见纹理/特写可见材质 |
| `prop_movement_narrative` | 道具在镜头中的运动如何参与叙事：拾取/放下/传递/争夺/销毁 |

### 世界观视觉语法

| subfield | requirement |
| --- | --- |
| `symbol_system` | 世界观符号系统：哪些视觉符号是本世界观特有的，如何识别 |
| `color_rule` | 世界观统一的色彩规则：主色调/辅助色/禁忌色，色彩是否有文化含义 |
| `material_system` | 世界观材质体系：哪些材质是本世界观特有的，材质如何标识身份/阶层/阵营 |
| `cultural_visual_markers` | 文化视觉标记：建筑风格/服饰规范/符号纹章/文字语言密度如何构建世界观可信度 |
| `world_visual_coherence` | 世界观的视觉一致性维护：如何在角色/场景/道具之间建立视觉连贯性 |
| `visual_deviation_permit` | 世界观规则的可允许偏离：什么程度的视觉创新不破坏世界观可信度 |

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| `设计风格解析.md` 是否只作为 `3-主体` side context，不直接生成正式角色/场景/道具设定或提示词终稿？ | `GATE-SBS-ADAPT-01` | `FAIL-SBS-ADAPT-SIDE-CONTEXT` | `N5-BRIDGE` | 使用边界、未写正式设计稿证据 |
| 角色、场景、道具三类解析是否分区完整，并对齐对应 `角色/2-设计`、`场景/2-设计`、`道具/2-设计` leaf？ | `GATE-SBS-DESIGN-01` | `FAIL-DESIGN-ROLE` | `N5-BRIDGE` | Required Sections 覆盖表与 downstream handoff |
| 场景解析是否提供空镜空间秩序、环境压力、可迁移装置关系和无人画面约束？ | `GATE-SBS-DESIGN-01A` | `FAIL-DESIGN-SCENE` | `N5-BRIDGE` | `## 场景解析` 与 empty scene constraints |
| 道具解析是否提供完整道具主体、功能压力、细节层级和纯色背景 45 度完整近摄约束？ | `GATE-SBS-DESIGN-01B` | `FAIL-DESIGN-PROP` | `N5-BRIDGE` | `## 道具解析` 与 prop image contract |
| 角色色调材质、空间叙事、道具功能层级和世界观视觉语法是否可迁移，而非复制参考片设计？ | `GATE-SBS-DESIGN-02` | `FAIL-DESIGN-WORLD` | `N5-BRIDGE` | design grammar sections 与 source abstraction |
| 角色色调与材质语法是否说明身份色彩系统、材质词汇、磨损纹理和细节层级？ | `GATE-SBS-DESIGN-02A` | `FAIL-DESIGN-CHAR-COLOR` | `N5-BRIDGE` | character_color_material_grammar |
| 空间叙事语法是否说明环境权力、残留物件、空镜语法、空间层级和地理文化信号？ | `GATE-SBS-DESIGN-02B` | `FAIL-DESIGN-SPACE` | `N5-BRIDGE` | space_narrative_grammar |
| 道具功能层级是否区分叙事核心、氛围、转场、象征系统、细节层级和道具运动？ | `GATE-SBS-DESIGN-02C` | `FAIL-DESIGN-PROP-HIERARCHY` | `N5-BRIDGE` | prop_functional_hierarchy |
| 视觉转译是否把参考片具体人物脸、纹样、空间构图、纹章、地图文字或专属符号转成目标项目自有设定？ | `GATE-SBS-DESIGN-03` | `FAIL-DESIGN-TRANSLATION` | `N5-BRIDGE` / `N4-PRINCIPLE` | visual_translation_seed 与 prompt_boundary |
| 三类画面合同是否无混淆：角色全身试装照无场景，场景空镜无人，道具纯色背景 45 度完整近摄无手无场景？ | `GATE-SBS-DESIGN-04` | `FAIL-DESIGN-DO-NOT` | `N5-BRIDGE` | fixed image contracts 检查 |
| 是否没有直接生成正式提示词终稿或复制参考片具体人物脸、服装纹样、空间构图、道具纹章、地图标记？ | `GATE-SBS-DESIGN-05` | `FAIL-DESIGN-DO-NOT` | `N4-PRINCIPLE` / `N5-BRIDGE` | Do Not Import 与 forbidden-copy ledger |

# AIGC Adaptation Output Contract

本文件定义 `shot-by-shot` 如何把参考片逐镜分析转成 `0-初始化`、`2-编导`、`3-摄影` 与 `5-设计` 可消费的项目 `CONTEXT/` 解析文档。

## Bridge Principle

`shot-by-shot` 的桥接输出是 side context，不是 canonical rewrite。

- `2-编导` 拥有剧本化投影、表演任务、场面调度和声画字段主真源。
- `3-摄影` 拥有 `分镜明细：` 注入、镜头节拍、摄影语法和下游 payload 主真源。
- `5-设计` 的角色、场景、道具 `2-设计` 子技能拥有正式设计稿、研究到提示词证据链和画面合同主真源。
- `0-初始化` 拥有 `north_star.yaml` 中 `全局风格 / 细分风格 / 类型元素` 的长期项目真源。
- `shot-by-shot` 只提供临摹原则、参考证据和转换建议，落点是项目 `CONTEXT/shot-by-shot/<reference_slug>/`。

## 0-初始化 North Star Compatible Packet

允许字段：

| field | requirement |
| --- | --- |
| `north_star_field` | 明确对齐 `全局风格`、`细分风格.画面风格` 或 `类型元素` |
| `global_style_dimension` | 提炼媒介属性、时代属性、光影逻辑、画面质感或避免出现的补强建议 |
| `sub_style_field` | 只服务全片共同画面基调，不写分场景摄影表 |
| `type_element` | 提炼题材、类型母题、类型元素提示词可继承的短语 |
| `safe_phrase_seed` | 可候选进入 north star 的短句，但必须标注为候选，不直接回写 |
| `do_not_import` | 不得导入的参考片具体构图、人物脸、地图文字、道具纹章和镜头顺序 |

禁止字段：

- 直接改写 `projects/aigc/<项目名>/0-初始化/north_star.yaml`。
- 把 `细分风格.画面风格` 写成场景别摄影策略或分镜明细。
- 把参考片专属红幕构图、黑匣纹章、地图字样或镜头顺序写入 `全局风格提示词`。

## 2-编导 Compatible Packet

允许字段：

| field | requirement |
| --- | --- |
| `dramatic_question_seed` | 从参考片提炼“这一场戏逼角色选择什么” |
| `audience_position_seed` | 观众知道、误解、等待或担心什么 |
| `character_pressure_seed` | 角色目标、阻碍、隐藏信息和外显策略 |
| `performance_task_seed` | 可执行身体动作、停顿、视线、呼吸、道具动作 |
| `blocking_power_seed` | 人物站坐、高低、远近、门口/桌边/光源等空间关系 |
| `controlled_enrichment_seed` | 不新增剧情的环境、群体反应、声音、道具和余波承托 |
| `do_not_import` | 不得导入的参考片台词、剧情、镜头、构图和具体表演 |

禁止字段：

- 机位、景别、焦段、镜头运动、`分镜N`、`分镜明细：`
- 参考片具体台词、角色关系、剧情事件、标志性画面复制

## 3-摄影 Compatible Packet

允许字段：

| field | requirement |
| --- | --- |
| `visual_unit_function` | 该类画面在目标项目中的观看任务 |
| `beat_map_seed` | 注意力、动作相位、信息揭示、情绪转折或空间关系的换镜理由 |
| `rhythm_profile_seed` | 收敛、标准展开、发散强化或断裂停顿的节奏建议 |
| `continuity_seed` | 轴线、运动方向、光色母题、景别梯度和交出点 |
| `camera_grammar_plan_seed` | 景别/视角/景深/焦点/镜头类型/构图/光色/运镜的迁移策略 |
| `functional_projection_payload` | 主体、动作、运镜、构图锚点、光色材质、空间接口、交出点 |
| `shot_detail_style_seed` | 可转成自然中文 `分镜明细：` 的写法参考 |

禁止字段：

- 改写项目 `2-编导` 正文。
- 固定照抄参考片镜头数量和镜头顺序。
- 使用无法被 AIGC 图像/视频阶段消费的空泛词。

## 5-设计 Compatible Packet

允许字段：

| field | requirement |
| --- | --- |
| `role_design_seed` | 面向 `角色/2-设计`，提炼身份压力、身体姿态、服装结构、材质和颜色策略 |
| `scene_design_seed` | 面向 `场景/2-设计`，提炼空镜空间秩序、材质、光色、道具残留和无人画面约束 |
| `prop_design_seed` | 面向 `道具/2-设计`，提炼完整道具主体、材质细节、功能压力和纯色背景近摄约束 |
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

## Fusion Output Shape

解析文档中的每条可用建议都应采用：

```yaml
imitation_unit:
  source_shot_refs: ["S001", "S002"]
  transferable_principle: ""
  project_fit: ""
  directing_bridge:
    dramatic_question_seed: ""
    performance_task_seed: ""
    blocking_power_seed: ""
  visual_style_bridge:
    north_star_field: ""
    global_style_dimension: ""
    sub_style_field: ""
    type_element: ""
    safe_phrase_seed: ""
  cinematography_bridge:
    visual_unit_function: ""
    beat_map_seed: []
    camera_grammar_plan_seed: ""
    functional_projection_payload: []
  design_bridge:
    role_design_seed: []
    scene_design_seed: []
    prop_design_seed: []
    prompt_boundary: []
  forbidden_copy:
    - ""
  risk_check:
    copyright_expression_copy: false
    stage_boundary_violation: false
    aigc_infeasible: false
```

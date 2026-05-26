# Output Template

## Output Contract Alignment

本模板承接 `SKILL.md` 的 Output Contract。canonical 解析文件名为 `全局风格解析.md`、`编剧风格解析.md`、`摄影风格解析.md`、`设计风格解析.md` 与 `分镜脚本.md`；旧命名仅可作为兼容镜像。

## Canonical Paths

```text
projects/aigc/<项目名>/shot-by-shot/<reference_slug>/
├── shot-by-shot.md
├── 分镜脚本.md
├── 全局风格解析.md
├── 编剧风格解析.md
├── 摄影风格解析.md
├── 设计风格解析.md
└── 执行报告.md
```

统一落点为 `shot-by-shot/<reference_slug>/`。旧路径 `CONTEXT/shot-by-shot/<reference_slug>/` 停止使用，已废弃。

`shot-by-shot.md` 是主报告；`分镜脚本.md` 是同次拉片包内的标准表格式分镜脚本；同目录下的四份解析是 owning stage 的附加上下文。

## Main Report Skeleton

```markdown
---
项目名: <项目名>
stage: shot-by-shot
reference_slug: <reference_slug>
source_ref: <video path / stills / notes / link>
evidence_grade: confirmed | partial | inferred | insufficient
bridge_targets: [全局风格, 编剧, 摄影, 设计, 分镜脚本]
output_path: projects/aigc/<项目名>/shot-by-shot/<reference_slug>/shot-by-shot.md
review_status: pending | pass | needs_rework | blocked
---

# shot-by-shot

## 思考过程

- business_goal:
- topology_fit:
- step_strategy:
- key_decisions:
- risk_decisions:

## 素材证据

| item | value |
| --- | --- |
| source_ref |  |
| time_range |  |
| evidence_grade |  |
| target_project |  |
| bridge_targets |  |

## 逐镜拆解表

| shot_id | timecode | observable_event | shot_function | directing/blocking | cinematography | editing/sound | design_signal | aigc_feasibility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 临摹原则

| principle_id | source_shots | transferable_principle | project_fit | how_to_apply |
| --- | --- | --- | --- | --- |

## 禁止照搬清单

| source_ref | do_not_copy | reason | safe_translation |
| --- | --- | --- | --- |

## 阶段对接

- `shot-by-shot/<reference_slug>/全局风格解析.md`:
- `shot-by-shot/<reference_slug>/编剧风格解析.md`:
- `shot-by-shot/<reference_slug>/摄影风格解析.md`:
- `shot-by-shot/<reference_slug>/设计风格解析.md`:
- `shot-by-shot/<reference_slug>/分镜脚本.md`:

## 风险与补证

- rights_risk:
- evidence_gap:
- aigc_feasibility_gap:
```

## 全局风格解析 Skeleton

```markdown
# 全局风格解析

## 使用边界

- 这是 `shot-by-shot/<reference_slug>` 提供给项目全局风格底座的 side context，参照 `global-style-director` 的字段逻辑。
- 本解析不直接改写 `north_star.yaml`，不直接生成或覆盖 `style_contract.json`。
- 默认提炼叙事、世界、类型承诺、视觉母题、年代质感、情绪曲线、媒介、渲染技术栈、美学范式与节奏锚点，不复制参考片具体对象、构图、颜色组合、材质组合或镜头顺序。

## 叙事与世界约束

| field | value | evidence | confidence |
| --- | --- | --- | --- |
| tldr |  |  |  |
| theme_triplet |  |  |  |
| world_triplet |  |  |  |
| era |  |  |  |
| region |  |  |  |
| narrative_type |  |  |  |
| pacing_tendency |  |  |  |

## 类型叙事承诺

| genre_core_contract | highlight_type_moments | promise_delivery_rhythm | sub_genre_or_hybrid | source_shots |
| --- | --- | --- | --- | --- |

## 视觉母题系统

| recurring_visual_symbols | color_tonal_nodes | iconic_visual_commitment | motif_grammar | source_shots |
| --- | --- | --- | --- | --- |

## 年代质感语法

| era_signal_source | signal_density | modern_interference | time_sense_construction | source_shots |
| --- | --- | --- | --- | --- |

## 情绪曲线轮廓

| curve_structure | act_emotion_anchor | climax_emotion_type | emotion_residual_design | source_shots |
| --- | --- | --- | --- | --- |

## 路由决议

| route | trigger | reason | fallback |
| --- | --- | --- | --- |

## 媒介与技术栈

| medium | tech_stack | narrative_service_reason | downstream_note |
| --- | --- | --- | --- |

## 美学范式

| aesthetic_paradigm | style_logic | why_it_serves_story | risk |
| --- | --- | --- | --- |

## 叙事节奏锚定

- 节奏档位：
- 判断依据：
- 拍摄段落执行字窗：
- 回退规则：无明确逻辑根源时默认中节奏

## 去污染审计

| item | verdict | evidence | action |
| --- | --- | --- | --- |

## 全局风格提示词候选

> <默认 200 字以内纯中文无污染提示词；R4 时保留用户锁定原文并标明 exact。>

## Do Not Import

-
```

## 编剧风格解析 Skeleton

```markdown
# 编剧风格解析

## 使用边界

- 这是 `shot-by-shot/<reference_slug>` 提供给 `2-编导` 的项目上下文解析，不改写上游正文。
- 不包含机位、景别、运镜、焦段、分镜编号、`分镜明细：` 或 `分镜提示词`。

## 戏剧结构摘要

| unit_id | source_shots | dramatic_question_seed | audience_position_seed | scene_state_delta |
| --- | --- | --- | --- | --- |

## 编剧风格 Seeds

| unit_id | source_shots | character_pressure_seed | dialogue_strategy_seed | controlled_enrichment_seed |
| --- | --- | --- | --- | --- |

## 潜台词与情感脉冲

| unit_id | source_shots | subtext_layer_seed | emotion_pulse_seed |
| --- | --- | --- | --- |

### 潜台词层字段说明

| unit_id | surface_dialogue_content | true_intent_beneath | hidden_info_layer | subtext_arc_design | audience_vs_character_knowledge |
| --- | --- | --- | --- | --- | --- |

### 情绪脉冲字段说明

| unit_id | pulse_type | emotion_accumulation | release_trigger | post_release_residual | shared_audience_empathy |
| --- | --- | --- | --- | --- | --- |

## 声音叙事接口

| unit_id | source_shots | music_thematic_identity | diegetic_sound_function | silence_as_narrative | sound_early_or_late | audio_visual_counterpoint |
| --- | --- | --- | --- | --- | --- | --- |

## 次要情节编织

| unit_id | source_shots | subplot_identity | main_line_pressure | foreshadow_plant_pattern | subplot_resolution_type | hidden_connective_tissue |
| --- | --- | --- | --- | --- | --- | --- |

## 场面调度与表演承托

| unit_id | performance_task_seed | blocking_power_seed | project_fit |
| --- | --- | --- | --- |

## 禁用摄影越权

-

## Do Not Import

-
```

## 摄影风格解析 Skeleton

```markdown
# 摄影风格解析

## 使用边界

- 这是 `shot-by-shot/<reference_slug>` 提供给 `3-摄影` 的项目上下文解析，不改写 `2-编导` 原文。
- 参考写法必须服务 `分镜明细：` 与 `分镜脚本.md`，不复制参考片具体镜头顺序。

## 摄影语法摘要

| unit_id | source_shots | visual_unit_function | rhythm_profile_seed | continuity_seed |
| --- | --- | --- | --- | --- |

## 视点与焦深语义

| unit_id | source_shots | point_of_view_profile | depth_of_field_semantic |
| --- | --- | --- | --- |

### 视点轮廓字段说明

| unit_id | pov_ownership | pov_switch_logic | subjective_vs_objective_boundary | pov_as_narrative_tool |
| --- | --- | --- | --- | --- |

### 焦深语义字段说明

| unit_id | dof_narrative_mode | foreground_semantic | background_semantic | rack_focus_trigger |
| --- | --- | --- | --- | --- |

## 光源叙事语法

| unit_id | source_shots | light_source_semantic |
| --- | --- | --- |

### 光源叙事字段说明

| unit_id | main_light_direction_as_power | natural_vs_artificial_narrative | light_color_temperature_narrative | light_source_visibility |
| --- | --- | --- | --- | --- |

## 运动与切点语法

| unit_id | source_shots | camera_movement_taxonomy | cut_grammar_seed |
| --- | --- | --- | --- |

### 运动类型系统字段说明

| unit_id | movement_type_inventory | movement_semantic_meaning | movement_transition_logic | handheld_narrative_usage | movement_speed_rhythm |
| --- | --- | --- | --- | --- | --- |

### 切点语法字段说明

| unit_id | cut_type_inventory | cut_type_emotion_sync | cut_timing_rhythm | reaction_shot_pattern | overlap_cut_usage |
| --- | --- | --- | --- | --- | --- |

## 长镜头结构

| unit_id | source_shots | long_take_threshold | phase_organization | camera_movement_within_take | spatial_revelation_in_take | long_take_emotion_function |
| --- | --- | --- | --- | --- | --- | --- |

## 摄影风格 Seeds

| unit_id | beat_map_seed | camera_grammar_plan_seed | functional_projection_payload | shot_detail_style_seed |
| --- | --- | --- | --- | --- |

## 分镜明细写法参考

```text
分镜明细：
分镜1: <根据目标项目重写后的自然中文运镜摄影设计，不照搬参考片具体构图。>
```

## AIGC 可执行性

| risk | mitigation |
| --- | --- |

## Do Not Import

-
```

## 设计风格解析 Skeleton

```markdown
# 设计风格解析

## 使用边界

- 这是 `shot-by-shot/<reference_slug>` 提供给 `5-设计` 的项目上下文解析，服务 `角色/2-设计`、`场景/2-设计`、`道具/2-设计`。
- 只提炼可迁移视觉设计原则，不复制参考片具体人物脸、服装纹样、场景构图、道具纹章或专属视觉符号。
- 下游必须遵守：角色为纯色背景全身服装试装照；场景为空镜且无人；道具为纯色背景 45 度完整道具近摄。

## 角色解析

| design_seed_id | source_shots | role_design_need | transferable_principle | visual_design_seed | prompt_boundary |
| --- | --- | --- | --- | --- | --- |

## 场景解析

| scene_seed_id | source_shots | scene_design_need | transferable_principle | empty_scene_seed | prompt_boundary |
| --- | --- | --- | --- | --- | --- |

## 道具解析

| prop_seed_id | source_shots | prop_design_need | transferable_principle | prop_design_seed | prompt_boundary |
| --- | --- | --- | --- | --- | --- |

## 角色色调与材质语法

| seed_id | source_shots | color_identity_system | color_emotion_mapping | color_contrast_with_environment | material_vocabulary | wear_and_texture_narrative | costume_detail_hierarchy |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 空间叙事语法

| seed_id | source_shots | space_as_character_metaphor | environmental_power_mapping | object_residue_narrative | empty_scene_design_grammar | spatial_tier_separation | world_geography_signal |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 道具功能层级

| seed_id | source_shots | narrative_core_prop | scene_atmosphere_prop | transition_trigger_prop | symbolic_prop_system | prop_detail_level_hierarchy | prop_movement_narrative |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 世界观视觉语法

| seed_id | source_shots | symbol_system | color_rule | material_system | cultural_visual_markers | world_visual_coherence | visual_deviation_permit |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 视觉转译原则

-

## Do Not Import

-
```

## 分镜脚本 Skeleton

```markdown
# 分镜脚本

## 使用边界

- 本表字段与内容编排参照 `input/苍穹裂缝·战神降维.numbers`。
- 学习字段组织、镜头生产信息密度和提示词结构，不复制示例具体角色、剧情、台词、场景或视觉表达。

## 字段来源

- source_example: `input/苍穹裂缝·战神降维.numbers`
- canonical_columns: `镜号, 时长, 画面描述, 角色1, 角色描述1, 角色图1, 角色2, 角色描述2, 角色图2, 参考, 景别, 角色动作, 情绪, 场景标签, 光影氛围, 音效, 对白, 分镜提示词, 视频运动提示词`

## 分镜脚本表

| 镜号 | 时长 | 画面描述 | 角色1 | 角色描述1 | 角色图1 | 角色2 | 角色描述2 | 角色图2 | 参考 | 景别 | 角色动作 | 情绪 | 场景标签 | 光影氛围 | 音效 | 对白 | 分镜提示词 | 视频运动提示词 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 生成检查

- 19 列完整：
- 每行一个镜头：
- 无对白写 `无`：
- 角色描述使用 `[角色名: ...]`：
- `分镜提示词` 使用方括号功能块：
- `视频运动提示词` 以 `[摄影机运镜：...]` 开头并以 `[时长：Xs]` 收束：
```

## Report Skeleton

```markdown
# shot-by-shot 执行报告

## 输入

- source_ref:
- project_root:
- output_root: shot-by-shot/<reference_slug>/
- bridge_targets:

## Review Result

- evidence_gate:
- shot_map_gate:
- observation_gate:
- imitation_boundary_gate:
- global_style_bridge_gate:
- screenwriter_bridge_gate:
- cinematography_bridge_gate:
- design_bridge_gate:
- storyboard_script_gate:
- rights_gate:
- output_gate:

## Repair / Block

- repair_actions:
- blocked_reason:
- next_entry:
```
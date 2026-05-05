# Output Template

## Canonical Paths

```text
projects/aigc/<项目名>/shot-by-shot/<reference_slug>/
├── shot-by-shot.md
└── 执行报告.md

projects/aigc/<项目名>/CONTEXT/shot-by-shot/<reference_slug>/
├── 画面风格解析.md
├── 编导解析.md
├── 摄影解析.md
└── 设计解析.md
```

`shot-by-shot.md` 是主报告，末端同技能包名；项目 `CONTEXT/` 下的阶段解析按实际目标阶段可选生成，供 owning stage 作为附加上下文加载。

## Main Report Skeleton

```markdown
---
项目名: <项目名>
stage: shot-by-shot
reference_slug: <reference_slug>
source_ref: <video path / stills / notes / link>
evidence_grade: confirmed | partial | inferred | insufficient
bridge_targets: [0-初始化, 2-编导, 3-摄影, 5-设计]
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

| shot_id | timecode | observable_event | shot_function | directing/blocking | cinematography | editing/sound | aigc_feasibility |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 临摹原则

| principle_id | source_shots | transferable_principle | project_fit | how_to_apply |
| --- | --- | --- | --- | --- |

## 禁止照搬清单

| source_ref | do_not_copy | reason | safe_translation |
| --- | --- | --- | --- |

## 阶段对接

- `CONTEXT/shot-by-shot/<reference_slug>/画面风格解析.md`:
- `CONTEXT/shot-by-shot/<reference_slug>/编导解析.md`:
- `CONTEXT/shot-by-shot/<reference_slug>/摄影解析.md`:
- `CONTEXT/shot-by-shot/<reference_slug>/设计解析.md`:

## 风险与补证

- rights_risk:
- evidence_gap:
- aigc_feasibility_gap:
```

## 画面风格解析 Skeleton

```markdown
# 画面风格解析

## 使用边界

- 这是 `shot-by-shot/<reference_slug>` 提供给 `0-初始化/north_star.yaml` 的项目上下文解析，服务 `全局风格`、`细分风格.画面风格` 与 `类型元素` 的后续复核、补强或回刷。
- 本解析不直接改写 `north_star.yaml`；若需要进入 canonical north star，必须由 `0-初始化` 或明确的 rebootstrap / source-layer sync 任务执行。
- 只提炼可迁移画面语法，不复制参考片具体构图、人物脸、地图文字、道具纹章或镜头顺序。

## North Star 对齐摘要

| north_star_field | 当前项目真源 | reference 可迁移补强 |
| --- | --- | --- |

## 全局风格补强

| style_seed_id | source_shots | global_style_dimension | transferable_principle | north_star_usage |
| --- | --- | --- | --- | --- |

## 细分风格补强

| style_seed_id | source_shots | sub_style_field | transferable_principle | safe_phrase_seed |
| --- | --- | --- | --- | --- |

## 类型元素补强

| type_seed_id | source_shots | type_element | visual_function | type_prompt_usage |
| --- | --- | --- | --- | --- |

## 可回刷建议

```yaml
细分风格:
  画面风格: ""
类型元素:
  类型元素提示词: ""
```

## Do Not Import

-
```

## 编导解析 Skeleton

```markdown
# 编导解析

## 使用边界

- 这是 `shot-by-shot/<reference_slug>` 提供给 `2-编导` 的项目上下文解析，不改写上游正文。
- 不包含机位、景别、运镜、分镜编号或 `分镜明细：`。

## Directing Seeds

| unit_id | source_shots | dramatic_question_seed | audience_position_seed | character_pressure_seed | performance_task_seed | blocking_power_seed | controlled_enrichment_seed |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Do Not Import

-
```

## 摄影解析 Skeleton

```markdown
# 摄影解析

## 使用边界

- 这是 `shot-by-shot/<reference_slug>` 提供给 `3-摄影` 的项目上下文解析，不改写 `2-编导` 原文。
- 参考写法必须服务 `分镜明细：`，不复制参考片具体镜头顺序。

## Cinematography Seeds

| unit_id | source_shots | visual_unit_function | beat_map_seed | rhythm_profile_seed | camera_grammar_plan_seed | functional_projection_payload | shot_detail_style_seed |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 分镜明细写法参考

```text
分镜明细：
分镜1: <根据目标项目重写后的自然中文运镜摄影设计，不照搬参考片具体构图。>
```
```

## 设计解析 Skeleton

```markdown
# 设计解析

## 使用边界

- 这是 `shot-by-shot/<reference_slug>` 提供给 `5-设计` 的项目上下文解析，服务 `角色/2-设计`、`场景/2-设计`、`道具/2-设计`。
- 只提炼可迁移视觉设计原则，不复制参考片具体人物脸、服装纹样、场景构图、道具纹章或专属视觉符号。
- 下游必须遵守：角色为纯色背景全身服装试装照；场景为空镜且无人；道具为纯色背景 45 度完整道具近摄。

## 角色解析

| design_seed_id | source_shots | role_design_need | transferable_principle | visual_design_seed | costume_material_seed | prompt_boundary |
| --- | --- | --- | --- | --- | --- | --- |

## 场景解析

| scene_seed_id | source_shots | scene_design_need | transferable_principle | empty_scene_seed | lighting_material_seed | prompt_boundary |
| --- | --- | --- | --- | --- | --- | --- |

## 道具解析

| prop_seed_id | source_shots | prop_design_need | transferable_principle | prop_design_seed | material_detail_seed | prompt_boundary |
| --- | --- | --- | --- | --- | --- | --- |

## Do Not Import

-
```

## Report Skeleton

```markdown
# shot-by-shot 执行报告

## 输入

- source_ref:
- project_root:
- output_root:
- context_output_root:
- bridge_targets:

## Review Result

- evidence_gate:
- shot_map_gate:
- observation_gate:
- imitation_boundary_gate:
- 2_directing_bridge_gate:
- 3_cinematography_bridge_gate:
- 5_design_bridge_gate:
- 0_visual_style_bridge_gate:
- rights_gate:
- output_gate:

## Repair / Block

- repair_actions:
- blocked_reason:
- next_entry:
```

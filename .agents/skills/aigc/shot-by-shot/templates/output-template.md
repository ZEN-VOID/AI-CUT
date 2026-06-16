# Output Template

## Output Contract Alignment

本模板承接 `SKILL.md` 的 Output Contract。风格解析已对齐 `.agents/skills/aigc/2-美学` 六子技能：`画面基调解析.md`、`角色风格解析.md`、`场景风格解析.md`、`道具风格解析.md`、`摄影风格解析.md`、`分镜风格解析.md`。`分镜脚本.md` 保持 `references/storyboard-script-contract.md` 的 19 列合同不变。

| marker | binding |
| --- | --- |
| Required output | 主拉片报告、启用的 2-美学 side context、可选编剧/运动/摄影 stage 解析、可选标准表格式分镜脚本、执行报告和风险说明 |
| Output format | Markdown 文档包 |
| Output path | `projects/aigc/<项目名>/shot-by-shot/<reference_slug>/` |
| Naming convention | `shot-by-shot.md`、`画面基调解析.md`、`角色风格解析.md`、`场景风格解析.md`、`道具风格解析.md`、`摄影风格解析.md`、`分镜风格解析.md`、`分镜脚本.md`、`执行报告.md` |
| Completion gate | 证据可回指、临摹边界清楚、2-美学字段不越权、AIGC 可执行、无具体表达复制、分镜脚本表头合规 |

## Canonical Paths

```text
projects/aigc/<项目名>/shot-by-shot/<reference_slug>/
├── shot-by-shot.md
├── 画面基调解析.md
├── 角色风格解析.md
├── 场景风格解析.md
├── 道具风格解析.md
├── 摄影风格解析.md
├── 分镜风格解析.md
├── 分镜脚本.md
└── 执行报告.md
```

`分镜脚本.md` 仅在用户要求或任务需要表格式分镜脚本时输出。旧路径 `CONTEXT/shot-by-shot/<reference_slug>/` 停止使用。

## Main Report Skeleton

```markdown
---
项目名: <项目名>
stage: shot-by-shot
reference_slug: <reference_slug>
source_ref: <video path / stills / notes / link>
evidence_grade: confirmed | partial | inferred | insufficient
bridge_targets: [2-美学/画面基调, 2-美学/角色风格, 2-美学/场景风格, 2-美学/道具风格, 2-美学/摄影风格, 2-美学/分镜风格]
output_path: projects/aigc/<项目名>/shot-by-shot/<reference_slug>/shot-by-shot.md
review_status: pending | pass | needs_rework | blocked
---

# shot-by-shot

## Execution Decision Trace

| decision | rule | input_evidence | rationale | output_landing |
| --- | --- | --- | --- | --- |

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

## 2-美学 Side Context

- `shot-by-shot/<reference_slug>/画面基调解析.md`:
- `shot-by-shot/<reference_slug>/角色风格解析.md`:
- `shot-by-shot/<reference_slug>/场景风格解析.md`:
- `shot-by-shot/<reference_slug>/道具风格解析.md`:
- `shot-by-shot/<reference_slug>/摄影风格解析.md`:
- `shot-by-shot/<reference_slug>/分镜风格解析.md`:

## 风险与补证

- rights_risk:
- evidence_gap:
- aigc_feasibility_gap:
```

## Aesthetic Side Context Skeleton

以下骨架用于六份 2-美学解析文件。每份文件必须换成对应标题，例如 `# 画面基调解析`。

```markdown
# <画面基调解析 / 角色风格解析 / 场景风格解析 / 道具风格解析 / 摄影风格解析 / 分镜风格解析>

## 使用边界

- side_context_for:
- not_canonical:
- do_not_import:

## Source Evidence

| evidence_id | source_shots | observable_fact | evidence_grade |
| --- | --- | --- | --- |

## Transferable Principles

| principle_id | source_shots | transferable_principle | project_fit | downstream_use |
| --- | --- | --- | --- | --- |

## Style Seeds

| seed_id | source_shots | allowed_seed | why_it_maps | boundary |
| --- | --- | --- | --- | --- |

## Pollution Audit

| item | risk | action | verdict |
| --- | --- | --- | --- |

## Do Not Import

-
```

## Aesthetic File Focus

| file | required focus |
| --- | --- |
| `画面基调解析.md` | `medium_and_rendering_seed`、`light_atmosphere_seed`、`aesthetic_paradigm_seed`、`master_anchor_candidate`、`global_style_prompt_candidate`、`contamination_scan` |
| `角色风格解析.md` | `silhouette_language_seed`、`hair_makeup_discipline_seed`、`costume_structure_tendency`、`body_tension_seed`、`age_texture_seed`、`performance_appearance_boundary` |
| `场景风格解析.md` | `space_type_seed`、`spatial_pressure_seed`、`material_light_order`、`empty_scene_rule`、`world_geography_signal`、`scene_do_not_import` |
| `道具风格解析.md` | `prop_function_hierarchy`、`material_system_seed`、`detail_density_rule`、`symbol_boundary`、`generation_forbidden_zone`、`prop_do_not_import` |
| `摄影风格解析.md` | `composition_order`、`shot_size_system`、`camera_height_rule`、`camera_movement_profile`、`movement_speed_rhythm`、`continuity_rule_seed` |
| `分镜风格解析.md` | `rhythm_density`、`shot_size_transition`、`shot_combo_grammar`、`transition_logic`、`action_carryover_rule`、`information_reveal_flow` |

## Optional Stage Context Skeleton

```markdown
# 编剧风格解析 / 导演风格解析 / 表演风格解析 / 分镜组织解析 / 摄影解析 / 光影解析

## 使用边界

- side_context_for:
- not_canonical:
- forbidden_overreach:

## Source Evidence

| evidence_id | source_shots | observable_fact | evidence_grade |
| --- | --- | --- | --- |

## Transferable Seeds

| seed_id | source_shots | allowed_seed | downstream_use | do_not_import |
| --- | --- | --- | --- | --- |
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

## Reference Execution Matrix

| reference | load_status | trigger_reason | applied_to | evidence_in_output | verdict | n/a_reason |
| --- | --- | --- | --- | --- | --- | --- |

## Execution Decision Trace

| decision | rule | input_evidence | rationale | output_landing |
| --- | --- | --- | --- | --- |

## Rule Evidence Map

| rule | output_location | evidence |
| --- | --- | --- |

## Review Result

- evidence_gate:
- shot_map_gate:
- observation_gate:
- imitation_boundary_gate:
- aesthetic_bridge_gate:
- storyboard_script_gate:
- rights_gate:
- output_gate:

## N/A Justification

-

## Repair Log

| fail_code | rework_target | action | result |
| --- | --- | --- | --- |
```

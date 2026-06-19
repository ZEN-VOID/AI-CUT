# 4-编剧 Output Template

## Output Contract Alignment

- Required output: `projects/aigc/<项目名>/4-编剧/第N集.md` and `projects/aigc/<项目名>/4-编剧/执行报告.md`.
- Output format: Markdown screenplay plus Markdown execution report.
- Output path: canonical `4-编剧/` project runtime only.
- Naming convention: `第N集.md`; report is `执行报告.md`.
- Completion gate: `GATE-SCR-01..25` blocking failures are zero, including `GATE-SCR-19` anti-scripted draft audit, `GATE-SCR-21` type style context application, `GATE-SCR-22` subject registry application, `GATE-SCR-23` upstream creative direction matrix, `GATE-SCR-24` scene asset context integration, and `GATE-SCR-25` screenplay mode compliance.
- Module trigger evidence: cite `reference_load_manifest` and the matching `Module Trigger Matrix` row.
- Business analysis evidence: include `business_profile`, `screenplay_mode_decision`, `type_axis_selection`, `screenwriting_type_combination_profile`, explicit `jieshuoju_source_unit_coverage_map` and `jieshuoju_field_variety_map` when `screenplay_mode=jieshuoju`, `upstream_creative_direction_matrix`, `type_style_application_map`, `subject_registry_application_map`, `scene_asset_integration_map` or N/A, `genre_narrative_profile`, `dramatic_intent_map`, `dramatization_gap_map`, `controlled_adaptation_plan` or N/A, and `rewrite_scope_check`.
- Quant criteria evidence: include source count, beat count, rhythm maps, climax/hook maps, A/V pair count, and same-frame continuity checks.
- Attention evidence: include drift signals and re-center actions if any.
- Checkpoint evidence: include `CHK-SCOPE`, `CHK-SEMANTIC`, `CHK-VALIDATION`, `CHK-DARWIN` status.
- Prompt eval evidence: include `test-prompts.json` ids and `eval_mode` when evaluation is requested.

## Episode Screenplay Skeleton

```markdown
---
stage: 4-编剧
episode_id: 第N集
source_episode_path: projects/aigc/<项目名>/1-分集/第N集.md
screenplay_mode: zhengju
screenplay_mode_label: 正剧
presentation_type_package: types/presentation/正剧.md
genre_type_package: types/default/default.md
type_combination_id: zhengjuxgeneric
type_combination_policy: presentation_axis_x_genre_axis
type_style_context_path: projects/aigc/<项目名>/2-美学/类型风格.md
subject_registry_context_path: projects/aigc/<项目名>/3-主体/主体注册表.md
scene_asset_context_policy: optional_read_only_with_required_map_when_present
output_path: projects/aigc/<项目名>/4-编剧/第N集.md
upstream_direction_policy: required
dramatic_adaptation_policy: source_grounded_controlled_supplement
narration_policy: zhengju_source_grounded_voice
jieshuoju_source_unit_policy: required_when_jieshuoju
jieshuoju_field_variety_policy: required_when_jieshuoju
genre_profile:
  primary_genre:
  secondary_genre:
rhythm_strategy:
  primary:
  secondary:
screenplay_field_policy: align_with_4_编剧_screenplay_layer
audio_visual_pairing: required
same_frame_continuity: required
review_verdict:
---

# 第N集

## 题材与叙事情节画像

## 剧本呈现模式

- screenplay_mode: `<zhengju | jieshuoju>`
- default_applied: `<true | false>`
- narration_policy: `<zhengju_source_grounded_voice | jieshuoju_narration_only>`
- source_unit_coverage: `<n/a_for_zhengju | required_for_jieshuoju>`
- field_variety_policy: `<n/a_for_zhengju | required_for_jieshuoju>`

## 类型轴组合

- presentation_type_package: `<types/presentation/正剧.md | types/presentation/解说剧.md>`
- genre_type_package: `<types/genre/武侠剧.md | types/genre/玄幻剧.md | types/genre/科幻剧.md | types/genre/魔幻剧.md | types/default/default.md>`
- type_combination_id: `<zhengjuxwuxia | jieshuojuxkehuan | ...>`
- type_combination_summary: `<声音/字段/节奏/补写/高潮尾钩策略摘要>`

## 4-编剧交接摘要

【剧本正文】

### 场景1：内景/外景 地点 - 日/夜 - 天气

环境描写：<地点、空间结构、光照、天气、静置物件、环境声底色；不写剧情解释。>

角色动作：<角色可见动作、姿态、视线、手部、呼吸、空间移动和与道具/他人的接触。>

对白（角色名，语态/状态短语）：“<对白内容>”
对白画面：<该句对白附近的可见承托；不复述对白；若与上一条动作/表情属于同一画面，合并为同一拍摄单位。>

独白（角色）：“<正剧中仅当非引号客观叙事通过派生语音 gate 时使用；解说剧不得用来承接陈述性 source。>”
独白画面：<独白发生时的身体、声线、空间、道具或环境声承托。>

内心独白（角色）：“<用户口语中的内心OS按本字段处理；优先第一人称或明确自指。>”
内心独白画面：<压住未说出口信息时的可见反应、停顿、呼吸、手部或对手未察觉细节。>

旁白（主体）：“<正剧中只有没有合法场内角色可拥有、但必须声音交代的信息才使用；解说剧中陈述性 source 全部使用本字段。>”
旁白画面：<旁白对应的信息载体、现场后果、可见行动、空间/道具/群像承托或留白画面；不复述旁白。>

音效（来源）：“<声音本体>”
音效画面：<声音源头、人物反应、空间承托或不可见来源处理；避免与道具特写/群像画面重复描述同一声源画面。>

道具特写：<关键物件、线索痕迹、归属压力或状态变化。>

心理反应：<把内心信息外化为可感知反应，不写抽象心理结论。>

场面调度：<人物站坐高低、远近、出入口、遮挡、道具归属、视线方向和权力关系变化。>

转场：<硬切、声音桥、动作中断、对比转场、物件串联、环境渐变、重复节奏或跳切压缩之一。>
```

显式 `解说剧` 补充要求：

- 正文不写 `【开场定调】`、`【童谣惊驾】` 等方括号叙事小标题；段落功能进入执行报告。
- 含 3 条及以上旁白对的场景，必须有非旁白视觉字段参与节奏组织。
- 不连续出现 4 组以上无承托 `旁白 + 旁白画面`；开篇 montage 例外必须在报告说明。

## Execution Report Skeleton

```markdown
# 4-编剧 执行报告

## Source Manifest

## Screenplay Mode Decision

| screenplay_mode | explicit_mode_signal | default_applied | mode_reason | narration_policy | script_landing_rule |
| --- | --- | --- | --- | --- | --- |

## Type Axis Selection Map

| presentation_mode | presentation_package | primary_genre_type | genre_package | secondary_genre_types | source_signals | upstream_type_style_basis | confidence | conflict_state | fallback_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Reference Load Manifest

## Execution Decision Trace

| node_id | decision | source_anchor | reference_or_gate | reason | output_landing |
| --- | --- | --- | --- | --- | --- |

## Reference Execution Matrix

| reference | load_status | trigger_reason | applied_to | evidence_in_output | verdict | n/a_reason |
| --- | --- | --- | --- | --- | --- | --- |

## Upstream Context Application Map

| upstream_source | preserved_truth | stage_projection | source_anchor | context_used | local_decision | preservation_check | conflict_or_na |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Upstream Creative Direction Matrix

| upstream_context | direction_role | used_as | script_decision | script_landing | boundary_check | evidence_map |
| --- | --- | --- | --- | --- | --- | --- |

## Type Style Application Map

| type_style_context_path | inherited_genre_rule | signature_element | expression_technique | local_script_decision | preservation_check | verdict |
| --- | --- | --- | --- | --- | --- | --- |

## Screenwriting Type Combination Profile

| combination_id | selected_presentation_strategy | selected_genre_strategy | combined_voice_and_field_strategy | combined_rhythm_strategy | combined_dramatization_strategy | combined_climax_hook_strategy | boundary_checks | report_landing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Subject Registry Application Map

| subject_registry_context_path | subject_type | registry_id_or_name | canonical_name_used | alias_or_source_name | script_landing | drift_check |
| --- | --- | --- | --- | --- | --- | --- |

## Scene Asset Integration Map

| scene_asset_context_path | asset_type | registry_scene_name_or_id | design_or_image_anchor | used_for | script_landing | boundary_check | n/a_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Rule Evidence Map

| rule_or_gate | source_anchor | script_landing | report_evidence | verdict |
| --- | --- | --- | --- | --- |

## Genre Narrative Profile

## Dramatic Intent Map

| source_anchor | dramatic_function | audience_need | character_pressure | must_preserve | script_implication |
| --- | --- | --- | --- | --- | --- |

## Dramatization Gap Map

| source_anchor | gap_type | viewer_risk | allowed_operation | script_landing | n/a_reason |
| --- | --- | --- | --- | --- | --- |

## Controlled Adaptation Plan

| operation | added_or_adjusted_material | source_basis | preservation_check | authorization_status | downstream_impact |
| --- | --- | --- | --- | --- | --- |

## Source To Script Map

## Narration To Voice Adaptation Map

| source_anchor | source_text | screenplay_mode | mode_policy | target_voice_field | voice_owner | derived_voice_line | paired_visual_field | risk_check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Jieshuoju Source Unit Coverage Map

| unit_id | source_anchor | source_text | source_unit_type | landing_policy | narrator_profile | visual_support_type | fidelity_operation | output_landing | coverage_status | risk_check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Jieshuoju Field Variety Map

| scene_id | source_anchor_range | segment_function | scene_heading | dominant_source_unit_types | non_narration_visual_fields | max_narration_pair_run | bracket_heading_check | exception_or_repair | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Audio Visual Pairing Map

## Same Frame Continuity Map

| visual_cluster | time_space_relation | merge_or_keep_decision | kept_field | downstream_split_risk |
| --- | --- | --- | --- | --- |

## AIGC Handoff Manifest

## N/A Justification

| rule_or_reference | why_not_triggered | safe_to_skip_reason |
| --- | --- | --- |

## Rhythm Strategy Map

## Climax Treatment Map

## Episode Final Image Map

## Continuity Detail Map

| script_landing | detail_type | continuity_need | source_or_gap_basis | downstream_need | verdict |
| --- | --- | --- | --- | --- | --- |

## Rewrite Scope Check

| changed_material | scope_type | preserved_fact | risk_level | authorization_status | verdict |
| --- | --- | --- | --- | --- | --- |

## Review Verdict

## Anti Scripted Draft Audit

| checked_sections | script_or_template_signals | anchor_replacement_risk | sentence_pattern_reuse | verdict |
| --- | --- | --- | --- | --- |

## Repair Actions

## Repair Log

| fail_code | rework_target | repair_action | result |
| --- | --- | --- | --- |

## Handoff
```

# Performance Evidence Type Map

## Purpose

本文件统一 `4-表演` 的证据字段结构，避免 `psychological_reaction_evidence`、`actor_performance_control_evidence` 等在 SKILL、steps、references、templates 和 review 中各自漂移。

## Evidence Fields

| evidence_key | owner node | required shape | consumed by |
| --- | --- | --- | --- |
| `psychological_reaction_evidence` | `N3-PERF-PSYCHOLOGICAL` | `source_anchor`、`subject`、`trigger`、`getability_channels`、`projection_target`、`risk_check` | `N7-PERF-DRAFT`、`N8-PERF-REVIEW` |
| `protagonist_inner_voice_evidence` | `N3-PERF-PSYCHOLOGICAL` | `source_anchor`、`original_pov`、`first_person_line`、`screen_support`、`third_person_exception` | `N7-PERF-DRAFT`、`GATE-PERF-01` |
| `actor_performance_control_evidence` | `N4-PERF-ACTOR-CONTROL` | `source_anchor`、`trigger`、`surface_emotion`、`suppressed_emotion`、`hidden_motive`、`micro_expression`、`body_linkage`、`ambient_support`、`micro_dynamics` | `N7-PERF-DRAFT`、`GATE-PERF-01` |
| `objective_action_purity_evidence` | `N5-PERF-SCENE-CRAFT` / `N7-PERF-DRAFT` | `field_anchor`、`risk_terms`、`replacement_action`、`subjective_emotion_projection` | `N8-PERF-REVIEW` |
| `scene_dramatic_map` | `N5-PERF-SCENE-CRAFT` | `scene_id`、`entry_state`、`pressure_source`、`turning_point`、`exit_state`、`embedded_targets` | `N7-PERF-DRAFT`、`GATE-PERF-01` |
| `performance_task_map` | `N2-PERF-TYPE` / `N5-PERF-SCENE-CRAFT` | `scene_id`、`actor_objective`、`obstacle`、`strategy`、`visible_behavior`、`forbidden_explanation` | `N7-PERF-DRAFT` |
| `blocking_power_map` | `N6-PERF-BLOCKING` | `scene_id`、`power_relation`、`height_distance_threshold`、`gaze_or_prop_owner`、`spatial_block`、`embedded_targets` | `GATE-PERF-02` |
| `integration_targets` | `N5-PERF-SCENE-CRAFT` / `N6-PERF-BLOCKING` | `field_anchor`、`inserted_performance_detail`、`must_not_add`、`downstream_note` | `N7-PERF-DRAFT`、`GATE-PERF-02` |
| `advisor_consultation_packet` | `N6.5-PERF-ADVISOR` | `roster_source`、`node_ref`、`pass_ref`、`gate_ref`、`role_lens`、`must_do`、`must_not_do`、`execution_brief`、`routeback_targets` | `N7-PERF-DRAFT`、`GATE-PERF-03` |

## Review Rule

- `N8-PERF-REVIEW` 必须按本表检查证据字段是否有 owner node、字段锚点和下游消费点。
- 证据字段缺失时，必须回到 owner node；不得在执行报告末尾补一段总结来替代节点证据。

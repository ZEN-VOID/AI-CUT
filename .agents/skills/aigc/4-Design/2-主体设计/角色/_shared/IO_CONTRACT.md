# 2-设计 Shared I/O Contract

本文件是 `aigc/4-Design/角色/2-设计` 的输入输出、命名与 handoff 单一真源。

## Inputs

| 类型 | 路径 | 作用 |
| --- | --- | --- |
| 必需 | `projects/aigc/<项目名>/4-Design/角色/1-清单/第N集/角色清单.json` | 当前集角色对象池与证据回链 |
| 必需 | `projects/aigc/<项目名>/3-Detail/第N集.json` | 镜头级角色表现、穿搭、场景与道具事实 |
| 可选 | `projects/aigc/<项目名>/编导/第N集.json` | 用户显式给 legacy 路径时的兼容回退 |
| 必需 | `projects/aigc/<项目名>/0-Init/north_star.yaml` | 项目级世界观、风格与目标 |
| 必需 | `projects/aigc/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段角色侧约束 |
| 必需 | `projects/aigc/<项目名>/2-Global/全局风格/全局风格设计.md` | 项目级审美底座 |
| 必需 | `projects/aigc/<项目名>/2-Global/类型元素.md` | 类型化导演协议 |
| 可选 | `projects/aigc/<项目名>/3-Detail/第N集.json` 中 `分镜组列表[].组间设计.导演意图` | 当前集、当前组的导演人物指导 |
| 可选 | `projects/aigc/<项目名>/4-Design/场景/1-清单/第N集/场景清单.json` | 场景兼容性上下文包 |
| 可选 | `projects/aigc/<项目名>/4-Design/道具/1-清单/第N集/prop_design_bridge.json` | 道具兼容性上下文包 |
| 可选 | `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/*` | 已有角色设计稿，供增量 patch 使用 |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| canonical | `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/character_design.json` | machine-first 角色设计主稿 |
| canonical | `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/[角色名].md` | 与 JSON 同源的人读稿 |
| canonical | `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/_manifest.json` | 本轮输入、命中角色、输出清单与审计摘要 |
| handoff | `agents_plan + patch / note / report` | subagents 返回给父 skill 的思考计划与局部增量 |

## Naming Contract

- `mission_brief_role_design`
- `subagent_brief_设计统筹`
- `subagent_brief_形象建模`
- `subagent_brief_服装设计`
- `subagent_brief_妆容设计`
- `subagent_brief_个性塑造`
- `subagent_brief_角色一致性复核`
- `subagent_brief_真源审计`
- `context_packet_role_list`
- `context_packet_episode_detail`
- `context_packet_global_style`
- `context_packet_scene_bridge`
- `context_packet_prop_bridge`
- `plan_patch_设计统筹`
- `artifact_patch_形象建模`
- `artifact_patch_服装设计`
- `artifact_patch_妆容设计`
- `artifact_patch_个性塑造`
- `review_note_角色一致性`
- `audit_report_真源一致性`
- `synthesis_report_2-设计`

## Slot Ownership

| 角色 | 默认输出 | 负责槽位 |
| --- | --- | --- |
| `设计统筹` | `agents_plan + patch + note + report` | `selected_roles[]`、批次、角色优先级、返工路径 |
| `形象建模` | `agents_plan + patch + note + report` | `visual_anchor`、`face_signature`、`body_signature`、`silhouette_signature`、`casting_reference`、`feature_markers`、`signature_elements`、`story_premise`、`reasoning_pivot`、`structured_fields.attribute_certainty`、`structured_fields.design_guardrails`、`structured_fields.photo_contract` |
| `服装设计` | `agents_plan + patch + note + report` | `wardrobe_profile`、`variation_rules`、`negative_constraints.costume` |
| `妆容设计` | `agents_plan + patch + note + report` | `makeup_profile`、`hair_profile`、`negative_constraints.makeup` |
| `个性塑造` | `agents_plan + patch + note + report` | `personality_profile`、`pose_profile`、`dialogue_presence`、`emotion_anchor` |
| `角色一致性复核` | `note + report` | 冲突字段、返工意见、一致性判断 |
| `真源审计` | `report` | evidence lineage、路径、越权项、完整度 |

## Hard Rules

1. subagents 只能返回 `agents_plan + patch / note / report`，不能直接落盘 canonical 产物。
2. `character_design.json` 是本阶段唯一 machine-first 真源；逐角色 Markdown 必须与其同源。
3. `shape -> costume/makeup/persona -> review -> audit` 的默认顺序不可跳过。
4. `casting_reference` 只作为具象化代理，不得覆盖 `角色清单.json`、`2-Global` 与 `3-Detail` 的证据优先级；最终必须转译为 `feature_markers / signature_elements`。
5. 场景/道具 carrier 只作为只读上下文包，不得反向变成角色设计组的新常驻职责。
6. 未命中的角色不得出现在本轮 `_manifest.json` 或被补空模板。
7. `species / age / gender / skin_tone / body_height / body_weight` 等基础属性若证据不足，必须以 `conservative` 标记或保守措辞落位，不得伪造确定事实。
8. 角色主体摄影字段默认遵循 `竖版 9:16 / 纯黑背景 / 自然站姿 / 单人 / 无多视图`；仅当用户或导演证据明确覆盖时才允许改写，且不得越权扩成导演调度。

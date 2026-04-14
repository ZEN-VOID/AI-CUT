# 2-设计 Shared I/O Contract

本文件是 `aigc/4-Design/服装/2-设计` 的输入输出、命名与 handoff 单一真源。

## Inputs

| 类型 | 路径 | 作用 |
| --- | --- | --- |
| 必需 | `projects/aigc/<项目名>/4-Design/服装/1-清单/第N集/costume_design_bridge.json` | 当前集服装桥接主输入 |
| 必需 | `projects/aigc/<项目名>/4-Design/服装/1-清单/第N集/服装研究.json` | 研究层证据与结论 |
| 必需 | `projects/aigc/<项目名>/4-Design/服装/1-清单/第N集/服装清单.json` | 当前集服装对象池 |
| 可选 | `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/character_design.json` | 角色锚点与角色兼容约束 |
| 必需 | `projects/aigc/<项目名>/3-Detail/第N集.json` | 镜头级穿搭与动作证据 |
| 必需 | `projects/aigc/<项目名>/0-Init/north_star.yaml` | 项目级世界观、风格与目标 |
| 必需 | `projects/aigc/<项目名>/0-Init/init_handoff.yaml` | 初始化阶段服装侧约束 |
| 必需 | `projects/aigc/<项目名>/2-Global/全局风格/全局风格设计.md` | 项目级审美底座 |
| 必需 | `projects/aigc/<项目名>/2-Global/类型元素.md` | 类型化导演协议 |
| 可选 | `projects/aigc/<项目名>/4-Design/服装/2-设计/第N集/*` | 已有服装设计稿，供增量 patch 使用 |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| canonical | `projects/aigc/<项目名>/4-Design/服装/2-设计/第N集/服装设计.json` | machine-first 服装设计主稿 |
| canonical | `projects/aigc/<项目名>/4-Design/服装/2-设计/第N集/<costume_id>-<canonical_label>.md` | 与 JSON 同源的人读稿 |
| canonical | `projects/aigc/<项目名>/4-Design/服装/2-设计/第N集/costume_design_prompt.json` | prompt sidecar |
| canonical | `projects/aigc/<项目名>/4-Design/服装/2-设计/第N集/_manifest.json` | 本轮输入、命中服装、输出清单与审计摘要 |
| handoff | `agents_plan + patch / note / report` | subagents 返回给父 skill 的思考计划与局部增量 |

## Naming Contract

- `mission_brief_costume_design`
- `subagent_brief_服装统筹`
- `subagent_brief_廓形层次设计师`
- `subagent_brief_材质纹样设计师`
- `subagent_brief_配饰连续性设计师`
- `subagent_brief_提示词架构师`
- `subagent_brief_服装一致性复核`
- `subagent_brief_真源审计`
- `context_packet_costume_catalog`
- `context_packet_costume_bridge`
- `context_packet_character_design`
- `plan_patch_服装统筹`
- `artifact_patch_廓形层次设计师`
- `artifact_patch_材质纹样设计师`
- `artifact_patch_配饰连续性设计师`
- `prompt_patch_提示词架构师`
- `review_note_服装一致性`
- `audit_report_真源审计`
- `synthesis_report_2-设计`

## Slot Ownership

| 角色 | 默认输出 | 负责槽位 |
| --- | --- | --- |
| `服装统筹` | `agents_plan + patch + note + report` | `selected_costumes[]`、批次、优先级、返工路径 |
| `廓形层次设计师` | `agents_plan + patch + note + report` | `design_thesis`、`silhouette_system`、`layering_system` |
| `材质纹样设计师` | `agents_plan + patch + note + report` | `material_and_pattern`、`color_script`、`fabric_finish` |
| `配饰连续性设计师` | `agents_plan + patch + note + report` | `accessory_system`、`mobility_and_continuity`、`negative_constraints` |
| `提示词架构师` | `agents_plan + patch + note + report` | `costume_design_prompt.json.costumes[]` |
| `服装一致性复核` | `note + report` | 冲突字段、返工意见、一致性判断 |
| `真源审计` | `report` | evidence lineage、路径、越权项、完整度 |

## Hard Rules

1. subagents 只能返回 `agents_plan + patch / note / report`，不能直接落盘 canonical 产物。
2. `服装设计.json` 是本阶段唯一 machine-first 真源；逐服装 Markdown 与 `costume_design_prompt.json` 必须与其同源。
3. `统筹 -> specialists -> review -> prompt -> audit` 的默认顺序不可跳过。
4. `character_design.json` 只作为只读约束输入，不得被服装链反向改写。

# 4-Design / 4-道具 / 2-设计 Shared I/O Contract

本文件是 `aigc/4-Design/4-道具/2-设计` 的输入输出、命名与 handoff 单一真源。

## Inputs

| 类型 | 路径 | 作用 |
| --- | --- | --- |
| 必需 | `projects/<项目名>/4-Design/4-道具/1-清单/第N集/prop_design_bridge.json` | 本阶段第一输入根 |
| 必需 | `projects/<项目名>/4-Design/4-道具/1-清单/第N集/道具研究.json` | 研究层补证 |
| 可选 | `projects/<项目名>/4-Design/4-道具/1-清单/第N集/道具清单.json` | 原始 shot/group 回链 |
| 必需 | `projects/<项目名>/3-Detail/第N集.json` | 镜头级事实 |
| 可选 | `projects/<项目名>/2-Global/全局风格.md` | 项目风格锚点 |
| 可选 | `projects/<项目名>/2-Global/类型指导.md` | 项目类型打法约束 |
| 可选 | `projects/<项目名>/0-Init/north_star.yaml` | 风格北极星 |
| 可选 | `projects/<项目名>/0-Init/init_handoff.yaml` | 初始化 handoff |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| canonical | `projects/<项目名>/4-Design/4-道具/2-设计/第N集/道具设计.json` | 道具设计事实与 render contract 真源 |
| sidecar | `projects/<项目名>/4-Design/4-道具/2-设计/第N集/prop_design_prompt.json` | prompt sidecar |
| sidecar | `projects/<项目名>/4-Design/4-道具/2-设计/第N集/_manifest.json` | lineage、coverage 与 path normalization |
| handoff | `agents_plan + patch / note / report` | subagents 返回给父 skill 的思考计划与局部增量 |

## Naming Contract

- `mission_brief_prop_design`
- `subagent_brief_模型师`
- `subagent_brief_材质工艺师`
- `subagent_brief_痕迹叙事师`
- `subagent_brief_提示词架构师`
- `subagent_brief_设计审计`
- `context_packet_模型师`
- `context_packet_材质工艺师`
- `context_packet_痕迹叙事师`
- `context_packet_提示词架构师`
- `context_packet_设计审计`
- `artifact_patch_模型师`
- `artifact_patch_材质工艺师`
- `artifact_patch_痕迹叙事师`
- `prompt_patch_提示词架构师`
- `review_note_设计审计`
- `audit_report_设计审计`
- `synthesis_report`

## Path Normalization Rule

- 若用户或上游 brief 中出现 `projects/<项目名>/4-Design/2-角色/4-道具` 等错位路径，本阶段必须规范化为：
  - `projects/<项目名>/4-Design/4-道具/2-设计/第N集/`
- 规范化行为必须记录到 `_manifest.json.path_normalization`。

## Hard Rules

1. subagents 只能返回 `agents_plan + patch / note / report`，不能直接落盘最终 JSON。
2. `道具设计.json` 只保留稳定设计事实、style refs 与 render contract。
3. `prop_design_prompt.json` 承载长 prompt、布局与调用话术，但不得改写业务事实。
4. 若缺少 `prop_design_bridge.json`，本阶段必须阻塞并回退到 `1-清单`。

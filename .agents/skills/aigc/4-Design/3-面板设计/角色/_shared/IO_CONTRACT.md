# 3-面板 Shared I/O Contract

本文件是 `aigc/4-Design/角色/3-面板` 的输入输出、命名与 packet 责任单一真源。

## Inputs

| 类型 | 路径 | 作用 |
| --- | --- | --- |
| 必需 | `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/character_design.json` | 当前集角色设计 canonical carrier |
| 可选但优先 | `projects/aigc/<项目名>/4-Design/角色/2-设计/第N集/[角色名].md` | 首选 `prompt整合` 提取源 |
| 可选 | `projects/aigc/<项目名>/4-Design/角色/1-清单/第N集/角色清单.json` | identity 与 evidence 补证 |
| 可选 | `projects/aigc/<项目名>/3-Detail/第N集.json` | 兼容回看，不作为第一 prompt 源 |
| 必需 | `.agents/skills/aigc/4-Design/角色/3-面板/templates/角色面板-提示词.json` | 布局模板 |

## Outputs

| 类型 | 路径 | 责任 |
| --- | --- | --- |
| canonical | `projects/aigc/<项目名>/4-Design/角色/3-面板/第N集/<role_id>-<role_name>-<costume_state>-CharacterPanel-layout.json` | 每角色 layout packet |
| canonical | `projects/aigc/<项目名>/4-Design/角色/3-面板/第N集/_manifest.json` | 本轮输入、输出、统计与 handoff 侧车 |

## Naming Contract

- `character_panel_layout_packet`
- `role_panel_prompt_packet`
- `context_packet_character_design`
- `context_packet_role_markdown`
- `synthesis_report_3-面板`

## Hard Rules

1. 第一输入根固定为 `character_design.json`。
2. `prompt整合` 是首选 design_subject 提取源；若缺失，必须显式记录 fallback。
3. packet 只负责 prompt/layout 收束，不直接出图。
4. `_manifest.json` 只记录输入输出与统计，不反写角色设计事实。
5. 输出目录固定为 `projects/aigc/<项目名>/4-Design/角色/3-面板/第N集/`，不得回写到 `2-设计/`。

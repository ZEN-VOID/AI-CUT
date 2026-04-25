---
name: aigc-design-scene
description: Use when producing scene lists, scene design truth, or scene generation handoff under `projects/aigc/<项目名>/4-设计/场景/`.
governance_tier: lite
---

# aigc 5-设计 场景

## Context Loading Contract

- 每次调用 `$aigc-design-scene` 时，必须同时加载同目录 `CONTEXT.md`。
- Domain output lands under `projects/aigc/<项目名>/4-设计/场景/`.

## Runtime Layout

| step | path | responsibility |
| --- | --- | --- |
| `1-清单` | `4-设计/场景/1-清单/` | scene inventory |
| `2-设计` | `4-设计/场景/2-设计/` | canonical scene design |
| `3-生成` | `4-设计/场景/3-生成/` | generation handoff and results |

## LLM-First Creative Authorship Contract

- 场景清单、场景设定、视觉描述、空间叙事功能和生成提示词的 canonical creative truth 必须由 LLM 直接完成。
- `scripts/` 只允许整理输入、套用已存在的 canonical 模板、校验字段完整性、打包设计请求或输出 provider handoff。
- 任何 legacy script authorship 必须显式使用 `--allow-legacy-script-authorship`，并保留错误信息 `LEGACY_SCRIPT_AUTHORSHIP_ERROR` 作为运行期护栏。

## Root-Cause Execution Contract (Mandatory)

- 若场景设计输出缺字段、路径错位或生成阶段无法接续，先回查 `1-清单 -> 2-设计 -> 3-生成` 的阶段边界。
- 若模板、脚本或 slot bundle 检查失败，继续上溯 `references/design-output-contract.md`、`references/design-slot-review-contract.md` 与父级 `5-设计/SKILL.md`。
- 不得通过脚本补写创作正文来掩盖输入缺失；缺失创作判断时回到 LLM 主创环节补齐。

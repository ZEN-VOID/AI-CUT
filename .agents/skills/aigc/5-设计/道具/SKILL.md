---
name: aigc-design-prop
description: Use when the 5-设计 stage needs one prop-domain Skill 2.0 package that runs prop list, prop design, and prop panel prompt generation in order, while writing final prop artifacts directly under `projects/aigc/<项目名>/4-设计/`.
governance_tier: full
metadata:
  short-description: Fuse prop list, design, and panel prompt work
---

# aigc-design-prop

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若当前任务绑定 `projects/aigc/<项目名>/`，还必须先加载项目根 `MEMORY.md`，再按需加载项目根 `CONTEXT/` 中与道具设计有关的文件。
- 本技能是 `.agents/skills/aigc/5-设计/` 下的道具域子技能包；清单、设计、面板不再作为独立 skill 入口展开。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` > `.agents/skills/aigc/SKILL.md` > `.agents/skills/aigc/5-设计/SKILL.md` > 本 `SKILL.md` > 本目录 `references/*` / `steps/*` / `review/*` / `types/*` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Input Contract

- Accepted input: 道具清单生成、道具主体设计、道具面板提示词生成，或要求把原 `1-清单/道具 -> 2-设计/道具 -> 3-面板/道具` 合并执行。
- Required input: `projects/aigc/<项目名>/3-Detail/第N集.json`，或已经存在的道具清单/道具设计文件。
- Optional input: `0-Init/*.yaml`、`2-Global/*.md`、项目 `team.yaml`、已有道具参考图、明确指定的道具主体名。
- Reject or clarify when: 项目名、集数、上游 `3-Detail` 或可替代的道具输入根完全不可定位；用户要求脚本直接主创道具研究/设计正文。

## Mode Selection

| mode | 触发信号 | 执行口径 |
| --- | --- | --- |
| `full_prop_chain` | 从 `3-Detail` 直接生成道具清单、设计文档和面板提示词 | 固定执行 `list -> design -> panel` |
| `design_from_list` | 已有 `道具清单` 或道具对象池 | 从设计节点进入，再生成面板提示词 |
| `panel_from_design` | 已有 `[主体名].md` 或道具设计兼容 JSON | 只生成对应 `[主体名].json` |
| `repair_projection` | 输出路径、模板或提示词侧车漂移 | 按 `review/review-contract.md` 定位并修复 |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 处理顺序与融合边界 | `references/processing-order.md` |
| 从 `3-Detail` 抽取道具对象 | `references/detail-output-consumption-contract.md`、`references/object-normalization-contract.md` |
| 清单输出字段边界 | `references/list-output-contract.md` |
| 道具设计装配与模板机制 | `references/design-input-contract.md`、`references/design-output-contract.md`、`references/prop-design-io-contract.md` |
| 面板提示词与内置 imagegen handoff | `references/smart-image-handoff-contract.md` |
| slot 级审计与返工 | `references/design-slot-review-contract.md`、`review/review-contract.md` |
| 旧清单/设计/面板合同追溯 | `references/legacy/` |

## Execution Contract

1. 锁定项目根、集数、输出根：`projects/aigc/<项目名>/4-设计/`。
2. 按 `types/type-map.md` 判定是整链、清单后半链、设计后半链还是修复。
3. 执行 `steps/processing-workflow.md` 中的顺序门：先清单，后设计，再面板提示词。
4. 清单阶段输出 `道具清单.md`，内部可继续保留旧 JSON 三真源作为兼容侧车，但不得把侧车升为最终交付主稿。
5. 设计阶段完全沿用 `templates/prop_masterprompt.structured.v2.md` 的设计文档结构与既有道具设计机制，逐主体写 `[主体名].md`。
6. 面板阶段完全沿用 `templates/道具面板-提示词.json` 与 SMART handoff 机制，逐主体写 `[主体名].json`。
7. 若调用脚本，脚本只能承担抽取、投影、校验、格式转换、request sidecar 等机械动作；道具研究判断、设计正文和面板 prompt 决策必须由 LLM 主创。

## LLM-First Creative Authorship Contract

- 道具清单判断、道具研究结论、道具设计正文与面板 prompt 决策必须由 LLM 直接完成。
- `scripts/` 中的旧 runner 只允许做抽取、投影、校验、格式转换和兼容侧车落盘。
- 若运行旧脚本需要 `--allow-legacy-script-authorship`，该输出只能视为受控兼容材料，不得直接升为 canonical creative truth。

## Root-Cause Execution Contract (Mandatory)

遇到失败时沿链路上溯：

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> AGENTS.md / skill-工作车间`

优先修复顺序：

1. 输出不在 `projects/aigc/<项目名>/4-设计/` 根：回到本 `Output Contract` 与 `references/processing-order.md`。
2. 道具名把状态句、动作句或服装部件误当主体：回到 `references/object-normalization-contract.md`。
3. 设计文档结构漂移：回到 `templates/prop_masterprompt.structured.v2.md` 与 `references/design-output-contract.md`。
4. 面板 JSON 结构漂移：回到 `templates/道具面板-提示词.json` 与 `references/smart-image-handoff-contract.md`。
5. 旧路径引用断链：回到 `references/legacy/` 与仓库引用扫描结果。

## Field Mapping

| field_id | owner | must_contain |
| --- | --- | --- |
| `PROP-FIELD-01` | `SKILL.md` | 输入合同、顺序门、动态引用、输出合同 |
| `PROP-FIELD-02` | `references/processing-order.md` | 清单 -> 设计 -> 面板的融合细则 |
| `PROP-FIELD-03` | `templates/prop_masterprompt.structured.v2.md` | 当前设计文档模板真源 |
| `PROP-FIELD-04` | `templates/道具面板-提示词.json` | 当前面板提示词 JSON 模板真源 |
| `PROP-FIELD-05` | `review/review-contract.md` | 清单、设计、面板三段验收门 |

## Thought Pass Map

| step_id | thought pass | action pass | evidence |
| --- | --- | --- | --- |
| `PROP-PASS-01` | 判断输入类型 | 进入整链/半链/修复模式 | `prop_type_profile` |
| `PROP-PASS-02` | 判断道具主体 | 写 `道具清单.md` | prop list rows |
| `PROP-PASS-03` | 判断设计模板 | 写 `[道具名].md` | template structure |
| `PROP-PASS-04` | 判断面板 handoff | 写 `[道具名].json` | same-stem JSON |

## Pass Table

| pass_id | pass_condition | rework_entry |
| --- | --- | --- |
| `PROP-PASS` | 清单、设计文档、面板 JSON 都在 5-设计 根目录且同 stem 对齐 | done |
| `PROP-REWORK-LIST` | 道具主体漂移或状态句污染 | `references/object-normalization-contract.md` |
| `PROP-REWORK-DESIGN` | 设计文档模板漂移 | `templates/prop_masterprompt.structured.v2.md` |
| `PROP-REWORK-PANEL` | 面板 JSON 回链失败 | `templates/道具面板-提示词.json` |

## Output Contract

- Required output: `道具清单.md`、N 份以道具主体名命名的设计文档 `[主体名].md`、N 份与设计文档同 stem 的面板提示词 `[主体名].json`。
- Output format: Markdown 清单、Markdown 设计文档、JSON 面板提示词；可选保留 `_manifest.json`、旧 `道具清单.json / 道具研究.json / prop_design_bridge.json / 道具设计.json / prop_design_prompt.json` 作为兼容侧车。
- Output path: `projects/aigc/<项目名>/4-设计/` 根目录。
- Naming convention: 清单固定为 `道具清单.md`；主体设计文档为 `[道具名].md`；面板提示词为 `[道具名].json`，两者 stem 必须一致。
- Completion gate: 输出文件存在且非空；设计文档遵循 `templates/prop_masterprompt.structured.v2.md`；面板 JSON 能回链同 stem 设计文档；`review/review-contract.md` 的清单、设计、面板门全部通过。

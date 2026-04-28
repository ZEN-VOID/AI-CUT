---
name: story-cards-skill
governance_tier: lite
description: Use when story2026 1-设定 needs to generate, rebuild, or repair skill cards for technologies, spells, martial arts, combat skills, craft talents, professional skills, or other capability systems.
---

# 技能卡

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 本技能只负责能力/技能对象判断与正式技能卡 payload，不替父层承担总线路由与最终 gate。

## Overview

`技能卡` 负责把广义“技能”收束为正式能力对象卡。

这里的技能是广义概念，包含但不限于：

- 科幻小说的科技、工程能力、系统权限、机甲/装备操作。
- 玄幻小说的法术、神通、血脉能力、仪式能力。
- 武侠小说的武功、身法、内功、兵器技。
- 现代战争小说的格斗、枪械、战术、侦察、协同作战技能。
- 生活小说的厨艺、才艺、职业技能、社交手腕与手工能力。

它必须直接产出：

- `skill_taxonomy`
- `narrative_functions`
- `activation_rules`
- `limits_and_costs`
- `progression_model`
- `counterplay`

## Business Requirement Analysis Contract

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把“角色会什么/世界能做什么”收束成“有学习条件、有使用规则、有成长线、有克制关系”的正式技能卡。 |
| `business_object` | `1-设定/5-技能卡/**/*.json`、`skill_links`、`progression_hooks` 的下游消费。 |
| `constraint_profile` | 技能卡不能绕过 `north_star.yaml` 的世界规则，也不能替角色卡改写人物命运。 |
| `success_criteria` | 每张技能卡都能回答谁能学、怎样启用、能解决什么、代价是什么、如何升级、如何被克制。 |

## Thinking-Action Network

| step_id | intent | required_output | fail_code | rework_entry |
| --- | --- | --- | --- | --- |
| `S1` | 确认当前真的是技能/能力问题 | `module_route=story-cards > 技能卡/SKILL.md` | `FAIL-CD-SKILL-ROUTE` | 回父技能 |
| `S2` | 判定技能桶与题材语义 | `skill_taxonomy + group` | `FAIL-CD-SKILL-TYPE` | 回类型包 |
| `S3` | 闭合启用、限制与代价 | `activation_rules + limits_and_costs` | `FAIL-CD-SKILL-RULES` | 回规则/代价 |
| `S4` | 建立成长与克制关系 | `progression_model + counterplay` | `FAIL-CD-SKILL-PROGRESSION` | 回成长/克制 |
| `S5` | 映射模板 | `skill-card payload` | `FAIL-CD-SKILL-TEMPLATE` | 回模板映射 |

## Total Input Contract

- `0-初始化/north_star.yaml`
- `0-初始化/init_handoff.yaml`
- 既有 `1-设定/5-技能卡/**/*.json`（若存在）
- mixed/full-build 时来自角色卡的能力接口、成长阶段、限制条件
- mixed/full-build 时来自场景卡的规则、危险、适用空间
- mixed/full-build 时来自物品卡的装备、媒介、消耗品、钥匙物

## One-Shot Output Contract

本技能只交付：

- 正式技能卡 payload
- 可进入索引的 `skill_links`
- 可供 planning/drafting 消费的 `progression_hooks`

## Root-Cause Execution Contract

技能问题优先检查：

1. 技能是否属于可写戏能力，而不只是题材名词。
2. 启用条件、限制和代价是否成立。
3. 成长模型是否与角色弧线和世界规则一致。
4. 克制关系是否能制造冲突，而不是单向开挂。
5. 模板映射是否完整。

## Lite Field Mapping

| field_id | step_id | intent | required_output | fail_code | rework_entry |
| --- | --- | --- | --- | --- | --- |
| `FIELD-CD-SKILL-01` | `S1` | 技能路由正确 | `content.module_route` | `FAIL-CD-SKILL-ROUTE` | 回父技能 |
| `FIELD-CD-SKILL-02` | `S2` | 技能桶成立 | `skill_taxonomy + group` | `FAIL-CD-SKILL-TYPE` | 回类型包 |
| `FIELD-CD-SKILL-03` | `S3` | 使用规则成立 | `activation_rules + limits_and_costs` | `FAIL-CD-SKILL-RULES` | 回规则/代价 |
| `FIELD-CD-SKILL-04` | `S4` | 成长克制成立 | `progression_model + counterplay` | `FAIL-CD-SKILL-PROGRESSION` | 回成长/克制 |
| `FIELD-CD-SKILL-05` | `S5` | 正式模板可写回 | `skill-card payload` | `FAIL-CD-SKILL-TEMPLATE` | 回模板映射 |

## Completion Gate

- 技能不是能力名词堆叠，而是可进入冲突、成长、训练、失败和代价的机制。
- `activation_rules + limits_and_costs` 已成立。
- `progression_model + counterplay` 真正能服务长篇结构。
- 技能卡没有替 `north_star.yaml` 发明新的世界规则源。

## Dispatch Note

- 本技能包名称不承载串行语义。
- 仅当请求完全是技能局部修复，且不要求刷新角色接口/场景规则/物品媒介时，允许与兄弟子技能并发。
- 一旦本轮需要吸收角色、场景或物品最新值，必须在父技能下按 `角色卡 -> 场景卡 -> 物品卡 -> 技能卡` 串行执行。

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 技能分类、启用规则、限制代价、成长模型和克制关系 | `references/skill-card-contract.md` |
| 执行技能卡生成、修复与回写节点 | `steps/skill-card-workflow.md` |
| 判定技能字段、trace 变量和类型桶 | `types/field-map.md` |
| 交付前质量门禁 | `review/review-contract.md` |
| 复用技能卡经验 | `knowledge-base/heuristics.md` |
| 正式 JSON skeleton 与交付报告模板 | `templates/skill-card.json`、`templates/output-template.md` |
| 机械辅助说明 | `scripts/README.md` |
| 产品侧入口元数据 | `agents/openai.yaml` |

## Output Contract

- Required output: `projects/story/<项目名>/1-设定/5-技能卡/**/*.json` 中的正式技能卡 payload。
- Output format: 使用 `templates/skill-card.json` 对齐的 JSON；过程摘要可使用 `templates/output-template.md`。
- Output path: 正式业务输出只写入项目根 `1-设定/5-技能卡/`。
- Naming convention: 技能卡文件名应使用 ASCII 安全 id 或项目既有命名规则，不得写入技能目录。
- Completion gate: 父层 `cards_writer.py` 写回成功，技能规则与世界/角色/场景/物品上游接口一致，coverage / review gate 无 blocking finding。

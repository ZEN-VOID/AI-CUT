---
name: story-cards
governance_tier: full
description: |
  Use when story2026 needs the 1-Cards skill-group guide: route cards tasks to global, type, style, character, scene, and item child skills; coordinate shared inputs, writeback, validation, and source-layer governance.
tools: [Read, Write, Edit, Grep, Bash]
color: amber
---

# 1-Cards

## Role

`1-Cards` 是 `story2026` 的卡片技能组导引层。

它负责判断本轮应该进入哪些子技能、以什么顺序执行、如何回读项目上下文、如何把子技能产物写回 `projects/story/<项目名>/1-Cards/` 并完成 gate。它不直接代替子技能做世界观、题材、风格、角色、场景或物品的创作判断。

一句话边界：

- 父层管路由、依赖、写回、验证与闭环。
- 子技能管各自对象的创作判断、字段成立条件与正式 card payload。
- 脚本只做读取、校验、落盘、统计等机械辅助，不得替代 LLM 主创。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 若任务绑定 `projects/story/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按需读取项目根 `CONTEXT/` 中与本轮 cards 相关的材料。
- 进入任一子技能前，必须加载该子技能自己的 `SKILL.md + CONTEXT.md`。
- 根级 `CONTEXT.md` 只提供 cards 技能组经验与返工启发，不得覆盖本文件的路由、所有权与 gate。

## Skill Group Members

| 子技能 | 负责对象 | 正式输出根 |
| --- | --- | --- |
| `全局卡` | 世界观、规则体系、年代约束、文化艺术、势力格局、科技/武功、金手指 | `1-Cards/0-全局卡/**/*.json` |
| `风格卡` | 整书风格契约、叙事/对白/画面/语言/场面风格、风格漂移 gate | `1-Cards/1-风格卡/**/*.json` |
| `角色卡` | 角色对象真源、关系、成长、专属物接口、关系图谱 | `1-Cards/2-角色卡/**/*.json` + `角色关系图谱.md` |
| `场景卡` | 场景功能、规则、危险、角色适配、复用策略 | `1-Cards/3-场景卡/**/*.json` |
| `物品卡` | 武器、线索、遗物、重要叙事物、归属链、代价、专属适配 | `1-Cards/4-物品卡/**/*.json` |
| `类型卡` | 读者承诺、主副题材组合、题材走廊、禁飞区、planning 导入投影 | `1-Cards/5-类型卡/**/*.json` |

硬边界：

1. 六个成员都是直连 child skills；父层不得把它们重新压回根层 `references/` 或根层 `templates/`。
2. 对象私有模板、字段映射、步骤和审查规则归子技能包本地所有。
3. 父层只聚合被实际调度的子技能产物，不为未调度子技能补空字段或占位稿。
4. 角色、场景、物品存在强依赖：`角色卡 -> 场景卡 -> 物品卡`。
5. `类型卡` 是 planning 默认题材方向盘；`风格卡` 是 drafting/validation 默认写法 gate。

## Mode Selection

| request_shape | 父层动作 | 调度策略 |
| --- | --- | --- |
| 单一对象请求 | 只进入命中的一个子技能 | 可单独执行 |
| 多个独立对象修复 | 只进入命中的子技能 | 无真实依赖时可并行；同一写回目标要串行收束 |
| `mixed` 建卡 | 进入多个子技能并聚合 | `全局卡 -> 类型卡 -> 风格卡 -> 角色卡 -> 场景卡 -> 物品卡` |
| `full-build` | 全量建卡并完成 gate | 固定按 mixed 顺序串行推进 |
| coverage repair | 先读 validator finding，再进入相关子技能 | 只修 blocking finding 指向的对象 |
| source-contract-fix | 修父子合同、模板、writer、validator、tests 的一致性 | 先修真源层，再跑局部 gate |

## Routing Guide

| 用户诉求关键词 | 目标子技能 | 路由说明 |
| --- | --- | --- |
| 世界、规则、年代、文化、势力、武功、科技、金手指 | `全局卡` | 整书级设定与运行规则 |
| 题材、类型、读者承诺、平台感、禁飞区、爽点/虐点边界 | `类型卡` | 故事方向盘和 planning 最小导入 |
| 气质、文风、对白、镜头感、叙事口吻、语言节奏 | `风格卡` | 写法合同和风格漂移约束 |
| 人物、关系、成长、伤口、欲望、专属物接口 | `角色卡` | 人物对象真源和关系网络 |
| 地点、空间、危险、规矩、常驻场、返场价值 | `场景卡` | 可写戏空间与规则压力 |
| 武器、道具、线索、遗物、钥匙、代价、归属 | `物品卡` | 剧情杠杆和使用成本 |

若请求同时命中多个对象，优先用依赖链判断顺序，而不是按技能目录名称判断。

## Shared Runtime Contract

正式写回和验证默认经由共享脚本辅助完成：

- `.agents/skills/story/scripts/cards_writer.py`
- `.agents/skills/story/scripts/cards_coverage_validator.py`
- `.agents/skills/story/scripts/story.py`

脚本职责仅限机械流程：

- 读取项目输入与既有 cards
- 投影子技能产出的结构化 payload
- 原子写入 JSON / Markdown side output
- 校验 schema、trace、数量、密度与 route parity
- 生成 gate 报告

脚本不得生成核心创作正文、审美判断、故事判断或对象成立理由。

## Canonical Output Root

正式业务输出只允许落在：

```text
projects/story/<项目名>/1-Cards/
├── 0-全局卡/
├── 1-风格卡/
├── 2-角色卡/
├── 3-场景卡/
├── 4-物品卡/
└── 5-类型卡/
```

禁止把技能目录、临时 sidecar、报告目录或 repo 根层模板当成项目 card 真源。

## Operating Flow

1. 锁定项目根、任务模式与输入范围。
2. 加载本 `SKILL.md + CONTEXT.md`、项目 `MEMORY.md` 与相关项目 `CONTEXT/`。
3. 根据请求路由到一个或多个子技能。
4. 对每个命中子技能加载其 `SKILL.md + CONTEXT.md`，再按其合同读取本地模板、references、steps、review 或 types。
5. 由 LLM 完成对象判断与 payload 创作，脚本只负责投影、落盘或校验。
6. 经 shared writer 写回正式输出根。
7. 经 coverage validator / cards-check 完成 gate。
8. 若失败，按 finding 指向回到父层路由、子技能合同、模板、writer、validator 或 card 内容中最窄的真实根因。

## Quality Gates

| gate | 通过条件 |
| --- | --- |
| 路由 gate | 请求命中对象与子技能 owner 一致 |
| 上下文 gate | 父层、项目记忆、相关项目上下文、命中子技能上下文已加载 |
| 创作权 gate | 核心 card 判断来自 LLM，不来自脚本拼接 |
| trace gate | payload 标记的 `source_skill_id / module_route / loaded_references` 与实际调度一致 |
| schema gate | 输出 JSON 符合对应子技能本地模板 |
| dependency gate | 物品卡没有绕过角色接口与场景规则 |
| coverage gate | 数量、结构、密度、规则刚性和 route parity 通过验证 |

## Root-Cause Contract

非平凡问题必须沿链路上溯：

`Symptom -> Direct Cause -> Source Layer -> Rule Source -> Fix Landing Point`

修复落点优先级：

1. 父层路由、依赖和写回 gate。
2. 子技能 `SKILL.md + CONTEXT.md` 合同。
3. 子技能本地模板、steps、review、types。
4. writer / validator / tests 的运行时一致性。
5. 单张 card 内容。

最终反馈应收束为：

- 根因位置
- 已修复内容
- 验证结果
- 仍需用户裁决的创作选择

## Completion Contract

一次 `1-Cards` 任务完成时，父层只交付一套收束结果：

- 命中的正式 cards 或相关合同修复。
- gate / validation 结论。
- 对未处理对象的明确边界说明。
- 若发生降级或跳过子技能，说明原因和影响。

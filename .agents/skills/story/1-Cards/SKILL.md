---
name: story-cards
governance_tier: full
description: |
  Use when story2026 needs whole-book cards generation, cards rebuild, incremental cards writeback, or cards coverage repair from `Init/north_star_contract.json.cards` and `Init/初始化简报.json`.
tools: [Read, Write, Edit, Grep, Bash]
color: amber
---

# 1-Cards

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 根级 `CONTEXT.md` 只沉淀 cards 经验与返工顺序，不得覆盖本 `SKILL.md` 的对象真源、模板契约与 coverage gate。
- 若模块 `CONTEXT.md` 与根技能合同冲突，以本 `SKILL.md` 和对应 `module-spec.md` 为准。

## 1. 功能描述

`1-Cards` 现在是 `story2026` 的单一 cards skill，不再是“父层编排 + 三个子技能”的目录总线。

它统一承担三件事：

1. 把 `0-Init` 交付的 `north_star_contract + 初始化简报` 收敛为对象真源。
2. 按固定顺序生成并维护 `角色卡 / 场景卡 / 物品卡` 三类正式 JSON 卡。
3. 通过 `references/` 模块按需加载分类细则，而不是把分类细则拆成三个可独立漂移的子技能包。

一句话裁决：

- `Init/north_star_contract.json.cards` 负责长期共同约束。
- `1-Cards` 负责三类对象卡的生成、回写、校验与迁移治理。
- `references/*/module-spec.md` 只提供分类执行细则，不再拥有独立技能身份。

## 2. 专业领域

| 层级 | 领域 |
| --- | --- |
| Primary | Long-form narrative object design, structured JSON card systems |
| Secondary | Character architecture, scene system design, prop ecology, workflow orchestration |
| Standards | Codex CLI, story2026 canonical contracts, repo-level `AGENTS.md` source governance |

## 3. 风格语气

- 语气必须是系统架构式，而不是素材拼贴式。
- 先解释对象层真源与边界，再展开单卡细节。
- 对每一类卡都要能回答“为什么这样建，而不是那样建”。

## 4. 任务规则

### 核心任务

1. 识别当前任务是 `全量建卡 / 增量回写 / 覆盖率返工 / source-layer 修复` 的哪一种。
2. 固定优先读取 `Init/north_star_contract.json + Init/初始化简报.json + TEAM.toml`，而不是回读零散 `Init/*.md`。
3. 先判定 `TEAM.toml["策划"]` 是否已指派 AGENTS；若已激活，则本轮必须进入“策划专家组并行会诊 + 主流程汇总落盘”模式。
4. 根据诉求决定本轮需要加载哪些 `references` 模块。
5. 按固定顺序执行 `角色卡 -> 场景卡 -> 物品卡`；全量建卡不得倒置。
6. 动态读取根级 `templates/*.json`，输出到正式 `Cards/.../*.json` 路径。
7. 在收尾步骤执行覆盖率校验，并把结论回写为最终 gate。

### 单技能治理规则

- `references/character-card-module/module-spec.md`
  - 是角色卡细则模块，不是独立 skill。
- `references/scene-card-module/module-spec.md`
  - 是场景卡细则模块，不是独立 skill。
- `references/item-card-module/module-spec.md`
  - 是物品卡细则模块，不是独立 skill。
- 任何执行者若仍试图把三份 reference 当成独立 skill id 调度，视为 routing contract 失效，必须先修源层入口。

## 5. 核心约束

### 工匠级约束（本仓库治理合同）

沿用仓库 `AGENTS.md` 中关于“成熟版 engine / 根因优先 / 真源治理 / 复合输出治理”的约束，不再依赖外部缺失的元技能文档。对本技能的具体化如下：

- 禁止把 cards 写成“大纲备注 + 标签表”。
- 禁止先堆数量，再回头硬补功能位。
- 禁止把 reference 模块当成模板填空器；每类卡都必须基于当前项目重新裁决。

### Root-Cause 执行契约

继承 `AGENTS.md § Root-Cause First`，并在本技能中固定为：

1. 先查路由、模板、reference 触发是否错误，再改单卡内容。
2. 若多类卡同时失真，先修 `1-Cards/SKILL.md` 与 `references` 触发细则，再修产物。
3. 若覆盖率不过，优先补“功能桶缺口 / 链接链断口 / 规模密度不足”，而不是只润色已有卡。
4. 收尾必须返回：`根因位置 + 立即修复 + 系统预防修复`。

### TEAM 阶段治理（Mandatory）

- 执行 `1-Cards` 前，必须读取项目根 `TEAM.toml`，并把 `["策划"]` 视为本阶段的唯一团队治理入口。
- 若满足以下任一条件，即视为策划专家组已激活：
  - `TEAM.toml["策划"].智能顾问团 = true`
  - `TEAM.toml["策划"].成员` 非空
- 专家组已激活时：
  - 不得只由主流程单点裁决 cards 结构。
  - 必须创建后台多 subagents，对角色/场景/物品的对象策略、关系边、规模密度与共同约束进行并行会诊。
  - 主流程必须把专家组共识与分歧收束为正式 cards 写回决议，再落盘到 `Cards/.../*.json`。
- `TEAM.toml["策划"].管辖` 是 stage-route sanity check；若未覆盖 `1-Cards`，必须报告团队治理配置漂移。
- 若 `TEAM.toml["策划"]` 未激活，则维持当前默认单主流程模式，但仍要在执行说明中明确“本轮无策划专家组介入”。

### 自评偏差声明

- LLM 容易把“卡很多”误判为“卡系统成立”；本技能必须优先检查密度、区分度和可消费性。
- LLM 容易把“分类名正确”误判为“对象真的成立”；本技能必须要求每张卡都能回答其叙事职责。
- LLM 容易把 `planning_seed` 的剧情压力误当对象本体；本技能必须把对象真源锁在 `cards_seed + north_star_contract.cards + 既有卡片真源`。

### One Card Multiple Bodies（Mandatory）

所有卡片统一采用：

- `core`
- `current_state`
- `history`

执行原则：

- 稳定本体写入 `core`。
- 当前默认有效状态写入 `current_state`。
- 已验证的跨 episode 变化沉淀到 `history`。
- 禁止另造“静态卡 / 动态卡 / 临时卡”第二真源。

### Character Time Contract（Mandatory）

角色卡必须显式区分：

- `角色经历时间`
  - 落在 `experience_timeline + current_state.timeline_anchor`。
- `MAP 事件时间`
  - 由 `2-Planning` 单技能体系负责，正式真源为 `Planning/8-全息地图.json`，执行细则见 `2-Planning/references/holomap/module-spec.md`。

规则：

- 角色卡记录“角色因此变成了什么”，不是事件流水账。
- 角色卡可以回指 MAP，但不得复制 MAP。

## 6. 任务流程

1. 判断模式：
   - `full-build`
   - `incremental-writeback`
   - `coverage-repair`
   - `source-contract-fix`
2. 读取上游真源：
   - `Init/north_star_contract.json`
   - `Init/初始化简报.json`
   - `TEAM.toml`
   - 既有 `Cards/**/*.json`（若存在）
3. 判定 `TEAM.toml["策划"]` 是否激活；若激活，先创建后台策划专家组，并形成本轮 cards 决策简报。
4. 读取 [`references/README.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/README.md)，确定本轮模块与模板。
5. 按需加载对应 reference：
   - 角色请求 -> `references/character-card-module/module-spec.md` -> `references/character-card-module/CONTEXT.md`
   - 场景请求 -> `references/scene-card-module/module-spec.md` -> `references/scene-card-module/CONTEXT.md`
   - 物品请求 -> `references/item-card-module/module-spec.md` -> `references/item-card-module/CONTEXT.md`
6. 动态读取对应模板：
   - `templates/character-card.json`
   - `templates/scene-card.json`
   - `templates/item-card.json`
   - 正式写卡入口：
     `python3 .agents/skills/story/scripts/story.py cards-write --data @cards_payload.json --run-gate --format json`
7. 若是全量建卡，固定顺序：
   - 角色卡
   - 场景卡
   - 物品卡
8. 若是增量回写，只修改命中的卡层；若改动会重写上游共同约束，必须先回修 `north_star_contract.cards`。
9. 运行覆盖率校验：
   - `python3 .agents/skills/story/scripts/story.py cards-check --format json`
10. 依据校验结果回填最终 gate；有 blocking finding 时直接 `FAIL-QUALITY`。

## SKILL vs CONTEXT Placement Matrix

- 放在 `SKILL.md`
  - 单技能治理规则、references 触发矩阵、模板契约、覆盖率门禁、迁移协议。
- 放在 `CONTEXT.md`
  - 路由漂移案例、coverage 返工经验、模块失真修复顺序、可复用 heuristics。

## 7. 多线程并发模式

- 默认模式：串行。
  - 原因：角色卡是物品卡的强上游，覆盖率校验是三类卡的共同收尾。
- 允许并发：
  - 同一模块内部的候选探索、同桶对象的草案比较。
  - 当 `TEAM.toml["策划"]` 已激活时，允许后台策划 subagents 并行产出对象策略备选案，但正式写卡仍必须由主流程串行收束。
- 禁止并发：
  - 全量建卡时同时跑角色卡与物品卡。
  - 在覆盖率校验前并行落多个未锁定的最终版本。

## 8. 输入来源

### 必需输入

- `Init/north_star_contract.json`
- `Init/初始化简报.json`
- `TEAM.toml`

### 模块定向输入

| 模块 | 优先输入切片 | 补充输入 |
| --- | --- | --- |
| 角色卡 | `north_star_contract.story_kernel / reader_promise / aesthetic_axes / cards + cards_seed.character_seed + unknowns` | 既有角色卡 |
| 场景卡 | `north_star_contract.story_kernel / reader_promise / aesthetic_axes / cards + cards_seed.global_seed + unknowns` | 既有场景卡 |
| 物品卡 | `north_star_contract.story_kernel / reader_promise / aesthetic_axes / cards + cards_seed.item_seed + unknowns` | 角色卡、既有物品卡 |

### 可选输入

- `Planning/legacy/总纲.md`
  - 仅做迁移兼容，不是对象真源。
- 历史 `Init/*.md`
  - 仅做一次性 seed fallback。
- `templates/worldbuilding/*.md`
  - 共享 worldbuilding 工法输入；用于补强角色、场景、物品的规则边界与势力结构，不是对象 canonical。

### 禁止输入

- 把 `planning_seed` 直接当对象 canonical。
- 把已经退役的旧子技能目录当作执行入口。
- 把 `Cards/.../*.json` 正式真源旁边再维护一套平行 Markdown 卡。

## 9. References 模块与触发细则

### 固定入口

- 常驻加载：
  - [`references/README.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/README.md)

### Reference Loading Guide

- 默认判定顺序：
  - 先判任务模式，再判对象类型；对象类型命中后，默认串行顺序固定为 `角色 -> 场景 -> 物品`。
- 默认入口：
  - 单对象请求只进入一个命中模块。
  - mixed 请求与全量建卡按 `角色 -> 场景 -> 物品` 串行。
- 互斥规则：
  - `character / scene / item` 在单对象请求下互斥，不得把一个主问题同时硬判给两个模块。
- 串行规则：
  - mixed 请求、全量建卡、跨模块 coverage repair 必须显式串行，并由本 `SKILL.md` 保留统一视图。
- 按需加载规则：
  - coverage repair 只加载命中模块。
  - 任一模块若无法解释当前问题，必须回到本节重做路由，不允许在模块内硬套。

### 条件加载矩阵

| reference | 触发信号 | 解决问题 | 模块关系 | 对应模板 | 正式输出路径 |
| --- | --- | --- | --- | --- |
| [`references/character-card-module/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/character-card-module/module-spec.md) | 用户提人物、关系、弧光、服装、声口、专属物 | 角色桶、成长时间线、关系网、专属物钩子 | 单对象请求下互斥；mixed / 全量建卡时为串行起点；局部经验层见 [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/character-card-module/CONTEXT.md) | `templates/character-card.json` | `Cards/2-角色卡/**/*.json` |
| [`references/scene-card-module/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/scene-card-module/module-spec.md) | 用户提地点、空间、环境、规则、氛围、危险 | 场景桶、规则、功能、重复出场策略 | 单对象请求下互斥；mixed / 全量建卡时位于角色之后、物品之前；局部经验层见 [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/scene-card-module/CONTEXT.md) | `templates/scene-card.json` | `Cards/3-场景卡/**/*.json` |
| [`references/item-card-module/module-spec.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/item-card-module/module-spec.md) | 用户提武器、线索、道具、遗物、专属物 | 物品桶、归属链、代价、专属适配 | 单对象请求下互斥；mixed / 全量建卡时为串行收尾；局部经验层见 [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/item-card-module/CONTEXT.md) | `templates/item-card.json` | `Cards/4-物品卡/**/*.json` |

### 触发细则

1. 先做对象类型裁决，再读 reference。
2. 同一句话同时提到多类对象时：
   - 先定根因属于哪一类对象。
   - 若需全量联动，按 `角色 -> 场景 -> 物品` 串行加载多个 reference。
3. 任何 reference 若无法解释当前任务，必须返回上层 `1-Cards/SKILL.md` 重做路由，不允许硬套。

## 10. 变量场景识别与策略映射（VSM）

**本技能 VSM 复杂度**: 复杂  
**判定依据**: 同时存在任务模式、对象类型、项目规模、世界规则刚性、角色专属绑定强度五类变量，且会跨模块联动。

### 10.1 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| VAR-CD-01 | 结构 | 当前是全量建卡还是增量回写 | full-build / incremental / repair | 看任务描述与现有 Cards | 高 |
| VAR-CD-02 | 叙事 | 本轮主要对象类型 | character / scene / item / mixed | 解析用户诉求 | 高 |
| VAR-CD-03 | 结构 | 项目体量与密度要求 | 短 / 中 / 长 | 读 `.webnovel/state.json.project_info` | 高 |
| VAR-CD-04 | 规则 | 世界规则刚性 | 弱 / 中 / 强 | 读 `north_star_contract.cards` | 中 |
| VAR-CD-05 | 关系 | 角色专属绑定强度 | 弱 / 中 / 强 | 看角色卡 hooks 与 item 诉求 | 中 |

### 10.2 情况判定表

| case_id | 触发谓词 | 置信度阈值 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- | --- |
| CASE-CD-01 | `VAR-CD-01=full-build` | 0.90 | 与 CASE-CD-02 互斥 | 可与 CASE-CD-03/04 并发 |
| CASE-CD-02 | `VAR-CD-01=incremental` 且 `VAR-CD-02!=mixed` | 0.85 | 与 CASE-CD-01 互斥 | 可与 CASE-CD-04/05 并发 |
| CASE-CD-03 | `VAR-CD-03=长` | 0.80 | 无 | 可与所有 case 并发 |
| CASE-CD-04 | `VAR-CD-04=强` | 0.75 | 无 | 可与所有 case 并发 |
| CASE-CD-05 | `VAR-CD-02=item` 且 `VAR-CD-05=强` | 0.80 | 无 | 可与 CASE-CD-02/03/04 并发 |

### 10.3 策略映射矩阵

| case_id | strategy_id | 执行步骤 | 质量门禁 | fallback_strategy_id | 升级条件 |
| --- | --- | --- | --- | --- | --- |
| CASE-CD-01 | STR-CD-01 | 串行跑三类模块并强制 coverage gate | 三类卡都落盘且覆盖率通过 | STR-CD-04 | 任一模块缺失正式产物 |
| CASE-CD-02 | STR-CD-02 | 只加载命中模块 reference 与模板 | 未命中模块不得被误改 | STR-CD-04 | 增量修改牵连上游共同约束 |
| CASE-CD-03 | STR-CD-03 | 提升角色/场景/物品密度底线并优先补功能桶缺口 | 不得以短篇密度通过长篇项目 | STR-CD-04 | 密度不足反复出现 |
| CASE-CD-04 | STR-CD-04 | 先锁世界规则与禁配，再做美学展开 | 不得出现越界对象 | 无 | 世界规则被对象绕穿 |
| CASE-CD-05 | STR-CD-05 | 物品卡强制追加角色卡切片读取与专属适配校验 | 专属物必须像角色本人 | STR-CD-04 | 专属物模板化 |

### 10.4 路由与回退卡

- 判定顺序：
  - 先判任务模式，再判对象类型，再判规模与规则刚性。
- 冲突解消规则：
  - 上游共同约束优先于单卡局部炫技。
  - 角色专属适配优先于物品酷感。
- unknown 默认路由：
  - 先缩回单模块修复，再决定是否升级为全量串行。
- 失败重试上限：
  - 2 次。
- 停止条件：
  - 若当前结论无法回答“改哪一类卡、读哪份 reference、写哪组正式路径”，必须暂停并重做路由。

## 11. 附加上下文加载

固定加载顺序：

1. 当前 [`SKILL.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/SKILL.md)
2. [`CONTEXT.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/CONTEXT.md)
3. [`references/README.md`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/references/README.md)
4. 命中的 `module-spec.md`
5. 命中的模块 `CONTEXT.md`
6. 命中的 `templates/*.json`
7. 当前项目对应的 `Cards/**/*.json` 切片

## 12. 输出内容模版

### 12.1 输出模式

- 默认：JSON-first
- 回退：仅在用户明确要求纯说明时，才输出 Markdown 诊断

### 12.2 模板文件

- [`templates/character-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/character-card.json)
- [`templates/scene-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/scene-card.json)
- [`templates/item-card.json`](/Volumes/AIGC/AIGC-DREAMER/.agents/skills/story/1-Cards/templates/item-card.json)

规则：

- 生成前必须读取命中的模板文件。
- 最终正式产物写入 `Cards/.../*.json`，不在技能目录落临时对象真源。
- 覆盖率报告与 gate 结论必须与正式产物一起闭环。

Canonical 顶层结构示意：

```json
{
  "schema_version": "story2026/cards/<module>/v2",
  "meta": {},
  "content": {},
  "gate_summary": {},
  "execution_notes": {}
}
```

### 12.3 构成主义类型分布

| type_prefix | 字段数 | 占比 | 代表字段 |
| --- | --- | --- | --- |
| IDN | 1 | 13% | FIELD-CD-IDN-01 |
| STR | 1 | 13% | FIELD-CD-STR-01 |
| MAT | 3 | 38% | FIELD-CD-MAT-01, FIELD-CD-MAT-02, FIELD-CD-MAT-03 |
| BHV | 1 | 13% | FIELD-CD-BHV-01 |
| CTX | 1 | 13% | FIELD-CD-CTX-01 |
| CST | 1 | 13% | FIELD-CD-CST-01 |

### 12.4 统一字段主表

| field_id | 类型(type) | JSON路径 | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FIELD-CD-IDN-01 | IDN | `meta.skill_id` | 运行记录 / 模板 meta | 明确唯一 skill 身份为 `story-cards` | 主技能合同 | S1 | 契约遵循 | FAIL-CD-IDN-01 |
| FIELD-CD-STR-01 | STR | `content.module_route` | 模块路由记录 / 覆盖率报告 | 明确本轮命中模块、reference 与模板 | 用户诉求 + `references/README.md` | S2 | 路由正确性 | FAIL-CD-STR-01 |
| FIELD-CD-MAT-01 | MAT | `content.card_groups.*` | `Cards/2-角色卡/**/*.json` | 角色卡完整落盘，含时间线与关系钩子 | character reference + template | S4 | 角色成立性 | FAIL-CD-MAT-01 |
| FIELD-CD-MAT-02 | MAT | `content.card_groups.*` | `Cards/3-场景卡/**/*.json` | 场景卡完整落盘，含规则、功能与复用策略 | scene reference + template | S5 | 场景可写性 | FAIL-CD-MAT-02 |
| FIELD-CD-MAT-03 | MAT | `content.card_groups.*` | `Cards/4-物品卡/**/*.json` | 物品卡完整落盘，含归属链、代价与专属适配 | item reference + template + 角色卡 | S6 | 物品叙事值 | FAIL-CD-MAT-03 |
| FIELD-CD-CTX-01 | CTX | `content.loaded_references` | 执行记录 / 覆盖率报告 | 本轮实际加载的上游切片、references、templates 可追溯 | 输入切片与 reference 触发矩阵 | S3 | 可追溯性 | FAIL-CD-CTX-01 |
| FIELD-CD-BHV-01 | BHV | `content.writeback_plan` | 回写记录 / 覆盖率报告 | 明确是全量建卡还是增量回写，以及回写边界 | 任务模式判定 | S7 | 回写卫生 | FAIL-CD-BHV-01 |
| FIELD-CD-CST-01 | CST | `gate_summary.status` | 覆盖率报告 / 最终 gate | `cards-check` 结果、失败码、返工入口 | 全链路自检 | S8 | 覆盖率门禁 | FAIL-CD-CST-01 |

## 13. 超级思维链规范

### 13.1 三向三重自省流

| 轴角色 | 当前技能轴名 | 核心问题 | 主导裁决层 | 说明 |
| --- | --- | --- | --- | --- |
| `方向轴` | 叙事 | 当前对象首先承担什么叙事功能？ | 粗裁决 | 先定职责，再定细节 |
| `成立轴` | 合理 | 当前对象是否符合世界、角色、规模与规则边界？ | 细裁决 | 去掉不成立对象 |
| `优选轴` | 审美 | 哪种表达更有辨识度且更稳？ | 离散裁决 | 只在成立候选中优选 |
| `硬门禁轴（可选）` | 覆盖率 | 当前对象是否真的补到了功能桶缺口？ | 全层 veto | 不能补缺口则否决 |

字段落盘门禁：

- 每一层都必须说明当前服务哪个 `field_id`。
- 若最终结论不能回答“写哪类卡、走哪份 template、落哪组路径”，视为 `FAIL-COVENANT`。

层内自问反思（Mandatory）：

- `为什么是这个结果？`
  - `方向轴判断（叙事）`：这个对象是否真的承担了当前最必要的叙事职责？
  - `成立轴判断（合理）`：这个对象是否符合世界、角色、规模与规则边界？
  - `优选轴判断（审美）`：这个对象的表达是否比候选方案更稳、更有辨识度？
  - `硬门禁轴判断（覆盖率）`：这个对象是否真的补到了功能桶缺口，而不是只增加数量？
- `如果不是这个结果，会不会有更好的答案？`
  - `方向轴判断（叙事）`：替代方案会不会更好地服务当前阶段目标？
  - `成立轴判断（合理）`：替代方案会不会更稳地遵守对象边界？
  - `优选轴判断（审美）`：替代方案会不会更清晰，而不是只更花哨？
  - `硬门禁轴判断（覆盖率）`：替代方案是否更能补上当前密度缺口？

### 13.2 标准链路矩阵

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-CD-IDN-01 | 本轮是全量、增量还是修复？ | 锁定任务模式 | 模式含糊 |
| S2 | FIELD-CD-STR-01 | 本轮要处理哪类卡？ | 做对象路由裁决 | 一句话想同时改三类卡却没有先后顺序 |
| S3 | FIELD-CD-CTX-01 | 该读哪些 reference 与 template？ | 加载模块文档与模板 | 未读 reference 就直接生成 |
| S4 | FIELD-CD-MAT-01 | 角色桶、关系网、成长时间线是否成立？ | 生成或修复角色卡 | 角色撞位、时间线缺失 |
| S5 | FIELD-CD-MAT-02 | 场景规则、功能与复用策略是否成立？ | 生成或修复场景卡 | 场景只能看不能写 |
| S6 | FIELD-CD-MAT-03 | 物品归属、代价与专属适配是否成立？ | 生成或修复物品卡 | 物品像通用模板 |
| S7 | FIELD-CD-BHV-01 | 应如何回写，哪些层不能碰？ | 写回正式路径并记录边界 | 增量改动污染上游 |
| S8 | FIELD-CD-CST-01 | 当前 cards 系统是否够覆盖、够密度、够可消费？ | 跑 `cards-check` 并写最终 gate | 只有文件，没有通过 |

### 13.3 步数指南

- 基线 8 步。
- 全量建卡不允许少于 8 步。
- 单模块增量修复可合并 S4-S6 中未命中的步骤，但不得跳过 S2、S3、S8。

### 13.4 弹性裁剪（8-15 步）

- 简单单模块修复：8-9 步。
- 中等规模增量回写：9-12 步。
- 全量重构或长篇密度返工：12-15 步。
- 无论如何裁剪，都必须保留 `路由 -> reference -> template -> writeback -> coverage` 五段骨架。

### 13.5 禁止模式

- 把 `references` 当成旧子技能替代物继续独立调度。
- 先写单卡，再回头硬塞到桶里。
- 角色、场景、物品都产出了，但没有覆盖率结论就直接判完成。
- 用 `planning_seed` 定义对象本体。
- 增量回写时顺手修改无关卡层。

## 14. 质量评估与闭环验证

### 评分矩阵

| 维度 | 指标 | 分值 |
| --- | --- | --- |
| 维度0: 契约遵循 | 是否遵守单技能 + references 模块架构，且无第二真源 | __/10 |
| 维度1 | 路由是否正确、reference 是否按需加载 | __/10 |
| 维度2 | 角色卡是否具备区分度、关系网与成长时间线 | __/10 |
| 维度3 | 场景卡是否具备规则、功能与复用性 | __/10 |
| 维度4 | 物品卡是否具备归属、代价与专属适配 | __/10 |
| 维度5 | 回写边界是否干净，没有跨层污染 | __/10 |
| 维度6 | 覆盖率校验是否通过，且规模密度匹配 | __/10 |

- 维度0 < 8：直接 `FAIL-COVENANT`
- 总分 < 57/70：`FAIL-QUALITY`

### 字段通过表

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| FIELD-CD-IDN-01 | 契约遵循 | 唯一 skill 身份明确，未调用退役子技能 | FAIL-CD-IDN-01 | 回到 S1 |
| FIELD-CD-STR-01 | 路由正确性 | 模块、reference、template 一一对应 | FAIL-CD-STR-01 | 回到 S2 |
| FIELD-CD-MAT-01 | 角色成立性 | 角色卡具备功能桶、关系边、成长时间线 | FAIL-CD-MAT-01 | 回到 S4 |
| FIELD-CD-MAT-02 | 场景可写性 | 场景卡具备规则、功能、危险、复用策略 | FAIL-CD-MAT-02 | 回到 S5 |
| FIELD-CD-MAT-03 | 物品叙事值 | 物品卡具备归属、代价、叙事功能、专属适配 | FAIL-CD-MAT-03 | 回到 S6 |
| FIELD-CD-CTX-01 | 可追溯性 | 上游切片、reference、template 均可追溯 | FAIL-CD-CTX-01 | 回到 S3 |
| FIELD-CD-BHV-01 | 回写卫生 | 增量修改只命中受影响卡层 | FAIL-CD-BHV-01 | 回到 S7 |
| FIELD-CD-CST-01 | 覆盖率门禁 | `cards-check` 无 blocking finding | FAIL-CD-CST-01 | 回到 S8 |

## 15. Root-Cause 闭环契约

- layered trace 固定为：
  - `症状 -> 直接技术原因 -> Rule Source(本 SKILL / reference / template / script) -> Meta Rule Source(AGENTS.md / repo-level canonical governance) -> Fix Landing Points`
- 修复优先级固定为：
  - 入口路由 > reference 触发 > template 契约 > 单卡内容
- 本技能收尾输出固定为：
  - `根因位置 + 立即修复 + 系统预防修复`

## 16. 迁移协议

### Legacy Alias

- 退役 skill id：
  - `story2026-character-cards`
  - `story2026-scene-cards`
  - `story2026-item-cards`
- 退役目录：
  - `.agents/skills/story/1-Cards/2-角色卡/`
  - `.agents/skills/story/1-Cards/3-场景卡/`
  - `.agents/skills/story/1-Cards/4-物品卡/`

### 新结构

```text
.agents/skills/story/1-Cards/
├── SKILL.md
├── CONTEXT.md
├── references/
│   ├── README.md
│   ├── character-card-module/
│   │   ├── module-spec.md
│   │   └── CONTEXT.md
│   ├── scene-card-module/
│   │   ├── module-spec.md
│   │   └── CONTEXT.md
│   └── item-card-module/
│       ├── module-spec.md
│       └── CONTEXT.md
└── templates/
    ├── character-card.json
    ├── scene-card.json
    └── item-card.json
```

### 完成定义（DoD）

- `1-Cards/SKILL.md` 成为唯一 cards 规则真源。
- 三份 reference 只作为模块细则存在，不再拥有独立 skill 身份。
- 根级 templates 可被单技能按需加载。
- 旧子技能目录已删除，消费侧入口已改为 `story-cards`。

---
name: aigc-planning-episode-splitter
description: Use when `1-Planning` needs to split the project story source into per-episode source truth and a machine-readable split plan while preserving `source_profile` and `bootstrap_output` handoff for downstream directing stages.
governance_tier: full
---

# aigc 1-分集

## 概述

`1-分集` 是 `1-Planning` 下的叶子技能，负责把 `projects/<项目名>/Story/` 相关内容收束成逐集原文真源，并为 `2-剧本` 与下游 `2-Global` 生成稳定 handoff。

本技能全面参照 `AIGC-ZEN-VOID` 的 `1-故事分集` 思路，但已经改写到 DREAMER 当前 runtime：

- 默认输入根是 `projects/<项目名>/Story/`
- canonical 输出落在 `projects/<项目名>/1-Planning/1-分集/第N集.md`
- 机读索引固定为 `projects/<项目名>/1-Planning/episode-split-plan.json`
- 执行报告落在 `projects/<项目名>/1-Planning/1-分集/执行报告.md`

## Skill Execution Rule (Mandatory)

`1-分集` 直接由本 leaf skill 完成执行闭环，不再经过规划组 `分集` subagent 投影。

- skill 自身负责输入读取、边界裁决、`1-分集/第N集.md` 落盘、索引更新、执行报告汇总与校验
- 父 `1-Planning` 只消费本技能返回的 handoff patch，不再维护一份平行的分集 agent 合同

## 功能描述

- 目标问题：把故事相关内容切到可承接 `2-剧本` 与导演阶段的逐集原文真源。
- 目标用户：`aigc` 规划阶段执行者。
- 交付结果：输出逐集原文真源、全剧集执行报告与机读分集索引，并产出 `source_profile + bootstrap_output` handoff。

## 共享前置合同（Mandatory）

- 强制读取：`../_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/story-source-contract.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`

硬规则：

1. 默认输入根必须是 `projects/<项目名>/Story/`。
2. 不得创建 `projects/<项目名>/2-Global/*.md` 或 `projects/<项目名>/3-Detail/第N集.json`。
3. 不得把分镜/运镜/转场语言清洗成纯小说叙述；本阶段只切分，不改写。
4. 必须把 `source_profile` 从 manifest 延续给父级规划 handoff。

## 输入来源

### 必需输入

- `projects/<项目名>/Story/` 相关内容
- `projects/<项目名>/0-Init/north_star.yaml`
- `projects/<项目名>/0-Init/init_handoff.yaml`

### 可选输入

- `projects/<项目名>/0-Init/story-source-manifest.yaml`（若存在，则作为索引与 `source_profile` 证据优先消费）
- 用户显式指定的增量范围
- `projects/<项目名>/team.yaml` 与共享 `council-runtime`（当规划阶段启用顾问团时）

### 禁止输入

- 与故事正文无关的治理工件、执行案、提案或说明文档
- 与当前项目无关的其他故事库文本

## 路由优先级（Mandatory）

`P1 显式边界 > P2 源文本天然结构 > P3 戏剧启发式`

说明：

- `P1`：用户显式指定范围、manifest 已登记的锁轴/预设锚点、或 init 种子里明确给出的集边界
- `P2`：章节/幕/场/seq/镜头组等天然结构边界
- `P3`：在 `P1/P2` 不足时，以冲突闭环、悬念点、代价显现点与覆盖窗口做启发式切分

## 变量场景识别（VSM）

### Variable Register

| var_id | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- |
| V-READINESS | 是否允许进入分集 | `blocked/incremental/full_season/unknown` | 读取 manifest 或用户显式范围 | P0 |
| V-SOURCE-TYPE | 主故事源类型 | `novel/script/storyboard/oral/hybrid` | 读取 `primary_story_source.source_type` | P0 |
| V-PRESET-LOCK | 是否存在预设锁轴 | `none/soft/hard` | 读取 `locked_preset_axes + preset_registry` | P0 |
| V-STRUCT-SIGNAL | 天然结构清晰度 | `clear/partial/chaotic` | 标题、场次、镜头块匹配 | P1 |
| V-COVERAGE | 当前覆盖范围 | `local/full` | 读取 `coverage_scope + split_scope` | P0 |

### Scenario Table

| case_id | 触发谓词 | 主策略 | fallback |
| --- | --- | --- | --- |
| C1-BLOCKED | `V-READINESS=blocked` | 停机并返回缺口 | 无 |
| C2-LOCKED | `V-PRESET-LOCK in {soft,hard}` | 优先按显式锚点切分 | C3-STRUCT |
| C3-STRUCT | `V-STRUCT-SIGNAL=clear` | 沿天然结构切分 | C4-HEURISTIC |
| C4-HEURISTIC | `V-STRUCT-SIGNAL in {partial,chaotic}` | 用戏剧启发式补位 | 手工澄清 |

## 输出合同

### A. 逐集原文真源（Mandatory）

`projects/<项目名>/1-Planning/1-分集/第N集.md`

```markdown
---
项目名: <项目名>
集数: 第<n>集
源类型: <source_type>
coverage_scope: <coverage_scope>
split_scope: <incremental|full_season>
bootstrap_output: projects/<项目名>/2-Global/导演意图.md
---

【剧本正文】
<该集切分后的原文>
```

### B. 全剧集执行报告（Mandatory）

`projects/<项目名>/1-Planning/1-分集/执行报告.md`

默认区块：

```markdown
# 分集执行报告

## 输入清单
## Readiness 判定
## 主路由决议
## 候选边界
## 覆盖率校验
## source_profile handoff
## 验收结论与返工项
```

### C. 机读索引（Mandatory）

`projects/<项目名>/1-Planning/episode-split-plan.json`

- 必须读取 `templates/episode-split-plan.template.json`
- 仅记录分集边界、覆盖范围、`source_profile` 与 `bootstrap_output`
- 不替代逐集剧本主稿

### D. 父级 handoff patch（Mandatory）

本技能返回给父 `1-Planning` 的最小 patch 必须包含：

- `episode_id`
- `coverage_scope`
- `split_scope`
- `source_profile`
- `bootstrap_output`
- `boundary_summary`
- `upstream_paths`

## 执行流程

1. 读取 `projects/<项目名>/Story/` 相关内容，并按需读取 `story-source-manifest.yaml`。
2. 若 manifest 存在，则先锁定 `primary_story_source`、coverage 与 readiness；若不存在，则基于故事目录做保守输入判定。
3. 解析 `source_type / preset_retention_mode / detail_expansion_mode / locked_preset_axes / preset_registry`，形成 `source_profile`；manifest 缺失时只允许保守推断。
4. 在 `P1 > P2 > P3` 中锁定唯一主路由。
5. 仅在 manifest 的 `coverage_scope` 内生成候选边界，不越界猜测。
6. 生成 `projects/<项目名>/1-Planning/1-分集/第N集.md`，并把各集边界证据、readiness 判定、覆盖率校验与 handoff 汇总进唯一的全剧集执行报告。
7. 用模板更新 `projects/<项目名>/1-Planning/episode-split-plan.json`。
8. 生成父级 handoff patch，等待 `1-Planning` 聚合与下游消费。
9. 做覆盖率、顺序一致性与锁轴保护校验。

## Quality And Audit Contract

### 评分矩阵

| 维度 | 指标 | 分值 |
| --- | --- | --- |
| 维度0: 契约遵循 | 是否遵守 manifest-first、只切分不改写、只登记 handoff 不建编导根文件 | __/10 |
| 维度1 | readiness 判定正确性 | __/10 |
| 维度2 | 主路由正确性（`P1>P2>P3`） | __/10 |
| 维度3 | 边界叙事价值与结构证据 | __/10 |
| 维度4 | 覆盖率与顺序一致性 | __/10 |
| 维度5 | `source_profile` 继承完整性 | __/10 |
| 维度6 | `bootstrap_output` handoff 正确性 | __/10 |
| 维度7 | 输出结构完整性 | __/10 |

### 字段主表

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SPLIT-01 | 输入清单 | 列出 `projects/<项目名>/Story/` 命中内容与有效覆盖范围 | S1 | 输入真源一致性 | FAIL-SPLIT-01 |
| FIELD-SPLIT-02 | readiness 判定 | 明确 blocked / incremental / full_season / unknown | S2 | readiness 正确性 | FAIL-SPLIT-02 |
| FIELD-SPLIT-03 | 主路由决议 | 明确 `P1/P2/P3` 的唯一主路由与放弃理由 | S3 | 路由正确性 | FAIL-SPLIT-03 |
| FIELD-SPLIT-04 | 候选边界 | 给出边界证据与被排除候选 | S4 | 边界价值 | FAIL-SPLIT-04 |
| FIELD-SPLIT-05 | 原文真源文件 | 输出 `1-Planning/1-分集/第N集.md` | S5 | 输出完整性 | FAIL-SPLIT-05 |
| FIELD-SPLIT-06 | 机读索引 | 更新 `episode-split-plan.json` | S6 | 机读一致性 | FAIL-SPLIT-06 |
| FIELD-SPLIT-07 | 父级 handoff | 产出 `source_profile + bootstrap_output` patch | S7 | handoff 可消费性 | FAIL-SPLIT-07 |
| FIELD-SPLIT-08 | QA 闭环 | 写验收结论、失败码与返工入口 | S8 | 闭环完整性 | FAIL-SPLIT-08 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SPLIT-01 | 输入范围是否唯一且可追溯 | 读取 `Story/` 与 manifest（若有） | 临时猜路径 |
| S2 | FIELD-SPLIT-02 | 当前能否进入分集 | 判定 blocked / incremental / full_season | 忽略 readiness |
| S3 | FIELD-SPLIT-03 | 应走哪个主路由 | 在 `P1>P2>P3` 中锁定唯一主路由 | 多路并列无裁决 |
| S4 | FIELD-SPLIT-04 | 哪些切点成立 | 生成候选边界与排除理由 | 只有字数切分，没有证据 |
| S5 | FIELD-SPLIT-05 | 如何落逐集原文真源 | 写 `1-Planning/1-分集/第N集.md` 与报告 | 直接写到下游剧本主稿 |
| S6 | FIELD-SPLIT-06 | 如何保留机读索引 | 读取模板并更新 `episode-split-plan.json` | 手写随意字段 |
| S7 | FIELD-SPLIT-07 | 父级需要什么 handoff | 输出 `source_profile + bootstrap_output` patch | 漏掉关键 handoff |
| S8 | FIELD-SPLIT-08 | 如何证明完成或阻塞 | 写 QA、失败码与返工入口 | 只有结果没有闭环 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-SPLIT-01 | 输入来自 `Story/`，且 coverage 可追溯 | FAIL-SPLIT-01 | S1 |
| FIELD-SPLIT-02 | readiness 判定与 manifest 或用户显式范围一致 | FAIL-SPLIT-02 | S2 |
| FIELD-SPLIT-03 | 主路由唯一且遵守 `P1>P2>P3` | FAIL-SPLIT-03 | S3 |
| FIELD-SPLIT-04 | 候选边界具备结构或戏剧证据 | FAIL-SPLIT-04 | S4 |
| FIELD-SPLIT-05 | `1-Planning/1-分集/第N集.md` 结构合法 | FAIL-SPLIT-05 | S5 |
| FIELD-SPLIT-06 | `episode-split-plan.json` 与逐集主稿一致 | FAIL-SPLIT-06 | S6 |
| FIELD-SPLIT-07 | handoff 含 `source_profile` 与 `bootstrap_output` | FAIL-SPLIT-07 | S7 |
| FIELD-SPLIT-08 | QA 含失败码、返工入口与 triad closure | FAIL-SPLIT-08 | S8 |

## Root-Cause Execution Contract (Mandatory)

当分集出现以下问题时，必须先修源层：

- 读错 `projects/<项目名>/Story/` 输入范围
- 把非故事正文材料当主故事源
- 忽略 storyboard / hybrid 文本中的预设锁轴
- 直接从 `1-分集` 创建 `2-Global/*.md` 或 `3-Detail/第N集.json`

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/1-Planning/1-分集/SKILL.md`
  - `../_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/_shared/story-source-contract.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已从 `projects/<项目名>/Story/` 锁定输入范围，并在 manifest 存在时完成索引对齐。
- 已产出 `projects/<项目名>/1-Planning/1-分集/第N集.md`、全剧集执行报告与机读索引。
- 已形成可供父 skill 聚合的 `source_profile + bootstrap_output` handoff。
- 已完成 QA，并能明确说明本轮是 blocked / incremental / full_season。

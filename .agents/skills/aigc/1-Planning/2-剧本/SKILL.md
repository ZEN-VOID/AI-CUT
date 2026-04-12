---
name: aigc-planning-script
description: Use when `1-Planning` needs to transform `1-分集` episode source truth into a canonical per-episode planning script, routing inside one skill package through `标准剧 / 解说剧` subagents instead of splitting them into local child skill packages.
governance_tier: full
---

# aigc 2-剧本

## 概述

`2-剧本` 是 `1-Planning` 下的单一技能包，用来把 `1-分集` 产出的逐集原文真源整理成可供 `3-分组`、`2-Global` 和人工审阅继续消费的逐集剧本主稿。

它全面参照 `AIGC-ZEN-VOID/.agents/skills/aigc2026/1-编剧/2-对白·独白·旁白` 的核心合同，但在当前仓库里做了两项关键改写：

1. 不再把 `标准剧 / 解说剧` 落成本地两个子技能包，而是统一收敛进一个 `2-剧本` 技能包。
2. 变体只通过 `.codex/agents/aigc/规划组/标准剧.md` 与 `.codex/agents/aigc/规划组/解说剧.md` 两个 subagents 触发。

## Skill / Subagent Execution Rule (Mandatory)

在 `2-剧本` 中，分工固定为：

- subagents 负责思考、`agents plan`、文本层判断与 patch / note
- skill 本身负责总路由、上下文装配、真正写回 `2-剧本/第N集.md`、运行 validator、生成执行报告与返回父级 handoff

`标准剧 / 解说剧` 可以决定“怎么整理”，但不能代替 `2-剧本` skill 完成真正执行。

## 功能描述

- 目标问题：将 `1-分集` 保留的逐集原文，整理为规划阶段 canonical 的逐集剧本主稿。
- 目标用户：`1-Planning` 执行者、规划组 `格式判模 / 标准剧 / 解说剧` subagents。
- 交付结果：输出 `projects/<项目名>/1-Planning/2-剧本/第N集.md`、单集执行报告，并回传供父级登记的 `patch / note / report`。

## Canonical Anchors

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| 剧本主稿 | `projects/<项目名>/1-Planning/2-剧本/第N集.md` | 当前规划阶段逐集 canonical 主稿 |
| 单集执行报告 | `projects/<项目名>/1-Planning/2-剧本/第N集-执行报告.md` | 记录变体裁决、校验结果与返工入口 |
| 阶段变更记录 | `projects/<项目名>/1-Planning/2-剧本/CHANGELOG.md` | 记录结构性迁移与合同更新 |
| 上游逐集真源 | `projects/<项目名>/1-Planning/1-分集/第N集.md` | `1-分集` 产出的逐集原文真源 |
| 上游分集报告 | `projects/<项目名>/1-Planning/1-分集/执行报告.md` | 分集边界、coverage 与 `source_profile` 证据 |
| 上游机读索引 | `projects/<项目名>/1-Planning/episode-split-plan.json` | 分集边界、`source_profile` 与 `bootstrap_output` 索引 |
| 共享校验器 | `.agents/skills/aigc/1-Planning/2-剧本/scripts/validate_script_output.py` | 校验 `标准剧 / 解说剧` 两种结构输出 |

## Single-Package Subagent Contract (Mandatory)

本技能禁止再拆出本地 `标准剧/`、`解说剧/` 子技能目录。

变体只通过现有规划组 subagents 路由：

- 默认裁决入口：`.codex/agents/aigc/规划组/格式判模.md`
- 标准剧 subagent：`.codex/agents/aigc/规划组/标准剧.md`
- 解说剧 subagent：`.codex/agents/aigc/规划组/解说剧.md`

### 触发规则

1. 用户显式要求“解说剧 / 旁白主导 / 非对白旁白化”时，进入 `解说剧`。
2. 用户显式要求“标准剧 / 表演优先 / 旁白节制”时，进入 `标准剧`。
3. 用户未显式指定时，读取 `格式判模` 的主变体结论。
4. 若 `格式判模` 无唯一结论，默认回退 `标准剧`，并在执行报告中写明原因。
5. 只有用户显式要求双案对照时，才允许同一轮并行调用 `标准剧 + 解说剧`。

### 边界

- `2-剧本` 技能包拥有：
  - 变体 subagent 路由
  - `projects/<项目名>/1-Planning/2-剧本/第N集.md` 的写回
  - 统一 validator 调用
  - 返回父级可登记的 `patch / note / report`
- `标准剧 / 解说剧` subagents 只拥有：
  - 结构骨架判断
  - 变体 `agents plan`
  - 文本层策略 patch
  - 变体风险 note
- `标准剧 / 解说剧` subagents 不拥有：
  - canonical 文件最终写回
  - 第二份剧本主稿
  - 绕过 `2-剧本` 父技能直接落盘

## 共享前置合同（Mandatory）

- 强制读取：`../_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/story-source-contract.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`

硬规则：

1. 输入真源必须来自 `1-分集` 的输出物，而不是重新回退到 `Story/` 根目录做第二次自由切分。
2. 本技能是 `1-Planning` 内部的剧本整形层，不得提前创建 `2-Global/*.md` 或 `3-Detail/第N集.json`。
3. `标准剧 / 解说剧` 只是变体 subagents，不是本地 sibling 真源。
4. 当前 skill package 写回的 `2-剧本/第N集.md` 是规划阶段 canonical 主稿，其他文件只能是 sidecar 或证据载体。

## 输入来源

### 必需输入

- `projects/<项目名>/1-Planning/1-分集/第N集.md`
- `projects/<项目名>/1-Planning/1-分集/执行报告.md`
- `projects/<项目名>/1-Planning/episode-split-plan.json`

### 可选输入

- `projects/<项目名>/0-Init/story-source-manifest.yaml`
- 用户显式指定的变体、受众、旁白密度或对白保真要求
- 父级已有的阶段 `validation-report.md`

### 禁止输入

- 当前项目外部剧本文本
- 直接来自 `2-Global / 3-Detail` 的导演扩写结果
- 未登记的临时对白整理稿

## 输出合同

### A. Canonical 剧本主稿（Mandatory）

`projects/<项目名>/1-Planning/2-剧本/第N集.md`

```markdown
---
项目名: <项目名>
集数: 第<n>集
剧本变体: <标准剧|解说剧>
source_type: <source_type>
coverage_scope: <coverage_scope>
split_scope: <incremental|full_season>
总字数: <当前正文实算值>
bootstrap_output: projects/<项目名>/2-Global/导演意图.md
upstream_source: projects/<项目名>/1-Planning/1-分集/第<n>集.md
---

【剧本正文】
<按场景组织的剧本文本>
```

### B. 单集执行报告（Mandatory）

`projects/<项目名>/1-Planning/2-剧本/第N集-执行报告.md`

默认区块：

```markdown
# 2-剧本执行报告

## 输入清单
## 变体裁决
## 结构重排摘要
## 校验结果
## 父级 handoff
## 验收结论与返工项
```

### C. 父级 handoff patch（Mandatory）

返回给父 `1-Planning` 的最小 patch 必须包含：

- `episode_id`
- `selected_variant`
- `script_output_path`
- `scene_count`
- `dialogue_policy`
- `narration_policy`
- `source_profile`
- `bootstrap_output`
- `upstream_paths`

### D. Subagent Agents Plan（Optional Evidence）

`projects/<项目名>/1-Planning/2-剧本/agents-plan/第N集.<standard|explainer>.md`

- 仅在需要保留变体规划证据时生成
- 记录主变体裁决、字段骨架、文本整理边界与放弃路径
- 不替代 `2-剧本/第N集.md`、`第N集-执行报告.md` 或父级 handoff patch

## Execution Workflow

1. 读取 `1-分集` 逐集原文、执行报告和 `episode-split-plan.json`。
2. 根据用户显式要求或 `格式判模` 结果锁定唯一主变体。
3. 调度命中的 `标准剧` 或 `解说剧` subagent，收集 `patch / note`。
4. 由本技能统一将 subagent 结果写回 `第N集.md` 与 `第N集-执行报告.md`。
5. 调用共享 validator：
   - `standard` -> `python3 scripts/validate_script_output.py --input <输出文件> --variant standard --upstream <上游文件>`
   - `explainer` -> `python3 scripts/validate_script_output.py --input <输出文件> --variant explainer --upstream <上游文件>`
6. 生成父级 handoff patch，供 `1-Planning` 阶段登记验收与下游 handoff。
7. 若 validator 失败，先返工本技能输出，再返回父级，不得把失败结果包装为完成。

## Quality And Audit Contract

### 评分矩阵

| 维度 | 指标 | 分值 |
| --- | --- | --- |
| 维度0: 契约遵循 | 是否遵守“单技能包 + subagent 变体”而非本地子技能拆分 | __/10 |
| 维度1 | 上游输入继承正确性 | __/10 |
| 维度2 | 变体裁决正确性 | __/10 |
| 维度3 | 场景结构完整性 | __/10 |
| 维度4 | 对白/旁白/独白格式合法性 | __/10 |
| 维度5 | 文本-画面同命题配对 | __/10 |
| 维度6 | `source_profile + bootstrap_output` handoff 完整性 | __/10 |
| 维度7 | 验收与返工闭环 | __/10 |

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-SCRIPT-01 | 输入锚点 | 锁定 `1-分集` 逐集原文、执行报告与机读索引 | S1 | 输入真源一致性 | FAIL-SCRIPT-01 |
| FIELD-SCRIPT-02 | 变体裁决 | 锁定 `标准剧 / 解说剧` 唯一主变体与理由 | S2 | 路由正确性 | FAIL-SCRIPT-02 |
| FIELD-SCRIPT-03 | 主稿落盘 | 写出 `2-剧本/第N集.md` | S3 | 输出完整性 | FAIL-SCRIPT-03 |
| FIELD-SCRIPT-04 | 结构校验 | 通过统一 validator 检查场景、主体、引号与配对 | S4 | 结构稳定性 | FAIL-SCRIPT-04 |
| FIELD-SCRIPT-05 | 父级 handoff | 返回 `selected_variant + source_profile + bootstrap_output` patch | S5 | handoff 可消费性 | FAIL-SCRIPT-05 |
| FIELD-SCRIPT-06 | 单包边界 | 不把变体 subagent 升成第二套本地真源 | S6 | 治理边界清晰度 | FAIL-SCRIPT-06 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-SCRIPT-01 | 上游输入是否唯一 | 读取 `1-分集` 输出物 | 重新回退到 `Story/` 自由切分 |
| S2 | FIELD-SCRIPT-02 | 本轮该走哪个变体 | 锁定单一主变体与理由 | 双案并列无裁决 |
| S3 | FIELD-SCRIPT-03 | canonical 主稿如何落盘 | 写单集 Markdown 与执行报告 | 只返 note 不写文件 |
| S4 | FIELD-SCRIPT-04 | 输出是否结构合法 | 调 validator 并修复失败项 | 只靠肉眼回放 |
| S5 | FIELD-SCRIPT-05 | 父级需要哪些 handoff | 回传 patch / note / report | 漏掉 `bootstrap_output` |
| S6 | FIELD-SCRIPT-06 | 是否重新长出子技能真源 | 固化“单包 + subagent 变体” | 本地再建 `标准剧/解说剧/SKILL.md` |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-SCRIPT-01 | 输入只来自 `1-分集` 输出物 | FAIL-SCRIPT-01 | S1 |
| FIELD-SCRIPT-02 | 主变体唯一且可追溯 | FAIL-SCRIPT-02 | S2 |
| FIELD-SCRIPT-03 | `第N集.md` 与执行报告都已落盘 | FAIL-SCRIPT-03 | S3 |
| FIELD-SCRIPT-04 | validator 通过或失败项已明确返工 | FAIL-SCRIPT-04 | S4 |
| FIELD-SCRIPT-05 | handoff 含 `selected_variant / source_profile / bootstrap_output` | FAIL-SCRIPT-05 | S5 |
| FIELD-SCRIPT-06 | 本地不存在第二套变体技能真源 | FAIL-SCRIPT-06 | S6 |

## Root-Cause Execution Contract (Mandatory)

当 `2-剧本` 出现以下问题时，必须先修源层：

- 把 `标准剧 / 解说剧` 再拆成两个本地子技能包
- 绕过 `1-分集` 输出物直接重做自由切分
- 让 subagent 直接写 canonical 文件
- 缺少统一 validator，导致格式性失误只能靠人工兜底

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/1-Planning/2-剧本/SKILL.md`
  - `../_shared/IO_CONTRACT.md`
  - `.codex/agents/aigc/规划组/格式判模.md`
  - `.codex/agents/aigc/规划组/标准剧.md`
  - `.codex/agents/aigc/规划组/解说剧.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/1-Planning/SKILL.md`
  - `.agents/skills/aigc/_shared/project-runtime-layout.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `2-剧本` 单技能包合同。
- 已明确 `标准剧 / 解说剧` 只作为 subagents 路由，不再是本地子技能包。
- 已能从 `1-分集` 输出物生成 `2-剧本/第N集.md` 与执行报告。
- 已具备统一 validator 与父级 handoff 闭环。

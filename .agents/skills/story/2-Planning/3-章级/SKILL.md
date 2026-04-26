---
name: story-plan-chapter-level
description: Use when `2-Planning` needs the micro chapter plan that locks one chapter's summary, conflict, rhythm handoff, participants, scenes, props, mission lines, clues, foreshadows, completion state, and avoidances.
governance_tier: full
metadata:
  short-description: Chapter-level story planning
---

# 2-Planning / 3-章级

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `SKILL.md` 只保留入口、Input Contract、动态引用、关键门禁、Root-Cause 合同和 Output Contract；章级长细则进入分区文件。
- 进入本技能前必须回读父层 `../SKILL.md`、`../CONTEXT.md`、`../_shared/fractal-planning-layout-contract.md`、`../_shared/fractal-planning-output-contract.md`、`../_shared/rhythm-design-field-matrix.md`、`../../_shared/core-constraints.md`、`../../_shared/character-planning-bridge.md`、`../../_shared/chapter-rhythm-handoff-contract.md`。
- 进入任何章级落盘前必须回读对应项目的 `2-Planning/整体规划.md` 与 `2-Planning/第N卷/卷规划.md`；若只是补写某一章的局部规划，也不得跳过上游完整回读。
- 若当前任务绑定 `projects/story/<项目名>/`，还必须先加载项目根 `MEMORY.md`，再加载项目根 `CONTEXT/` 中与本章相关的上下文文件。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > 父层 `2-Planning/SKILL.md` > 本 `SKILL.md` > `references/` / `steps/` / `review/` / `types/` / `templates/` > 项目级 `MEMORY.md` > 项目级 `CONTEXT/` > 本 `CONTEXT.md`。

## Input Contract

- Accepted input: 生成、补写、修订或审查 `projects/story/<项目名>/2-Planning/第N卷/第N章.md` 的章级规划任务。
- Required input: 项目根、目标卷号与章号、已确认的 `2-Planning/整体规划.md`、目标卷 `2-Planning/第N卷/卷规划.md`，以及可用的 `1-Cards` 真源。
- Optional input: 已存在的目标章规划、用户给出的章节口味、局部修订要求、需要保留或规避的角色/场景/道具/任务线。
- Reject or clarify when: 缺少 `整体规划.md`、缺少目标卷 `卷规划.md`、无法确认目标卷章编号、用户要求直接写正文、用户要求跳过上游回读后落盘，或请求把建议写法写成不可改的正文段落。

## Overview

本 child skill 负责把卷级规划下钻为单章执行蓝图，但仍停留在 planning 层。它锁定章标题、故事概要、冲突、章级节奏 handoff、登场人物、主要场景、关键道具、任务线、线索、伏笔、章末达成与规避；它不越权改写卷级职责，也不直接产出正文。

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 章级业务边界、必填标题、硬规则与 canonical sources | `references/chapter-planning-contract.md` |
| 章级节奏落盘细则与 shared handoff 回指 | `references/chapter-rhythm-rules.md` |
| 思维与执行步骤、分支、证据门和失败回路 | `steps/chapter-planning-workflow.md` |
| 章级字段、类型画像与多模式处理 | `types/chapter-planning-type-map.md` |
| 质量审计、review verdict 和 reviewer/provider 接入 | `review/chapter-planning-review.md` |
| 可复用经验与稳定 heuristic 索引 | `knowledge-base/chapter-planning-heuristics.md` |
| 输出内容模板与 Output Contract 对齐 | `templates/output-template.md`、`templates/chapter-planning.template.md` |
| 机械辅助脚本边界 | `scripts/README.md` |
| agent / product-specific 元信息 | `agents/openai.yaml` |

## Visual Maps

```mermaid
flowchart TD
    A["触发章级规划"] --> B["加载 SKILL.md + CONTEXT.md"]
    B --> C["回读整体规划.md 与目标卷规划.md"]
    C --> D{"任务模式"}
    D -->|"create"| E["新建第N章.md"]
    D -->|"revise"| F["增量修订既有章规划"]
    D -->|"review"| G["只做章级审计"]
    E --> H["执行 steps 章级网络"]
    F --> H
    H --> I["应用 chapter template"]
    I --> J["review gate"]
    G --> J
    J --> K{"通过?"}
    K -->|"Yes"| L["交付章级规划"]
    K -->|"No"| M["回到失败 owner 修正"]
    M --> H
```

```mermaid
flowchart LR
    A["references/章级细则"] --> E["第N章.md"]
    B["steps/执行网络"] --> E
    C["types/字段画像"] --> E
    D["templates/输出模板"] --> E
    E --> F["review/质量门禁"]
    F --> G["drafting 可消费 handoff"]
```

## Mode Selection

| mode | trigger | action |
| --- | --- | --- |
| `create` | 目标章级规划不存在，且上游 `整体规划.md` 与 `卷规划.md` 齐全 | 按 `steps/chapter-planning-workflow.md` 生成完整章级规划 |
| `revise` | 目标章级规划已存在，用户要求补写、修订或对齐 | 先回读上游与旧章规划，再输出局部 patch 或重写相关 section |
| `review` | 用户要求检查章级规划是否可供 drafting 消费 | 只执行 `review/chapter-planning-review.md`，不改业务真源，除非用户明确要求修复 |

## Execution Contract

1. 按 Input Contract 锁定项目根、卷号、章号、上游文档与可用卡片真源。
2. 形成 `type_profile`：默认 `domain_type=story`、`artifact_type=markdown`、`execution_type=llm-authored`、`topology_type=hybrid`、`review_type=checklist+provider-optional`、`output_type=chapter-plan`。
3. 加载 `references/chapter-planning-contract.md` 与 `references/chapter-rhythm-rules.md`，确认章级硬规则与 shared rhythm handoff。
4. 按 `steps/chapter-planning-workflow.md` 执行回读、概要、冲突、节奏、资源、任务线、线索/伏笔、章末达成与规避节点。
5. 使用 `templates/chapter-planning.template.md` 渲染章级规划结构；若是局部修订，只更新命中的 section，不补未执行子任务的占位推理。
6. 交付前执行 `review/chapter-planning-review.md` 的质量门禁，确认必填标题、节奏 handoff、任务汇聚、线索/伏笔分离和非正文化边界。
7. 若失败，按 Root-Cause Execution Contract 回到对应 owner 修正。

## Root-Cause Execution Contract

固定追溯链路：

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> Meta Rule Source`

| symptom | direct owner | rework target |
| --- | --- | --- |
| 缺上游仍落盘 | `SKILL.md` 输入门 | `Input Contract` 与 `steps/N1-UPSTREAM-REREAD` |
| 章级只有梗概没有节奏 handoff | `references/` + `steps/` | `references/chapter-rhythm-rules.md` 与 `steps/N4-CHAPTER-RHYTHM` |
| 任务线没有汇聚动作或未汇聚去向 | `references/` + `templates/` | `references/chapter-planning-contract.md` 与 `templates/chapter-planning.template.md` |
| 线索与伏笔混写 | `review/` + `templates/` | `review/chapter-planning-review.md` 与模板信息层槽位 |
| 输出中出现正文句段、对白或桥段 | `review/` | 非正文化门禁与 `references/Chapter-Specific Rule` |
| 模板与 Output Contract 不一致 | `templates/` | `templates/output-template.md` 与 `templates/chapter-planning.template.md` |

## Field Mapping

### Directory Ownership Table

| field_id | owner | requirement | fail_code |
| --- | --- | --- | --- |
| `FIELD-CH-01` | `SKILL.md` | 输入边界、模式选择、动态引用、Output Contract | `FAIL-CH-ENTRY` |
| `FIELD-CH-02` | `references/` | 章级硬规则、节奏落盘细则、shared contract 回指 | `FAIL-CH-REFERENCE` |
| `FIELD-CH-03` | `steps/` | 回读、生成、修订、审查的思行节点网络 | `FAIL-CH-STEPS` |
| `FIELD-CH-04` | `types/` | 章级字段画像、模式变量与下游消费映射 | `FAIL-CH-TYPES` |
| `FIELD-CH-05` | `templates/` | `第N章.md` 输出模板与 Output Contract Alignment | `FAIL-CH-TEMPLATE` |
| `FIELD-CH-06` | `review/` | 章级质量门禁、findings 与 verdict | `FAIL-CH-REVIEW` |
| `FIELD-CH-07` | `CONTEXT.md` / `knowledge-base/` | 经验型 Type Map、Repair Playbook 与 heuristic | `FAIL-CH-CONTEXT` |
| `FIELD-CH-08` | `scripts/` / `agents/` | 机械辅助说明与产品入口元信息 | `FAIL-CH-METADATA` |

### Node Handoff Table

| node_id | input | action | output | next_gate |
| --- | --- | --- | --- | --- |
| `N1-UPSTREAM-REREAD` | 项目根、卷号、章号、整体规划、卷规划 | 回读并锁定本章上承职责 | `upstream_profile` | `N2-CHAPTER-SPINE` |
| `N2-CHAPTER-SPINE` | `upstream_profile` | 锁章标题、概要、章末方向 | `chapter_spine` | `N3-CHAPTER-CONFLICT` |
| `N3-CHAPTER-CONFLICT` | `chapter_spine` | 锁表层冲突、深层冲突、状态变化 | `conflict_profile` | `N4-CHAPTER-RHYTHM` |
| `N4-CHAPTER-RHYTHM` | `chapter_spine` + `conflict_profile` | 锁 pack/mode、七步职责、规划义务、义务段位、建议写法与 Mermaid 图 | `rhythm_handoff` | `N5-CHAPTER-ELEMENTS` |
| `N5-CHAPTER-ELEMENTS` | `rhythm_handoff` + 上游任务线 | 收束人物、场景、道具、任务线与汇聚去向 | `chapter_resources` | `N6-INFO-LAYER` |
| `N6-INFO-LAYER` | `chapter_resources` | 分离线索、伏笔铺设与兑现 | `info_layer` | `N7-CLOSE` |
| `N7-CLOSE` | 全部 section | 锁章末达成、规避、模板落盘与 review gate | `chapter_plan` | done |

### Failure Routing Table

| fail_code | symptom | rework_target |
| --- | --- | --- |
| `FAIL-CH-ENTRY` | 输入边界不清、缺上游仍执行、模式不明 | `SKILL.md` |
| `FAIL-CH-REFERENCE` | 章级规则与 shared rhythm contract 冲突 | `references/chapter-planning-contract.md` 或 `references/chapter-rhythm-rules.md` |
| `FAIL-CH-STEPS` | 节点没有证据门、缺汇流或失败回路 | `steps/chapter-planning-workflow.md` |
| `FAIL-CH-TYPES` | 章级字段、任务模式或 review 类型散落 | `types/chapter-planning-type-map.md` |
| `FAIL-CH-TEMPLATE` | 输出模板缺标题或与 Output Contract 冲突 | `templates/output-template.md` |
| `FAIL-CH-REVIEW` | 审查门禁无法判断是否可供 drafting 消费 | `review/chapter-planning-review.md` |
| `FAIL-CH-CONTEXT` | `CONTEXT.md` 变成过程日志或缺知识库三件套 | `CONTEXT.md` |
| `FAIL-CH-METADATA` | 缺 `agents/openai.yaml`、脚本边界或默认提示 | `agents/openai.yaml` / `scripts/README.md` |

## Output Contract

- Required output: `projects/story/<项目名>/2-Planning/第N卷/第N章.md`，或对该文件的局部 section patch / review verdict。
- Output format: Markdown 章级规划，必须包含章标题、故事概要、冲突、节奏曲线、人物、场景、道具、任务线、章末达成、线索、伏笔、规避；节奏曲线必须包含 `selected_pack`、`selected_mode`、七步职责映射、规划义务、义务段位、建议写法和 Mermaid 图。
- Output path: canonical 业务真源固定为 `projects/story/<项目名>/2-Planning/第N卷/第N章.md`；技能包自身模板位于 `templates/chapter-planning.template.md`。
- Naming convention: 卷目录使用 `第N卷`，章文件使用 `第N章.md`；章级规划中的任务 ID 和引用 ID 必须保持 ASCII 安全字符；不得另建旧式 `章节规划` 并列真源。
- Completion gate: 上游 `整体规划.md` 与目标卷 `卷规划.md` 已回读；必填标题齐全；节奏 handoff 齐全且含 Mermaid 图；任务线含汇聚动作与未汇聚去向；线索/伏笔分离；无正文、对白、叙述段落或正文桥段；review verdict 至少为 `pass_with_followups`。

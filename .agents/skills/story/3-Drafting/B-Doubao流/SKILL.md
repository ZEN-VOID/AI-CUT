---
name: story-drafting-doubao
description: Use when story2026 needs chapter-native novel drafting that turns current planning truth plus global/style/north-star/project context into `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`.
governance_tier: full
---

# 3-Drafting / B-Doubao流

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读 story 根层 `../../SKILL.md` 与 `../../CONTEXT.md`，先锁定 `story2026` 总线边界，再进入当前 chapter-native 正文创作。
- 若 `../SKILL.md` 与 `../CONTEXT.md` 非空，必须同时读取作为 `3-Drafting` 阶段路由层。
- 必须同时读取 `../../_shared/context-loading-contract.md` 与 `../../_shared/core-constraints.md`。
- 若当前任务已绑定 `projects/story/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按当前卷/章相关性加载项目根 `CONTEXT/` 中的上下文文件。
- 必须读取当前项目的三层 planning 真源、对象/风格真源与 `north_star.yaml`；具体清单见 `references/chapter-drafting-contract.md`。
- 若上一章正文已存在，必须读取它作为连续性增强输入；若不存在，不得因此阻塞本章起稿。
- 若目标文件已存在，必须先回读现有 `第N卷/第N章.md`，再决定是续写、重写还是局部重构。
- `CONTEXT.md` 只承载经验层 Type Map、Repair Playbook 与 Reusable Heuristics，不得重定义本入口合同。

## Purpose

`B-Doubao流` 是 `story2026` 主链 `3-Drafting` 阶段的豆包 provider 路径。它负责在路由选择豆包流时，把当前章 planning 义务、全局卡、风格卡、`north_star.yaml`、项目记忆、项目上下文与上一章承接，转成可落盘的中文小说章节。

它拥有：

- 当前章正文根文件写权：`projects/story/<项目名>/3-Drafting/第N卷/第N章.md`
- 当前章 YAML frontmatter 的写权
- provider artifacts 的辅助落盘权

它不拥有：

- `0-Init`、`1-Cards`、`2-Planning` 的真源改写权
- `4-Review` 的 PASS/FAIL 判定权
- `5-Loopback` 的 validated actualization 写回权

## Mode Selection

| mode | 触发信号 | 主路径 |
| --- | --- | --- |
| `chapter_draft` | 当前章尚无正文，用户要求起草/写正文 | 读取上游真源后调用豆包生成完整章节 |
| `chapter_rewrite` | 目标章已存在，用户显式要求重写/大修 | 先回读现有正文，要求 `--force` 后按当前 planning 与用户约束重写 |
| `chapter_continue` | 目标章已存在，用户要求续写或补全，且提供续写边界或补充约束 | 保留已成立承接，补足未完成正文；正式写回要求 `--force` |
| `local_repair` | 审查或用户指出局部问题，且提供 finding 或补充约束 | 定位问题层，限制修复范围；正式写回要求 `--force` |
| `dry_run` | 用户或调试要求只装配上下文包 | 只生成 messages pack 与报告，不调用 provider、不写正文真源 |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 需要章节输入、frontmatter、provider 与输出细则 | `references/chapter-drafting-contract.md` |
| 需要兼容旧 step-after-write 即时审计链路 | `../_shared/drafting-instant-validation-contract.md` |
| 需要执行拓扑、分支、汇流、失败回路 | `steps/chapter-drafting-workflow.md` |
| 需要判定起草/重写/续写/修复/dry-run 类型 | `types/drafting-type-map.md` |
| 需要质量门禁、provider 证据与 reviewer 规则 | `review/review-contract.md` |
| 需要可复用写作与迁移经验 | `CONTEXT.md` 与 `knowledge-base/drafting-heuristics.md` |
| 需要章节文件骨架或豆包系统提示 | `templates/chapter-root.template.md`、`templates/doubao-system-prompt.md`、`templates/output-template.md` |
| 需要执行机械辅助 | `scripts/write_chapter_via_doubao.py` |

## Input Contract

### Required Input

- 项目根：`projects/story/<项目名>/`
- 当前卷章定位：`volume_num / chapter_num` 或可由 `chapter_num` 推导的卷号
- 三层 planning：`2-Planning/整体规划.md`、`2-Planning/第N卷/卷规划.md`、`2-Planning/第N卷/第N章.md`
- 对象/风格真源：`1-Cards/0-全局卡/**/*.json`、`1-Cards/1-风格卡/**/*.json`
- 北极星：`0-Init/north_star.yaml`

### Conditional Input

- `projects/story/<项目名>/MEMORY.md`：项目存在时必须加载。
- `projects/story/<项目名>/CONTEXT/**/*.md`：存在时按当前卷/章相关性加载。
- `projects/story/<项目名>/3-Drafting/第N卷/第N-1章.md`：存在时作为承接增强。
- 当前目标章正文：存在时必须回读后再续写、重写或修复。

### Reject Or Block

- 缺少任一必需 planning、全局卡、风格卡或 `north_star.yaml`。
- 用户要求脚本、模板或本地会话直接替代实际 LLM 主创正文。
- provider 失败、认证失败、返回格式不合法，却要求静默写回。
- 目标章已存在但用户未显式选择 `chapter_rewrite / chapter_continue / local_repair`。
- 目标章已存在且不是 `--dry-run` / `--no-writeback`，但未显式传入 `--force`。
- `chapter_continue` 缺少 `--continue-from`、`--instruction` 或 `--instruction-file`。
- `local_repair` 缺少 `--repair-finding`、`--instruction` 或 `--instruction-file`。
- 输出路径被要求降格到平铺 `3-Drafting/第N章.md`、`正文/` 或临时 sibling 文件。

## Actual Creative Engine

正式创作路径固定为：

1. 本地脚本锁路径、读 context、整理模板与约束。
2. AnyFast `doubao-seed-2.0-pro` 负责实际生成完整章节 Markdown 文件。
3. 本地脚本校验返回内容是否满足 frontmatter / heading / 输出路径合同，再写回 `第N卷/第N章.md`。

硬边界：

- “LLM-first creative authorship” 在本技能上的 owning provider 固定为 `doubao-seed-2.0-pro`。
- `scripts/write_chapter_via_doubao.py` 只能装配上下文、调用 provider、校验返回与落盘，不得以规则拼接、模板灌字或启发式扩写替代正文主创。
- 未经用户显式改口，不得把本地 GPT 直写、手工改写或其他 provider 伪装成当前技能的正常主路径。
- 若豆包 provider 因认证、网络、返回格式不合法或上层策略阻断而不可用，必须硬失败并报告阻断来源。

## Visual Maps

```mermaid
flowchart TD
    A["N1 Intake: 锁定项目根与卷章"] --> B["N2 Type Profile: 判定起草/续写/重写/修复"]
    B --> C["N3 Source Alignment: 读取 planning/cards/north_star/MEMORY/CONTEXT/上一章"]
    C --> D{"执行分支"}
    D -->|"chapter_draft"| E["组装新章上下文包"]
    D -->|"chapter_rewrite"| F["回读现稿并组装重写约束"]
    D -->|"chapter_continue"| G["回读现稿并组装续写承接"]
    D -->|"local_repair"| H["定位局部问题与源层"]
    E --> I["调用 doubao-seed-2.0-pro"]
    F --> I
    G --> I
    H --> I
    I --> J["校验 frontmatter / heading / 正文完整度"]
    J --> K{"Gate"}
    K -->|"pass"| L["写回 第N卷/第N章.md"]
    K -->|"fail"| M["Root-Cause Route"]
    M --> C
```

```mermaid
graph LR
    A["整体规划.md"] --> H["north_star_chapter_brief"]
    B["卷规划.md"] --> H
    C["第N章.md"] --> H
    D["全局卡"] --> I["global_context"]
    E["风格卡"] --> J["style_context"]
    F["项目 MEMORY.md"] --> K["project_memory_constraints"]
    G["项目 CONTEXT/ + 上一章"] --> L["continuity bridge"]
    H --> M["YAML frontmatter"]
    I --> M
    J --> M
    K --> M
    L --> N["chapter body"]
    M --> O["第N卷/第N章.md"]
    N --> O
```

## Core Gates

- 必须先锁定当前章 planning，再读取 global/style/north-star；不得凭风格或世界观反推当前章义务。
- YAML 头必须显式包含 `写作模型`、`global_context`、`style_context` 与 `north_star_chapter_brief`；`写作模型` 固定为 `Doubao`。
- 正文主体必须是小说 prose，不得把 planning 中的标题、任务线或规避条目原样复制成正文段落。
- 输出路径固定为 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`。
- provider 返回内容缺完整可解析 YAML frontmatter、必需字段、`写作模型: Doubao`、非空 `global_context / style_context / north_star_chapter_brief`、`# 第N章｜章标题` 标题行或正文完整度时，禁止写回业务真源。
- provider artifacts 可落到项目 `reports/3-Drafting/doubao/.../`，但它们不是业务真源。

## Root-Cause Execution Contract

失败追溯链固定为：

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> Meta Rule Source`

| symptom | direct owner | rework target |
| --- | --- | --- |
| 草稿跑偏或 planning 语言直贴 | 章节正文细则层 | `references/chapter-drafting-contract.md` |
| 章节结构断裂、分支/汇流不清 | 思行网络层 | `steps/chapter-drafting-workflow.md` |
| 起草/续写/重写/修复误判 | 类型策略层 | `types/drafting-type-map.md` |
| 审查口号化或无法给 verdict | 质量门禁层 | `review/review-contract.md` |
| 输出路径、命名或模板冲突 | 入口与模板层 | `SKILL.md` Output Contract + `templates/output-template.md` |
| 脚本越权生成正文 | 自动化辅助层 | `scripts/write_chapter_via_doubao.py` + AGENTS.md LLM-first 规则 |
| 可复用失败模式再次出现 | 经验层 | `CONTEXT.md` |

## Field Mapping

### Directory Ownership Table

| field_id | directory_or_file | owner_role | must_contain | fail_code |
| --- | --- | --- | --- | --- |
| `FIELD-DRAFT-01` | `SKILL.md` | 入口与裁决层 | trigger、loading、mode、reference guide、root-cause、Output Contract | `FAIL-DRAFT-ENTRY` |
| `FIELD-DRAFT-02` | `references/` | 章节细则层 | input、frontmatter、provider、正文硬规则 | `FAIL-DRAFT-REFERENCE` |
| `FIELD-DRAFT-03` | `steps/` | 思行网络层 | node network、branch、merge、failure route | `FAIL-DRAFT-STEPS` |
| `FIELD-DRAFT-04` | `types/` | 类型策略层 | drafting mode、type variables、route matrix | `FAIL-DRAFT-TYPES` |
| `FIELD-DRAFT-05` | `review/` | 质量门禁层 | verdict model、finding shape、provider evidence gate | `FAIL-DRAFT-REVIEW` |
| `FIELD-DRAFT-06` | `templates/` | 模板层 | chapter skeleton、system prompt、Output Contract Alignment | `FAIL-DRAFT-TEMPLATE` |
| `FIELD-DRAFT-07` | `scripts/` | 自动化辅助层 | context assembly、provider bridge、validation、writeback | `FAIL-DRAFT-SCRIPT` |
| `FIELD-DRAFT-08` | `CONTEXT.md` | 经验层 | Type Map、Repair Playbook、Reusable Heuristics | `FAIL-DRAFT-CONTEXT` |
| `FIELD-DRAFT-09` | `agents/openai.yaml` | 入口元数据层 | display name、short description、default prompt | `FAIL-DRAFT-AGENT` |

### Node Handoff Table

| node_id | input | action | output | next_gate |
| --- | --- | --- | --- | --- |
| `N1-SOURCE-LOCK` | 用户请求与项目根 | 锁定卷章与 canonical output | `source_lock_note` | `N2-TYPE-PROFILE` |
| `N2-TYPE-PROFILE` | 目标章状态与用户意图 | 判定 drafting mode | `type_profile` | `N3-CONTEXT-PACK` |
| `N3-CONTEXT-PACK` | planning/cards/north_star/MEMORY/CONTEXT/上一章 | 组装 provider context | `messages_pack` | `N4-DRAFT-BRANCH` |
| `N4-DRAFT-BRANCH` | `type_profile` 与 context pack | 选择新章/重写/续写/修复分支 | `branch_prompt` | `N6-PROVIDER-DRAFT` |
| `N6-PROVIDER-DRAFT` | provider prompt | 调用豆包生成完整章节 | `provider_output` | `N7-VALIDATE-WRITEBACK` |
| `N7-VALIDATE-WRITEBACK` | provider output | 校验并写回 canonical path | `chapter_file` | done |

### Failure Routing Table

| fail_code | symptom | rework_target |
| --- | --- | --- |
| `FAIL-DRAFT-ENTRY` | 入口缺 loading、mode、Output Contract 或 root-cause 合同 | `SKILL.md` |
| `FAIL-DRAFT-REFERENCE` | 输入、frontmatter 或 provider 硬规则缺失 | `references/chapter-drafting-contract.md` |
| `FAIL-DRAFT-STEPS` | 流程只有 checklist，没有分支、汇流或 gate | `steps/chapter-drafting-workflow.md` |
| `FAIL-DRAFT-TYPES` | 起草、续写、重写、修复误判 | `types/drafting-type-map.md` |
| `FAIL-DRAFT-REVIEW` | 无法给出可执行 verdict 或 provider evidence gate | `review/review-contract.md` |
| `FAIL-DRAFT-TEMPLATE` | 模板与 Output Contract 不一致 | `templates/output-template.md` |
| `FAIL-DRAFT-SCRIPT` | 脚本越权主创或未校验 provider 输出 | `scripts/write_chapter_via_doubao.py` |

## Standard Invocation

```bash
python3 .agents/skills/story/3-Drafting/B-Doubao流/scripts/write_chapter_via_doubao.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --mode chapter_draft
```

Dry run:

```bash
python3 .agents/skills/story/3-Drafting/B-Doubao流/scripts/write_chapter_via_doubao.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --dry-run
```

Rewrite existing chapter:

```bash
python3 .agents/skills/story/3-Drafting/B-Doubao流/scripts/write_chapter_via_doubao.py \
  --project-root "projects/story/<项目名>" \
  --chapter 12 \
  --mode chapter_rewrite \
  --instruction "按 review finding 修正节奏断裂与人物失声口" \
  --force
```

## Output Contract

| field | contract |
| --- | --- |
| Required output | 当前章完整中文小说 Markdown 文件，以及必要的 provider sidecar artifacts。 |
| Output format | YAML frontmatter、空行、`# 第N章｜章标题`、章节正文；frontmatter schema 见 `references/chapter-drafting-contract.md`。 |
| Output path | 业务真源固定写入 `projects/story/<项目名>/3-Drafting/第N卷/第N章.md`；provider artifacts 可写入 `projects/story/<项目名>/reports/3-Drafting/doubao/.../`。 |
| Naming convention | 卷目录使用 `第N卷`，章节文件使用 `第N章.md`；不得降格为平铺旧路径、`正文/` 或临时 sibling 文件。 |
| Completion gate | 豆包 provider 真实命中；返回内容通过 frontmatter、必需字段、标题行与正文完整度校验；正式正文已写回 canonical path；必要 sidecar 能追溯 messages pack、raw output 与 writeback。 |

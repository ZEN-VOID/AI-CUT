---
name: story-polishing
description: Use when story2026 needs chapter-level second-pass polishing from `projects/story/<项目名>/3-初稿/第N卷/第N章.md` into `projects/story/<项目名>/4-润色/第N卷/第N章.md`.
governance_tier: lite
skill_role: parent_guide
---

# 4-润色

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 必须回读 story 根层 `../SKILL.md` 与 `../CONTEXT.md`，先锁定 `story2026` 总线边界，再进入本阶段。
- 若当前任务绑定 `projects/story/<项目名>/`，必须先加载项目根 `MEMORY.md`，再按当前卷/章相关性加载项目根 `CONTEXT/`。
- 必须读取当前章 `projects/story/<项目名>/3-初稿/第N卷/第N章.md` 作为润色主输入；若缺失，禁止凭 planning、摘要或记忆直接生成润色稿。
- 当前章 planning、`north_star.yaml` 与项目上下文只用于校准义务、风格和题材质感，不得取代 `3-初稿` 成为润色主文本。
- `CONTEXT.md` 只承载经验层 Type Map、Repair Playbook 与 Reusable Heuristics，不得重定义本入口合同。

## Purpose

`4-润色` 是 `story2026` 在 `3-初稿` 之后的章节级二次改写阶段。它承接 `3-初稿` 的正文真源，在不改写核心剧情事实、不替代 planning/cards/north_star 的前提下，输出更自然、更贴合题材质感的中文小说章节。

它拥有：

- 当前章润色稿写权：`projects/story/<项目名>/4-润色/第N卷/第N章.md`
- 当前章润色稿写权仅限：`projects/story/<项目名>/4-润色/第N卷/第N章.md`
- 只对本次被调度 lane 的有效输出做父级聚合与最终落盘的裁决权

它不拥有：

- `0-初始化`、`1-设定`、`2-卷章` 的真源改写权
- `3-初稿` 原始正文覆盖权
- `review` 的 PASS/FAIL 判定权
- 未被本轮实际调度 lane 的占位输出、空字段或理论补丁生成权

## Mode Selection

| lane | 默认状态 | 触发信号 | 子技能 |
| --- | --- | --- | --- |
| `B-Doubao流` | default active | 用户未点名 provider、强调中文表达、网文质感、去 AI 味、整章润色 | `B-Doubao流/SKILL.md` |
| `A-GPT原生` | explicit | 用户点名 GPT 原生、当前会话直接润色、或需要人工式本地落盘校验 | `A-GPT原生/SKILL.md` |
| `C-Deepseek流` | explicit | 用户点名 DeepSeek、需要 deepseek-v4-pro 高推理润色 | `C-Deepseek流/SKILL.md` |

## Task Modes

| mode | 触发信号 | 父级动作 | 子流动作 |
| --- | --- | --- | --- |
| `chapter_polish` | `4-润色` 目标章不存在 | 锁定源初稿、选择 lane、生成第一版润色稿 | 从 `3-初稿` 生成 `4-润色` |
| `polish_rewrite` | `4-润色` 目标章已存在，用户要求重润、覆盖、重新润色 | 回读源初稿与既有润色稿；要求显式覆盖确认 | 重新生成完整润色稿 |
| `local_repair` | 用户或 review 指出局部表达、质感、连续性或事实漂移问题 | 把 finding 路由到最小有效修复范围 | 局部修复，不扩大为整章重写，除非 finding 指向全章失效 |
| `dry_run` | 用户或脚本只要求装配上下文 | 只返回 stdout 摘要，不写正文真源 | 不调用 provider 或不落盘正文 |

## Input Contract

### Required Input

- 项目根：`projects/story/<项目名>/`
- 当前卷章定位：`volume_num / chapter_num`，或可由 `chapter_num` 推导卷号。
- 初稿正文：`projects/story/<项目名>/3-初稿/第N卷/第N章.md`
- 规划参考：`projects/story/<项目名>/2-卷章/整体规划.md`
- 规划参考：`projects/story/<项目名>/2-卷章/第N卷/卷规划.md`
- 规划参考：`projects/story/<项目名>/2-卷章/第N卷/第N章.md`
- 风格/题材参考：`projects/story/<项目名>/0-初始化/north_star.yaml`

### Conditional Input

- `projects/story/<项目名>/MEMORY.md`：项目存在时必须加载。
- `projects/story/<项目名>/CONTEXT/**/*.md`：存在时按当前章相关性加载。
- 既有 `projects/story/<项目名>/4-润色/第N卷/第N章.md`：存在时必须回读，覆盖需显式 force 或等价确认。
- 上一章初稿或润色稿：存在时作为连续性、文气和章间节奏参考。
- review finding / 用户局部问题描述：进入 `local_repair` 时必须加载。

### Reject Or Block

- 缺少当前章 `3-初稿` 正文。
- 用户要求润色阶段凭 planning 从零写正文。
- 用户要求润色时静默改动核心事件、人物关系、世界观事实或章级任务结果。
- 用户要求把润色结果写回 `3-初稿/`、`正文/`、平铺章节文件或临时 sibling 文件。
- 目标章已存在但用户没有明确允许覆盖，且当前不是 `dry_run` / `no_writeback`。

## Base Polishing Rules

1. 更符合中文表达风格：去掉翻译腔、说明腔、AI 腔、过度工整的平均句长，让句群有自然呼吸、轻重和停顿。
2. 更符合题材的写作质感：读取 `north_star.yaml.genre_contract` 与风格约束，让场景密度、情绪颗粒、对白锋利度、心理节奏和段落推进服务当前题材。
3. 初稿事实优先：保留初稿已成立的事件顺序、人物动机、信息揭示、章末牵引；只在用户明确要求时做结构级重写。
4. 润色不是摘要：输出必须是完整润色章节 prose，不得变成点评、建议、改写说明或段落清单。
5. 润色不是审查结论：发现源层问题时生成 repair finding 或阻断报告，不把下游润色伪装成上游真源修复。
6. 润色不是同义词替换：必须有句群节奏、段落密度、动作/感官/对白/心理层面的二次加工。
7. 润色不是清洗风格：不得把作者口味、项目长期偏好、题材锋芒和人物声音修成通用顺滑文本。

## Polishing Quality Gates

| gate_id | gate | pass condition |
| --- | --- | --- |
| `G1-SOURCE-ANCHOR` | 初稿锚定 | 润色稿的核心事件、人物动机、信息揭示和章末牵引可追溯到 `3-初稿` |
| `G2-CHINESE-PROSE` | 中文语感 | 没有明显翻译腔、说明腔、AI 腔、平均句长和段落机械对称 |
| `G3-GENRE-TEXTURE` | 题材质感 | `north_star.yaml.genre_contract` 能落实到场景压力、情绪颗粒、对白和节奏 |
| `G4-CONTINUITY` | 连续性 | 与上一章、当前章 planning、项目记忆不冲突 |
| `G5-OUTPUT-SHAPE` | 输出形态 | 完整 Markdown 章节；frontmatter 至少包含 `润色模型` 与 `初稿来源` |
| `G6-PATH` | 路径 | 写入 `4-润色/第N卷/第N章.md` |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| GPT 原生润色 | `A-GPT原生/SKILL.md` + `A-GPT原生/CONTEXT.md` |
| Doubao provider 润色 | `B-Doubao流/SKILL.md` + `B-Doubao流/CONTEXT.md` |
| DeepSeek provider 润色 | `C-Deepseek流/SKILL.md` + `C-Deepseek流/CONTEXT.md` |
| 需要 lane 级细则 | 对应 lane 的 `references/chapter-polishing-contract.md` |
| 需要执行拓扑 | 对应 lane 的 `steps/chapter-polishing-workflow.md` |
| 需要判定 mode | 对应 lane 的 `types/polishing-type-map.md` |
| 需要质量门禁 | 对应 lane 的 `review/review-contract.md` |
| 需要输出骨架或系统提示 | 对应 lane 的 `templates/` |
| 需要机械辅助 | 对应 lane 的 `scripts/polish_chapter_*.py` |
| 父级导引最小结构 | 本父级导引 skill 只要求同目录 `SKILL.md + CONTEXT.md`；润色模板、类型包、provider bridge 和质量 gate 归 A/B/C 子路径 |

## Execution Topology

```mermaid
flowchart TD
    A["N1 Intake: 项目根与卷章"] --> B["N2 Source Lock: 读取 3-初稿 源章"]
    B --> C["N3 Context Pack: planning/north_star/MEMORY/CONTEXT/上一章"]
    C --> D{"N4 Lane Route"}
    D -->|"default"| E["B-Doubao流"]
    D -->|"GPT explicit"| F["A-GPT原生"]
    D -->|"DeepSeek explicit"| G["C-Deepseek流"]
    E --> H["N5 Validate: 中文表达/题材质感/事实锚定"]
    F --> H
    G --> H
    H --> I{"Gate"}
    I -->|"pass"| J["写回 4-润色/第N卷/第N章.md"]
    I -->|"fail"| K["Root-Cause Route"]
    K --> B
```

## Root-Cause Execution Contract

失败追溯链固定为：

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> Meta Rule Source`

| symptom | direct owner | rework target |
| --- | --- | --- |
| 缺少 `3-初稿` 仍尝试润色 | 输入合同层 | `SKILL.md` Input Contract |
| 润色稿改动核心剧情事实 | 源文本锚定层 | `Base Polishing Rules` + 对应 lane prompt |
| 语言顺但没有中文小说手感 | 中文语感层 | `Polishing Quality Gates` + `CONTEXT.md` Type Map |
| 题材味被磨平 | 题材质感层 | `north_star.yaml.genre_contract` + `CONTEXT.md` Type Map |
| 输出成点评、摘要或差异说明 | 输出形态层 | `Output Contract` + lane template |
| 覆盖既有润色稿没有确认或 backup | 写回安全层 | 对应 lane script + review gate |
| 输出无法追溯源初稿或 provider/GPT 执行 | 证据链层 | lane script + `Output Contract` |
| 子流没有加载同目录 `CONTEXT.md` | Skill 2.0 加载层 | lane `Context Loading Contract` |

## Field Mapping

### Directory Ownership Table

| field_id | directory_or_file | owner_role | must_contain | fail_code |
| --- | --- | --- | --- | --- |
| `FIELD-POLISH-01` | `SKILL.md` | 父级入口与路由裁决层 | loading、mode/lane、input/output、base rules、quality gates | `FAIL-POLISH-ENTRY` |
| `FIELD-POLISH-02` | `CONTEXT.md` | 父级经验层 | Type Map、Repair Playbook、Reusable Heuristics | `FAIL-POLISH-CONTEXT` |
| `FIELD-POLISH-03` | `A-GPT原生/` | GPT 原生 lane | GPT-native 润色合同、模板、脚本、证据链 | `FAIL-POLISH-GPT-LANE` |
| `FIELD-POLISH-04` | `B-Doubao流/` | 默认 provider lane | Doubao 润色合同、模板、脚本、provider evidence | `FAIL-POLISH-DOUBAO-LANE` |
| `FIELD-POLISH-05` | `C-Deepseek流/` | DeepSeek provider lane | DeepSeek 润色合同、模板、脚本、provider evidence | `FAIL-POLISH-DEEPSEEK-LANE` |
| `FIELD-POLISH-06` | lane `templates/` | 输出模板层 | frontmatter、heading、正文骨架、Output Contract Alignment | `FAIL-POLISH-TEMPLATE` |
| `FIELD-POLISH-07` | lane `scripts/` | 自动化辅助层 | context pack、provider bridge、校验、writeback、backup | `FAIL-POLISH-SCRIPT` |

### Node Handoff Table

| node_id | input | action | output | next_gate |
| --- | --- | --- | --- | --- |
| `N1-INTAKE` | 用户请求、项目根、卷章 | 判定 `chapter_polish / polish_rewrite / local_repair / dry_run` | `polish_task_profile` | `N2-SOURCE-LOCK` |
| `N2-SOURCE-LOCK` | `polish_task_profile` | 锁定并读取 `3-初稿` 源章与目标 `4-润色` 路径 | `source_lock` | `N3-CONTEXT-PACK` |
| `N3-CONTEXT-PACK` | 源章、planning、north_star、MEMORY、CONTEXT、上一章 | 组装 lane 可消费上下文 | `context_pack` | `N4-LANE-ROUTE` |
| `N4-LANE-ROUTE` | 用户 provider 意图与上下文 | 选择 A/B/C lane | `lane_selection` | `N5-LANE-EXECUTE` |
| `N5-LANE-EXECUTE` | `context_pack`、lane 合同 | 由 LLM/provider 完成润色主创 | `polished_markdown` | `N6-QUALITY-GATE` |
| `N6-QUALITY-GATE` | 润色稿、源章 | 校验事实锚定、中文语感、题材质感、路径与 frontmatter | `gate_result` | `N7-WRITEBACK` |
| `N7-WRITEBACK` | `gate_result=pass` | 写入 canonical path | `4-润色/第N卷/第N章.md` | done |

## Output Contract

| field | contract |
| --- | --- |
| Required output | 当前章完整中文润色稿 Markdown 文件。 |
| Output format | YAML frontmatter、空行、`# 第N章｜章标题`、章节润色稿；frontmatter 至少包含 `润色模型` 与 `初稿来源`。 |
| Output path | 业务真源固定写入 `projects/story/<项目名>/4-润色/第N卷/第N章.md`。 |
| Naming convention | 卷目录 `第N卷`，章节文件 `第N章.md`。 |
| Completion gate | 已真实读取 `3-初稿` 源章；已执行所选 lane 的润色主创；中文表达与题材质感门禁通过；输出写回 canonical path。 |

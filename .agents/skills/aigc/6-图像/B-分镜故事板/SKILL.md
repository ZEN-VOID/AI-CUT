---
name: aigc-image-storyboard-sheet
description: Use when projects/aigc/<项目名>/4-分组 storyboard groups must become complete multi-panel storyboard prompts, reference-bound subject slots, and batch imagegen outputs under projects/aigc/<项目名>/6-图像/B-分镜故事板/.
governance_tier: full
metadata:
  short-description: AIGC group storyboard sheet generation
---

# aigc 6-图像 / B-分镜故事板

`B-分镜故事板` 负责把 `projects/aigc/<项目名>/4-分组/` 中的每个分镜组转为一张组级多格 storyboard：直接使用现有分镜组内容作为生图提示词主体，按组底 YAML 绑定角色、场景、道具图片参照，并调用 `.agents/skills/cli/imagegen` 以分镜组为单位批量生成图像。

## Context Loading Contract

- 每次调用 `$aigc-image-storyboard-sheet` 时，必须同时加载同目录 `CONTEXT.md`。
- 若任务绑定 `projects/aigc/<项目名>/`，必须先加载项目根 `MEMORY.md`，再加载 `projects/aigc/<项目名>/0-初始化/north_star.yaml` 与项目根 `CONTEXT/` 中和图像阶段相关的上下文。
- `4-分组` 是本技能的主要信息来源；不得回到 `3-摄影` 或更早阶段重写分镜组内容，除非用户显式要求修复上游。
- 分镜故事板 prompt 主体直接采用 `4-分组` 的现有分镜组正文；LLM 只负责裁决提取范围、保真组织、缺口说明和审查，不得扩写或改写剧情事实。
- 主体参照以分镜组底部 YAML 的 `角色 / 场景 / 道具` 为基准；不得用正文泛词、子串或猜测名自动扩展主体列表。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `.agents/skills/aigc/SKILL.md` > `.agents/skills/aigc/6-图像/SKILL.md` > 本 `SKILL.md` > `references/` / `steps/` / `types/` / `review/` / `templates/` > `.agents/skills/cli/imagegen/SKILL.md` > `agents/openai.yaml` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Input Contract

Accepted input:

- 项目名、项目路径、单集或多集范围，要求从 `4-分组` 批量生成组级分镜故事板。
- 用户指定一个或多个三段式分镜组 ID，例如 `1-1-1`。
- 已有 `6-图像/B-分镜故事板/` prompt、参照绑定、imagegen 计划或生成结果需要 repair / review / rerun。

Required input:

- 可定位的 `projects/aigc/<项目名>/4-分组/第N集.md`。
- 每个目标分镜组必须有可解析的 `## x-y-z` 标题、组正文和底部 fenced YAML。
- 可定位的设计生成目录：`5-设计/角色/3-生成`、`5-设计/场景/3-生成`、`5-设计/道具/3-生成`；目录缺失时允许 prompt-only 或缺图继续，但必须写入报告。
- 调用 imagegen 前必须能确定项目内输出目录，默认 `projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/`。

Optional input:

- `prompt_only`：只生成故事板 prompt 与参照 manifest，不执行 imagegen。
- `episode_batch`：一次处理一集全部分镜组。
- `group_batch`：一次处理多个指定分镜组。
- `imagegen_mode`：默认遵循 `.agents/skills/cli/imagegen` 的内置 `image_gen` 路由；CLI/API fallback 只有用户显式要求时允许。
- 用户指定 aspect ratio、尺寸、额外禁止项、执行节奏、输出目录或 rerun / replace 策略。

Reject or clarify when:

- `4-分组` 缺失、目标分镜组 ID 无法唯一追溯，或组底 YAML 缺失到无法确定主体槽位。
- 用户要求改变 `4-分组` 的剧情核心、镜头顺序、角色事实、动作结果或组边界。
- 用户要求脚本主创 storyboard prompt 正文、自动扩写剧情或用模板补写未知画面。
- 任务目标是单一四段式 `分镜ID` 的单帧图，应转入 `A-分镜画面`。

## Positioning

本技能是 `6-图像` 阶段的组级多格 storyboard 入口，向上承接 `4-分组`，向下调用 `.agents/skills/cli/imagegen`。它拥有组级 prompt 包、主体参照绑定、批量生图计划、生成结果持久化和执行报告的裁决权；它不拥有上游分组改写权，也不拥有主体资产重设计权。

## Mode Selection

| mode | 触发信号 | 主要动作 |
| --- | --- | --- |
| `prompt_only` | 只要求提示词、配置或 prompt 包 | 执行 step1-step2，写 prompt 与 reference manifest |
| `single_group_generate` | 指定一个三段式分镜组 ID 且要求出图 | 执行 step1-step3，单组调用 imagegen |
| `episode_batch_generate` | 指定一集或默认整集批量 | 对该集全部分镜组执行 step1-step3，按 imagegen 当前能力顺序或受控批量执行 |
| `group_batch_generate` | 指定多个分镜组 ID | 只处理目标分镜组集合，保持独立 prompt 与输出 |
| `repair` | prompt 缺组、槽位错绑、图片缺失、生成计划漂移 | 按 `review/review-contract.md` 定位返工节点 |
| `review_only` | 只检查现有输出 | 审查 prompt、参照、imagegen 计划与落盘结果，不生成新图 |

## Reference Loading Guide

| 场景 | 必读文件 |
| --- | --- |
| 从 `4-分组` 提取组级正文与底部 YAML | `references/group-source-extraction.md` |
| 组装多格 storyboard prompt 固定开头与主体正文 | `references/prompt-assembly-contract.md` |
| 查找并绑定角色、场景、道具参照图 | `references/reference-slot-binding.md` |
| 调用 `.agents/skills/cli/imagegen` 与批量生成交接 | `references/imagegen-handoff.md` |
| 执行 step1-step3 主流程 | `steps/storyboard-sheet-workflow.md` |
| 判定单组、整集、多组、修复模式 | `types/type-map.md` |
| 输出审查与返工 | `review/review-contract.md` |
| 输出模板 | `templates/output-template.md`、`templates/storyboard-sheet-prompt-template.md` |
| 脚本辅助边界 | `scripts/README.md` |
| 可复用经验 | `knowledge-base/storyboard-sheet-heuristics.md` |
| 产品侧入口元数据 | `agents/openai.yaml` |

## Visual Maps

```mermaid
flowchart TD
    A["projects/aigc/<项目名>/4-分组/第N集.md"] --> B["step1 锁定分镜组"]
    B --> C["直接保留组正文作为 prompt 主体"]
    B --> D["读取组底 YAML: 角色/场景/道具"]
    C --> E["固定 storyboard 开头 + 组正文"]
    D --> F["step2 主体图片参照绑定"]
    G["5-设计/角色/3-生成"] --> F
    H["5-设计/场景/3-生成"] --> F
    I["5-设计/道具/3-生成"] --> F
    E --> J["组级 prompt package"]
    F --> J
    J --> K["step3 imagegen batch handoff"]
    K --> L["6-图像/B-分镜故事板/第N集"]
```

```mermaid
flowchart TD
    A["分镜组 x-y-z"] --> B["固定英文开头"]
    B --> C["4-分组现有正文"]
    C --> D["保留分镜1..N完整顺序"]
    D --> E{"生成布局"}
    E -->|"少量镜头"| F["紧凑横向或 2xN"]
    E -->|"中等镜头"| G["自适应网格"]
    E -->|"大量镜头"| H["分页或密集网格并记录风险"]
```

```mermaid
stateDiagram-v2
    [*] --> Intake
    Intake --> ExtractGroups
    ExtractGroups --> AssembleStoryboardPrompt
    AssembleStoryboardPrompt --> BindSubjects
    BindSubjects --> ReviewGate
    ReviewGate --> PromptOnly
    ReviewGate --> ImagegenBatch
    ImagegenBatch --> PersistResults
    PersistResults --> CloseReport
    ReviewGate --> Repair
    Repair --> ExtractGroups
    CloseReport --> [*]
```

## Execution Contract

1. 加载本 `SKILL.md + CONTEXT.md`；项目任务中加载 `MEMORY.md`、`north_star.yaml` 与相关项目上下文。
2. 按 `types/type-map.md` 锁定 mode、集号范围、目标分镜组集合、是否执行 imagegen。
3. 执行 step1：以 `projects/aigc/<项目名>/4-分组` 为主要信息来源，解析每个 `## x-y-z` 分镜组，完整提取组正文和底部 YAML；prompt 主体直接使用现有组内容，不进行剧情改写。
4. step1 组装 prompt 时必须添加固定开头：`Create a multi-panel storyboard based on the following shot breakdown. Add the shot sequence number in the bottom-left corner of each panel (no other text). Auto-adapt the panel layout grid based on the total number of shots.`
5. 执行 step2：读取每个分镜组底部 YAML 的 `角色 / 场景 / 道具`，检查 `projects/aigc/<项目名>/5-设计/角色/3-生成`、`5-设计/场景/3-生成`、`5-设计/道具/3-生成` 中是否存在对应主体名称图片；多视图优先，没有多视图就主图，都没有就空着并从参照槽位移除。
6. 执行 step3：按 `.agents/skills/cli/imagegen` 规范调用图像生成。每个分镜组是一个独立任务，prompt 必须包含完整分镜故事板信息和已绑定的角色、场景、道具参照；默认使用内置 `image_gen` 路由，执行节奏按当前工具能力顺序或受控批量处理，不设置后台并行要求。
7. built-in `image_gen` 默认可用 `text_prompt_only` 方式生成并复制到项目 `images/`；本地 reference path 记录在 prompt / manifest / plan 中，但不得宣称已作为视觉输入传给工具。该状态不阻断生成，必须在 results/report 中写 `reference_input_status: not_passed_to_generation_tool` 或等价说明。
8. 生成时可根据每个分镜组的分镜数量灵活布局，但必须确保所有镜头都进入 storyboard；若镜头数过多导致单图完整性风险，应在计划中标记分页或人工确认策略。
9. 每个分镜组的 canonical 输出写入 `projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/`，并生成执行报告。
10. 交付前执行 `review/review-contract.md`；组 ID 追溯、固定开头、组正文完整性、YAML 主体基准、参照路径存在性、imagegen 输出持久化必须通过。

## Field Mapping

| field_id | 输出/证据 | 内容要求 | 失败码 |
| --- | --- | --- | --- |
| `FIELD-SHEET-01` | input manifest | 项目根、集号、`4-分组`、设计生成目录可追溯 | `FAIL-SHEET-INPUT` |
| `FIELD-SHEET-02` | group index | 三段式 `x-y-z` 可回指 `## x-y-z`，组正文和 YAML 被完整提取 | `FAIL-SHEET-GROUP` |
| `FIELD-SHEET-03` | prompt package | 固定英文开头 + 现有组内容主体，保留分镜顺序和完整性 | `FAIL-SHEET-PROMPT` |
| `FIELD-SHEET-04` | reference manifest | Characters / Scene / Props 只来自组底 YAML，且只绑定真实图片，多视图优先 | `FAIL-SHEET-REF` |
| `FIELD-SHEET-05` | imagegen plan/result | 一组一任务，调用 `.agents/skills/cli/imagegen`，按当前工具能力执行，输出持久化到项目内 | `FAIL-SHEET-IMAGEGEN` |
| `FIELD-SHEET-06` | execution report | 说明 generated / skipped / failed、缺图、分页或完整性风险 | `FAIL-SHEET-REPORT` |

## Field Master

| field_id | owner | canonical file | must contain | fail code |
| --- | --- | --- | --- | --- |
| `FIELD-SHEET-01` | input lock | `第N集-group-index.json` / report | 项目根、集号、`4-分组`、设计生成目录 | `FAIL-SHEET-INPUT` |
| `FIELD-SHEET-02` | group extraction | `第N集-group-index.json` | `group_id`、source heading、shot count、YAML subjects | `FAIL-SHEET-GROUP` |
| `FIELD-SHEET-03` | prompt assembly | `第N集-分镜故事板-prompts.md` | 固定开头、组正文主体、完整分镜顺序 | `FAIL-SHEET-PROMPT` |
| `FIELD-SHEET-04` | reference binding | `第N集-reference-manifest.json` | 角色/场景/道具真实图片路径，多视图优先 | `FAIL-SHEET-REF` |
| `FIELD-SHEET-05` | imagegen handoff | `第N集-imagegen-plan.json` / `第N集-imagegen-results.json` | 一组一任务、合法 mode、项目内输出路径 | `FAIL-SHEET-IMAGEGEN` |
| `FIELD-SHEET-06` | convergence | `执行报告.md` | generated / skipped / failed、review verdict、返工入口 | `FAIL-SHEET-REPORT` |

## Thought Pass Map

| pass_id | focus field | core question | action | evidence |
| --- | --- | --- | --- | --- |
| `PASS-SHEET-01` | `FIELD-SHEET-01` | 本轮处理哪个项目、集号和分镜组范围 | 锁定 mode、读取项目上下文 | input manifest |
| `PASS-SHEET-02` | `FIELD-SHEET-02` | 如何从 `4-分组` 保真提取组正文和 YAML | 解析 `## x-y-z` 与 fenced YAML | group index |
| `PASS-SHEET-03` | `FIELD-SHEET-03` | 如何保证 prompt 是多格 storyboard 而不是单帧 | 添加固定开头，直接接组正文主体 | prompt markdown |
| `PASS-SHEET-04` | `FIELD-SHEET-04` | 哪些 YAML 主体有真实本地图片可绑定 | 多视图优先、主图次之、缺图移除槽位 | reference manifest |
| `PASS-SHEET-05` | `FIELD-SHEET-05` | 生成任务如何按组安全执行 | 生成一组一任务 imagegen plan 并按需调用 | plan / results |
| `PASS-SHEET-06` | `FIELD-SHEET-06` | 输出如何闭环并可返工 | 汇总审查、失败和跳过原因 | execution report |

## Pass Table

| pass_id | pass standard | fail code | rework entry |
| --- | --- | --- | --- |
| `PASS-SHEET-01` | 必需输入可读，设计生成目录状态已记录 | `FAIL-SHEET-INPUT` | `types/type-map.md` |
| `PASS-SHEET-02` | 每个 `group_id` 唯一且可回指源标题、组正文和 YAML | `FAIL-SHEET-GROUP` | `references/group-source-extraction.md` |
| `PASS-SHEET-03` | prompt 以固定开头起笔，现有组内容作为主体，镜头未缺失乱序 | `FAIL-SHEET-PROMPT` | `references/prompt-assembly-contract.md` |
| `PASS-SHEET-04` | 所有绑定路径存在，且图片选择遵守 YAML 基准和多视图优先 | `FAIL-SHEET-REF` | `references/reference-slot-binding.md` |
| `PASS-SHEET-05` | imagegen plan 一组一任务，默认内置路由，输出路径在项目内 | `FAIL-SHEET-IMAGEGEN` | `references/imagegen-handoff.md` |
| `PASS-SHEET-06` | 执行报告记录 verdict、处理范围、失败/跳过与返工入口 | `FAIL-SHEET-REPORT` | `review/review-contract.md` |

## Root-Cause Execution Contract (Mandatory)

出现失败时必须沿链路上溯：

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> AGENTS.md / skill-工作车间`

优先修复：

1. 组无法追溯或 YAML 解析失败：回到 `references/group-source-extraction.md` 与 `steps/storyboard-sheet-workflow.md`。
2. prompt 固定开头漂移、缺镜头或改写组正文：回到 `references/prompt-assembly-contract.md`。
3. 槽位错绑、路径不存在、猜测引用或没有多视图优先：回到 `references/reference-slot-binding.md`。
4. imagegen 误用 CLI/API、执行节奏越权、写位冲突或输出未持久化：回到 `.agents/skills/cli/imagegen/SKILL.md` 与 `references/imagegen-handoff.md`。
5. 输出格式不一致：回到 `templates/output-template.md`。
6. 同类失败可复用：沉淀到同目录 `CONTEXT.md`，稳定后晋升到本文件或分区规范。

## Output Contract

- Required output: 组级 storyboard prompt 包、参照绑定 manifest、imagegen 执行计划或生成结果、逐集执行报告。
- Output format: Markdown prompt 文档 + JSON manifest / plan / result；生成图片为 PNG/JPEG/WebP 等 bitmap 文件，默认按 imagegen 2K 目标执行。
- Output path: `projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/`，其中 prompt 文档、manifest、plan、结果报告与生成图片均在该集目录或其 `images/` 子目录下。
- Naming convention: prompt 文档命名 `第N集-分镜故事板-prompts.md`；索引命名 `第N集-group-index.json`；参照清单命名 `第N集-reference-manifest.json`；生成计划命名 `第N集-imagegen-plan.json`；执行报告命名 `执行报告.md`；图片命名 `<分镜组ID>.png`，例如 `1-1-1.png`。
- Completion gate: 目标分镜组均可从 `4-分组` 回指；每条 prompt 以固定英文开头起笔并完整保留组正文主体；参照槽位只绑定存在的本地图片且多视图优先；执行 imagegen 时遵循 `.agents/skills/cli/imagegen` 的默认路由与项目持久化门禁；审查结果为 `pass` 或 `pass_with_todo`。

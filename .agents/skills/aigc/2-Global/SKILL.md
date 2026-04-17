---
name: aigc-global
description: Use when the global directing stage needs a single thinking-action skill to turn planning grouping outputs and init presets into project-level global style, episode-group type guidance, episode-group director intent, and a shared episode-root group shell seed.
governance_tier: full
---

# aigc 2-Global

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 概述

`2-Global` 是 `aigc` 技能树位于 `1-Planning` 与 `3-Detail` 之间的导演前置全局合同阶段。

它不再把导演能力外包给外置导演组 contracts。从本轮开始，`全局风格`、`全集类型元素`、`分组类型元素`、`导演意图` 四个能力面全部内收在同一 `SKILL.md` 内，以“串行锁定前提 + 项目级双链并行 + 分组级双链并行 + 先在 Markdown 定稿 + 对照字段标题提取入 shared episode root”的知行合一网络完成执行。

本轮重编排遵循两个原则：

- 内容层面全量继承现有 `2-Global` 已沉淀的四份真源、模板口径、项目级/组级分层与下游 handoff 边界
- 机制层面改写为单技能真源，不再维护平行的导演组 team、角色 agent 合同或外置创作方法真源

同时追加一个受 shared runtime 治理的阶段末端强化回路：

- 业务生成仍由当前 `SKILL.md` 的内部能力链完成
- 当项目根 `team.yaml` 启用且 `roles.supervision` 对当前阶段有效时，允许在 canonical 输出首次落盘后，按 `team.yaml -> shared council runtime -> reviewer skill` 的顺序触发一次 `监制 subagents` 会审与优化
- 这条回路只负责评审、给 patch、促成主 agent 二次收束；不生成第二套阶段真源，也不夺取最终写回权

## Skill Execution Rule (Mandatory)

`2-Global` 采用“单技能内部生成 + 阶段末端监制强化”模式：

- skill 自身负责输入读取、业务分析、并发链裁决、模板约束、四份 Markdown 首次写回、字段提取入壳、shared episode root seed、汇流审计与下游回接
- `全局风格`、`全集类型元素`、`分组类型元素`、`导演意图` 的业务生成不是外置 subagents，而是父 skill 的内部能力链
- 若项目根 `team.yaml.enabled == true` 且当前阶段命中 `roles.supervision`，stage-end refine 允许按 shared `council-runtime` 规则调度 reviewer subagents，对已写出的 canonical 文件做一轮监制会审与最小必要优化
- 中间只允许形成内部 `plan / note / report / patch set`；最终 canonical 写回始终由当前 `SKILL.md` / 主 agent 完成
- 不得再回指任何外置导演组 contracts 作为业务生成真源；监制 subagents 只作为阶段末端共享运行时，不得冒充第二创作总线

## When to Use

- 已经有 `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`，需要进入导演前置全局合同阶段。
- 需要把初始化预设、规划分组结果与当前项目定位沉淀为四份 Markdown 长文本真源，并同步写入可被 `3-Detail` 直接继承的 shared episode root。
- 需要在阶段末段先给每个分镜组直接写入固定 `分镜切换` 数字，为 `3-Detail` 的真实切镜提供上游真值。
- 需要同时处理项目级稳定项与当前集分镜组级导演构思，但又不希望把它们混成一份空泛总稿。
- 需要按知行合一方式，把复杂导演判断写成“思行节点 + 并发链 + 汇流门”。

## When Not to Use

- 当前连 `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md` 都不存在。
- 当前任务其实还是分集、剧本或分组问题，应回到 `1-Planning`。
- 当前任务已经在补镜级字段、主体、设计、画面或视频产物，应进入 `3-Detail / 4-Design / 5-Image / 6-Video`。

## Business Requirement Analysis Contract (Mandatory)

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把规划分组结果与初始化预设收束为 `全局风格.md`、`导演意图.md`、`全集类型元素.md`、`分组类型元素.md` 四份导演前置真源，并把已确认字段、固定 `分镜切换` 与完整分组正文直接写入 shared episode root |
| `business_object` | `0-Init` 的项目基线、`1-Planning` 的当前集分组正文、已有 `2-Global` 文档、shared episode root 与四个模板 |
| `constraint_profile` | `全局风格.md` 必须是项目级稳定、可被角色/场景/道具/分镜无污染继承的底层摄影风格协议，并最终形成可直接投放到 Midjourney 等生图/生视频工具前部的统一风格前缀；叙事气质只能作为内部分析与画面映射依据，不得把剧情母题、人物命运判断或导演宣言直接写入最终字段。最终字段默认组织为“媒介属性 + 摄影参照锚点 + 渲染技术栈 + 摄影级总体属性 + 可执行摄影构词”，优先使用能统摄全局的摄影属性词组，例如真实皮肤层次、低饱和暖金室内、潮湿夜色、玻璃反射、轻颗粒、克制电影级照明、高光不过曝、暗部可读、可拍空间光比；重点是统一照明质感、反射控制、颗粒纯度、反差策略、皮肤与材质呈现，不需要再写“空间/时间处理”“统一画面气压”这类抽象总结词，也不固定景别、镜头距离或具体对象内容，且默认禁止具体颜色词、具体材质词、构图术语、焦段/推拉摇移等摄影操作词，以及 `--ar`、`--stylize` 之类工具参数直接进入 canonical 字段；若项目根 `team.yaml.enabled == true` 且当前阶段命中 team 模式，则 `全局风格.md` 必须自然显影 team 痕迹：优先把 `roles.supervision.members` / `team_setup.shared_agents` 中已锁定的 team 成员转写为“参照 XXX 的 XXX”式摄影锚点，并进一步下钻成 AIGC 工具可理解、可执行的具体构词；Markdown 中可额外给出跨工具投影建议，但 `组间设计.全局风格` 与 JSON 提取字段只保留 tool-agnostic core prefix。`全集类型元素.md` 只写项目级类型总则，`分组类型元素.md` 与 `导演意图.md` 都必须按 `第N集 -> 【x-x-x】` 组织；`2-Global/类型元素.md` 只允许作为旧项目迁移输入 fallback，不得作为新输出；`组间设计.全局风格 / 类型元素 / 导演意图` 必须分别直接提取自 Markdown 同名字段，默认字符窗为 `220 / 50 / 100`；`分镜切换` 必须以 `总时长 + 类型元素 + 导演意图 + 分组正文` 为输入，直接写成一个固定镜数，不再写预算包；`组间设计.出场角色及穿搭` 为组级服装摘要槽，`2-Global` 阶段允许先留空字符串，由 `3-Detail` 回填 `角色名-服装简述`；`剧本正文` 必须完整整理入 JSON，除组号标题外不得二次摘要；不得在本阶段发明 shot-level 明细；不再依赖外置导演组 contracts |
| `success_criteria` | 四份 Markdown 真源结构完整、项目级与组级边界清楚、每条内部链都有细致步骤、并发关系与汇流门明确，并且 shared episode root 已写入完整分镜组壳：`分镜组ID / 总时长 / 剧本正文 / 组间设计（含空或已填的出场角色及穿搭） / 分镜切换 / 空分镜明细[]`，可被 `3-Detail` 直接继承 |
| `non_goals` | 不生成 shot-level 明细；不把本阶段写成大而空的“导演宣言”；不再维护第二套导演组 agent 真源 |
| `complexity_source` | 项目级稳定项与当前集组级增量并存；全集类型总则和分组类型打法必须分层；多个能力链共享证据却关注点不同；并发与依赖关系容易打架；质量要求高于普通摘要 |
| `topology_fit` | 前段串行锁输入与不变量，中段按“全局风格 + 全集类型 + 分组类型 + 导演意图预解构”展开，`分组类型元素` 必须继承 `全集类型元素`，`导演意图` 必须等待风格/类型三层约束稳定后再完成写回，后段统一审计与写回 |
| `step_strategy` | 采用“串行主干 + 项目级双链并行 + 分组级双链并行 + 汇流审计”的思行网络，并为四个输出面分别提供细致步骤表与质量门 |

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. 本 `SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/_shared/project-runtime-layout.md`
5. `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
6. `.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
7. `.codex/commands/master-check-team.md`
8. `.codex/commands/master-check.md`
9. `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
10. `.agents/skills/aigc/_shared/group_design_seed_contract.md`
11. `.agents/skills/aigc/_shared/director_episode_output.schema.json`
12. `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
13. `projects/aigc/<项目名>/team.yaml`（若存在）
14. `projects/aigc/<项目名>/0-Init/north_star.yaml`
15. `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
16. `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml`（若存在）
17. `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md`（若存在）
18. `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
19. `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md`（若存在）
20. 现有 `projects/aigc/<项目名>/2-Global/*.md`
21. `projects/aigc/<项目名>/3-Detail/第N集.json`（若存在）
22. 四个模板：
   - `templates/全局风格.template.md`
   - `templates/全集类型元素.template.md`
   - `templates/分组类型元素.template.md`
   - `templates/导演意图.template.md`

## Shared Canonical Sources (Mandatory)

- 强制读取：`.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.agents/skills/aigc/_shared/council-runtime/module-spec.md`
- 强制读取：`.agents/skills/aigc/_shared/council-runtime/team.template.yaml`
- 强制读取：`.agents/skills/aigc/_shared/group_design_seed_contract.md`
- 强制读取：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- 强制读取：`.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
- 条件读取：`.codex/commands/master-check-team.md`（命中阶段末 `监制强化` 时）
- 条件读取：`.codex/commands/master-check.md`（命中阶段末 `监制强化` 时）
- 强制读取：
  - `.agents/skills/aigc/2-Global/templates/全局风格.template.md`
  - `.agents/skills/aigc/2-Global/templates/全集类型元素.template.md`
  - `.agents/skills/aigc/2-Global/templates/分组类型元素.template.md`
  - `.agents/skills/aigc/2-Global/templates/导演意图.template.md`

硬规则：

1. 本阶段的第一输入根固定为 `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`。
2. 项目级稳定约束优先来自 `0-Init/north_star.yaml`、`0-Init/init_handoff.yaml` 与 `story-source-manifest.yaml`。
3. `全局风格.md` 只允许维护项目级稳定总则，且最终字段默认必须保持“无污染底层风格协议”口径；`全集类型元素.md` 只允许维护项目级类型总则；`分组类型元素.md` 必须按 `第N集 -> 【x-x-x】` 组织组级类型判断；三者都不得被某一集局部气氛污染，`类型元素.md` 只允许作为旧项目迁移输入 fallback。
4. `导演意图.md` 必须按 `## 第N集 -> ### 【x-x-x】` 的层次做增量写回，并在命中组内用字段标题 `导演意图` 定稿组级摘要。
5. `3-分组` 的组标题是三段式 `分镜组ID`；四段式 `分镜ID` 属于下游 `3-Detail`。
6. 本阶段必须把 `组间设计` seed 与固定 `分镜切换` 写入 `projects/aigc/<项目名>/3-Detail/第N集.json`，并同步维护 `分镜组列表[].分镜组ID / 总时长 / 剧本正文 / 分镜切换 / 分镜明细=[]` 的组壳；`剧本正文` 必须完整整理自 `1-Planning/3-分组/第N集.md` 的命中组正文，除组号标题外不得二次摘要。
7. `组间设计.全局风格 / 类型元素 / 导演意图` 的 JSON 文本必须分别直接提取自四份 Markdown 中已确认的同名字段；写入 JSON 时只允许剥离字段标题与空白，不允许现场重写。`出场角色及穿搭` 为组级摘要槽，本阶段可先写空字符串占位。
8. `组间设计.全局风格 / 类型元素 / 导演意图` 的默认字符窗固定为 `220 / 50 / 100` 个字符以内；其中 `全局风格` 允许为 AIGC 统一风格前缀做适度放宽，但必须先在 Markdown 中确认。`出场角色及穿搭` 默认采用 `角色名-服装简述` 的短句格式。
9. 四个输出面的判断逻辑、细化步骤与质量门都必须内收在本 `SKILL.md`，不得外包给任何外置导演组 contracts。

## Total Input Contract (Mandatory)

### 必需输入

- `projects/aigc/<项目名>/1-Planning/3-分组/第N集.md`
- `projects/aigc/<项目名>/0-Init/north_star.yaml`
- `projects/aigc/<项目名>/0-Init/init_handoff.yaml`

### 可选输入

- `projects/aigc/<项目名>/0-Init/story-source-manifest.yaml`
- `projects/aigc/<项目名>/1-Planning/2-格式/第N集.md`
- `projects/aigc/<项目名>/1-Planning/3-分组/执行报告.md`
- `projects/aigc/<项目名>/team.yaml`
- 现有 `projects/aigc/<项目名>/2-Global/*.md`
- `projects/aigc/<项目名>/3-Detail/第N集.json`
- 用户显式指定的风格、类型或导演偏好

### 禁止输入

- 与当前项目无关的外部参考文本
- 要求本阶段直接写 shot-level 字段或镜头 JSON 的额外指令
- 任何外置导演组 team、agent、creative method 文档

### 输入处理原则

1. 先锁项目级不变量，再进入全局风格、全集类型、分组类型与导演意图链。
2. 用户显式指定范围或偏好时，用户指定优先，但不得越过项目已锁定真源。
3. 现有 `2-Global/*.md` 只作为增量 patch 依据，不作为绕开上游证据的捷径。
4. 若分组正文不稳定或关键组界不明，`类型元素`、`导演意图` 与 `group_design seed` 只能生成保守版 patch 或 `report`，不得幻想补洞。
5. shared episode root 的 `剧本正文` 必须直接整理自命中组全文；如果落盘内容更像摘要而不是原组正文，视为写回失败。
6. 若存在 `projects/aigc/<项目名>/team.yaml`，必须在输出前读取 shared `council-runtime`，锁定当前阶段是否需要在 canonical 首次落盘后触发 `roles.supervision` 的 stage-end refine。
7. `2-Global` 的 stage-end refine 只允许评审并优化本轮命中的 canonical 文件：`全局风格.md`、`导演意图.md`、`全集类型元素.md`、`分组类型元素.md`、`3-Detail/第N集.json`；不得扩展到无关阶段。

## Visual Maps

```mermaid
flowchart TD
    A["锁定 0-Init + 1-Planning 证据"] --> B["N1 输入与阶段门"]
    B --> C["N2 项目不变量抽取"]
    C --> D["项目级双链 + 导演预解构启动"]
    D --> D1["N3A 全局风格链"]
    D --> D2["N3B 全集类型元素链"]
    D --> D4["N3D 导演意图预解构链"]
    D2 --> D3["N3C 分组类型元素链"]
    D1 --> E["N4 Markdown 字段与约束汇流"]
    D2 --> E
    D3 --> E
    D4 --> F["N5 导演意图完成链"]
    E --> F
    F --> G["N6 JSON 提取 + 固定分镜切换内化 + 组壳写回链"]
    G --> H["N7 汇流审计"]
    H --> I["N8 canonical 首次写回"]
    I --> J["N9 监制 subagents 会审与 refine"]
    J --> K["N10 回接 3-Detail"]
```

```mermaid
flowchart LR
    A["项目证据"] --> B{{"并发能力面"}}
    B --> C["全局风格: 媒介属性 / 渲染底座 / 美学范式 / 纯度过滤 / AIGC 统一前缀 / 禁区"]
    B --> D["全集类型元素: 观众合同 / 主副类型 / 混合公式 / 共用禁区 / 下游规则"]
    D --> E["分组类型元素: 第N集 -> 分镜组 / 类型信号 / 揭示策略 / 负例"]
    B --> K["导演意图预解构: 组任务 / 关注焦点 / 情绪推进 / 空间压力"]
    C --> F{{"风格稳定?"}}
    D --> G{{"全集类型稳定?"}}
    E --> L{{"分组类型稳定?"}}
    K --> H["等待上游约束"]
    F --> I["确认 Markdown 提取字段"]
    G --> I
    L --> I
    H --> I
    I --> J["固定分镜切换内化 + JSON 字段位置 + 剧本正文完整性 + 长度窗校验"]
```

```mermaid
stateDiagram-v2
    [*] --> IntakeLocked
    IntakeLocked --> StageReady
    StageReady --> ParallelRunning
    ParallelRunning --> ConstraintsConverged
    ConstraintsConverged --> DirectorIntentFinalized
    DirectorIntentFinalized --> Audited
    Audited --> FirstWriteback
    FirstWriteback --> SupervisionReview
    SupervisionReview --> Finalized
    Audited --> Rework
    SupervisionReview --> Rework
    Rework --> ParallelRunning
```

```mermaid
graph LR
    A["north_star / init_handoff"] --> B["FIELD-GLOBAL-02 项目不变量"]
    C["第N集分组正文"] --> D["FIELD-GLOBAL-06 组级导演任务"]
    B --> E["FIELD-GLOBAL-04 全局风格"]
    B --> F["FIELD-GLOBAL-05 类型元素"]
    D --> G["FIELD-GLOBAL-07 导演意图"]
    E --> G
    F --> G
    C --> H["FIELD-GLOBAL-08 剧本正文完整入壳"]
    E --> H["FIELD-GLOBAL-08 JSON 提取与组间设计"]
    F --> H
    G --> H
    H --> I["FIELD-GLOBAL-09 汇流审计"]
    I --> J["FIELD-GLOBAL-10 shared root + 3-Detail handoff"]
```

## Internal Capability Fusion Contract (Mandatory)

`2-Global` 不再把导演能力拆给外置角色文档。以下能力面全部内收为父 skill 的内部能力链：

| 能力面 | 作用 | 典型输出 | 何时触发 |
| --- | --- | --- | --- |
| `global_style_engine` | 从项目级证据中提炼稳定的媒介属性、渲染底座、摄影级总体属性、全局控制轴、禁区与下游继承约束，并收束为可跨工具复用的无污染统一风格前缀；必要时补充 `Midjourney` 等工具的投影组织建议 | `global_style_plan`、`global_style_patch`、`style_note`、`style_report` | 每次进入 `2-Global` 时评估；缺风格底座或风格约束变化时强触发 |
| `type_bible_engine` | 把题材、观众合同、主副类型、混合公式、共用禁区与下游读取规则收束为项目级 `全集类型元素.md` | `type_bible_plan`、`type_bible_patch`、`project_type_note`、`type_reference_note` | 每次进入 `2-Global` 时评估；缺项目级类型总则或类型裁决变化时强触发 |
| `group_type_engine` | 继承 `全集类型元素.md`，把当前集分镜组翻译成按组可提取、可执行的 `分组类型元素.md` | `group_type_plan`、`group_type_patch`、`group_type_note`、`group_type_negative_map` | 项目级类型总则稳定后触发；当前集分组变化时强触发 |
| `director_intent_engine` | 把当前集分组结果翻译成按组可消费的导演构思 | `director_intent_plan`、`director_intent_patch`、`director_note`、`director_report` | 当前集分组已稳定时默认触发 |
| `group_design_distill_engine` | 把四份 Markdown 中已确认字段、固定分镜切换与完整分组正文提取到 shared episode root 的分镜组壳，并内化 former `镜花/1-切换` 的 fixed-shot-count 接受逻辑 | `group_design_seed_plan`、`group_design_seed_patch`、`episode_seed_patch`、`switching_rationale_note` | 风格/类型/导演意图都稳定且 Markdown 提取字段已确认后强触发 |
| `convergence_audit_engine` | 校验四个输出面与 `group_design seed` 是否边界正确、模板一致、下游可消费且无越权 | `convergence_report`、`writeback_patch_set`、`blocking_note` | 四个输出面与 seed 草案产出后、写回前必须触发 |
| `supervision_council_engine` | 在 canonical 输出首次落盘后，读取项目根 `team.yaml` 的 `roles.supervision` 配置，按 shared `council-runtime` 与 `master-check` 风格规则解析 reviewer、分发 subagents、汇流 findings，并对命中真源文件做最小必要优化 | `supervision_runtime_decision`、`supervision_reviewer_list`、`supervision_report`、`supervision_patch_set`、`supervision_refine_note` | `team.yaml.enabled == true` 且当前阶段命中 `roles.supervision` 时评估；当 `runtime_policy.use_subagents_by_default == true` 且 reviewer 可稳定解析时强触发 |

硬规则：

1. `global_style / type_bible / group_type / director_intent / group_design_distill / convergence_audit` 是当前 `SKILL.md` 的内部业务节点，不是外置真源。
2. `supervision_council_engine` 是阶段末端 shared runtime hook，不是新的业务生成主链；它只能围绕已落盘的 canonical 文件给出会审与 patch 建议。
3. 任何能力面都不得绕过父 skill 直接写 canonical Markdown 或 shared episode root；监制 subagents 只能产出局部 findings / patch 建议，最终写回仍归主 agent。
4. 若未来继续细化 `2-Global`，必须直接扩写本 `SKILL.md` 的思行网络、seed 合同、监制 refine 合同与模板合同，不得重新长出外置导演组平行真源。

## Topology Contract (Mandatory)

### Topology Fit

本技能采用 `串行前提锁定 + 项目级双链并行 + 分组级双链并行 + 依赖汇流` 的混合思行网络：

1. 串行主干：
   - 锁输入
   - 判阶段 readiness
   - 抽项目不变量
2. 项目级双链并行：
   - `全局风格`
   - `全集类型元素`
3. 分组级双链并行：
   - `分组类型元素`
   - `导演意图预解构`
4. 依赖汇流：
   - `分组类型元素` 必须继承 `全集类型元素` 的项目级类型总则，不得直接从分组正文另起类型总线
   - `导演意图` 的最终定稿必须等待 `全局风格 + 全集类型元素 + 分组类型元素` 的稳定约束
5. 最终收束：
   - Markdown 字段确认
   - JSON 提取与组壳写回
   - 模板与长度窗校验
   - 边界审计
   - 写回四份 Markdown 与 shared episode root
   - 回接 `3-Detail`

### Ordered / Unordered Rules

- `N1 -> N2` 固定串行。
- `N3A-GLOBAL-STYLE + N3B-TYPE-BIBLE + N3D-DIRECTOR-PREP` 默认并发。
- `N3C-GROUP-TYPE-PROTOCOL` 必须等待 `N3B-TYPE-BIBLE` 至少形成 project-level type bible 后再定稿；允许先做组级草案，但不得先写 canonical 字段。
- `N4-CONSTRAINT-CONVERGENCE` 必须等待 `N3A/N3B/N3C` 三个约束面稳定。
- `N5-DIRECTOR-FINALIZE` 必须等待 `N4` 与 `N3D` 同时通过；导演意图可预解构，但最终写回必须服从风格、全集类型与分组类型三层约束。
- `N6 -> N7 -> N8 -> N9 -> N10` 固定串行。
- 若用户显式只要求其中一份产物，只命中对应能力链，不补空路径。

## Thinking-Action Node Contract (Mandatory)

每个思行节点至少要定义以下字段：

| slot | 要求 |
| --- | --- |
| `node_id` | 稳定节点标识 |
| `objective` | 该节点要解决的判断/动作目标 |
| `inputs` | 进入该节点的输入与依赖 |
| `actions` | 该节点真正执行的动作 |
| `evidence` | 该节点留下的证据、产物或验证结果 |
| `route_out` | 成功、失败、分支时分别流向何处 |
| `gate` | 是否允许进入最终汇流 |

对于 `2-Global` 当前的“单技能生成 + 阶段末端监制强化”模式，各节点还必须显式回答以下执行语义：

| slot | 要求 |
| --- | --- |
| `decision_lock` | 该节点锁定什么决策，例如 `project_vs_group_boundary`、`md_field_anchor`、`team_runtime_enabled`、`supervision_reviewer_resolution` |
| `dispatch_contract` | 该节点是否会启动 subagents；若会，必须写明 reviewer 来源、owner、是否允许降级 |
| `write_scope` | 该节点允许生成哪些 patch / note，禁止直接写哪些 canonical |
| `blocker_rule` | 该节点在什么条件下必须阻塞，而不是继续推断 |
| `reentry_rule` | 审计失败、team 配置变化或会审后返工时，应从哪个节点重新进入 |

### Node Semantics (Mandatory)

| node_id | decision_lock | dispatch_contract | write_scope | blocker_rule | reentry_rule |
| --- | --- | --- | --- | --- | --- |
| `N1-INPUT-GATE` | `stage_scope == 2-Global`、`required_inputs_present` | 不启动 subagents | 只允许 `input_lock_note + missing_input_report` | 缺 `north_star / init_handoff / 第N集分组正文` 任一关键输入时必须阻塞 | 缺口补齐后回 `N1` |
| `N2-INVARIANT-LOCK` | `project_vs_group_boundary`、`forbidden_overreach_set` | 不启动 subagents | 只允许 `invariant_brief + branch_scope_plan + boundary_note` | 项目级/组级边界未拆开、或仍混入旧输出真源时必须阻塞 | 上游输入或边界定义变化回 `N2` |
| `N3A-GLOBAL-STYLE` | `global_style_baseline` | 不启动 subagents | 只允许 `global_style_plan / patch / note`，不得提前写 shared root | 风格仍污染到具体镜头/颜色/材质/对象层时必须返工 | 风格基线或上游不变量变化回 `N3A` |
| `N3B-TYPE-BIBLE` | `project_type_bible` | 不启动 subagents | 只允许 `type_bible_plan / patch / note`，不得混写组级打法 | 项目级类型总则未锁或与当前组打法混写时必须返工 | 类型总则变化回 `N3B` |
| `N3C-GROUP-TYPE-PROTOCOL` | `group_type_inheritance` | 不启动 subagents | 只允许 `group_type_plan / patch / note`，不得改写项目级类型总则 | 未显式继承 `全集类型元素.md`、或未按 `第N集/【x-x-x】` 组织时必须返工 | `N3B` 或组正文变化后回 `N3C` |
| `N3D-DIRECTOR-PREP` | `director_focus_map`、`detail_amplification_candidates` | 不启动 subagents | 只允许 `director_intent_plan / note`，禁止提前定稿 `导演意图` 字段 | 若把预解构写成最终口号或失去后续受约束空间，必须返工 | 组任务变化回 `N3D` |
| `N4-CONSTRAINT-CONVERGENCE` | `md_field_anchor`、`constraint_bridge_locked` | 不启动 subagents | 只允许 `constraint_bridge_note + md_field_anchor_note + detail_execution_bridge` | `全局风格 / 类型元素` 字段未在 Markdown 定稿，或导演意图仍未受约束时必须阻塞 | 任一上游链变化回 `N4` |
| `N5-DIRECTOR-FINALIZE` | `director_intent_ready_for_writeback` | 不启动 subagents | 允许 `director_intent_patch / report`，禁止跳过 `N6/N7` 直接终结 | 参考桥段、具像化表述或 detail 落地指令不足时必须返工 | `N3D/N4` 变化后回 `N5` |
| `N6-GROUP-DESIGN-DISTILL` | `seed_fields_locked`、`fixed_switching_count` | 不启动 subagents | 允许 `group_design_seed_patch + episode_seed_patch + switching_rationale_note`，禁止发明 shot-level `分镜明细[]` | Markdown 字段未定稿、`剧本正文` 被摘要化、或 `分镜切换` 未完成媒介/平台/类型密度裁定时必须阻塞 | 上游字段或命中组变化回 `N6` |
| `N7-CONVERGENCE-AUDIT` | `writeback_ready` | 不启动 subagents | 只允许 `convergence_report + writeback_patch_set` | 模板一致性、字段引用、长度窗、越权或完整性任一失败时必须阻塞 | Fail 回目标节点 `N3A/N3B/N3C/N5/N6` |
| `N8-WRITEBACK-CANONICAL` | `first_writeback_done`、`output_target_set` | 不启动 subagents | 允许首次写回 `全局风格.md / 导演意图.md / 全集类型元素.md / 分组类型元素.md / 3-Detail/第N集.json`，不允许扩写无关文件 | 任一 canonical 文件路径不明或 patch provenance 不全时必须阻塞 | 写回目标或 patch 集变化回 `N8` |
| `N9-SUPERVISION-SUBAGENT-REFINE` | `team_runtime_enabled`、`supervision_reviewer_resolution`、`supervision_mode` | 若 `team.yaml.enabled == true` 且当前阶段命中 `roles.supervision`，必须先读 `team.yaml` 与 shared `council-runtime`；当 `runtime_policy.use_subagents_by_default == true` 且 reviewer 为 `1-4` 个时，默认真实启动 subagents，一 reviewer skill 对应一个 subagent；仅在环境不可用、上层策略阻断或用户显式禁止 subagents 时允许降级 | 只允许 `supervision_runtime_decision + supervision_report + supervision_patch_set + supervision_refine_note`，并只 patch 本轮命中的 canonical 文件；不得创建平行评审真源 | 当 `team.yaml.enabled == true`、`roles.supervision.enabled == true` 且 reviewer 既不能从 `roles.supervision.members / team_setup.shared_agents / roles.supervision.source_skill_refs` 稳定解析，也无法基于 `focus + target_type` 安全补选时必须阻塞；若仅是 subagents 不可用，可按 shared runtime 规则降级并显式报告 | team 配置变化、首次写回内容变化或会审指出重大问题时回 `N3A/N3B/N3C/N5/N6/N8`，随后重跑 `N9` |
| `N10-FINAL-HANDOFF` | `post_supervision_closure`、`next_stage_truth` | 不启动 subagents；只汇流既有 findings | 允许输出 `handoff_note + closure_triad + supervision_summary`，禁止再改业务范围 | 若会审结论未汇流、下一阶段入口不唯一或仍有未声明 blocker，不得结案 | 若闭环不完整回 `N7/N9` |

## Thinking-Action Node Network

| node_id | 对应 Step | 聚焦字段 | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N1-INPUT-GATE` | S1 | `FIELD-GLOBAL-01` `FIELD-GLOBAL-02` | 锁定当前确属 `2-Global` 且输入齐备 | 读取 `north_star / init_handoff / 第N集分组正文`，确认阶段边界与文件存在性 | `input_lock_note`、缺口列表 | pass -> `N2`；fail -> 结束并返回 `report` | 输入与阶段边界达标后才可继续 |
| `N2-INVARIANT-LOCK` | S2 | `FIELD-GLOBAL-02` `FIELD-GLOBAL-03` | 抽出项目级不变量、全集类型边界与当前集组级范围 | 提取题材边界、观众合同、风格基线、全集类型走廊、组级范围、禁止越权项，并标记哪些属于项目级稳定项、哪些只属于当前集/当前组 | `invariant_brief`、`branch_scope_plan`、`project_vs_group_boundary_note` | pass -> `N3A/N3B/N3D`；冲突 -> 回 `S1/S2` | 不变量明确、项目级/组级边界拆开后才可并发 |
| `N3A-GLOBAL-STYLE` | S3-S4 | `FIELD-GLOBAL-04` | 形成项目级全局风格底座，并确认它作为 AIGC 生图/生视频统一风格前缀时对 `3-Detail/5-Image/6-Video` 都具有可实现指导意义 | 运行全局风格细化步骤，先锁媒介属性、渲染技术栈、美学范式与全局控制轴；若 `team.yaml` 已启用，则把 team lineup 转译为“参照 XXX 的 XXX”式视觉锚点与 AIGC 可执行构词；再经过无污染过滤生成候选比较、禁区、继承约束、最佳示例参照与统一风格前缀，并先在 Markdown 中定稿字段标题 `全局风格` | `global_style_plan`、`global_style_patch`、`style_note`、`style_reference_note`、`team_style_anchor_note` | pass -> `N4`；fail -> 回 `S3/S4` | 项目级风格不得 episode 化；最终字段不得被具体镜头/景别/对象污染，也不能只停留在抽象形容词 |
| `N3B-TYPE-BIBLE` | S5 | `FIELD-GLOBAL-05` | 形成 `全集类型元素.md` 的项目级类型总则，锁定观众合同、主副类型、混合公式、共用禁区与下游读取规则 | 从 `north_star / init_handoff / 第N集分组正文` 中抽取项目级类型不变量，拆开“全集类型走廊”和“当前组打法”，写出类型裁决依据、参考桥段、可迁移处理逻辑、不可迁移误区，并明确 `分组类型元素.md` 必须继承哪些规则 | `type_bible_plan`、`type_bible_patch`、`project_type_note`、`type_reference_note` | pass -> `N3C/N4`；fail -> 回 `S5` | `全集类型元素.md` 只能写项目级类型总则，不得混入单组临场打法；旧 `类型元素.md` 不得作为新输出 |
| `N3C-GROUP-TYPE-PROTOCOL` | S6 | `FIELD-GLOBAL-05` | 形成 `分组类型元素.md` 的组级类型协议，并确认它能转译成后续 detail 的导演动作 | 继承 `全集类型元素.md`，按 `第N集 -> 【x-x-x】` 为每组生成主副类型、冲突引擎、揭示策略、节奏/表演/镜头倾向、参考桥段、具像化表述、wrong-genre 负例、fallback floor，并在命中组用字段标题 `类型元素` 定稿 | `group_type_plan`、`group_type_patch`、`group_type_note`、`group_type_negative_map` | pass -> `N4`；fail -> 回 `S6` 或 `N3B` | 组级类型必须可提取、可执行、可约束下游；不得改写项目级类型总则 |
| `N3D-DIRECTOR-PREP` | S7 | `FIELD-GLOBAL-06` | 提前解构当前集各组的导演任务，并预判哪些判断值得在 detail 被放大 | 逐个读取 `【x-x-x】`，提取剧情任务、关注焦点、情绪推进、空间压力、候选参考桥段、表演抓手与下游放大抓手；只产出预解构，不写最终 `导演意图` 字段 | `director_intent_plan`、`director_note`、`director_reference_candidates`、`director_focus_map` | pass -> 等待 `N4` 后进 `N5`；fail -> 回 `S7` | 仅允许预解构，不得提前定稿；必须保留可被风格/类型约束修正的空间 |
| `N4-CONSTRAINT-CONVERGENCE` | S8 | `FIELD-GLOBAL-04` `FIELD-GLOBAL-05` | 汇流风格、全集类型与分组类型约束，确认四份 Markdown 中供 JSON 直接引用的字段与位置 | 对齐 `全局风格.md` 的风格前缀、`全集类型元素.md` 的项目级类型总则、`分组类型元素.md` 的组级类型字段、禁区、无污染过滤结果、参考桥段与下游继承要求；检查 `全局风格 / 类型元素` 字段已在 Markdown 中定稿，并形成导演意图必须服从的约束桥 | `constraint_bridge_note`、`type_inheritance_note`、`detail_execution_bridge`、`md_field_anchor_note` | pass -> `N5`；fail -> 回 `N3A/N3B/N3C` | 风格、全集类型与分组类型必须先稳定；项目级规则和组级打法不得互相污染 |
| `N5-DIRECTOR-FINALIZE` | S9 | `FIELD-GLOBAL-07` | 在约束已稳定的前提下完成导演意图 patch，并把参考锚点翻译成当前组的可执行指令 | 将组级预解构翻译成 `导演意图.md` 的 `第N集/【x-x-x】` patch，补齐参考桥段、具像化表述、detail 放大方向，并先在组内定稿字段标题 `导演意图` | `director_intent_patch`、`director_report`、`director_implementation_note` | pass -> `N6`；fail -> 回 `N3D/N4` | 每组必须可被 `3-Detail` 直接消费，不能只有口号 |
| `N6-GROUP-DESIGN-DISTILL` | S10 | `FIELD-GLOBAL-08` | 把四份 Markdown 中已确认字段、固定分镜切换与完整剧本正文直接提取到 shared episode root 的组级壳，并控制长度窗 | 按 `group_design_seed_contract` 对照字段标题，直接提取 `全局风格.md` 的项目级 `全局风格`、`分组类型元素.md` 的命中组 `类型元素`、`导演意图.md` 的命中组 `导演意图`；同步核对该组 `类型元素` 是否继承 `全集类型元素.md`；再基于 `总时长 + 媒介形态 + 平台形态 + 类型元素 + 导演意图 + 组正文` 直接裁定 `分镜切换`，先判定当前 `rhythm_density_profile`：漫画/恐怖漫画默认以面板密度计数，24 秒左右分镜组通常不得低于 4 镜，常规压迫组 4-6 镜，强峰值/信息反转组 5-7 镜；短剧/竖屏短剧默认以高信息递送密度计数，24 秒左右分镜组通常不得低于 5 镜，钩子/反转/冲突升级组通常 6-9 镜；长剧/电影可按场面调度保留更长镜头，但必须说明张力如何不丢失。注意“快节奏”不是一律快速剪，恐怖/悬疑可以慢停顿，但必须保持高信息密度；低于下限必须在 `switching_rationale_note` 写明不可拆原因；并以内化 former `镜花/1-切换` 的口径写出 `switching_rationale_note`；最后将命中组全文去掉组号标题后完整写入 `分镜组列表[].剧本正文`，生成 `episode_seed_patch` | `group_design_seed_plan`、`group_design_seed_patch`、`episode_seed_patch`、`switching_rationale_note`、`type_inheritance_check`、`medium_density_check`、`rhythm_density_profile` | pass -> `N7`；fail -> 回 `N3A/N3B/N3C/N5` | 三个 seed 字段必须来自已确认 Markdown，`类型元素` 必须继承全集总则，`分镜切换` 必须是组级固定数值并满足媒介/平台/类型密度，且 `剧本正文` 必须是完整组正文 |
| `N7-CONVERGENCE-AUDIT` | S11 | `FIELD-GLOBAL-09` | 检查模板一致性、字段引用位置、剧本正文完整性、长度窗、边界正确性、媒介密度、参考锚点清晰度与下游 handoff | 运行模板对齐、项目级/组级边界检查、JSON 字段位置检查、`group_design` 长度窗检查、`分镜切换` 媒介密度检查、越权检查、空话审计、reference/bridge 审计、剧本正文完整性审计与可实现性审计 | `convergence_report`、`writeback_patch_set` | pass -> `N8`；fail -> 回目标节点返工 | 通过后才能写回 |
| `N8-WRITEBACK-CANONICAL` | S12 | `FIELD-GLOBAL-10` | 统一完成 canonical 首次写回，为后续监制会审提供真实目标文件 | 先按增量策略写回四份长文本真源，再将已确认字段与组全文提取入 `第N集.json` 的分镜组壳，形成本轮 output target set | 四份 canonical 文档、shared root、`first_writeback_note` | pass -> `N9`；fail -> 回 `N7` | 仅父 skill 拥有首次写回权 |
| `N9-SUPERVISION-SUBAGENT-REFINE` | S13 | `FIELD-GLOBAL-11` | 在输出相关真源文件已存在的前提下，根据项目根 `team.yaml` 的监制配置触发 stage-end 会审与最小必要优化 | 读取 `team.yaml` 的 `roles.supervision`、`team_setup.shared_agents`、`runtime_policy`、`focus` 与 shared `council-runtime`；按 `master-check-team / master-check` 风格规则解析 reviewer、判定 `single-reviewer / parallel-council / serial-refine / independent-only`；若满足条件则真实启动 subagents，对 `全局风格.md / 导演意图.md / 全集类型元素.md / 分组类型元素.md / 3-Detail/第N集.json` 做局部会审，并由主 agent 汇流后回写最小 patch | `supervision_runtime_decision`、`supervision_reviewer_list`、`supervision_report`、`supervision_patch_set`、`supervision_refine_note` | pass -> `N10`；fail -> 回 `N3A/N3B/N3C/N5/N6/N8` | reviewer 来源、模式裁决与是否降级都必须可追溯；最终写回仍归主 agent |
| `N10-FINAL-HANDOFF` | S14 | `FIELD-GLOBAL-12` | 汇流 stage-end 会审结果，输出下一入口与闭环 triad | 汇总业务生成链与监制 refine 链，输出 `root cause / immediate fix / systemic prevention`、`supervision_summary` 与固定下一入口 `3-Detail` | `handoff_note`、`closure_triad`、`supervision_summary` | Final | 只有本节点允许结案 |

## Capability Chain Detail (Mandatory)

### 全局风格链

| branch_step | 要从哪些方面着手 | 具体动作 | 输出要求 |
| --- | --- | --- | --- |
| `GS1` | 媒介属性与渲染技术栈 | 从 `north_star / init_handoff` 判断整片是更偏真人、2D、3D 还是混合媒介，并锁定对应渲染技术栈 | 不允许只写“高级感”“电影感” |
| `GS2` | 摄影基调与画面制式 | 选择最能服务题材与观众合同的摄影基调，明确照明、反差、颗粒、反射、皮肤与材质呈现这些总体属性，并说明它为什么属于项目级稳定项 | 必须聚焦摄影层，而不是泛美学概述 |
| `GS3` | 全局控制轴 | 内部判断观演距离、主客观模式、炫技倾向、运镜/转场偏置、光影戏剧性、色彩振幅、空间气压分层与视觉回声密度 | 这些控制轴用于约束后续判断，不应直接污染最终字段 |
| `GS4` | 无污染过滤 | 将候选描述中过于具体的颜色词、材质词、构图术语、焦段/推拉摇移与对象内容清除，改写为媒介、渲染、光学或美学层术语 | 最终字段默认只描述 HOW 与 WHAT STYLE，不描述 WHAT CONTENT |
| `GS5` | team 锚点与摄影语料组织参照 | 若 `team.yaml` 启用，则优先把 team 成员转译成“参照 XXX 的 XXX”式摄影锚点，并补全对应的成熟摄影表达样本、无污染改写范例与 `Midjourney` 类工具友好的前缀顺序 | 必须写清“参照哪一段、借的是哪种摄影处理逻辑”，不能只报作品名，也不能只有 team 名单不下钻 |
| `GS6` | AIGC 统一风格前缀 | 把风格判断收束为可直接作为 AIGC 生图/生视频统一前缀的一段话，并在 Markdown 用字段标题 `全局风格` 定稿；若需要工具投影，只能从同一句 core prefix 派生 | 可在原字数窗基础上适度放宽，但必须保持单段、稳定、可直接提取 |
| `GS7` | 对下游的继承边界 | 检查该风格是否真能被 `3-Detail/4-Design/5-Image/6-Video` 无污染继承，并明确哪些只作为节点判断、哪些可写进最终字段 | 必须对后续阶段具有可实现指导意义 |
| `GS8` | 稳定禁区与允许自由度 | 写清必须禁止的表达、谨慎使用的表达与可留给下游变化的自由度 | 必须同时给正向锚点和负向禁区 |
| `GS9` | 候选比较与增量 patch | 比较多个风格路径，只保留主路径，并生成项目级 patch 与取舍说明 | 不得并列塞进互相冲突的风格方向 |

### 全集类型元素链

| branch_step | 要从哪些方面着手 | 具体动作 | 输出要求 |
| --- | --- | --- | --- |
| `TB1` | 项目级观众合同 | 从 `north_star / init_handoff / story-source-manifest` 抽出观众为什么要看、期待怎样的类型体验、最终应得到哪种情绪兑现 | 不得只堆题材标签；必须写成项目级长期合同 |
| `TB2` | 主类型、副类型与混合公式 | 判断主类型、副类型、辅助类型的权重与先后关系，写清“谁主导、谁服务、何时转向” | 不允许多个类型平铺并列；必须有主次与转向逻辑 |
| `TB3` | 全集揭示语法与节奏母法 | 抽取整集/全集共同遵守的信息揭示、节奏递进、恐怖/喜剧/悬疑/动作等类型递送规律 | 必须能约束所有分组，不得只描述当前一个组 |
| `TB4` | 参考桥段与类型运作逻辑 | 选择适合项目级类型的成熟桥段或结构样本，说明借鉴的是类型运作、信息递送或情绪兑现机制 | 只能借处理逻辑，不能搬运剧情或模仿特定作者风格 |
| `TB5` | 共用禁区与下游读取规则 | 写清 wrong-genre、禁用 register、下游必须继承的类型边界，以及 `分组类型元素.md` 应如何继承 | 必须给 `3-Detail / 4-Design / 5-Image` 可检查的规则 |
| `TB6` | `全集类型元素.md` 定稿 | 将项目级类型总则写入 `全集类型元素.md`，并明确旧 `2-Global/类型元素.md` 不再作为新输出 | 不得混入组级打法、分镜节奏细节或当前集局部情绪 |

### 分组类型元素链

| branch_step | 要从哪些方面着手 | 具体动作 | 输出要求 |
| --- | --- | --- | --- |
| `GT1` | 继承全集类型总则 | 读取 `全集类型元素.md`，为当前集/当前组标出必须继承的观众合同、主副类型边界与共用禁区 | 未继承全集总则不得写组级字段 |
| `GT2` | 分镜组范围与组级任务 | 以 `第N集 -> 【x-x-x】` 为最小单元，从当前组冲突、信息任务与情绪任务中提炼观众在本组该期待什么 | 不得只复述剧情或只写题材标签 |
| `GT3` | 当前组主副类型权重 | 判断当前组主类型、副类型、混合公式与权重，说明本组和全集总则的差异化位置 | 必须写清主次、转向点和局部功能 |
| `GT4` | 冲突引擎、揭示策略与节奏递送 | 提炼当前组如何制造 tension、何时揭示、如何递送信息、如何控制节奏与表演强度 | 必须能指导下游镜头节奏和分镜密度 |
| `GT5` | 参考桥段与组级类型样本 | 为当前组类型组合寻找最贴切的作品或桥段样本，提炼其类型运作方式而非搬运剧情 | 必须说明参照桥段对当前组的可借鉴点 |
| `GT6` | 具像化导演打法 | 把当前组类型判断翻译成镜头组织、表演强弱、节奏推进、情绪传递、信息显隐与转场方式 | 不能停留在类型名词层 |
| `GT7` | 字段定稿与对 `3-Detail` 的落地指导 | 把当前组类型协议压成 detail 可执行的一段话，并在 Markdown 用字段标题 `类型元素` 定稿 | 必须短、准、可直接提取进 `组间设计.类型元素` |
| `GT8` | 错误类型负例、保底策略与增量 patch | 指出 wrong-genre 信号、禁用 register、fallback floor；多个候选并存时只保留主路径并记录未采纳方向 | 下游必须能据此判断“不能怎么做”；不得把互斥打法同时写进真源 |

### 导演意图链

| branch_step | 要从哪些方面着手 | 具体动作 | 输出要求 |
| --- | --- | --- | --- |
| `DI1` | 组级边界与剧情任务 | 逐个读取 `【x-x-x】`，确认每组真正承担的叙事任务 | 不得只复述剧情梗概 |
| `DI2` | 观众注意焦点 | 判断“画面里最该看见什么”，而不是“能看见什么” | 必须有单一主焦点 |
| `DI3` | 信息推进与情绪转弯 | 说明本组把什么信息推到观众面前，角色状态如何发生变化 | 必须体现动态推进 |
| `DI4` | 参考作品桥段与处理样本 | 为当前组寻找最接近的作品或桥段样本，借其镜头组织、信息揭示或情绪转弯方式 | 必须说清借鉴的是处理逻辑，不是照抄剧情 |
| `DI5` | 表演抓手与空间压力 | 写明表演重心、空间调度、气氛压力怎样服务组任务 | 不得只写“营造氛围” |
| `DI6` | 节奏与镜头处理方向 | 在风格/类型约束下判断本组节奏密度、镜头呼吸和强调方式 | 必须兼容项目级风格与类型协议 |
| `DI7` | 具像化表述与 detail 落地指令 | 把导演意图翻译成 `3-Detail` 可继续展开的镜头、表演、调度、节奏和视觉强调语言 | 必须形成可执行而非抽象的指导语 |
| `DI8` | 下游放大方向与禁用方向 | 告诉 `3-Detail` 最值得放大什么，并标出不应滑向哪里 | 必须形成直接可消费指令 |
| `DI9` | 字段定稿与局部 patch | 多个处理路径并存时只保留主路径，局部写回当前集命中组，并在组内用字段标题 `导演意图` 定稿一段话 | 不得重写未命中的集或组 |

## One-Shot Output Contract (Mandatory)

`2-Global` 的一次性输出不是多个平行草案，而是同一 bundle 内的六类结果：

1. `projects/aigc/<项目名>/2-Global/全局风格.md`
   - 项目级风格底座唯一真源
2. `projects/aigc/<项目名>/2-Global/导演意图.md`
   - 按集、按组沉淀的导演构思唯一真源
3. `projects/aigc/<项目名>/2-Global/全集类型元素.md` 与 `projects/aigc/<项目名>/2-Global/分组类型元素.md`
   - 前者持有项目级类型总则，后者持有按集、按组组织的类型化导演协议；`类型元素.md` 仅允许作为旧项目迁移输入 fallback
4. `projects/aigc/<项目名>/3-Detail/第N集.json`
   - shared episode root；本阶段写 `分镜组ID / 总时长 / 剧本正文 / 组间设计 / 分镜切换 / 分镜明细=[]` 的分镜组壳与相关 metadata
5. `supervision runtime report`
   - 若项目根 `team.yaml` 启用且当前阶段命中 `roles.supervision`，必须给出 `reviewer_source / reviewers / mode / used_subagents / patched_targets / key_findings`
   - 若未启用或降级，也必须显式说明原因
6. `closure triad + handoff note`
   - 说明 `root cause location / immediate fix / systemic prevention fix`
   - 给出下一入口固定为 `3-Detail`

## Canonical Output Governance (Mandatory)

1. `全局风格.md` 只能写项目级稳定总则；`全集类型元素.md` 只能写项目级类型总则；`分组类型元素.md` 必须按 `第N集 -> 【x-x-x】` 写组级类型判断，`类型元素.md` 只允许作为旧项目迁移输入 fallback。
2. `全局风格.md` 的 canonical 字段必须服务“统一画面风格锚定”，不是导演阐释、人物命运总结或剧情摘要；叙事信息若确有必要，只能以内化后的视觉倾向、空间气压、时间处理方式出现。
3. 若项目根 `team.yaml` 启用且当前阶段命中 team 模式，`全局风格.md` 必须留下可识别但不脏乱的 team 痕迹：优先使用“参照《作品》的处理 / 参照某导演的某类组织 / 参照某摄影的某类光影与空间”这类句法，并补出对应 AIGC 构词。
4. `导演意图.md` 只写按集、按组的导演构思，并在命中组内用字段标题 `导演意图` 定稿，不得冒充项目级风格总则。
5. 四份文档都由当前 skill 聚合写回，不存在平行导演组 writeback owner。
6. shared episode root 的 `剧本正文 + 组间设计 + 分镜切换` 也由当前 skill 聚合写入，但本阶段不得发明 shot-level `分镜明细[]`。
7. JSON 写回时，`组间设计.全局风格 / 类型元素 / 导演意图` 只能直接引用 Markdown 中同名字段，不得临场改写或另起第二套摘要。
8. 若在 `全局风格.md` 中提供 `Midjourney`、`即梦`、`nano-banana` 等工具投影建议，它们只能是 canonical core prefix 的派生组织方式，不得把工具参数、纵横比参数或单工具专属魔法词写进 JSON 提取字段。
9. 现有文档或 shared root 存在时，只允许增量更新命中章节与命中组，不得整稿抹平历史内容。
10. 对 `3-Detail` 的第一结构化 handoff 以 shared episode root 为准；`2-Global/*.md` 仍保留为长文本解释载体。
11. 若 `team.yaml` 启用 `roles.supervision`，stage-end 会审只能围绕本轮已写出的 canonical 文件给 patch 建议；不得生成新的“监制稿”“评审稿”或旁路总稿。
12. `supervision_report / supervision_patch_set` 只属于内部运行时侧车；最终 canonical 改动仍必须回写到既有五个真源文件。

## Subagents 监制强化（Mandatory）

`2-Global` 在阶段末端必须兼容 `master-check-team` / `master-check` 的 reviewer runtime 机制，但采用当前阶段专用的 `roles.supervision` 优先路由。

### 触发时机

1. 先完成 `N8-WRITEBACK-CANONICAL`，确保输出相关真源文件已经存在。
2. 再读取 `projects/aigc/<项目名>/team.yaml`。
3. 若 `team.yaml.enabled != true`、`roles.supervision.enabled != true`、或当前阶段不在 `roles.supervision.operates_on`，跳过 `N9` 的 reviewer 分发，只保留 `skip_reason`。
4. 若命中 `roles.supervision`，必须围绕本轮 output target set 触发一次 stage-end refine。

### reviewer 解析顺序

对于 `2-Global`，reviewer 解析优先级固定为：

1. `roles.supervision.members`
2. `team_setup.shared_agents` 中与当前阶段输出相关的 `.agents/skills/team/` reviewer
3. `roles.supervision.source_skill_refs`
4. 基于 `roles.supervision.focus + target_type` 的安全补选

解析规则：

- 若条目已是 `.agents/skills/team/**/SKILL.md`，直接作为 reviewer skill。
- 若条目指向 `.agents/skills/aigc/**/SKILL.md` 这类阶段 skill，只把它视为领域提示，不得直接拿阶段 skill 充当 reviewer；必须再映射到 `.agents/skills/team/` 下的 reviewer skill。
- `roles.supervision.source_skill_refs` 主要用于确认当前阶段的适配域，不替代 reviewer 真源。
- 当显式 reviewer 不足时，才允许基于 `focus + target_type` 补选 1-2 个 reviewer；补选必须显式说明是推断，不是 `team.yaml` 的显式声明。
- `2-Global` 的输出默认属于“文本/导演协议/组级 JSON handoff”类型，补选时优先：
  - 导演组 1 位
  - 若 `focus` 更偏人物关系、剧情执行或可拍性，补编剧组 1 位
  - 若 `focus` 更偏风格纯度、画面组织或整体气质，补摄影组或设计组 1 位
- reviewer 总数必须限制在 `1-4` 个。

### 模式裁决

1. 若 reviewer 为 1 个，默认 `single-reviewer`，仍优先真实启动 1 个 subagent。
2. 若 `runtime_policy.use_subagents_by_default == true` 且 reviewer 为 `2-4` 个，优先 `parallel-council`。
3. 若目标明显需要链式 refine，再改为 `serial-refine`。
4. 若目标不适合主 agent 直接改写，才允许 `independent-only`。

### Subagent Dispatch Gate

- `2-Global` 的默认语义不是“主 agent 模拟监制团”，而是“一个 reviewer skill 对应一个 subagent，由主 agent 汇流并最终 patch”。
- 只要命中 reviewer skill，且环境真实支持 subagents、也不存在更高优先级策略阻断，就应实际启动 subagents。
- 仅在以下情况允许降级：
  - 当前环境无法真实使用 subagents
  - 更高优先级策略明确阻断 subagent 调度
  - 用户显式要求不要启用 subagents
- 降级时必须在 `supervision_runtime_decision` 中写明降级原因与替代执行方式。

### 输出与优化范围

- 会审目标固定为本轮命中的：
  - `projects/aigc/<项目名>/2-Global/全局风格.md`
  - `projects/aigc/<项目名>/2-Global/导演意图.md`
  - `projects/aigc/<项目名>/2-Global/全集类型元素.md`
  - `projects/aigc/<项目名>/2-Global/分组类型元素.md`
  - `projects/aigc/<项目名>/3-Detail/第N集.json`
- 每个 subagent 只负责局部判断和建议，不拥有最终写回权。
- 主 agent 必须汇流为：
  - `共识`
  - `关键分歧`
  - `建议采用方案`
  - `少数派高价值提醒`
- 若 `output` 语义允许优化，则由主 agent 直接对上述真源文件做最小必要 patch。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-GLOBAL-01` | 阶段定位 | 明确 `2-Global` 是 `1-Planning` 与 `3-Detail` 之间的导演前置全局合同阶段 | S1 | 边界清晰度 | FAIL-GLOBAL-01 |
| `FIELD-GLOBAL-02` | 输入与不变量 | 锁定项目级硬证据、组级范围和禁止越权项 | S2 | 输入真源一致性 | FAIL-GLOBAL-02 |
| `FIELD-GLOBAL-03` | 并发拓扑 | 明确全局风格、全集类型、分组类型、导演意图预解构之间的并发、依赖汇流与父 skill 写回边界 | S3 | 编排可执行性 | FAIL-GLOBAL-03 |
| `FIELD-GLOBAL-04` | 全局风格真源 | 项目级风格底座稳定，具备媒介属性、渲染技术栈、摄影级总体属性、全局控制轴、AIGC 统一风格前缀、跨工具组织建议、team 模式下的参照句法与 AIGC 摄影构词、参考桥段、禁区与下游继承；最终字段保持无污染底层摄影风格协议 | S4 | 项目级稳定性 | FAIL-GLOBAL-04 |
| `FIELD-GLOBAL-05` | 类型元素真源 | `全集类型元素.md` 持有项目级观众合同、主副类型、混合公式、共用禁区与下游读取规则；`分组类型元素.md` 继承全集总则并按 `第N集 -> 【x-x-x】` 组织，每组具备主副类型、参考桥段、具像化导演打法、detail 落地导向与错误类型禁区；`类型元素.md` 不参与新输出真源 | S5-S6 | 类型化有效性 | FAIL-GLOBAL-05 |
| `FIELD-GLOBAL-06` | 导演意图预解构 | 当前集组级任务、关注焦点、情绪推进与空间压力被正确解构 | S7 | 组级分析精度 | FAIL-GLOBAL-06 |
| `FIELD-GLOBAL-07` | 导演意图写回 | `导演意图.md` 当前集命中组的 patch 具体、可消费、具备参考桥段与具像化落地指令、不过界，并在字段标题 `导演意图` 定稿组级摘要 | S9 | 下游可消费性 | FAIL-GLOBAL-07 |
| `FIELD-GLOBAL-08` | JSON 提取与组壳写回 | shared episode root 的 `剧本正文 / 全局风格 / 类型元素 / 导演意图 / 分镜切换` 已按正确字段位置写回，其中 `组间设计` 字段来自 Markdown 直接提取并满足 `220 / 50 / 100` 字符窗，`分镜切换` 来自同轮固定数值裁决，且 former `镜花/1-切换` 的 fixed-shot-count 接受逻辑已内化为 `switching_rationale_note` | S10 | 提取可消费性 | FAIL-GLOBAL-08 |
| `FIELD-GLOBAL-09` | 汇流审计 | 空话、越权、边界污染、字段错引、剧本正文摘要化、长度窗违规与依赖断裂被拦住 | S11 | 收束完整性 | FAIL-GLOBAL-09 |
| `FIELD-GLOBAL-10` | canonical 首次写回 | 四份 Markdown 与 shared root 已完成首次合法写回，且 output target set 明确 | S12 | 首次写回完整性 | FAIL-GLOBAL-10 |
| `FIELD-GLOBAL-11` | 监制会审与 refine | `team.yaml` 的 `roles.supervision` 已被解释，reviewer 选择、模式裁决、subagent 使用与会审 patch 可追溯 | S13 | stage-end refine 有效性 | FAIL-GLOBAL-11 |
| `FIELD-GLOBAL-12` | 下一阶段 handoff | 返回 triad closure、supervision summary，并固定回接 `3-Detail` 与 shared episode root | S14 | 闭环可执行性 | FAIL-GLOBAL-12 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-GLOBAL-01` | 当前是不是 `2-Global` 阶段问题 | 锁定阶段边界与上下游职责 | 把本阶段写成 `3-Detail` 或 `1-Planning` |
| `S2` | `FIELD-GLOBAL-02` | 当前轮必须先锁哪些不变量 | 写出输入清单、禁止越权项与组级范围 | 输入根或不变量漂移 |
| `S3` | `FIELD-GLOBAL-03` | 四个输出面如何并发且不打架 | 写出全局风格、全集类型、分组类型、导演意图预解构的并发拓扑、依赖和汇流门 | 只说“并发”，没写 `全集类型 -> 分组类型 -> 导演意图` 的依赖条件 |
| `S4` | `FIELD-GLOBAL-04` | 项目级风格底座到底稳定在哪，是否已经经过无污染过滤并能直接指导后续阶段 | 产出全局风格 patch、控制轴判断、参考桥段、无污染统一前缀与取舍说明 | 风格文档被某一集情绪污染、只剩抽象形容词，或最终字段混入景别/镜头/对象细节 |
| `S5` | `FIELD-GLOBAL-05` | 项目级类型总则如何约束所有分组与下游阶段 | 产出 `全集类型元素.md` patch、观众合同、主副类型、混合公式、参考桥段、共用禁区与下游读取规则 | 项目级类型只剩标签，或混入当前组临场打法 |
| `S6` | `FIELD-GLOBAL-05` | 分组类型协议如何继承全集总则并落到 detail 执行 | 产出 `分组类型元素.md` 按组 patch、参考桥段、具像化打法、负例与保底策略 | 只有类型词，没有导演打法或 detail 导向，未按组组织，或未继承全集类型总则 |
| `S7` | `FIELD-GLOBAL-06` | 当前集各组真正的导演任务是什么，哪些处理值得被 detail 放大 | 逐组预解构剧情任务、关注焦点、情绪推进、参考桥段候选与下游抓手 | 只复述剧情摘要，没有下游抓手 |
| `S8` | `FIELD-GLOBAL-04` `FIELD-GLOBAL-05` | 风格、全集类型与分组类型怎样变成导演意图约束与下游执行语言 | 形成约束桥接说明、type inheritance note 与 detail 执行桥 | 导演意图不受项目级风格/类型约束，组级类型未继承全集总则，或没有执行桥 |
| `S9` | `FIELD-GLOBAL-07` | 当前集导演构思是否足够具体，是否具备参考桥段与具像化指令 | 写入 `导演意图.md` 命中章节 patch，并在字段标题 `导演意图` 定稿组级摘要 | 只剩空泛口号，或只有参照名词没有具像化处理 |
| `S10` | `FIELD-GLOBAL-08` | Markdown 已确认字段、固定分镜切换与完整组正文能否被正确提取进 shared episode root，并保持 `220 / 50 / 100` 字符窗 | 生成 `group_design_seed_patch`、`episode_seed_patch` 与 `switching_rationale_note` | 字段错引、固定镜数缺失、剧本正文被摘要化、跨组混写、旧 `1-切换` 逻辑仍留在下游或超窗 |
| `S11` | `FIELD-GLOBAL-09` | 四份文档与 shared root 能否一起合法落盘，并被下游直接消费 | 执行模板/字段位置/剧本正文完整性/边界/长度窗/越权/空话/reference 可实现性审计 | 结构断裂、字段错位、边界污染、长度窗违规、参照失焦或越权写回 |
| `S12` | `FIELD-GLOBAL-10` | 如何完成本轮 output target set 的首次合法写回 | 写回四份 Markdown 与 shared root，并锁定会审目标集合 | canonical 文件未落盘、patch provenance 不清或目标集合不明确 |
| `S13` | `FIELD-GLOBAL-11` | team.yaml 的监制配置如何转成 reviewer 选择、subagent 分发与 stage-end 优化 | 解析 `roles.supervision`、裁决模式、启动或降级 subagents、汇流 findings 并 patch 命中真源 | `team.yaml` 已启用却未读取、reviewer 无法解析、应起 subagents 却被静默跳过，或会审输出变成第二真源 |
| `S14` | `FIELD-GLOBAL-12` | 如何证明会审结果已汇流并交给下游 | 输出 triad closure、supervision summary 与 `3-Detail` 回接说明 | 没有返工入口、会审未汇流、shared root 未落盘或下一阶段缺失 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-GLOBAL-01` | 阶段定位、上下游边界与四份真源职责明确 | FAIL-GLOBAL-01 | S1 |
| `FIELD-GLOBAL-02` | 项目级硬证据、组级范围与禁止越权项锁定 | FAIL-GLOBAL-02 | S2 |
| `FIELD-GLOBAL-03` | 全局风格、全集类型、分组类型、导演意图预解构的并发、依赖和写回权边界明确 | FAIL-GLOBAL-03 | S3 |
| `FIELD-GLOBAL-04` | `全局风格.md` 具备媒介属性、渲染技术栈、美学范式、控制轴、AIGC 统一风格前缀、参考桥段、禁区与下游继承，且最终字段无污染 | FAIL-GLOBAL-04 | S4 |
| `FIELD-GLOBAL-05` | `全集类型元素.md` 已锁项目级观众合同、主副类型、混合公式与共用禁区；`分组类型元素.md` 已继承全集总则并按组组织，且具备主副类型、参考桥段、导演打法、负例、保底策略与 detail 导向；`类型元素.md` 仅作旧项目迁移输入 fallback | FAIL-GLOBAL-05 | S5-S6 |
| `FIELD-GLOBAL-06` | 组级导演任务预解构具体且与 `【x-x-x】` 对齐 | FAIL-GLOBAL-06 | S7 |
| `FIELD-GLOBAL-07` | `导演意图.md` 当前集命中组的 patch 具体、可消费、具备参考桥段、具像化落地指令且不过界，并在字段标题 `导演意图` 定稿组级摘要 | FAIL-GLOBAL-07 | S8-S9 |
| `FIELD-GLOBAL-08` | `剧本正文 + 组间设计 + 分镜切换` 已按正确字段位置写入分镜组壳，其中三条组级上下文来自 Markdown 直接提取，且 fixed-shot-count 接受逻辑已在本阶段内化 | FAIL-GLOBAL-08 | S10 |
| `FIELD-GLOBAL-09` | 无空话、无越权、无项目级/组级污染、无字段错引、无剧本正文摘要化、无字符窗违规 | FAIL-GLOBAL-09 | S11 |
| `FIELD-GLOBAL-10` | 四份 Markdown 与 shared root 已完成首次合法写回，且会审目标集合明确 | FAIL-GLOBAL-10 | S12 |
| `FIELD-GLOBAL-11` | `team.yaml` 的监制配置、reviewer 解析、subagent 模式、降级原因与 refine patch 都可追溯 | FAIL-GLOBAL-11 | S13 |
| `FIELD-GLOBAL-12` | 返回 triad closure、supervision summary，shared root 已 seed，并固定回接 `3-Detail` | FAIL-GLOBAL-12 | S14 |

## Root-Cause Execution Contract (Mandatory)

当 `2-Global` 出现以下问题时，必须先修源层而不是补单次文案：

- `2-Global` 仍回指已退役的导演组外置 contracts
- 内部能力链只有并发口号，没有写清 `全集类型 -> 分组类型 -> 导演意图` 的依赖汇流门
- `全局风格.md` 或 `分组类型元素.md` 被写成当前集情绪杂糅稿
- `全局风格` 最终字段混入具体景别、镜头距离、构图术语、具体颜色词、具体材质词或对象级内容
- `分组类型元素.md` 没有按 `第N集/【x-x-x】` 组织，或新输出仍生成 `类型元素.md`，导致 JSON 无法按组正确引用
- `分组类型元素.md` 未显式继承 `全集类型元素.md`，导致组级打法另起类型真源
- `导演意图.md` 没有回链到 `第N集/【x-x-x】`
- `导演意图` 在风格/类型约束未稳定前就提前定稿
- 风格、类型、导演意图只剩抽象词，无法指导 `3-Detail` 的实际展开
- 只写了参考作品名，没有指出具体桥段与可借鉴的处理逻辑
- 写 JSON 时重新改写了 `全局风格 / 类型元素 / 导演意图`，而不是直接引用 Markdown 已确认字段
- `分镜切换` 没有在 `2-Global` 末段直接写成固定数值，导致 `3-Detail` 又要临场决定组级镜数
- `分镜切换` 虽已固定，但没有按媒介形态、平台形态与类型任务裁定密度，例如把漫画/恐怖漫画按影视镜头低密度处理，或把短剧/竖屏短剧按长剧场面调度密度处理，导致后续缺少声效格、停顿格、反应格、钩子格、冲突升级格和局部递进格
- former `镜花/1-切换` 的 fixed-shot-count 接受逻辑仍滞留在 `3-Detail/镜花`，导致上游/下游出现第二套切换真源
- `剧本正文` 写进 shared episode root 时只剩摘要，没有完整保留命中组正文
- `组间设计` 没有 seed 到 shared episode root，或长度窗失控
- 项目根 `team.yaml` 存在且 `roles.supervision` 对 `2-Global` 生效，但阶段输出后没有读取其配置、没有解析 reviewer、或没有按规则触发监制会审与最小必要优化
- `roles.supervision.source_skill_refs` 被直接当 reviewer 使用，导致阶段 skill 与 reviewer skill 混淆
- `runtime_policy.use_subagents_by_default == true` 且 reviewer 已稳定命中，但主 agent 仍静默跳过真实 subagents，退回本地模拟却未报告
- stage-end 会审输出生成了平行“监制稿”或旁路文件，而不是回写既有 canonical 真源
- 阶段越权在 `2-Global` 发明 shot-level `分镜明细[]`

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
  - `.agents/skills/aigc/_shared/council-runtime/module-spec.md`
  - `.agents/skills/aigc/2-Global/templates/*.template.md`
  - `.agents/skills/aigc/_shared/group_design_seed_contract.md`
  - `.agents/skills/aigc/_shared/director_episode_output.schema.json`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/SKILL.md`
  - `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-知行合一/SKILL.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `2-Global` 的单技能知行合一真源。
- 已明确全局风格、全集类型、分组类型、导演意图预解构/定稿的内部能力链与并发/汇流关系。
- 已把 `全局风格 / 全集类型元素 / 分组类型元素 / 导演意图` 的细致步骤写入同一 `SKILL.md`。
- 已把 `分组类型元素.md` 固定为按组组织的真源，把 `类型元素.md` 降级为旧项目迁移输入 fallback，并把三类字段的 Markdown -> JSON 提取位置写成唯一真源。
- 已固定 shared episode root 中 `剧本正文` 必须完整保留命中组正文，不得再写成摘要。
- 已要求四个输出面都回答 `3-Detail` 可实现性、参考作品桥段与具像化表述。
- 已明确不再依赖外置导演组 contracts。
- 已把 `输出相关真源文件后 -> 读取 team.yaml -> 命中 roles.supervision -> reviewer 解析 -> subagent 会审 -> 主 agent 最小 patch` 收束为阶段末端唯一监制强化回路。
- 已把监制会审模式、reviewer 来源、降级条件与最终写回权边界写成思维·执行节点，而不是只放在 prose 补充说明里。
- 已锁定四份 Markdown 的长文本口径、shared episode root 的 `组间设计` seed 合同，以及 `3-Detail` 的唯一回接闭环。

---
name: aigc-global
description: Use when the global directing stage needs a single thinking-action skill to turn planning grouping outputs and init presets into project-level global style, episode-group type guidance, episode-group director intent, and a shared episode-root group shell seed.
governance_tier: full
---

# aigc 2-Global

## 概述

`2-Global` 是 `aigc` 技能树位于 `1-Planning` 与 `3-Detail` 之间的导演前置全局合同阶段。

它不再把导演能力外包给外置导演组 contracts。从本轮开始，`全局风格`、`类型元素`、`导演意图` 三个能力面全部内收在同一 `SKILL.md` 内，以“串行锁定前提 + 并发展开三链 + 先在 Markdown 定稿 + 对照字段标题提取入 shared episode root”的知行合一网络完成执行。

本轮重编排遵循两个原则：

- 内容层面全量继承现有 `2-Global` 已沉淀的三份真源、模板口径、项目级/组级分层与下游 handoff 边界
- 机制层面改写为单技能真源，不再维护平行的导演组 team、角色 agent 合同或外置创作方法真源

## Skill Execution Rule (Mandatory)

`2-Global` 采用单技能内部融合模式：

- skill 自身负责输入读取、业务分析、并发链裁决、模板约束、三份 Markdown 写回、字段提取入壳、shared episode root seed、汇流审计与下游回接
- `全局风格`、`类型元素`、`导演意图` 不是外置 subagents，而是父 skill 的三条内部能力链
- 中间只允许形成内部 `plan / note / report / patch set`，最终 canonical 写回只能由当前 `SKILL.md` 完成
- 不得再回指任何外置导演组 contracts 作为执行真源

## When to Use

- 已经有 `projects/<项目名>/1-Planning/3-分组/第N集.md`，需要进入导演前置全局合同阶段。
- 需要把初始化预设、规划分组结果与当前项目定位沉淀为三份 Markdown 长文本真源，并同步写入可被 `3-Detail` 直接继承的 shared episode root。
- 需要在阶段末段先给每个分镜组直接写入固定 `分镜切换` 数字，为 `3-Detail` 的真实切镜提供上游真值。
- 需要同时处理项目级稳定项与当前集分镜组级导演构思，但又不希望把它们混成一份空泛总稿。
- 需要按知行合一方式，把复杂导演判断写成“思行节点 + 并发链 + 汇流门”。

## When Not to Use

- 当前连 `projects/<项目名>/1-Planning/3-分组/第N集.md` 都不存在。
- 当前任务其实还是分集、剧本或分组问题，应回到 `1-Planning`。
- 当前任务已经在补镜级字段、主体、设计、画面或视频产物，应进入 `3-Detail / 4-Design / 5-Image / 6-Video`。

## Business Requirement Analysis Contract (Mandatory)

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把规划分组结果与初始化预设收束为 `全局风格.md`、`类型元素.md`、`导演意图.md` 三份导演前置真源，并把已确认字段、固定 `分镜切换` 与完整分组正文直接写入 shared episode root |
| `business_object` | `0-Init` 的项目基线、`1-Planning` 的当前集分组正文、已有 `2-Global` 文档、shared episode root 与三个模板 |
| `constraint_profile` | `全局风格.md` 必须是项目级稳定、可被角色/场景/道具/分镜无污染继承的底层风格协议，并最终形成 AIGC 生图/生视频统一风格前缀；默认只描述媒介属性、渲染技术栈、美学范式与全局控制轴，不固定景别、镜头距离或具体对象内容，且默认禁止具体颜色词、具体材质词、构图术语与焦段/推拉摇移等摄影操作词直接进入最终字段；`类型元素.md` 与 `导演意图.md` 都必须按 `第N集 -> 【x-x-x】` 组织；`组间设计.全局风格 / 类型元素 / 导演意图` 必须分别直接提取自 Markdown 同名字段，默认字符窗为 `220 / 50 / 100`；`分镜切换` 必须以 `总时长 + 类型元素 + 导演意图 + 分组正文` 为输入，直接写成一个固定镜数，不再写预算包；`组间设计.出场角色及穿搭` 为组级服装摘要槽，`2-Global` 阶段允许先留空字符串，由 `3-Detail` 回填 `角色名-服装简述`；`剧本正文` 必须完整整理入 JSON，除组号标题外不得二次摘要；不得在本阶段发明 shot-level 明细；不再依赖外置导演组 contracts |
| `success_criteria` | 三份 Markdown 真源结构完整、项目级与组级边界清楚、每条内部链都有细致步骤、并发关系与汇流门明确，并且 shared episode root 已写入完整分镜组壳：`分镜组ID / 总时长 / 剧本正文 / 组间设计（含空或已填的出场角色及穿搭） / 分镜切换 / 空分镜明细[]`，可被 `3-Detail` 直接继承 |
| `non_goals` | 不生成 shot-level 明细；不把本阶段写成大而空的“导演宣言”；不再维护第二套导演组 agent 真源 |
| `complexity_source` | 项目级稳定项与当前集组级增量并存；三条能力链共享证据却关注点不同；并发与依赖关系容易打架；质量要求高于普通摘要 |
| `topology_fit` | 前段串行锁输入与不变量，中段三链并发展开，`导演意图` 允许并发预解构但必须等待风格/类型约束稳定后再完成写回，后段统一审计与写回 |
| `step_strategy` | 采用“串行主干 + 并发三链 + 汇流审计”的思行网络，并为三链分别提供细致步骤表与质量门 |

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. 本 `SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/_shared/project-runtime-layout.md`
5. `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
6. `.agents/skills/aigc/_shared/group_design_seed_contract.md`
7. `.agents/skills/aigc/_shared/director_episode_output.schema.json`
8. `.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
9. `projects/<项目名>/0-Init/north_star.yaml`
10. `projects/<项目名>/0-Init/init_handoff.yaml`
11. `projects/<项目名>/0-Init/story-source-manifest.yaml`（若存在）
12. `projects/<项目名>/1-Planning/2-剧本/第N集.md`（若存在）
13. `projects/<项目名>/1-Planning/3-分组/第N集.md`
14. `projects/<项目名>/1-Planning/3-分组/执行报告.md`（若存在）
15. 现有 `projects/<项目名>/2-Global/*.md`
16. `projects/<项目名>/3-Detail/第N集.json`（若存在）
17. 三个模板：
   - `templates/全局风格.template.md`
   - `templates/类型元素.template.md`
   - `templates/导演意图.template.md`

## Shared Canonical Sources (Mandatory)

- 强制读取：`.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.agents/skills/aigc/_shared/group_design_seed_contract.md`
- 强制读取：`.agents/skills/aigc/_shared/director_episode_output.schema.json`
- 强制读取：`.agents/skills/aigc/_shared/director_episode_bootstrap.template.json`
- 强制读取：
  - `.agents/skills/aigc/2-Global/templates/全局风格.template.md`
  - `.agents/skills/aigc/2-Global/templates/类型元素.template.md`
  - `.agents/skills/aigc/2-Global/templates/导演意图.template.md`

硬规则：

1. 本阶段的第一输入根固定为 `projects/<项目名>/1-Planning/3-分组/第N集.md`。
2. 项目级稳定约束优先来自 `0-Init/north_star.yaml`、`0-Init/init_handoff.yaml` 与 `story-source-manifest.yaml`。
3. `全局风格.md` 只允许维护项目级稳定总则，且最终字段默认必须保持“无污染底层风格协议”口径；`类型元素.md` 必须按 `第N集 -> 【x-x-x】` 组织组级类型判断；两者都不得被某一集局部气氛污染。
4. `导演意图.md` 必须按 `## 第N集 -> ### 【x-x-x】` 的层次做增量写回。
5. `3-分组` 的组标题是三段式 `分镜组ID`；四段式 `分镜ID` 属于下游 `3-Detail`。
6. 本阶段必须把 `组间设计` seed 与固定 `分镜切换` 写入 `projects/<项目名>/3-Detail/第N集.json`，并同步维护 `分镜组列表[].分镜组ID / 总时长 / 剧本正文 / 分镜切换 / 分镜明细=[]` 的组壳；`剧本正文` 必须完整整理自 `1-Planning/3-分组/第N集.md` 的命中组正文，除组号标题外不得二次摘要。
7. `组间设计.全局风格 / 类型元素 / 导演意图` 的 JSON 文本必须分别直接提取自三份 Markdown 中已确认的同名字段；写入 JSON 时只允许剥离字段标题与空白，不允许现场重写。`出场角色及穿搭` 为组级摘要槽，本阶段可先写空字符串占位。
8. `组间设计.全局风格 / 类型元素 / 导演意图` 的默认字符窗固定为 `220 / 50 / 100` 个字符以内；其中 `全局风格` 允许为 AIGC 统一风格前缀做适度放宽，但必须先在 Markdown 中确认。`出场角色及穿搭` 默认采用 `角色名-服装简述` 的短句格式。
9. 三条能力链的判断逻辑、细化步骤与质量门都必须内收在本 `SKILL.md`，不得外包给任何外置导演组 contracts。

## Total Input Contract (Mandatory)

### 必需输入

- `projects/<项目名>/1-Planning/3-分组/第N集.md`
- `projects/<项目名>/0-Init/north_star.yaml`
- `projects/<项目名>/0-Init/init_handoff.yaml`

### 可选输入

- `projects/<项目名>/0-Init/story-source-manifest.yaml`
- `projects/<项目名>/1-Planning/2-剧本/第N集.md`
- `projects/<项目名>/1-Planning/3-分组/执行报告.md`
- 现有 `projects/<项目名>/2-Global/*.md`
- `projects/<项目名>/3-Detail/第N集.json`
- 用户显式指定的风格、类型或导演偏好

### 禁止输入

- 与当前项目无关的外部参考文本
- 要求本阶段直接写 shot-level 字段或镜头 JSON 的额外指令
- 任何外置导演组 team、agent、creative method 文档

### 输入处理原则

1. 先锁项目级不变量，再进入三条能力链。
2. 用户显式指定范围或偏好时，用户指定优先，但不得越过项目已锁定真源。
3. 现有 `2-Global/*.md` 只作为增量 patch 依据，不作为绕开上游证据的捷径。
4. 若分组正文不稳定或关键组界不明，`类型元素`、`导演意图` 与 `group_design seed` 只能生成保守版 patch 或 `report`，不得幻想补洞。
5. shared episode root 的 `剧本正文` 必须直接整理自命中组全文；如果落盘内容更像摘要而不是原组正文，视为写回失败。

## Visual Maps

```mermaid
flowchart TD
    A["锁定 0-Init + 1-Planning 证据"] --> B["N1 输入与阶段门"]
    B --> C["N2 项目不变量抽取"]
    C --> D["并发三链启动"]
    D --> D1["N3A 全局风格链"]
    D --> D2["N3B 类型元素链"]
    D --> D3["N3C 导演意图预解构链"]
    D1 --> E["N4 Markdown 字段与约束汇流"]
    D2 --> E
    D3 --> F["N5 导演意图完成链"]
    E --> F
    F --> G["N6 JSON 提取 + 固定分镜切换内化 + 组壳写回链"]
    G --> H["N7 汇流审计"]
    H --> I["N8 父 skill 唯一写回"]
    I --> J["回接 3-Detail"]
```

```mermaid
flowchart LR
    A["项目证据"] --> B{{"并发三链"}}
    B --> C["全局风格: 媒介属性 / 渲染底座 / 美学范式 / 纯度过滤 / AIGC 统一前缀 / 禁区"]
    B --> D["类型元素: 第N集 -> 分镜组 / 类型信号 / 揭示策略 / 负例"]
    B --> E["导演意图预解构: 组任务 / 关注焦点 / 情绪推进 / 空间压力"]
    C --> F{{"风格稳定?"}}
    D --> G{{"类型稳定?"}}
    E --> H["等待上游约束"]
    F --> I["确认 Markdown 提取字段"]
    G --> I
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
    Audited --> Finalized
    Audited --> Rework
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
| `global_style_engine` | 从项目级证据中提炼稳定的媒介属性、渲染底座、美学范式、全局控制轴、禁区与下游继承约束，并收束为无污染统一风格前缀 | `global_style_plan`、`global_style_patch`、`style_note`、`style_report` | 每次进入 `2-Global` 时评估；缺风格底座或风格约束变化时强触发 |
| `type_guidance_engine` | 把题材、主副类型、混合公式与导演打法收束为按组可提取的类型协议 | `type_guidance_plan`、`type_guidance_patch`、`type_note`、`type_report` | 每次进入 `2-Global` 时评估；缺类型协议或类型裁决变化时强触发 |
| `director_intent_engine` | 把当前集分组结果翻译成按组可消费的导演构思 | `director_intent_plan`、`director_intent_patch`、`director_note`、`director_report` | 当前集分组已稳定时默认触发 |
| `group_design_distill_engine` | 把三份 Markdown 中已确认字段、固定分镜切换与完整分组正文提取到 shared episode root 的分镜组壳，并内化 former `镜花/1-切换` 的 fixed-shot-count 接受逻辑 | `group_design_seed_plan`、`group_design_seed_patch`、`episode_seed_patch`、`switching_rationale_note` | 风格/类型/导演意图都稳定且 Markdown 提取字段已确认后强触发 |
| `convergence_audit_engine` | 校验三链与 `group_design seed` 是否边界正确、模板一致、下游可消费且无越权 | `convergence_report`、`writeback_patch_set`、`blocking_note` | 三链与 seed 草案产出后、写回前必须触发 |

硬规则：

1. 这些能力面是当前 `SKILL.md` 的内部节点，不是外置真源。
2. 任何能力面都不得绕过父 skill 直接写 canonical Markdown 或 shared episode root。
3. 若未来继续细化 `2-Global`，必须直接扩写本 `SKILL.md` 的思行网络、seed 合同与模板合同，不得重新长出外置导演组平行真源。

## Topology Contract (Mandatory)

### Topology Fit

本技能采用 `串行前提锁定 + 并发三链 + 依赖汇流` 的混合思行网络：

1. 串行主干：
   - 锁输入
   - 判阶段 readiness
   - 抽项目不变量
2. 并发三链：
   - `全局风格`
   - `类型元素`
   - `导演意图预解构`
3. 依赖汇流：
   - `导演意图` 的最终定稿必须等待 `全局风格 + 类型元素` 的稳定约束
4. 最终收束：
   - Markdown 字段确认
   - JSON 提取与组壳写回
   - 模板与长度窗校验
   - 边界审计
   - 写回三份 Markdown 与 shared episode root
   - 回接 `3-Detail`

### Ordered / Unordered Rules

- `N1 -> N2` 固定串行。
- `N3A + N3B + N3C` 默认并发。
- `N3C` 允许提前做组级预解构，但 `N5` 的最终写回必须等待 `N3A/N3B` 通过约束汇流。
- `N6 -> N7 -> N8` 固定串行。
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

## Thinking-Action Node Network

| node_id | 对应 Step | 聚焦字段 | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `N1-INPUT-GATE` | S1 | `FIELD-GLOBAL-01` `FIELD-GLOBAL-02` | 锁定当前确属 `2-Global` 且输入齐备 | 读取 `north_star / init_handoff / 第N集分组正文`，确认阶段边界与文件存在性 | `input_lock_note`、缺口列表 | pass -> `N2`；fail -> 结束并返回 `report` | 输入与阶段边界达标后才可继续 |
| `N2-INVARIANT-LOCK` | S2 | `FIELD-GLOBAL-02` `FIELD-GLOBAL-03` | 抽出项目级不变量与当前集组级范围 | 提取题材边界、观众合同、风格基线、组级范围、禁止越权项 | `invariant_brief`、`branch_scope_plan` | pass -> `N3A/N3B/N3C`；冲突 -> 回 `S1/S2` | 不变量明确后才可并发 |
| `N3A-GLOBAL-STYLE` | S3-S4 | `FIELD-GLOBAL-04` | 形成项目级全局风格底座，并确认它作为 AIGC 生图/生视频统一风格前缀时对 `3-Detail/5-Image/6-Video` 都具有可实现指导意义 | 运行全局风格细化步骤，先锁媒介属性、渲染技术栈、美学范式与全局控制轴，再经过无污染过滤生成候选比较、禁区、继承约束、最佳示例参照与统一风格前缀，并先在 Markdown 中定稿字段标题 `全局风格` | `global_style_plan`、`global_style_patch`、`style_note`、`style_reference_note` | pass -> `N4`；fail -> 回 `S3/S4` | 项目级风格不得 episode 化；最终字段不得被具体镜头/景别/对象污染，也不能只停留在抽象形容词 |
| `N3B-TYPE-GUIDANCE` | S5-S6 | `FIELD-GLOBAL-05` | 形成按分镜组组织的类型元素协议，并确认它能转译成后续 detail 的导演动作 | 运行类型元素细化步骤，按 `第N集 -> 【x-x-x】` 生成每组的类型信号、打法、禁区、参考作品桥段、具像化表述与 `3-Detail` 落地导向，并先在 Markdown 中定稿字段标题 `类型元素` | `type_guidance_plan`、`type_guidance_patch`、`type_note`、`type_reference_note` | pass -> `N4`；fail -> 回 `S5/S6` | 类型协议须按组可提取，可约束下游，且必须给出可操作的导演翻译 |
| `N3C-DIRECTOR-PREP` | S7 | `FIELD-GLOBAL-06` | 提前解构当前集各组的导演任务，并预判哪些判断值得在 detail 被放大 | 逐个读取 `【x-x-x】`，提取剧情任务、关注焦点、情绪推进、空间压力、候选参考桥段与下游放大抓手 | `director_intent_plan`、`director_note`、`director_reference_candidates` | pass -> `N5`；fail -> 回 `S7` | 仅允许预解构，不得提前定稿 |
| `N4-CONSTRAINT-CONVERGENCE` | S8 | `FIELD-GLOBAL-04` `FIELD-GLOBAL-05` | 汇流风格与类型约束，确认三份 Markdown 中供 JSON 直接引用的字段与位置 | 对齐风格稳定项、全局控制轴、按组类型打法、禁区、无污染过滤结果、参考桥段与下游继承要求，并检查 `全局风格 / 类型元素` 字段已在 Markdown 中定稿 | `constraint_bridge_note`、`detail_execution_bridge`、`md_field_anchor_note` | pass -> `N5`；fail -> 回 `N3A/N3B` | 风格与类型必须先稳定；控制轴可服务判断，但最终字段不得越权滑成镜头细则 |
| `N5-DIRECTOR-FINALIZE` | S9 | `FIELD-GLOBAL-07` | 在约束已稳定的前提下完成导演意图 patch，并把参考锚点翻译成当前组的可执行指令 | 将组级预解构翻译成 `导演意图.md` 的 `第N集/【x-x-x】` patch，补齐参考桥段、具像化表述、detail 放大方向，并先在组内定稿字段标题 `导演意图` | `director_intent_patch`、`director_report`、`director_implementation_note` | pass -> `N6`；fail -> 回 `N3C/N4` | 每组必须可被 `3-Detail` 直接消费，不能只有口号 |
| `N6-GROUP-DESIGN-DISTILL` | S10 | `FIELD-GLOBAL-08` | 把三份 Markdown 中已确认字段、固定分镜切换与完整剧本正文直接提取到 shared episode root 的组级壳，并控制长度窗 | 按 `group_design_seed_contract` 对照字段标题，直接提取 `全局风格.md` 的项目级 `全局风格`、`类型元素.md` 的命中组 `类型元素`、`导演意图.md` 的命中组 `导演意图`；同步基于 `总时长 + 类型元素 + 导演意图 + 组正文` 直接裁定 `分镜切换`，并以内化 former `镜花/1-切换` 的口径写出 `switching_rationale_note`；再将 `1-Planning/3-分组/第N集.md` 命中组全文去掉组号标题后完整写入 `分镜组列表[].剧本正文`，并生成 `episode_seed_patch` | `group_design_seed_plan`、`group_design_seed_patch`、`episode_seed_patch`、`switching_rationale_note` | pass -> `N7`；fail -> 回 `N3A/N3B/N5` | 三个字段必须来自已确认 Markdown，`分镜切换` 必须是组级固定数值，且 `剧本正文` 必须是完整组正文 |
| `N7-CONVERGENCE-AUDIT` | S11 | `FIELD-GLOBAL-09` | 检查模板一致性、字段引用位置、剧本正文完整性、长度窗、边界正确性、参考锚点清晰度与下游 handoff | 运行模板对齐、项目级/组级边界检查、JSON 字段位置检查、`group_design` 长度窗检查、越权检查、空话审计、reference/bridge 审计、剧本正文完整性审计与可实现性审计 | `convergence_report`、`writeback_patch_set` | pass -> `N8`；fail -> 回目标节点返工 | 通过后才能写回 |
| `N8-WRITEBACK-HANDOFF` | S12 | `FIELD-GLOBAL-10` | 统一写回三份 Markdown、shared episode root，并回接 `3-Detail` | 先按增量策略写回三份长文本真源，再将已确认字段与组全文提取入 `第N集.json` 的分镜组壳，输出下一入口与闭环 triad | 三份 canonical 文档、shared root、`handoff_note` | Final | 仅父 skill 拥有最终写回权 |

## Capability Chain Detail (Mandatory)

### 全局风格链

| branch_step | 要从哪些方面着手 | 具体动作 | 输出要求 |
| --- | --- | --- | --- |
| `GS1` | 媒介属性与渲染技术栈 | 从 `north_star / init_handoff` 判断整片是更偏真人、2D、3D 还是混合媒介，并锁定对应渲染技术栈 | 不允许只写“高级感”“电影感” |
| `GS2` | 美学范式与叙事服务 | 选择最能服务题材与观众合同的美学范式，并解释它如何服务叙事而非只服务好看 | 必须说明为什么它属于项目级稳定项 |
| `GS3` | 全局控制轴 | 内部判断观演距离、主客观模式、炫技倾向、运镜/转场偏置、光影戏剧性、色彩振幅与母题密度 | 这些控制轴用于约束后续判断，不应直接污染最终字段 |
| `GS4` | 无污染过滤 | 将候选描述中过于具体的颜色词、材质词、构图术语、焦段/推拉摇移与对象内容清除，改写为媒介、渲染、光学或美学层术语 | 最终字段默认只描述 HOW 与 WHAT STYLE，不描述 WHAT CONTENT |
| `GS5` | 类型化语料与最佳示例参照 | 为当前风格判断寻找最贴切的成熟风格表达样本与无污染改写范例，提炼其组织方式与处理逻辑 | 必须写清“参照哪一段、借的是哪种处理逻辑”，不能只报作品名 |
| `GS6` | AIGC 统一风格前缀 | 把风格判断收束为可直接作为 AIGC 生图/生视频统一前缀的一段话，并在 Markdown 用字段标题 `全局风格` 定稿 | 可在原字数窗基础上适度放宽，但必须保持单段、稳定、可直接提取 |
| `GS7` | 对下游的继承边界 | 检查该风格是否真能被 `3-Detail/4-Design/5-Image/6-Video` 无污染继承，并明确哪些只作为节点判断、哪些可写进最终字段 | 必须对后续阶段具有可实现指导意义 |
| `GS8` | 稳定禁区与允许自由度 | 写清必须禁止的表达、谨慎使用的表达与可留给下游变化的自由度 | 必须同时给正向锚点和负向禁区 |
| `GS9` | 候选比较与增量 patch | 比较多个风格路径，只保留主路径，并生成项目级 patch 与取舍说明 | 不得并列塞进互相冲突的风格方向 |

### 类型元素链

| branch_step | 要从哪些方面着手 | 具体动作 | 输出要求 |
| --- | --- | --- | --- |
| `TG1` | 分镜组范围与观众合同 | 以 `第N集 -> 【x-x-x】` 为最小单元，从故事目标、当前组冲突与 init 预设中提炼观众到底该期待什么 | 不得只堆题材标签 |
| `TG2` | 当前组主类型、副类型、混合公式 | 判断当前组的主副关系和权重，而不是把多个类型平铺并列 | 必须写清主次与混合逻辑 |
| `TG3` | 冲突引擎与揭示策略 | 提炼当前组如何制造 tension、何时揭示、如何递送信息 | 必须能指导下游镜头节奏 |
| `TG4` | 参考作品桥段与类型样本 | 为当前组类型组合寻找最贴切的作品或桥段样本，提炼其类型运作方式而非搬运剧情 | 必须说明参照桥段对当前组的可借鉴点 |
| `TG5` | 具像化导演打法 | 把当前组类型判断翻译成镜头组织、表演强弱、节奏推进、情绪传递和信息显隐方式 | 不能停留在类型名词层 |
| `TG6` | 字段定稿与对 `3-Detail` 的落地指导 | 把当前组类型协议压成 detail 可执行的镜头、表演、转场与揭示指令，并在 Markdown 用字段标题 `类型元素` 定稿一段话 | 必须对后续 detail 具有可实现指导意义 |
| `TG7` | 错误类型负例与禁区 | 指出 wrong-genre 信号、禁用 register 与保底退化策略 | 下游必须能据此判断“不能怎么做” |
| `TG8` | 候选比较与增量 patch | 只保留主路径，生成按组 patch 与取舍说明 | 不得把互斥打法同时写进真源 |

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

`2-Global` 的一次性输出不是多个平行草案，而是同一 bundle 内的五类结果：

1. `projects/<项目名>/2-Global/全局风格/全局风格设计.md`
   - 项目级风格底座唯一真源
2. `projects/<项目名>/2-Global/类型元素/全集设计.md` 与 `projects/<项目名>/2-Global/类型元素/分组设计.md`
   - 前者持有项目级类型总则，后者持有按集、按组组织的类型化导演协议；`类型元素.md` 仅允许作为兼容投影
3. `projects/<项目名>/2-Global/设计元素/设计元素.md`
   - 按集、按组沉淀的导演构思唯一真源
4. `projects/<项目名>/3-Detail/第N集.json`
   - shared episode root；本阶段写 `分镜组ID / 总时长 / 剧本正文 / 组间设计 / 分镜切换 / 分镜明细=[]` 的分镜组壳与相关 metadata
5. `closure triad + handoff note`
   - 说明 `root cause location / immediate fix / systemic prevention fix`
   - 给出下一入口固定为 `3-Detail`

## Canonical Output Governance (Mandatory)

1. `全局风格.md` 只能写项目级稳定总则；`类型元素.md` 必须按 `第N集 -> 【x-x-x】` 写组级类型判断。
2. `导演意图.md` 只写按集、按组的导演构思，不得冒充项目级风格总则。
3. 三份文档都由当前 skill 聚合写回，不存在平行导演组 writeback owner。
4. shared episode root 的 `剧本正文 + 组间设计 + 分镜切换` 也由当前 skill 聚合写入，但本阶段不得发明 shot-level `分镜明细[]`。
5. JSON 写回时，`组间设计.全局风格 / 类型元素 / 导演意图` 只能直接引用 Markdown 中同名字段，不得临场改写或另起第二套摘要。
6. 现有文档或 shared root 存在时，只允许增量更新命中章节与命中组，不得整稿抹平历史内容。
7. 对 `3-Detail` 的第一结构化 handoff 以 shared episode root 为准；`2-Global/*.md` 仍保留为长文本解释载体。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-GLOBAL-01` | 阶段定位 | 明确 `2-Global` 是 `1-Planning` 与 `3-Detail` 之间的导演前置全局合同阶段 | S1 | 边界清晰度 | FAIL-GLOBAL-01 |
| `FIELD-GLOBAL-02` | 输入与不变量 | 锁定项目级硬证据、组级范围和禁止越权项 | S2 | 输入真源一致性 | FAIL-GLOBAL-02 |
| `FIELD-GLOBAL-03` | 并发拓扑 | 明确三链并发、依赖汇流与父 skill 写回边界 | S3 | 编排可执行性 | FAIL-GLOBAL-03 |
| `FIELD-GLOBAL-04` | 全局风格真源 | 项目级风格底座稳定，具备媒介属性、渲染技术栈、美学范式、全局控制轴、AIGC 统一风格前缀、参考桥段、禁区与下游继承；最终字段保持无污染底层风格协议 | S4 | 项目级稳定性 | FAIL-GLOBAL-04 |
| `FIELD-GLOBAL-05` | 类型元素真源 | `类型元素.md` 已按 `第N集 -> 【x-x-x】` 组织，且每组都具备主副类型、参考桥段、具像化导演打法、detail 落地导向与错误类型禁区 | S5 | 类型化有效性 | FAIL-GLOBAL-05 |
| `FIELD-GLOBAL-06` | 导演意图预解构 | 当前集组级任务、关注焦点、情绪推进与空间压力被正确解构 | S7 | 组级分析精度 | FAIL-GLOBAL-06 |
| `FIELD-GLOBAL-07` | 导演意图写回 | `导演意图.md` 当前集命中组的 patch 具体、可消费、具备参考桥段与具像化落地指令、不过界 | S9 | 下游可消费性 | FAIL-GLOBAL-07 |
| `FIELD-GLOBAL-08` | JSON 提取与组壳写回 | shared episode root 的 `剧本正文 / 全局风格 / 类型元素 / 导演意图 / 分镜切换` 已按正确字段位置写回，其中 `组间设计` 字段来自 Markdown 直接提取并满足 `220 / 50 / 100` 字符窗，`分镜切换` 来自同轮固定数值裁决，且 former `镜花/1-切换` 的 fixed-shot-count 接受逻辑已内化为 `switching_rationale_note` | S10 | 提取可消费性 | FAIL-GLOBAL-08 |
| `FIELD-GLOBAL-09` | 汇流审计 | 空话、越权、边界污染、字段错引、剧本正文摘要化、长度窗违规与依赖断裂被拦住 | S11 | 收束完整性 | FAIL-GLOBAL-09 |
| `FIELD-GLOBAL-10` | shared root + 下一阶段 handoff | 返回 triad closure，并固定回接 `3-Detail` 与 shared episode root | S12 | 闭环可执行性 | FAIL-GLOBAL-10 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-GLOBAL-01` | 当前是不是 `2-Global` 阶段问题 | 锁定阶段边界与上下游职责 | 把本阶段写成 `3-Detail` 或 `1-Planning` |
| `S2` | `FIELD-GLOBAL-02` | 当前轮必须先锁哪些不变量 | 写出输入清单、禁止越权项与组级范围 | 输入根或不变量漂移 |
| `S3` | `FIELD-GLOBAL-03` | 三条能力链如何并发且不打架 | 写出并发拓扑、依赖和汇流门 | 只说“并发”，没写依赖条件 |
| `S4` | `FIELD-GLOBAL-04` | 项目级风格底座到底稳定在哪，是否已经经过无污染过滤并能直接指导后续阶段 | 产出全局风格 patch、控制轴判断、参考桥段、无污染统一前缀与取舍说明 | 风格文档被某一集情绪污染、只剩抽象形容词，或最终字段混入景别/镜头/对象细节 |
| `S5` | `FIELD-GLOBAL-05` | 类型协议如何按组约束后续导演链并落到 detail 执行 | 产出按组的类型元素 patch、参考桥段、具像化打法与禁区 | 只有类型词，没有导演打法或 detail 导向，或未按组组织 |
| `S6` | `FIELD-GLOBAL-05` | 类型候选如何取舍 | 压缩主路径，记录未采纳方向 | 多种互斥打法并列留在主稿 |
| `S7` | `FIELD-GLOBAL-06` | 当前集各组真正的导演任务是什么，哪些处理值得被 detail 放大 | 逐组预解构剧情任务、关注焦点、情绪推进、参考桥段候选与下游抓手 | 只复述剧情摘要，没有下游抓手 |
| `S8` | `FIELD-GLOBAL-04` `FIELD-GLOBAL-05` | 风格与类型怎样变成导演意图约束与下游执行语言 | 形成约束桥接说明与 detail 执行桥 | 导演意图不受项目级约束，或没有执行桥 |
| `S9` | `FIELD-GLOBAL-07` | 当前集导演构思是否足够具体，是否具备参考桥段与具像化指令 | 写入 `导演意图.md` 局部 patch | 只剩空泛口号，或只有参照名词没有具像化处理 |
| `S10` | `FIELD-GLOBAL-08` | Markdown 已确认字段、固定分镜切换与完整组正文能否被正确提取进 shared episode root，并保持 `220 / 50 / 100` 字符窗 | 生成 `group_design_seed_patch`、`episode_seed_patch` 与 `switching_rationale_note` | 字段错引、固定镜数缺失、剧本正文被摘要化、跨组混写、旧 `1-切换` 逻辑仍留在下游或超窗 |
| `S11` | `FIELD-GLOBAL-09` | 三份文档与 shared root 能否一起合法落盘，并被下游直接消费 | 执行模板/字段位置/剧本正文完整性/边界/长度窗/越权/空话/reference 可实现性审计 | 结构断裂、字段错位、边界污染、长度窗违规、参照失焦或越权写回 |
| `S12` | `FIELD-GLOBAL-10` | 如何证明本轮完成并交给下游 | 输出 triad closure、shared root seed 与 `3-Detail` 回接说明 | 没有返工入口、shared root 未落盘或下一阶段缺失 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-GLOBAL-01` | 阶段定位、上下游边界与三份真源职责明确 | FAIL-GLOBAL-01 | S1 |
| `FIELD-GLOBAL-02` | 项目级硬证据、组级范围与禁止越权项锁定 | FAIL-GLOBAL-02 | S2 |
| `FIELD-GLOBAL-03` | 三链并发、依赖和写回权边界明确 | FAIL-GLOBAL-03 | S3 |
| `FIELD-GLOBAL-04` | `全局风格.md` 具备媒介属性、渲染技术栈、美学范式、控制轴、AIGC 统一风格前缀、参考桥段、禁区与下游继承，且最终字段无污染 | FAIL-GLOBAL-04 | S4 |
| `FIELD-GLOBAL-05` | `类型元素.md` 已按组组织，且具备主副类型、参考桥段、导演打法、负例、保底策略与 detail 导向 | FAIL-GLOBAL-05 | S5-S6 |
| `FIELD-GLOBAL-06` | 组级导演任务预解构具体且与 `【x-x-x】` 对齐 | FAIL-GLOBAL-06 | S7 |
| `FIELD-GLOBAL-07` | `导演意图.md` 当前集命中组的 patch 具体、可消费、具备参考桥段、具像化落地指令且不过界 | FAIL-GLOBAL-07 | S8-S9 |
| `FIELD-GLOBAL-08` | `剧本正文 + 组间设计 + 分镜切换` 已按正确字段位置写入分镜组壳，其中三条组级上下文来自 Markdown 直接提取，且 fixed-shot-count 接受逻辑已在本阶段内化 | FAIL-GLOBAL-08 | S10 |
| `FIELD-GLOBAL-09` | 无空话、无越权、无项目级/组级污染、无字段错引、无剧本正文摘要化、无字符窗违规 | FAIL-GLOBAL-09 | S11 |
| `FIELD-GLOBAL-10` | 返回 triad closure，shared root 已 seed，并固定回接 `3-Detail` | FAIL-GLOBAL-10 | S12 |

## Root-Cause Execution Contract (Mandatory)

当 `2-Global` 出现以下问题时，必须先修源层而不是补单次文案：

- `2-Global` 仍回指已退役的导演组外置 contracts
- 三条能力链只有并发口号，没有依赖汇流门
- `全局风格.md` 或 `类型元素.md` 被写成当前集情绪杂糅稿
- `全局风格` 最终字段混入具体景别、镜头距离、构图术语、具体颜色词、具体材质词或对象级内容
- `类型元素.md` 没有按 `第N集/【x-x-x】` 组织，导致 JSON 无法按组正确引用
- `导演意图.md` 没有回链到 `第N集/【x-x-x】`
- `导演意图` 在风格/类型约束未稳定前就提前定稿
- 风格、类型、导演意图只剩抽象词，无法指导 `3-Detail` 的实际展开
- 只写了参考作品名，没有指出具体桥段与可借鉴的处理逻辑
- 写 JSON 时重新改写了 `全局风格 / 类型元素 / 导演意图`，而不是直接引用 Markdown 已确认字段
- `分镜切换` 没有在 `2-Global` 末段直接写成固定数值，导致 `3-Detail` 又要临场决定组级镜数
- former `镜花/1-切换` 的 fixed-shot-count 接受逻辑仍滞留在 `3-Detail/镜花`，导致上游/下游出现第二套切换真源
- `剧本正文` 写进 shared episode root 时只剩摘要，没有完整保留命中组正文
- `组间设计` 没有 seed 到 shared episode root，或长度窗失控
- 阶段越权在 `2-Global` 发明 shot-level `分镜明细[]`

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/2-Global/SKILL.md`
  - `.agents/skills/aigc/2-Global/_shared/IO_CONTRACT.md`
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
- 已明确三条内部能力链与并发/汇流关系。
- 已把 `全局风格 / 类型元素 / 导演意图` 的细致步骤写入同一 `SKILL.md`。
- 已把 `类型元素.md` 改成按组组织，并把三类字段的 Markdown -> JSON 提取位置写成唯一真源。
- 已固定 shared episode root 中 `剧本正文` 必须完整保留命中组正文，不得再写成摘要。
- 已要求三条能力链都回答 `3-Detail` 可实现性、参考作品桥段与具像化表述。
- 已明确不再依赖外置导演组 contracts。
- 已锁定三份 Markdown 的长文本口径、shared episode root 的 `组间设计` seed 合同，以及 `3-Detail` 的唯一回接闭环。

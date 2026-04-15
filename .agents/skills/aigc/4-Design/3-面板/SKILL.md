---
name: aigc-design-panel
description: Use when the `4-Design/3-面板` tranche needs to route stable design outputs into panel layout JSONs and SMART nano-banana image generation under `projects/aigc/<项目名>/4-Design/<域>/3-面板/`.
governance_tier: full
---

# aigc 4-Design / 3-面板

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 概述

`3-面板` 是 `4-Design` 的展示与派生生图 tranche。它只消费 `2-设计` 已稳定的设计产物，把其中可直接下游使用的 `full_generation_prompt / prompt整合` 收束为面板 layout JSON，并在默认路径下自动桥接 `.agents/skills/api/image/nano-banana/general` 生图。

`2-设计` 当前会为单一主体生成同目录同 stem 概念图；`3-面板` 在批量上下文中可把这些图片作为 SMART 连续性参照，但不得把它们升格为面板 layout 真源。

真实 provider 调用默认继承 `.agents/skills/aigc/_shared/image-generation-execution-contract.md`：先写 `panel_auto_generate_batch.json`，再后台批量并发提交；只有显式 `--foreground` 时才前台等待图片完成。

本 tranche 当前已重建的 active leaf：

- `.agents/skills/aigc/4-Design/3-面板/场景`
- `.agents/skills/aigc/4-Design/3-面板/角色`
- `.agents/skills/aigc/4-Design/3-面板/道具`

未重建 sibling 仍不得伪装为 active；父 tranche 只提供路由、共享 SMART 桥与门禁。

## Business Requirement Analysis Contract

| 分析槽位 | 当前答案 |
| --- | --- |
| `business_goal` | 把设计真源的 `full_generation_prompt / prompt整合` 转换成 review-ready panel layout JSON，并默认生成派生 PNG |
| `business_object` | `2-设计/<域>/第N集/` 下的 Markdown 设计卡、结构化 JSON、同 stem 单主体图片、layout 模板、SMART 参考图与 nano-banana request |
| `constraint_profile` | 不改写 `2-设计` 真源；layout JSON 是面板层第一派生真源；PNG 是再派生资产；SMART 参照只在批量 4-Design 调度时自动发现 |
| `success_criteria` | 每个命中主体都有独立 `*-Panel-layout.json`、可追踪 `_manifest.json`、默认触发 nano-banana/general；批量上下文可绑定 `2-设计` 同 stem 图片，单文件/自然语言直生图默认无参照 |
| `non_goals` | 不重新设计主体；不回写 `3-Detail`、`1-清单` 或 `2-设计`；不把历史旧仓路径升为当前 runtime |
| `complexity_source` | 输入形态多样，且批量链路需要 continuity refs，单文件链路又不能自动污染参考图 |
| `topology_fit` | 适合“输入判型 -> leaf 路由 -> layout 写回 -> SMART 桥接 -> manifest 汇流”的混合型思行网络 |

## Total Input Contract

### 默认输入

- `projects/aigc/<项目名>/4-Design/<域>/2-设计/第N集/*.md`
- `projects/aigc/<项目名>/4-Design/<域>/2-设计/第N集/_manifest.json`
- `projects/aigc/<项目名>/4-Design/<域>/2-设计/第N集/*.{png,jpg,jpeg,webp}`（批量 SMART 参照，可选）
- 兼容 JSON：`道具设计.json`、`prop_design_prompt.json` 等 leaf 声明的投影

### 固定输出

- `projects/aigc/<项目名>/4-Design/<域>/3-面板/第N集/*-Panel-layout.json`
- `projects/aigc/<项目名>/4-Design/<域>/3-面板/第N集/_manifest.json`
- 自动生图请求侧车：`projects/aigc/<项目名>/4-Design/<域>/3-面板/第N集/generated/requests/*.json`
- 派生 PNG：`projects/aigc/<项目名>/4-Design/<域>/3-面板/第N集/generated/<layout-stem>/*.png`

### 硬门槛

1. `3-面板` 不拥有设计事实，只引用上游 `full_generation_prompt / prompt整合`。
2. `layout.json` 必须先落盘，再调用图片生成。
3. 自动生图统一走 `.agents/skills/api/image/nano-banana/general` 的结构化请求承接。
4. 批量 `4-Design` 调度默认启用 `continuous-batch`，自动扫描 `2-设计` 目录中同主体同 stem 图片作为参照。
5. 单独指定文件、目录、layout JSON 或自然语言生图默认启用 `single-doc-t2i / natural-language-t2i`，除非用户显式传 `--reference`，否则不自动绑定参照图。
6. `layout-only / json-only` 仍必须写出 `generated/requests/panel_auto_generate_batch.json` 与 bridge report；只是不调用 nano。

## Visual Maps

```mermaid
flowchart TD
    A["2-设计 产物"] --> B{"命中 leaf?"}
    B -->|"场景"| C1["3-面板/场景"]
    B -->|"角色"| C2["3-面板/角色"]
    B -->|"道具"| C3["3-面板/道具"]
    B -->|"未重建 sibling"| X["阻塞: leaf pending"]
    C1 --> D["直引 full_generation_prompt / prompt整合"]
    C2 --> D
    C3 --> D
    D --> E["写 layout JSON"]
    E --> F["SMART bridge"]
    F --> G["nano-banana/general"]
    G --> H["PNG + request trace"]
```

```mermaid
flowchart LR
    A{"执行上下文"} -->|"批量 4-Design 调度"| B["continuous-batch"]
    A -->|"单文件 / 目录 / 自然语言"| C["single-doc-t2i / natural-language-t2i"]
    B --> D["扫描 2-设计 同 stem 单主体图片"]
    C --> E["默认不扫描参照"]
    D --> F["I2I request if refs found"]
    E --> G["T2I request unless explicit --reference"]
```

```mermaid
stateDiagram-v2
    [*] --> Routed
    Routed --> LayoutWritten
    LayoutWritten --> SmartResolved
    SmartResolved --> RequestBuilt
    RequestBuilt --> Generated
    Generated --> Manifested
    Routed --> ReworkRoute: FAIL-PANEL-ROUTE
    LayoutWritten --> ReworkLayout: FAIL-PANEL-LAYOUT
    SmartResolved --> ReworkSmart: FAIL-PANEL-SMART
    RequestBuilt --> ReworkNano: FAIL-PANEL-NANO
```

## Shared Canonical Sources

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| SMART bridge | `.agents/skills/aigc/4-Design/3-面板/_shared/panel_auto_generate.py` | layout JSON -> nano-banana/general request |
| image execution contract | `.agents/skills/aigc/_shared/image-generation-execution-contract.md` | 后台批量并发默认执行模式 |
| design output contract | `.agents/skills/aigc/4-Design/2-设计/_shared/design-output-contract.md` | `full_generation_prompt` 与同目录同名单主体图真源 |
| 场景 leaf | `.agents/skills/aigc/4-Design/3-面板/场景/SKILL.md` | 当前 active leaf |
| 角色 leaf | `.agents/skills/aigc/4-Design/3-面板/角色/SKILL.md` | 当前 active leaf |
| 道具 leaf | `.agents/skills/aigc/4-Design/3-面板/道具/SKILL.md` | 当前 active leaf |
| API 契约 | `.agents/skills/api/image/nano-banana/general/SKILL.md` | 生图请求承接真源 |

## Route And Topology Contract

1. 命中 `场景面板 / scene panel / 场景 layout / 场景面板生图` 时进入 `3-面板/场景`。
2. 命中 `角色面板 / character panel / 角色 layout / 角色面板生图` 时进入 `3-面板/角色`。
3. 命中 `道具面板 / prop panel / 道具 layout / 道具面板生图` 时进入 `3-面板/道具`。
4. 用户要求整个 `4-Design` 批量推进，且对应 `2-设计/<域>` 已产出，允许自动进入已 active 的 panel leaf。
5. 未重建的 `服装` panel leaf 只报告 pending，不得引用旧路径执行。
6. leaf 产出的 layout JSON 必须遵循共享 SMART bridge 合同；leaf 只能调用 `_shared/panel_auto_generate.py`，不得私造第二套 nano payload、Assets 扫描或 SMART mode 解析。

## Thinking-Action Node Network

### NODE-PANEL-01 路由判型

- `objective`: 判断本轮是批量 4-Design panel、单 leaf panel、单文件生图还是自然语言直生图。
- `actions`: 锁定 leaf、project、episode、输入根与 SMART 默认模式。
- `evidence`: `leaf_id`、`pipeline_context`、`smart_mode_resolved`。
- `route_out`: 场景/角色/道具 -> 对应 active leaf；未重建 sibling -> `FAIL-PANEL-ROUTE`。
- `gate`: 只有命中 active leaf 才允许执行。

### NODE-PANEL-02 JSON 先行

- `objective`: 保证任何生图前都已有可追溯 layout JSON。
- `actions`: leaf 从设计产物提取 `full_generation_prompt / prompt整合`，写 `*-Panel-layout.json` 与 `_manifest.json`。
- `evidence`: layout 文件列表、manifest 输出统计。
- `route_out`: JSON 完成 -> `NODE-PANEL-03`；缺 prompt 或模板 -> `FAIL-PANEL-LAYOUT`。
- `gate`: 不允许跳过 JSON 直接调用 API。

### NODE-PANEL-03 SMART 生图桥

- `objective`: 根据执行上下文决定是否自动绑定设计图参照。
- `actions`: 批量上下文扫描 `2-设计` 同 stem 单主体图片；单文件/自然语言上下文默认不扫描；构造 nano-banana request sidecar；默认以 `background-batch-concurrent + max_concurrent=100` 提交 provider。
- `evidence`: `prompt_reference.smart_mode_resolved`、`continuity_reference_images`、`explicit_references`、`execution_mode`、`background_pid/background_log`。
- `route_out`: request 生成 -> nano-banana/general；映射失败 -> `FAIL-PANEL-SMART`。
- `gate`: 自动参照图只允许在批量上下文中出现。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-PANEL-01` | leaf route | 只调度 active leaf | `NODE-PANEL-01` | 路由准确性 | `FAIL-PANEL-ROUTE` |
| `FIELD-PANEL-02` | `*-Panel-layout.json.prompt` | 直接来自上游 `full_generation_prompt / prompt整合` | `NODE-PANEL-02` | prompt 真源性 | `FAIL-PANEL-LAYOUT` |
| `FIELD-PANEL-03` | `image_generation` | 指向 nano-banana/general，记录 SMART 默认，并按共享执行合同默认后台批量并发提交 | `NODE-PANEL-03` | 生图桥接 | `FAIL-PANEL-SMART` |
| `FIELD-PANEL-04` | request sidecar | 批量自动参照、单文件默认无参照 | `NODE-PANEL-03` | SMART 语义 | `FAIL-PANEL-SMART` |
| `FIELD-PANEL-05` | `_manifest.json` | 记录 layout、request sidecar、`background_submitted` 或前台执行结果 | `NODE-PANEL-02/03` | 可追溯性 | `FAIL-PANEL-MANIFEST` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-PANEL-01` | 当前 leaf 是否已重建 | 锁定 active leaf | 调度 pending sibling |
| `S2` | `FIELD-PANEL-02` | prompt 是否来自设计产物 | 提取上游 `full_generation_prompt / prompt整合` | 重新创作 prompt |
| `S3` | `FIELD-PANEL-03/04` | 是否该自动参照图 | 根据上下文解析 SMART 模式并扫描同 stem 设计图 | 单文件任务被自动塞参照 |
| `S4` | `FIELD-PANEL-05` | 是否能审计 layout 与生图 | 写 manifest 与 request trace | 成功/失败不可定位 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-PANEL-01` | 只进入 active leaf | `FAIL-PANEL-ROUTE` | `NODE-PANEL-01` |
| `FIELD-PANEL-02` | prompt 非空、可回链上游文件，且优先使用 `full_generation_prompt` | `FAIL-PANEL-LAYOUT` | leaf prompt extraction |
| `FIELD-PANEL-03` | request 指向 nano-banana/general 标准字段，默认 `execution_mode=background-batch-concurrent` 且并发上限可追踪 | `FAIL-PANEL-SMART` | `_shared/panel_auto_generate.py` |
| `FIELD-PANEL-04` | 批量/单文件参照策略符合合同 | `FAIL-PANEL-SMART` | `_shared/panel_auto_generate.py` |
| `FIELD-PANEL-05` | manifest 记录输出与生图结果 | `FAIL-PANEL-MANIFEST` | leaf manifest writeback |

## Root-Cause Execution Contract (Mandatory)

问题排查必须上溯：

`Symptom -> Direct Technical Cause -> Rule Source (3-面板 leaf / _shared bridge / template) -> Meta Rule Source (AGENTS.md / skill-知行合一 / nano-banana general) -> Fix Landing Points`

优先修复：

1. leaf `SKILL.md` 的输入/输出合同。
2. `_shared/panel_auto_generate.py` 的 SMART 判型与 request 映射。
3. layout template 的字段结构。
4. nano-banana/general 的结构化请求承接说明。
5. `.agents/skills/aigc/_shared/image-generation-execution-contract.md` 的执行模式真源。

## Completion Criteria

- active leaf 产出 `layout.json`。
- 默认自动桥接 nano-banana/general。
- 默认后台批量并发提交 provider，并在 manifest/bridge report 中记录 request sidecar、pid 与日志。
- 批量上下文自动扫描 `2-设计` 同 stem 单主体图片作为参照。
- 单文件或自然语言生图默认无参照。
- `_manifest.json` 可追溯 layout 与生图状态。

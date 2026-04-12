---
name: aigc-design-costume-panel
description: Use when the `4-Design/3-服装/3-面板` stage needs to turn `服装设计.json + costume_design_prompt.json` into review-ready costume panel layout JSONs under `projects/<项目名>/4-Design/3-服装/3-面板/`.
governance_tier: full
---

# 4-Design / 3-服装 / 3-面板

## 概述

`3-面板` 是 `4-Design/3-服装` 类目下承接设计真源的展示型叶子技能。

它消费 `2-设计` 已经稳定写出的 `服装设计.json` 与 `costume_design_prompt.json`，把每套服装收束成可审阅、可追溯、可继续下游消费的 panel layout JSON，而不是回头重扫 `角色清单`、`编导` 或直接越权生图。

当前仓库的 canonical 交付停点是：

1. 每套服装一份 `<costume_id>-<canonical_label>-CostumePanel-layout.json`
2. 每集一份 `_manifest.json`

## When to Use

- 已有 `projects/<项目名>/4-Design/3-服装/2-设计/第N集/服装设计.json`，需要继续生成服装展示面板布局。
- 需要把 design master 收束成可审阅的 panel dossier，而不是直接跳到 `5-Image`。
- 需要给后续 image / review / costume-swap 工具提供稳定的 panel handoff JSON。

## When Not to Use

- 还没有 `costume_design_bridge.json` 或 `服装设计.json`，应先回到 `1-清单` 或 `2-设计`。
- 当前任务是直接执行图片生成、视频请求或素材发布，而不是先固化 panel layout。
- 当前只是修补角色设计或导演事实，不应在本阶段绕行。

## Canonical Anchors

| 载体 | 位置 | 作用 |
| --- | --- | --- |
| design master | `projects/<项目名>/4-Design/3-服装/2-设计/第N集/服装设计.json` | panel 的第一输入真源 |
| prompt sidecar | `projects/<项目名>/4-Design/3-服装/2-设计/第N集/costume_design_prompt.json` | 长 prompt、负面约束与渲染提示 |
| panel output root | `projects/<项目名>/4-Design/3-服装/3-面板/第N集/` | 本阶段唯一输出根 |
| layout template | `.agents/skills/aigc/4-Design/3-服装/3-面板/templates/服装面板-提示词.json` | 面板模板真源 |
| runner | `.agents/skills/aigc/4-Design/3-服装/3-面板/scripts/generate_costume_panels.py` | 最小可执行入口 |

## Stage Boundary (Mandatory)

### 本阶段拥有

- 读取 design master 与 prompt sidecar。
- 以固定 template_type `COSTUME_SYSTEM_DOSSIER` 组装 layout JSON。
- 为每套服装写出独立 panel layout JSON 和 episode 级 manifest。
- 把 panel 约束与 identity badge 固定成后续可重复消费的结构化 handoff。

### 本阶段不拥有

- 改写 `服装设计.json` 或 `costume_design_prompt.json`。
- 直接篡改 `角色清单.json` 或 `3-Detail/第N集.json`。
- 自动调用图片生成器写 PNG。
- 再造第二份 panel 模板真源。

## Shared I/O Contract (Mandatory)

### 输入

默认输入根：

- `projects/<项目名>/4-Design/3-服装/2-设计/第N集/服装设计.json`
- `projects/<项目名>/4-Design/3-服装/2-设计/第N集/costume_design_prompt.json`

### 输出

固定输出根：

- `projects/<项目名>/4-Design/3-服装/3-面板/第N集/`

固定输出物：

1. `<costume_id>-<canonical_label>-CostumePanel-layout.json`
2. `_manifest.json`

## Execution Workflow

1. 读取当前项目 `2-设计` episode 根，锁定 `服装设计.json` 是否存在。
2. 读取 `costume_design_prompt.json`，按 `costume_id` 建立 prompt index。
3. 读取固定模板，锁定 `layout_generation_prompt`、`layout_modules` 与 `mandatory_rules`。
4. 针对每套服装合成：
   - identity badge
   - 设计主体 prompt
   - layout prompt
   - 负面约束
5. 写出每套服装的 `CostumePanel-layout.json`。
6. 写回 episode 级 `_manifest.json`，记录输入、输出、degraded mode 与数量统计。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| FIELD-COSTUME-PANEL-01 | 阶段定位 | 明确 `3-面板` 是 design master 下游的 layout handoff，而不是重新设计或直接生图 | S1 | 边界清晰度 | FAIL-COSTUME-PANEL-01 |
| FIELD-COSTUME-PANEL-02 | 输入真源 | 锁定 `服装设计.json + costume_design_prompt.json` 为唯一输入 | S2 | 真源稳定性 | FAIL-COSTUME-PANEL-02 |
| FIELD-COSTUME-PANEL-03 | 模板契约 | 固定 `COSTUME_SYSTEM_DOSSIER + 16:9 + three-column` | S3 | 模板一致性 | FAIL-COSTUME-PANEL-03 |
| FIELD-COSTUME-PANEL-04 | identity badge | 每个 layout 必须写 `<costume_id>+<canonical_label>` 的固定身份标签 | S4 | 可追溯性 | FAIL-COSTUME-PANEL-04 |
| FIELD-COSTUME-PANEL-05 | prompt assembly | 组装 identity / layout / negative prompt，并落成最终 `prompt` | S5 | 可执行性 | FAIL-COSTUME-PANEL-05 |
| FIELD-COSTUME-PANEL-06 | 输出治理 | 每套服装独立 layout，episode 统一 manifest | S6 | 落盘完整性 | FAIL-COSTUME-PANEL-06 |
| FIELD-COSTUME-PANEL-07 | 降级记录 | prompt sidecar 缺失时必须记录 degraded mode | S7 | 审计完整性 | FAIL-COSTUME-PANEL-07 |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-COSTUME-PANEL-01 | 当前是不是 panel layout handoff 问题 | 锁定阶段边界与停点 | 把本阶段写成重新设计或自动生图 |
| S2 | FIELD-COSTUME-PANEL-02 | design master 与 prompt sidecar 是否齐备 | 建立输入根与 prompt index | 回头重扫 `角色清单` 或 `编导` |
| S3 | FIELD-COSTUME-PANEL-03 | 模板是不是唯一真源 | 读取模板并提取 mandatory rules | 本地再造第二套模板结构 |
| S4 | FIELD-COSTUME-PANEL-04 | identity badge 是否稳定可追溯 | 生成 `<costume_id>+<canonical_label>` | 只有名字没有 ID |
| S5 | FIELD-COSTUME-PANEL-05 | prompt 是否足够支持 panel 审阅/下游消费 | 拼装 identity/layout/negative 段 | prompt 缺规则或缺负面约束 |
| S6 | FIELD-COSTUME-PANEL-06 | 输出命名与 episode manifest 是否统一 | 写每套服装 layout 与 manifest | 整集只出一个泛化 JSON |
| S7 | FIELD-COSTUME-PANEL-07 | sidecar 缺失时是否显式标记 | 记录 degraded flags | 静默回退，没有审计痕迹 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| FIELD-COSTUME-PANEL-01 | 阶段边界、停点与上下游职责明确 | FAIL-COSTUME-PANEL-01 | S1 |
| FIELD-COSTUME-PANEL-02 | 输入根固定为 `2-设计` 产物 | FAIL-COSTUME-PANEL-02 | S2 |
| FIELD-COSTUME-PANEL-03 | 模板结构与 `16:9` 布局被稳定执行 | FAIL-COSTUME-PANEL-03 | S3 |
| FIELD-COSTUME-PANEL-04 | 每个 layout 都含稳定 identity badge | FAIL-COSTUME-PANEL-04 | S4 |
| FIELD-COSTUME-PANEL-05 | 最终 prompt 可执行且不丢负面约束 | FAIL-COSTUME-PANEL-05 | S5 |
| FIELD-COSTUME-PANEL-06 | layout 与 manifest 全部落盘且命名正确 | FAIL-COSTUME-PANEL-06 | S6 |
| FIELD-COSTUME-PANEL-07 | 所有降级路径都有 manifest 记录 | FAIL-COSTUME-PANEL-07 | S7 |

## Root-Cause Execution Contract (Mandatory)

当 `3-面板` 出现以下问题时，必须先修源层而不是补单次 JSON：

- 已有 `服装设计.json`，但仍从 `角色清单` 或 `编导` 直接拼 panel prompt。
- template_type、画幅或模块规则漂移。
- 整集只产出一个泛化 panel，而不是逐服装 layout。
- sidecar 缺失时静默回退，没有任何审计记录。

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/3-服装/3-面板/SKILL.md`
  - `.agents/skills/aigc/4-Design/3-服装/3-面板/CONTEXT.md`
  - `.agents/skills/aigc/4-Design/3-服装/3-面板/templates/服装面板-提示词.json`
  - `.agents/skills/aigc/4-Design/3-服装/3-面板/scripts/generate_costume_panels.py`
- `Meta Rule Source`
  - `.agents/skills/aigc/4-Design/3-服装/SKILL.md`
  - `.agents/skills/aigc/4-Design/SKILL.md`
  - 根 `AGENTS.md`

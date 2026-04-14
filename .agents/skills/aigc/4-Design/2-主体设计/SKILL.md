---
name: aigc-design-object-design
description: Use when the `4-Design/2-主体设计` stage needs to route `场景 / 角色 / 服装 / 道具` design skills, inherit design-source artifacts from `1-主体清单`, and aggregate design-stage validation under `projects/aigc/<项目名>/4-Design/`.
governance_tier: full
---

# aigc 4-Design / 2-主体设计

## 概述

`2-主体设计` 是 `4-Design` 阶段承接 `1-主体清单`、连接 `3-面板设计 / 5-Image / 6-Video` 的阶段父 skill。

在标准 handoff 之外，父层允许一个受控的自动生图快路径：

- 当用户显式要求“自动生图 / 自动调用 nano-banana”时，可在 design master 已稳定后直接调用 `.agents/skills/api/image/nano-banana/general/SKILL.md`
- 该快路径只消费设计阶段已稳定的 prompt carrier，不重新发明 prompt，不替代 `5-Image` 的请求蒸馏/参照绑定/多 provider 编排真源

当前 active 子技能固定为：

1. `场景`
2. `角色`
3. `服装`
4. `道具`

父层拥有：

- `design-source -> design master` 的阶段入口判定
- 跨域 selective dispatch 与批次裁决
- `角色 -> 服装` 的软依赖门
- 各域 canonical 设计真源的覆盖率与 handoff 一致性检查
- `auto-image-fast-path` 的触发裁决、prompt 引用优先级与 provider 统一入口
- `projects/aigc/<项目名>/4-Design/validation-report.md` 的设计阶段验收摘要

父层不拥有：

- 直接写某一域的 canonical 设计产物
- 代替子技能内部 capability mirror 或 direct leaf 细则
- 把 prompt sidecar 升格为 design master
- 跳过 `1-主体清单` 直接发明设计事实

## Stage Coverage Status

| 单元 | 当前状态 | 第一输入根 | canonical 输出 |
| --- | --- | --- | --- |
| `场景` | active | `场景清单.json` | `场景设计.json + <scene_key>.md` |
| `角色` | active | `角色清单.json` | `character_design.json + [角色名].md` |
| `服装` | active | `costume_design_bridge.json` | `服装设计.json + costume_design_prompt.json + 设计卡` |
| `道具` | active | `prop_design_bridge.json` | `道具设计.json + prop_design_prompt.json + _manifest.json` |

## Shared Canonical Sources (Mandatory)

- 强制读取：`.agents/skills/aigc/4-Design/1-主体清单/SKILL.md`
- 强制读取：`.agents/skills/aigc/4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
- 强制读取：`.agents/skills/aigc/_shared/project-runtime-layout.md`
- 强制读取：`.agents/skills/aigc/3-Detail/SKILL.md`
- 强制读取：`.agents/skills/api/image/nano-banana/SKILL.md`
- 强制读取：`.agents/skills/api/image/nano-banana/general/SKILL.md`
- 强制读取：`场景/SKILL.md`
- 强制读取：`角色/SKILL.md`
- 强制读取：`服装/SKILL.md`
- 强制读取：`道具/SKILL.md`

硬规则：

1. 任一设计域都必须从本域 `1-主体清单` 输出起步，不得直接绕回 `3-Detail` 当第一输入根。
2. `design master` 永远先于 `prompt sidecar / panel packet / image request`。
3. 同时命中 `角色` 与 `服装` 时，默认先更新 `角色`，再决定 `服装` 是否需要跟进。
4. 父层只做路由与验收，不建立跨域 `design_master_of_masters`。
5. `auto-image-fast-path` 只能读取已稳定 design carrier 中的 prompt 字段，不得跳过 design master / sidecar 直接临场拼 prompt。
6. 自动生图产物是 derived assets，不得反向覆盖任一域的 canonical design truth。

## Context Preload (Mandatory)

加载顺序固定为：

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/4-Design/SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/3-Detail/SKILL.md + CONTEXT.md`
5. `.agents/skills/aigc/4-Design/1-主体清单/SKILL.md + CONTEXT.md`
6. 本 `SKILL.md + CONTEXT.md`
7. `.agents/skills/aigc/4-Design/1-主体清单/_shared/detail-output-consumption-contract.md`
8. `.agents/skills/aigc/_shared/project-runtime-layout.md`
9. `.agents/skills/api/image/nano-banana/SKILL.md`
10. `.agents/skills/api/image/nano-banana/general/SKILL.md + CONTEXT.md`
11. `场景/SKILL.md + CONTEXT.md`
12. `角色/SKILL.md + CONTEXT.md`
13. `服装/SKILL.md + CONTEXT.md`
14. `道具/SKILL.md + CONTEXT.md`
15. `projects/aigc/<项目名>/0-Init/north_star.yaml`
16. `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
17. `projects/aigc/<项目名>/2-Global/全局风格.md`
18. `projects/aigc/<项目名>/2-Global/类型元素.md`
19. `projects/aigc/<项目名>/3-Detail/第N集.json`
20. 各域 `1-主体清单` 产物与已存在 `2-主体设计` 输出（若存在）

## Total Input Contract (Mandatory)

### 必需输入

- `projects/aigc/<项目名>/0-Init/north_star.yaml`
- `projects/aigc/<项目名>/0-Init/init_handoff.yaml`
- `projects/aigc/<项目名>/2-Global/全局风格.md`
- `projects/aigc/<项目名>/2-Global/类型元素.md`

### 条件必需输入

- `场景`：`4-Design/场景/1-清单/第N集/场景清单.json`
- `角色`：`4-Design/角色/1-清单/第N集/角色清单.json`
- `服装`：`4-Design/服装/1-清单/第N集/costume_design_bridge.json`
- `道具`：`4-Design/道具/1-清单/第N集/prop_design_bridge.json`

### 可选输入

- `projects/aigc/<项目名>/3-Detail/第N集.json`
- `projects/aigc/<项目名>/2-Global/导演意图.md`
- 已存在的各域 `2-主体设计` 输出
- 用户显式指定的 `selected_domains[] / selected_roles[] / selected_scenes[] / selected_props[] / selected_costumes[]`

### 硬规则

1. 父层先判域，再读取该域的最小 design-source bundle。
2. 若桥接文件缺失，必须回退到 `1-主体清单`，而不是在设计阶段补猜。
3. 若本轮只是 prompt-only 或 partial-refresh，也必须先读取现有 design master。
4. 父层不得因为某一域 blocked 就隐式跳过其输入缺口并宣称全局完成。

## Route And Topology Contract (Mandatory)

### 默认模式

1. `single-domain`
2. `multi-domain`
3. `full-build`
4. `incremental-repair`
5. `auto-image-fast-path`

### 路由规则

1. 需要从对象池进入结构化设计时，统一先进入 `2-主体设计`。
2. `场景`、`角色`、`道具` 可以按 scope 独立命中。
3. `服装` 可独立命中，但当本轮同时刷新角色设计时，默认等待角色设计先稳定。
4. 全量构建时，默认先跑 `场景 + 角色 + 道具`，再决定 `服装` 是否跟进。
5. 若用户只要某一域的 design master 或 prompt sidecar，本轮不得补跑其他域。
6. 若用户显式要求“设计后直接自动生图”，且命中对象已具备稳定 prompt carrier，则可进入 `auto-image-fast-path`。
7. `auto-image-fast-path` 只适用于 design-derived 单体/单域概念图；分镜组、批量 story request、参照绑定或 provider 选择仍进入 `5-Image`。

## Auto-Image Fast Path Contract (Mandatory)

### 目标与边界

`auto-image-fast-path` 只解决一类问题：

- design master 已稳定
- 用户明确要“顺手出图 / 自动生图 / 直接调 nano-banana”
- 当前需求是单域或少量命中对象的概念图，而不是完整 `5-Image` 请求链

它不替代：

- `.agents/skills/aigc/5-Image/1-提示词蒸馏`
- `.agents/skills/aigc/5-Image/2-参照引用`
- `.agents/skills/aigc/5-Image/3-图像生成`

### 固定 provider

- handoff skill：`.agents/skills/api/image/nano-banana/general/SKILL.md`
- API 契约父级：`.agents/skills/api/image/nano-banana/SKILL.md`
- 默认调用脚本：`python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`

### Prompt 引用优先级表

| 域 | 第一引用 | 允许回退 | 备注 |
| --- | --- | --- | --- |
| `场景` | `场景设计.json.scene_designs[].final_scene_prompt` | `prompt_integration` | `final_scene_prompt` 是兼容下游消费字段，优先级最高 |
| `角色` | `character_design.json.roles[].prompt_integration` | 无 | 直接使用角色设计真源中的整合 prompt |
| `服装` | `costume_design_prompt.json.costumes[].prompt_cn` | 无 | 必须走 prompt sidecar，不得回退到 design facts 临场改写 |
| `道具` | `prop_design_prompt.json.props[].prompt_cn` | 无 | 必须走 prompt sidecar，不得跳过 `prop_design_prompt.json` |

### Prompt 组装硬规则

1. 先锁定 design master / prompt sidecar，再取 prompt 文本。
2. prompt 缺失时必须阻塞并回到对应 design 子技能补真源，不得在父层临时重写。
3. `negative_constraints`、`reverse_taboos`、`render_hints` 等约束字段允许作为补充约束并入，但不得覆盖主 prompt 的真源位置。
4. 若本地已存在明确参照图资产，可按 `I2I` 方式传给 `nano-banana/general`；若没有稳定参照图，则按 `T2I` 调用。
5. 自动生图默认沿用 `nano-banana/general` 的输出约定；生成图片属于 derived asset，不升格为 design master。

### 最小调用合同

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --project-name "<项目名>" \
  --task-kind project \
  --caller-skill ".agents/skills/aigc/4-Design/2-主体设计" \
  --episode-id "<第N集>" \
  --prompt "<resolved_prompt_from_design_carrier>" \
  --no-report
```

若已有稳定参照图，可额外附带：

```bash
--image-url "<existing_reference_image_path_or_url>"
```

若当前已经知道更细的叶子技能来源，优先把 `--caller-skill` 细化到：

- `.agents/skills/aigc/4-Design/2-主体设计/场景`
- `.agents/skills/aigc/4-Design/2-主体设计/角色`
- `.agents/skills/aigc/4-Design/2-主体设计/服装`
- `.agents/skills/aigc/4-Design/2-主体设计/道具`

这样脚本会把默认图片输出目录进一步收束到对应域的 `projects/aigc/<项目名>/4-Design/<域>/2-设计/<第N集>/generated/`。

## Canonical Output Governance (Mandatory)

| 领域 | canonical design master | secondary outputs | audit sidecar |
| --- | --- | --- | --- |
| `场景` | `场景设计.json` | `<scene_key>.md` | `_manifest.json`（可选） |
| `角色` | `character_design.json` | `[角色名].md` | `_manifest.json` |
| `服装` | `服装设计.json` | `costume_design_prompt.json`、设计卡 | `_manifest.json` |
| `道具` | `道具设计.json` | `prop_design_prompt.json` | `_manifest.json` |

父层补充规则：

1. 各域只在自己的 runtime 下写 canonical design truth。
2. 父层只汇总 dispatch、blocked domains、handoff readiness 到 `projects/aigc/<项目名>/4-Design/validation-report.md`。
3. prompt sidecar、Markdown 卡片、设计卡都不得反向覆盖 design master。
4. 下游 `3-面板设计` 只能消费已稳定写出的 design carrier。
5. `auto-image-fast-path` 的图片产物不进入本表的 canonical truth；它们只是从 design carrier 派生出的 provider 资产。

## Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-DESIGN-STAGE-01` | 阶段定位 | 锁父层只做路由、依赖门、验收 | `S1` | 边界清晰度 | `FAIL-DESIGN-STAGE-01` |
| `FIELD-DESIGN-STAGE-02` | 调度与批次 | 写清命中域、full-build 顺序与 dependency gate | `S2` | 路由完整性 | `FAIL-DESIGN-STAGE-02` |
| `FIELD-DESIGN-STAGE-03` | 输入 bundle | 固定 design-source、global、init、detail 的装配顺序 | `S3` | 真源一致性 | `FAIL-DESIGN-STAGE-03` |
| `FIELD-DESIGN-STAGE-04` | 输出治理 | 固定 design master 与 secondary outputs 分层 | `S4` | 输出治理 | `FAIL-DESIGN-STAGE-04` |
| `FIELD-DESIGN-STAGE-05` | 验收回接 | 锁 `3-面板设计 / 5-Image / 6-Video` handoff | `S5` | 闭环完整性 | `FAIL-DESIGN-STAGE-05` |
| `FIELD-DESIGN-STAGE-06` | 自动生图快路径 | 固定 `nano-banana/general` 入口与 prompt 引用优先级 | `S6` | provider handoff 正确性 | `FAIL-DESIGN-STAGE-06` |

## Thought Pass Map

| step_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `S1` | `FIELD-DESIGN-STAGE-01` | 当前是不是设计阶段父级问题 | 锁父子边界与不拥有项 | 父层越权写某域设计稿 |
| `S2` | `FIELD-DESIGN-STAGE-02` | 本轮命中哪些域、顺序怎样 | 写 route 与 dependency gate | 多域构建没有批次规则 |
| `S3` | `FIELD-DESIGN-STAGE-03` | design-source 与 global/init 是否装配正确 | 回指输入 bundle 顺序 | 设计阶段重新扫描 detail 代替对象池/bridge |
| `S4` | `FIELD-DESIGN-STAGE-04` | design master 与 sidecar 是否分层 | 写输出治理表 | prompt 或卡片反向污染主稿 |
| `S5` | `FIELD-DESIGN-STAGE-05` | 如何证明设计阶段已可交给下游 | 写 validation 摘要与 handoff | 没有下游入口或返工口 |
| `S6` | `FIELD-DESIGN-STAGE-06` | 自动生图是否走对 provider，并且 prompt 引用是否来自真源 | 锁定 `nano-banana/general` 与 prompt 引用表 | 直接手写 prompt，或把自动生图误当成 `5-Image` 替代品 |

## Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-DESIGN-STAGE-01` | 父层职责、子层职责与不拥有项明确 | `FAIL-DESIGN-STAGE-01` | `S1` |
| `FIELD-DESIGN-STAGE-02` | 多域路由、批次与依赖门明确 | `FAIL-DESIGN-STAGE-02` | `S2` |
| `FIELD-DESIGN-STAGE-03` | design-source、global、init、detail 输入顺序稳定 | `FAIL-DESIGN-STAGE-03` | `S3` |
| `FIELD-DESIGN-STAGE-04` | design master 与 secondary outputs 分层稳定 | `FAIL-DESIGN-STAGE-04` | `S4` |
| `FIELD-DESIGN-STAGE-05` | `validation-report` 与 `3-面板设计` handoff 明确 | `FAIL-DESIGN-STAGE-05` | `S5` |
| `FIELD-DESIGN-STAGE-06` | `nano-banana/general` 入口唯一，且 prompt 来源按域稳定回链 | `FAIL-DESIGN-STAGE-06` | `S6` |

## Root-Cause Execution Contract (Mandatory)

当 `2-主体设计` 出现以下问题时，必须先修源层而不是补单次设计稿：

- 某一域跳过 `1-主体清单` 直接造设计事实
- design master 与 prompt sidecar 混层
- `角色` 与 `服装` 同轮改动但没有依赖门
- 下游 `3-面板设计` 需要重新猜 design carrier
- 自动生图读取了错误 prompt，或父层临时重写 prompt 绕过 design carrier

必经链路：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/4-Design/2-主体设计/SKILL.md`
  - 四个子技能 `SKILL.md`
  - `.agents/skills/aigc/4-Design/1-主体清单/SKILL.md`
  - `.agents/skills/api/image/nano-banana/general/SKILL.md`
- `Meta Rule Source`
  - `AGENTS.md`
  - `.agents/skills/aigc/SKILL.md`
  - `.agents/skills/aigc/3-Detail/SKILL.md`

面向用户的闭环固定返回：

1. root cause location
2. immediate fix
3. systemic prevention fix

## Completion Criteria

- 已建立 `2-主体设计` 父级阶段合同
- 已锁定四域 design-source 输入与 canonical 输出边界
- 已明确 `角色 -> 服装` 的软依赖门与 multi-domain 批次规则
- 已给出 `projects/aigc/<项目名>/4-Design/validation-report.md` 的设计阶段验收回接
- 已给出 `auto-image-fast-path` 的适用边界、`nano-banana/general` 唯一入口与四域 prompt 引用优先级表

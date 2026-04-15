---
name: aigc-image-reference-binding
description: Use when a `5-Image` request JSON from `1-提示词蒸馏` must bind or normalize local image references for `即梦 CLI` local-path handoff, `NANO-banana` BASE64-compatible handoff, or dual-compatible image-generation preparation.
governance_tier: full
---

# aigc 5-Image / 2-参照引用

## Mode Selection

- 当前任务属于 `原生创建 + 既有优化`：目录已存在但无真源合同，且必须承接 `1-提示词蒸馏` 的既有请求 JSON。
- `复杂链路的骨架 / 细则分层 = true`：本 `SKILL.md` 负责总输入、总输出、路由、节点与验收；provider-specific 细则下沉到 `references/`。
- 默认工作模式不是单 provider 绑定，而是 `dual_mode`：先保持 provider-neutral 引用真源，再按目标 provider 解析为 `即梦 CLI` 本地路径或 `NANO-banana` BASE64 兼容载体。

## 概述

`2-参照引用` 是 `5-Image` 阶段里承接“稳定请求对象 -> 本地图片引用绑定 -> provider-ready 引用解析骨架 -> 严格校验”的叶子父技能。

它不重新写 prompt，也不直接生成图片。它只负责把已经存在于项目本地的图片资产，绑定进 `reference_images / image_markers`，并把同一批引用准备成：

1. `即梦 CLI` 可直接消费的本地图片路径
2. `NANO-banana` 可继续编码为 BASE64 的兼容槽位
3. 若 provider 尚未锁定，则维持 `dual_mode` 可续跑态

## Single Truth Boundary

### `2-参照引用` 拥有

- 从 `1-提示词蒸馏` 请求 JSON 绑定本地图片引用的总合同
- provider-neutral `reference_images / image_markers` 真源
- `jimeng_cli / nano_banana / dual_mode` 三种引用模式裁决
- 绑定后 `第N集.json + _manifest.json + match-report.md` 的落盘与严格校验

### `2-参照引用` 不拥有

- 改写 `1-提示词蒸馏` 的 prompt 或镜头事实
- 直接进入 provider 提交
- 伪造网络 URL、外部路径或不存在的图片
- 在有歧义时猜测性绑定

## Shared Canonical Sources (Mandatory)

- `.agents/skills/aigc/SKILL.md`
- `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md`
- `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
- `projects/aigc/<项目名>/5-Image/分镜故事板/<第N集>/<第N集>.json`
- `projects/aigc/<项目名>/5-Image/分镜帧/<第N集>/<第N集>.json`
- `projects/aigc/<项目名>/5-Image/漫画/<第N集>/<第N集>.json`
- `projects/aigc/<项目名>/Assets/`
- `projects/aigc/<项目名>/4-Design/`
- [references/jimeng-cli.md](references/jimeng-cli.md)
- [references/nano-banana.md](references/nano-banana.md)

硬规则：

1. `1-提示词蒸馏` 请求 JSON 是第一请求真源。
2. `reference_images / image_markers` 是本阶段唯一引用真源。
3. provider-specific 解析结果只能写进 `image_markers[].provider_variants.*`，不得覆盖 provider-neutral `image_ref / ref_kind`。
4. 若 provider 未锁定，默认保持 `dual_mode`，不得提前丢掉另一种兼容槽位。

## Reference Module Selection Contract

### 固定模块

- `即梦 CLI` 模块：`references/jimeng-cli.md`
- `NANO-banana` 模块：`references/nano-banana.md`

### 选择机制

1. 用户显式要求 `即梦 CLI`：加载 `references/jimeng-cli.md`
2. 用户显式要求 `NANO-banana`：加载 `references/nano-banana.md`
3. 用户要求“双模式”或未明确 provider：同时加载两个模块，并进入 `dual_mode`
4. `dual_mode` 下的默认策略：
   - provider-neutral 真源始终写入本地 canonical `image_ref`
   - `jimeng_cli` 变体立即解析为本地路径
   - `nano_banana` 变体默认标记为 `pending_encode`，由 `3-图像生成` 再决定是否实编码为 BASE64

## Business Requirement Analysis Contract (Mandatory)

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把 `1-提示词蒸馏` 的 image-request JSON 绑定到真实本地图片，并保持 provider-neutral + provider-specific 双层兼容。 |
| `business_object` | `1-提示词蒸馏` 输出 JSON、项目本地图片资产、共享 image-generation 模板。 |
| `constraint_profile` | 只绑定本地真实文件；外部 URL 不是本阶段主真源；`即梦 CLI` 需要本地路径；`NANO-banana` 需要 BASE64-compatible 槽位；provider 未锁定时不得过早丢失兼容性。 |
| `success_criteria` | `reference_images / image_markers` 能回链真实本地文件；`jimeng_cli` 本地路径 ready；`nano_banana` 兼容槽位 ready 或 pending_encode；三件套落盘可复核。 |
| `non_goals` | 不生成图片、不直接提交 provider、不重新改 prompt、不伪造远程资源。 |
| `complexity_source` | 当前复杂度来自 provider-neutral 与 provider-specific 双层并存、来源资产判型、歧义控制和双模式选择。 |
| `topology_fit` | 采用“串行主干 + provider 模块侧支 + 最终汇流”拓扑：先锁输入，再定位图片资产，再按 provider 模块写兼容槽位，最后统一审计。 |
| `step_strategy` | 主合同只写总路由、主节点、验收与落盘；provider-specific 细则放在两个 reference 模块。 |

## Context Preload (Mandatory)

1. 根 `AGENTS.md`
2. `.agents/skills/aigc/SKILL.md + CONTEXT.md`
3. `.agents/skills/aigc/5-Image/SKILL.md + CONTEXT.md`
4. `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md + CONTEXT.md`
5. 本 `SKILL.md + CONTEXT.md`
6. `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`
7. 命中的 `1-提示词蒸馏` 请求 JSON
8. `projects/aigc/<项目名>/Assets/` 与 `projects/aigc/<项目名>/4-Design/`
9. 命中的 `references/*.md`

## Total Input Contract (Mandatory)

### 必需输入

- 一份来自 `1-提示词蒸馏` 的稳定请求 JSON
- `.agents/skills/aigc/5-Image/_shared/image-generation-input.template.json`

### 推荐输入

- `projects/aigc/<项目名>/Assets/`
- `projects/aigc/<项目名>/4-Design/`
- 用户或上游显式给出的 `provider_mode`

### Readiness Gate

进入绑定前必须确认：

1. 请求 JSON 已存在 `meta / prompt_style / model / prompt / prompt_char_count`
2. `model.reference_images` 与 `model.image_markers` 字段存在
3. 若 `meta.source_tranche` 缺失，可从路径或 `shot_level` 推断
4. 引用来源必须是本地文件，不是外部 URL 主链

## Canonical Landing

- 根目录：`projects/aigc/<项目名>/5-Image/2-参照引用/`
- 模式目录：`projects/aigc/<项目名>/5-Image/2-参照引用/<jimeng_cli|nano_banana|dual_mode>/<source_tranche>/<第N集>/`
- 主文件：`projects/aigc/<项目名>/5-Image/2-参照引用/<mode>/<source_tranche>/<第N集>/<第N集>.json`
- manifest：`projects/aigc/<项目名>/5-Image/2-参照引用/<mode>/<source_tranche>/<第N集>/_manifest.json`
- 报告：`projects/aigc/<项目名>/5-Image/2-参照引用/<mode>/<source_tranche>/<第N集>/match-report.md`

## Topology Contract (Mandatory)

- 主干节点：
  - `R0 输入锁定`
  - `R1 请求对象审计`
  - `R2 引用候选推导`
  - `R3 本地图片匹配`
  - `R4 provider 模式解析`
  - `R5 写回与审计`
- 条件支路：
  - `B1 即梦 CLI 模块`
  - `B2 NANO-banana 模块`
- 只有 `R5` 可宣告完成

## Visual Maps

```mermaid
flowchart TD
    A["R0 输入锁定"] --> B["R1 请求对象审计"]
    B --> C["R2 推导候选引用"]
    C --> D["R3 匹配本地图片"]
    D --> E["R4 按 provider 模块解析"]
    E --> F["R5 写回与审计"]
    F --> G["输出 2-参照引用 三件套"]
```

```mermaid
flowchart TD
    A["R4 provider 模式解析"] --> B{"provider_mode"}
    B -->|"jimeng_cli"| C["B1 读取 references/jimeng-cli.md"]
    B -->|"nano_banana"| D["B2 读取 references/nano-banana.md"]
    B -->|"dual_mode"| E["同时读取两个模块"]
    C --> F["写 local_path ready 槽位"]
    D --> G["写 base64 compatible 槽位"]
    E --> H["同时保留两种槽位"]
```

```mermaid
stateDiagram-v2
    [*] --> IntakeLocked
    IntakeLocked --> RequestAudited
    RequestAudited --> AssetsMatched
    AssetsMatched --> ProviderResolved
    ProviderResolved --> Audited
    Audited --> [*]
    AssetsMatched --> Blocked
    ProviderResolved --> Blocked
```

## Thinking-Action Node Network

| node_id | objective | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- |
| `R0-intake-lock` | 锁定 source request 与目标模式 | 读取输入 JSON，决定 `jimeng_cli / nano_banana / dual_mode` | `intake_note` | `R1` | 未锁模式不得继续 |
| `R1-request-audit` | 校验请求对象结构与模板兼容性 | 检查 `meta/prompt/model`、引用骨架、source tranche | `request_audit` | `R2` 或阻断 | 空壳请求不得继续 |
| `R2-candidate-derive` | 推导该绑定哪些本地图片 | 从 `source_tranche / group_id / shot_id / related_subject` 推导候选 | `candidate_requests` | `R3` | 无依据不得猜测绑定 |
| `R3-local-match` | 绑定真实本地图片 | 扫描 `Assets/` 与 `4-Design/`，锁定唯一文件 | `match_results` | `R4` 或阻断 | 歧义文件不得放行 |
| `R4-provider-resolve` | 生成 provider-specific 兼容槽位 | 按命中 reference 模块写 `provider_variants.*` | `provider_resolution_note` | `R5` | 未写明 provider 兼容态不得结束 |
| `R5-writeback-audit` | 写回三件套并审计 | 落盘 JSON/manifest/report，给出下一入口 | `validation_report` | `Done` | 仅本节点可宣告完成 |

## Workflow

1. 读取 `1-提示词蒸馏` 请求 JSON。
2. 审计模板字段是否兼容 `v2` 双模式骨架；若是旧 `image_url` 结构，统一升级为 `image_ref + ref_kind + provider_variants`。
3. 从路径、`shot_level`、`group_id`、`source_shot_ids`、`related_subject` 推导图片候选。
4. 在 `Assets/` 与 `4-Design/` 中只绑定真实本地图片。
5. 按 provider 模式写入：
   - `jimeng_cli`: `resolved_input=本地路径`，`resolution_status=ready`
   - `nano_banana`: 默认 `resolved_input=""`，`resolution_status=pending_encode`
   - `dual_mode`: 同时保留两种槽位
6. 写回 `2-参照引用` 三件套。

## Output Contract

最低交付：

1. 绑定后的 `第N集.json`
2. `_manifest.json`
3. `match-report.md`
4. `next_entry`

硬规则：

1. `reference_images[]` 只存 canonical 本地图片引用。
2. `image_markers[].image_ref` 与 `reference_images[]` 必须一一可回链。
3. `image_markers[].provider_variants.jimeng_cli.resolved_input` 只能是本地路径。
4. `image_markers[].provider_variants.nano_banana.resolution_status` 允许为 `pending_encode`，但不得写入虚构 BASE64。
5. 若 `provider_mode=dual_mode`，不得删除任何一方 provider 槽位。

## Root-Cause Execution Contract (Mandatory)

当出现以下症状时，先修本技能源层：

- 请求对象已存在，但引用字段仍是旧 `image_url`
- `即梦 CLI` 槽位被写成 URL 或外部路径
- `NANO-banana` 槽位提前塞入伪 BASE64
- 双模式下只保留了一边 provider 槽位
- `3-图像生成` 收到的请求对象仍无法判断 provider 输入该怎么解析

链路固定为：

`Symptom -> Direct Technical Cause -> Rule Source -> Meta Rule Source -> Fix Landing Points`

优先检查：

- `Rule Source`
  - `.agents/skills/aigc/5-Image/2-参照引用/SKILL.md`
  - `.agents/skills/aigc/5-Image/2-参照引用/CONTEXT.md`
  - `.agents/skills/aigc/5-Image/2-参照引用/references/jimeng-cli.md`
  - `.agents/skills/aigc/5-Image/2-参照引用/references/nano-banana.md`
- `Meta Rule Source`
  - `.agents/skills/aigc/5-Image/1-提示词蒸馏/SKILL.md`
  - `.agents/skills/aigc/SKILL.md`
  - 根 `AGENTS.md`

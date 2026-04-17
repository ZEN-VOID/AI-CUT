---
name: video-api
description: Use when the task needs to choose, route, or maintain provider-specific video generation skills under `.agents/skills/api/video`, especially when the user names a provider loosely, only describes capability shape, or a cross-provider source-layer fix is required.
governance_tier: full
---

# 视频 API 路由父技能

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md` > 子技能 `SKILL.md` > 子技能 `CONTEXT.md`。

## 1. 作用范围

- 本文件是 `.agents/skills/api/video/` 的父级路由与治理真源，不直接发起具体 provider 请求。
- 父技能职责：
  - 统一解释“视频生成”用户意图。
  - 在现有 provider 子技能之间做单一路由。
  - 维护跨 provider 的输入语义、闭环预期、输出目录与失败上溯口径。
  - 在出现跨子技能重复问题时，优先修父级路由规则或共享表述，而不是在每个子技能里各修一遍。
- 子技能职责：
  - 维护 provider 专属接口契约、字段映射、脚本入口、轮询/下载闭环与本地经验层。
- 父技能不拥有第二份平行 payload 模板。
  - 具体请求体、脚本参数和 provider 特有字段，始终以下钻后的子技能 `SKILL.md` 为准。

## 2. 子技能索引

| 子技能 | 路径 | 当前职责摘要 | 闭环状态 |
| --- | --- | --- | --- |
| `grok` | `grok/` | FineAPI `POST /v1/video/create`，Grok Video 3 创建任务 | `create-only` |
| `kling` | `kling/` | FineAPI Kling 图生视频，`submit/status/download/run` | `full-loop` |
| `luma` | `luma/` | Luma Ray，文生/首帧/首尾帧，`submit/status/download/run` | `full-loop` |
| `minimax` | `minimax/` | FineAPI Hailuo / MiniMax 创建任务 | `create-only` |
| `runway` | `runway/` | Runway image-to-video，`submit/status/download/run` | `full-loop` |
| `seedance` | `seedance/` | Seedance，文生/首帧/首尾帧/多模态，`submit/status/download/run` | `full-loop` |
| `sora` | `sora/` | OpenAI Sora 2，经 AnyFast 接口提交与闭环下载 | `full-loop` |
| `veo` | `veo/` | Google Veo，经 `/v1/video/create` 创建任务 | `create-only` |
| `vidu` | `vidu/` | Vidu，经 `/v1/video/generations` 创建任务 | `create-only` |

## 3. 路由原则（Mandatory）

### 3.1 一级优先级：显式 provider / 显式接口命中

- 用户直接点名 provider、模型族、脚本、端点或字段形态时，必须直达对应子技能，不做“智能改投”。
- 显式命中示例：
  - `Sora / OpenAI / /v1/videos` -> `sora/`
  - `Runway / /runwayml/v1/image_to_video` -> `runway/`
  - `Seedance / seedance-fast / reference_audio` -> `seedance/`
  - `Luma / ray-2 / /luma/generations` -> `luma/`
  - `Kling / /kling/v1/videos/image2video` -> `kling/`
  - `Veo / Grok / Vidu / Hailuo / MiniMax` -> 对应 provider 子技能

### 3.2 二级优先级：能力形态命中

- 当用户没点名 provider，只描述能力形态时，按下表路由：

| 能力形态 / 约束 | 默认路由 |
| --- | --- |
| 只说“OpenAI Sora / remix / `/v1/videos`” | `sora/` |
| 只说“Runway 风格图生视频” | `runway/` |
| 只说“Luma Ray / start-end frame” | `luma/` |
| 只说“Seedance 多模态 / 首尾帧 / 参考音频” | `seedance/` |
| 只说“Kling 图生视频” | `kling/` |
| 只说“Google Veo 创建任务” | `veo/` |
| 只说“Grok Video 3 创建任务” | `grok/` |
| 只说“Vidu 创建任务” | `vidu/` |
| 只说“Hailuo / 海螺 / MiniMax 创建任务” | `minimax/` |

### 3.3 三级优先级：未指定 provider 时的默认裁决

- 用户未指定 provider 时，先判断是否要求完整闭环：
  - 若要求 `提交 -> 轮询 -> 下载`，优先在 `full-loop` 子技能中选。
  - 若任务本身只要求“创建回执”或已知目标 provider 当前只有创建接口真源，允许进入 `create-only` 子技能。
- 未指定 provider 且只给功能描述时，默认按以下最小路由：
  - 纯文本生视频，且希望完整闭环：优先 `sora/` 或 `seedance/`；若用户更强调 OpenAI 生态，走 `sora/`，否则走 `seedance/`。
  - 单张首帧图生视频：优先 `runway/`、`luma/`、`seedance/`；若还要求首尾帧或多模态参考，优先 `seedance/`。
  - 首尾帧图生视频：优先 `luma/` 或 `seedance/`。
  - 多模态参考（图/视频/音频混合）：优先 `seedance/`。
  - 只要求“当前 provider 能否创建任务并返回 receipt”：允许进入 `grok/`、`veo/`、`vidu/`、`minimax/` 这类 `create-only` 子技能。

### 3.4 Tie-Break 规则

- 同时满足多个子技能时，按以下顺序裁决：
  1. 用户显式 provider / endpoint / model family。
  2. 是否要求 `full-loop`。
  3. 输入媒体拓扑是否被子技能原生支持。
  4. 子技能当前真源是否稳定且与用户目标完全贴合。
  5. 若仍并列，优先路由到约束更少、闭环更完整的子技能。

## 4. 统一输入与输出契约（Mandatory）

### 4.1 输入收束

- 父技能层只做这些统一语义收束：
  - `prompt`
  - `images / image_url / image_infos / first_frame / last_frame`
  - `video references`
  - `audio references`
  - `project_name`
  - 是否要求 `create-only` 或 `full-loop`
- 父技能不得把不同 provider 的字段直接拼成一份“通用 payload”。
- 一旦完成 provider 路由，字段命名必须立即切回子技能合同。

### 4.2 输出预期

- 默认项目化输出目录由子技能决定，父技能只维护统一认知：
  - 子技能默认目录一般落在 `output/影片/[项目名]/5-API/video/<provider>/`
  - 若子技能合同声明了别的项目化运行时路径，以子技能为准。
- 父技能统一区分两类输出：
  - `create-only`：任务回执、请求摘要、诊断提示、原始响应。
  - `full-loop`：创建回执 + 状态轮询摘要 + 成片下载结果 + 项目化落盘路径。
- 不得把 `create-only` 子技能包装成已经下载成片的闭环技能。

### 4.3 复合治理边界

- 父技能只做单一路由，不并行混投多个 provider。
- 同一轮任务默认只进入一个子技能，除非用户明确要求横向比较或迁移。
- 若确需比较多个 provider，必须把每个 provider 的结果视为独立 sidecar，不合并成一份伪统一业务真相。

## 5. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-VIDEO-API-01` | 路由输入摘要：`provider_hint / endpoint_hint / capability_shape / lifecycle_need` | 用户意图被完整归一，显式 provider 与隐式能力不混淆 | 用户请求、命名线索、接口线索 | Step 1 | 输入收束完整度 | `FAIL-VIDEO-API-INPUT` |
| `FIELD-VIDEO-API-02` | 路由结论：`selected_skill / selected_reason / rejected_alternatives` | 只选一个子技能，路由理由可解释 | 子技能合同、父级路由规则 | Step 2 | 路由正确性 | `FAIL-VIDEO-API-ROUTE` |
| `FIELD-VIDEO-API-03` | 子技能移交摘要：`expected_action / expected_closure / handoff_fields` | 移交后不再混写跨 provider 字段 | 父技能合同、子技能 `SKILL.md` | Step 3 | 移交契约稳定性 | `FAIL-VIDEO-API-HANDOFF` |
| `FIELD-VIDEO-API-04` | 输出预期：`output_class / runtime_path_family / report_shape` | `create-only` 与 `full-loop` 被清晰区分 | 子技能输出约定 | Step 4 | 输出边界清晰度 | `FAIL-VIDEO-API-OUTPUT` |
| `FIELD-VIDEO-API-05` | 失败上溯：`symptom / direct_cause / rule_source / meta_rule_source` | 问题可上溯到父级或子技能真源 | 父级合同、子技能合同、仓库 AGENTS | Step 5 | 根因闭环完整性 | `FAIL-VIDEO-API-RCA` |

## 6. 思维导引与执行流程（Mandatory）

### 6.1 固定步骤

1. **Step 1 / 意图收束**
   - 识别用户是否显式点名 provider、端点、模型族或脚本。
   - 识别任务是否要求 `create-only` 还是 `full-loop`。
2. **Step 2 / 单一路由裁决**
   - 按本文件第 3 节做单一路由。
   - 明确说明为什么不走其他相邻 provider。
3. **Step 3 / 子技能移交**
   - 只保留与目标子技能有关的输入字段。
   - 立即切换到目标子技能的字段与脚本语义。
4. **Step 4 / 输出边界确认**
   - 先确认目标子技能是 `create-only` 还是 `full-loop`。
   - 再按子技能合同执行并解释输出。
5. **Step 5 / 失败上溯与修源层**
   - 若问题出在 provider 特有字段、脚本或接口漂移，优先修子技能。
   - 若问题出在多个 provider 共享的 Base URL 回退链、通用 host 误用或 `200 + HTML` 伪成功模式，优先把该模式上提到父级经验层，再回落到受影响子技能。
   - 若问题出在 provider 误路由、父级索引缺失、闭环类型误判或共享表述漂移，优先修本父技能。

### 6.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-VIDEO-API-01` | 用户是在点名 provider，还是只描述能力形态？ | 收束 provider / endpoint / capability / lifecycle 线索 | provider 明明已显式给出，却仍被当成模糊意图 |
| `Step 2` | `FIELD-VIDEO-API-02` | 当前到底该进哪个子技能？ | 生成单一路由结论和拒绝理由 | 同时想进多个子技能，或把 create-only 误当 full-loop |
| `Step 3` | `FIELD-VIDEO-API-03` | 移交后是否还残留其他 provider 的字段心智？ | 切换为子技能专属字段与脚本语义 | 在同一次请求里混入多个 provider 的字段 |
| `Step 4` | `FIELD-VIDEO-API-04` | 输出预期是 receipt 还是成片闭环？ | 明确报告类型和路径族 | 用回执冒充成片、或对 full-loop 少报下载结果 |
| `Step 5` | `FIELD-VIDEO-API-05` | 问题该修父级还是修子技能？ | 生成分层上溯链和修复落点 | 只修单次调用，不修真源 |

## 7. 标准进入方式

### 7.1 用户显式点名 provider

- 直接进入对应子技能，并同步加载其同目录 `CONTEXT.md`。

### 7.2 用户只描述能力

- 先按本文件完成路由，再进入目标子技能。
- 不得在父级停留为抽象建议稿。

### 7.3 用户要求“完善视频 API 技能树”

- 先检查本父技能是否覆盖全部现有子技能与共享路由规则。
- 再检查对应子技能是否需要同步补齐。

## 8. Root-Cause 执行契约（Mandatory）

当出现 provider 误路由、把创建回执误说成闭环结果、把多个 provider 字段拼成一份伪通用 payload、父级索引漏掉现有子技能，或跨 provider 的共享说明发生漂移时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：provider 判断错误、闭环类型误判、父级索引缺失、共享术语漂移、父级与子技能边界不清
-> `规则源`：`.agents/skills/api/video/SKILL.md`、`.agents/skills/api/video/CONTEXT.md`、目标子技能 `SKILL.md`
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的 Root-Cause First / Canonical Source / Composite Output / Context Loading 治理契约
-> `Fix Landing Points`：优先修父级路由真源、子技能索引、闭环分类和共享表述；若是 provider 专属字段或脚本问题，再下钻修对应子技能

用户侧关闭语必须至少包含：

- 根因位置
- 立即修复
- 系统性预防修复

## 9. 失败排查

1. 先看用户是否已经显式点名 provider、端点或模型族。
2. 若已点名，不要再做“更优 provider”替换。
3. 若未点名，先判断任务是否要求 `full-loop`。
4. 若目标子技能本身是 `create-only`，必须在输出里明确只到 receipt。
5. 若一个请求里出现多个 provider 的字段语义，先回到父级做路由切分，再进入单一子技能。
6. 若发现当前目录存在子技能但父级索引未覆盖，应先补父技能真源。

## 10. 字段通过表（Mandatory）

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| `FIELD-VIDEO-API-01` | 输入收束完整度 | provider / endpoint / capability / lifecycle 线索已收束清楚 | `FAIL-VIDEO-API-INPUT` | 回到 `Step 1` |
| `FIELD-VIDEO-API-02` | 路由正确性 | 只选一个子技能，且选择理由符合第 3 节规则 | `FAIL-VIDEO-API-ROUTE` | 回到 `Step 2` |
| `FIELD-VIDEO-API-03` | 移交契约稳定性 | 已切到目标子技能字段语义，无跨 provider 混写 | `FAIL-VIDEO-API-HANDOFF` | 回到 `Step 3` |
| `FIELD-VIDEO-API-04` | 输出边界清晰度 | `create-only` 与 `full-loop` 区分明确 | `FAIL-VIDEO-API-OUTPUT` | 回到 `Step 4` |
| `FIELD-VIDEO-API-05` | 根因闭环完整性 | 能完整给出 `Symptom -> Direct Cause -> Rule Source -> Meta Rule Source` | `FAIL-VIDEO-API-RCA` | 回到 `Step 5` |

---
name: nano-banana
version: “v2.0”
governance_tier: full
description: |
  nano-banana 图像生成 API 契约层。封装 AnyFast Gemini 原生图像接口（默认模型 `gemini-3.1-flash-image-preview`），提供参数枚举、默认值注入、原生请求构造、批量并发调度与项目化落盘。本技能为纯 API 基座，不含应用层 prompt 模板——具体生图场景由子技能包承载（general / face-swap / costume-swap / multiview-character / multiview-scene / multiview-prop）。当你需要调用 nano-banana 生图但不确定用哪个子技能时，先读本文件确认 API 契约，再路由到对应子技能。
tools: [Read, Write, Edit, Bash]
color: yellow
---

# nano-banana API 契约层

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 作用范围

本文件是 nano-banana 的 **纯 API 契约层**，定义参数枚举、请求格式、并发调度与落盘规则。所有应用场景（通用生图、换脸、换装、多视图等）由子技能包承载。

- AnyFast 加速端点：
  - 平台地址：`https://www.anyfas.ai`
  - 文档地址：`https://docs.anyfast.ai`
  - API 基础端点：`https://fw2afus.ent.acc.kurtisasia.com`
  - 默认请求形态：`POST /v1beta/models/<model>:generateContent?key=...`
- 默认模型：`gemini-3.1-flash-image-preview`
- 支持两类任务：文本生图（T2I）、参考图生图（I2I）
- 统一调用脚本：`scripts/nano_banana_generate.py`

## 1.1 子技能路由

| 子技能 | 路径 | 触发场景 |
|--------|------|----------|
| general | `general/` | 通用 T2I / I2I，无特化 prompt 模板 |
| face-swap | `face-swap/` | 保留服装姿态，替换角色面貌 |
| costume-swap | `costume-swap/` | 保留角色形象，替换服装 |
| multiview-character | `multiview-character/` | 角色多视图设计页（CHARACTER_DESIGN_SHEET） |
| multiview-scene | `multiview-scene/` | 场景多视图设计页（3x3 九宫格） |
| multiview-prop | `multiview-prop/` | 道具多视图设计页（PROP_DESIGN_SHEET） |

路由规则：用户意图明确匹配某子技能时直接路由；意图模糊时默认走 `general/`。

## 2. 必需输入

- `prompt`
- API Key（优先读取根目录 `.env` 中的 `ANYFAST_API_KEY`，回退 `GEMINI_API_KEY`，也可显式传 `--api-key`）

可选输入：
- `model`
- `project_name`
- `task_kind`（`project / test / temp`）
- `aspect_ratio`
- `image_size`
- `max_concurrent`
- `images[].url`
- `request_id`
- `caller_skill`
- `episode_id`
- `output_dir`
- `filename_prefix`
- `input_json`
- `no_report`

职责边界：
- `images[] / --image-url` 在本技能中属于“已解析好的消费态参考图输入”。
- 项目级资产注册 contract 不在 `5-API` 定义；其单一事实源位于 `output/影片/<项目名>/3-设定/5-注册/asset_registry.*.json`，由 `0-初始` 初始化合同与 `4-prompts` 消费层负责衔接；旧 `.schema` 仅作兼容读回退。

## 3. 核心约束（Mandatory）

1. **默认值刚性注入**
   - 当用户或上游输入未明确指定 `aspect_ratio` 时，必须默认使用 `16:9`。
   - 当用户或上游输入未明确指定 `image_size` 时，必须默认使用 `4K`。
   - “未明确指定”包含：字段缺失、空字符串、`null`、只写了模糊描述但未落到接口枚举值。
2. **显式值优先**
   - 若用户或上游已明确给出合法 `aspect_ratio / image_size`，必须保留其原值，不得被默认值覆盖。
3. **枚举校验**
   - `aspect_ratio` 仅允许：
     - `1:1` `3:4` `4:3` `9:16` `16:9`
   - `image_size` 仅允许：
     - `1K` `2K` `4K`
4. **质量大小写纠偏**
   - 若输入为 `1k / 2k / 4k`，必须在调用前规范化为大写 `K`。
5. **原生格式契约**
   - 请求体必须使用 Gemini 原生格式：
     - `contents[].parts[].text`
     - `contents[].parts[].inline_data`
     - `generationConfig.responseModalities`
     - `generationConfig.imageConfig.aspectRatio / imageSize`
   - 禁止混入与该文档不兼容的旧字段，如 `ratio`、`quality`、`images[].url` 直接透传到 API。
   - API URL 必须优先由 `.env` 中的 `ANYFAST_API_BASE_URL` 组装，不再把固定官网域名硬编码为唯一入口。
6. **参考图统一转译**
   - 参考图若来自 URL、本地文件或 data URL，必须统一转译为：
     - `inline_data.mime_type`
     - `inline_data.data`
   - 禁止把远程 URL 直接塞入 API 请求体。
   - 当本地/远程参考图过大时，桥接层必须在内存中先执行保守压缩与缩边，再写入 `inline_data`，避免请求体触发 `413 Request Entity Too Large`；该过程不得改写 canonical 原图，也不得强制生成额外临时文件。
7. **调用方技能包驱动的输出路径**
   - 默认输出路径不得再固定为单一路径常量；应按以下优先级解析：
     1. `--output-dir`
     2. `input_json.output_dir`
     3. `caller_skill + episode_id` 推导出的调用方默认输出路径
     4. 兜底到 `general` 的项目化目录
   - 若调用方提供 `caller_skill`，脚本必须优先遵循该技能包的输出策略，而不是回退到统一的 `5-API` 根目录。
   - `general` 直调时，默认输出路径为：
     - `output/影片/[项目名]/5-API/image/nano-banana/general/`
   - `face-swap / costume-swap / multiview-*` 这类输入图驱动的子技能，默认输出应优先跟随第一张本地输入图所在目录；仅在无法定位本地输入图时，才回退到项目化目录。
   - `aigc/4-Design/2-设计` 系调用方若未显式传 `--output-dir`，默认输出应进入对应 `projects/aigc/<项目名>/4-Design/<域>/2-设计/<episode_id>/generated/` 运行时路径；若调用方已传 `--output-dir + --output-filename`，必须优先尊重同目录同名策略。
   - 若任务类型为测试且未显式传 `project_name`，则 `[项目名]` 自动使用 `测试`。
   - 若任务类型为临时且未显式传 `project_name`，则 `[项目名]` 自动使用 `临时`。
8. **多任务自动并发契约**
   - 当输入为多个任务时（`--input-json` 为对象数组，或对象内含 `tasks[]`），必须自动进入批量并发模式，不得退回逐任务串行。
   - 默认最大并发为 `100`。
   - `--max-concurrent` 允许显式下调或上调请求值，但执行时必须被硬限制在 `100` 以内。
   - 单任务保持单请求执行；多任务才启用并发调度。
9. **下游 `BASE64` 交接契约**
   - AnyFast 返回的生成图片应视为 `BASE64` 主形态。
   - 当下一环节需要引用生成结果或执行二改时，优先直接按 `BASE64` 方式传入。
   - 禁止无必要先落本地文件、再回读重编码，或强制改写成 URL 等中间载体。
10. **失败优先修源层**
    - 若出现默认值漂移、参数枚举错误、参考图结构不兼容或响应解析失败，优先修复：
      - `scripts/nano_banana_generate.py`
      - 本 `SKILL.md`
    - 禁止只在单次调用时手工绕过而不修技能源层。
11. **日志与报告密钥脱敏**
    - 控制台日志、重试提示、失败 report、`pending_retry.json` 不得写出 `key=...`、`api_key=...`、Bearer token 或 `sk-...` 原文。
    - 若底层 HTTP 异常字符串包含已拼接密钥的完整 URL，必须先脱敏再打印或写入报告。

## 4. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-DXJ2-01` | 输入解析结果：`prompt / images / request_id / input_json` | 所有输入源必须先收束为统一字段，`prompt` 非空，参考图列表结构稳定 | 用户输入、上游结构化请求、CLI 参数 | Step 1 | 输入收束完整度 | `FAIL-DXJ2-INPUT` |
| `FIELD-DXJ2-02` | 参数解析结果：`aspect_ratio / image_size / defaults_applied` | 未指定时自动补齐 `16:9 / 4K`；显式值优先保留；小写 `k` 自动纠偏 | 用户输入、上游文档、默认规则 | Step 2 | 默认值契约稳定性 | `FAIL-DXJ2-DEFAULTS` |
| `FIELD-DXJ2-03` | 请求体：`api_url / model / contents / generationConfig.imageConfig` | 请求体必须符合 AnyFast Gemini 原生格式，API URL 从 `.env` 基础端点组装，参考图统一转为 `inline_data` | AnyFast 官方文档、`.env`、脚本构造结果 | Step 3 | 请求体合法性 | `FAIL-DXJ2-PAYLOAD` |
| `FIELD-DXJ2-04` | 调度结果：`task_count / batch_mode / requested_max_concurrent / effective_max_concurrent` | 单任务维持串行；多任务必须自动并发；实际执行并发不得超过 `100` | 上游任务清单、CLI 参数、调度日志 | Step 4 | 并发调度稳定性 | `FAIL-DXJ2-CONCURRENCY` |
| `FIELD-DXJ2-05` | 输出产物：图片文件、文本回包、可选 `nano_banana_report_*.json`、可选 `nano_banana_batch_report_*.json`、项目化目录路径、下游交接形态 | 图片、文本说明、finish reason、默认值注入信息、并发汇总信息、`项目名 -> 输出目录` 映射均可追溯；显式 `--no-report` 时允许跳过 report 文件；下一环节默认按 `BASE64` 透传生成结果 | API 响应、落盘报告或返回结果、项目名/任务类型 | Step 5 | 输出可追溯性 | `FAIL-DXJ2-OUTPUT` |

## 5. 思维导引与执行流程（Mandatory）

### 5.1 固定步骤

1. **Step 1 / 输入收束**
   - 读取 CLI 参数或 `--input-json`
   - 统一抽取 `prompt / project_name / task_kind / aspect_ratio / image_size / images / request_id / caller_skill / episode_id`
2. **Step 2 / 默认值补齐**
   - 保留显式合法值
   - 缺失 `aspect_ratio` 时注入 `16:9`
   - 缺失 `image_size` 时注入 `4K`
   - 对小写 `k` 做规范化
3. **Step 3 / 原生请求构造**
   - 参考图转为 `inline_data`
   - 若参考图体积过大，先在内存里缩边/压缩到安全预算，再写入 `inline_data`
   - 从 `.env` 读取 `ANYFAST_API_BASE_URL`
   - 组装 `/v1beta/models/<model>:generateContent`
   - 构造 `contents[].parts[]`
   - 构造 `generationConfig.responseModalities=["TEXT","IMAGE"]`
   - 构造 `generationConfig.imageConfig`
4. **Step 4 / 批量调度裁决**
   - 判断输入任务数
   - 单任务时保持单请求执行
   - 多任务时自动进入并发模式
   - `--max-concurrent` 默认 `100`，实际执行并发必须钳制到 `<=100`
5. **Step 5 / 调用与落盘**
   - 发起请求
   - 同时兼容解析 `candidates[].content.parts[].inline_data` 与 `inlineData`
   - 若需向下一环节交接生成结果，优先保留原始 `BASE64` 形态
   - 将输出落到调用方技能包解析出的默认输出路径；若未提供调用方技能信息，再回退到 `general` 项目化目录
   - 保存图片、记录文本回包与任务报告 JSON
   - 若显式追加 `--no-report`，允许跳过任务报告与批量汇总报告 JSON
   - 若为多任务且未启用 `--no-report`，再额外写出批量汇总报告 JSON

### 5.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-DXJ2-01` | 输入是 CLI 直输还是上游结构化文档？项目名/任务类型是否明确？ | 收束字段并统一命名 | `prompt` 丢失、参考图结构混乱、项目名无法落盘 |
| `Step 2` | `FIELD-DXJ2-02` | 哪些值是显式指定，哪些需默认补齐？ | 保留显式值并注入 `16:9 / 4K` | 默认值覆盖显式值，或缺少默认注入 |
| `Step 3` | `FIELD-DXJ2-03` | 请求体是否完全符合原生接口契约？ | 构造 `contents + generationConfig`，转译参考图 | 仍透传旧字段、参考图未转 `inline_data` |
| `Step 4` | `FIELD-DXJ2-04` | 当前是单任务还是多任务？并发值是否超过硬上限？ | 自动裁决串行/并发并钳制最大并发 | 多任务仍串行、并发值超过 `100` |
| `Step 5` | `FIELD-DXJ2-05` | 输出是否可复盘？ | 保存图片、记录文本、写任务报告与批量汇总 | 无报告、无法区分任务级与批量级结果 |

## 6. 脚本入口

所有子技能共享同一脚本入口：

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py [参数]
```

具体调用示例见各子技能 SKILL.md。

## 7. 输出约定

- 默认输出目录由调用方技能包决定：
  - `general`：`output/影片/[项目名]/5-API/image/nano-banana/general/`
  - `face-swap / costume-swap / multiview-*`：默认与第一张本地输入图同目录
  - `aigc/4-Design/2-设计`：未显式传输出时为 `projects/aigc/[项目名]/4-Design/<域>/2-设计/<episode_id>/generated/`；显式传 `--output-dir + --output-filename` 时可落到设计文件同目录同名
  - 若无法识别调用方，则回退到 `output/影片/[项目名]/5-API/image/nano-banana/general/`
- 子技能输出目录：默认与输入图（原图）同目录
  - 命名规则：在原图文件名基础上追加子技能后缀（如 `-face-swap`、`-multiview` 等）
  - 若已存在同名文件，自动递增（如 `-face-swap-1.png`、`-face-swap-2.png`）
  - 若显式传入的输出文件后缀与接口实际返回 MIME 不一致，脚本自动按真实 MIME 校正后缀，避免“文件名是 PNG、内容却是 JPEG”
  - 若显式传 `--output-dir`，允许覆盖默认目录；覆盖优先级高于 `caller_skill`
  - 永不覆盖原则：原始文件保持不变
- 目录映射规则：
  - `--project-name <项目名>`：使用显式项目名
  - `--task-kind test` 且未传 `project_name`：使用 `测试`
  - `--task-kind temp` 且未传 `project_name`：使用 `临时`
- 默认产物：
  - `*.png / *.jpg / *.jpeg / *.webp`
  - `nano_banana_report_YYYYmmdd_HHMMSS.json`（默认启用；`--no-report` 时跳过）
  - `nano_banana_batch_report_YYYYmmdd_HHMMSS.json`（仅多任务且未启用 `--no-report`）
- 下游交接默认：
  - 下一环节引用生成结果或执行二改时，默认直接传递上游返回的 `BASE64`
  - 文件落盘仅作为资产沉淀与人工复核载体，不作为强制唯一交接载体
- 未启用 `--no-report` 时，任务报告文件必须包含：
  - `request_summary`
  - `defaults_applied`
  - `response_meta`
  - `response_texts`
  - `saved_files`
  - `error`（若失败）
- 多任务且未启用 `--no-report` 时，批量汇总报告必须包含：
  - `batch_summary`
  - `tasks`
  - `results`

## 8. 参考资料

- 接口摘要：`.agents/skills/api/image/nano-banana/references/api.md`
- 官方文档：`https://docs.anyfast.ai`
- 环境变量源：根目录 `.env`

## 9. Root-Cause 执行契约（Mandatory）

当调用失败、默认值异常或输出与预期不符时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：请求字段不符原生格式、`aspectRatio / imageSize` 缺失、参考图未转 `inline_data`、多任务仍串行、并发值未钳制到 `100` 以内、`caller_skill` 未传或输出目录未按调用方技能包策略解析
-> `规则源`：`.agents/skills/api/image/nano-banana/SKILL.md` 与 `scripts/nano_banana_generate.py`
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的 Root-Cause First / Field-Centric / CONTEXT 基线契约
-> `Fix Landing Points`：优先修脚本默认值逻辑、批量并发调度、原生请求构造、响应解析和技能说明，再修局部调用样例

用户侧关闭语必须至少包含：
- 根因位置
- 立即修复
- 系统性预防修复

## 10. 失败排查

1. 检查 `.env` 是否存在 `ANYFAST_API_KEY` 或 `GEMINI_API_KEY`
2. 检查 `.env` 是否存在 `ANYFAST_API_BASE_URL` 与 `DXJ2_DEFAULT_MODEL`
3. 先运行 `--dry-run --print-payload` 检查最终 payload
   - 若包含参考图，`dry-run` 只验证 payload 结构，不会真实下载 URL / 读取本地图片；参考图位置会以占位 `inline_data` 保持同形结构。
4. 确认 `aspectRatio / imageSize` 是否被正确解析：
   - 缺失时应自动变为 `16:9 / 4K`
   - 小写 `4k` 应被规范化为 `4K`
5. 确认输出目录是否符合：
   - `--output-dir` / `input_json.output_dir` 是否正确覆盖
   - 若传了 `caller_skill`，默认输出是否已切到该技能包策略
   - `general` 直调是否进入 `output/影片/[项目名]/5-API/image/nano-banana/general/`
   - `4-Design/2-设计` 若显式传了 `--output-dir + --output-filename`，是否遵循同目录同名；未显式传时是否进入 `projects/aigc/[项目名]/.../generated/`
   - 测试任务未传项目名时是否自动映射到 `测试`
   - 临时任务未传项目名时是否自动映射到 `临时`
6. 若参考图调用失败：
   - 检查是否成功转成 `inline_data.mime_type + data`
7. 若返回 4xx/5xx：
   - 检查报告文件中的 `error.http_body`
   - 对照 `references/api.md` 复核字段
8. 若多任务执行异常：
   - 检查 `--input-json` 是否为对象数组或包含 `tasks[]`
   - 检查批量汇总报告中的 `requested_max_concurrent / effective_max_concurrent`
   - 未启用 `--no-report` 时，确认是否自动写出 `nano_banana_batch_report_*.json`
   - 已启用 `--no-report` 时，改查控制台结果与返回值
9. 若下一环节引用或二改异常：
   - 确认是否直接使用 AnyFast 返回的原始 `BASE64`
   - 确认是否误改写成文件路径、URL 或二次转码后的中间格式

## 11. 字段通过表（Mandatory）

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| `FIELD-DXJ2-01` | 输入收束完整度 | `prompt` 存在；参考图被统一收束；无双轨字段命名 | `FAIL-DXJ2-INPUT` | 回到 `Step 1` 统一输入解析 |
| `FIELD-DXJ2-02` | 默认值契约稳定性 | 缺失 `aspect_ratio / image_size` 时必得 `16:9 / 4K`；显式值保留不被覆盖 | `FAIL-DXJ2-DEFAULTS` | 回到 `Step 2` 修正默认值与优先级 |
| `FIELD-DXJ2-03` | 请求体合法性 | payload 仅含原生文档字段；参考图转为 `inline_data`；`imageSize` 为大写 `K` | `FAIL-DXJ2-PAYLOAD` | 回到 `Step 3` 复核校验与请求体构造 |
| `FIELD-DXJ2-04` | 并发调度稳定性 | 多任务必走并发；默认并发请求值为 `100`；实际并发值不得超过 `100` | `FAIL-DXJ2-CONCURRENCY` | 回到 `Step 4` 修正批量裁决与并发钳制 |
| `FIELD-DXJ2-05` | 输出可追溯性 | 成功/失败都可定位；默认生成任务报告 JSON，多任务时默认再生成批量汇总报告；若显式 `--no-report`，允许仅依赖返回结果与控制台追踪；下游交接默认按 `BASE64` 透传 | `FAIL-DXJ2-OUTPUT` | 回到 `Step 5` 修正落盘、报告写入与交接形态 |

### 回环映射表

| rule_id | 责任Step | 聚焦维度 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| R-DXJ2-01 | Step 1 | 输入收束完整度 | FAIL-DXJ2-INPUT | 回到 Step 1 |
| R-DXJ2-02 | Step 2 | 默认值契约稳定性 | FAIL-DXJ2-DEFAULTS | 回到 Step 2 |
| R-DXJ2-03 | Step 3 | 请求体合法性 | FAIL-DXJ2-PAYLOAD | 回到 Step 3 |
| R-DXJ2-04 | Step 4 | 并发调度稳定性 | FAIL-DXJ2-CONCURRENCY | 回到 Step 4 |
| R-DXJ2-05 | Step 5 | 输出可追溯性 | FAIL-DXJ2-OUTPUT | 回到 Step 5 |

### 评分矩阵

| 维度 | 权重 | 聚焦 field_id | 说明 |
| --- | --- | --- | --- |
| 维度0: 契约遵循 | 10 | 全部 | 脚本路径、输出目录、默认值注入规则是否与 SKILL.md 一致 |
| 维度1: 输入完整度 | 10 | FIELD-DXJ2-01 | prompt 非空、参考图结构稳定、项目名可落盘 |
| 维度2: 参数合规性 | 10 | FIELD-DXJ2-02, FIELD-DXJ2-03 | 默认值正确注入、请求体符合原生格式 |
| 维度3: 调度正确性 | 10 | FIELD-DXJ2-04 | 单/多任务判定正确、并发钳制有效 |
| 维度4: 输出可追溯 | 10 | FIELD-DXJ2-05 | 报告完整、文件落盘、BASE64 交接 |

- 总分门槛: >= 40/50
- 维度0 < 8 一票否决

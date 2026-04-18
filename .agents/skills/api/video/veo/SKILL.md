---
name: veo
description: Use when the task must submit Google Veo video generation jobs through FineAPI's `/v1/video/create` interface, especially for text-to-video or image-conditioned creation with `model/prompt/enable_upsample/enhance_prompt/images/aspect_ratio` JSON payloads.
governance_tier: full
---

# FineAPI Veo 生视频技能

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 作用范围

- 本技能用于通过 FineAPI 的 Veo 创建接口提交异步视频任务。
- 当前已确认真源：
  - 显式 Veo/FineAPI 创建接口：`POST /v1/video/create`
  - AnyFast 风格回退创建接口：`POST /v1/video/generations`
  - 请求头：`Accept / Content-Type / Authorization`
  - 已确认字段：`model / prompt / enable_upsample / enhance_prompt / images / aspect_ratio`
  - 已确认覆盖：文生视频、图生视频
- 当前输入材料只稳定确认了“创建任务”这一步；旧版 `GET /v1/videos/{id}`、`/content`、`input_reference multipart` 不再视为本技能当前真源。
- 默认执行脚本：

```bash
python3 .agents/skills/api/video/veo/scripts/veo_video_generate.py submit ...
```

- 默认模型治理统一回指父级 `../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族。
  - 脚本共享骨架使用 `../shared/default_model_policy.py`
  - Veo 的 provider 特有差异是：排除 `frames / components` 这类要求图片输入的专用模型
  - 截至 2026-04-17，本地白名单解析结果为 `veo3.1-pro`。

## 2. 已确认接口契约

### 2.1 请求头

- `Accept: application/json`
- `Content-Type: application/json`
- `Authorization: Bearer <token>`

### 2.2 Body 字段

| 字段 | 类型 | 必填 | 当前规则 |
| --- | --- | --- | --- |
| `model` | string | 是 | 支持当前已见 Veo 2 / Veo 3 / Veo 3.1 家族枚举 |
| `prompt` | string | 是 | 提示词 |
| `enable_upsample` | boolean | 文档有漂移 | 文生页写可选，图生页写必填；脚本允许显式传 `true/false` |
| `enhance_prompt` | boolean | 文档有漂移 | 文生页写可选，图生页写必填；若提示词含中文，建议显式传 `true` |
| `images` | array[string] | 可选 | 图生时传图片 URL 数组；当前不扩展本地文件直传 |
| `aspect_ratio` | string | 文档有漂移 | 仅 `veo3*` 支持；可选值 `16:9 / 9:16` |

### 2.3 响应字段

当前可见材料存在两套响应示例，技能必须同时保留原始响应并做最小规范化：

1. 简洁回执：
   - `id`
   - `status`
   - `status_update_time`
   - `enhanced_prompt`
2. OpenAI 风格包裹：
   - `id`
   - `object`
   - `created`
   - `choices`
   - `usage`

## 3. 核心约束（Mandatory）

1. **当前真源是 `/v1/video/create` JSON 接口**
   - 对显式 Veo/FineAPI host，优先使用 `/v1/video/create`
   - 若当前网关对 `/v1/video/create` 返回 `Invalid URL`，可自动回退到 `/v1/video/generations`
   - 不再使用旧的 `/v1/videos`
   - 不再使用 `input_reference` multipart
2. **文生与图生都走同一创建端点**
   - 无图时走文生
   - 传 `images[]` 时走图生/首尾帧/组件参考
3. **图片输入当前按 URL 数组处理**
   - `images` 是 `array[string]`
   - 本地路径、二进制文件、base64 文本不得静默塞进 JSON
4. **`aspect_ratio` 只对 `veo3*` 家族开放**
   - 当前只接受 `16:9 / 9:16`
   - 非 `veo3*` 模型不得发送该字段
5. **模型枚举必须受控**
   - 只接受当前材料中已明确出现的模型值
   - 不得继续沿用旧的 `veo_3_1 / veo_3_1-fast` 下划线命名
6. **图片数量约束有局部已确认、局部漂移**
   - `veo2-fast-frames`：最多 2 张
   - `veo3-pro-frames`：最多 1 张
   - `veo2-fast-components`：最多 3 张
   - `veo3-fast-frames` 样例显示可传 2 张；脚本按样例兼容，但保留漂移提示
7. **当前只锁定创建回执**
   - 本轮校正依据只稳定覆盖创建接口
   - 在拿到新的状态/下载文档前，不得把旧查询/下载端点继续写成当前真源
8. **Base URL 必须显式配置**
   - 当前材料只给相对路径 `/v1/video/create`
   - 调用时必须通过 `.env` 或 `--base-url` 提供 API Base URL
9. **默认模型总是前移到当前最高版本通用模型**
   - 具体选择算法不再在本文件重复展开，统一遵循父级 `../runbooks/default-model-policy.md`
   - 脚本默认值不得再写死旧模型；共享骨架通过 `../shared/default_model_policy.py` 执行
   - Veo 本地过滤条件是“不把 `frames / components` 变体当作默认值”；截至 2026-04-17 当前自动解析结果为 `veo3.1-pro`
10. **环境变量回退链必须对齐仓库视频技能基线**
   - Key 优先级：`VEO_API_KEY -> ANYFAST_VIDEO_API_KEY -> ANYFAST_API_KEY -> FINEAPI_API_KEY`
   - Base URL 优先级：`VEO_API_BASE_URL -> ANYFAST_API_BASE_URL -> FINEAPI_API_BASE_URL`
   - 不得只读空置的 `VEO_* / FINEAPI_*` 键而忽略仓库实际在用的 `ANYFAST_*`
    - 当 Base URL 实际落到 `ANYFAST_API_BASE_URL` 且 `/v1/video/create` 返回 `Invalid URL` 时，脚本应自动回退到 `/v1/video/generations`
11. **失败优先修源层**
   - 若出现字段名不匹配、模型枚举漂移、图片数组不合法、`aspect_ratio` 越界或旧端点回流，优先修：
     - `scripts/veo_video_generate.py`
     - 本 `SKILL.md`
     - `references/api.md`

## 4. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任 Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-VEO-01` | 输入解析结果：`prompt / images / project_name` | `prompt` 非空；`images` 缺省或为公网 URL 数组 | 用户输入、CLI 参数、接口样例 | Step 1 | 输入收束完整度 | `FAIL-VEO-INPUT` |
| `FIELD-VEO-02` | 参数裁决结果：`model / enable_upsample / enhance_prompt / aspect_ratio / base_url` | 模型命中已确认集合；`aspect_ratio` 只在 `veo3*` 使用；布尔开关支持显式透传 | 用户样例、文档字段说明、脚本默认值 | Step 2 | 参数与环境一致性 | `FAIL-VEO-PARAMS` |
| `FIELD-VEO-03` | 创建请求：`POST /v1/video/create` JSON 请求体 | 头与 Body 字段名准确；`images` 为数组；不出现 `input_reference` | 文档页、用户样例 | Step 3 | 请求体合法性 | `FAIL-VEO-CREATE` |
| `FIELD-VEO-04` | 创建回执：规范化回执 + `raw_response` | 同时保留原始响应与最小规范化字段，不虚构后续下载结果 | 用户样例、API 响应 | Step 4 | 回执闭环完整性 | `FAIL-VEO-RECEIPT` |

## 5. 思维导引与执行流程（Mandatory）

### 5.1 固定步骤

1. **Step 1 / 输入收束**
   - 读取 `prompt`、`images`、`project_name`
   - 校验 `images` 缺省或全为 `http/https` 公网 URL
2. **Step 2 / 参数与环境裁决**
   - 校验 `model` 在已确认集合中
   - 校验 `aspect_ratio` 仅在 `veo3*` 模型上使用
   - 读取 `VEO_API_KEY / ANYFAST_VIDEO_API_KEY / ANYFAST_API_KEY / FINEAPI_API_KEY`
   - 读取 `VEO_API_BASE_URL / ANYFAST_API_BASE_URL / FINEAPI_API_BASE_URL`
3. **Step 3 / 创建任务**
   - 组装 JSON：`model / prompt / enable_upsample / enhance_prompt / images / aspect_ratio`
   - 默认先尝试 `/v1/video/create`
   - 若网关返回 `Invalid URL`，自动回退到 `/v1/video/generations`
4. **Step 4 / 回执落盘**
   - 保存任务回执 JSON
   - 输出最小规范化字段
   - 明确声明“当前闭环停在 create receipt，不含状态轮询与下载”

### 5.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-VEO-01` | prompt 与 images 是否收束完整？ | 校验 prompt 与公网图片链接数组 | prompt 为空、images 中混入本地路径 |
| `Step 2` | `FIELD-VEO-02` | 模型、布尔开关、比例参数、Key 与 Base URL 回退链是否可解释？ | 裁决环境变量与参数约束 | 旧模型命名、aspect_ratio 越界、Key/Base URL 缺失 |
| `Step 3` | `FIELD-VEO-03` | 是否严格按 JSON 接口提交，并在 `Invalid URL` 时正确回退到兼容端点？ | 构造并发送 JSON 请求 | 错用 multipart、字段错名、继续发 `input_reference`、未做端点回退 |
| `Step 4` | `FIELD-VEO-04` | 是否把创建回执完整落盘并正确解释？ | 保存 submit report，回传最小规范化回执 | 把创建成功误说成已出成片 |

## 6. 标准调用

### 6.1 文生视频

```bash
python3 .agents/skills/api/video/veo/scripts/veo_video_generate.py submit \
  --base-url "https://<your-fineapi-host>" \
  --model veo3.1-pro \
  --prompt "make animate" \
  --enhance-prompt true \
  --enable-upsample true \
  --aspect-ratio 16:9
```

### 6.2 图生视频

```bash
python3 .agents/skills/api/video/veo/scripts/veo_video_generate.py submit \
  --base-url "https://<your-fineapi-host>" \
  --model veo3-fast-frames \
  --prompt "牛飞上天了" \
  --image "https://filesystem.site/cdn/20250612/VfgB5ubjInVt8sG6rzMppxnu7gEfde.png" \
  --image "https://filesystem.site/cdn/20250612/998IGmUiM2koBGZM3UnZeImbPBNIUL.png" \
  --enhance-prompt true \
  --enable-upsample true \
  --aspect-ratio 16:9
```

### 6.3 Dry Run 检查请求体

```bash
python3 .agents/skills/api/video/veo/scripts/veo_video_generate.py submit \
  --base-url "https://<your-fineapi-host>" \
  --prompt "测试请求" \
  --enhance-prompt true \
  --enable-upsample true \
  --dry-run \
  --print-payload
```

## 7. 参数约定

| CLI 参数 | 创建字段 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--model` | `model` | 自动选择最高版本通用模型，当前 `veo3.1-pro` | 仅接受当前已确认模型集合 |
| `--prompt` | `prompt` | 必填 | 视频提示词 |
| `--image` | `images[]` | 可重复传参 | 当前只接受公网图片 URL |
| `--enhance-prompt` | `enhance_prompt` | 不发送 | `true / false`；中文 prompt 建议显式传 `true` |
| `--enable-upsample` | `enable_upsample` | 不发送 | `true / false` |
| `--aspect-ratio` | `aspect_ratio` | 不发送 | 仅 `veo3*` 支持：`16:9 / 9:16` |
| `--submit-path` | 提交端点 | `auto` | `auto` 会优先 `/v1/video/create`，若收到 `Invalid URL` 再回退 `/v1/video/generations` |
| `--base-url` | API Base URL | `.env` 回退链：`VEO_API_BASE_URL -> ANYFAST_API_BASE_URL -> FINEAPI_API_BASE_URL` | 当前必须显式配置 |
| `--api-key` | 鉴权 Token | `.env` 回退链：`VEO_API_KEY -> ANYFAST_VIDEO_API_KEY -> ANYFAST_API_KEY -> FINEAPI_API_KEY` | 支持原始 token 或 `Bearer ...` |

完整字段说明见：`references/api.md`

## 8. 输出约定

- 默认输出目录：`output/影片/[项目名]/5-API/video/veo/`
- 默认产物：
  - `veo_submit_report_YYYYmmdd_HHMMSS.json`
- 报告至少包含：
  - `ok`
  - `command`
  - `request_summary`
- `normalized_submit`
- `raw_response`
- `submit_path`
- `attempts`
- `diagnostic_hint`
- `validation_notes`
- `error`

## 9. Root-Cause 执行契约（Mandatory）

当创建失败、继续打旧 `/v1/videos`、把 `images` 当本地文件、继续发 `input_reference`、`aspect_ratio` 用在非 `veo3*` 模型上，或把创建回执误解为成片结果时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：端点漂移、请求体仍按 multipart 构造、模型枚举仍是旧下划线命名、图片输入不是 URL 数组、默认模型未前移、`ANYFAST_*` 回退链缺失、`Invalid URL` 后未自动切到 `/v1/video/generations`、参数漂移未收束、错误解释创建回执
-> `规则源`：`.agents/skills/api/video/veo/SKILL.md`、`references/api.md`、`scripts/veo_video_generate.py`
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的 Root-Cause First / Context Loading / Canonical Source / Composite Output 治理契约
-> `Fix Landing Points`：优先修脚本的端点与 JSON 构造、模型/参数校验与回执解释，再修示例与说明

用户侧关闭语必须至少包含：
- 根因位置
- 立即修复
- 系统性预防修复

## 10. 失败排查

1. 使用 `submit --dry-run --print-payload` 检查最终 JSON
2. 检查 `.env` 或命令行是否已提供 `VEO_API_BASE_URL / ANYFAST_API_BASE_URL / FINEAPI_API_BASE_URL / --base-url`
3. 若响应为 `404 Invalid URL (POST /v1/video/create)`，确认是否已启用默认 `--submit-path auto` 或显式改用 `/v1/video/generations`
4. 若传图，确认 `--image` 全为可访问的 `http/https` URL
5. 若 prompt 含中文且供应商报提示词问题，显式追加 `--enhance-prompt true`
6. 若 `aspect_ratio` 报错，先确认当前模型是否属于 `veo3*`
7. 若回执结构和示例不完全一致，优先看 `raw_response`，不要强行套单一 schema

## 11. 字段通过表（Mandatory）

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| `FIELD-VEO-01` | 输入收束完整度 | `prompt` 存在；`images` 缺省或为合法 URL 数组 | `FAIL-VEO-INPUT` | 回到 `Step 1` |
| `FIELD-VEO-02` | 参数与环境一致性 | 模型命中集合；`aspect_ratio` 只用于 `veo3*`；Base URL 明确 | `FAIL-VEO-PARAMS` | 回到 `Step 2` |
| `FIELD-VEO-03` | 请求体合法性 | `application/json`；优先 `/v1/video/create`，必要时可回退 `/v1/video/generations`；不出现 `input_reference` | `FAIL-VEO-CREATE` | 回到 `Step 3` |
| `FIELD-VEO-04` | 回执闭环完整性 | 原始响应保留，最小规范化字段可解释，且不虚构后续下载 | `FAIL-VEO-RECEIPT` | 回到 `Step 4` |

## 12. 参考资料

- 接口摘要：`.agents/skills/api/video/veo/references/api.md`
- 当前审计输入：用户提供的文生/图生接口字段与示例

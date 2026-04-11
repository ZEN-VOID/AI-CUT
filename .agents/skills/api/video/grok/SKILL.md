---
name: grok
description: Use when the task must submit GROK video generation jobs through api.ai666.net with model grok-video-3, especially for text-to-video or image-to-video requests that need local or remote image reading, dual JSON or multipart request handling, normalized task_id or id responses, and projectized submission reports.
governance_tier: full
---

# GROK 生视频技能

## 1. 作用范围

- 本技能用于通过 `https://api.ai666.net` 提交 GROK 生视频任务，默认模型为 `grok-video-3`。
- 已确认的两类提交形态都来自 `PRPs/grok.md` 与配套截图：
  - `POST /v1/video/create`，`application/json`，支持 `images[]`，适合文本生视频与多图/读图生视频。
  - `POST /v1/videos`，`multipart/form-data`，支持单个 `input_reference`，适合严格跟随 OpenAPI 文本版接口时使用。
- 本技能当前合同只覆盖“任务提交与提交回执落盘”：
  - 返回规范化后的 `task_id`、`status`、`status_update_time`
  - 生成提交报告 JSON
  - 不承诺下载最终 MP4，因为 `PRPs/grok.md` 未提供独立查询/下载接口

## 2. 必需输入

- `prompt`
- API Key
  - 优先读取根目录 `.env` 中的 `GROK_API_KEY`
  - 回退 `AI666_API_KEY`
  - 再回退 `OPENAI_API_KEY`
  - 也可显式传 `--api-key`

可选输入：

- `image`：可重复，支持本地路径、远程 URL、`data:` URL
- `request-mode`：`auto / json / multipart`
- `aspect-ratio`：`16:9 / 9:16 / 2:3 / 3:2 / 1:1`
- `size`：`720P / 1080P`
- `seconds`：`6 / 10 / 15`
- `project-name`
- `output-dir`
- `report-json`
- `timeout`
- `dry-run`

## 3. 核心约束（Mandatory）

1. **双接口合同并存**
   - 文本版 PRP 明示 `multipart /v1/videos`。
   - 截图版示例明示 `json /v1/video/create`。
   - 技能必须同时记录两种形态，不得擅自抹平成单一路径。
2. **默认优先 JSON 提交**
   - 默认 `request-mode=auto`。
   - `auto` 下优先裁决为 `json`，因为它天然支持多图与统一“图片读取 -> data URL”流程。
   - 只有用户显式要求 OpenAPI 文字版接口或必须使用 `input_reference` 时，才走 `multipart`。
3. **图片读取刚性**
   - `--image` 必须接受三种输入：本地文件、远程 URL、`data:` URL。
   - `json` 模式必须统一转成 `data:image/...;base64,...` 写入 `images[]`。
   - `multipart` 模式只允许单张参考图；若传入多张图，必须报错而不是静默丢弃。
4. **参数标准化**
   - `seconds` 与截图中的 `duration` 视为同一业务字段，统一对外以 `seconds` 表达。
   - `task_id` 与 `id` 视为同一提交任务标识，脚本必须归一化为 `task_id`。
5. **项目化输出路径**
   - 默认输出目录必须为 `output/影片/[项目名]/5-API/video/grok/`。
   - 若未显式传 `project-name`，默认项目名使用 `测试`。
6. **能力边界诚实**
   - 由于 `PRPs/grok.md` 未提供查询/下载端点，本技能默认只做到“提交任务 + 回执落盘”。
   - 禁止在技能文档里虚构最终视频下载闭环。
7. **失败优先修源层**
   - 若出现请求模式漂移、图片编码错误、返回字段不一致或报告缺字段，优先修复：
     - `scripts/grok_video_generate.py`
     - 本 `SKILL.md`
     - `references/api.md`

## 4. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-GROK-01` | 输入解析结果：`prompt / image_inputs / project_name` | `prompt` 非空；图片输入被收束为稳定列表；项目名可用于路径落盘 | 用户输入、CLI 参数 | Step 1 | 输入收束完整度 | `FAIL-GROK-INPUT` |
| `FIELD-GROK-02` | 参数裁决结果：`request_mode / aspect_ratio / size / seconds` | 模式裁决可解释；参数值均在允许枚举内；`seconds` 与 `duration` 语义统一 | PRP 文本、截图示例、脚本默认值 | Step 2 | 参数与模式一致性 | `FAIL-GROK-PARAMS` |
| `FIELD-GROK-03` | 提交请求：`endpoint / headers / payload_or_form` | `json` 模式使用 `images[] data URL`；`multipart` 模式使用单个 `input_reference`；认证头合法 | `PRPs/grok.md`、截图、脚本构造结果 | Step 3 | 请求体合法性 | `FAIL-GROK-PAYLOAD` |
| `FIELD-GROK-04` | 提交回执：`task_id / status / status_update_time / raw_response` | 兼容 `task_id` 与 `id`；状态值可归一化；异常时保留原始响应 | API 响应、截图示例 | Step 4 | 回执归一化稳定性 | `FAIL-GROK-RESPONSE` |
| `FIELD-GROK-05` | 输出产物：`grok_video_report_*.json` 与项目化目录 | 至少生成报告 JSON；请求摘要、图片摘要、原始响应、规范化字段均可追溯 | 报告文件、输出目录 | Step 5 | 输出可追溯性 | `FAIL-GROK-OUTPUT` |

## 5. 思维导引与执行流程（Mandatory）

### 5.1 固定步骤

1. **Step 1 / 输入收束**
   - 读取 `prompt`、`image_inputs`、`project_name`
   - 把每个图片输入标记为 `local_file / remote_url / data_url`
2. **Step 2 / 模式与参数裁决**
   - 校验 `aspect_ratio / size / seconds`
   - `request-mode=auto` 时默认裁决为 `json`
   - 若显式 `multipart`，强校验图片数量不超过 1
3. **Step 3 / 请求构造**
   - `json`：将图片统一转为 data URL，提交到 `/v1/video/create`
   - `multipart`：将首张图转为文件部件，提交到 `/v1/videos`
   - 注入 `Authorization: Bearer ...`
4. **Step 4 / 回执归一化**
   - 解析 JSON 响应
   - 规范化 `task_id = task_id or id`
   - 透传 `status`、`status_update_time`、`created_at`
5. **Step 5 / 报告落盘**
   - 默认写到 `output/影片/[项目名]/5-API/video/grok/`
   - 产出 `grok_video_report_YYYYmmdd_HHMMSS.json`
   - 记录图片来源摘要、请求模式、请求摘要、原始响应、规范化回执

### 5.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-GROK-01` | 是否已经明确 prompt、图片来源类型与项目名？ | 收束输入并分类图片来源 | `prompt` 为空、图片源不可读、项目名无法路由 |
| `Step 2` | `FIELD-GROK-02` | 本次应该走 JSON 还是 multipart？时长/比例/分辨率是否合法？ | 裁决模式并校验枚举 | 模式选择不可解释、参数越界 |
| `Step 3` | `FIELD-GROK-03` | 请求体是否与对应接口形态完全匹配？ | 构造 JSON 或 multipart 提交体 | `images[]` 不是 data URL、multipart 多图、认证头缺失 |
| `Step 4` | `FIELD-GROK-04` | 响应里有没有字段漂移？ | 兼容 `task_id/id` 并保留原始响应 | 任务 ID 丢失、状态字段无法解释 |
| `Step 5` | `FIELD-GROK-05` | 是否已经形成可复盘报告？ | 写报告并输出最终摘要 | 没有报告、没有图片摘要、无规范化字段 |

## 6. 标准调用

统一脚本入口：

```bash
python3 .agents/skills/api/video/grok/scripts/grok_video_generate.py [参数]
```

### 6.1 文本生视频

```bash
python3 .agents/skills/api/video/grok/scripts/grok_video_generate.py \
  --prompt "一只橘猫在雨夜霓虹街道慢慢回头，电影感，镜头缓推" \
  --aspect-ratio 16:9 \
  --size 720P \
  --seconds 10 \
  --project-name "测试"
```

### 6.2 读本地图片生视频

```bash
python3 .agents/skills/api/video/grok/scripts/grok_video_generate.py \
  --prompt "让角色从静止肖像转为缓慢抬头看向镜头，真实电影光影" \
  --image "/absolute/path/to/reference.png" \
  --aspect-ratio 9:16 \
  --size 1080P \
  --seconds 6 \
  --project-name "测试"
```

### 6.3 读远程图片生视频

```bash
python3 .agents/skills/api/video/grok/scripts/grok_video_generate.py \
  --prompt "让图中的猫看向追逐对象，镜头轻微摇移" \
  --image "https://example.com/cat.png" \
  --image "https://example.com/fish.png" \
  --request-mode json \
  --aspect-ratio 3:2 \
  --size 1080P \
  --seconds 6
```

### 6.4 严格走 multipart 参考图接口

```bash
python3 .agents/skills/api/video/grok/scripts/grok_video_generate.py \
  --prompt "让参考图人物缓慢转身并向前迈步" \
  --image "/absolute/path/to/reference.png" \
  --request-mode multipart \
  --aspect-ratio 2:3 \
  --size 720P \
  --seconds 10
```

### 6.5 Dry Run 验证

```bash
python3 .agents/skills/api/video/grok/scripts/grok_video_generate.py \
  --prompt "测试请求" \
  --image "/absolute/path/to/reference.png" \
  --dry-run \
  --print-payload
```

## 7. 参数约定

| CLI 参数 | JSON 模式字段 | multipart 模式字段 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `--model` | `model` | `model` | `grok-video-3` | 模型 ID |
| `--prompt` | `prompt` | `prompt` | 必填 | 提示词 |
| `--image` | `images[]` | `input_reference` | 无 | 图片输入，支持本地/远程/data URL |
| `--aspect-ratio` | `aspect_ratio` | `aspect_ratio` | `16:9` | 视频比例 |
| `--size` | `size` | `size` | `720P` | 分辨率 |
| `--seconds` | `duration` | `seconds` | `10` | 时长，支持 `6/10/15` |
| `--request-mode` | 决定是否走 `/v1/video/create` | 决定是否走 `/v1/videos` | `auto` | `auto` 默认裁决为 `json` |

## 8. 输出约定

- 默认输出目录：`output/影片/[项目名]/5-API/video/grok/`
- 默认报告文件：`grok_video_report_YYYYmmdd_HHMMSS.json`
- 报告至少包含：
  - `ok`
  - `request_mode`
  - `endpoint`
  - `request_summary`
  - `image_inputs`
  - `normalized_submission`
  - `raw_response`
  - `error`

## 9. Root-Cause 执行契约（Mandatory）

当调用失败、图片读不到、接口模式选错或报告缺字段时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：图片未转 data URL、误把多图送入 multipart、`duration/seconds` 字段漂移、`task_id/id` 未归一化、输出目录不符合项目化路径
-> `规则源`：`.agents/skills/api/video/grok/SKILL.md`、`references/api.md`、`scripts/grok_video_generate.py`
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的 Root-Cause First / Progressive Convergence / Field-Centric / CONTEXT 基线契约
-> `Fix Landing Points`：优先修请求构造、图片读取、字段归一化与报告合同，再修局部调用样例

用户侧关闭语必须至少包含：
- 根因位置
- 立即修复
- 系统性预防修复

## 10. 失败排查

1. 检查 `.env` 是否存在 `GROK_API_KEY` 或 `AI666_API_KEY`
2. 先运行 `--dry-run --print-payload`，确认模式裁决和请求摘要正确
3. 若是 JSON 模式失败，检查 `images[]` 是否已被转成 `data:image/...;base64,...`
4. 若是 multipart 模式失败，检查是否误传多张图
5. 若响应只有 `id` 没有 `task_id`，确认脚本是否已做归一化
6. 若出现 `SSL EOF`、`RemoteDisconnected`、`Empty reply from server`：
   - 先判定为上游端点可用性问题，而不是 payload 结构问题
   - 可用 `curl -Ivs https://api.ai666.net` 与 `curl -Ivs http://api.ai666.net` 复验
   - 若两条链路都在握手或首包阶段断开，应暂停业务层调参，等待上游恢复或更换可用网关
7. 若需要最终视频下载能力，先确认上游是否补充了查询/下载接口；本技能当前不虚构该能力

## 11. 字段通过表（Mandatory）

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| `FIELD-GROK-01` | 输入收束完整度 | `prompt` 非空；图片输入可读；项目名可落盘 | `FAIL-GROK-INPUT` | 回到 `Step 1` 修输入 |
| `FIELD-GROK-02` | 参数与模式一致性 | 模式裁决清晰；`aspect_ratio / size / seconds` 都在枚举内 | `FAIL-GROK-PARAMS` | 回到 `Step 2` 重裁决 |
| `FIELD-GROK-03` | 请求体合法性 | `json` 使用 `images[] data URL`；`multipart` 只用单图 `input_reference`；认证头正确 | `FAIL-GROK-PAYLOAD` | 回到 `Step 3` 修请求体 |
| `FIELD-GROK-04` | 回执归一化稳定性 | 至少解析出 `task_id`、`status`；原始响应被保留 | `FAIL-GROK-RESPONSE` | 回到 `Step 4` 修响应解析 |
| `FIELD-GROK-05` | 输出可追溯性 | 报告 JSON 落盘成功；请求摘要与规范化回执完整 | `FAIL-GROK-OUTPUT` | 回到 `Step 5` 修报告与路径 |

## 12. 参考资料

- 接口摘要与证据：`.agents/skills/api/video/grok/references/api.md`
- 提交脚本：`.agents/skills/api/video/grok/scripts/grok_video_generate.py`
- 依赖：`.agents/skills/api/video/grok/requirements.txt`

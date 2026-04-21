---
name: seedream
description: |
  调用火山引擎方舟 Ark API（模型 `doubao-seedream-5-0-260128`）执行 SEEDREAM 5.0 AI 生图任务，支持文本生图（T2I）、参考图生图（I2I）、连续多图（sequential_image_generation）与流式返回（SSE）。
  <triggers>
  - 用户要求"seedream / SEEDREAM 5.0 / 方舟生图"
  - 需要通过火山引擎 Ark OpenAI 兼容接口生成图片
  - 上游文档指定使用 `doubao-seedream-5-0-260128` 模型
  </triggers>
tools: [Read, Write, Edit, Bash]
color: orange
version: "v1.0"
---

# SEEDREAM 5.0 生图技能

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 作用范围

- 本技能用于通过火山引擎方舟 Ark API 执行 SEEDREAM 5.0 图像生成：
  - API 端点：`POST https://ark.cn-beijing.volces.com/api/v3/images/generations`
  - 默认模型：`doubao-seedream-5-0-260128`
  - 官方文档：[Volcengine SEEDREAM 5.0](https://www.volcengine.com/docs/82379/1824121?lang=zh)
- 支持任务类型：
  - 文本生图（T2I）
  - 参考图生图（I2I，通过 `--image-url` 传入参考图 URL 列表）
  - 连续多图生成（`sequential_image_generation=auto`，`max_images` 控制上限）
- 默认调用脚本：
  - `python3 .agents/skills/api/anyfast/image/seedream/scripts/seedream_generate.py ...`

## 2. 必需输入

- `prompt`（必填提示词）
- API Key（优先读取根目录 `.env` 中的 `SEEDREAM_API_KEY`，回退 `ARK_API_KEY`、`VOLCENGINE_ARK_API_KEY`，也可显式传 `--api-key`）

可选输入：
- `model`（默认 `doubao-seedream-5-0-260128`）
- `image-url`（可重复，参考图 URL 列表）
- `sequential-image-generation`（连续图模式，默认 `auto`）
- `max-images`（连续图最大数量，默认 `4`）
- `response-format`（`url` 或 `b64_json`，默认 `url`）
- `size`（默认 `2K`）
- `stream`（启用流式返回）
- `watermark / no-watermark`（默认启用水印）
- `output-dir`（输出目录）
- `filename-prefix`（输出文件名前缀，默认 `seedream`）
- `save-images / no-save-images`（是否下载到本地，默认启用）
- `report-json`（报告 JSON 路径）
- `extra-json`（额外 JSON 字段，合并到请求体顶层）

## 3. 核心约束（Mandatory）

1. **API 认证刚性**
   - 真实请求必须在 `.env` 中配置 `SEEDREAM_API_KEY`（或 `ARK_API_KEY` / `VOLCENGINE_ARK_API_KEY`）。
   - 脚本启动时自动从 `.env` 加载；无密钥时真实请求硬退出，但 `--dry-run --print-payload` 允许跳过认证，仅用于结构校验。
2. **模型锁定**
   - 默认模型为 `doubao-seedream-5-0-260128`，除非用户显式传 `--model` 覆盖。
3. **连续多图契约**
   - 默认 `sequential_image_generation=auto`，`max_images=4`。
   - 用户可通过 `--max-images` 调整上限。
4. **参考图直传**
   - 参考图通过 `image` 字段以 URL 列表形式直接传入 Ark API。
   - 无需转换为 `inline_data`（与 Gemini 接口不同）。
5. **流式返回兼容**
   - 支持 `--stream` 启用 SSE 流式返回。
   - 脚本自动解析 SSE `data:` 行并合并去重。
   - 流式图片结果可能出现在 `image_generation.partial_succeeded` 事件顶层的 `url / b64_json`，也必须兼容非流式 `data[]` 结构。
   - 若流式不稳定，可去掉 `--stream` 回退非流式。
6. **项目化输出路径**
   - 默认输出路径为：`output/影片/[项目名]/5-API/image/seedream/`
   - 若显式传 `--output-dir`，允许覆盖默认路径。
7. **失败优先修源层**
   - 若出现认证错误、请求参数异常、流式解析失败或输出异常，优先修复：
     - `scripts/seedream_generate.py`
     - 本 `SKILL.md`
   - 禁止只在单次调用时手工绕过而不修技能源层。

## 4. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-SDR-01` | 输入解析结果：`prompt / image_urls / extra_json` | `prompt` 非空；参考图列表为合法 URL；`extra_json` 为合法 JSON 对象 | 用户输入、CLI 参数 | Step 1 | 输入完整度 | `FAIL-SDR-INPUT` |
| `FIELD-SDR-02` | 参数解析结果：`model / size / max_images / response_format / stream / watermark` | 所有参数显式传入或使用脚本默认值；`size` 为合法值；`response_format` 仅 `url` 或 `b64_json` | 用户输入、脚本默认值 | Step 2 | 参数合规性 | `FAIL-SDR-PARAMS` |
| `FIELD-SDR-03` | 请求体：Ark API payload（`model / prompt / image / sequential_image_generation / size / stream / watermark`） | 请求体符合 Ark `images/generations` 接口契约；参考图为 URL 列表；`extra_json` 正确合并 | Ark API 文档、脚本构造结果 | Step 3 | 请求体合法性 | `FAIL-SDR-PAYLOAD` |
| `FIELD-SDR-04` | 执行结果：HTTP 响应 / SSE 事件流 / 合并去重后的图片列表 | 请求成功返回 200；SSE 解析兼容顶层 `url / b64_json` 与非流式 `data[]`；图片列表为空时必须生成失败报告 | API 响应、SSE 事件流 | Step 4 | 执行稳定性 | `FAIL-SDR-EXEC` |
| `FIELD-SDR-05` | 输出产物：图片文件、`seedream_report_*.json`、项目化目录路径 | 图片正确落盘（URL 下载或 Base64 解码）；报告 JSON 包含完整请求/响应信息；输出在正确目录 | API 响应、落盘结果、报告文件 | Step 5 | 输出可追溯性 | `FAIL-SDR-OUTPUT` |

## 5. 思维导引与执行流程（Mandatory）

### 5.1 固定步骤

1. **Step 1 / 输入收束**
   - 读取 CLI 参数：`--prompt`（必填）、`--image-url`（可重复）、`--extra-json`
   - 验证 `prompt` 非空
   - 验证参考图 URL 列表格式合法
   - 验证 `extra_json` 可解析为 JSON 对象
2. **Step 2 / 参数解析**
   - 解析并确认：`--model`（默认 `doubao-seedream-5-0-260128`）、`--size`（默认 `2K`）、`--max-images`（默认 `4`）、`--response-format`（默认 `url`）、`--stream`、`--watermark`
   - 从 `.env` 读取 `SEEDREAM_API_KEY`（回退 `ARK_API_KEY` / `VOLCENGINE_ARK_API_KEY`）
   - 无 API Key 时真实请求硬退出；若只是 `--dry-run`，允许继续打印 payload
3. **Step 3 / 请求体构造**
   - 组装 Ark API payload：
     - `model`、`prompt`、`sequential_image_generation`、`sequential_image_generation_options.max_images`
     - `response_format`、`size`、`stream`、`watermark`
   - 若有参考图，写入 `image[]` 字段
   - 若有 `extra_json`，合并到请求体顶层
   - 支持 `--dry-run --print-payload` 仅打印不调用
4. **Step 4 / 调用与响应处理**
   - 流式（`--stream`）：发起 SSE 请求，逐行解析 `data:` 事件，遇 `[DONE]` 停止，收集所有 payload
   - 流式图片提取必须读取 `image_generation.partial_succeeded` 顶层 `url / b64_json`
   - 非流式：发起普通 POST 请求，直接读取 JSON 响应
   - 合并去重所有图片项（`url` 或 `b64_json`）
   - 若最终图片列表为空，写入 `ok=false` 报告并以非零退出码结束
   - 异常时捕获错误并生成错误报告
5. **Step 5 / 落盘与报告**
   - 创建输出目录（默认 `output/影片/[项目名]/5-API/image/seedream/`）
   - 若启用 `--save-images`：
     - URL 格式：下载图片到本地
     - Base64 格式：解码写入文件
   - 生成 `seedream_report_YYYYmmdd_HHMMSS.json`，包含请求参数、结果列表、保存文件路径、错误信息

### 5.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-SDR-01` | prompt 是否非空？参考图 URL 是否合法？extra_json 是否可解析？ | 收束并校验所有输入 | `prompt` 缺失、URL 格式错误、JSON 解析失败 |
| `Step 2` | `FIELD-SDR-02` | API Key 是否存在？各参数是否在合法范围内？ | 解析参数并读取环境变量 | 无 API Key、参数值不合法 |
| `Step 3` | `FIELD-SDR-03` | 请求体是否完全符合 Ark API 接口契约？ | 构造 payload 并合并 extra_json | 字段缺失、结构不符接口文档 |
| `Step 4` | `FIELD-SDR-04` | 请求是否成功？SSE 解析是否正确？图片是否完整提取？ | 发起请求并解析响应 | HTTP 错误、SSE 解析异常、图片列表为空 |
| `Step 5` | `FIELD-SDR-05` | 图片是否正确落盘？报告是否完整？输出目录是否正确？ | 保存图片并生成报告 JSON | 落盘失败、报告缺失、目录错误 |

## 6. 标准调用

### 6.1 文本生图（T2I）

```bash
python3 .agents/skills/api/anyfast/image/seedream/scripts/seedream_generate.py \
  --prompt "生成连贯插画，核心为同一庭院一角的四季变迁，以统一风格展现四季独特色彩、元素与氛围" \
  --max-images 4 \
  --size 2K \
  --stream \
  --watermark
```

### 6.2 参考图生图（I2I）

```bash
python3 .agents/skills/api/anyfast/image/seedream/scripts/seedream_generate.py \
  --prompt "生成女孩和奶牛玩偶在游乐园开心地坐过山车的图片，涵盖早晨、中午、晚上" \
  --image-url "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_1.png" \
  --image-url "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_imagesToimages_2.png" \
  --max-images 3 \
  --size 2K \
  --stream \
  --watermark
```

### 6.3 Dry Run 验证

```bash
python3 .agents/skills/api/anyfast/image/seedream/scripts/seedream_generate.py \
  --prompt "测试提示词" \
  --dry-run --print-payload
```

### 6.4 自定义输出目录

```bash
python3 .agents/skills/api/anyfast/image/seedream/scripts/seedream_generate.py \
  --prompt "赛博朋克城市天际线" \
  --output-dir "output/影片/赛博唐人街/5-API/image/seedream/" \
  --filename-prefix "cyber"
```

## 7. 参数约定

| CLI 参数 | API 字段 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--model` | `model` | `doubao-seedream-5-0-260128` | 模型 ID |
| `--prompt` | `prompt` | （必填） | 提示词 |
| `--image-url` | `image[]` | 无 | 参考图 URL，可重复传入 |
| `--sequential-image-generation` | `sequential_image_generation` | `auto` | 连续图模式 |
| `--max-images` | `sequential_image_generation_options.max_images` | `4` | 连续图最大张数 |
| `--response-format` | `response_format` | `url` | `url` 或 `b64_json` |
| `--size` | `size` | `2K` | 输出尺寸 |
| `--stream` | `stream` | `false` | 启用流式返回 |
| `--watermark/--no-watermark` | `watermark` | `true` | 是否加水印 |
| `--extra-json` | 合并到请求体顶层 | 无 | 额外 JSON 字段 |

完整参数与字段说明见：`references/api.md`

## 8. 输出约定

- 默认输出目录：`output/影片/[项目名]/5-API/image/seedream/`
- 默认产物：
  - `*.png / *.jpg / *.jpeg / *.webp`（启用落盘时）
  - `seedream_report_YYYYmmdd_HHMMSS.json`（请求参数、结果 URL/Base64、错误信息）
- 报告文件必须包含：
  - `ok`：布尔，是否成功
  - `request`：完整请求 payload
  - `result_count`：提取图片数量
  - `results`：图片项列表（含 `url` / `b64_json` / `revised_prompt`）
  - `saved_files`：落盘文件路径列表
  - `final_payload`：最终 SSE 事件或响应体
  - `stream_event_count / stream_event_types`：流式事件摘要
  - `error`：失败时的错误信息

## 9. Root-Cause 执行契约（Mandatory）

当调用失败、参数异常或输出与预期不符时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：API Key 缺失、请求字段不符 Ark 接口、SSE 解析异常、图片落盘失败、输出目录不正确
-> `规则源`：`.agents/skills/api/anyfast/image/seedream/SKILL.md` 与 `scripts/seedream_generate.py`
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的 Root-Cause First / Field-Centric / CONTEXT 基线契约
-> `Fix Landing Points`：优先修脚本认证逻辑、请求体构造、SSE 解析、落盘逻辑和技能说明，再修局部调用样例

用户侧关闭语必须至少包含：
- 根因位置
- 立即修复
- 系统性预防修复

## 10. 失败排查

1. 检查 `.env` 是否存在 `SEEDREAM_API_KEY`（或 `ARK_API_KEY` / `VOLCENGINE_ARK_API_KEY`）
   - 若只是 `--dry-run --print-payload`，可在无 key 情况下先验证 payload
2. 使用 `--dry-run --print-payload` 确认请求参数正确
3. 若返回 4xx/5xx，查看报告文件中的 `error` 字段和 HTTP body
4. 若启用 `--stream` 无输出，先切到非流式重试（去掉 `--stream`）
5. 若 `--max-images >= 5` 的非流式连续多图读超时，先改用 `--stream`，或降低 `--max-images` 分批验证；脚本报告中的 `diagnostic_hint` 会给出建议
6. 若流式最终事件显示 `usage.generated_images > 0` 但 `result_count=0`，检查解析器是否兼容顶层 `url / b64_json` 事件
7. 确认输出目录是否符合：`output/影片/[项目名]/5-API/image/seedream/`
8. 若参考图调用失败：
   - 检查 `--image-url` 传入的 URL 是否可公网访问
   - 检查 payload 中 `image[]` 是否正确构造
9. 若图片落盘失败：
   - 检查 `response_format` 是否与实际返回匹配
   - 检查输出目录是否有写权限
10. 若报告文件不完整：
   - 检查 `--report-json` 路径是否合法
   - 检查磁盘空间

## 11. 字段通过表（Mandatory）

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| `FIELD-SDR-01` | 输入完整度 | `prompt` 存在且非空；参考图 URL 格式合法；`extra_json` 可解析 | `FAIL-SDR-INPUT` | 回到 `Step 1` 校验输入参数 |
| `FIELD-SDR-02` | 参数合规性 | API Key 存在；`response_format` 为 `url` 或 `b64_json`；`size` 为合法值 | `FAIL-SDR-PARAMS` | 回到 `Step 2` 修正参数与环境变量 |
| `FIELD-SDR-03` | 请求体合法性 | payload 符合 Ark `images/generations` 接口文档；`image[]` 为 URL 列表；`extra_json` 正确合并 | `FAIL-SDR-PAYLOAD` | 回到 `Step 3` 复核请求体构造 |
| `FIELD-SDR-04` | 执行稳定性 | HTTP 200 返回；SSE 正确解析并合并去重；图片列表为空时报告 `ok=false`；异常时生成错误报告 | `FAIL-SDR-EXEC` | 回到 `Step 4` 排查网络/SSE/API 问题 |
| `FIELD-SDR-05` | 输出可追溯性 | 至少生成报告 JSON；成功时图片正确落盘；报告字段完整；输出在正确目录 | `FAIL-SDR-OUTPUT` | 回到 `Step 5` 修正落盘与报告逻辑 |

## 12. 参考资料

- 接口摘要：`.agents/skills/api/anyfast/image/seedream/references/api.md`
- 官方文档：[Volcengine SEEDREAM 5.0](https://www.volcengine.com/docs/82379/1824121?lang=zh)
- 环境变量源：根目录 `.env`
- 依赖安装：`pip install -r .agents/skills/api/anyfast/image/seedream/requirements.txt`

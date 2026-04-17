---
name: sora
description: Use when the task must submit OpenAI Sora 2 video generation jobs through AnyFast, especially for text-to-video, first-frame image-to-video, async polling, remix reuse, and projectized download/report handling via `/v1/videos`.
governance_tier: full
---

# Sora 2 生视频技能

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 作用范围

- 本技能用于通过 AnyFast 的 OpenAI Sora 2 视频接口执行异步生视频任务。
- 官方文档主路径：
  - 文档索引：`https://docs.anyfast.ai/llms.txt`
  - 创建任务：`POST /v1/videos`
  - 查询任务：`GET /v1/videos/{id}`
  - 下载结果：`GET /v1/videos/{id}/content`
- 默认模型应始终指向当前已知最高档位；当前默认候选链为 `official-sora-2-pro -> sora-2-pro -> official-sora-2 -> sora-2`。技能必须保留这类模型别名漂移与档位回退的兼容空间，而不是把它当作调用者手误直接抹掉。
- 默认执行脚本：

```bash
python3 .agents/skills/api/video/sora/scripts/sora_video_generate.py ...
```

- 覆盖三类动作：
  - 文生视频
  - 图生视频（`input_reference` 首帧参考）
  - 视频混音（`remix_video_id`）

## 2. 必需输入

- `prompt`
- API Key
  - 优先读取根目录 `.env` 中的 `SORA_API_KEY`
  - 回退 `ANYFAST_VIDEO_API_KEY`
  - 再回退 `ANYFAST_API_KEY`
  - 也可显式传 `--api-key`

可选输入：

- `model`：不传时默认走最高档位候选链（当前首选 `official-sora-2-pro`）
- `image`：单张参考图，支持本地路径、远程 URL、`data:` URL
- `remix-video-id`
- `seconds`：`4 / 8 / 12`
- `size`：`720x1280 / 1280x720 / 1024x1792 / 1792x1024`
- `base-url`：优先 `.env` 中 `SORA_API_BASE_URL`，回退 `ANYFAST_API_BASE_URL`
- `project-name`
- `output-dir`
- `poll-interval`
- `max-wait-seconds`
- `filename-prefix`
- `report-json`
- `timeout`
- `dry-run`

## 3. 核心约束（Mandatory）

1. **三段异步流程刚性**
   - 不得把 Sora 2 当作同步接口。
   - 标准流程固定为：创建任务 -> 轮询状态 -> 下载结果。
2. **单参考图边界**
   - `input_reference` 只接受单张图。
   - 多图需求不得静默截断，必须报错并提示当前接口只支持单张首帧参考。
3. **模型漂移兼容**
   - 文档正文当前使用 `sora-2`，但真实网关还可能暴露 `official-sora-2` / `official-sora-2-pro`。
   - 未显式传 `--model` 时，脚本默认先尝试最高档位 `official-sora-2-pro`，再按质量顺序向下回退。
   - 显式传入 `--model` 时，优先尊重用户指定，只在同档别名间做兼容回退；不得在技能合同里假装只有单一模型名。
4. **下载端点返回 JSON，不是直接 MP4**
   - `GET /v1/videos/{id}/content` 返回的是包含 `video_url` 的 JSON。
   - 真正的 MP4 下载需要再访问 `video_url` / `url` 字段。
5. **项目化输出路径**
   - 默认输出目录必须为 `output/影片/[项目名]/5-API/video/sora/`。
   - 若未显式传 `project-name`，默认项目名使用 `测试`。
6. **密钥与加速端点分离**
   - AnyFast 的平台 URL、文档 URL、API Base URL、专用 Sora Key 需要分开表达。
   - 技能文档与报告只引用环境变量名，不落明文密钥。
7. **失败优先修源层**
   - 若出现模型名漂移、轮询逻辑缺失、下载逻辑错误、输出目录错误或鉴权/网关配置错配，优先修复：
     - `scripts/sora_video_generate.py`
     - 本 `SKILL.md`
     - `references/api.md`

## 4. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-SORA-01` | 输入解析结果：`prompt / image_input / remix_video_id / project_name` | `prompt` 非空；参考图至多一张；混音 ID 可选但格式可追溯 | 用户输入、CLI 参数 | Step 1 | 输入收束完整度 | `FAIL-SORA-INPUT` |
| `FIELD-SORA-02` | 参数裁决结果：`model / base_url / seconds / size / alias_candidates` | 枚举值合法；模型别名回退路径可解释；API 基础 URL 已明确 | 文档、截图、脚本默认值 | Step 2 | 参数与环境一致性 | `FAIL-SORA-PARAMS` |
| `FIELD-SORA-03` | 创建请求：`POST /v1/videos` multipart 请求体 | `model/prompt/seconds/size` 正确；参考图为单文件；必要时带 `remix_video_id` | AnyFast Sora 2 创建文档、脚本构造结果 | Step 3 | 请求体合法性 | `FAIL-SORA-CREATE` |
| `FIELD-SORA-04` | 轮询状态：`GET /v1/videos/{id}` 返回体 | 状态值被稳定识别；`queued/in_progress/completed/failed` 被正确处理 | AnyFast Sora 2 查询文档、API 响应 | Step 4 | 异步状态机稳定性 | `FAIL-SORA-STATUS` |
| `FIELD-SORA-05` | 下载结果：`GET /v1/videos/{id}/content` + 本地 MP4 | 先拿 `video_url/url`，再下载 MP4；报告里保留 JSON 响应和本地文件路径 | AnyFast Sora 2 下载文档、下载响应 | Step 5 | 输出闭环完整性 | `FAIL-SORA-DOWNLOAD` |

## 5. 思维导引与执行流程（Mandatory）

### 5.1 固定步骤

1. **Step 1 / 输入收束**
   - 读取 `prompt`、`image_input`、`remix_video_id`、`project_name`
   - 若存在参考图，只允许一张，并统一读成 `bytes + mime_type`
2. **Step 2 / 参数与环境裁决**
   - 校验 `seconds` 与 `size` 枚举
   - 读取 `SORA_API_KEY / ANYFAST_VIDEO_API_KEY / ANYFAST_API_KEY`
   - 读取 `SORA_API_BASE_URL / ANYFAST_API_BASE_URL`
   - 构造模型候选序列：若用户显式指定则优先该模型；若未指定则从最高档位链 `official-sora-2-pro -> sora-2-pro -> official-sora-2 -> sora-2` 依次尝试
3. **Step 3 / 创建任务**
   - 组装 multipart/form-data 请求到 `/v1/videos`
   - 提交 `model / prompt / seconds / size`
   - 若有参考图，提交 `input_reference`
   - 若有混音 ID，提交 `remix_video_id`
4. **Step 4 / 轮询状态**
   - 访问 `/v1/videos/{id}`
   - 若状态为 `queued / in_progress`，按 `poll_interval` 轮询直到完成或超时
   - 若状态为 `failed`，保留错误并终止
5. **Step 5 / 下载与落盘**
   - 调用 `/v1/videos/{id}/content`
   - 从返回 JSON 中提取 `video_url` 或 `url`
   - 下载 MP4 到默认项目化目录
   - 生成报告 JSON，记录创建、状态、下载三段摘要

### 5.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-SORA-01` | 是否已经收束 prompt、参考图和 remix 输入？ | 统一输入并校验参考图数量 | prompt 为空、多图输入、remix ID 丢失上下文 |
| `Step 2` | `FIELD-SORA-02` | API Key、Base URL、模型候选是否都已明确？ | 裁决环境变量与模型别名策略 | 环境变量缺失、模型别名无解释、参数越界 |
| `Step 3` | `FIELD-SORA-03` | 创建请求是否完全贴合 multipart 接口？ | 构造提交表单并发起创建 | `input_reference` 不是文件部件、字段错名、模型不被接受 |
| `Step 4` | `FIELD-SORA-04` | 轮询是否正确处理进行中、完成、失败三类状态？ | 稳定轮询并规范化状态报告 | 无限轮询、完成后未停、失败状态被吞掉 |
| `Step 5` | `FIELD-SORA-05` | 下载逻辑是否先拿 JSON 再取 MP4？ | 提取 `video_url` 并保存视频 | 把 `/content` 当作二进制、未落盘 MP4、报告缺下载摘要 |

## 6. 标准调用

### 6.1 一步跑完：提交 + 轮询 + 下载

```bash
python3 .agents/skills/api/video/sora/scripts/sora_video_generate.py run \
  --prompt "一只橘猫在金色夕阳下穿过向日葵田，电影镜头缓慢跟拍，暖色逆光" \
  --seconds 12 \
  --size 1280x720 \
  --project-name "测试"
```

### 6.2 图生视频：单张首帧参考

```bash
python3 .agents/skills/api/video/sora/scripts/sora_video_generate.py run \
  --prompt "让角色从静止首帧缓慢抬头，看向镜头，电影级自然光" \
  --image "/absolute/path/to/reference.png" \
  --seconds 8 \
  --size 720x1280 \
  --project-name "测试"
```

### 6.3 视频混音：沿用已有视频结构

```bash
python3 .agents/skills/api/video/sora/scripts/sora_video_generate.py run \
  --prompt "保持原视频的构图与运动节奏，但改成暴风雨夜景，霓虹反射更强" \
  --remix-video-id "video_69b131ea03548190925a6a06febf993b" \
  --seconds 12 \
  --size 1280x720
```

### 6.4 只创建任务，不等待

```bash
python3 .agents/skills/api/video/sora/scripts/sora_video_generate.py submit \
  --prompt "赛博城市高空俯拍，雨夜，车流穿梭" \
  --seconds 4 \
  --size 1792x1024
```

### 6.5 只查状态

```bash
python3 .agents/skills/api/video/sora/scripts/sora_video_generate.py status \
  --video-id "video_69b131ea03548190925a6a06febf993b"
```

### 6.6 只下载

```bash
python3 .agents/skills/api/video/sora/scripts/sora_video_generate.py download \
  --video-id "video_69b131ea03548190925a6a06febf993b" \
  --project-name "测试"
```

### 6.7 Dry Run 检查请求体

```bash
python3 .agents/skills/api/video/sora/scripts/sora_video_generate.py submit \
  --prompt "测试请求" \
  --seconds 4 \
  --size 720x1280 \
  --dry-run \
  --print-payload
```

## 7. 参数约定

| CLI 参数 | 创建/查询/下载字段 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--model` | `model` | `official-sora-2-pro` | 模型 ID；不传时默认走最高档位候选链，可显式覆盖为 `sora-2-pro` 或 `official-*` |
| `--prompt` | `prompt` | 必填 | 视频提示词 |
| `--image` | `input_reference` | 无 | 单张参考图，支持本地/远程/data URL |
| `--remix-video-id` | `remix_video_id` | 无 | 复用已完成视频的结构、动作和取景 |
| `--seconds` | `seconds` | `4` | `4 / 8 / 12` |
| `--size` | `size` | `720x1280` | `720x1280 / 1280x720 / 1024x1792 / 1792x1024` |
| `--base-url` | API Base URL | `.env` 回退链 | 优先 `SORA_API_BASE_URL`，回退 `ANYFAST_API_BASE_URL` |
| `--poll-interval` | 轮询间隔 | `10` | 仅 `run` 命令使用 |
| `--max-wait-seconds` | 最大等待时长 | `900` | 仅 `run` 命令使用 |

完整参数与字段说明见：`references/api.md`

## 8. 输出约定

- 默认输出目录：`output/影片/[项目名]/5-API/video/sora/`
- 默认产物：
  - `sora_submit_report_YYYYmmdd_HHMMSS.json`
  - `sora_status_report_YYYYmmdd_HHMMSS.json`
  - `sora_download_report_YYYYmmdd_HHMMSS.json`
  - `sora_run_report_YYYYmmdd_HHMMSS.json`
  - `*.mp4`
- 报告至少包含：
  - `ok`
  - `command`
  - `request_summary`
  - `normalized_submit`
  - `normalized_status`
  - `normalized_download`
  - `saved_file`
  - `raw_response`
  - `error`

## 9. Root-Cause 执行契约（Mandatory）

当创建失败、轮询卡住、下载缺 MP4、模型名不被接受或加速端点配置错位时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：API Key 缺失、`base_url` 指错、`/content` 被误当成二进制、模型别名漂移、参考图多于一张、轮询超时
-> `规则源`：`.agents/skills/api/video/sora/SKILL.md`、`references/api.md`、`scripts/sora_video_generate.py`
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的 Root-Cause First / Context Loading / Field-Centric / Canonical Source 治理契约
-> `Fix Landing Points`：优先修脚本环境变量回退、模型候选策略、轮询与下载逻辑，再修调用样例

用户侧关闭语必须至少包含：
- 根因位置
- 立即修复
- 系统性预防修复

## 10. 失败排查

1. 检查 `.env` 是否存在 `ANYFAST_VIDEO_API_KEY`，必要时补 `SORA_API_KEY`
2. 使用 `submit --dry-run --print-payload` 确认请求体和端点
3. 若创建阶段报模型错误：
   - 先检查默认候选链是否已从 `official-sora-2-pro` 向下尝试
   - 若用户显式指定了旧档模型，再确认是否需要切换到同档别名或更高档位
   - 若官方端点和当前加速端点都报 `No available channel for model ... under group auto (distributor)`，直接转查账户分组/渠道开通，不再重复试模型别名
4. 若状态一直停在 `queued / in_progress`：
   - 先确认 `max-wait-seconds` 是否太短
   - 再检查网关侧是否只接受查询但未真正入队
5. 若 `/content` 返回 400：
   - 先确认任务是否已经 `completed`
   - 再检查是否拿错了 `video_id`
6. 若 `/content` 成功但本地没有 MP4：
   - 检查响应里是否有 `video_url`
   - 检查二次下载是否被 CDN 拒绝或超时
7. 若参考图调用失败：
   - 检查 `--image` 是否只有一张
   - 检查远程 URL 是否可访问，或本地文件是否存在
8. 若报告缺字段：
   - 优先修 `scripts/sora_video_generate.py` 的规范化层
   - 不要只在单次运行里手工补值

## 11. 字段通过表（Mandatory）

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| `FIELD-SORA-01` | 输入收束完整度 | `prompt` 非空；参考图至多一张；`remix_video_id` 可追溯 | `FAIL-SORA-INPUT` | 回到 `Step 1` 复核输入 |
| `FIELD-SORA-02` | 参数与环境一致性 | API Key 存在；`seconds/size` 在允许枚举内；`base_url` 明确；模型候选可解释 | `FAIL-SORA-PARAMS` | 回到 `Step 2` 修正环境与参数 |
| `FIELD-SORA-03` | 请求体合法性 | multipart 请求符合文档；参考图为文件部件；模型字段有效 | `FAIL-SORA-CREATE` | 回到 `Step 3` 修正创建请求 |
| `FIELD-SORA-04` | 异步状态机稳定性 | 正确识别 `queued/in_progress/completed/failed`；轮询按间隔退出 | `FAIL-SORA-STATUS` | 回到 `Step 4` 修正轮询逻辑 |
| `FIELD-SORA-05` | 输出闭环完整性 | `/content` 先返回 JSON，再由 `video_url/url` 下载 MP4；报告路径与视频路径完整 | `FAIL-SORA-DOWNLOAD` | 回到 `Step 5` 修正下载与落盘 |

## 12. 参考资料

- 接口摘要：`.agents/skills/api/video/sora/references/api.md`
- 文档索引：[AnyFast llms.txt](https://docs.anyfast.ai/llms.txt)
- 创建任务：[Sora 2 创建视频](https://docs.anyfast.ai/zh/api-reference/model-api/openai/sora-2)
- 查询任务：[Sora 2 查询任务](https://docs.anyfast.ai/zh/api-reference/model-api/openai/sora-2-query)
- 下载视频：[Sora 2 下载视频](https://docs.anyfast.ai/zh/api-reference/model-api/openai/sora-2-download)

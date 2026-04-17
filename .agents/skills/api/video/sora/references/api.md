# AnyFast Sora 2 API 摘要

更新时间：`2026-04-17`

## 1. 文档入口

- 文档索引：`https://docs.anyfast.ai/llms.txt`
- 创建任务：`https://docs.anyfast.ai/zh/api-reference/model-api/openai/sora-2`
- 查询任务：`https://docs.anyfast.ai/zh/api-reference/model-api/openai/sora-2-query`
- 下载结果：`https://docs.anyfast.ai/zh/api-reference/model-api/openai/sora-2-download`

## 2. 基本工作流

Sora 2 是异步接口，标准流程固定为：

1. `POST /v1/videos` 创建任务
2. `GET /v1/videos/{id}` 轮询状态
3. `GET /v1/videos/{id}/content` 获取下载信息
4. 使用返回 JSON 中的 `video_url` 或 `url` 下载 MP4

## 3. 创建任务

### 3.1 端点

- API 网关端点：`https://fw2afus.ent.acc.kurtisasia.com/v1/videos`
- 加速端点：优先从 `.env` 读取 `SORA_API_BASE_URL`，回退 `ANYFAST_API_BASE_URL`

### 3.2 请求形态

- `multipart/form-data`

### 3.3 核心字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | 文档当前给出 `sora-2`；技能默认会先尝试最高已知档位 `official-sora-2-pro`，再按候选链回退 |
| `prompt` | string | 是 | 视频自然语言描述 |
| `seconds` | string | 否 | `4 / 8 / 12`，默认 `4` |
| `size` | string | 否 | `720x1280 / 1280x720 / 1024x1792 / 1792x1024` |
| `input_reference` | file | 否 | 单张首帧参考图，支持 `jpeg/png/webp` |
| `remix_video_id` | string | 否 | 已完成视频 ID，用于复用结构、动作、取景 |

### 3.4 响应核心字段

| 字段 | 说明 |
| --- | --- |
| `id` | 视频任务 ID，例如 `video_...` |
| `object` | 常见为 `video` |
| `model` | 返回的模型名 |
| `status` | 初始通常为 `queued` |
| `progress` | 初始通常为 `0` |
| `created_at` | Unix 时间戳 |
| `seconds` | 回显时长 |
| `size` | 回显分辨率 |

## 4. 查询状态

### 4.1 端点

- `GET /v1/videos/{id}`

### 4.2 状态枚举

- `queued`
- `in_progress`
- `completed`
- `failed`

### 4.3 常用响应字段

| 字段 | 说明 |
| --- | --- |
| `id` | 任务 ID |
| `status` | 当前状态 |
| `progress` | 当前进度 |
| `prompt` | 原始提示词 |
| `completed_at` | 完成时间，可能为 `null` |
| `expires_at` | 过期时间，可能为 `null` |
| `error` | 失败时的错误信息 |
| `remixed_from_video_id` | 混音来源视频 ID |

## 5. 下载结果

### 5.1 端点

- `GET /v1/videos/{id}/content`

### 5.2 关键注意

- 文档页面名叫“下载视频”，但返回体是 JSON，而不是直接的 MP4 字节流。
- 需要从返回 JSON 中拿：
  - `video_url`
  - 或 `url`
- 然后再下载该 URL 指向的 MP4 文件。

### 5.3 常用响应字段

| 字段 | 说明 |
| --- | --- |
| `id` | 任务 ID |
| `status` | 通常为 `completed` |
| `progress` | 通常为 `100` |
| `url` | 视频下载地址 |
| `video_url` | 视频下载地址，和 `url` 等价时应优先取其一 |
| `size` | 返回尺寸 |
| `seconds` | 返回时长 |
| `created_at` | 创建时间 |

## 6. 环境变量建议

建议在根目录 `.env` 使用以下分层：

```dotenv
# AnyFast API
ANYFAST_PLATFORM_URL=...
ANYFAST_API_BASE_URL=...
ANYFAST_DOCS_URL=https://docs.anyfast.ai
ANYFAST_API_KEY=...
ANYFAST_VIDEO_API_KEY=...

# Optional Sora overrides
SORA_API_BASE_URL=...
SORA_API_KEY=...
```

优先级建议：

- Key：`SORA_API_KEY` -> `ANYFAST_VIDEO_API_KEY` -> `ANYFAST_API_KEY`
- Base URL：`SORA_API_BASE_URL` -> `ANYFAST_API_BASE_URL` -> `https://fw2afus.ent.acc.kurtisasia.com`

## 7. 模型名漂移说明

文档正文当前使用：

- `sora-2`

真实加速网关还可能存在以下更高或等价档位：

- `official-sora-2-pro`
- `sora-2-pro`
- `official-sora-2`

因此脚本层建议保留质量优先的候选模型链：

1. 未显式传 `--model` 时，按 `official-sora-2-pro -> sora-2-pro -> official-sora-2 -> sora-2` 依次尝试
2. 显式传 `--model` 时，只在同档等价别名之间做兼容回退，避免擅自覆盖用户意图

## 8. 推荐验证顺序

1. 先跑 `submit --dry-run --print-payload`
2. 再跑 `submit` 拿到 `video_id`
3. 用 `status` 验证状态推进
4. 任务完成后再跑 `download`
5. 稳定后再用 `run` 一步串起来

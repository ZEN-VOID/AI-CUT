# FineAPI / Luma API 摘要

更新时间：`2026-04-17`

## 1. 当前可确认真源

- FineAPI 文档页：`https://docs.fineapi.cloud/403045611e0`
- 用户提供的 FineAPI 截图
- 用户提供的请求示例与响应示例
- 官方 Luma 文档：
  - 创建与 generation 管理：[Video Generation](https://docs.lumalabs.ai/docs/video-generation)
  - 轮询与成片获取：[Python Video Generation](https://docs.lumalabs.ai/docs/python-video-generation)

说明：

- FineAPI 文档页当前是前端渲染页面，直接抓取拿到的是页面壳；本文件只沉淀本轮稳定确认的信息。
- FineAPI 的创建接口已直接确认。
- FineAPI 的查询路径未在当前页面中直接展开；本文件将其与官方 Luma generation 轮询模型分开表达，避免把推断伪装成已确认真源。

## 2. FineAPI 创建任务

### 2.1 端点

- `POST /luma/generations`

### 2.2 请求头

```http
Accept: application/json
Content-Type: application/json
Authorization: Bearer <token>
```

### 2.3 请求体

最小样例：

```json
{
  "user_prompt": "一阵风吹过树林，使女人的面纱微微飘动。",
  "model_name": "ray-2",
  "duration": "5s",
  "resolution": "720p"
}
```

截图可见的扩展字段：

```json
{
  "user_prompt": "一阵风吹过树林，使女人的面纱微微飘动。",
  "expand_prompt": true,
  "loop": false,
  "image_url": "https://example.com/frame0.png",
  "image_end_url": "https://example.com/frame1.png",
  "notify_hook": "https://example.com/webhook",
  "resolution": "720p",
  "duration": "5s",
  "model_name": "ray-2"
}
```

### 2.4 字段说明

| 字段 | 类型 | 必填 | 已确认说明 |
| --- | --- | --- | --- |
| `user_prompt` | string | 是 | FineAPI 创建接口的提示词字段 |
| `model_name` | string | 是 | 官方当前模型文档以 `ray-2` 为最新稳定名；FineAPI 既有样例/截图曾出现 `ray-v1 / ray-v2`，默认模型治理统一回指 `../../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族，当前解析结果为 `ray-2`，并保留对 `ray-v2` 的兼容回退 |
| `duration` | string | 是 | 截图明确“时长只支持 5s” |
| `resolution` | string | 是 | 截图显示 `720p` 或 `1080p`，默认 `720p` |
| `expand_prompt` | boolean | 否 | 提示词优化开关 |
| `loop` | boolean | 否 | 是否循环视频 |
| `image_url` | string | 否 | 起始关键帧图片 URL |
| `image_end_url` | string | 否 | 目标关键帧图片 URL |
| `notify_hook` | string | 否 | 完成后的回调地址 |

## 3. FineAPI 创建响应

用户提供样例：

```json
{
  "id": "4665a07c-7641-4809-a133-10786201bb56",
  "prompt": "",
  "state": "pending",
  "queue_state": null,
  "created_at": "2024-12-22T13:38:40.139409Z",
  "batch_id": "",
  "video": null,
  "video_raw": null,
  "liked": null,
  "estimate_wait_seconds": null,
  "thumbnail": null,
  "last_frame": null
}
```

### 3.1 已确认字段

| 字段 | 说明 |
| --- | --- |
| `id` | generation ID，UUID 形态 |
| `prompt` | 当前样例为空字符串 |
| `state` | 当前样例为 `pending` |
| `queue_state` | 队列状态，可能为 `null` |
| `created_at` | ISO 时间戳 |
| `batch_id` | 批次 ID，可能为空 |
| `video` | 成片字段之一，初始可能为 `null` |
| `video_raw` | 原始视频字段之一，初始可能为 `null` |
| `thumbnail` | 缩略图 |
| `last_frame` | 最后一帧图像 |
| `estimate_wait_seconds` | 预计等待时间 |

## 4. 官方 Luma generation 模型

官方 Luma 文档当前确认：

- 创建端点：`POST https://api.lumalabs.ai/dream-machine/v1/generations`
- 查询端点：`GET https://api.lumalabs.ai/dream-machine/v1/generations/{id}`
- Python 文档明确说明：
  - create 返回 UUID
  - 拿到视频的方式是 polling
  - completed 后可从 generation 中读取视频地址（示例写成 `generation.assets.video`）

因此：

- “异步三段式：创建 -> 轮询 -> 下载”是官方 confirmed 模式。
- FineAPI 是否把查询端点精确映射成 `/luma/generations/{id}`，当前仍属于镜像推断，不是当前页面直接展示的真源。

## 5. 当前技能采用的查询策略

默认查询路径模板：

```text
/luma/generations/{id}
```

这是基于以下两点做的最小风险推断：

1. FineAPI 已确认创建端点为 `/luma/generations`
2. 官方 Luma generation 查询端点与创建端点共享 `generations/{id}` 资源结构

为了避免把推断写死，脚本必须允许：

- `--status-path-template`

如果当前网关不是该路径，调用方应显式覆盖，而不是修改技能真源去假装已经确认。

## 6. 环境变量建议

建议在根目录 `.env` 使用以下分层：

```dotenv
FINEAPI_DOCS_URL=https://docs.fineapi.cloud
FINEAPI_API_BASE_URL=
FINEAPI_API_KEY=

LUMA_API_BASE_URL=
LUMA_API_KEY=

# Generic video fallback
ANYFAST_API_BASE_URL=
ANYFAST_API_KEY=
ANYFAST_VIDEO_API_KEY=
```

优先级建议：

- Key：`LUMA_API_KEY` -> `FINEAPI_API_KEY` -> `ANYFAST_VIDEO_API_KEY` -> `ANYFAST_API_KEY`
- Base URL：`LUMA_API_BASE_URL` -> `FINEAPI_API_BASE_URL`

补充：

- 2026-04-17 实测当前工作区的 `ANYFAST_API_BASE_URL=https://fw2afus.ent.acc.kurtisasia.com`
  - `POST /luma/generations` 返回前端 HTML 壳页
  - `POST /v1/luma/generations` 返回 `Invalid URL`
- 因此对 Luma 技能，不应再把 `ANYFAST_API_BASE_URL` 当成默认 Base URL 回退。

## 7. 模型名说明

当前信号存在两套命名：

- FineAPI 既有示例与截图：`ray-v1 / ray-v2`
- 官方 Luma 文档：`ray-2`（以及其他官方系列名）

因此脚本层建议保留候选模型重试策略：

1. 先尝试用户指定值；未指定时按 `../../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族取当前已登记 Ray 系列最高版本（当前为 `ray-2`）
2. 若创建报模型不可用，再回退 `ray-v2`
3. 若使用旧模型链路，可尝试 `ray-v1 -> ray-1.6`

## 8. 推荐验证顺序

1. 先跑 `submit --dry-run --print-payload`
2. 再跑 `submit` 拿到 `generation_id`
3. 用 `status` 验证默认查询模板是否适配当前网关
4. 若状态进入 `completed`，再跑 `download`
5. 稳定后再使用 `run` 一步串起来

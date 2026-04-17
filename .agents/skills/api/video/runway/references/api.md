# FineAPI Runway / 官方 Runway API 摘要

更新时间：`2026-04-17`

## 1. 真源与分层

### 1.1 FineAPI 创建页

- 页面：`https://docs.fineapi.cloud/403045611e0`
- 已确认：
  - `POST /runwayml/v1/image_to_video`
  - Header：`Accept`、`Authorization`、`Content-Type`
  - Body 字段：
    - `promptImage`
    - `model`
    - `promptText`
    - `watermark`
    - `duration`
    - `ratio`
    - `seed`
- 用户给出的请求示例：

```json
{
  "promptImage": "https://www.bt.cn/bbs/template/qiao/style/image/btlogo.png",
  "model": "gen4_turbo",
  "promptText": "cat dance",
  "watermark": false,
  "duration": 5,
  "ratio": "1280:768"
}
```

- 用户给出的创建响应示例：

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

### 1.2 官方 Runway 任务模型

来源：

- 官方 API Reference：`https://docs.dev.runwayml.com/api/`
- SDK / 任务轮询说明：`https://docs.dev.runwayml.com/api-details/sdks/`
- 输出格式：`https://docs.dev.runwayml.com/assets/outputs/`
- 输入与 ratio 说明：`https://docs.dev.runwayml.com/assets/inputs/`

已确认：

- 创建：`POST /v1/image_to_video`
- 任务查询：`GET /v1/tasks/{id}`
- 成功输出：`output[]`
- 任务会异步流转到：
  - `PENDING`
  - `RUNNING` / 类似进行中状态
  - `SUCCEEDED`
  - `FAILED`
  - `CANCELED`

## 2. 本技能采用的兼容路径

### 2.1 创建路径

直接来自 FineAPI 页面：

```text
POST /runwayml/v1/image_to_video
```

### 2.2 状态路径

**这是兼容推导，不是 FineAPI 页面当前已明示字段。**

推导方式：

1. 官方 Runway 任务查询是 `GET /v1/tasks/{id}`
2. FineAPI 创建页使用了 `runwayml` 前缀
3. 因此本技能默认尝试：

```text
GET /runwayml/v1/tasks/{id}
```

若代理网关未暴露该路径，最常见症状是 `404`。

## 3. Header 与鉴权

FineAPI 创建页给出的最小头：

```http
Accept: application/json
Authorization: Bearer <token>
Content-Type: application/json
```

本技能统一从 `.env` 读取：

```dotenv
ANYFAST_VIDEO_API_KEY=...
```

建议同时保留：

```dotenv
RUNWAY_API_BASE_URL=...
FINEAPI_API_BASE_URL=...
```

优先级建议：

- Key：`ANYFAST_VIDEO_API_KEY -> RUNWAY_API_KEY -> ANYFAST_API_KEY`
- Base URL：真实请求用 `RUNWAY_API_BASE_URL -> FINEAPI_API_BASE_URL`
- `ANYFAST_API_BASE_URL` 只建议保留给 dry-run 或其他已验证 provider；2026-04-17 实测当前工作区该通用 host 对 `/runwayml/v1/image_to_video` 返回前端 HTML，不应再作为 Runway 真实请求默认回退

## 4. 请求字段

| 字段 | 类型 | 必填 | 当前处理 |
| --- | --- | --- | --- |
| `promptImage` | string | 是 | HTTPS URL、Data URI；本地图由脚本转成 Data URI |
| `model` | string | 是 | 默认按当前已知最高版本自动解析，当前为 `gen4.5` |
| `promptText` | string | 是 | 非空提示词 |
| `watermark` | boolean | 否 | 显式传值时才发送 |
| `duration` | integer | 否 | 页面截图显示 `5 / 10` |
| `ratio` | string | 是 | 输出比例/分辨率字符串 |
| `seed` | integer | 否 | 随机种子 |

## 5. 模型与 ratio 漂移

### 5.1 FineAPI 页面/用户示例

- FineAPI 用户示例仍是 `gen4_turbo`
- 本技能默认已切到当前官方图生视频已知最高版本 `gen4.5`
- 本技能默认 ratio 改为随模型动态补齐；当前默认组合为 `gen4.5 + 1280:720`

### 5.2 官方 Runway ratio 说明

根据官方 `Inputs` 页面摘要：

- `gen3a_turbo` 支持：`1280:768`、`768:1280`
- `gen4_turbo` 支持：
  - `1280:720`
  - `1584:672`
  - `1104:832`
  - `720:1280`
  - `832:1104`
  - `960:960`
- `gen4.5` 支持：
  - `1280:720`
  - `1584:672`
  - `1104:832`
  - `720:1280`
  - `832:1104`
  - `672:1584`
  - `960:960`

### 5.3 本技能的处理原则

- 不直接硬拒 `gen4_turbo + 1280:768`
- 在报告中写入 `validation_notes`
- 若代理报错，再回退到官方推荐的 ratio
- 默认组合必须保持自洽；当前默认值以 `gen4.5 + 1280:720` 为准，不再沿用旧的 `gen4_turbo + 1280:768`

## 6. 图片输入规则

官方 Runway 输入文档指出：

- URL 必须是 `https://`
- URL 不应是裸 IP
- 服务端应返回正确 `Content-Type` / `Content-Length`
- 不跟随重定向

本技能处理策略：

- `https://...`：原样提交
- `data:image/...`：原样提交
- 本地文件：读取后转 `data:image/...;base64,...`
- `http://...`：拒绝

## 7. 响应与下载

### 7.1 FineAPI 创建响应

当前已见字段：

- `id`
- `prompt`
- `state`
- `queue_state`
- `created_at`
- `video`
- `video_raw`
- `thumbnail`
- `last_frame`

### 7.2 官方 Runway 任务成功响应

官方输出文档说明成功任务会返回：

```json
{
  "id": "<task-id>",
  "status": "SUCCEEDED",
  "createdAt": "...",
  "output": [
    "https://.../output.mp4?_jwt=..."
  ]
}
```

注意：

- `output[]` URL 是临时地址
- 官方说明通常在 24-48 小时内失效
- 应立即下载到本地或自有存储
- 若 `submit/status` 返回 `200` 但响应体是 `<!doctype html>...` 之类前端页面，则说明命中了错误网关或控制台壳页，不得把它当作成功 JSON

### 7.3 本技能下载字段优先级

1. `output[]`
2. `video`
3. `video_raw`
4. `video_url`

## 8. 推荐验证顺序

1. 先跑：

```bash
python3 .agents/skills/api/video/runway/scripts/runway_video_generate.py submit \
  --prompt "测试请求" \
  --image "https://www.bt.cn/bbs/template/qiao/style/image/btlogo.png" \
  --dry-run \
  --print-payload
```

2. 再提交真实任务
3. 用 `status` 验证 `GET /runwayml/v1/tasks/{id}` 是否被当前网关接受
4. 任务成功后立即下载成片
5. 如遇 ratio 报错，再切到官方推荐组合重试

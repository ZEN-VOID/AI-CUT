# 漫涂 Grok 视频 API 参考

## 1. 基础信息

- Base URL：优先使用根目录 `.env` 中的 `MAN_TUI_GROK_API_BASE_URL`，回退 `MAN_TUI_GROK_CONNECTION_JSON.url`、`MAN_TUI_API_BASE_URL`
- 默认值：`https://api.man-tui.com`
- 默认模型：`grok-imagine-video`
- 认证：`Authorization: Bearer <MAN_TUI_GROK_API_KEY>`，回退 `MAN_TUI_GROK_CONNECTION_JSON.key`、`MAN_TUI_API_KEY`

## 2. 创建任务

- `POST /v1/videos`
- 请求类型：`multipart/form-data`

### 核心字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `model` | string | 默认 `grok-imagine-video` |
| `prompt` | string | 视频描述词 |
| `input_reference` | binary | 本地参考图上传，单张 |
| `image_reference` | string | 远程参考图 URL 数组字符串 |
| `seconds` | integer | 允许值：`6 / 10 / 12 / 16 / 20` |
| `size` | string | 允许值：`1280x720 / 720x1280 / 1792x1024 / 1024x1792 / 1024x1024` |
| `quality` | string | `standard / high` |

### 创建成功响应

```json
{
  "id": "task_xxx",
  "task_id": "task_xxx",
  "object": "video",
  "model": "grok-imagine-video",
  "status": "queued",
  "progress": 0,
  "created_at": 1776166320,
  "seconds": "10",
  "size": "1792x1024"
}
```

## 3. 查询任务状态

- `GET /v1/videos/{task_id}`

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 任务 ID |
| `status` | string | 典型值：`queued / completed / failed` |
| `progress` | integer | 任务进度 |
| `model` | string | 模型名 |
| `url` | string or null | 有时会直接给最终视频地址 |

## 4. 获取视频内容

- `GET /v1/videos/{task_id}/content`
- 典型行为：
  - 直接返回 `200 application/octet-stream`
  - 或返回 `302` 跳转到 CDN 下载地址

## 5. 认证说明

- 推荐 Header：

```http
Authorization: Bearer <MAN_TUI_GROK_API_KEY>
```

- 平台也兼容直接传 API Key 或 `x-api-key`，但本技能默认统一使用 Bearer 方案，减少歧义。

## 6. curl 示例

### 6.1 远程参考图

```bash
curl https://api.man-tui.com/v1/videos \
  -H "Authorization: Bearer ${MAN_TUI_GROK_API_KEY}" \
  -F "model=grok-imagine-video" \
  -F "prompt=动漫电影质感，双角色同框，电影级光影，不要字幕，不要水印。" \
  -F "seconds=10" \
  -F "size=1792x1024" \
  -F "quality=high" \
  -F 'image_reference=["https://example.com/ref-a.png","https://example.com/ref-b.png"]'
```

### 6.2 本地参考图

```bash
curl https://api.man-tui.com/v1/videos \
  -H "Authorization: Bearer ${MAN_TUI_GROK_API_KEY}" \
  -F "model=grok-imagine-video" \
  -F "prompt=电影级夜景角色视频，动作克制自然。" \
  -F "seconds=10" \
  -F "size=1792x1024" \
  -F "quality=high" \
  -F "input_reference=@/abs/path/ref.png"
```

### 6.3 查询状态

```bash
curl https://api.man-tui.com/v1/videos/task_xxx \
  -H "Authorization: Bearer ${MAN_TUI_GROK_API_KEY}"
```

### 6.4 下载视频

```bash
curl https://api.man-tui.com/v1/videos/task_xxx/content \
  -H "Authorization: Bearer ${MAN_TUI_GROK_API_KEY}" \
  --output task_xxx.mp4
```

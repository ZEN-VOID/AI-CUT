# 漫涂 Sora 2 视频 API 参考

## 1. 基础信息

- Base URL：优先使用根目录 `.env` 中的 `MAN_TUI_API_BASE_URL`
- 默认值：`https://api.man-tui.com`
- 默认模型：`sora-2`
- provider 口径补充（2026-04-19）：`sora` 在“默认分组”，不在 `GrokVideo-异步轮询`
- 认证：
  - 推荐 Header：`Authorization: Bearer <MAN_TUI_API_KEY>`
  - 兼容：`Authorization: <MAN_TUI_API_KEY>` 或 `x-api-key: <MAN_TUI_API_KEY>`
  - 实测注记（2026-04-19）：当前环境下 `Authorization` 可达，但 `x-api-key` 返回 `401 Invalid token`；执行技能时应优先使用 `Authorization`

## 1.1 repo-local 分组覆盖约定

由于当前公开片段没有给出 provider “group” 的正式写法，本仓库为 `man-tui-sora-video` 额外补了一个本地兼容层：

- 默认 `group=default`
- 默认 `group_transport=header`
- 默认 `group_header=X-Group`

可通过以下环境变量覆盖：

- `MAN_TUI_API_GROUP`
- `MAN_TUI_API_GROUP_TRANSPORT`
- `MAN_TUI_API_GROUP_HEADER`

也可通过 CLI 覆盖：

- `--group`
- `--group-transport off|header|body|both`
- `--group-header`

当前这套 group 覆盖属于 repo-local routing workaround，不是来自公开 OpenAPI 的正式字段定义。
provider 后续已明确表示：当前问题更像后台默认分组选错，而不是客户端没传对某个 group 字段。

## 2. 创建任务

- `POST /v1/videos`
- 请求类型：`application/json`

### 核心字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `prompt` | string | 视频描述词，支持中英文 |
| `model` | string | 固定 `sora-2` |
| `seconds` | string/int | 允许值：`10 / 15` |
| `size` | string | 允许值：`720x1280 / 1280x720` |
| `input_reference` | string | 图生视频参考图 URL，必须公网可访问 |
| `group` | string | repo-local 可选覆盖字段，默认 `default`；仅在 `group_transport` 包含 `body` 时注入 |

### 创建成功响应

```json
{
  "id": "task_xxx",
  "task_id": "task_xxx",
  "object": "ai_workflow.generation",
  "model": "sora-2",
  "status": "queued",
  "progress": 0,
  "created_at": 1776185746
}
```

## 3. 查询任务状态

- `GET /v1/videos/{task_id}`

### 状态说明

| 状态 | 说明 |
| --- | --- |
| `queued` | 排队中 |
| `in_progress` | 生成中 |
| `completed` | 已完成，可尝试读取下载链接 |

### 关键响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `status` | string | 当前任务状态 |
| `progress` | integer | 进度 0~100 |
| `content_violation` | boolean | 为 `true` 时视频不可用 |
| `watermark_free_url` | string/null | 去水印视频主下载地址，优先使用 |
| `video_url` | string/null | 备用视频链接 |
| `image_url` | string/null | 封面图 URL |
| `result` | object/array | 完成后常为对象，包含详细结果 |

### 完成态中的 `result` 常见字段

| 字段 | 说明 |
| --- | --- |
| `message` | 完成提示，例如 `Sora创建完成` |
| `share_url` | 原始分享链接，可作为次级下载回退 |
| `thumb_url` | 原始缩略图链接 |
| `preview_image_url` | 预览图 |
| `watermark_free_url` | 去水印视频链接 |
| `watermark_free_url_src` | 去水印原始源地址 |
| `generation_id` | 生成 ID |

## 4. 下载策略

本接口文档未单列 `/content` 下载端点；完成后应从状态响应中解析 URL：

1. 顶层 `watermark_free_url`
2. 顶层 `video_url`
3. `result.watermark_free_url`
4. `result.share_url`

下载链接常带签名参数，通常 5 天内有效，报告中必须脱敏后再落盘。

## 4.1 实测兼容性注记

- 2026-04-19 实测：
  - `Authorization: Bearer <key>` -> 可达，但当前账号/分发组对 `sora-2` 返回 `503 model_not_found`
  - `Authorization: <key>` -> 同样可达，并返回相同 `model_not_found`
  - `x-api-key: <key>` -> 返回 `401 Invalid token`
- 因此，若看到 `No available channel for model sora-2 under group ...`，优先判定为 provider 通道不可用，而不是本地脚本 JSON 构造错误。
- 后续若要验证“默认分组”是否真的生效，优先对比三种模式：
  - `--group default --group-transport header`
  - `--group default --group-transport body`
  - `--group default --group-transport both`
- 2026-04-19 实测补充：三种模式都仍返回 `under group GrokVideo-异步轮询 (distributor)`，说明当前 provider 至少没有按本地 group 覆盖改变实际路由。
- provider 后续回复：`sora` 走默认分组，`grok` 异步单独一个分组，画图单独一个分组；因此后续主修复路径应是让 provider 切换 key 的后台默认分组。

## 5. curl 示例

### 5.1 文生视频

```bash
curl https://api.man-tui.com/v1/videos \
  -H "Authorization: Bearer ${MAN_TUI_API_KEY}" \
  -H "X-Group: default" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"一只橙色猫咪在樱花树下打盹，花瓣飘落，电影级光影",
    "model":"sora-2",
    "seconds":"10",
    "size":"1280x720"
  }'
```

### 5.2 图生视频

```bash
curl https://api.man-tui.com/v1/videos \
  -H "Authorization: Bearer ${MAN_TUI_API_KEY}" \
  -H "X-Group: default" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"花瓣随风飘落，猫咪缓缓睁开眼睛",
    "model":"sora-2",
    "seconds":"10",
    "size":"720x1280",
    "input_reference":"https://example.com/reference.png",
    "group":"default"
  }'
```

### 5.3 查询状态

```bash
curl https://api.man-tui.com/v1/videos/task_xxx \
  -H "X-Group: default" \
  -H "Authorization: Bearer ${MAN_TUI_API_KEY}"
```

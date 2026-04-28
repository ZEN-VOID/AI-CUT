# Vidu 视频 API 总览

## 官方链接

- [reference-to-video](https://platform.vidu.cn/docs/reference-to-video)
- [text-to-video](https://platform.vidu.cn/docs/text-to-video)
- [image-to-video](https://platform.vidu.cn/docs/image-to-video)
- [start-end-to-video](https://platform.vidu.cn/docs/start-end-to-video)
- [multi-frame](https://platform.vidu.cn/docs/multi-frame)
- [template](https://platform.vidu.cn/docs/template)
- [template-story](https://platform.vidu.cn/docs/template-story)
- [search-task-api](https://platform.vidu.cn/docs/search-task-api)
- [tasks-list](https://platform.vidu.cn/docs/tasks-list)
- [cancel-task-api](https://platform.vidu.cn/docs/cancel-task-api)
- [search-credits](https://platform.vidu.cn/docs/search-credits)
- [callback-signature](https://platform.vidu.cn/docs/callback-signature)
- [error-code](https://platform.vidu.cn/docs/error-code)

## 最后核对日期

- `2026-04-21`

## 端点/认证

- Base URL：`https://api.vidu.cn`
- 企业版前缀：`/ent/v2`
- 默认认证头：
  - `Authorization: Token <VIDU_API_KEY>`
  - `Content-Type: application/json`

## 请求体字段总表

| 模块 | 端点 | 核心输入 |
| --- | --- | --- |
| `reference2video` | `POST /ent/v2/reference2video` | `model` `subjects` `prompt` |
| `text2video` | `POST /ent/v2/text2video` | `model` `prompt` |
| `img2video` | `POST /ent/v2/img2video` | `model` `images` |
| `start-end2video` | `POST /ent/v2/start-end2video` | `model` `images(2张)` |
| `multiframe` | `POST /ent/v2/multiframe` | `model` `start_image` `image_settings` |
| `template` | `POST /ent/v2/template` | `template` `images` |
| `template-story` | `POST /ent/v2/template-story` | `story` `images` |

## 子字段展开表

| 复合字段 | 关键子字段 | 说明 |
| --- | --- | --- |
| `subjects[]` | `name` `images` `videos` `voice_id` `server_id` | 主体参照专用 |
| `image_settings[]` | `key_image` `prompt` `duration` | 智能多帧关键帧 |
| `creations[]` | `id` `url` `watermarked_url` `cover_url` | 查询生成物接口返回 |

## 模型差异矩阵

| 模式 | 模型差异要点 |
| --- | --- |
| `reference2video` | `viduq3-turbo/viduq3` 支持智能切镜与音画同出；`viduq2-pro` 额外支持视频主体 |
| `text2video` | `viduq3-turbo` 更快；`viduq3-pro` 质量更高；`style` 在 q2/q3 不生效 |
| `img2video` | q3/q2/q1/2.0 的模型面最广；不同模型的时长/清晰度能力不完全一致 |
| `start-end2video` | 与 `img2video` 类似，但必须首尾两张图 |
| `multiframe` | 仅 `viduq2-turbo`、`viduq2-pro` |
| `template-story` | 当前示例故事包括 `love_story`、`workday_feels`、`monkey_king`、`pigsy`、`monk_tang`、`one_shot` |

## 默认值/范围/限制

- 通用图片格式：`png / jpeg / jpg / webp`
- 通用图片比例：小于 `1:4` 或 `4:1`
- Base64 必须带 `data:<mime>;base64,`
- 图像/视频 URL 必须可访问
- 查询生成物里的下载 URL 通常只有 `24h` 有效

## 响应体字段

- 创建类端点通常返回：
  - `task_id`
  - `state`
  - `model`
  - `prompt/images/...`
  - `credits`
  - `created_at`
- 真正的成片下载地址不在创建响应里，而在：
  - `GET /ent/v2/tasks/{id}/creations`

## 任务状态/错误码

- 通用任务状态：
  - `created`
  - `queueing`
  - `processing`
  - `success`
  - `failed`
- 常见错误码：
  - `FieldLacking`
  - `FieldUnwanted`
  - `FieldItemCountOutOfRange`
  - `PageSizeOutOfRange`
  - `ImageDownloadFailure`

## repo-local 执行建议

- 简单模式走 CLI sugar。
- 复杂模式优先走 `--input-json`。
- 本地媒体由脚本转成 `data:` URL，但大文件要慎用。
- 创建成功只代表拿到 `task_id`，不能代表视频已经可下载。
- 下载、状态与积分统一以 `task-management.md` 对应接口为准。

## 已验证的真实踩坑记录

- `reference2video + q3-turbo + 16秒` 在“大图 + 长 prompt + 多张 PNG”组合下容易在创建阶段超时；压缩为轻量 JPEG 后可成功受理。
- `template-story one_shot` 当前实测不是单图模板，至少需要 `3` 张图。
- `img2video + viduq3-pro-fast` 传 `resolution=540p` 会被服务端拒绝，省略后服务端默认回填 `720p`。
- `multiframe` 在大图场景更容易遇到连接层问题，优先使用轻量 JPG。

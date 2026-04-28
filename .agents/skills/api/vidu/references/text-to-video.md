# Vidu 文生视频

## 官方链接

- [text-to-video](https://platform.vidu.cn/docs/text-to-video)

## 最后核对日期

- `2026-04-21`

## 端点/认证

- `POST https://api.vidu.cn/ent/v2/text2video`
- 认证：`Authorization: Token <VIDU_API_KEY>`

## 请求体字段总表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | `string` | 是 | `viduq3-turbo` `viduq3-pro` `viduq2` `viduq1` |
| `style` | `string` | 否 | `general/anime`；q2/q3 不生效 |
| `prompt` | `string` | 是 | 最长 `5000` 字符 |
| `duration` | `int` | 否 | 随模型变化 |
| `seed` | `int` | 否 | 随机种子 |
| `aspect_ratio` | `string` | 否 | 默认 `16:9` |
| `resolution` | `string` | 否 | 随模型变化 |
| `movement_amplitude` | `string` | 否 | q2/q3 不生效 |
| `payload` | `string` | 否 | 透传字段 |
| `off_peak` | `bool` | 否 | 错峰生成 |
| `watermark` | `bool` | 否 | 水印开关 |
| `wm_position` | `int` | 否 | 水印位置 |
| `wm_url` | `string` | 否 | 水印图片 URL |
| `meta_data` | `string` | 否 | 元数据 JSON 字符串 |
| `callback_url` | `string` | 否 | 状态回调 |

## 子字段展开表

本接口无复杂嵌套结构；重点是 `model/duration/resolution/off_peak/audio` 的组合约束。

## 模型差异矩阵

| 模型 | 特点 | 时长 | 分辨率 |
| --- | --- | --- | --- |
| `viduq3-turbo` | 较 `q3-pro` 更快 | `3-16s`，默认 `5s` | `540p/720p/1080p`，默认 `720p` |
| `viduq3-pro` | 质量更高 | `3-16s`，默认 `5s` | `540p/720p/1080p`，默认 `720p` |
| `viduq2` | 最新 q2 文生能力 | `1-10s`，默认 `5s` | `540p/720p/1080p`，默认 `720p` |
| `viduq1` | 画面清晰、运镜稳定 | `5s` | `1080p` |

## 默认值/范围/限制

- `style` 默认 `general`
- `anime` 只在动漫风格表现突出
- q2/q3 系列模型中 `style` 不生效
- `prompt` 最长 `5000` 字符
- `movement_amplitude` 在 q2/q3 不生效

## 响应体字段

常见字段：
- `task_id`
- `state`
- `model`
- `prompt`
- `duration`
- `resolution`
- `aspect_ratio`
- `credits`
- `created_at`

## 任务状态/错误码

- 任务状态：
  - `created`
  - `queueing`
  - `processing`
  - `success`
  - `failed`
- 常见错误：
  - `FieldLacking`
  - `FieldUnwanted`
  - `FieldItemCountOutOfRange`

## repo-local 执行建议

- 常规 smoke test 优先 `viduq3-turbo + 3s/5s`。
- 需要稳定快速验证链路时，先用短时长和默认 `720p`。
- 若后续要长期批量化，文生任务也建议保留 JSON 真源，以便回放。

## 已验证的真实踩坑记录

- `viduq3-turbo` 的 `text2video` 已在本地真实跑通，查询与下载链路可用。
- `off_peak` 创建后可被取消，取消后任务会落为 `failed` 且 `err_code=UserCancelled`。

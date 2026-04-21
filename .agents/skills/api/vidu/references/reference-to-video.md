# Vidu 参考生视频

## 官方链接

- [reference-to-video](https://platform.vidu.cn/docs/reference-to-video)

## 最后核对日期

- `2026-04-21`

## 端点/认证

- `POST https://api.vidu.cn/ent/v2/reference2video`
- 请求头：
  - `Authorization: Token <VIDU_API_KEY>`
  - `Content-Type: application/json`

## 请求体字段总表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | `string` | 是 | `viduq3-turbo` `viduq3` `viduq2-pro` `viduq2` `viduq1` `vidu2.0` |
| `auto_subjects` | `bool` | 否 | 智能主体库，默认 `false` |
| `subjects` | `array` | 是 | 主体列表 |
| `prompt` | `string` | 是 | 最长 `5000` 字符，可用 `@主体name` 引用主体 |
| `audio` | `bool` | 否 | q3/q3-turbo 默认 `true` |
| `audio_type` | `string` | 条件 | `audio=true` 时使用，`all/speech_only/sound_effect_only` |
| `duration` | `int` | 否 | 时长，随模型变化 |
| `seed` | `int` | 否 | 0 或不传时随机 |
| `aspect_ratio` | `string` | 否 | 默认 `16:9`；常用 `16:9/9:16/1:1` |
| `resolution` | `string` | 否 | 默认与模型、时长相关 |
| `movement_amplitude` | `string` | 否 | `auto/small/medium/large`，q2/q3 不生效 |
| `payload` | `string` | 否 | 透传，最多 `1048576` 字符 |
| `off_peak` | `bool` | 否 | 错峰生成 |
| `watermark` | `bool` | 否 | 是否带水印 |
| `wm_position` | `int` | 否 | `1/2/3/4` |
| `wm_url` | `string` | 否 | 水印图片 URL |
| `meta_data` | `string` | 否 | JSON 字符串元数据 |
| `callback_url` | `string` | 否 | 状态回调地址 |

## 子字段展开表

### `subjects[]`

| 子字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | `string` | 是 | 主体 id，可在 prompt 里用 `@name` 引用 |
| `images` | `array[string]` | 条件 | 与 `videos` 二选一 |
| `videos` | `array[string]` | 条件 | 与 `images` 二选一；仅 `viduq2-pro` 支持视频主体 |
| `voice_id` | `string` | 否 | 音色 ID；q3 参考生不生成该参数 |
| `server_id` | `string` | 否 | 使用已有主体库时必传 |

### `subjects[].images`

| 规则 | 内容 |
| --- | --- |
| 输入形式 | 图片 URL 或 `data:image/...;base64,...` |
| 数量限制 | 最多 `3` 张 |
| 格式 | `png/jpeg/jpg/webp` |
| 比例 | 小于 `1:4` 或 `4:1` |
| 大小 | base64 decode 后小于 `20MB` |

### `subjects[].videos`

| 规则 | 内容 |
| --- | --- |
| 适用模型 | 仅 `viduq2-pro` |
| 槽位规则 | 图片和视频共享 `3` 个槽位 |
| 视频数量 | 支持 `1` 个 `5s` 视频 |
| 格式 | `mp4/avi/mov` |
| 尺寸 | 像素不能小于 `128x128`，比例小于 `1:4` 或 `4:1` |
| 大小 | base64 decode 后小于 `20MB` |

## 模型差异矩阵

| 模型 | 主体能力 | 音频 | 时长 | 分辨率 |
| --- | --- | --- | --- | --- |
| `viduq3-turbo` | 图片/文字主体 | 默认 `audio=true` | `3-16s`，默认 `5s` | `540p/720p/1080p`，默认 `720p` |
| `viduq3` | 图片/文字主体 | 默认 `audio=true` | `3-16s`，默认 `5s` | `540p/720p/1080p`，默认 `720p` |
| `viduq2-pro` | 图片/文字/视频主体 | 默认 `audio=false` | `0-10s`，默认 `5s` | `540p/720p/1080p`，默认 `720p` |
| `viduq2` | 图片/文字主体 | 默认 `audio=false` | `1-10s`，默认 `5s` | `540p/720p/1080p`，默认 `720p` |
| `viduq1` | 图片/文字主体 | 默认 `audio=false` | `5s` | `1080p` |
| `vidu2.0` | 图片/文字主体 | 默认 `audio=false` | `4s` | `360p/720p`，默认 `360p` |

## 默认值/范围/限制

- q3/q2/q1/2.0：
  - 只能使用图片主体和文字主体
  - 图片或文字主体最多不超过 `7` 个
- q2-pro：
  - 图片或文字主体最多不超过 `4` 个
  - 视频主体最多不超过 `2` 个
  - 如果是临时视频主体，则最多 `1` 个
- `viduq3-mix` 当前不支持主体
- `movement_amplitude` 在 q2/q3 不生效
- `off_peak`：
  - q3 模型需 `audio=true` 才支持
  - q2/q1/2.0 系列需 `audio=false` 才支持

## 响应体字段

创建响应常见字段：

| 字段 | 说明 |
| --- | --- |
| `task_id` | 任务 ID |
| `state` | `created/queueing/processing/success/failed` |
| `model` | 本次模型 |
| `prompt` | 本次提示词 |
| `images` | 调用时的图像参数 |
| `duration` | 时长 |
| `resolution` | 分辨率 |
| `aspect_ratio` | 比例 |
| `credits` | 积分消耗 |
| `created_at` | 创建时间 |

## 任务状态/错误码

- 常见状态：
  - `created`
  - `queueing`
  - `processing`
  - `success`
  - `failed`
- 常见错误：
  - `FieldLacking`
  - `FieldUnwanted`
  - `FieldItemCountOutOfRange`
  - `PageSizeOutOfRange`
  - `ImageDownloadFailure`

## repo-local 执行建议

- `subjects` 请优先走 `--input-json`。
- 一个 `name` 代表一个主体，同一主体下的多张 `images` 应优先使用“同一人不同角度/光线/表情”的参考。
- 本地图片和视频可直接传路径，由脚本转 `data:` URL。
- 复杂 prompt 建议先从 `aigc/6-Video` 的上游真源提炼，再压缩到适合 Vidu 的主体参照句法。

## 已验证的真实踩坑记录

- `@name` 的多图不是“多主体混装”，而是同一主体的多视角/多状态参考。
- `q3-turbo + 16秒 + 主体参照` 本身可用，但“大 PNG + 长 prompt + 多图”容易在创建阶段连接超时。
- 把主体图压缩成轻量 JPEG、减少图数后，可以稳定受理并完成生成。

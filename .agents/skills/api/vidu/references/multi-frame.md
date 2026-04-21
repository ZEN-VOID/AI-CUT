# Vidu 智能多帧

## 官方链接

- [multi-frame](https://platform.vidu.cn/docs/multi-frame)

## 最后核对日期

- `2026-04-21`

## 端点/认证

- `POST https://api.vidu.cn/ent/v2/multiframe`
- 认证：`Authorization: Token <VIDU_API_KEY>`

## 请求体字段总表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | `string` | 是 | `viduq2-turbo` `viduq2-pro` |
| `start_image` | `string` | 是 | 首帧图像 |
| `image_settings` | `array` | 是 | 关键帧配置，最少 2，最多 9 |
| `resolution` | `string` | 否 | `540p/720p/1080p`，默认 `720p` |
| `watermark` | `bool` | 否 | 水印开关 |
| `wm_url` | `string` | 否 | 水印图 |
| `wm_position` | `string` | 否 | `top_left/top_right/bottom_right/bottom_left` |
| `meta_data` | `string` | 否 | 元数据 |
| `payload` | `string` | 否 | 透传字段 |
| `callback_url` | `string` | 否 | 状态回调 |

## 子字段展开表

### `start_image`

| 规则 | 内容 |
| --- | --- |
| 数量 | 仅 `1` 张 |
| 格式 | `png/jpeg/jpg/webp` |
| 比例 | 小于 `1:4` 或 `4:1` |
| 图片大小 | 小于 `50MB` |
| POST body | 文档注明 `post body` 不超过 `10MB` |

### `image_settings[]`

| 子字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `key_image` | `string` | 是 | 当前关键帧图像 |
| `prompt` | `string` | 否 | 从上一张延长到当前帧的提示词 |
| `duration` | `int` | 否 | 当前段时长，默认 `5s`，可选 `2-7s` |

补充规则：
- 输入顺序即时间轴顺序
- 每个 `key_image` 只支持 `1` 张图
- 文档注明 `post body` 不超过 `20MB`

## 模型差异矩阵

| 模型 | 说明 |
| --- | --- |
| `viduq2-turbo` | 速度优先 |
| `viduq2-pro` | 质量更强 |

## 默认值/范围/限制

- 关键帧最少 `2`，最多 `9`
- `resolution` 默认 `720p`
- `wm_position` 默认 `bottom_left`
- `payload` 最多 `1048576` 字符

## 响应体字段

常见字段：
- `task_id`
- `state`
- `model`
- `start_image`
- `image_settings`
- `resolution`
- `credits`
- `created_at`

## 任务状态/错误码

- 状态：
  - `created`
  - `queueing`
  - `processing`
  - `success`
  - `failed`
- 常见错误：
  - `FieldLacking`
  - `FieldItemCountOutOfRange`
  - `PageSizeOutOfRange`

## repo-local 执行建议

- 强烈建议走 `--input-json` 或 `--image-setting-json-file`
- 关键帧顺序必须按时间轴写好
- 多帧比普通图生更容易卡在请求体体积上，优先小图

## 已验证的真实踩坑记录

- 使用原始大图时，创建阶段出现过 `urllib/ssl` 连接异常。
- 换成更轻量的 JPG 后，`multiframe` 成功受理并完成生成。

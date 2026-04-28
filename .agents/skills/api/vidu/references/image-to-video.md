# Vidu 图生视频

## 官方链接

- [image-to-video](https://platform.vidu.cn/docs/image-to-video)

## 最后核对日期

- `2026-04-21`

## 端点/认证

- `POST https://api.vidu.cn/ent/v2/img2video`
- 认证：`Authorization: Token <VIDU_API_KEY>`

## 请求体字段总表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | `string` | 是 | `viduq3-turbo` `viduq3-pro` `viduq3-pro-fast` `viduq2-pro-fast` `viduq2-pro` `viduq2-turbo` `viduq1` `viduq1-classic` `vidu2.0` |
| `images` | `array[string]` | 是 | 图像输入 |
| `prompt` | `string` | 否 | 文本描述 |
| `duration` | `int` | 否 | 时长 |
| `seed` | `int` | 否 | 随机种子 |
| `aspect_ratio` | `string` | 否 | 比例 |
| `resolution` | `string` | 否 | 分辨率 |
| `movement_amplitude` | `string` | 否 | q2/q3 不生效 |
| `payload` | `string` | 否 | 透传字段 |
| `off_peak` | `bool` | 否 | 错峰生成 |
| `watermark` | `bool` | 否 | 水印开关 |
| `wm_position` | `int` | 否 | 水印位置 |
| `wm_url` | `string` | 否 | 水印图片 URL |
| `meta_data` | `string` | 否 | 元数据 |
| `callback_url` | `string` | 否 | 状态回调 |

## 子字段展开表

### `images`

| 规则 | 内容 |
| --- | --- |
| 输入方式 | URL 或 `data:image/...;base64,...` |
| 图片数量 | 以官方该接口当前页面约束为准；repo-local 常用 1 张 |
| 格式 | `png/jpeg/jpg/webp` |
| 比例 | 小于 `1:4` 或 `4:1` |

## 模型差异矩阵

| 模型 | 特点 |
| --- | --- |
| `viduq3-pro-fast` | 速度更快，性价比较高 |
| `viduq3-turbo` | 较 `q3-pro` 更快 |
| `viduq3-pro` | 质量更好 |
| `viduq2-pro-fast` | 较 `q2-turbo` 提速 2-3 倍 |
| `viduq2-pro` | 效果好、细节丰富 |
| `viduq2-turbo` | 生成快 |
| `viduq1` | 清晰、平滑转场 |
| `viduq1-classic` | 转场和运镜更丰富 |
| `vidu2.0` | 生成速度快 |

## 默认值/范围/限制

- q2/q3 下 `movement_amplitude` 不生效
- 图像必须满足官方比例与格式要求
- 本地脚本支持把文件路径自动转成 `data:` URL

## 响应体字段

创建响应常见字段：
- `task_id`
- `state`
- `model`
- `images`
- `duration`
- `resolution`
- `aspect_ratio`
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
  - `FieldUnwanted`
  - `PageSizeOutOfRange`

## repo-local 执行建议

- 单张首帧驱动时，优先用较小的 JPG/PNG。
- 图生链路的最终成片 URL 仍要从查询生成物接口拿。
- 需要复现具体服务端字段行为时，保留原始 JSON。

## 已验证的真实踩坑记录

- `viduq3-pro-fast` 图生视频真实跑通。
- `viduq3-pro-fast + resolution=540p` 当前实测会返回 `400 FieldInvalid: resolution`。
- 省略 `resolution` 后，服务端会默认回填 `720p` 并成功生成。
- 使用过大的 PNG 更容易在创建阶段超时，轻量图更稳。

# Vidu 首尾帧生视频

## 官方链接

- [start-end-to-video](https://platform.vidu.cn/docs/start-end-to-video)

## 最后核对日期

- `2026-04-21`

## 端点/认证

- `POST https://api.vidu.cn/ent/v2/start-end2video`
- 认证：`Authorization: Token <VIDU_API_KEY>`

## 请求体字段总表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | `string` | 是 | `viduq3-turbo` `viduq3-pro` `viduq2-pro-fast` `viduq2-pro` `viduq2-turbo` `viduq1` `viduq1-classic` `vidu2.0` |
| `images` | `array[string]` | 是 | 首尾帧图像 |
| `prompt` | `string` | 否 | 从首帧过渡到尾帧的描述 |
| `duration` | `int` | 否 | 时长 |
| `seed` | `int` | 否 | 随机种子 |
| `resolution` | `string` | 否 | 分辨率 |
| `payload` | `string` | 否 | 透传字段 |
| `off_peak` | `bool` | 否 | 错峰生成 |
| `watermark` | `bool` | 否 | 水印开关 |
| `callback_url` | `string` | 否 | 状态回调 |

## 子字段展开表

### `images`

| 规则 | 内容 |
| --- | --- |
| 数量 | 应为 `2` 张 |
| 顺序 | 第 1 张起始帧，第 2 张结束帧 |
| 输入方式 | URL 或 `data:image/...;base64,...` |

## 模型差异矩阵

| 模型 | 说明 |
| --- | --- |
| `viduq3-turbo` | 更快 |
| `viduq3-pro` | 质量更优 |
| `viduq2-pro-fast` | 更高性价比 |
| `viduq2-pro` | 细节更丰富 |
| `viduq2-turbo` | 生成快 |
| `viduq1` | 稳定 |
| `viduq1-classic` | 运镜更丰富 |
| `vidu2.0` | 速度快 |

## 默认值/范围/限制

- `images` 不足 2 张或多于 2 张都不应提交
- 首尾帧应尽量保持同一主体与空间连续性

## 响应体字段

常见字段：
- `task_id`
- `state`
- `model`
- `images`
- `duration`
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

- 本地脚本默认按数组顺序解释两张图，不做额外推断。
- 先用小图确认可用性，再切回高质量图。

## 已验证的真实踩坑记录

- `viduq3-pro + 3s` 的首尾帧生视频真实跑通。
- 使用较小的角色图更容易稳定完成创建与生成。

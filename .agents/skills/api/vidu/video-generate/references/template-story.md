# Vidu 模板成片

## 官方链接

- [template-story](https://platform.vidu.cn/docs/template-story)

## 最后核对日期

- `2026-04-21`

## 端点/认证

- `POST https://api.vidu.cn/ent/v2/template-story`
- 认证：`Authorization: Token <VIDU_API_KEY>`

## 请求体字段总表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `story` | `string` | 是 | `love_story` `workday_feels` `monkey_king` `pigsy` `monk_tang` `one_shot` |
| `images` | `array[string]` | 是 | 输入图像 |
| `payload` | `string` | 否 | 透传字段 |
| `callback_url` | `string` | 否 | 状态回调 |

## 子字段展开表

### `images`

| 规则 | 内容 |
| --- | --- |
| 输入形式 | URL 或 `data:image/...;base64,...` |
| 格式 | `png/jpeg/jpg/webp` |
| 比例 | 以官方示例中心说明为准 |
| 大小 | 小于 `50MB` |
| POST body | 不超过 `20MB` |

## 模型差异矩阵

- 模板成片当前更像固定故事模板能力，不由外部 `model` 字段切换。
- `one_shot` 的视频比例与输入首图比例相同。

## 默认值/范围/限制

- `story` 只能取当前页面列出的枚举
- 图片比例要求需再查官方“场景示例中心-模板成片”

## 响应体字段

常见字段：
- `task_id`
- `state`
- `story`
- `images`
- `payload`
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

- 使用模板成片时，图片数量不要凭直觉猜。
- 优先保留为 JSON 真源，便于复盘故事模板与图片集合。

## 已验证的真实踩坑记录

- `one_shot` 不是单图模板。
- 当前实测中：
  - 单图调用返回 `400`
  - 服务端明确要求至少 `3` 张图、最多 `10` 张图
- 补足 `3` 张图后任务成功。

# Vidu 场景特效模板

## 官方链接

- [template](https://platform.vidu.cn/docs/template)

## 最后核对日期

- `2026-04-21`

## 端点/认证

- `POST https://api.vidu.cn/ent/v2/template`
- 认证：`Authorization: Token <VIDU_API_KEY>`

## 请求体字段总表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `template` | `string` | 是 | 模板名；需去场景示例中心确认 |
| `images` | `array[string]` | 是 | 输入图像 |
| `prompt` | `string` | 否 | 模板补充描述 |
| `payload` | `string` | 否 | 透传字段 |
| `callback_url` | `string` | 否 | 状态回调 |

## 子字段展开表

### `images`

| 规则 | 内容 |
| --- | --- |
| 输入形式 | URL 或 `data:image/...;base64,...` |
| 格式 | `png/jpeg/jpg/webp` |
| 比例 | 小于 `1:4` 或 `4:1` |
| 大小 | 小于 `50MB` |
| POST body | 不超过 `20MB` |

## 模型差异矩阵

- 模板能力以模板本身为主，不像普通 `model` 字段那样由调用方直接切换。
- 不同模板的参数要求不同，应以官方“场景示例中心”为准。

## 默认值/范围/限制

- 模板名不应靠猜，应先从官方示例中心确认
- 某些模板会有额外图片数或比例要求

## 响应体字段

常见字段：
- `task_id`
- `state`
- `template`
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
  - `FieldUnwanted`
  - `FieldItemCountOutOfRange`

## repo-local 执行建议

- 优先走 `--input-json`
- 模板名和专属参数必须先去官方示例中心确认，不建议在 CLI 层硬编码猜测

## 已验证的真实踩坑记录

- 当前仓库尚未对 `/template` 做成功任务实测。
- 现阶段最大的风险不是脚本，而是模板名和模板专属字段来源不足。

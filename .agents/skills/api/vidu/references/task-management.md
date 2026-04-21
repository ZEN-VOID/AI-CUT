# Vidu 任务管理

## 官方链接

- [search-task-api](https://platform.vidu.cn/docs/search-task-api)
- [tasks-list](https://platform.vidu.cn/docs/tasks-list)
- [cancel-task-api](https://platform.vidu.cn/docs/cancel-task-api)
- [search-credits](https://platform.vidu.cn/docs/search-credits)
- [error-code](https://platform.vidu.cn/docs/error-code)

## 最后核对日期

- `2026-04-21`

## 端点/认证

| 动作 | 端点 | 方法 |
| --- | --- | --- |
| 查询生成物 | `https://api.vidu.cn/ent/v2/tasks/{id}/creations` | `GET` |
| 查询任务列表 | `https://api.vidu.cn/ent/v2/tasks` | `GET` |
| 取消任务 | `https://api.vidu.cn/ent/v2/tasks/{id}/cancel` | `POST` |
| 查询积分 | `https://api.vidu.cn/ent/v2/credits` | `GET` |

认证统一为：
- `Authorization: Token <VIDU_API_KEY>`
- `Content-Type: application/json`

## 请求体字段总表

### 查询生成物

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | `string` | 是 | 任务 ID |

### 查询任务列表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `created_at.from` | `string` | 否 | 开始时间，默认 7 天 |
| `created_at.to` | `string` | 否 | 结束时间，默认 7 天 |
| `task_ids` | `array` | 否 | 任务 ID 列表 |
| `templates` | `array` | 否 | 模板列表 |
| `model_versions` | `array` | 否 | 模型版本 |
| `resolutions` | `array` | 否 | 分辨率 |
| `states` | `array` | 否 | 状态过滤 |
| `paper.page` | `int` | 否 | 页码，默认 0 |
| `paper.pagesz` | `int` | 否 | 每页数量，默认 10，最大 100 |
| `pager.page_token` | `string` | 否 | 下一页起始 token |

### 取消任务

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | `string` | 是 | 任务 ID |

### 查询积分

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `show_detail` | `bool` | 是 | 默认 `false` |

## 子字段展开表

### `creations[]`

| 子字段 | 说明 |
| --- | --- |
| `id` | 生成物 ID |
| `url` | 无水印视频 URL，通常 `24h` 有效 |
| `watermarked_url` | 带水印视频 URL |
| `cover_url` | 封面 URL |

### 积分返回 `remains[]`

| 子字段 | 说明 |
| --- | --- |
| `type` | 资源包类型 |
| `credit_remain` | 剩余积分 |
| `concurrency_limit` | 并发上限 |
| `current_concurrency` | 当前并发 |

## 模型差异矩阵

- 查询与取消接口不按模型拆分，但列表接口支持 `model_versions` 过滤。
- 错峰任务与即时任务都经同一套任务管理接口查询。

## 默认值/范围/限制

- 任务列表默认时间范围：最近 `7` 天
- `paper.pagesz` 最大 `100`
- 下载 URL 通常为短期签名链接，应尽快落盘

## 响应体字段

### 查询生成物

常见字段：
- `state`
- `err_code`
- `credits`
- `payload`
- `creations[]`

### 查询任务列表

常见字段：
- `tasks[]`
- `paper`
- `pager`

### 取消任务

- 成功返回 `{}` 空对象

### 查询积分

常见字段：
- `packages`
- `remains`
- `queue_count`

## 任务状态/错误码

### 通用状态

- `created`
- `queueing`
- `processing`
- `success`
- `failed`

### 常见错误码

| 错误码 | 说明 |
| --- | --- |
| `BadRequest` | 不合法请求 |
| `FieldLacking` | 缺字段 |
| `FieldUnwanted` | 传了不该传的字段 |
| `FieldItemCountOutOfRange` | 列表数量超限 |
| `PageSizeOutOfRange` | 图像尺寸或分页大小相关限制问题 |
| `ImageDownloadFailure` | 远程图像下载失败 |

## repo-local 执行建议

- 创建成功后，一律用查询生成物接口看终态和拿下载地址。
- 任务列表适合作为旁路取证，不适合替代单任务查询。
- `cancel` 更适合验证管理链路，取消后再查状态确认是否落成 `failed/UserCancelled`。
- `credits` 应在真实消耗前后各查一次。

## 已验证的真实踩坑记录

- `task/list/cancel/credits` 已全部真实跑通。
- 取消测试任务后：
  - 任务状态为 `failed`
  - `err_code=UserCancelled`
  - `credits=0`
- `character2video` 这类主体参照任务，创建响应可能较慢，用 `list` 旁路取证很有帮助。

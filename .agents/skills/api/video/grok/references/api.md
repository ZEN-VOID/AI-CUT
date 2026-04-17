# FineAPI Grok Video 3 API 摘要

更新时间：`2026-04-17`

## 1. 当前可确认真源

- 文档页：`https://docs.fineapi.cloud/403045611e0`
- 用户提供的截图
- 用户提供的请求示例与响应示例

说明：

- 该文档页在当前环境下为前端渲染页面，直接抓取只能拿到页面壳。
- 因此本文件只沉淀本轮已稳定确认的创建接口事实与本地 live probe 结果；未确认的后续接口不写成真源。

## 1.1 当前默认模型结论

- 官方文档截图与历史样例稳定出现的是 `grok-video-3`。
- `2026-04-17` 在当前配置环境做真实提交时，`grok-video-3` 成功创建任务。
- 同日对 `grok-video-3-max` 做真实提交，返回：
  - `status_code: 503`
  - `error.code: model_not_found`
  - `error.message`: `分组 auto 下模型 grok-video-3-max 无可用渠道（distributor）`
- 因此当前技能的默认模型保持为“当前环境最高已验证可用版本” `grok-video-3`，而不是按外部命名推测升级。

## 2. 创建任务

### 2.1 端点

- `POST /v1/video/create`

### 2.2 请求头

```http
Accept: application/json
Content-Type: application/json
Authorization: Bearer <token>
```

### 2.3 Body 结构

```json
{
  "model": "grok-video-3",
  "prompt": "小猫在吃鱼 --mode=custom",
  "aspect_ratio": "3:2",
  "size": "720P",
  "images": [
    "https://ark-project.tos-cn-beijing.volces.com/doc_image/seedream4_5_imageToimage.png"
  ]
}
```

### 2.4 字段说明

| 字段 | 类型 | 必填 | 已确认说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | 官方截图与样例稳定出现 `grok-video-3`；当前环境 live probe 也验证它可用 |
| `prompt` | string | 是 | 提示词；样例保留 `--mode=custom` 后缀 |
| `aspect_ratio` | string | 是 | 截图显示可选 `2:3 / 3:2 / 1:1` |
| `size` | string | 是 | 截图写有 `720P` 或 `1080P`，并注明“暂只支持 720P” |
| `images` | array[string] | 是 | 截图说明为“图片链接” |

## 3. 创建响应

```json
{
  "id": "veo3.1-components:1762241017-xTL0P9HvGF",
  "status": "pending",
  "status_update_time": 1762241017286
}
```

### 3.1 已确认字段

| 字段 | 说明 |
| --- | --- |
| `id` | 任务 ID |
| `status` | 示例值为 `pending` |
| `status_update_time` | 状态更新时间戳 |

## 4. 当前未锁定的部分

以下内容本轮没有拿到稳定文档，因此不得写死到脚本或主合同里：

- 查询状态端点
- 下载视频端点
- API 默认 host
- 失败响应的固定 schema
- 比 `grok-video-3` 更高的可用模型 ID（当前只验证到 `grok-video-3-max` 不可用）

## 5. 环境变量建议

建议在根目录 `.env` 使用以下分层：

```dotenv
ANYFAST_PLATFORM_URL=https://www.anyfas.ai
ANYFAST_DOCS_URL=https://docs.anyfast.ai
ANYFAST_API_BASE_URL=
ANYFAST_VIDEO_API_KEY=
ANYFAST_API_KEY=

FINEAPI_DOCS_URL=https://docs.fineapi.cloud
FINEAPI_API_BASE_URL=
FINEAPI_API_KEY=
FINEAPI_GROK_API_KEY=

GROK_VIDEO_API_BASE_URL=
GROK_VIDEO_API_KEY=
```

优先级建议：

- Key：`ANYFAST_VIDEO_API_KEY` -> `GROK_VIDEO_API_KEY` -> `ANYFAST_API_KEY` -> `FINEAPI_GROK_API_KEY` -> `FINEAPI_API_KEY`
- Base URL：`ANYFAST_API_BASE_URL` -> `GROK_VIDEO_API_BASE_URL` -> `FINEAPI_GROK_API_BASE_URL` -> `FINEAPI_API_BASE_URL`

## 6. 推荐验证顺序

1. 先跑 `submit --dry-run --print-payload`
2. 再用默认模型和一张已知可访问的公网图跑 `submit`
3. 确认只收到 `task receipt`
4. 若尝试更高模型名，必须以真实回执判定是否可用；`model_not_found` 视为不可用而非“默认值应继续上调”
5. 若要补查询/下载闭环，先取得对应文档页，再扩展脚本

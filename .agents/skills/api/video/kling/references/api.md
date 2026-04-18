# FineAPI Kling API 摘要

更新时间：`2026-04-17`

## 1. 真源页面映射

### 1.1 本轮确认有效的 Kling 页面

- 新版创建页（推荐主真源）：<https://docs.fineapi.cloud/422568253e0>
- 旧版创建页（补边界说明）：<https://docs.fineapi.cloud/403045624e0>
- 查询页：<https://docs.fineapi.cloud/403045626e0>

### 1.2 页面漂移说明

用户给出的 `<https://docs.fineapi.cloud/403045611e0>` 在 2026-04-17 实际对应 **Veo 的 OpenAI 风格创建视频页**，不是 Kling。维护 `kling` 技能时不得再把该页当作真源。

## 2. 创建图生视频任务

### 2.1 端点

- `POST /kling/v1/videos/image2video`

### 2.2 请求形态

- `application/json`

### 2.3 Header

- `Accept: application/json`
- `Content-Type: application/json`
- `Authorization: Bearer <token>`

### 2.4 已确认字段

| 字段 | 类型 | 必填 | 来源 | 说明 |
| --- | --- | --- | --- | --- |
| `model_name` | string | 否 | 新版页 | 新版页枚举含 `kling-v3`；旧版页未出现 `kling-v3`；默认模型治理统一回指 `../../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族 |
| `mode` | string | 否 | 新版页 | `std / pro` |
| `duration` | string | 否 | 新版页 | `3-15` |
| `image` | string | 否 | 新旧页 | URL 或裸 Base64，和 `image_tail` 至少二选一 |
| `image_tail` | string | 否 | 新旧页 | URL 或裸 Base64；尾帧控制 |
| `prompt` | string | 条件必填 | 新版页 | `multi_shot=false` 或 `shot_type=intelligence` 时必填 |
| `negative_prompt` | string | 否 | 新旧页 | 负向提示词 |
| `cfg_scale` | number | 否 | 新版页 | 仅 `kling-v1.x` 稳定支持 |
| `sound` | string | 否 | 新版页 | `on / off`，说明写明仅 `v2.6+` 支持 |
| `multi_shot` | boolean | 否 | 新版页 | 多镜头模式 |
| `shot_type` | string | 条件必填 | 新版页 | `customize / intelligence` |
| `multi_prompt` | array | 条件必填 | 新版页 | `multi_shot=true` 且 `shot_type=customize` 时必填 |
| `static_mask` | string | 否 | 新版页 | URL 或 Base64 |
| `dynamic_masks` | array | 否 | 新版页 | 蒙版与轨迹 |
| `camera_control` | object\|null | 否 | 新版页 | 相机控制 |
| `element_list` | array | 否 | 新版页 | 最多 3 个；与 `voice_list` 互斥 |
| `voice_list` | array | 否 | 新版页 | 最多 2 个；与 `element_list` 互斥 |
| `watermark_info` | object | 否 | 新版页 | 仅确认 `enabled` 子字段 |
| `callback_url` | string | 否 | 新旧页 | 状态回调 |
| `external_task_id` | string | 否 | 新版页 | 用户侧唯一任务 ID |

### 2.5 新旧页共同边界

- `image` / `image_tail` 支持：
  - 公网 URL
  - 裸 Base64
- 若用 Base64：
  - **不要带 `data:image/...;base64,` 前缀**
- 图片要求：
  - `.jpg / .jpeg / .png`
  - 大小不超过 `10MB`
  - 宽高不小于 `300px`
  - 宽高比在 `1:2.5 ~ 2.5:1`

### 2.6 关键依赖/互斥

- `image` 与 `image_tail` 至少二选一
- `image_tail`、`dynamic_masks/static_mask`、`camera_control` 三组选项互斥
- `static_mask` 与 `dynamic_masks` 不应同时传入
- `multi_shot=true` 时：
  - `shot_type` 必填
  - `shot_type=customize` 时 `multi_prompt` 必填
  - `shot_type=intelligence` 时 `prompt` 仍必填
- `element_list` 与 `voice_list` 互斥
- `cfg_scale` 仅 `kling-v1.x` 支持
- `sound=on` 仅 `kling-v2-6` 及后续版本支持

### 2.7 本地默认值与文档默认值的差异

- FineAPI 新版页写的 `model_name` 默认值仍是 `kling-v1`
- 本任务要求：默认模型治理统一回指 `../../runbooks/default-model-policy.md`
- Kling 当前归属 `highest-available-general` 规则族；脚本通过 `../../shared/default_model_policy.py` 从允许列表解析当前结果 `kling-v3`
- 截至 `2026-04-17`，本地白名单解析结果为 `kling-v3`
- 这属于本地技能合同覆写，不代表 FineAPI 页面默认值已经变更

### 2.8 创建响应

旧版页明确展示的响应示例：

```json
{
  "id": "2016934404056231936",
  "task_id": "2016934404056231936",
  "object": "video",
  "model": "kling-v1-6",
  "status": "",
  "progress": 0,
  "created_at": 1769709609
}
```

用户提供的简化响应示例：

```json
{
  "code": 0,
  "message": "string",
  "data": {}
}
```

因此脚本层必须同时兼容：

- 直接返回 `id/task_id/...`
- 包裹在 `code/message/data` 里的新式响应

## 3. 查询任务(免费)

### 3.1 端点

- `GET /kling/v1/{action}/{action2}/{task_id}`

本技能固定使用：

- `action=videos`
- `action2=image2video`

即：

- `GET /kling/v1/videos/image2video/{task_id}`

### 3.2 Header

- `Accept: application/json`
- `Content-Type: application/json`
- `Authorization: Bearer <token>`

### 3.3 查询页示例

页面样例请求使用的是 `text2video`，但端点模板支持 `image2video`。本技能必须固定为 `image2video`，不得把 `text2video` 示例直接复制为 `kling` 图生视频技能的真源。

查询响应示例：

```json
{
  "code": 0,
  "data": {
    "task_id": "CjMT7WdSwWcAAAAAALvB3g",
    "created_at": 1733851336696,
    "updated_at": 1733851344553,
    "task_result": {
      "images": [
        {
          "id": "",
          "url": "https://cdn.klingai.com/..."
        }
      ]
    },
    "task_status": "succeed",
    "task_status_msg": ""
  },
  "message": "SUCCEED",
  "request_id": "CjNTkGdSwxYAAAAAALud5A"
}
```

### 3.4 查询页现实含义

- 查询页示例里的 `task_result.images` 明显来自图片类任务或通用模板
- 对 `image2video` 来说，更可能返回：
  - `task_result.videos`
  - 或等价的视频 URL 字段
- 因此脚本必须：
  - 保留 `raw_response`
  - 先尝试常见视频路径
  - 再回退到其他媒体路径

## 4. 推荐脚本策略

### 4.1 创建

- 创建端点按 JSON 提交
- 本地图自动转裸 Base64
- 远程 URL 保持原样

### 4.2 查询

- 以 `task_status` 为主状态字段
- `code != 0` 时，即使 HTTP 200 也要按失败处理

### 4.3 下载

没有独立 `/content` 页时，下载来自查询结果里的资产 URL：

- 优先尝试：
  - `data.task_result.videos[0].url`
- 回退尝试：
  - `data.task_result.video.url`
  - `data.task_result.assets[0].url`
  - `data.task_result.images[0].url`

## 5. 环境变量建议

```dotenv
ANYFAST_PLATFORM_URL=https://www.anyfas.ai
ANYFAST_DOCS_URL=https://docs.anyfast.ai
ANYFAST_API_BASE_URL=https://fw2afus.ent.acc.kurtisasia.com
ANYFAST_VIDEO_API_KEY=...
ANYFAST_API_KEY=...

FINEAPI_API_BASE_URL=...
FINEAPI_API_KEY=...

KLING_API_BASE_URL=...
KLING_API_KEY=...
```

优先级建议：

- API Key：`ANYFAST_VIDEO_API_KEY` -> `KLING_API_KEY` -> `FINEAPI_KLING_API_KEY` -> `ANYFAST_API_KEY` -> `FINEAPI_API_KEY`
- Base URL：`ANYFAST_API_BASE_URL` -> `KLING_API_BASE_URL` -> `FINEAPI_KLING_API_BASE_URL` -> `FINEAPI_API_BASE_URL`

## 6. 推荐验证顺序

1. `submit --dry-run --print-payload`
2. `submit` 拿到 `task_id`
3. `status` 看真实 `task_status`
4. 状态成功后再 `download`
5. 成熟后再用 `run` 串联整个闭环

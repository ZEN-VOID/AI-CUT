# FineAPI Veo API 摘要

更新时间：`2026-04-17`

## 1. 当前可确认真源

- 用户提供的文生视频接口字段说明
- 用户提供的图生视频接口字段说明
- 用户提供的请求示例与响应示例

说明：

- 当前轮输入稳定确认的是创建接口 `POST /v1/video/create`。
- 旧版 `/v1/videos`、`input_reference` multipart、状态查询与下载链路不再视为本轮校正的当前真源。
- 本技能本地默认模型另有覆写：按允许列表自动选择最高版本的通用模型，不直接沿用页面示例值；截至 2026-04-17 本地解析结果为 `veo3.1-pro`。
- 2026-04-17 本地 live probe 补充结论：
  - 当前 `.env` 的 `ANYFAST_API_BASE_URL` 上，`POST /v1/video/create` 返回 `404 Invalid URL`
  - 同一 host 上，`POST /v1/video/generations` 会进入鉴权/额度校验，说明这是当前环境的有效视频创建路径
  - 因此脚本默认采用 `submit_path=auto`：先试 `/v1/video/create`，若收到 `Invalid URL` 再回退 `/v1/video/generations`

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

文生示例：

```json
{
  "enable_upsample": true,
  "enhance_prompt": true,
  "model": "veo3.1-fast",
  "prompt": "make animate",
  "aspect_ratio": "16:9"
}
```

图生示例：

```json
{
  "prompt": "牛飞上天了",
  "model": "veo3-fast-frames",
  "images": [
    "https://filesystem.site/cdn/20250612/VfgB5ubjInVt8sG6rzMppxnu7gEfde.png",
    "https://filesystem.site/cdn/20250612/998IGmUiM2koBGZM3UnZeImbPBNIUL.png"
  ],
  "enhance_prompt": true,
  "enable_upsample": true,
  "aspect_ratio": "16:9"
}
```

### 2.4 字段说明

| 字段 | 类型 | 必填 | 已确认说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | 当前材料出现 Veo 2 / Veo 3 / Veo 3.1 多个家族枚举 |
| `prompt` | string | 是 | 提示词 |
| `enable_upsample` | boolean | 文档有漂移 | 文生页写可选；图生页写必填 |
| `enhance_prompt` | boolean | 文档有漂移 | 文生页写可选；图生页写必填；用于中文 prompt 自动转英文 |
| `images` | array[string] | 可选 | 图生时使用；当前只确认 URL 字符串数组，不确认本地文件上传 |
| `aspect_ratio` | string | 文档有漂移 | 文生页写可选，图生页写必填；仅 `veo3*` 支持，值为 `16:9 / 9:16` |

### 2.5 已确认模型集合

以下模型值在当前材料中明确出现：

- `veo2`
- `veo2-fast`
- `veo2-fast-frames`
- `veo2-fast-components`
- `veo2-pro`
- `veo2-pro-components`
- `veo3`
- `veo3-fast`
- `veo3-fast-frames`
- `veo3-frames`
- `veo3-pro`
- `veo3-pro-frames`
- `veo3.1`
- `veo3.1-fast`
- `veo3.1-pro`

### 2.6 图片数量约束

当前材料只对部分模型给出明确约束：

- `veo2-fast-frames`：最多 2 张，分别为首尾帧
- `veo3-pro-frames`：最多 1 张首帧
- `veo2-fast-components`：最多 3 张元素图

另外，图生示例显示：

- `veo3-fast-frames` 可传 2 张图

因此脚本层应：

- 对明确给出上限的模型做硬校验
- 对仅样例出现的 `veo3-fast-frames` 按样例兼容，并保留漂移提示
- 不擅自为未确认模型编造更细的图片数量规则

## 3. 创建响应

当前材料存在两套响应示例。

### 3.1 简洁回执

```json
{
  "id": "string",
  "status": "string",
  "status_update_time": 0,
  "enhanced_prompt": "string"
}
```

### 3.2 OpenAI 风格包裹

```json
{
  "id": "string",
  "object": "string",
  "created": 0,
  "choices": [],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```

### 3.3 脚本策略

- 保留 `raw_response`
- 同时抽取最小规范化字段：
  - `id`
  - `status`
  - `status_update_time`
  - `enhanced_prompt`
  - `object`
  - `created`
  - `usage`

## 4. 当前未锁定的部分

以下内容当前没有新的稳定文档支撑，因此不得继续写成当前真源：

- `GET /v1/videos/{id}`
- `GET /v1/videos/{id}/content`
- `input_reference` multipart 上传
- 旧的 `veo_3_1 / veo_3_1-fast` 下划线模型命名
- API 默认 host
- 失败响应固定 schema

## 5. 环境变量建议

建议在根目录 `.env` 使用以下分层：

```dotenv
FINEAPI_API_BASE_URL=
FINEAPI_API_KEY=

VEO_API_BASE_URL=
VEO_API_KEY=

ANYFAST_API_BASE_URL=
ANYFAST_VIDEO_API_KEY=
ANYFAST_API_KEY=
```

优先级建议：

- Key：`VEO_API_KEY` -> `ANYFAST_VIDEO_API_KEY` -> `ANYFAST_API_KEY` -> `FINEAPI_API_KEY`
- Base URL：`VEO_API_BASE_URL` -> `ANYFAST_API_BASE_URL` -> `FINEAPI_API_BASE_URL`

## 6. 本技能默认模型覆写

- 覆写目标：让本地默认值总是自动前移到当前允许列表中的最高版本通用模型。
- 解析规则：
  - 先按 `major.minor` 比较版本号
  - 再在同版本内按 `pro > 基础版 > fast`
  - `frames / components` 变体不参与默认值竞争，因为它们依赖图片输入
- 截至 2026-04-17，本地白名单解析结果为：`veo3.1-pro`

## 7. 当前环境端点分流

- 显式 Veo/FineAPI host：
  - 优先路径：`POST /v1/video/create`
- AnyFast 回退 host：
  - 若 `/v1/video/create` 返回 `Invalid URL`，回退：`POST /v1/video/generations`
- 不再把 `POST /v1/videos` 当作本技能的默认真源；它虽然在某些聚合网关上存在，但当前 Veo 技能不以它为主路径

## 8. 推荐验证顺序

1. 先跑 `submit --dry-run --print-payload`
2. 再用 `submit_path=auto` 验证默认路径与回退路径
3. 再用文生示例验证无图 JSON
4. 再用图生示例验证 `images[]` JSON
5. 若需要补状态/下载闭环，先拿到新文档再扩展脚本

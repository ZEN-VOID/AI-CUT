# Vidu Video Generations API 摘要

更新时间：`2026-04-17`

## 1. 当前可确认真源

- 文档页：`https://docs.fineapi.cloud/403045611e0`
- 用户提供的 4 张接口截图
- 用户明确要求：
  - 默认模型总是调整为最高版本
  - 统一引用 `.env` 中的 `ANYFAST_VIDEO_API_KEY`
- 官方补充真源：
  - `https://platform.vidu.com/docs/pricing`
  - `https://platform.vidu.com/docs/model-map`

说明：

- 该文档页在当前环境下主要是前端渲染页面，终端直接抓取只能拿到页面壳。
- 因此本文件只沉淀本轮已稳定确认的**创建接口**事实；查询状态与下载结果端点不写成真源。

## 2. 创建任务

### 2.1 端点

- `POST /v1/video/generations`

### 2.2 请求头

```http
Accept: application/json
Content-Type: application/json
Authorization: Bearer <token>
```

### 2.3 Body 字段

| 字段 | 类型 | 必填 | 已确认说明 |
| --- | --- | --- | --- |
| `Model` | string | 否 | 文档展示支持多个模型；本技能默认由脚本自动裁决当前最高通用 Vidu 型号，当前为 `Vidu-q3-pro` |
| `SceneType` | string | 否 | 场景类型 |
| `Prompt` | string | 否 | 正向提示词；与 `ImageUrl / ImageInfos` 至少填一项 |
| `NegativePrompt` | string | 否 | 负向提示词 |
| `EnhancePrompt` | boolean | 否 | 是否开启提示词增强 |
| `ImageUrl` | string | 否 | 参考图 URL；可用于图生视频 / 首帧图 |
| `ImageInfos` | array[object] | 否 | 多图参考列表；与 `Prompt / ImageUrl` 至少填一项 |
| `ImageInfos[].ImageUrl` | string | 否 | 图片 URL |
| `ImageInfos[].ReferenceType` | string | 否 | 截图标注：`asset / style`，且“仅 GV 模型支持” |
| `LastImageUrl` | string | 否 | 尾帧图 URL |
| `Duration` | integer | 否 | 视频时长（秒）；截图示例为 `5` |
| `AdditionalParameters` | string | 否 | 附加参数，JSON 字符串格式 |
| `Operator` | string | 否 | 操作者标识 |
| `StoreCosParam` | object | 否 | 腾讯云 COS 存储参数 |
| `StoreCosParam.CosBucketName` | string | 否 | COS Bucket 名称 |
| `StoreCosParam.CosBucketRegion` | string | 否 | COS Bucket 地域 |
| `StoreCosParam.CosBucketPath` | string | 否 | COS 存储路径 |
| `ExtraParameters` | object | 否 | 扩展参数 |
| `ExtraParameters.Resolution` | string | 否 | `720P / 768P / 1080P` |
| `ExtraParameters.AspectRatio` | string | 否 | `16:9 / 9:16 / 1:1 / 4:3 / 3:4` |
| `ExtraParameters.LogoAdd` | integer | 否 | `0 / 1` |
| `ExtraParameters.EnableAudio` | boolean | 否 | 是否生成音频 |
| `ExtraParameters.OffPeak` | boolean | 否 | 截图标注：仅 Vidu 支持 |

## 3. 模型列表

当前可确认：

- 官方 Vidu 文档已公开：
  - `Vidu-q3-pro`
  - `Vidu-q3-turbo`
  - `Vidu-q3-mix`
- 当前网关与截图中已见：

- `Hunyuan`
- `Hailuo-02`
- `Hailuo-2.3`
- `Kling-2.0`
- `Kling-2.1`
- `Kling-2.5`
- `Kling-2.6`
- `Kling-01`
- `Vidu-q3-pro`
- `Vidu-q3-turbo`
- `Vidu-q3-mix`
- `Vidu-q2`
- `Vidu-q2-pro-fast`
- `Vidu-q2-pro`
- `Vidu-q2-turbo`
- `OS-2.0`
- `GV-3.1`

本技能默认值改为脚本自动裁决，当前解析结果为：

```text
Vidu-q3-pro
```

## 4. 模型边界备注

### 4.1 `ReferenceType`

- 截图标注：`ReferenceType` “仅 GV 模型支持”
- 本技能处理原则：
  - 不直接硬拒
  - 但在非 `GV-*` 模型上写 `validation_notes`

### 4.2 `AspectRatio`

- 截图标注：
  - Vidu 支持：`16:9 / 9:16 / 4:3 / 3:4 / 1:1`
  - 且 `4:3 / 3:4` 仅 `q2` 支持
- 本技能处理原则：
  - 若模型非 `Vidu-q2*` 且 ratio 为 `4:3 / 3:4`
  - 不直接硬拒，但写风险提示

### 4.3 `Resolution`

- 截图标注：
  - Kling / Vidu / GV 默认 `720P`
  - Hailuo 默认 `768P`
  - OS 仅支持 `720P`（且图片模式不可指定）
- 本技能处理原则：
  - 不对未证实组合做本地硬拒
  - 仅保留提示

### 4.4 `OffPeak`

- 截图标注：仅 Vidu 支持
- 本技能处理原则：
  - 非 `Vidu-*` 模型上写提示

## 5. 创建响应

截图当前可见成功回执字段：

```json
{
  "id": "string",
  "task_id": "string",
  "model": "string",
  "status": "queued | processing | succeeded | failed",
  "created_at": 1761622232
}
```

### 5.1 已确认字段

| 字段 | 说明 |
| --- | --- |
| `id` | 任务 ID |
| `task_id` | 任务 ID（同 id） |
| `model` | 使用的模型名 |
| `status` | 截图展示状态枚举：`queued / processing / succeeded / failed` |
| `created_at` | Unix 时间戳 |

## 6. 当前未锁定的部分

以下内容本轮没有拿到稳定文档，因此不得写死到脚本或主合同里：

- 查询状态端点
- 下载视频端点
- 失败响应的固定 schema
- 成功后的下载 URL 字段

## 7. 环境变量建议

建议在根目录 `.env` 使用以下分层：

```dotenv
ANYFAST_API_BASE_URL=...
ANYFAST_VIDEO_API_KEY=...
ANYFAST_API_KEY=...

VIDU_API_BASE_URL=...
VIDU_API_KEY=...

FINEAPI_API_BASE_URL=...
FINEAPI_API_KEY=...
```

优先级建议：

- Key：`ANYFAST_VIDEO_API_KEY -> VIDU_API_KEY -> ANYFAST_API_KEY -> FINEAPI_API_KEY`
- Base URL：`VIDU_API_BASE_URL -> ANYFAST_API_BASE_URL -> FINEAPI_API_BASE_URL -> https://fw2afus.ent.acc.kurtisasia.com`

## 8. 推荐验证顺序

1. 先跑 `submit --dry-run --print-payload`
2. 确认 `.env` 中 `ANYFAST_VIDEO_API_KEY` 已生效
3. 再验证最小文生视频请求
4. 然后验证单图 / 首尾帧 / 多图参考
5. 若要补状态与下载闭环，先取得对应文档页，再扩展脚本

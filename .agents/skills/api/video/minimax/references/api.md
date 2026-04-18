# MiniMax Hailuo Video Generations API 摘要

更新时间：`2026-04-17`

## 1. 当前可确认真源

- 文档页：`https://docs.fineapi.cloud/403045611e0`
- 用户提供的接口截图（请求头、Body 字段、ExtraParameters、成功回执）
- 用户明确要求：
  - 默认模型：治理规则统一回指 `../../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族，当前解析结果为 `Hailuo-2.3`
  - 统一引用 `.env` 中的 `ANYFAST_VIDEO_API_KEY`

说明：

- 该文档页在当前环境下主要是前端渲染页面，终端直接抓取只能稳定拿到页面壳。
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
| `Model` | string | 否 | 文档展示支持多个模型；默认模型治理统一回指 `../../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族，当前解析结果为 `Hailuo-2.3` |
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

截图当前可见：

- `Hunyuan`
- `Hailuo-02`
- `Hailuo-2.3`
- `Kling-2.0`
- `Kling-2.1`
- `Kling-2.5`
- `Kling-2.6`
- `Kling-01`
- `Vidu-q2`
- `Vidu-q2-pro`
- `Vidu-q2-turbo`
- `OS-2.0`
- `GV-3.1`

本技能默认值按父级共享 runbook 的 `highest-available-general` 规则族自动推导，当前解析为：

```text
Hailuo-2.3
```

## 4. 海螺与跨模型边界备注

### 4.1 `Resolution`

- 截图标注：
  - Kling / Vidu / GV 默认 `720P`
  - Hailuo 默认 `768P`
  - OS 仅支持 `720P`
- 本技能处理原则：
  - 海螺默认值明确写为 `768P`
  - 若用户显式传其他分辨率，不在本地硬拒，但保留说明与 dry-run 可见性

### 4.2 `AspectRatio`

- 截图标注：
  - Kling 文生视频支持 `16:9 / 9:16 / 1:1`
  - Vidu 支持 `16:9 / 9:16 / 4:3 / 3:4 / 1:1`
  - GV / OS 支持 `16:9 / 9:16`
  - Hailuo 暂不支持
- 本技能处理原则：
  - 默认海螺模型上若传 `AspectRatio`，写入 validation note
  - 不直接硬拒，以免代理网关存在兼容扩展

### 4.3 `LogoAdd`

- 截图标注：Hailuo / Kling / Vidu 支持
- 本技能处理原则：
  - 允许在海螺模型上使用
  - 取值仅 `0 / 1`

### 4.4 `ReferenceType`

- 截图标注：仅 GV 模型支持
- 本技能处理原则：
  - 在非 `GV-*` 模型上不直接硬拒
  - 但在报告中写风险提示

### 4.5 `OffPeak`

- 截图标注：仅 Vidu 支持
- 本技能处理原则：
  - 海螺模型上保留提交能力
  - 但明确写 warning

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

MINIMAX_API_BASE_URL=...

FINEAPI_API_BASE_URL=...
FINEAPI_API_KEY=...
```

优先级建议：

- Key：`ANYFAST_VIDEO_API_KEY -> ANYFAST_API_KEY -> FINEAPI_API_KEY`
- Base URL：`MINIMAX_API_BASE_URL -> ANYFAST_API_BASE_URL -> FINEAPI_API_BASE_URL -> https://fw2afus.ent.acc.kurtisasia.com`

## 8. 推荐验证顺序

1. 先跑 `submit --dry-run --print-payload`
2. 确认 `.env` 中 `ANYFAST_VIDEO_API_KEY` 已生效
3. 再验证最小文生视频请求
4. 然后验证单图 / 首尾帧 / 多图参考
5. 若默认海螺模型提交失败且传了 `AspectRatio`，先去掉该字段再重试
6. 若要补状态与下载闭环，先取得对应文档页，再扩展脚本

# Seedance Video Generations API 摘要

更新时间：`2026-04-17`

## 1. 当前可确认真源

- AnyFast 官方 `Seedance 2.0`
- AnyFast 官方 `Seedance 2.0 Fast`
- AnyFast 官方 `Seedance 任务查询`
- 用户明确要求：统一引用根目录 `.env` 中的 `ANYFAST_VIDEO_API_KEY`

说明：

- 本文件只沉淀当前稳定确认的信息，不把未证实字段伪装成真源。
- `seedance` / `seedance-fast` 在 AnyFast 当前文档中是滚动别名：
  - `seedance` = 当前最新质量优先档（`Seedance 2.0`）
  - `seedance-fast` = 当前最新速度优先档（`Seedance 2.0 Fast`）
  - 默认模型治理统一回指 `../../runbooks/default-model-policy.md` 的 `rolling-latest-quality-alias` 规则族

## 2. 创建任务

### 2.1 端点

- `POST https://fw2afus.ent.acc.kurtisasia.com/v1/video/generations`

### 2.2 请求头

```http
Accept: application/json
Content-Type: application/json
Authorization: Bearer <token>
```

### 2.3 请求体主字段

| 字段 | 类型 | 必填 | 已确认说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | `seedance`（最新质量优先）或 `seedance-fast`（最新速度优先） |
| `content` | array[object] | 是 | 输入内容数组，承载文本/图片/视频/音频 |
| `generate_audio` | boolean | 否 | `seedance` 默认 `true` |
| `tools` | array[object] | 否 | 当前仅见 `web_search` |
| `resolution` | string | 否 | `480p / 720p`，默认 `720p` |
| `ratio` | string | 否 | `16:9 / 4:3 / 1:1 / 3:4 / 9:16 / 21:9 / adaptive` |
| `duration` | integer | 否 | `4-15` 的整数，或 `-1` |
| `watermark` | boolean | 否 | 出现在用户示例中 |

## 3. `content[]` 输入类型

### 3.1 文本

```json
{
  "type": "text",
  "text": "输入给模型的提示词"
}
```

### 3.2 图片

```json
{
  "type": "image_url",
  "image_url": {
    "url": "https://example.com/ref.jpg"
  },
  "role": "first_frame"
}
```

已确认：

- `url` 可为公网 URL、Data URL、`asset://<ASSET_ID>`
- 图片单张格式支持：`jpeg/png/webp/bmp/tiff/gif`
- 图片数量规则：
  - 首帧：1 张
  - 首尾帧：2 张
  - 多模态参考图：最多 9 张

### 3.3 视频

```json
{
  "type": "video_url",
  "video_url": {
    "url": "https://example.com/ref.mp4"
  },
  "role": "reference_video"
}
```

已确认：

- 支持 URL 或 `asset://<ASSET_ID>`
- 最多 3 个参考视频
- 单个视频时长 `[2,15]s`

### 3.4 音频

```json
{
  "type": "audio_url",
  "audio_url": {
    "url": "https://example.com/ref.mp3"
  },
  "role": "reference_audio"
}
```

已确认：

- 支持 URL、Data URL、`asset://<ASSET_ID>`
- 最多 3 段参考音频
- 单个音频时长 `[2,15]s`
- 音频不能单独输入，至少要伴随 1 个图片或视频参考

## 4. 场景互斥规则

### 4.1 首帧图生视频

- `content` 中有 1 个 `image_url`
- `role` 为 `first_frame` 或不填
- 不得混用 `reference_image/reference_video/reference_audio`

### 4.2 首尾帧图生视频

- `content` 中有 2 个 `image_url`
- 第一张 `role=first_frame`
- 第二张 `role=last_frame`
- 不得混用参考图/视频/音频

### 4.3 多模态参考生视频

- 图片角色统一 `reference_image`
- 视频角色统一 `reference_video`
- 音频角色统一 `reference_audio`
- 可以是以下任意组合：
  - 文本
  - 文本 + 图片
  - 文本 + 视频
  - 文本 + 图片 + 音频
  - 文本 + 图片 + 视频
  - 文本 + 视频 + 音频
  - 文本 + 图片 + 视频 + 音频

### 4.4 联网搜索增强

- 仅支持文本生视频
- 请求体中出现：

```json
"tools": [
  {
    "type": "web_search"
  }
]
```

## 5. 查询任务

### 5.1 端点

- `GET https://fw2afus.ent.acc.kurtisasia.com/v1/video/generations/{id}`

### 5.2 处理中样例

```json
{
  "code": "success",
  "message": "",
  "data": {
    "task_id": "cgt-20260312231129-7db6s",
    "action": "omniGenerate",
    "status": "QUEUED",
    "fail_reason": "",
    "submit_time": 1773328294,
    "start_time": 0,
    "finish_time": 0,
    "progress": "10%",
    "data": {
      "created_at": 1773328294,
      "draft": false,
      "execution_expires_after": 172800,
      "generate_audio": true,
      "id": "cgt-20260312231129-7db6s",
      "model": "seedance",
      "service_tier": "default",
      "status": "queued",
      "updated_at": 1773328294
    }
  }
}
```

### 5.3 成功样例

```json
{
  "code": "success",
  "message": "",
  "data": {
    "task_id": "cgt-20260312203514-k9lcj",
    "action": "omniGenerate",
    "status": "SUCCESS",
    "fail_reason": "https://xxx.com/video.mp4",
    "submit_time": 1773318919,
    "start_time": 1773318925,
    "finish_time": 1773319107,
    "progress": "100%",
    "data": {
      "content": {
        "video_url": "https://xxx.com/video.mp4"
      },
      "created_at": 1773318919,
      "draft": false,
      "duration": 8,
      "execution_expires_after": 172800,
      "framespersecond": 24,
      "generate_audio": true,
      "id": "cgt-20260312203514-k9lcj",
      "model": "seedance",
      "ratio": "16:9",
      "resolution": "720p",
      "seed": 56607,
      "service_tier": "default",
      "status": "succeeded",
      "updated_at": 1773319103,
      "usage": {
        "completion_tokens": 281700,
        "total_tokens": 281700
      }
    }
  }
}
```

## 6. 当前模型别名治理

### 6.1 质量优先默认值

- AnyFast 官方 `Seedance 2.0` 页面当前只公开 `model=seedance`
- 因此本技能默认值固定为 `seedance`
- 该默认值的语义不是“某个旧常量”，而是父级共享 runbook 定义的“当前最新质量优先版本”

### 6.2 速度优先可选值

- AnyFast 官方 `Seedance 2.0 Fast` 指南当前公开 `model=seedance-fast`
- 该值用于低时延/低成本试跑
- 当用户明确要求最高版本或最佳质量时，不应把默认值切到 `seedance-fast`

### 6.3 技能侧治理策略

- 默认模型保持 `seedance`
- 允许显式切到 `seedance-fast`
- 若未来官方继续升级 2.x/3.x，只要 AnyFast 维持别名语义，本技能无需改成长模型号即可继续跟随最新版本

## 7. 环境变量建议

建议根目录 `.env` 至少包含：

```dotenv
ANYFAST_PLATFORM_URL=https://www.anyfas.ai
ANYFAST_DOCS_URL=https://docs.anyfast.ai
ANYFAST_VIDEO_API_KEY=...
ANYFAST_API_BASE_URL=https://fw2afus.ent.acc.kurtisasia.com

SEEDANCE_API_BASE_URL=
SEEDANCE_API_KEY=

ANYFAST_API_KEY=
FINEAPI_API_KEY=
FINEAPI_API_BASE_URL=
```

优先级建议：

- Key：`ANYFAST_VIDEO_API_KEY -> SEEDANCE_API_KEY -> ANYFAST_API_KEY -> FINEAPI_API_KEY`
- Base URL：`SEEDANCE_API_BASE_URL -> ANYFAST_API_BASE_URL -> FINEAPI_API_BASE_URL -> https://fw2afus.ent.acc.kurtisasia.com`

## 8. 推荐验证顺序

1. 先跑 `submit --dry-run --print-payload`
2. 先验证纯文本生视频
3. 再验证首帧 / 首尾帧
4. 再验证 `mode=multimodal`
5. 最后再测 `seedance-fast` 的速度优先路径

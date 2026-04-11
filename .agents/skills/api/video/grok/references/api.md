# GROK Video API Reference

## Source of Truth

本参考来自两类本地证据，二者都必须保留：

1. `PRPs/grok.md` 的 OpenAPI 文字版
2. `PRPs/image/grok/*.png` 的截图示例

结论：当前能确认的是“同一业务能力存在两种提交形态”，而不是其中一份一定过时。

## Observed Endpoints

### Variant A: JSON submit

- Source:
  - `PRPs/image/grok/1775202638719.png`
  - `PRPs/image/grok/1775202655941.png`
  - `PRPs/image/grok/1775202663454.png`
  - `PRPs/image/grok/1775202675162.png`
- Method: `POST`
- Path: `/v1/video/create`
- Content-Type: `application/json`
- Body shape:

```json
{
  "model": "grok-video-3",
  "prompt": "cat fish --mode=custom",
  "images": [
    "data:image/png;base64,..."
  ],
  "aspect_ratio": "3:2",
  "size": "1080P",
  "duration": 6
}
```

- Notes:
  - 截图明确展示 `images` 为字符串数组，内容是 `data:image/...;base64,...`
  - 更适合多图与“图片读取 -> 统一编码”流程
  - 返回示例出现 `task_id`

### Variant B: multipart submit

- Source: `PRPs/grok.md`
- Method: `POST`
- Path: `/v1/videos`
- Content-Type: `multipart/form-data`
- Fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `model` | string | yes | 示例 `grok-video-3` |
| `prompt` | string | yes | 提示词 |
| `input_reference` | binary | no | 单个参考图 |
| `aspect_ratio` | string | no | `16:9` `9:16` `2:3` `3:2` `1:1` |
| `size` | string | no | `720P` or `1080P` |
| `seconds` | integer | no | 默认 10，支持 6/10/15 |

- Notes:
  - 文字版只给了单个 `input_reference`
  - 与截图版 `images[]` 多图模式不同

## Response Drift

截图与 OpenAPI 文本里的返回字段存在轻微漂移：

| Observed field | Meaning | Normalized field |
| --- | --- | --- |
| `task_id` | 任务 ID | `task_id` |
| `id` | 任务 ID | `task_id` |
| `status` | `processing` `failed` `completed` | `status` |
| `status_update_time` | 状态更新时间 | `status_update_time` |
| `created_at` | 任务创建时间 | `created_at` |

技能脚本必须做字段归一化，不得把 `id` / `task_id` 分歧直接甩给上游。

## Request Mode Decision

默认决策：

1. 若 `request-mode=auto`，优先走 `json`
2. 若传入多图，必须走 `json`
3. 若显式要求 `multipart` 或需要严格对齐 OpenAPI 文本版，则走 `multipart`

## Current Known Gaps

- 未提供公开的查询/下载端点
- 未提供最终视频文件字段
- 未确认 JSON 模式下 `seconds` 是否也被服务端接受，因此技能内部使用：
  - JSON 提交时发送 `duration`
  - multipart 提交时发送 `seconds`
  - 对外统一抽象为 `seconds`

## Safe Contract for This Skill

- 保证：
  - 可以提交任务
  - 可以读本地/远程/data URL 图片
  - 可以归一化回执
  - 可以生成项目化提交报告
- 不保证：
  - 查询任务完成状态
  - 下载最终 MP4
  - 推断未在 PRP 中出现的额外接口

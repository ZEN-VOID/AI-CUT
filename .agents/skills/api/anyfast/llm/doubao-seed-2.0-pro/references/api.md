# 豆包 Seed 2.0 Pro API 参考

## 1. 官方来源

- 模型指南：
  - `https://docs.anyfast.ai/zh/guides/model-api/bytedance/doubao-seed-2.0-pro`
- 模型 API 参考：
  - `https://docs.anyfast.ai/zh/api-reference/model-api/bytedance/doubao-seed-2.0-pro`
- 豆包兼容端点：
  - `https://docs.anyfast.ai/zh/guides/endpoints/doubao`
- 文档索引：
  - `https://docs.anyfast.ai/llms.txt`

## 2. 接口地址

- Chat Completions：
  - `POST https://www.anyfast.ai/v1/chat/completions`

若仓库根 `.env` 使用 base URL 方式，脚本应自动补全为 `/v1/chat/completions`。

## 3. 认证

- Header：
  - `Authorization: Bearer <API_KEY>`
- 建议环境变量：
  - `ANYFAST_DOUBAO_SEED_2_0_PRO_API_KEY`
  - `ANYFAST_API_KEY`（专用 key 缺失时回退）

AnyFast Quickstart 还提示：模型映射到对应 channel，调用前需在控制台启用相应 channel。

## 4. 模型定位

- 模型名：
  - `doubao-seed-2.0-pro`
- 官方定位：
  - 字节跳动 Seed 2.0 Pro 旗舰模型
  - 推理能力最强
  - 支持流式输出

## 5. 核心请求字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `model` | string | 固定为 `doubao-seed-2.0-pro` |
| `messages` | array | 对话消息数组；每条消息包含 `role` 与 `content` |
| `max_tokens` | integer | 最大生成 token，`>= 1` |
| `temperature` | number | `0..2`，默认 `1` |
| `top_p` | number | `0..1`，默认 `1` |
| `frequency_penalty` | number | 官方模型页示例中支持，默认 `0` |
| `presence_penalty` | number | 官方模型页示例中支持，默认 `0` |
| `stream` | boolean | 是否启用 SSE，默认 `false` |
| `stop` | string[] | 最多 4 条停止序列 |

## 6. messages 结构

最简单的文本消息可直接写字符串：

```json
[
  {
    "role": "user",
    "content": "你好！"
  }
]
```

兼容端点文档还说明，`content` 也可以是多模态数组，元素类型包括：

- `text`
- `image_url`
- `video_url`

因此本 skill 默认支持：

- 简单文本：由 `prompt/system` 组装
- 高级或多模态输入：通过 `messages_json/messages_file/input_json.messages` 直传

## 7. 官方示例

### 7.1 cURL

```bash
curl https://www.anyfast.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seed-2.0-pro",
    "messages": [
      { "role": "user", "content": "用简单的话解释量子纠缠。" }
    ]
  }'
```

### 7.2 Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://www.anyfast.ai/v1",
)

response = client.chat.completions.create(
    model="doubao-seed-2.0-pro",
    messages=[
        {"role": "user", "content": "用简单的话解释量子纠缠。"}
    ],
)

print(response.choices[0].message.content)
```

### 7.3 流式输出

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://www.anyfast.ai/v1",
)

stream = client.chat.completions.create(
    model="doubao-seed-2.0-pro",
    messages=[
        {"role": "user", "content": "写一首关于大海的短诗。"}
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

## 8. CLI 与 API 字段映射

| CLI 参数 | API 字段 |
| --- | --- |
| `--prompt` + `--system` | `messages[]` |
| `--messages-json` / `--messages-file` | `messages` |
| `--model` | `model` |
| `--max-tokens` | `max_tokens` |
| `--temperature` | `temperature` |
| `--top-p` | `top_p` |
| `--frequency-penalty` | `frequency_penalty` |
| `--presence-penalty` | `presence_penalty` |
| `--stream` | `stream` |
| `--stop` | `stop[]` |
| `--extra-json` | 合并到请求体顶层 |

# DeepSeek API 参考

## 1. 官方来源

- 快速开始：
  - `https://api-docs.deepseek.com/zh-cn/`
- 思考模式：
  - `https://api-docs.deepseek.com/zh-cn/guides/thinking_mode`
- 对话补全：
  - `https://api-docs.deepseek.com/zh-cn/api/create-chat-completion`
- JSON Output：
  - `https://api-docs.deepseek.com/zh-cn/guides/json_mode`
- Tool Calls：
  - `https://api-docs.deepseek.com/zh-cn/guides/tool_calls`

## 2. 接口地址

- Chat Completions：
  - `POST https://api.deepseek.com/chat/completions`
- OpenAI SDK base URL：
  - `https://api.deepseek.com`
- Anthropic 兼容 base URL：
  - `https://api.deepseek.com/anthropic`

若仓库根 `.env` 使用 base URL 方式，脚本应自动补全为 `/chat/completions`。

## 3. 认证

- Header：
  - `Authorization: Bearer <DEEPSEEK_API_KEY>`
- 建议环境变量：
  - `DEEPSEEK_API_KEY`
  - `DEEPSEEK_BASE_URL`（可选）
  - `DEEPSEEK_API_BASE_URL`（可选）

## 4. 模型定位

- 固定模型：
  - `deepseek-v4-pro`
- 兼容别名：
  - `deepseek-chat`
  - `deepseek-reasoner`

本技能固定使用 `deepseek-v4-pro`。`deepseek-v4-flash` 与兼容别名不在本技能内调用。

## 5. 核心请求字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `model` | string | 固定 `deepseek-v4-pro` |
| `messages` | array | 对话消息数组；每条消息包含 `role` 与对应内容 |
| `thinking` | object | `{"type":"enabled"}` 或 `{"type":"disabled"}`，默认 enabled |
| `reasoning_effort` | string | 仅 thinking enabled 时发送；`high` 或 `max`；兼容输入 `low/medium/xhigh` 应本地映射 |
| `max_tokens` | integer | 最大生成 token，`>= 1` |
| `temperature` | number | `0..2`；思考模式下不生效 |
| `top_p` | number | `0..1`；思考模式下不生效 |
| `frequency_penalty` | number | `-2..2`；思考模式下不生效 |
| `presence_penalty` | number | `-2..2`；思考模式下不生效 |
| `response_format` | object | `{"type":"json_object"}` 启用 JSON Output |
| `stream` | boolean | 是否启用 SSE，默认 `false` |
| `stream_options.include_usage` | boolean | 流式最后一个额外块返回 usage |
| `stop` | string/string[] | 最多 16 条停止序列 |
| `tools` | array | function tool 定义，最多 128 个 |
| `tool_choice` | string/object | `none` / `auto` / `required` / 指定函数 |

## 6. messages 结构

最简单的文本消息：

```json
[
  {
    "role": "user",
    "content": "你好！"
  }
]
```

思考模式下的后续多轮工具调用，需要保留 assistant 消息中的 `reasoning_content` 与 `tool_calls`：

```json
{
  "role": "assistant",
  "content": "",
  "reasoning_content": "模型此前的思考内容",
  "tool_calls": [
    {
      "id": "call_...",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"location\":\"Hangzhou\"}"
      }
    }
  ]
}
```

## 7. 思考模式注意事项

- 默认启用思考模式。
- 普通请求默认 `reasoning_effort=high`。
- 复杂 Agent 类请求可能自动设置为 `max`。
- `low` / `medium` 兼容映射为 `high`；`xhigh` 兼容映射为 `max`。
- `thinking disabled` 时不要发送 `reasoning_effort`。
- 思考模式不支持 `temperature`、`top_p`、`presence_penalty`、`frequency_penalty` 的实际控制；设置这些参数通常不会报错，但不会生效。
- 非流式响应中，思考内容位于 `choices[0].message.reasoning_content`。
- 流式响应中，思考内容位于 `choices[].delta.reasoning_content`。

## 8. JSON Output 注意事项

启用 JSON Output 时：

1. 设置 `response_format={"type":"json_object"}`。
2. system 或 user prompt 中必须包含 `json` 字样。
3. prompt 中应给出希望输出的 JSON 格式或示例。
4. 合理设置 `max_tokens`，避免 JSON 被截断。
5. API 可能返回空 content，可尝试修改 prompt 缓解。

## 9. 官方示例

### 9.1 cURL

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
        "model": "deepseek-v4-pro",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
        ],
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "stream": false
      }'
```

### 9.2 Python SDK

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},
)

print(response.choices[0].message.content)
```

## 10. CLI 与 API 字段映射

| CLI 参数 | API 字段 |
| --- | --- |
| `--prompt` + `--system` | `messages[]` |
| `--messages-json` / `--messages-file` | `messages` |
| `--model` | `model` |
| `--thinking` | `thinking.type` |
| `--reasoning-effort` | `reasoning_effort` |
| `--max-tokens` | `max_tokens` |
| `--temperature` | `temperature` |
| `--top-p` | `top_p` |
| `--frequency-penalty` | `frequency_penalty` |
| `--presence-penalty` | `presence_penalty` |
| `--json-output` | `response_format={"type":"json_object"}` |
| `--stream` | `stream` |
| `--stream-include-usage` | `stream_options.include_usage` |
| `--stop` | `stop[]` |
| `--extra-json` | 合并到请求体顶层 |

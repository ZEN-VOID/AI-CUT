# types

本分区承载 DeepSeek provider skill 的类型策略。

当前类型：

- `text-chat`：普通 `prompt/system` 对话。
- `messages-passthrough`：结构化 `messages` 直传。
- `thinking-reasoning`：启用 thinking 与 reasoning effort。
- `json-output`：启用 `response_format={"type":"json_object"}`。
- `tool-calls`：通过 `extra_json` 或 messages 支持工具调用。

所有类型固定使用 `deepseek-v4-pro`。

---
name: deepseek
version: "v1.0"
governance_tier: full
description: "Use when calling DeepSeek-compatible chat completions for deterministic text tasks."
tools: [Read, Write, Edit, Bash]
color: blue
---

# DeepSeek API

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 作用范围

本技能是 DeepSeek 官方 API 的 repo-local provider skill，负责把任务整理为 OpenAI 兼容 `chat/completions` 请求，执行调用，并把文本结果、思考内容摘要、流式事件摘要和报告 JSON 落到可复盘目录。

- 官方文档：
  - `https://api-docs.deepseek.com/zh-cn/`
  - `https://api-docs.deepseek.com/zh-cn/guides/thinking_mode`
  - `https://api-docs.deepseek.com/zh-cn/api/create-chat-completion`
- 兼容端点：
  - `POST https://api.deepseek.com/chat/completions`
- 固定模型：
  - `deepseek-v4-pro`
- 默认脚本入口：
  - `python3 .agents/skills/api/deepseek/scripts/deepseek_chat.py ...`

职责边界：

- 本技能负责：
  - 普通文本对话
  - 结构化 `messages` 直传
  - 思考模式 `thinking` 与 `reasoning_effort` 参数处理
  - JSON Output / Tool Calls 等 OpenAI 兼容字段透传
  - 流式/非流式响应解析
  - 文本与报告落盘
- 本技能不负责：
  - 上游业务 prompt 模板设计
  - 项目主真源裁决
  - 多技能编排后的最终业务写回
  - 把 API key 写入可提交文件或日志

## 1.1 视觉流程

```mermaid
flowchart TD
    A["收集输入: prompt / messages / input_json"] --> B["解析 .env 与 CLI 默认值"]
    B --> C["构造 DeepSeek chat/completions payload"]
    C --> D{"dry-run?"}
    D -- "yes" --> E["打印/写出 payload 供检查"]
    D -- "no" --> F{"stream?"}
    F -- "yes" --> G["发起 SSE 请求并累积 delta"]
    F -- "no" --> H["发起普通 POST 请求"]
    G --> I["抽取 content / reasoning_content / usage"]
    H --> I
    I --> J["解析输出目录与文件名"]
    J --> K["写文本 sidecar 与 report JSON"]
    K --> L["向用户返回可复盘结果"]
```

## 1.2 分支与回退

```mermaid
flowchart TD
    A["输入来源"] --> B{"messages 已显式提供?"}
    B -- "yes" --> C["直接使用 messages_json / messages_file / input_json.messages"]
    B -- "no" --> D["由 system + prompt 组装基础 messages"]
    C --> E{"thinking enabled?"}
    D --> E
    E -- "yes" --> F["设置 thinking.enabled 与 reasoning_effort"]
    E -- "no" --> G["可使用采样参数 temperature / top_p / penalties"]
    F --> H{"stream?"}
    G --> H
    H -- "yes" --> I["SSE 解析 reasoning_content 与 content"]
    H -- "no" --> J["JSON 响应解析"]
```

## 2. 必需输入

- 二选一：
  - `prompt`
  - `messages`（通过 `--messages-json` / `--messages-file` / `--input-json` 提供）
- API Key：
  - 优先读取根目录 `.env` 中的 `DEEPSEEK_API_KEY`
  - 可显式传 `--api-key`

可选输入：

- `system`
- `model`（固定 `deepseek-v4-pro`，不支持覆盖）
- `thinking`（默认 `enabled`）
- `reasoning_effort`（默认 `high`；支持 `high` / `max`，兼容 `low` / `medium` / `xhigh` 映射）
- `max_tokens`
- `temperature`
- `top_p`
- `frequency_penalty`
- `presence_penalty`
- `response_format`
- `stream`
- `stop`
- `extra_json`
- `output_dir`
- `project_name`
- `task_kind`
- `filename_prefix`
- `text_output`
- `report_json`

## 3. 核心约束（Mandatory）

1. **模型默认锁定**
   - 固定模型必须是 `deepseek-v4-pro`。
   - 即使官方存在其它模型或兼容别名，本技能也不得静默切换。
   - 若用户明确要求其它 DeepSeek 模型，应先更新本技能合同或另建 provider skill，不得在当前技能内临时漂移。
2. **认证单一事实源**
   - 本技能专用密钥默认从根目录 `.env` 的 `DEEPSEEK_API_KEY` 读取。
   - 无密钥时必须硬退出，不得发出匿名请求。
   - 控制台、报告 JSON 与错误信息不得输出 Bearer token 或 `sk-...` 明文。
3. **端点解析优先级**
   - API URL 优先级：
     1. `--api-url`
     2. `.env` 的 `DEEPSEEK_BASE_URL`
     3. `.env` 的 `DEEPSEEK_API_BASE_URL`
     4. 官方默认 `https://api.deepseek.com`
   - 若拿到的是 base URL，脚本必须自动补全为 `/chat/completions`。
4. **输入收束契约**
   - 若显式提供 `messages`，不得再强制改写为 `prompt` 单字符串模式。
   - 若未提供 `messages`，必须由 `system + prompt` 生成最小合法消息数组。
   - 思考模式与工具调用多轮拼接时，必须保留 assistant 消息中的 `reasoning_content` / `tool_calls`，不得因 content 为空而丢弃合法 assistant 消息。
5. **思考模式参数**
   - 默认启用 `{"thinking": {"type": "enabled"}}`。
   - `thinking=enabled` 时默认 `reasoning_effort=high`；`xhigh` 映射为 `max`，`low` / `medium` 映射为 `high`。
   - `thinking=disabled` 时不得发送 `reasoning_effort`，否则 DeepSeek 会返回 `invalid_request_error`。
   - 思考模式下不要把 `temperature` / `top_p` / `presence_penalty` / `frequency_penalty` 当成有效控制项；如用户显式传入，应在报告中标记为兼容透传而非可靠调参。
6. **参数范围校验**
   - `temperature` 必须位于 `0..2`
   - `top_p` 必须位于 `0..1`
   - `frequency_penalty` / `presence_penalty` 必须位于 `-2..2`
   - `max_tokens >= 1`
   - `stop` 最多 `16` 条
7. **JSON Output**
   - 使用 JSON Output 时设置 `response_format={"type":"json_object"}`。
   - system 或 user prompt 中必须包含 `json` 字样，并提供目标 JSON 格式说明或示例。
   - 需要合理设置 `max_tokens`，避免 JSON 被截断。
8. **流式解析双轨兼容**
   - `stream=true` 时必须从 SSE `data:` 事件中累积 `choices[].delta.content` 与 `choices[].delta.reasoning_content`。
   - 若最终汇总为空，必须回退检查最终 payload 的 `choices[].message.content`。
9. **输出项目化**
   - 默认输出目录：`output/影片/[项目名]/5-API/llm/deepseek/`
   - 若未显式提供 `project_name`：
     - `task_kind=test` 使用 `测试`
     - `task_kind=temp` 使用 `临时`
     - 其他情况使用 `未命名项目`
10. **失败优先修源层**
    - 若出现认证错误、URL 拼装错误、思考参数漂移、SSE 解析失败、报告缺失或输出路径漂移，应优先修复：
      - `scripts/deepseek_chat.py`
      - 本 `SKILL.md`
    - 禁止只在单次调用里手工绕过而不修技能源层。

## 4. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-DS-01` | 输入解析结果：`prompt / system / messages / input_json` | 至少形成一组合法 `messages`；不得出现“既无 prompt 也无 messages”的空请求 | CLI 参数、结构化输入 | Step 1 | 输入完整度 | `FAIL-DS-INPUT` |
| `FIELD-DS-02` | 参数解析结果：`model / thinking / reasoning_effort / max_tokens / sampling / stop / stream` | 默认值清晰，范围合法，思考模式参数不误导 | CLI 参数、官方文档 | Step 2 | 参数合规性 | `FAIL-DS-PARAMS` |
| `FIELD-DS-03` | 请求体：`api_url / payload` | 必须符合 DeepSeek OpenAI 兼容 `chat/completions` 契约 | 官方文档、脚本构造结果 | Step 3 | 请求体合法性 | `FAIL-DS-PAYLOAD` |
| `FIELD-DS-04` | 执行结果：`stream_events / response_json / usage / content / reasoning_content` | 能稳定抽取文本、reasoning 与 usage 摘要；失败时报告应可复盘 | API 响应、SSE 事件流 | Step 4 | 解析稳定性 | `FAIL-DS-EXEC` |
| `FIELD-DS-05` | 输出产物：文本 sidecar、报告 JSON、输出目录 | 产物路径清晰、文件命名稳定、错误信息脱敏 | 落盘结果、报告文件 | Step 5 | 输出可追溯性 | `FAIL-DS-OUTPUT` |

## 5. 思维导引与执行流程（Mandatory）

### 5.1 固定步骤

1. **Step 1 / 输入收束**
   - 读取 `--prompt / --system / --messages-json / --messages-file / --input-json`
   - 若已有 `messages` 则直接保留
   - 否则用 `system + prompt` 构造最小消息数组
2. **Step 2 / 参数解析**
   - 解析 `model / thinking / reasoning_effort / max_tokens / temperature / top_p / penalties / stop / stream`
   - 从 `.env` 解析 `DEEPSEEK_API_KEY` 与 base URL
   - 做范围校验和 reasoning effort 兼容映射
3. **Step 3 / 请求体构造**
   - 构造 OpenAI 兼容 payload
   - 合并 `extra_json`
   - 支持 `--json-output`
   - 支持 `--dry-run --print-payload`
4. **Step 4 / 调用与响应处理**
   - 流式：解析 SSE，累积 `delta.content` 与 `delta.reasoning_content`
   - 非流式：直接读取 JSON body
   - 同时提取 `content / reasoning_content / finish_reason / usage`
5. **Step 5 / 落盘与汇报**
   - 解析输出目录
   - 视配置写文本 sidecar
   - 写 `deepseek_report_*.json`
   - 控制台输出主文本

### 5.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-DS-01` | 当前是简单 prompt，还是高级 messages 直传？ | 统一为合法 `messages[]` | `messages` 为空、角色缺失、关键 content 缺失 |
| `Step 2` | `FIELD-DS-02` | 思考模式、effort 和采样参数是否互相误导？ | 注入默认值并校验范围 | thinking 参数缺失、effort 非法、stop 超限 |
| `Step 3` | `FIELD-DS-03` | payload 是否贴合官方 chat/completions 契约？ | 构造并可选打印 payload | 字段名错误、base URL 未补全 |
| `Step 4` | `FIELD-DS-04` | 流式和非流式能否都稳定拿到文本与 reasoning？ | 解析响应并抽取 usage / finish_reason | SSE 累积为空、usage 丢失、响应报错 |
| `Step 5` | `FIELD-DS-05` | 结果是否可复盘且路径稳定？ | 写文本与报告，并输出主结果 | 无 report、无文本、路径漂移 |

## 6. 标准调用

### 6.1 最小文本调用

```bash
python3 .agents/skills/api/deepseek/scripts/deepseek_chat.py \
  --prompt "用简单的话解释量子纠缠。"
```

### 6.2 带 system 的高推理任务

```bash
python3 .agents/skills/api/deepseek/scripts/deepseek_chat.py \
  --system "你是一个严谨的中文研究助手。" \
  --prompt "请比较方案 A 和方案 B 的主要风险，并给出结论。" \
  --thinking enabled \
  --reasoning-effort high
```

### 6.3 流式输出

```bash
python3 .agents/skills/api/deepseek/scripts/deepseek_chat.py \
  --prompt "写一首关于大海的短诗。" \
  --stream
```

### 6.4 JSON Output

```bash
python3 .agents/skills/api/deepseek/scripts/deepseek_chat.py \
  --system "请输出 json，格式为 {\"summary\":\"...\",\"risks\":[\"...\"]}。" \
  --prompt "分析这个方案的主要风险。" \
  --json-output \
  --max-tokens 2048
```

### 6.5 结构化 messages 直传

```bash
python3 .agents/skills/api/deepseek/scripts/deepseek_chat.py \
  --messages-file /absolute/path/messages.json \
  --max-tokens 2048
```

### 6.6 Dry Run

```bash
python3 .agents/skills/api/deepseek/scripts/deepseek_chat.py \
  --prompt "测试 payload" \
  --dry-run --print-payload
```

## 7. 参数约定

| CLI 参数 | API 字段 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--model` | `model` | `deepseek-v4-pro` | 固定模型名；脚本会拒绝其它值 |
| `--prompt` + `--system` | `messages[]` | 无 | 简单文本输入 |
| `--messages-json` / `--messages-file` | `messages` | 无 | 高级消息直传 |
| `--thinking` | `thinking.type` | `enabled` | 思考模式开关 |
| `--reasoning-effort` | `reasoning_effort` | `high` | 仅 thinking enabled 时发送；`high` 或 `max`；兼容映射低档值 |
| `--max-tokens` | `max_tokens` | 无 | 最大生成 token |
| `--temperature` | `temperature` | 无 | 非思考模式下的采样温度 |
| `--top-p` | `top_p` | 无 | 非思考模式下的核采样阈值 |
| `--frequency-penalty` | `frequency_penalty` | 无 | 非思考模式下的频率惩罚 |
| `--presence-penalty` | `presence_penalty` | 无 | 非思考模式下的存在惩罚 |
| `--json-output` | `response_format` | 无 | 设置 `{"type":"json_object"}` |
| `--stream` | `stream` | `false` | 是否使用 SSE |
| `--stop` | `stop` | 无 | 最多 16 条停止序列 |
| `--extra-json` | 顶层合并 | 无 | 扩展参数透传 |

详细字段见 `references/api.md`。

## 8. 输出约定

- 默认输出目录：
  - `output/影片/[项目名]/5-API/llm/deepseek/`
- 默认产物：
  - `deepseek_YYYYmmdd_HHMMSS.txt`
  - `deepseek_report_YYYYmmdd_HHMMSS.json`
- 报告必须至少包含：
  - `ok`
  - `api_url`
  - `request_summary`
  - `compatibility_warnings`
  - `response_text`
  - `reasoning_content`
  - `usage`
  - `finish_reason`
  - `saved_files`
  - `error`

## 9. 参考资料

- 接口摘要：`.agents/skills/api/deepseek/references/api.md`
- 官方快速开始：`https://api-docs.deepseek.com/zh-cn/`
- 思考模式：`https://api-docs.deepseek.com/zh-cn/guides/thinking_mode`
- 对话补全 API：`https://api-docs.deepseek.com/zh-cn/api/create-chat-completion`
- JSON Output：`https://api-docs.deepseek.com/zh-cn/guides/json_mode`
- Tool Calls：`https://api-docs.deepseek.com/zh-cn/guides/tool_calls`

## 10. Root-Cause 执行契约（Mandatory）

当调用失败、参数异常或输出与预期不符时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：缺少密钥、URL 拼装错误、思考参数误用、messages 拼接错误、SSE 解析失败、文本 sidecar 或 report 缺失
-> `规则源`：`.agents/skills/api/deepseek/SKILL.md` 与 `scripts/deepseek_chat.py`
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的 Root-Cause First / CONTEXT / 技能治理基线
-> `Fix Landing Points`：优先修脚本的输入收束、URL 组装、思考模式参数、流式解析、报告落盘和本技能说明，再修局部样例

用户侧关闭语必须至少包含：

- 根因位置
- 立即修复
- 系统性预防修复

## 11. 失败排查

1. 检查根目录 `.env` 是否存在 `DEEPSEEK_API_KEY`
2. 检查 `.env` 是否存在 `DEEPSEEK_BASE_URL` 或 `DEEPSEEK_API_BASE_URL`
3. 先运行 `--dry-run --print-payload` 检查最终 payload
4. 若 JSON Output 卡住，确认 system 或 user prompt 中含有 `json` 字样并设置足够 `max_tokens`
5. 若思考模式下采样参数无效，确认这是 DeepSeek 官方兼容行为；改用 `thinking disabled` 或调整提示词
6. 若流式为空，先去掉 `--stream` 回退非流式
7. 若工具调用多轮报 400，确认后续请求保留了此前 assistant 的 `reasoning_content`
8. 若日志出现密钥片段，优先修脚本脱敏逻辑

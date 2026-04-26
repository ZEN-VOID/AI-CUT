# Context: deepseek

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
current_chars: auto
current_lines: auto
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-26T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `deepseek` 技能的经验层，聚焦 DeepSeek OpenAI 兼容对话接口的输入收束、思考模式、端点拼装、SSE 解析、文本落盘与脱敏排错。它是知识库，不是过程日志。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-DS-AUTH-MISSING` | 启动即报缺少 API Key | 环境配置层 | 在根目录 `.env` 设置 `DEEPSEEK_API_KEY`，或显式传 `--api-key` | 保持密钥单一事实源，不在 skill 内硬编码密钥 | `--dry-run` 不再报认证错误 |
| `TM-DS-MODEL-DRIFT` | 调用时切到 `deepseek-v4-flash` 或兼容别名 | 模型真源层 | 拒绝非 `deepseek-v4-pro` 的 `--model` | 在脚本与 `SKILL.md` 固定单模型合同 | dry-run 只能生成 `deepseek-v4-pro` payload |
| `TM-DS-URL-DRIFT` | 实际请求地址不是 `/chat/completions` | 端点组装层 | 用 base URL 自动补全 `/chat/completions` | 固化优先级：显式 URL > DEEPSEEK_BASE_URL > DEEPSEEK_API_BASE_URL > 官方默认 | 报告中的 `api_url` 正确 |
| `TM-DS-THINKING-SAMPLING` | 思考模式下 temperature/top_p 等参数看似设置但结果无变化 | 参数语义层 | 标记为兼容透传 warning；若需要采样控制，关闭 thinking 或改 prompt | 在 `SKILL.md` 和脚本报告中固定思考模式采样参数无效提示 | report 中出现 compatibility warning |
| `TM-DS-DISABLED-EFFORT` | `thinking disabled` 时 API 报 `thinking options type cannot be disabled when reasoning_effort is set` | 参数互斥层 | 禁止在 disabled 模式发送 `reasoning_effort` | payload 构造层只在 thinking enabled 时注入 effort | 非思考模式 dry-run payload 不含 `reasoning_effort` |
| `TM-DS-EFFORT-MAP` | 传入 `low/medium/xhigh` 后和官方枚举不一致 | 兼容映射层 | `low/medium -> high`，`xhigh -> max` | CLI 接受兼容值但 payload 只发 `high/max` | dry-run payload 中 effort 合法 |
| `TM-DS-MESSAGES-SHAPE` | `messages` 结构错误导致接口报 400 | 输入收束层 | 先用 `--dry-run --print-payload` 检查最终 `messages` | prompt 模式与 messages 直传模式分开处理，不强制互相覆盖 | payload 中 `messages` 至少一条且结构合法 |
| `TM-DS-REASONING-TOOL-400` | 思考模式 + tool calls 多轮后 API 报 400 | 多轮拼接层 | 保留 assistant 消息中的 `reasoning_content` 与 `tool_calls` 后再继续请求 | messages 校验允许 assistant content 为空但保留 reasoning/tool_calls | 后续 tool 请求不再因 reasoning 缺失失败 |
| `TM-DS-JSON-EMPTY` | JSON Output 返回空 content 或请求长时间卡住 | JSON Output 提示层 | prompt 中加入 `json` 字样、结构示例，并设置足够 `max_tokens` | JSON Output 调用入口固定检查提示语和 max_tokens | 非流式响应可被 `json.loads` 解析 |
| `TM-DS-STREAM-EMPTY` | `stream=true` 时控制台没有输出或最终文本为空 | SSE 解析层 | 回退非流式；同时检查最终 payload 的 `choices[].message.content` | 解析器同时支持 delta 累积和最终消息兜底 | 流式/非流式至少有一种能稳定出文本 |
| `TM-DS-REASONING-MISS` | 模型有思考内容，但报告里没有 `reasoning_content` | 响应解析层 | 同时检查 `delta.reasoning_content` 和最终 `message.reasoning_content` | 把 reasoning 提取写成双路径兼容 | 报告中 `reasoning_content` 不再丢失 |
| `TM-DS-STOP-OVERFLOW` | stop 传太多导致请求非法 | 参数校验层 | 限制 stop 最多 16 条 | 在 CLI 和 skill 合同中固定 stop 上限 | stop 超限时本地先报错 |
| `TM-DS-OUTPUT-PATH` | 文本和报告落到非项目化目录 | 输出路由层 | 用 `output_dir > project_name/task_kind 推导` 解析目录 | 默认输出根固定为 `output/影片/[项目名]/5-API/llm/deepseek/` | 文本与 report 都落到同一项目目录 |
| `TM-DS-SECRET-LOG` | report 或日志里泄露 Bearer token / sk- 前缀 | 安全日志层 | 所有错误消息与 URL 统一走脱敏函数 | 把脱敏逻辑收口到脚本公共函数 | 构造错误时输出只保留 `<redacted>` |

## Repair Playbook

1. 优先跑：
   - `python3 .agents/skills/api/deepseek/scripts/deepseek_chat.py --prompt "test" --dry-run --print-payload`
2. 先核查 `.env`：
   - `DEEPSEEK_API_KEY`
   - `DEEPSEEK_BASE_URL` 或 `DEEPSEEK_API_BASE_URL`
3. 若请求实际要做多轮工具调用：
   - 优先使用 `--messages-file`
   - 确认 assistant 消息保留 `reasoning_content` 与 `tool_calls`
4. 若 JSON Output 异常：
   - 确认 prompt 包含 `json`
   - 补输出格式示例
   - 增大 `max_tokens`
5. 若流式异常：
   - 先去掉 `--stream` 验证基本路径
   - 再检查 SSE 事件中的 `choices[].delta`
6. 若输出缺少文本文件或报告：
   - 检查是否显式使用 `--no-save-text` 或 `--no-report`
   - 再检查输出目录权限与解析结果
7. 若日志含密钥：
   - 优先修脚本脱敏函数，不要只手工删一次日志

## Reusable Heuristics

- DeepSeek 官方 API 优先走 OpenAI 兼容 `chat/completions`，本地脚本只做机械调用与产物管理，不承担主创判断。
- 对简单文本任务，`prompt + system` 足够；对多轮、工具调用、JSON 结构或复杂上下文，优先走 `messages` 直传。
- `--dry-run --print-payload` 是验证 skill 合同最稳的入口，因为它不依赖真实 API 成功也能检查输入收束、thinking 参数与 URL 组装。
- DeepSeek 思考模式默认启用；如果用户抱怨采样参数“不听话”，先解释并检查 thinking，而不是盲目调 temperature。
- DeepSeek tool calls 在思考模式下的多轮拼接比普通对话更严格；丢失 `reasoning_content` 会导致后续请求失败。
- 默认输出目录应当项目化，否则 provider skill 很容易在大量实验调用后留下难以清理的散落文本。

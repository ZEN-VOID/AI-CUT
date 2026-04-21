# Context: doubao-seed-2.0-pro

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
last_checked_at: 2026-04-21T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `doubao-seed-2.0-pro` 技能的经验层，聚焦 AnyFast OpenAI 兼容对话接口的输入收束、端点拼装、SSE 解析、文本落盘与脱敏排错。它是知识库，不是过程日志。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-DBP-AUTH-MISSING` | 启动即报缺少 API Key | 环境配置层 | 在根目录 `.env` 设置 `ANYFAST_API_KEY`，或显式传 `--api-key` | 保持密钥单一事实源，不在 skill 内硬编码密钥 | `--dry-run` 不再报认证错误 |
| `TM-DBP-URL-DRIFT` | 实际请求地址不是 `/v1/chat/completions` | 端点组装层 | 用 base URL 自动补全 `/v1/chat/completions` | 固化优先级：显式 URL > ANYFAST_BASE_URL > ANYFAST_API_BASE_URL > 官方默认 | 报告中的 `api_url` 正确 |
| `TM-DBP-MESSAGES-SHAPE` | `messages` 结构错误导致接口报 400 | 输入收束层 | 先用 `--dry-run --print-payload` 检查最终 `messages` | prompt 模式与 messages 直传模式分开处理，不强制互相覆盖 | payload 中 `messages` 至少一条且结构合法 |
| `TM-DBP-STREAM-EMPTY` | `stream=true` 时控制台没有输出或最终文本为空 | SSE 解析层 | 回退非流式；同时检查最终 payload 的 `choices[].message.content` | 解析器同时支持 delta 累积和最终消息兜底 | 流式/非流式至少有一种能稳定出文本 |
| `TM-DBP-REASONING-MISS` | 模型有推理信息，但报告里没有 `reasoning_content` | 响应解析层 | 同时检查 `delta.reasoning_content` 和最终 `message.reasoning_content` | 把 reasoning 提取写成双路径兼容 | 报告中 `reasoning_content` 不再丢失 |
| `TM-DBP-STOP-OVERFLOW` | stop 传太多导致请求非法 | 参数校验层 | 限制 stop 最多 4 条 | 在 CLI 和 skill 合同中固定 stop 上限 | stop 超限时本地先报错 |
| `TM-DBP-OUTPUT-PATH` | 文本和报告落到非项目化目录 | 输出路由层 | 用 `output_dir > project_name/task_kind 推导` 解析目录 | 默认输出根固定为 `output/影片/[项目名]/5-API/llm/doubao-seed-2.0-pro/` | 文本与 report 都落到同一项目目录 |
| `TM-DBP-SECRET-LOG` | report 或日志里泄露 Bearer token / sk- 前缀 | 安全日志层 | 所有错误消息与 URL 统一走脱敏函数 | 把脱敏逻辑收口到脚本公共函数 | 构造错误时输出只保留 `<redacted>` |

## Repair Playbook

1. 优先跑：
   - `python3 .agents/skills/api/anyfast/llm/doubao-seed-2.0-pro/scripts/doubao_seed_chat.py --prompt "test" --dry-run --print-payload`
2. 先核查 `.env`：
   - `ANYFAST_API_KEY`
   - `ANYFAST_BASE_URL` 或 `ANYFAST_API_BASE_URL`
3. 若请求实际要做多模态消息：
   - 优先使用 `--messages-file`
   - 不要把复杂数组内容硬塞回 `--prompt`
4. 若流式异常：
   - 先去掉 `--stream` 验证基本路径
   - 再检查 SSE 事件中的 `choices[].delta`
5. 若输出缺少文本文件或报告：
   - 检查是否显式使用 `--no-save-text` 或 `--no-report`
   - 再检查输出目录权限与解析结果
6. 若日志含密钥：
   - 优先修脚本脱敏函数，不要只手工删一次日志

## Reusable Heuristics

- AnyFast 的豆包对话能力优先走 OpenAI 兼容 `chat/completions`，这比为单模型写专用请求结构更稳。
- 对简单文本任务，`prompt + system` 足够；对复杂上下文、多模态或工具化消息，优先走 `messages` 直传。
- `--dry-run --print-payload` 是验证 skill 合同最稳的入口，因为它不依赖真实 API 成功也能检查输入收束与 URL 组装。
- 流式输出要把“边收边打”和“最终兜底抽取”都实现，否则只要 SSE 事件稍有差异就会出现空文本假失败。
- 默认输出目录应当项目化，否则 provider skill 很容易在大量实验调用后留下难以清理的散落文本。

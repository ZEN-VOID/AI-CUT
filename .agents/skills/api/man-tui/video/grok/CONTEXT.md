# Context: man-tui-grok-video

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
last_checked_at: 2026-04-19T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `man-tui-grok-video` 技能的经验层，聚焦漫涂 Grok 异步视频 API 的 multipart 创建、状态轮询、内容重定向下载、项目化输出路径与日志脱敏。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-MTG-AUTH-MISSING` | 脚本启动即报缺少 API Key | 环境配置层 | 在根目录 `.env` 配置 `MAN_TUI_GROK_API_KEY` 或 `MAN_TUI_GROK_CONNECTION_JSON` | 保持 Grok 专用连接为优先事实源，通用 `MAN_TUI_API_KEY` 只作回退；脚本只接受显式 `--api-key` 作为覆盖 | `create --dry-run` 不再报认证错误 |
| `TM-MTG-CONN-JSON-DRIFT` | 用户给了 `newapi_channel_conn`，但脚本仍走旧全局 key | 环境解析层 | 让脚本优先解析 `MAN_TUI_GROK_CONNECTION_JSON.key/url` | 将 Grok 专用连接 JSON 纳入脚本默认读取顺序，并在技能文档写明回退链 | dry-run 的 base_url 与认证来源符合 Grok 专用配置 |
| `TM-MTG-MULTIPART-MISMATCH` | 创建任务返回 4xx，提示字段或请求体不合法 | 请求体构造层 | 确认创建接口使用 multipart，而不是 JSON body | 在脚本与 `SKILL.md` 固化 multipart 合同 | `--dry-run --print-request` 显示 form-data 摘要 |
| `TM-MTG-REFERENCE-CONFLICT` | 同时传本地参考图和远程参考图，结果不可预期 | 输入合同层 | 让 `input_reference` 与 `image_reference` 互斥 | 在参数解析阶段提前硬拒绝 | 同时传两种参考图时脚本非零退出 |
| `TM-MTG-REMOTE-REF-STRING` | 远程参考图传了 URL 列表但接口仍报错 | 字段编码层 | 把 URL 列表转为 JSON 字符串再写入 `image_reference` | 统一通过一个函数构造远程参考图字段 | 请求摘要里 `image_reference` 是字符串化 JSON 数组 |
| `TM-MTG-WAIT-TIMEOUT` | `--wait` 长时间无结果或误判失败 | 轮询层 | 区分终态、非终态与超时；给出明确 timeout 说明 | 固化状态轮询 helper，不在命令层各自手写等待 | `status --wait` 超时后有明确诊断字段 |
| `TM-MTG-CONTENT-REDIRECT` | `/content` 调用成功但本地没有视频文件 | 下载层 | 确保 GET 下载允许跟随重定向并流式写文件 | 在报告中记录 `final_url` 与保存路径 | 下载后 `saved_file` 存在且非空 |
| `TM-MTG-OUTPUT-PATH` | 报告和视频落到随机目录，和项目 runtime 脱节 | 输出路由层 | 统一走 `output_dir > project_name/task_kind -> 默认项目化路径` | 把输出路径解析收口到单一 helper | 报告与 MP4 位于 `output/影片/[项目名]/5-API/video/man-tui/grok/` |
| `TM-MTG-SECRET-LOG` | 报告或异常文本里出现 Bearer token / sk- 前缀 | 安全日志层 | 对日志、URL、错误信息做统一脱敏 | 把脱敏逻辑内建到报告写入和异常格式化 | 构造异常时输出中只保留 `<redacted>` |

## Repair Playbook

1. 先跑创建 dry-run：

```bash
python3 .agents/skills/api/man-tui/video/grok/scripts/grok_video.py create \
  --prompt "test" \
  --dry-run --print-request
```

2. 检查 `.env`：
   - `MAN_TUI_GROK_API_KEY`
   - `MAN_TUI_GROK_API_BASE_URL`
   - 或 `MAN_TUI_GROK_CONNECTION_JSON`
3. 若是远程参考图任务：
   - 先确认传入方式是重复 `--image-reference-url` 或合法 `--image-reference-json`
   - 再确认脚本摘要中 `image_reference` 已变成 JSON 字符串
4. 若是本地参考图任务：
   - 先检查文件路径存在
   - 再检查只传了单张文件
5. 若等待卡住：
   - 先单查 `status`
   - 再检查 `wait_timeout` 与 `poll_interval`
6. 若下载失败：
   - 先看状态是否已 `completed`
   - 再看报告中的 `final_url` 和 `saved_file`
7. 若出现密钥泄露：
   - 直接修脚本脱敏逻辑
   - 不接受“测试环境可以泄露”的局部豁免

## Reusable Heuristics

- 漫涂这组接口是标准异步三段式：创建、查询、取内容；最稳的 CLI 不是只封一条 POST，而是把轮询和下载也纳入同一脚本契约。
- 当同一个 provider 存在 Grok 专用 key 与通用 key 时，优先让脚本读 provider-specific env，再回退全局 env，避免为了某一路接口切换而误伤别的 Man-Tui 能力。
- `image_reference` 最容易出错的点不是 URL 本身，而是接口要求它是“JSON 字符串”，不是原生数组。
- `GET /content` 可能走 `302`，所以“状态完成但没有 MP4”往往不是生成失败，而是下载逻辑没跟重定向。
- 同一个技能里若同时支持创建、查询、下载，报告格式要尽量统一，不然排障时很难横向比对。
- 对视频类 provider skill，默认项目化输出目录最好固定到 `output/影片/[项目名]/5-API/video/<provider>/<model>/`，这样后续批量治理和资产搜索都更稳定。
- 若只是验证请求结构，不要真的发网路请求；优先用 `--dry-run --print-request` 验 multipart 摘要、参考图模式与输出路径。

# Context: man-tui-sora-video

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

本文件作为 `man-tui-sora-video` 技能的经验层，聚焦漫涂 Sora 2 异步视频 API 的 JSON 创建、状态轮询、去水印 URL 优先级下载、项目化输出路径与日志脱敏。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-MTS-AUTH-MISSING` | 脚本启动即报缺少 API Key | 环境配置层 | 在根目录 `.env` 配置 `MAN_TUI_API_KEY` | 保持 `.env` 为密钥单一事实源；脚本只接受显式 `--api-key` 作为覆盖 | `create --dry-run` 不再报认证错误 |
| `TM-MTS-JSON-MISMATCH` | 创建任务返回 4xx，提示 body 不合法 | 请求体构造层 | 确认创建接口使用 JSON，而不是 multipart | 在脚本与 `SKILL.md` 固化 JSON body 合同 | `--dry-run --print-request` 显示 JSON 摘要 |
| `TM-MTS-GROUP-OVERRIDE` | 用户要求切到默认分组，但请求仍被路由到旧分发组 | Provider 路由覆盖层 | 给脚本补显式 `group / group_transport / group_header`，默认发 `group=default` | 把 group 从“隐式推断”收口为可见 CLI / env 合同，并在 dry-run 中打印 | 请求摘要中能看到 `group=default` 与注入方式 |
| `TM-MTS-BACKEND-DEFAULT-GROUP` | Provider 明确说 Sora 在默认分组，但请求仍落到 Grok 异步轮询组 | Provider 后台配置层 | 直接要求 provider 切换当前 key 的后台默认分组 | 在技能中把“后台默认分组”与“客户端 group 字段”分开，避免继续误修客户端 | provider 明确回复分组选错且切后台后恢复 |
| `TM-MTS-REF-NOT-URL` | 图生视频提交失败，提示参考图无效 | 输入合同层 | 让 `input_reference` 只接受公网 URL | 在参数解析阶段提前拒绝本地路径/相对路径 | 本地路径输入时脚本非零退出 |
| `TM-MTS-CHANNEL-UNAVAILABLE` | `sora-2` 创建请求直接返回 `503 model_not_found` | Provider 通道路由层 | 识别为 Man-Tui 当前账号/分发组下无可用 Sora 通道，不把问题误判为请求体错误 | 在技能经验层固定“先用 raw HTTP 复核认证与 body，再把 `model_not_found under group ...` 归类为服务端路由缺口” | Bearer / raw Authorization 都返回同一 `model_not_found` |
| `TM-MTS-GROUP-IGNORED` | 本地已显式发送 `group=default`，但服务端仍回 `under group GrokVideo-异步轮询` | Provider 接入兼容层 | 判定为服务端未接受本地 group 覆盖，停止继续猜测单一字段名 | 保留 `header/body/both` 三模式以便快速验证，但把最终结论收口为“需 provider 确认正式 group 契约” | 三种 transport 与 `.env` 默认值都不改变错误中的 group 名 |
| `TM-MTS-WAIT-TIMEOUT` | `--wait` 长时间无结果或误判失败 | 轮询层 | 区分终态、非终态与超时；给出明确 timeout 说明 | 固化状态轮询 helper，不在命令层各自手写等待 | `status --wait` 超时后有明确诊断字段 |
| `TM-MTS-CONTENT-VIOLATION` | `status=completed` 但实际不可下载 | 状态解释层 | 把 `content_violation=true` 视为不可下载终态 | 在下载前固定执行状态/违规检查 | 完成但违规时不会伪装成成功下载 |
| `TM-MTS-URL-PRIORITY` | 已完成但下载逻辑拿错链接或拿不到链接 | 结果解析层 | 按 `watermark_free_url -> video_url -> result.watermark_free_url -> result.share_url` 固定优先级解析 | 收口到单一 URL 解析函数 | 完成任务能稳定拿到最终下载 URL |
| `TM-MTS-OUTPUT-PATH` | 报告和视频落到随机目录，和项目 runtime 脱节 | 输出路由层 | 统一走 `output_dir > project_name/task_kind -> 默认项目化路径` | 把输出路径解析收口到单一 helper | 报告与 MP4 位于 `output/影片/[项目名]/5-API/video/man-tui/sora/` |
| `TM-MTS-SECRET-LOG` | 报告或异常文本里出现 Bearer token / sk- 前缀 / 带签名 URL | 安全日志层 | 对日志、URL、错误信息做统一脱敏 | 把脱敏逻辑内建到报告写入和异常格式化 | 构造异常时输出中只保留 `<redacted>` |
| `TM-MTS-XAPIKEY-DRIFT` | 文档称 `x-api-key` 可用，但实测返回 `401 Invalid token` | 文档兼容层 | 当前环境统一使用 `Authorization` 请求头，不依赖 `x-api-key` | 在参考文档中标注“兼容声明与实测存在漂移”，把 `Authorization` 作为稳定主路径 | Bearer / raw Authorization 可达，`x-api-key` 不可达 |

## Repair Playbook

1. 先跑创建 dry-run：

```bash
python3 .agents/skills/api/man-tui/video/sora/scripts/sora_video.py create \
  --prompt "test" \
  --dry-run --print-request
```

2. 检查 `.env`：
   - `MAN_TUI_API_KEY`
   - `MAN_TUI_API_BASE_URL`
3. 若是图生视频任务：
   - 先确认 `--input-reference` 是公网 URL
   - 再确认请求摘要中 `input_reference` 仅在图生视频模式出现
4. 若等待卡住：
   - 先单查 `status`
   - 再检查 `wait_timeout` 与 `poll_interval`
5. 若下载失败：
   - 先看状态是否已 `completed`
   - 再看 `content_violation`
   - 再看报告中的 `final_url` 和 `saved_file`
6. 若出现密钥或签名 URL 泄露：
   - 直接修脚本脱敏逻辑
   - 不接受“测试环境可以泄露”的局部豁免

## Reusable Heuristics

- 漫涂 Sora 这组接口是标准异步两段式主链：创建、查询；下载不是独立业务接口，而是从状态结果里解析 URL 再取文件。
- `watermark_free_url` 是最重要的落点；若顶层没有，再向 `video_url` 和 `result.*` 回退，不要反过来。
- `content_violation=true` 是高优先级信号，不能因为 `status=completed` 就直接当成功。
- 对视频类 provider skill，默认项目化输出目录最好固定到 `output/影片/[项目名]/5-API/video/<provider>/<model>/`，这样后续批量治理和资产搜索都更稳定。
- 若只是验证请求结构，不要真的发网络请求；优先用 `--dry-run --print-request` 验 JSON 摘要、URL 模式与输出路径。
- provider 已明确区分三类后台分组：`grok` 异步、`sora`、画图；如果请求持续落到 `GrokVideo-异步轮询`，优先怀疑 key 的后台默认分组配置错了。
- 对当前 skill，客户端 `group` 注入只保留为兼容性排障工具，不再把它当成默认修复路径。
- 因为公开片段没披露 group 的正式写法，所以本地实现保留 `header / body / both` 三种注入方式；排障时先看 dry-run 摘要里是否真的带上了预期 group。
- 若 `header / body / both` 三种模式都仍然返回同一个 `under group GrokVideo-异步轮询`，高概率不是本地字段名拼错，而是 provider 根本没有开放客户端覆盖分组，或当前 key 被强制绑到了固定 distributor group。
- 若 Bearer 与 raw `Authorization` 都返回 `model_not_found`，且错误里带 `under group ...`，优先判定为 Man-Tui 当前分发组没有可用 Sora 通道，而不是脚本 JSON body 写错。
- 当前环境下 `x-api-key` 与文档描述不一致；若需要真实调用，先坚持使用 `Authorization` 头，不要把 `401 Invalid token` 误判为 `.env` 缺失。

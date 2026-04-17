# Context: grok

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
last_checked_at: 2026-04-17T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `grok` 技能的经验层，默认以知识库模式维护：优先沉淀 FineAPI Grok Video 3 的创建接口约束、图片链接输入边界、Base URL 显式配置要求，以及“创建回执 != 成片结果”的执行认知。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-GROK-CREATE-ONLY` | 调用方把 `POST /v1/video/create` 的回执误当成视频成片 | 工作流契约层 | 明确当前只完成 create receipt 阶段 | 在 `SKILL.md` 与脚本输出中显式标注“当前未覆盖状态/下载” | 报告只出现 `id/status/status_update_time`，不虚构下载地址 |
| `TM-GROK-IMAGE-URL` | 把本地路径或二进制内容塞进 `images`，接口报错 | 输入边界层 | 只接受公网 `http/https` 链接 | 在脚本前置校验中强制拦截非 URL 输入 | `--image ./foo.png` 直接报错并给动作建议 |
| `TM-GROK-BASE-URL` | 文档只给相对路径，脚本无默认 host 或未继承共享网关导致无法调用 | 环境配置层 | 通过 `.env` 或 `--base-url` 提供 API Base URL，并优先继承 `ANYFAST_API_BASE_URL` | 保持“共享 AnyFast 基线 + provider 覆盖”的策略，并把缺失诊断写成硬错误 | 未配置 Base URL 时，脚本直接给出明确报错 |
| `TM-GROK-SHARED-ANYFAST-ENV` | 仓库已配置 `ANYFAST_VIDEO_API_KEY / ANYFAST_API_BASE_URL`，但 `grok` 仍误报缺少 key 或 host，或被旧 `GROK_*` 抢回错误 host | 真源同步层 | 把 `ANYFAST_*` 加入脚本、主合同与参考文档回退链，并把共享基线提到本地变量前 | 固定“同系列 provider 先继承共享 AnyFast 环境，`GROK_*` 只做局部补充”的合同 | 不显式传 `GROK_*` 时，dry-run 仍能从共享 `.env` 得到完整请求摘要，且优先落到共享网关 |
| `TM-GROK-720P-FIRST` | 调用 `1080P` 后失败，但使用者以为技能坏了 | 供应商能力漂移层 | 回退到 `720P` | 把“字段枚举存在 1080P，但截图注明暂只支持 720P”沉到技能合同 | `720P` 成为默认值，`1080P` 仅保留风险提示 |
| `TM-GROK-HIGHEST-VERIFIED` | 调用方希望把默认模型盲目上调到更高命名版本 | 供应商可用渠道层 | 以真实提交结果判定；当前回退到 `grok-video-3` | 把“默认模型 = 当前环境最高已验证可用版本”写入合同，并在 `model_not_found` 时给出回退提示 | `grok-video-3` 可成功创建任务，`grok-video-3-max` 返回 `model_not_found` |
| `TM-GROK-PROMPT-SUFFIX` | 把 `--mode=custom` 等提示后缀清洗掉，导致供应商模式失真 | Prompt 保真层 | 提示词原样透传 | 在脚本中不对 prompt 追加额外清洗逻辑 | 报告中的 `prompt` 与输入一致 |
| `TM-GROK-JSON-SHAPE` | 错用 multipart 或把 `images` 写成单字符串 | 请求构造层 | 固定 `application/json`，并保持 `images` 为数组 | 在 dry-run 中输出最终 JSON 结构，便于人工核对 | `request_summary.data.images` 始终是数组 |
| `TM-GROK-DRYRUN-SECRET-GATE` | 只是想先检查请求体，却因为缺少 API Key 无法运行 `--dry-run` | CLI 执行入口层 | 允许 dry-run 在无密钥时继续，只打印结构化请求摘要 | 将“dry-run 不强制密钥”写入脚本与 `SKILL.md`，避免把预检步骤绑死在鉴权上 | 未配置 API Key 时，`submit --dry-run --print-payload` 仍能输出请求摘要 |
| `TM-GROK-REPORT-SELF-DESCRIBE` | 终端打印结果含 `report_json`，但落盘文件缺少该字段 | 报告落盘层 | 在写 JSON 前先补齐 `report_json` | 保持打印结果与落盘结果同构，避免后续自动化读取到两套 schema | 报告文件内也包含 `report_json` |

## Repair Playbook

1. **先做 Dry Run**
   - 运行 `submit --dry-run --print-payload`
   - 先确认 `base_url / model / aspect_ratio / size / images`
2. **再查图片输入**
   - 每一项都必须是可访问的 `http/https` URL
   - 若是本地图片，先走上游上传流程取得 URL
3. **再查尺寸**
   - 默认先用 `720P`
   - 若用户坚持 `1080P`，应先提醒当前存在供应商侧不支持风险
4. **再查 Base URL**
   - 先看共享 `.env` 里的 `ANYFAST_API_BASE_URL` 是否已提供，再看 `GROK_VIDEO_API_BASE_URL`
   - 若两者都没有，再要求调用方显式传 `--base-url`
5. **最后看回执解释**
   - 成功回执只代表任务已创建
   - 没有确认后续查询/下载接口前，不要承诺成片位置

## Reusable Heuristics

- 当供应商文档只给相对路径而不暴露 host 时，最稳的策略不是拍脑袋写默认值，而是把 Base URL 升级成显式配置项。
- 同一供应商家族若已经有共享网关和共享视频 key，默认应先吃共享基线；provider 局部变量只在共享基线缺失或需要特例时再介入。
- “最高版本”应该以当前 provider 的真实可用性为准，而不是按第三方站点、命名后缀或营销文案猜更高版本。
- 只要接口字段名已经明确写成 `images: array[string]` 且说明是“图片链接”，就不要偷偷扩展成文件上传能力。
- 当截图同时出现“枚举包含 1080P”和“暂只支持 720P”两种信号时，应保留两者，而不是把其中之一抹平。
- 异步视频接口的第一步回执经常非常像“成功结果”；技能合同必须明确区分“任务已创建”和“视频已可下载”。
- 预检型 dry-run 的目标是尽早暴露 JSON 结构问题；不要把它和真实鉴权强绑定，否则最便宜的检查步骤会失效。
- 如果 CLI 会把结果写盘，终端输出与落盘 JSON 应尽量同构；否则后续脚本会遇到“屏幕上有、文件里没有”的隐性 schema 漂移。

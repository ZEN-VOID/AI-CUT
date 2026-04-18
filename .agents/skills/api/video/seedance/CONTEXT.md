# Context: seedance

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

本文件作为 `seedance` 技能的经验层，默认以知识库模式维护：优先沉淀 `content[]` 场景互斥、模型别名真源同步、状态响应归一、以及视频 URL 抽取回退链。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-SEEDANCE-MODE-MIX` | 请求同时出现 `first_frame` 和 `reference_image` | 场景合同层 | 回到单一模式重新构造 `content[]` | 把 `mode -> role` 映射集中到单一 builder，不在外层零散拼角色 | dry-run 中角色始终与场景一致 |
| `TM-SEEDANCE-WEB-TEXT-ONLY` | 开启 `web_search` 后仍带图片/视频/音频，网关拒绝 | 工具边界层 | `web_search` 只用于纯文本生视频 | 在脚本本地校验中硬拦截“联网搜索 + 媒体”组合 | `--web-search` 搭配媒体时本地即失败 |
| `TM-SEEDANCE-AUDIO-NOT-ALONE` | 只传音频导致请求不合法 | 输入边界层 | 强制要求至少有 1 个图片或视频参考 | 在 builder 中把“audio 不能单独存在”做成硬校验 | 只传音频时本地即失败 |
| `TM-SEEDANCE-ALIAS-DRIFT` | 本地技能仍按旧版本/旧冲突口径解释 `seedance` 与 `seedance-fast` | 真源同步层 | 回到父级 `../runbooks/default-model-policy.md` 的 `rolling-latest-quality-alias` 规则族，再核对官方 AnyFast 文档 | 子技能只声明 Seedance 的滚动别名语义，不再在多个载体平行重写“最新质量优先”算法 | 默认运行 `run` 时不显式传 `--model` 仍落到最新质量档 |
| `TM-SEEDANCE-PLATFORM-VS-API` | 平台站点被误写成 API Base URL，导致默认请求落错 host | 网关基线层 | 把默认 Base URL 改回已验证 AnyFast API 网关，并拆开平台/文档/API 三类 URL | 在脚本默认值和参考文档里只把 `ANYFAST_API_BASE_URL` 指向真实网关 | dry-run 中 `url` 不再指向平台首页域名 |
| `TM-SEEDANCE-LOCAL-MEDIA` | 本地图片/音频路径原样塞进请求体 | 输入归一层 | 转成 Data URL | 把本地编码逻辑集中到 helper，并禁止本地视频假支持 | payload 中不再出现本地图片/音频路径 |
| `TM-SEEDANCE-STATUS-SHAPE` | 查询接口返回 200，但状态读取错层或外层给出 `IN_PROGRESS` 这类供应商态 | 响应归一层 | 同时读取外层 `data.status` 与内层 `data.data.status`，并把 `in_progress` 归入运行态 | 将状态规范化收敛到单一 helper，保留 `raw_response` 和显式运行态集合 | status report 同时含 `normalized_status` 与原始响应 |
| `TM-SEEDANCE-VIDEO-URL-FALLBACK` | SUCCESS 了却拿不到 `content.video_url` | 结果提取层 | 回退检查 `fail_reason` 是否异常承载 URL | 把 URL 抽取路径集中到 helper，并在报告里记录尝试路径 | 成功报告含 `video_url` 或 `video_url_paths_tried` |

## Repair Playbook

1. 先跑 `submit --dry-run --print-payload`
2. 确认当前 `mode` 与 `content[]` 角色映射一致
3. 若带 `web_search`，确认没有任何媒体输入
4. 若需要确认默认模型是否仍指向最新质量档，先核对官方 AnyFast 文档与本地 `references/api.md`
5. 查询成功但没有视频时，先看 `data.data.content.video_url`
6. 若仍为空，再看 `fail_reason` 是否误承载了 URL

## Reusable Heuristics

- 对存在滚动别名的模型接口，默认值不应写成易过期的长版本号；先回到父级共享 runbook 确认其属于 `rolling-latest-quality-alias`，再由子技能补别名语义。
- `content[]` 一旦支持多种角色，最容易出错的不是 HTTP 层，而是模式识别层；把模式裁决和角色构造放在同一个 builder 里，比让 CLI 参数层分别拼装更稳。
- 如果查询响应外层和内层都有 `status`，默认应同时保留两者，再用统一归一层给出 `normalized_status`，不要过早只信其中一个。
- 当供应商成功响应样例都出现字段错位时，下载 URL 抽取就必须保留回退链和尝试路径报告，而不是只盯着一个理想字段。
- 平台站点、文档站点和 API 网关必须分三套变量维护；只要脚本真的要发请求，默认值就只能来自已验证网关，而不是前台站点。

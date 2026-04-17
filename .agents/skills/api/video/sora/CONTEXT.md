# Context: sora

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

本文件作为 `sora` 技能的经验层，默认以知识库模式维护：优先沉淀 AnyFast Sora 2 的三段异步合同、模型别名漂移、加速端点配置回退、参考图读取，以及下载阶段的 JSON->MP4 二跳逻辑。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-SORA-ASYNC-MISREAD` | 调用方把 `/v1/videos` 当作同步返回成片接口 | 工作流契约层 | 回到“创建 -> 查询 -> 下载”三段流程 | 在 `SKILL.md` 与脚本子命令中显式拆出 `submit/status/download/run` | `run` 能完整拿到 MP4；`submit` 只返回任务回执 |
| `TM-SORA-CONTENT-JSON` | 误把 `/v1/videos/{id}/content` 当作二进制下载，结果保存失败 | 下载契约层 | 先解析 JSON，再取 `video_url/url` 二次下载 | 在脚本里固定把 `/content` 响应保存为结构化 JSON，而不是直接流式写盘 | 报告里能看到 `video_url` 与本地 MP4 路径 |
| `TM-SORA-MODEL-LADDER` | 默认仍落在低档 `sora-2`，导致“默认最高版本”要求失效或先打到旧通道 | 网关兼容层 | 将默认模型提升到最高已知档位，并按 `official-sora-2-pro -> sora-2-pro -> official-sora-2 -> sora-2` 向下回退 | 把默认模型与候选链拆开：未显式传参时走质量优先链，显式传参时只做同档别名兼容 | Dry-run 中能看到最高档位在首位；真实提交时若首位不可用会继续向下尝试 |
| `TM-SORA-GROUP-CHANNEL-MISSING` | 多个模型在自定义网关和官方端点都报 `No available channel for model ... under group auto (distributor)` | 账户通道层 | 停止继续试模型别名，转查账户分组/渠道是否开通 Sora | 在脚本诊断里把“别名不对”与“账户分组无通道”分开；双端点同错时直接指向账户层 | 官方端点与加速端点都报同类 `group auto (distributor)` 错误时，不再重复试模型链 |
| `TM-SORA-BASE-URL-DRIFT` | 平台站点被误写成 `/v1/videos` 的默认 host，实际调用应走 AnyFast API 网关 | 环境配置层 | 在 `.env` 中设置 `SORA_API_BASE_URL` 或 `ANYFAST_API_BASE_URL`，并把兜底改回已验证网关 `https://fw2afus.ent.acc.kurtisasia.com` | 把平台 URL、文档 URL、API Base URL 拆成独立环境变量 | `--dry-run` 中可见实际请求 URL 指向目标网关 |
| `TM-SORA-SINGLE-REFERENCE` | 用户传了多张图，接口报错或行为不确定 | 输入边界层 | 立即拒绝多图输入，提示当前接口只支持单张首帧参考 | 脚本参数校验与 `SKILL.md` 双重卡死 | `--image a --image b` 直接报错 |
| `TM-SORA-REMOTE-IMAGE` | 远程参考图 URL 可访问，但脚本没转成文件上传导致接口不认 | 请求构造层 | 先把远程图下载为 bytes，再以 multipart 文件部件提交 | 保留统一图片读取层：本地/远程/data URL 都归一到 `bytes + mime_type` | 三种图片输入都能走到相同 multipart 构造逻辑 |
| `TM-SORA-POLL-TIMEOUT` | 状态长期停在 `queued/in_progress`，脚本无限等待 | 轮询控制层 | 设置 `max_wait_seconds` 并在超时后带报告退出 | 固定轮询间隔与上限时长，超时视为显式失败而不是悬挂 | 超时后报告含最后一次状态与等待时长 |
| `TM-SORA-SECRET-HYGIENE` | 报告或技能文件中出现明文 Authorization Token | 安全层 | 只在运行时拼接鉴权头，报告里做脱敏 | 把 `.env` 作为密钥单一事实源；报告只保留 `Bearer ***` | 仓内 grep 不出现新增明文密钥泄露 |
| `TM-SORA-CLI-ARG-ORDER` | `run --project-name ...` 或 `submit --output-dir ...` 被判为未知参数 | CLI 入口层 | 让公共参数同时挂到根解析器与各子命令 | 对 `submit/status/download/run` 都复用同一个 `common_parser`，兼容参数放在子命令前后两侧 | `python3 ... run --project-name 测试 --dry-run` 可正常解析 |
| `TM-SORA-QUOTA-EXHAUSTED` | 创建任务立即返回 `401` 令牌额度耗尽，或 `403 insufficient_user_quota` / `quota not enough` | 账户配额层 | 先确认当前 key 是否还有余额；若专用 `ANYFAST_VIDEO_API_KEY` 耗尽，再显式切到其他有额度的 key | 脚本在创建失败时输出 `diagnostic_hint`，把“额度不足”和“模型通道不存在”区分开 | 失败报告里能直接看到额度诊断，而不是只剩原始错误体 |

## Repair Playbook

1. **先做 Dry Run**
   - 运行 `submit --dry-run --print-payload`
   - 先确认 `base_url / model / seconds / size / image_summary`
2. **再查模型名**
   - 未显式传 `--model` 时，默认应从 `official-sora-2-pro` 开始
   - 若高档位不可用，再沿候选链降到 `sora-2-pro -> official-sora-2 -> sora-2`
3. **参考图排查**
   - 本地图：确认路径存在
   - 远程图：确认 URL 可 GET
   - data URL：确认以 `data:image/` 开头
4. **状态轮询排查**
   - 若任务长时间不完成，先看 `status` 是否持续变化
   - 若完全不变化，优先判断上游排队或网关未入队，而不是继续改 prompt
5. **下载排查**
   - 先看 `/content` JSON 是否含 `video_url` 或 `url`
   - 再看二次下载是否超时、403 或保存路径错误
6. **输出路径排查**
   - 默认应为 `output/影片/[项目名]/5-API/video/sora/`
   - 若上游另有项目化路径合同，显式传 `--output-dir`
7. **CLI 参数顺序排查**
   - 如果公共参数写在子命令后面时报“unknown arguments”，优先检查解析器是否把公共参数只挂在根层
   - `submit/status/download/run` 应共享同一套公共参数定义
8. **额度排查**
   - 若创建阶段直接返回 `额度已用尽`、`insufficient_user_quota` 或 `quota not enough`，先停在账户层，不要继续改 prompt
   - 专用 `ANYFAST_VIDEO_API_KEY` 耗尽时，可显式用 `--api-key` 切到另一把有余额的 key 验证
9. **通道排查**
   - 若多个模型都报 `No available channel for model ... under group auto (distributor)`，先用官方端点再复核一次
   - 若官方端点与当前加速端点同样报错，直接判为账户分组未开通 Sora 通道，而不是模型别名问题

## Reusable Heuristics

- 看到异步视频接口时，第一反应应该是“任务对象 + 轮询状态”，不是“同步拿文件”。
- 同一供应商的网页文档值与加速网关实值不完全一致时，优先把差异建模为“候选别名链”，而不是把其中一方宣判为错。
- “默认模型”与“兼容回退链”是两件事：默认应指向最高已知质量档位，回退链再负责兼容旧别名和低档通道。
- 同一把 key 在官方端点和加速端点都报 `group auto (distributor)` 无通道时，继续切模型名价值很低，应该转查供应商后台是否给该组开通了 Sora。
- 远程参考图最稳的处理方式不是把 URL 原样塞进 multipart，而是先读成 bytes，再统一作为文件部件上传。
- `/content` 返回 JSON 的接口，最容易出现的误修是把它当成 MP4 二进制直接保存；先看 `Content-Type` 和返回体结构。
- `.env` 里应把平台 URL、文档 URL、API Base URL、专用 API Key 分开表达，这样切换加速网关时不需要顺手改坏文档或控制台地址。
- 带子命令的 CLI，只把公共参数挂在根解析器上是不够的；如果希望参数能自然写在子命令后面，子命令本身也要复用同一套公共参数定义。
- 同一轮创建失败里同时出现“额度不足”和“模型通道不存在”时，先处理额度；没有余额时，模型别名是否可用没有验证意义。

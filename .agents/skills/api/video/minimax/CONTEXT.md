# Context: minimax

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

本文件作为 `minimax` 技能的经验层，默认以知识库模式维护：优先沉淀 `POST /v1/video/generations` 的 JSON 创建合同、海螺默认模型随“已登记 Hailuo 系列最高版本”自动推进的规则（当前解析为 `Hailuo-2.3`）、`.env` 中 `ANYFAST_VIDEO_API_KEY` 的统一鉴权、以及“只到 create receipt”为止的闭环边界。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-MINIMAX-DEFAULT-MODEL-DRIFT` | 新增更高 Hailuo 版本后默认模型仍停在旧值 | 默认值治理层 | 把默认值改回“按已登记 Hailuo 系列最高版本自动选择” | 只在 `KNOWN_MODELS` 维护模型集合，由脚本统一推导 `DEFAULT_MODEL`，文档只描述规则与当前解析结果 | 新增更高版本模型后，无需改 CLI 默认值常量即可自动前进 |
| `TM-MINIMAX-CREATE-ONLY` | 调用方把创建回执误当成视频成片 | 工作流契约层 | 明确当前只覆盖 create receipt | 在 `SKILL.md` 与脚本输出中显式标注“当前未覆盖状态/下载” | 报告只出现 `id/task_id/status/created_at`，不虚构下载地址 |
| `TM-MINIMAX-QUOTA-EXHAUSTED` | 返回 JSON 失败，但 CLI 没给出额度耗尽提示 | 失败诊断层 | 递归提取嵌套 `error.message` 等文本，再识别 quota/额度关键词 | 不只看第一层 `message/error/detail`；脚本统一递归扫描响应文本叶子节点 | 额度耗尽时 `diagnostic_hint` 明确提示检查 token 余额 |
| `TM-MINIMAX-MODEL-CHANNEL-MISSING` | 默认最高版本模型返回 `model_not_found` / `No available channel for model` | 渠道路由层 | 明确提示该 token/分组暂未开通该模型，而不是静默降级 | 诊断层显式区分“额度耗尽”和“模型未上架/未分发”；默认值继续保持最高版本 | 备用 token 命中老模型可用、最新模型不可用时，CLI 明确返回渠道缺口 |
| `TM-MINIMAX-INPUT-TRIAD` | `Prompt / ImageUrl / ImageInfos` 全空仍试图提交 | 输入边界层 | 在本地先拒绝空请求 | 把“三选一至少一项”固化到脚本与主合同 | `submit --dry-run` 在三项全空时直接报错 |
| `TM-MINIMAX-FIELD-CASE` | 请求体字段改成小写，网关不认 | 协议映射层 | 恢复为文档同名字段：`Model / Prompt / ImageUrl ...` | 在脚本里统一由 builder 生成 UpperCamelCase 字段 | dry-run payload 可见字段名大小写正确 |
| `TM-MINIMAX-HAILUO-ASPECT` | 默认海螺模型带了 `AspectRatio`，接口报错或行为不稳定 | 模型能力边界层 | 去掉 `AspectRatio` 后重试 | 把“Hailuo 当前不支持 AspectRatio”固定进 validation notes 与主合同 | `Hailuo-* + --aspect-ratio` 时报告含风险提示 |
| `TM-MINIMAX-HAILUO-DEFAULT-RESOLUTION` | 调用方误以为海螺默认是 720P | 模型能力边界层 | 按文档改回“默认 768P”的认知 | 在文档、脚本提示、样例里统一写明 Hailuo 默认 `768P` | 不传 `--resolution` 时报告含默认值提示 |
| `TM-MINIMAX-REFERENCE-TYPE-SCOPE` | 在非 GV 模型上使用 `ReferenceType`，结果行为不稳定 | 模型能力边界层 | 保留提交，但在报告写风险提示 | 把“仅 GV 模型支持”固定进 validation notes | 非 GV + `ReferenceType` 时报告含提示 |
| `TM-MINIMAX-SECRET-HYGIENE` | 文档或报告中出现明文 token | 安全层 | 只在运行时拼接鉴权头，报告里脱敏 | 统一以 `.env` 的 `ANYFAST_VIDEO_API_KEY` 为真源，不回写明文 | 仓内 grep 不出现新增明文 token |
| `TM-MINIMAX-BASE-URL-DRIFT` | 平台站点被误当成 API Base URL，或文档只给相对路径导致默认 host 漂移 | 环境配置层 | 从 `MINIMAX_API_BASE_URL / ANYFAST_API_BASE_URL / FINEAPI_API_BASE_URL` 读取，并把兜底改回已验证 AnyFast 网关 | 把平台 URL、文档 URL、API 网关拆开治理，不再让 `https://www.anyfast.ai` 冒充默认 API host | 无 base_url 时本地报错或回退链可解释；有默认值时也落在真实网关 |

## Repair Playbook

1. 先跑 `submit --dry-run --print-payload`
2. 确认 `.env` 中存在 `ANYFAST_VIDEO_API_KEY`
3. 确认 `base_url` 已来自 `MINIMAX_API_BASE_URL / ANYFAST_API_BASE_URL / FINEAPI_API_BASE_URL`
4. 检查 `Prompt / ImageUrl / ImageInfos` 至少一项非空
5. 若默认海螺模型还传了 `AspectRatio`，先去掉该字段
6. 若用了 `ImageInfos.ReferenceType`，确认是否真的需要 GV 模型语义
7. 若返回只有 `id / task_id / status / created_at`，停在 create receipt，不继续脑补状态与下载

## Reusable Heuristics

- 对前端渲染型 API 文档页，如果当前能稳定确认的只有创建字段，就把技能闭环先收束到 create receipt，而不是为了“看起来完整”去发明 query/download 端点。
- 当供应商文档把字段名展示为 UpperCamelCase 时，脚本 builder 应直接输出同名字段，不要在不同层各自重新拼大小写。
- Hailuo 的关键差异不在“另一个接口”，而在同一接口下的默认值与参数边界；最稳的技能设计是保留统一创建协议，再把海螺特有的 `768P 默认值` 与 `AspectRatio 暂不支持` 写成显式提示。
- 当同一家族模型会持续涨版本时，默认值不该再写成单点常量；更稳的做法是把“家族内最高版本解析”沉到脚本真源，文档只同步当前解析结果。
- 涉及同一供应商下多套 gateway 时，密钥真源先统一，再让 provider 局部变量只做覆盖；本技能以 `ANYFAST_VIDEO_API_KEY` 为主事实源。

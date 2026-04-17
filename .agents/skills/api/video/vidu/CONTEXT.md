# Context: vidu

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

本文件作为 `vidu` 技能的经验层，默认以知识库模式维护：优先沉淀 `POST /v1/video/generations` 的 JSON 创建合同、三选一输入门槛、默认模型自动升到当前最高通用 Vidu 版本的裁决逻辑、模型边界提示、环境变量回退，以及“只到 create receipt”为止的闭环边界。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-VIDU-CREATE-ONLY` | 调用方把创建回执误当成视频成片 | 工作流契约层 | 明确当前只覆盖 create receipt | 在 `SKILL.md` 与脚本输出中显式标注“当前未覆盖状态/下载” | 报告只出现 `id/task_id/status/created_at`，不虚构下载地址 |
| `TM-VIDU-INPUT-TRIAD` | `Prompt / ImageUrl / ImageInfos` 全空仍试图提交 | 输入边界层 | 在本地先拒绝空请求 | 把“三选一至少一项”固化到脚本与主合同 | `submit --dry-run` 在三项全空时直接报错 |
| `TM-VIDU-FIELD-CASE` | 请求体字段改成小写，网关不认 | 协议映射层 | 恢复为截图同名字段：`Model / Prompt / ImageUrl ...` | 在脚本里统一由 builder 生成大写字段，不在外层重复拼装 | dry-run payload 可见字段名大小写正确 |
| `TM-VIDU-DEFAULT-MODEL-DRIFT` | 默认模型长期停留在旧版本，如 `Vidu-q2-pro` | 真源治理层 | 把默认模型改回脚本统一自动裁决 | 只允许脚本维护最高版本选择逻辑，文档/元数据仅引用当前解析结果 | `--help` 与 dry-run 中默认模型随已知型号集合同步更新 |
| `TM-VIDU-QUOTA-CHANNEL-SPLIT` | 主视频 key 返回“额度已用尽”，备用通用 key 返回 `model_not_found` | 网关能力层 | 先区分是额度阻塞还是模型通道未开通 | 脚本从嵌套错误体中提取 `quota / model_not_found` 提示，不再只给空白诊断 | 失败报告出现对应 `validation_notes` |
| `TM-VIDU-REFERENCE-TYPE-SCOPE` | 在非 GV 模型上使用 `ReferenceType`，结果行为不稳定 | 模型能力边界层 | 保留提交，但在报告写风险提示 | 把“仅 GV 模型支持”固定进 validation notes | 非 GV + `ReferenceType` 时报告含提示 |
| `TM-VIDU-ASPECT-RATIO-SCOPE` | 非 q2 模型使用 `4:3 / 3:4` 被网关拒绝 | 模型能力边界层 | 先改回 `16:9 / 9:16 / 1:1` | 把“4:3 / 3:4 仅 q2 支持”写进脚本和主合同 | 非 q2 + `4:3` 时报告含提示 |
| `TM-VIDU-OFFPEAK-SCOPE` | 非 Vidu 模型传 `OffPeak`，行为不确定 | 模型能力边界层 | 仅在 Vidu 模型上推荐使用 | 把“仅 Vidu 支持”写进 validation notes | 非 Vidu + `OffPeak` 时报告含提示 |
| `TM-VIDU-SECRET-HYGIENE` | 文档或报告中出现明文 token | 安全层 | 只在运行时拼接鉴权头，报告里脱敏 | 统一以 `.env` 的 `ANYFAST_VIDEO_API_KEY` 为真源，不回写明文 | 仓内 grep 不出现新增明文 token |
| `TM-VIDU-BASE-URL-DRIFT` | 平台站点被误当成 API Base URL，或文档只给相对路径导致默认 host 漂移 | 环境配置层 | 从 `VIDU_API_BASE_URL / ANYFAST_API_BASE_URL / FINEAPI_API_BASE_URL` 读取，并把兜底改回已验证 AnyFast 网关 | 把平台 URL、文档 URL、API 网关拆开治理，不再让 `https://www.anyfast.ai` 冒充默认 API host | 无 base_url 时本地报错或回退链可解释；有默认值时也落在真实网关 |

## Repair Playbook

1. 先跑 `submit --dry-run --print-payload`
2. 确认 `.env` 中存在 `ANYFAST_VIDEO_API_KEY`
3. 确认 `base_url` 已来自 `VIDU_API_BASE_URL / ANYFAST_API_BASE_URL / FINEAPI_API_BASE_URL`
4. 检查 `Prompt / ImageUrl / ImageInfos` 至少一项非空
5. 若用了 `ImageInfos.ReferenceType`，确认是否真的需要 GV 模型语义
6. 若用了 `4:3 / 3:4`，确认模型是否属于 `Vidu-q2` 系列
7. 若返回只有 `id / task_id / status / created_at`，停在 create receipt，不继续脑补状态与下载

## Reusable Heuristics

- 对前端渲染型 API 文档页，如果当前能稳定确认的只有创建字段，就把技能闭环先收束到 create receipt，而不是为了“看起来完整”去发明 query/download 端点。
- 当供应商文档把字段名展示为 UpperCamelCase 时，脚本 builder 应直接输出同名字段，不要在不同层各自重新拼大小写。
- 类似 `Prompt / ImageUrl / ImageInfos 至少一项` 这种互斥/并列输入门槛，最稳的做法是写成单一布尔判定，而不是分散到多个 if 里。
- 默认模型如果需要“总是跟最高版本走”，就不能在 `SKILL.md`、参考摘要和入口元数据里分别写死字面量；应由脚本单点解析，其他载体只引用当前解析结果。
- 当同一网关下的主视频 key 与通用 key 返回不同失败型（例如一个是 quota，一个是 model_not_found），不要把它们混成一个问题；前者是额度层，后者是渠道开通层。
- 对“仅某模型支持”的字段，第一选择不是本地硬拒，而是保留提交能力并写清 validation note；这样既不堵死代理兼容，也不掩盖边界。
- 涉及同一供应商下多套 gateway 时，密钥真源先统一，再让 provider 局部变量只做覆盖；本技能以 `ANYFAST_VIDEO_API_KEY` 为主事实源。

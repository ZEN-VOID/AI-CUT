# Context: kling

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

本文件作为 `kling` 技能的经验层，默认以知识库模式维护：优先沉淀 FineAPI Kling 的页面漂移、默认模型自动前移到最高版本的覆写规则、`image/image_tail` 二选一约束、以及查询结果中 `task_result` 结构漂移下的媒体 URL 提取策略。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-KLING-PAGE-DRIFT` | 调用或维护时继续引用 `403045611e0` | 真源映射层 | 改回 `422568253e0 / 403045624e0 / 403045626e0` | 在 `SKILL.md` 与 `references/api.md` 固定写明 2026-04-17 页面映射 | 技能文档不再把 Veo 页当 Kling |
| `TM-KLING-DEFAULT-MODEL` | 脚本或文档仍把默认模型写死在旧版本，或新增高版本后默认值没有前移 | 默认值治理层 | 改回父级 `../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族 | 让脚本通过 `../shared/default_model_policy.py` 负责共享骨架，子技能文档只声明 Kling 的排序差异与当前解析结果 | `--help`、dry-run 请求体和入口文案都显示当前最高版本 |
| `TM-KLING-ANYFAST-SHARED-ENV` | 同系列技能已统一走 AnyFast，但 `kling` 仍只读取自有 env 键或让 `KLING_*` 抢在共享网关前面 | 环境回退层 | 把 `ANYFAST_VIDEO_API_KEY / ANYFAST_API_KEY / ANYFAST_API_BASE_URL` 作为 `kling` 的主回退链 | 在脚本、技能合同、参考文档里同步声明 AnyFast 体系优先级，`KLING_*` 只作局部覆盖 | 与 `seedance / veo / vidu / minimax` 共用同一套 AnyFast env 时可直接运行 |
| `TM-KLING-WRONG-HOST-INFERENCE` | 参考了 `grok` 的历史报告把 `https://ai.ai666.net` 当成 `kling` 真正 host | 真源映射层 | 回到同系列已跑通技能与 AnyFast env，把 Base URL 改回 `ANYFAST_API_BASE_URL=https://fw2afus.ent.acc.kurtisasia.com` | 以后优先以上游 AnyFast env 和同系列成功报告为真源，不再用跨 provider 历史 host 反推 | `kling` 的真实请求 host 与 `seedance` 成功链路对齐 |
| `TM-KLING-QUOTA-AUTH-SPLIT` | AnyFast `kling` 真实请求报 401，但实际错误文本是“令牌额度已用尽” | 诊断分流层 | 从响应文本中拆分额度/配额与纯鉴权两类提示 | 在脚本里把 `quota / RemainQuota / 额度` 识别为余额问题，避免只返回笼统鉴权提示 | 报告中的 `diagnostic_hint` 能明确指出是额度不足而非 host/path 错误 |
| `TM-KLING-MEDIA-NORMALIZE` | 本地图片路径原样塞进 JSON 导致接口不认 | 输入归一层 | 本地文件转成裸 Base64；data URL 去掉前缀 | 统一媒体归一函数，覆盖 `image / image_tail / mask` | dry-run 请求体不再出现本地路径 |
| `TM-KLING-STALE-HARD-CONSTRAINT` | 文档或脚本把旧经验误写成当前接口硬限制 | 规范同步层 | 回退到当前接口真源，删除无证据的硬限制 | 只有当当前真源明确写出时，才能把经验升级为本地硬校验 | 合同与脚本不再保留 `image_tail => duration=5` 之类的旧限制 |
| `TM-KLING-MULTI-SHOT` | `multi_shot=true` 时缺 `shot_type` 或 `multi_prompt` | 高级字段依赖层 | 按 `shot_type` 校验 `prompt` / `multi_prompt` | 在技能合同写清依赖；脚本做本地硬校验 | customize 模式无 `multi_prompt` 直接失败 |
| `TM-KLING-VOICE-ELEMENT-MUTEX` | `element_list` 与 `voice_list` 同时传导致服务端拒绝 | 字段互斥层 | 本地禁止两者同时存在 | 在脚本与 `references/api.md` 同步写互斥关系 | 同时传两组字段时本地即失败 |
| `TM-KLING-CONTROL-GROUP-MUTEX` | `image_tail`、mask、camera_control 混用导致服务端拒绝 | 高级控制互斥层 | 本地按控制组互斥提前拒绝 | 在文档和脚本同时声明三组互斥，不再依赖调用者自行记忆 | 多组控制同时启用时本地即失败 |
| `TM-KLING-MODEL-FEATURE-GATE` | `cfg_scale` 或 `sound` 与模型版本不匹配 | 特性门槛层 | 依据模型版本做本地校验 | 把 `cfg_scale` / `sound` 的支持矩阵写入 `SKILL.md` 和脚本 | 不支持的模型组合在提交前就失败 |
| `TM-KLING-QUERY-SHAPE` | 查询页 200 了，但状态字段提取失败 | 响应规范化层 | 优先读取 `code/data/task_status/task_result`，保留原始 JSON | 把状态规范化与原始响应并存，避免只剩错 schema | `status` 报告同时含 `normalized_status` 与 `raw_response` |
| `TM-KLING-ASSET-URL` | 查询成功，但下载阶段拿不到视频 URL | 结果提取层 | 在 `task_result.videos[].url` 之外增加回退路径 | 保持多路径提取函数，并在报告里输出 `asset_url_paths_tried` | 完成态可在报告中看到提取到的 URL 或尝试路径 |

## Repair Playbook

1. **先看页面 ID**
   - 先确认当前维护的是 `422568253e0 / 403045624e0 / 403045626e0`
   - 不是 `403045611e0`
2. **先跑 dry-run**
   - `submit --dry-run --print-payload`
   - 重点看 `model_name / mode / duration / image_summary`
3. **创建失败先查输入归一**
   - 本地图应已转裸 Base64
   - 远程图应保留 URL
4. **查询失败先查 action2**
   - 本技能固定 `videos/image2video`
   - 不要误用 `text2video`
5. **下载失败先查 task_result**
   - 优先看 `videos[].url`
   - 再回退看 `video.url / assets[].url / images[].url`

## Reusable Heuristics

- FineAPI 同一模型族经常出现“旧页 + 新页并存”，最稳的做法不是让 `SKILL.md / references / openai.yaml` 各自解释默认值，而是回到父级 runbook，再由脚本共享 helper 解析当前最高版本。
- 当用户给的文档页和截图冲突时，先按截图主题定位真实页面，再把“错页映射”写进技能真源，避免后续重复踩坑。
- 图生视频这类 JSON 接口如果支持 Base64，就应该优先把本地文件归一成裸 Base64，而不是要求调用者手工预处理。
- 查询页没有独立下载端点时，`download` 子命令就应当围绕查询结果中的 URL 工作，不要为追求和别的 provider 一致而虚构 `/content`。
- 经验性限制只有在当前真源仍明确出现时，才可以升级成脚本硬校验；旧页面、旧实验或“之前踩坑”不足以单独构成当前合同。
- 同系列视频 provider 若已有 `seedance / veo / vidu / minimax` 等成功链路，应优先以 `ANYFAST_API_BASE_URL` 为真源，不要再用别的 provider 历史 host 做类推。
- AnyFast 系列若返回 `401`，不能立刻等同于“token 错”；先看错误文本，`RemainQuota`、`额度已用尽` 一类信号应归到余额问题。

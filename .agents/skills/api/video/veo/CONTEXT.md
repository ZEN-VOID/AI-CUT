# Context: veo

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

本文件作为 `veo` 技能的经验层，默认以知识库模式维护：优先沉淀 `/v1/video/create` 的 JSON 契约、文生/图生统一端点、模型枚举漂移、布尔字段漂移，以及“创建回执 != 成片结果”的执行认知。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-VEO-ENDPOINT-DRIFT` | 技能仍在调用 `/v1/videos` 或继续讲 `input_reference` | 源层合同漂移 | 统一切回 `POST /v1/video/create` + JSON | 在 `SKILL.md` / `references/api.md` / 脚本三处同时移除旧端点真源地位 | dry-run 的 URL 只出现 `/v1/video/create` |
| `TM-VEO-JSON-SHAPE` | 仍按 multipart 上传或继续读本地文件为 `input_reference` | 请求构造层 | 固定 `application/json`，并只接受 `images: array[string]` | 在脚本前置校验中拦截本地路径，防止旧调用方式回流 | `request_summary.data.images` 始终是数组或缺省 |
| `TM-VEO-CREATE-ONLY` | 调用方把创建回执误当成状态查询或下载完成 | 工作流契约层 | 明确当前闭环只到 create receipt | 在 `SKILL.md` 与脚本输出中显式标注“当前未覆盖状态/下载” | 报告只出现 submit receipt，不虚构下载地址 |
| `TM-VEO-RESPONSE-DRIFT` | 同一端点出现两套响应格式，调用方只按单一 schema 解析导致丢字段 | 响应规范化层 | 同时保留 `raw_response` 与最小规范化字段 | 在脚本中只做最小抽取，不强推单一固定响应 schema | 报告同时含 `raw_response` 与 `normalized_submit` |
| `TM-VEO-CHINESE-PROMPT` | 中文 prompt 提交后供应商报提示词问题或效果偏差 | Prompt 约束层 | 显式传 `--enhance-prompt true` | 在技能合同里把“中文 prompt 建议显式开启 enhance_prompt”写成固定提醒 | 中文 prompt 的 dry-run 含 `enhance_prompt: true` |
| `TM-VEO-ASPECT-RATIO-VEO3` | 非 `veo3*` 模型也发送 `aspect_ratio`，被网关拒绝 | 参数边界层 | 仅在 `veo3*` 模型上发送 `aspect_ratio` | 在脚本校验中把该约束前置为硬错误 | `veo2-fast --aspect-ratio 16:9` 直接本地失败 |
| `TM-VEO-BOOL-DRIFT` | `enable_upsample / enhance_prompt` 在文生与图生页的必填性不一致，导致误判 | 文档契约层 | 脚本允许显式传 `true/false`，不偷偷补值 | 在 `references/api.md` 记录“可选/必填”双重信号，避免单边固化 | dry-run 可清楚看到这两个字段是否被发送 |
| `TM-VEO-DEFAULT-MODEL-DRIFT` | 默认模型仍停在旧值，不能自动前移到当前最高版本 | 默认值治理层 | 改回父级 `../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族 | 共享算法骨架只保留在 `../shared/default_model_policy.py`；Veo 子技能只声明“排除 `frames / components` 变体”这一 provider 特有过滤条件与当前解析结果 | `--help` / dry-run 在未显式传 `--model` 时落到当前最高结果 `veo3.1-pro` |
| `TM-VEO-ENV-FALLBACK-DRIFT` | `.env` 里 `VEO_* / FINEAPI_*` 为空，但仓库统一的 `ANYFAST_*` 实际有值，导致脚本误报缺 Key/Base URL | 环境回退链治理层 | 把 Veo 的 env 查找补齐到 `ANYFAST_VIDEO_API_KEY / ANYFAST_API_KEY / ANYFAST_API_BASE_URL` | 让 `veo` 与同类视频技能共享同一回退链基线，并在合同里写明优先级 | 在仅配置 `ANYFAST_*` 的环境下真实提交不再被本地前置校验拦住 |
| `TM-VEO-ENDPOINT-FAMILY-DRIFT` | 当前 host 对 `/v1/video/create` 返回 `Invalid URL`，但 `/v1/video/generations` 实际可达，技能仍卡死在旧路径 | 端点族治理层 | 在 `submit_path=auto` 下，当主路径返回 `Invalid URL` 时自动回退到 `/v1/video/generations` | 在脚本、`SKILL.md`、`references/api.md` 三处同步记录“显式 Veo host 优先 create，AnyFast host 可回退 generations” | live report 中出现 `attempts[]`，可看到 create 404 后自动切到 generations |

## Repair Playbook

1. **先做 Dry Run**
   - 运行 `submit --dry-run --print-payload`
   - 先确认 `base_url / model / prompt / images / enable_upsample / enhance_prompt / aspect_ratio`
2. **先看端点和头**
   - URL 必须是 `/v1/video/create`
   - 头必须是 `application/json`
3. **再看图片输入**
   - `images` 只接受公网 `http/https` URL
   - 若是本地文件，先走上游上传流程取得 URL
4. **再看模型与比例**
   - `aspect_ratio` 只给 `veo3*`
   - 帧模型、组件模型若传图数量越界，先按当前材料给出的显式上限回退
5. **最后看回执解释**
   - 创建成功只代表任务已创建
   - 没有新的状态/下载文档前，不要承诺成片位置

## Reusable Heuristics

- 当同一供应商接口从旧的 multipart 上传切到 JSON URL 数组时，优先把旧输入方式从真源层彻底降级，而不是做“双栈默认兼容”；否则旧合同会反复回流。
- 如果用户给了比本地技能更新的字段表，优先按用户契约重建源层，不要让旧 `references/` 继续主导实现。
- 当同一创建端点出现两套响应示例时，最稳的策略是“原始体全保留 + 最小规范化抽取”，而不是抢先定义新的强 schema。
- `aspect_ratio` 这类带模型家族条件的字段，必须在本地校验里前置，不要等供应商拒绝后再追因。
- 文档把布尔字段一处写可选、一处写必填时，脚本层应支持显式透传 `true/false`，并把是否发送该字段写进 dry-run 报告，便于人工核对。
- “默认模型总是前移到最高版本”不能简单按字符串或全量枚举取最大值；正确做法是先回到父级共享 runbook 的 `highest-available-general` 规则族，再由 Veo 子技能补上“排除 `frames / components` 变体”的本地过滤条件。
- 当同仓库的多个视频技能已经统一收敛到 `ANYFAST_*` 为主事实源时，新补的 provider skill 不能只查 provider 私有键或空置的 `FINEAPI_*`；否则看起来像“用户没配环境”，实际上是源层回退链掉队。
- 当网关已经明确返回 `Invalid URL` 时，不要继续把“文档写的是这个路径”当作唯一真相；应把 live gateway behavior 视为当前环境的一手证据，并在 `auto` 模式里最小化回退到已验证可达的同族端点。

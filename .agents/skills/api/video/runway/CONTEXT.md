# Context: runway

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

本文件作为 `runway` 技能的经验层，默认以知识库模式维护：优先沉淀 FineAPI Runway 创建页、官方 Runway 任务模型、代理前缀推导、图片输入归一化、模型比例漂移与成片 URL 下载。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-RUNWAY-PROXY-TASK-PATH` | 创建成功但状态查询 404 | 代理路径契约层 | 先核对是否应走 `/runwayml/v1/tasks/{id}` | 在 `references/api.md` 显式标记“该路径来自官方 Runway 任务模型 + 代理前缀推导” | `status --task-id ...` 能返回任务状态或清晰 404 诊断 |
| `TM-RUNWAY-LOCAL-IMAGE` | 本地图片路径直接塞进 `promptImage`，接口拒绝 | 输入归一化层 | 将本地图转成 Data URI | 脚本统一图片归一化：HTTPS URL 保留，Data URI 透传，本地图转 Data URI | `submit --dry-run` 中 `promptImage` 为 Data URI 而不是本地路径 |
| `TM-RUNWAY-RATIO-DRIFT` | `gen4_turbo + 1280:768` 是否合法出现冲突信息 | 文档漂移层 | 不直接硬拒，先记录 `validation_notes` | 把 FineAPI 示例和官方 Runway ratio 表同时写入参考文档，脚本只做提示不做误杀 | 报告里能看到漂移提示 |
| `TM-RUNWAY-DEFAULT-COUPLING` | 默认模型升级后，默认 ratio 仍停留在旧组合，导致“不传 ratio 的默认请求”自相矛盾 | 默认参数层 | 让 `ratio` 默认值按 `model` 动态补齐 | 默认模型不再硬编码单点；脚本统一从模型集合推导当前最高版本，并给每个已知模型绑定自洽默认 ratio | 不传 `--ratio` 时，请求体里的 `model` 与 `ratio` 组合仍落在官方支持表内 |
| `TM-RUNWAY-OUTPUT-FIELD-DRIFT` | 任务完成后字段不只 `output[]`，还可能出现 `video / video_raw` | 输出兼容层 | 下载逻辑兼容多种视频 URL 字段 | `download` 先查 `output[]`，再回退 `video / video_raw / video_url` | 成功任务能稳定下载成片 |
| `TM-RUNWAY-SECRET-HYGIENE` | 技能文档或报告里出现明文 token | 安全层 | 文档只保留环境变量名，报告里脱敏 Authorization | 统一以 `.env` 的 `ANYFAST_VIDEO_API_KEY` 为真源，不回写明文密钥 | 仓内 grep 不出现新增明文 token |
| `TM-RUNWAY-TERMINAL-STATE` | 任务完成但轮询一直不停，或失败状态被当成 pending | 状态机层 | 明确区分 `pending/running/processing` 与 `SUCCEEDED/FAILED/CANCELED` | 在脚本中统一状态规范化，并把终态集合放成显式常量 | `run` 能在成功或失败终态退出，而不是无限轮询 |
| `TM-RUNWAY-UTCNOW-DEPRECATION` | dry-run 报告生成时触发 `datetime.utcnow()` 弃用警告 | Python 运行时兼容层 | 改成 `datetime.now(timezone.utc)` | 所有时间戳默认使用时区感知 UTC 写法，避免 Python 3.12+ 兼容性回退 | dry-run 不再输出弃用警告 |
| `TM-RUNWAY-HTML-200` | `submit/status` 返回 HTTP 200，但其实是 AnyFast 前端 HTML，`task_id` 为空，`run` 路径继续盲轮询 | 网关路由层 | 把非 JSON 或缺 `task_id` 的响应直接判为失败 | 对 Runway 技能移除 `ANYFAST_API_BASE_URL` 的真实请求默认回退，并在脚本中加入 HTML/JSON/task_id 三重 gate | 真实请求若回 HTML，CLI 立即非零退出，不再出现 `task_id=null` 的伪成功 |

## Repair Playbook

1. **先做 Dry Run**
   - 运行 `submit --dry-run --print-payload`
   - 先确认 `promptImage / model / duration / ratio / base_url`
2. **再查图片输入**
   - HTTPS URL：确认是 `https://` 而不是 `http://`
   - Data URI：确认以 `data:image/` 开头
   - 本地图：确认脚本已转成 Data URI
3. **模型比例排查**
   - 用户给的 FineAPI 示例可先按原样提交
   - 若代理拒绝，再改用官方 Runway 文档推荐的 ratio 重试
4. **先查 Base URL 是否是 Runway 专用**
   - 真实请求优先使用 `RUNWAY_API_BASE_URL / FINEAPI_API_BASE_URL`
   - 若当前只有 `ANYFAST_API_BASE_URL`，先补专用 Base URL，再做真实提交
5. **状态路径排查**
   - 默认走 `/runwayml/v1/tasks/{id}`
   - 若 404，先认定是“代理路径未明示或未开放”，而不是立刻改 prompt
6. **下载排查**
   - 先看 `output[]`
   - 再看 `video / video_raw / video_url`
   - 最后检查 URL 是否已过期

## Reusable Heuristics

- 代理页只展示创建接口时，不要把后续查询路径包装成“页面已明示”；应明确标成兼容推导。
- 对接图片首帧接口时，本地图转 Data URI 往往比临时上传到公网更稳，尤其适合 dry-run 与本地脚本工作流。
- 供应商示例与官方文档冲突时，最稳的策略通常不是硬拒其中一方，而是“允许提交 + 显式警告 + 失败后回退到官方推荐组合”。
- 默认值升级不能只改 `model` 一个字段；凡模型与比例存在耦合，必须同步把 `ratio` 默认值改成按模型动态推导，否则默认请求本身就是脏的。
- 对 Runway/FineAPI 这类代理接口，HTTP 200 不是成功的充分条件；必须同时检查 `Content-Type`、JSON 可解析性和 `task_id` 等关键字段。
- 视频任务完成后的下载字段常会漂移；脚本层应优先兼容多个候选视频 URL 字段，而不是把单一字段当绝对真源。
- 对带子命令的 CLI，`submit/status/download/run` 都应生成结构化报告，这样路径漂移或字段漂移时更容易定位根因。
- 在 Python 3.12+ 环境下，dry-run 或报告脚本不要再用 `datetime.utcnow()`；统一改为时区感知 UTC 时间，能少掉一类无意义告警。
- 对 Runway 图生视频，当前官方文档可见的最高版本默认位应视为 `gen4.5`；只有当官方文档新增更高版本且模型集合同步更新后，默认值才应再次抬升。
- 当某个视频 provider 尚未验证通用 `ANYFAST_API_BASE_URL` 路由时，不要沿用其他技能的通用 host 回退链；应要求 provider 专用 Base URL 或显式 `--base-url`。

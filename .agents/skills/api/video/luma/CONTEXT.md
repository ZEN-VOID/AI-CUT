# Context: luma

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

本文件作为 `luma` 技能的经验层，默认以知识库模式维护：优先沉淀 FineAPI Luma 创建字段映射、官方 Luma generation 轮询模型、查询路径推断边界、视频 URL 抽取兼容，以及 `.env` 密钥回退顺序。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-LUMA-FIELD-MAP` | 创建接口报字段缺失或参数非法 | 请求契约层 | 把创建字段改回 `user_prompt / model_name` | 在 `SKILL.md` 与脚本中双重固定 FineAPI 命名，避免把官方 `prompt/model` 直接透传到 FineAPI 创建口 | `submit --dry-run` 中请求体字段名正确 |
| `TM-LUMA-BASE-URL-DRIFT` | `.env` 里只有 `ANYFAST_API_BASE_URL`，Luma 请求却拿到 HTML 首页或 `Invalid URL` | 环境配置层 | 改为显式配置 `LUMA_API_BASE_URL / FINEAPI_API_BASE_URL`，不要默认吃通用 AnyFast host | 对 Luma 技能移除 `ANYFAST_API_BASE_URL` 的默认回退；若只检测到通用 host，就在本地直接报错 | 没有 Luma/FineAPI Base URL 时，本地 fail-fast；错误信息明确指向配置层 |
| `TM-LUMA-HTML-200` | `submit/status` 收到 HTTP 200，但返回体其实是前端 HTML 页面 | 网关路由层 | 把该响应判为失败，而不是当作成功回执 | 在脚本里增加 generation JSON 结构校验；只有命中 generation 字段集合才允许进入成功分支 | 真实请求若回 HTML，CLI 退出非零并给出 Base URL/路由诊断 |
| `TM-LUMA-STATUS-PATH` | 创建成功但 `status` 阶段 404/405 | 路由兼容层 | 显式覆盖 `--status-path-template` 或先停在 create receipt | 把“官方轮询模型已确认，但 FineAPI 查询路径是镜像推断”写进合同，并保留模板可覆盖能力 | 默认模板失配时，用户可用 CLI 覆盖继续验证 |
| `TM-LUMA-VIDEO-URL` | 状态已完成但脚本拿不到成片 | 响应兼容层 | 同时检查 `video / video_raw / assets.video` | 把成片抽取逻辑集中到单一 helper，而不是在多个命令里散写字段判断 | `download` 能从至少一种返回形态拿到 MP4 |
| `TM-LUMA-DURATION-5S` | 传入其他时长后供应商拒绝 | 供应商边界层 | 当前固定回退到 `5s` | 在 `SKILL.md`、参考文档与 CLI 枚举中统一写死 `5s` 边界，防止样例与脚本漂移 | `--duration 5s` 可过，其他值直接被本地校验拦截 |
| `TM-LUMA-MODEL-ALIAS` | `ray-2` 或 `ray-v2` 在某些网关下不被接受 | 模型漂移层 | 默认先发脚本自动解析出的最高 Ray 版本（当前为 `ray-2`），再回退 `ray-v2`；旧模型链路继续保留 `ray-v1 -> ray-1.6` | 把“最高版本解析规则”与“代理旧别名”同时沉到脚本和 references，避免默认值再次散落成硬编码 | 默认名失败后别名候选可继续尝试 |
| `TM-LUMA-SECRET-HYGIENE` | 报告或技能文件出现明文 token | 安全层 | 只在运行时拼接鉴权头，报告里统一脱敏 | `.env` 作为密钥单一事实源；技能合同和报告只保留变量名与 `Bearer ***` | 仓内 grep 不出现新增明文 token 泄露 |
| `TM-LUMA-IMAGE-URL-ONLY` | 把本地路径传给 `image_url` / `image_end_url` 导致网关不认 | 输入边界层 | 当前只接受远程 URL | 在 CLI 前置校验中直接拦截非 `http/https` 输入，避免“看起来提交成功但服务端不认” | `--image-url ./foo.png` 直接报错 |

## Repair Playbook

1. **先做 Dry Run**
   - 运行 `submit --dry-run --print-payload`
   - 先确认 `base_url / model_candidates / resolution / duration / image_url / image_end_url`
2. **先查 Base URL 是否是 Luma 专用**
   - 优先使用 `LUMA_API_BASE_URL / FINEAPI_API_BASE_URL`
   - 若当前只有 `ANYFAST_API_BASE_URL`，先补专用 Base URL，再做真实提交
3. **再查字段映射**
   - 创建请求必须是 `user_prompt / model_name`
   - 若看到 `prompt / model`，说明误混了官方字段
4. **再查响应结构**
   - 若 HTTP 200 但返回的是 HTML 壳页，不得视为成功
   - 这通常意味着 Base URL 错位、路由未开，或网关把未知路径回退到了前端页面
5. **再查查询路径**
   - 默认模板是 `/luma/generations/{id}`
   - 若 404/405，优先判断网关是否未镜像该路径，而不是立刻改 prompt
6. **再查视频 URL**
   - 先看 `video`
   - 再看 `video_raw`
   - 再看 `assets.video`
7. **最后查模型与时长**
   - 先用 `ray-2 + 5s + 720p`
   - 模型报错时再回退 `ray-v2`
8. **观察 run 的实时进度**
   - `run` 现在会把 `generation_id` 与每轮 `state` 打到 `stderr`
   - 若长时间停在 `pending / dreaming / processing`，优先判定为远端排队而不是本地卡死
   - 时长不要超出 `5s`

## Reusable Heuristics

- 当代理网关重写了官方字段名时，最容易坏的是“官方文档记忆”压过了代理层真实请求体；把字段映射收口到脚本 helper 和参考文档里，比在样例里零散提醒更稳。
- 当官方模型命名已经切到 `ray-2`，而代理样例还停留在 `ray-v2` 时，默认值应优先跟随“已登记模型中的最高版本”，兼容性靠 alias fallback 兜底，而不是继续把旧别名写成默认真源。
- 当某个视频供应商的真实路由尚未在通用 AnyFast host 上被确认时，宁可要求显式 `LUMA_API_BASE_URL / FINEAPI_API_BASE_URL`，也不要沿用别的技能的通用网关回退链。
- 只要官方文档确认“create 返回 id，video 需靠 polling 拿”，就应该优先把技能设计成异步三段式；即便代理层查询路径还没百分百锁死，也要把“路径可覆盖”作为合同的一部分。
- 对 generation 对象，视频地址往往不是永远稳定在同一个字段；把 URL 抽取逻辑写成多分支兼容，比要求用户记忆不同网关差异更可靠。
- 如果用户明确要求统一引用 `.env` 的通用视频 key，可以把该变量放进回退链，但不要因此抹掉更贴近供应商的专用变量名。

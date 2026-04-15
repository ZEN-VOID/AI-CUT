# Context: nano-banana (API 契约层)

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
last_checked_at: 2026-03-20T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `nano-banana` **API 契约层**的经验层，聚焦 AnyFast 原生 Gemini 接口的请求构造、参考图 `inline_data` 转译、默认值注入策略、并发调度与响应解析。应用层经验（换脸/换装/多视图等）由各子技能的 `CONTEXT.md` 独立维护。

## 子技能索引

| 子技能 | CONTEXT 路径 | 经验聚焦 |
|--------|-------------|----------|
| general | `general/CONTEXT.md` | 通用 T2I/I2I prompt 技巧 |
| face-swap | `face-swap/CONTEXT.md` | 身份锁定/服装锁定 |
| costume-swap | `costume-swap/CONTEXT.md` | 身份保持/服装还原 |
| multiview-character | `multiview-character/CONTEXT.md` | 三栏布局/身份一致性 |
| multiview-scene | `multiview-scene/CONTEXT.md` | 九宫格/空镜头护栏 |
| multiview-prop | `multiview-prop/CONTEXT.md` | 三栏布局/空场景护栏 |

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-DXJ2-DEFAULTS-MISSING` | 未指定比例/清晰度时请求体缺少 `aspectRatio` 或 `imageSize` | 默认值逻辑层 | 在脚本中强制补齐 `16:9 / 4K` | 保持 `FIELD-DXJ2-02` 与脚本常量同源 | `--dry-run --print-payload` 中能看到 `16:9 / 4K` |
| `TM-DXJ2-ENV-DRIFT` | 技能文档、脚本与真实端点不一致 | 环境配置层 | 统一从根目录 `.env` 读取 `ANYFAST_API_BASE_URL / ANYFAST_API_KEY / DXJ2_DEFAULT_MODEL` | 把端点与模型的单一事实源收口到 `.env` | 报告中的 `api_url` 与 `.env` 一致 |
| `TM-DXJ2-OUTPUT-PATH` | 产物落到固定 `5-API` 根目录，忽略调用方 skill 的运行时路径 | 输出路由层 | 改为 `output_dir > input_json.output_dir > caller_skill 推导 > general 兜底` | 由脚本集中维护 caller-skill 路径解析，测试/临时任务仅作为项目名兜底 | 报告中的 `caller_skill / episode_id / output_dir` 与调用方合同一致 |
| `TM-DXJ2-TASK-KIND-PRECEDENCE` | `input_json.task_kind=project` 被 CLI 默认 `test` 覆盖，导致报告元数据漂移 | 输入优先级层 | 取消 CLI parser 的 `task_kind` 默认值，让 `input_json.task_kind` 先参与解析 | 固化优先级：显式 CLI > input_json > 缺省 `test` | `--input-json` 单独运行时 report 保留 JSON 内的 `task_kind` |
| `TM-DXJ2-BATCH-SERIAL` | 明明给了多个任务，但脚本仍一张一张串行执行 | 调度层 | 把 `--input-json` 扩展为支持对象数组 / `tasks[]`，任务数 `>1` 时自动并发执行 | 在脚本与 `SKILL.md` 同步固化“默认最大并发 100、硬上限 100”的同源合同 | 多任务运行时出现批量汇总报告，且 `effective_max_concurrent <= 100` |
| `TM-DXJ2-SHAPE-MISMATCH` | 仍沿用旧版 `ratio / quality` 或 `images[].url` 直传，接口报错 | 请求体结构层 | 改为 `contents.parts + generationConfig.imageConfig` | 在技能合同和脚本中固定原生格式 | payload 中仅出现原生字段 |
| `TM-DXJ2-RESPONSE-CAMELCASE` | 请求成功但报告里没有图片文件，`candidate_count=1` 且 `finishReason=STOP` | 响应解析层 | 同时兼容解析 `inlineData/mimeType` 与 `inline_data/mime_type` | 把响应解析写成 camelCase + snake_case 双兼容 | 成功调用后 `saved_files` 非空 |
| `TM-DXJ2-INLINE-DATA` | 参考图输入后接口无法识别 | 参考图转译层 | 先下载/读取图片，再转 `inline_data` | 统一通过 `_coerce_image_part` 处理所有图源 | payload 中每张参考图都有 `mime_type + data` |
| `TM-DXJ2-EXTENSION-DRIFT` | 落盘文件后缀与真实图片 MIME 不一致，导致 `.png` 文件实际是 JPEG | 输出落盘层 | 按接口真实返回的 MIME 统一校正落盘后缀 | 显式文件名与自动命名都走同一个 MIME->extension 归一化函数 | `file <产物>` 的类型与文件后缀一致 |
| `TM-DXJ2-BASE64-HANDOFF` | 下一环节引用生成结果或执行二改时，错误地改走本地文件 / URL / 二次转码，导致下游输入不稳定 | 下游交接层 | 把 AnyFast 返回图像视为 `BASE64` 主形态，直接原样传入下一环节 | 在跨阶段交接约定中固定“生成结果优先按 `BASE64` 透传，不强制改写为其他载体” | 下游请求体直接携带上游返回的 `BASE64` 图像数据 |
| `TM-DXJ2-TRACEABILITY` | 成功或失败后无法复盘文本/图片响应 | 输出报告层 | 记录 `response_texts / finish_reasons / saved_files / error` | 统一写出 `nano_banana_report_*.json` | 报告字段完整 |
| `TM-DXJ2-NO-REPORT` | 面板批量调用默认不需要 report，但 CLI/脚本仍强依赖 report 文件存在 | 输出合同层 | 新增 `--no-report` 并让返回结果/控制台输出可独立追踪 | 在技能合同与调用方统一“report 可选、返回结果必可定位” | `--no-report` 下无 report 文件但结果仍可判定 |
| `TM-DXJ2-DRYRUN-REF-FETCH` | `--dry-run` 仍真实下载 URL / 读取参考图，导致“只验 payload”被外部图源阻塞 | dry-run 预检层 | dry-run 改为生成占位 `inline_data`，不触发真实图源读取 | 在 API 契约中明确“dry-run 验结构，不解引用参考图” | 带 `images[]` 的 `--dry-run --print-payload` 可直接通过 |
| `TM-DXJ2-PAYLOAD-413` | I2I 请求带多张 8MB 级参考图时直接报 `413 Request Entity Too Large` | 请求体预算层 | 在桥接层对超大参考图做内存缩边/压缩，再写入 `inline_data` | 把“超大图入模前预算收缩”固化到脚本与 `SKILL.md`，并在 report 中记录 `image_budget / image_part_stats` | 同一批参考图重跑时不再因请求体过大被 AnyFast 拒绝 |
| `TM-DXJ2-SECRET-LOG` | HTTP 重试或失败日志把 `key=...` 的完整 API URL 打印出来 | 安全日志层 | 对异常字符串、HTTP body、report error 与 pending retry error 统一脱敏 | 在脚本与 `SKILL.md` 固化“日志/报告不得写出 key、Bearer、sk-* 原文” | 构造含 `key=sk-...` 的错误字符串时，输出只保留 `<redacted>` |

## Repair Playbook

1. 先跑：
   - `python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py --prompt "test" --dry-run --print-payload`
2. 先核查 `.env`：
   - `ANYFAST_API_BASE_URL=https://fw2afus.ent.acc.kurtisasia.com`
   - `DXJ2_DEFAULT_MODEL=gemini-3.1-flash-image-preview`
3. 核查输出路径：
   - 先看是否传了 `--output-dir` 或 `input_json.output_dir`
   - 再看是否传了 `caller_skill / episode_id`
   - 再看 `task_kind` 是否遵循“显式 CLI > input_json > 默认 test”
   - `general` 直调默认应进入 `output/影片/[项目名]/5-API/image/nano-banana/general/`
   - `4-Design/2-设计` 系若显式传 `--output-dir + --output-filename`，应遵循调用方同目录同名策略；未显式传时才进入 `projects/aigc/<项目名>/.../generated/`
   - `task_kind=test` 且未传项目名时应映射到 `测试`
   - `task_kind=temp` 且未传项目名时应映射到 `临时`
4. 核查默认值：
   - 未显式传参时，`aspectRatio` 必须是 `16:9`
   - 未显式传参时，`imageSize` 必须是 `4K`
5. 核查多任务调度：
   - `--input-json` 若为对象数组或包含 `tasks[]`，必须自动进入并发模式
   - 默认 `--max-concurrent` 为 `100`
   - 实际执行并发必须 `<=100`
   - 未启用 `--no-report` 时，多任务结束后必须存在 `nano_banana_batch_report_*.json`
6. 若报参数错误：
   - 先看是否仍使用旧字段名
   - 再看 `imageSize` 是否为大写 `K`
7. 若参考图异常：
   - 检查输入是否成功转成 `inline_data`
   - 检查 `mime_type` 是否匹配真实图片类型
8. 若输出异常：
   - 检查报告 JSON 是否已写入 `response_texts / error.http_body`
   - 若显式使用 `--no-report`，改为检查返回结果与控制台日志，而不是期待 report 文件
   - 若图片能打开但素材系统识别异常，继续用 `file <产物>` 交叉检查二进制类型是否与后缀一致
9. 若日志或 report 出现完整 URL：
   - 先检查是否包含 `key=... / api_key=... / token=... / Bearer ... / sk-...`
   - 所有异常字符串进入控制台、report 或 `pending_retry.json` 前必须走脱敏函数
10. 若进入下一环节引用或二改：
   - 优先直接传递 AnyFast 返回的原始 `BASE64`
   - 不要先强制落本地文件、再回读重编码
   - 不要无必要改写成 URL 或其他中间载体
11. 若只是验证 payload 结构：
   - 优先使用 `--dry-run --print-payload`
   - 带参考图时，不要求外部 URL 可访问或本地文件必须存在；dry-run 只验证 `inline_data` 结构位是否保留

## Reusable Heuristics

- 对上游结构化请求，优先用 `--input-json` 统一承接，再转译为 Gemini 原生请求体。
- 当 `--input-json` 承接到多个任务时，不要让上游再手写外部并发；技能自身应自动切入并发调度。
- 当用户只说“横版高清图”但未给技术枚举时，本技能强制落为：
  - `aspectRatio=16:9`
  - `imageSize=4K`
- 若用户已明确指定 `9:16` 或 `2K`，不得因默认策略而覆盖。
- 并发配置默认取 `100`，但实际执行值必须硬限制在 `100` 以内，避免文档推荐值失控上飘。
- 默认输出不是单一路径常量，而是调用方技能包策略：
  - `general` 走 `output/影片/[项目名]/5-API/image/nano-banana/general/`
  - 输入图驱动的子技能优先贴着第一张本地输入图
  - `4-Design/2-设计` 系显式输出参数优先，可服务同目录同名图片快路径；未显式传时走 `projects/aigc/[项目名]/.../generated/`
- 测试任务未显式给 `project_name` 时，默认映射为 `测试`；临时任务默认映射为 `临时`。
- AnyFast 这版接口的参考图不是 URL 直传，而是 `inline_data`；这是与旧版 `nano-banana` 包最关键的差异点。
- AnyFast 平台这边生成的图片可直接视为 `BASE64` 返回；当下一环节引用生成结果或执行二改时，优先直接按 `BASE64` 方式传入，不额外改写成文件路径或 URL。
- 若调用方传了带后缀的 `--output-filename`，最终落盘后缀仍必须以接口真实返回的 MIME 为准，不能盲信调用方传入的后缀。
- 端点、默认模型、密钥优先从根目录 `.env` 读取，避免技能文档和脚本各自维护一份配置。
- 控制台与 report 是可分享诊断面，任何来自 HTTP 异常的完整 URL 都必须先脱敏；`key=...` 泄露不是单次日志问题，而是脚本错误处理层的问题。
- 当调用方只关心图片结果、不需要复盘 JSON 时，应优先开启 `--no-report`，减少标准布局阶段冗余文件。
- 当目标只是验证结构、映射和默认值时，`--dry-run` 不应被参考图可达性阻塞；最稳妥的做法是让 dry-run 保留 `inline_data` 同形占位，而把真实下载留给正式调用阶段。
- `5-API` 只消费已解析好的参考图输入；项目级资产注册的单一事实源应位于 `output/影片/<项目名>/3-设定/5-注册/asset_registry.*.json`，不应反向漂移到 API 层定义；旧 `.schema` 只作兼容回退。
- 当上游一次携带多张 4K 级本地参考图时，最稳的修复点通常不是删图，而是先在 API 桥接层做“只影响请求体、不改 canonical 原图”的内存压缩；这样能同时保住上游事实源和下游 I2I 稳定性。

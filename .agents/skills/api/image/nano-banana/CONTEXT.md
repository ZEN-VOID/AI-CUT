# Context: nano-banana (API 契约层)

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: auto
current_lines: auto
current_cases: auto
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
| `TM-DXJ2-OUTPUT-PATH` | 产物落到技能级散目录或旧别名目录 | 输出路由层 | 默认输出统一改为 `output/影片/[项目名]/5-API/image/nano-banana/` | 由脚本集中构造默认路径，测试/临时任务自动映射项目名 | 报告中的 `project_name / task_kind / output_dir` 与规则一致 |
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

## Repair Playbook

1. 先跑：
   - `python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py --prompt "test" --dry-run --print-payload`
2. 先核查 `.env`：
   - `ANYFAST_API_BASE_URL=https://fw2afus.ent.acc.kurtisasia.com`
   - `DXJ2_DEFAULT_MODEL=gemini-3.1-flash-image-preview`
3. 核查输出路径：
   - 默认应进入 `output/影片/[项目名]/5-API/image/nano-banana/`
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
9. 若进入下一环节引用或二改：
   - 优先直接传递 AnyFast 返回的原始 `BASE64`
   - 不要先强制落本地文件、再回读重编码
   - 不要无必要改写成 URL 或其他中间载体
10. 若只是验证 payload 结构：
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
- 默认输出走项目资产树：
  - `output/影片/[项目名]/5-API/image/nano-banana/`
- 测试任务未显式给 `project_name` 时，默认映射为 `测试`；临时任务默认映射为 `临时`。
- AnyFast 这版接口的参考图不是 URL 直传，而是 `inline_data`；这是与旧版 `nano-banana` 包最关键的差异点。
- AnyFast 平台这边生成的图片可直接视为 `BASE64` 返回；当下一环节引用生成结果或执行二改时，优先直接按 `BASE64` 方式传入，不额外改写成文件路径或 URL。
- 若调用方传了带后缀的 `--output-filename`，最终落盘后缀仍必须以接口真实返回的 MIME 为准，不能盲信调用方传入的后缀。
- 端点、默认模型、密钥优先从根目录 `.env` 读取，避免技能文档和脚本各自维护一份配置。
- 当调用方只关心图片结果、不需要复盘 JSON 时，应优先开启 `--no-report`，减少标准布局阶段冗余文件。
- 当目标只是验证结构、映射和默认值时，`--dry-run` 不应被参考图可达性阻塞；最稳妥的做法是让 dry-run 保留 `inline_data` 同形占位，而把真实下载留给正式调用阶段。
- `5-API` 只消费已解析好的参考图输入；项目级资产注册的单一事实源应位于 `output/影片/<项目名>/3-设定/5-注册/asset_registry.*.json`，不应反向漂移到 API 层定义；旧 `.schema` 只作兼容回退。
- 当上游一次携带多张 4K 级本地参考图时，最稳的修复点通常不是删图，而是先在 API 桥接层做“只影响请求体、不改 canonical 原图”的内存压缩；这样能同时保住上游事实源和下游 I2I 稳定性。

## Case Log

### [CASE-20260309-DXJ2-INIT] 新建 AnyFast 版 nano-banana 技能基线

- symptom: 需要在 `.agents/skills/api/image/nano-banana` 新建技能包，并按 AnyFast 官方 `gemini-3.1-flash-image-preview` 图像接口格式重构技能。
- root cause: 目标目录为空，且旧版 `nano-banana` 技能使用的是另一套 `images/generations` 接口，不能直接复用请求体。
- final fix: 新建 `SKILL.md`、`CONTEXT.md`、`scripts/nano_banana_generate.py`、`references/api.md`、`agents/openai.yaml`、`requirements.txt`，并把默认 `16:9 / 4K`、`inline_data` 转译与原生 `generateContent` 请求体固化到脚本和技能合同中。
- prevention checklist:
  - [x] 默认值策略同时写入 `SKILL.md` 与脚本常量
  - [x] 使用 `contents + generationConfig.imageConfig` 作为唯一请求体结构
  - [x] 参考图统一转成 `inline_data`
  - [x] `CONTEXT.md` 建立 Type Map / Playbook / Heuristics 基线
- evidence paths:
  - `.agents/skills/api/image/nano-banana/SKILL.md`
  - `.agents/skills/api/image/nano-banana/CONTEXT.md`
  - `.agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`
  - `.agents/skills/api/image/nano-banana/references/api.md`
  - `.agents/skills/api/image/nano-banana/agents/openai.yaml`
  - `.agents/skills/api/image/nano-banana/requirements.txt`
- user feedback/constraint: 用户要求“也是 nano-banana 图像生成”，但参照文档切换为 AnyFast 官方 `image-generation-pro-preview`，且未明确指定比例和质量时默认 `16:9` 与 `4K`。

### [CASE-20260309-DXJ2-CONFIG] 把端点、密钥与默认模型收口到根目录 .env

- symptom: 新技能初版仍以内置默认 URL 为主，尚未把真实平台地址、加速端点、密钥和默认模型收口到 `.env`。
- root cause: 源层配置分散在技能文档与脚本常量中，缺少环境变量单一事实源。
- final fix: 在根目录 `.env` 写入 `ANYFAST_PLATFORM_URL`、`ANYFAST_API_BASE_URL`、`ANYFAST_DOCS_URL`、`ANYFAST_API_KEY`、`DXJ2_DEFAULT_MODEL`，并同步把 `SKILL.md`、`references/api.md`、脚本读取逻辑改为优先引用这些环境变量。
- prevention checklist:
  - [x] `.env` 成为端点/密钥/默认模型的单一事实源
  - [x] 脚本支持从 `.env` 自动构造完整 API URL
  - [x] 文档与脚本引用相同变量名，避免漂移
- evidence paths:
  - `.env`
  - `.agents/skills/api/image/nano-banana/SKILL.md`
  - `.agents/skills/api/image/nano-banana/references/api.md`
  - `.agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`

### [CASE-20260309-DXJ2-RESPONSE-PARSE] AnyFast 成功回图但脚本未识别 camelCase 图片字段

- symptom: 真实生图请求返回 `finishReason=STOP`、`candidate_count=1`，但 `saved_files` 为空，导致误判“未出图”。
- root cause: 直接技术原因是脚本只解析 `inline_data/mime_type`，而 AnyFast 实测返回 `inlineData/mimeType`；规则源在 `scripts/nano_banana_generate.py` 的响应解析函数；规则源的规则源是仓库 `AGENTS.md` 要求的 Root-Cause First 与源层增强契约。
- final fix: 把响应解析升级为同时兼容 camelCase 和 snake_case，并把实测字段写回 `references/api.md` 与本 `CONTEXT.md`。
- prevention checklist:
  - [x] 响应解析函数同时兼容 `inlineData` / `inline_data`
  - [x] MIME 字段同时兼容 `mimeType` / `mime_type`
  - [x] 成功 smoke test 后检查 `saved_files` 是否非空
- evidence paths:
  - `.agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`
  - `.agents/skills/api/image/nano-banana/references/api.md`

### [CASE-20260309-DXJ2-OUTPUT-ROUTING] 默认输出目录切换到项目资产树

- symptom: 目录命名调整为 `nano-banana` 后，若仍沿用旧别名目录，会导致产物无法稳定并入项目正式资产树。
- root cause: 直接技术原因是脚本与文档残留旧目录别名；规则源在 `scripts/nano_banana_generate.py` 的默认输出路径构造与相关文档引用；规则源的规则源是仓库 `AGENTS.md` 对 canonical `output/影片/<项目名>/...` 目录的全局约束。
- final fix: 统一把默认输出目录改为 `output/影片/[项目名]/5-API/image/nano-banana/`，并保留 `project_name + task_kind(project/test/temp)` 映射；测试/临时任务在未显式传项目名时自动映射到 `测试/临时`。
- prevention checklist:
  - [x] 输出目录由脚本单一构造，不再散落旧别名路径
  - [x] 报告记录 `project_name / task_kind / output_dir`
  - [x] `SKILL.md / references/api.md / CONTEXT.md` 同步改为 `nano-banana`
- evidence paths:
  - `.agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`
  - `.agents/skills/api/image/nano-banana/SKILL.md`
  - `.agents/skills/api/image/nano-banana/references/api.md`

### [CASE-20260309-DXJ2-BATCH-CONCURRENCY] 多任务默认自动切入批量并发，硬上限 100

- symptom: 用户确认当前脚本在多任务场景下会一张一张串行执行，要求改为“当要求执行多个任务时，默认自动按并发模式执行，最大并发限制 100”。
- root cause: 直接技术原因是 `scripts/nano_banana_generate.py` 只有单任务单请求路径，缺少多任务输入识别、批量调度与 `max_concurrent` 钳制；规则源在技能脚本与 `SKILL.md`；规则源的规则源是仓库 `AGENTS.md` 要求的 Root-Cause First、源层增强与 field-centric 同源合同。
- final fix: 把 `--input-json` 扩展为支持对象数组与 `tasks[]`，在任务数 `>1` 时自动启用 `ThreadPoolExecutor` 并发调度；新增 `--max-concurrent`，默认值 `100`、执行硬上限 `100`；同步在 `SKILL.md` 增加并发字段、步骤、通过标准与批量汇总报告约定。
- prevention checklist:
  - [x] 多任务输入自动判定，不再要求上游额外手写外部并发
  - [x] `--max-concurrent` 默认 `100`
  - [x] 实际执行并发钳制到 `<=100`
  - [x] 多任务输出新增 `nano_banana_batch_report_*.json`
  - [x] `SKILL.md` / 脚本 / `CONTEXT.md` 三处同步并发合同
- evidence paths:
  - `.agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`
  - `.agents/skills/api/image/nano-banana/SKILL.md`
  - `.agents/skills/api/image/nano-banana/CONTEXT.md`
- user feedback/constraint: 用户明确要求“必须增加批量并发调度，且默认为当要求执行多个任务时自动按照并发模式进行，最大并发限制100”。

### [CASE-20260312-DXJ2-NO-REPORT] 标准布局批量生图默认 report 可选化

- symptom: 标准布局 `layout.json` 已可直接承载生图请求，但 `nano_banana_generate.py` 仍默认为每个任务和每个 batch 生成 report，导致面板链路冗余文件激增。
- root cause: 直接技术原因是 CLI 和 `run_generation_from_docs()` 虽已加入 `no_report` 参数雏形，但未完整透传到桥接调用、主流程打印和批量汇总写入；规则源在 `scripts/nano_banana_generate.py` 与标准布局 bridge；规则源的规则源是仓库 `AGENTS.md` 的 Root-Cause First 与源层增强契约。
- final fix: 完整打通 `--no-report` 到任务执行、批量汇总和控制台提示；标准布局 bridge 与三类面板脚本默认传 `no_report=True`，仅保留图片与返回结果追踪。
- prevention checklist:
  - [x] `run_generation_from_docs()` 与 CLI 主流程使用同一 `no_report` 合同
  - [x] `--no-report` 时不再打印“报告已写入”误导性文案
  - [x] 调用方默认策略与 `SKILL.md` / `CONTEXT.md` 同步
- evidence paths:
  - `.agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`
  - `.agents/skills/api/image/nano-banana/SKILL.md`
  - `.agents/skills/aigc2026/3-设定/_shared/IO_CONTRACT.md`

### [CASE-20260329-DXJ2-EXTENSION-DRIFT] 显式输出文件名会保留错误后缀，导致名实不符

- milestone_type: source_contract_change
- symptom: `multiview-scene` 实际成功出图，但调用方显式传入 `SCN-001-肖记小吃店-室内-multiview.png` 后，AnyFast 返回 JPEG 时仍以 `.png` 落盘，形成“文件名是 PNG、内容是 JPEG”的资产。
- root cause: 直接技术原因是 `scripts/nano_banana_generate.py` 在 `output_filename` 已带后缀时直接复用该后缀，没有再校验接口真实返回的 `mime_type`；规则源在 API 契约层脚本的保存逻辑；规则源的规则源是仓库 `AGENTS.md` 的 Root-Cause First、源层增强与输出可追溯契约。
- final fix: 新增统一的输出路径归一化函数，保存时始终以返回 MIME 推导最终后缀；同时把该约束补入 `SKILL.md` 与本 `CONTEXT.md`。
- prevention checklist:
  - [x] 显式 `--output-filename` 也要走 MIME->extension 归一化
  - [x] 多图返回时 `_2/_3...` 命名沿用归一化后的真实后缀
  - [x] 验收时可用 `file <产物>` 交叉检查文件类型与后缀是否一致
- evidence paths:
  - `.agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`
  - `.agents/skills/api/image/nano-banana/SKILL.md`
  - `.agents/skills/api/image/nano-banana/CONTEXT.md`
  - `output/影片/美食争霸第三版/0-初始/3-参照/SCN-001-肖记小吃店-室内-multiview.png`
- user feedback/constraint: 本次执行目标是直接完成 `multiview-scene` 生成，产物已成功落盘，因此修复必须保持调用参数与资产位置不变，只增强保存阶段的正确性。

### [CASE-20260402-DXJ2-DRYRUN-REF-FETCH] `dry-run` 被参考图读取阻塞，无法只验证 payload 结构

- milestone_type: source_contract_change
- symptom: 上层技能在调用 `run_generation_from_docs(..., dry_run=True)` 验证 `design payload -> nano-banana` 映射时，只因 `images[]` 里有 URL，就在 `_coerce_image_part()` 阶段真实发起下载，导致还没到“不调用 API”的 dry-run 目标，就先被外部证书/图源可达性拦住。
- root cause: 直接技术原因是 `scripts/nano_banana_generate.py::_prepare_task()` 即使在 `dry_run=True` 下，仍统一调用 `_coerce_image_part()` 去下载 URL / 读取本地参考图；规则源在 API 脚本的 dry-run 路径；规则源的规则源是仓库 Root-Cause First 与 `test-and-improve` 要求的“先命中主实例、失败后优先修源层入口”。
- final fix: 为 dry-run 增加 `_coerce_image_part_dry_run()` 占位路径，保持 `inline_data` 同形结构但不真实解引用参考图；同时在 `SKILL.md` / `CONTEXT.md` 明确 dry-run 只验证 payload 结构。
- prevention checklist:
  - [x] `dry_run=True` 时不再真实下载 URL 或读取本地参考图
  - [x] payload 仍保留 `inline_data.mime_type + data` 结构位
  - [x] 文档明确“dry-run 验结构，不验图源可达性”
- evidence paths:
  - `.agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`
  - `.agents/skills/api/image/nano-banana/SKILL.md`
  - `.agents/skills/api/image/nano-banana/CONTEXT.md`
- user feedback/constraint: 本次问题由 `3-设定/2-设计` 的直生图 dry-run 验证触发，要求优先修 API 契约层，而不是在应用层绕过参考图。

### [CASE-20260408-DXJ2-PAYLOAD-413] 超大参考图在桥接层内存压缩后再入模

- milestone_type: source_contract_change
- symptom: `谁与争锋/第1集` 漫画故事板实跑时，单组请求携带 7 张约 8MB 的本地参考图，AnyFast 在正式发包阶段连续返回 `413 Request Entity Too Large`。
- root cause: 直接技术原因是 `scripts/nano_banana_generate.py` 以前会把本地/远程参考图原样 base64 塞进 `inline_data`，没有任何请求体预算控制；规则源在 API 桥接层的 `_coerce_image_part()`；规则源的规则源是仓库 `AGENTS.md` 的 Root-Cause First、失败优先修源层与“canonical 原图不得被工作流副作用改写”。
- final fix: 在桥接层新增“超大参考图内存压缩”路径，对 URL / 本地文件 / data URL 的图像先做保守缩边与编码压缩，再写入 `inline_data`；同时把 `image_budget / image_part_stats` 写进 report，便于后续追溯请求体预算。
- prevention checklist:
  - [x] 超大参考图在桥接层入模前自动预算收缩
  - [x] 压缩仅发生在内存中，不改动 canonical 原图
  - [x] `SKILL.md` 同步补入请求体预算合同
  - [x] report 记录 `image_budget / image_part_stats`
- evidence paths:
  - `.agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py`
  - `.agents/skills/api/image/nano-banana/SKILL.md`
  - `.agents/skills/api/image/nano-banana/CONTEXT.md`
  - `output/影片/谁与争锋/4-分镜/漫画故事板/第1集/pending_retry.json`
- user feedback/constraint: 用户要求先刷新 `3-设定/5-注册`，随后直接执行 `4-分镜/漫画故事板`，因此修复必须落在可复用源层，而不是只手工裁掉当前分镜的参照图。

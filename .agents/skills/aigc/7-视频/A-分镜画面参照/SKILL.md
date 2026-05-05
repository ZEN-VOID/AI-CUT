---
name: aigc-video-frame-visual-reference
description: "Use when creating LibTV video jobs from each storyboard frame visual reference."
governance_tier: full
metadata:
  short-description: AIGC frame-image referenced group video generation
---

# aigc 7-视频 / A-分镜画面参照

`A-分镜画面参照` 负责把 `projects/aigc/<项目名>/4-分组/` 中的分镜组转为 LibTV 组级视频生成任务：step1 直接使用现有分镜组内容作为生视频提示词主体，并把组内 `分镜N` 转为四段式 `分镜ID`；step2 检查 `6-图像/A-分镜画面/` 是否存在对应四段式 `分镜ID` 的图像，有则在对应 `分镜ID` 后标注 `@路径` 并写入参照清单，没有则移除空槽位；step3 调用 `.agents/skills/cli/libTV`，以分镜组为单位组织“完整组内容 + 多张分镜画面参照”的 LibTV 视频任务，默认后台多线程批量并发执行。

## Context Loading Contract

- 每次调用 `$aigc-video-frame-visual-reference` 时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 若任务绑定 `projects/aigc/<项目名>/`，必须先加载项目根 `MEMORY.md`，再加载项目根 `CONTEXT/` 中与视频阶段、分镜画面、风格、角色、场景或生成限制相关的上下文。
- `4-分组` 是本技能的视频内容主要信息来源；不得回到 `3-摄影`、`3-Detail` 或更早阶段改写分镜组内容，除非用户显式要求修复上游。
- 分镜组视频 prompt 主体直接采用 `4-分组` 的现有分镜组正文；LLM 只负责保真组织、LibTV 指令化封装、参照映射说明、缺口说明和审查，不得扩写或改写剧情事实。
- 分镜画面参照图只来自 `projects/aigc/<项目名>/6-图像/A-分镜画面/` 中与四段式 `分镜ID` 对应的真实本地图片；不存在时移除该空槽位，不猜测、不补占位、不改用无关图片。
- 调用 LibTV 前必须同时遵循 `.agents/skills/cli/libTV/SKILL.md + CONTEXT.md`：先执行 `LIBTV_ACCESS_KEY credential check`，多任务写 queue ledger，异步任务保留 `sessionId`。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `.agents/skills/aigc/SKILL.md` > `.agents/skills/aigc/7-视频/SKILL.md` > 本 `SKILL.md` > `references/` / `steps/` / `types/` / `review/` / `templates/` > `.agents/skills/cli/libTV/SKILL.md` > `agents/openai.yaml` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md`。

## Multi-Subskill Continuous Workflow

当本技能被整体调用时，在满足必要输入、显式选择和安全门后，不再为“是否继续下一步”额外确认。

- 无序号同级子技能包默认全选并发执行，由所属父级汇总、裁决和写回唯一 canonical 输出。
- 数字序号子技能包或节点默认按数字升序串行执行，前一节点产物自动作为后一节点输入。
- 英文序号子技能包或路线默认按用户意图、父级路由或输入类型单选分流；只有用户明确要求对比、并跑或批量多路线时才多选。
- 卫星技能、旁路 reviewer、query/resume/review 类辅助入口不默认纳入主链连续调度；只有用户请求、阶段门禁或父级合同显式需要时才回接。
- 连续调度不得绕过阻断门：缺少项目根、分镜组、参照路线、`LIBTV_ACCESS_KEY` 或参照绑定歧义会造成错误提交时，必须先阻断并说明最小修复项。
- 每个被调度的子技能包仍必须加载自身 `SKILL.md + CONTEXT.md`；脚本只能承担机械辅助，不得替代 LLM 视频 prompt 主创、参照裁决或父级最终裁决。

## Input Contract

Accepted input:

- 项目名、项目路径、单集或多集范围，要求从 `4-分组` 批量生成组级视频，并使用 `6-图像/A-分镜画面` 的镜级图像作为多图参照。
- 用户指定一个或多个三段式分镜组 ID，例如 `1-1-1`；或指定一个或多个四段式 `分镜ID`，由本技能回推所属分镜组。
- 已有 `7-视频/A-分镜画面参照/` 的 prompt、参照 manifest、LibTV batch YAML、queue ledger 或生成结果需要 repair / review / rerun / query。
- 用户要求“在对应分镜ID后添加 `@路径`”“按分镜组多图参照出视频”“后台并发跑 LibTV”等任务。

Required input:

- 可定位的 `projects/aigc/<项目名>/4-分组/第N集.md`。
- 每个目标分镜组必须有可解析的 `## x-y-z` 标题和非空组正文；组内分镜应能从 `分镜N`、`分镜 N` 或等价标签映射到 `x-y-z-N`。
- 调用 LibTV 前必须能确定项目内输出目录，默认 `projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/`。
- 执行生成前必须能运行 `LIBTV_ACCESS_KEY credential check`；若失败，停止提交并进入 LibTV 登录/环境排障。

Optional input:

- `prompt_only`：只生成 shot index、prompt 包、参照 manifest 和 LibTV batch YAML，不执行 LibTV。
- `episode_batch`：一次处理一集全部分镜组。
- `group_batch`：一次处理多个指定分镜组。
- `shot_batch`：指定多个四段式 `分镜ID`，本技能按所属组聚合生成组级任务。
- `execution.concurrency`：并发 worker 数；默认 `min(4, job_count)`，不得让多个 worker 同时改写同一个最终报告。
- 默认视频规格为 720P、15 秒、16:9；用户显式指定 LibTV 模型、duration、ratio、video_resolution、poll 秒数、输出目录、rerun / replace 策略或下载策略时，以用户要求为准。

Reject or clarify when:

- `4-分组` 缺失、目标分镜组 ID 无法唯一追溯、四段式 `分镜ID` 与组内 `分镜N` 无法稳定对应，或用户要求改变分镜组剧情核心、镜头顺序、角色事实、动作结果或组边界。
- 用户要求脚本主创视频 prompt 正文、自动扩写剧情或用模板补写未知画面。
- 用户要求生成分镜画面图本体，应转入 `6-图像/A-分镜画面`。
- 用户指定的图片参照路径不存在、位于项目外且未明确授权，或同一 `分镜ID` 命中多个同优先级图片候选。

## Positioning

本技能是 `7-视频` 阶段的组级多图分镜画面参照入口，向上承接 `4-分组`，横向读取 `6-图像/A-分镜画面` 的已生成单帧图，向下调用 `.agents/skills/cli/libTV`。它拥有视频 prompt 包、镜级参照 manifest、LibTV batch YAML、queue ledger、结果下载记录和执行报告的裁决权；它不拥有上游分组改写权，也不拥有分镜画面生成权。

## LLM-First Creative Authorship Contract

- 视频 prompt 的 LibTV 指令化组织、镜级参照解释、运动/声音约束、节奏保真说明和失败诊断必须由 LLM 直接完成。
- 脚本只允许承担读取、抽取、路径匹配、YAML/JSON 投影、队列台账、并发提交、状态查询、下载和校验等机械辅助职责。
- 脚本不得把 `4-分组` 正文规则拼接成新的创作正文，不得扩写剧情、替代镜头判断或生成 canonical prompt truth。
- 参照图路径属于机械绑定；是否使用参照图、如何在 prompt 中把 `分镜ID@路径` 转换为 LibTV `@图N` 映射，仍须由本技能合同和 LLM 审查裁决。

## Mode Selection

| mode | 触发信号 | 主要动作 |
| --- | --- | --- |
| `prompt_only` | 只要求配置、YAML、prompt 包或提交计划 | 执行 step1-step2，写 LibTV batch YAML，不提交 |
| `single_group_generate` | 指定一个三段式分镜组 ID 且要求出视频 | 执行 step1-step3，单组提交 LibTV |
| `episode_batch_generate` | 指定一集或默认整集批量 | 对该集全部分镜组执行 step1-step3，默认后台多线程并发提交 |
| `group_batch_generate` | 指定多个分镜组 ID | 只处理目标分镜组集合，保持独立 YAML job 与输出 |
| `shot_batch_generate` | 指定多个四段式 `分镜ID` | 按所属组聚合，只生成命中镜头所在组的组级 job |
| `query_or_download` | 已有 sessionId 或 queue ledger，需要查询/下载 | 按 LibTV queue 规则刷新状态和下载结果 |
| `repair` | prompt 缺组、ID 映射错、图像错绑、YAML 漂移、sessionId 缺失、下载不完整 | 按 review gate 定位返工节点 |
| `review_only` | 只检查现有输出 | 审查 prompt、参照、LibTV plan、queue 和本地视频结果 |

## Reference Loading Guide

| 场景 | 必读文件 |
| --- | --- |
| 从 `4-分组` 提取组级正文并映射四段式分镜 ID | `references/group-shot-source-contract.md` |
| 匹配 `6-图像/A-分镜画面` 的镜级图 | `references/frame-image-binding-contract.md` |
| 组织 LibTV YAML、命令和后台并发提交 | `references/libtv-handoff-contract.md`、`.agents/skills/cli/libTV/SKILL.md`、`.agents/skills/cli/libTV/CONTEXT.md` |
| 执行 step1-step3 主流程 | `steps/frame-reference-video-workflow.md` |
| 判定单组、整集、多组、多镜、查询、修复模式 | `types/type-map.md` |
| 输出审查与返工 | `review/review-contract.md` |
| 输出模板 | `templates/output-template.md`、`templates/libtv-batch.template.yaml` |
| 脚本辅助边界 | `scripts/README.md` |
| 外部知识材料索引 | `knowledge-base/frame-reference-video-knowledge-index.md` |
| 产品侧入口元数据 | `agents/openai.yaml` |

## Visual Maps

```mermaid
flowchart TD
    A["projects/aigc/<项目名>/4-分组/第N集.md"] --> B["step1 提取完整分镜组内容"]
    B --> C["组内 分镜N -> 四段式 x-y-z-N"]
    C --> D["按分镜ID标注源镜头"]
    E["projects/aigc/<项目名>/6-图像/A-分镜画面/第N集/images/<shot_id>.*"] --> F["step2 绑定分镜画面图"]
    F --> G{"图片存在?"}
    G -->|"Yes"| H["在对应分镜ID后追加 @路径"]
    G -->|"No"| I["移除空参照槽位"]
    D --> J["完整组内容 + 分镜ID@路径 映射"]
    H --> J
    I --> J
    J --> K["LibTV batch YAML"]
    K --> L["step3 $libTV backend worker pool"]
    L --> M["sessionId queue ledger"]
    M --> N["7-视频/A-分镜画面参照/第N集"]
```

```mermaid
flowchart TD
    A["Group job YAML"] --> B{"frame reference_images 非空?"}
    B -->|"Yes"| C["upload_file.py + create_session.py"]
    C --> D["upload_file.py <shot_1_path> ... upload_file.py <shot_n_path>"]
    D --> E["prompt maps @图N to shot_id@path"]
    B -->|"No"| F["create_session.py"]
    E --> G["async submit + query_session"]
    F --> G
    G --> H["download_dir videos/"]
```

```mermaid
stateDiagram-v2
    [*] --> Intake
    Intake --> ExtractGroups
    ExtractGroups --> MapShotIds
    MapShotIds --> BindFrameImages
    BindFrameImages --> BuildLibTVYaml
    BuildLibTVYaml --> ReviewGate
    ReviewGate --> PromptOnly
    ReviewGate --> BackgroundSubmit
    BackgroundSubmit --> QueueTracking
    QueueTracking --> QueryDownload
    QueryDownload --> CloseReport
    ReviewGate --> Repair
    Repair --> ExtractGroups
    CloseReport --> [*]
```

## Execution Contract

1. 加载本 `SKILL.md + CONTEXT.md`；项目任务中加载项目 `MEMORY.md` 与相关项目 `CONTEXT/`。
2. 按 `types/type-map.md` 锁定 mode、集号范围、目标分镜组集合、目标四段式 `分镜ID` 集合、是否执行 LibTV、是否查询下载。
3. step1：以 `projects/aigc/<项目名>/4-分组` 为主要信息来源，解析每个 `## x-y-z` 分镜组，完整提取组正文；`## x-y-z~x-y-z` 组间连接件默认忽略，不进入视频 prompt、四段式映射、参照 manifest 或 LibTV job；视频 prompt 主体直接使用现有组内容，不进行剧情改写。
4. step1 镜级映射：组内每个 `分镜N` 转为四段式 `x-y-z-N`；若组稿已经提供匹配的四段式 `分镜ID`，以其为基准，不重新编号覆盖。
5. step1 组装 prompt 时添加 LibTV 视频约束前缀：`根据以下完整分镜组内容生成一条连续视频。保持分镜顺序、角色动作、镜头运动、场景与情绪连续；不生成字幕，不生成BGM，保留物理互动音效与环境音。`
6. step2：检查 `projects/aigc/<项目名>/6-图像/A-分镜画面/第N集/` 下是否存在与四段式 `分镜ID` 对应的图片；优先 `images/<shot_id>.*`，其次同集目录内 `<shot_id>.*`，允许常见扩展名 `png/jpg/jpeg/webp`。
7. step2 绑定结果必须写入 manifest 与 YAML：有图则在对应 `分镜ID` 后添加 `@<path>`，并写 `reference_images[]`；无图则该镜头不写空图片槽位，只记录 `reference_status: missing_optional`。
8. step3：根据 YAML 转换为 `$libTV` 脚本提交格式。一组一个 job：有一张或多张分镜画面图时，先逐图运行 `upload_file.py <path>`，再把返回的 URL 编号写入 prompt，并运行 `create_session.py "<完整组内容 + 参照图URL>"`；无图时直接运行 `create_session.py "<完整组内容>"`。
9. LibTV `libtv_session_with_uploaded_references` 当前图片输入上限按 `.agents/skills/cli/libTV` 执行；若某组可用分镜画面图超过当前 LibTV 参照限制，必须记录 `reference_over_limit`，按用户策略选择阻断、分段提交或降级为文字 prompt，不得静默丢图。
10. 默认后台多线程批量并发执行：提交前生成 `第N集-libtv-batch.yaml` 和 queue ledger；worker 数默认 `min(4, job_count)`，每个 worker 只写自己的临时结果，最终由主流程汇流更新 `第N集-libtv-results.json` 与 `执行报告.md`。
11. 每次生成前必须运行 `LIBTV_ACCESS_KEY credential check`；若失败，停止提交并按 `$libTV` 技能进入登录或环境排障。
12. 短轮询只作等待窗口；超时后必须保存 `sessionId`，把状态写入 queue ledger，并使用 `python3 .agents/skills/cli/libTV/scripts/query_session.py <sessionId>` 后续查询。下载默认写入 `projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/videos/`。
13. 交付前执行 `review/review-contract.md`：组 ID 追溯、四段式 ID 映射、prompt 完整性、`分镜ID@路径` 参照路径、LibTV 上传/会话/查询/下载计划、queue ledger、并发写入边界和本地视频结果状态必须可复核。

## Field Mapping

| field_id | 输出/证据 | 内容要求 | 失败码 |
| --- | --- | --- | --- |
| `FIELD-FVID-01` | input manifest | 项目根、集号、`4-分组`、目标组/镜范围可追溯 | `FAIL-FVID-INPUT` |
| `FIELD-FVID-02` | group and shot index | `group_id` 可回指 `## x-y-z`，四段式 `shot_id` 可回指组内 `分镜N` | `FAIL-FVID-SHOT-ID` |
| `FIELD-FVID-03` | prompt package | LibTV 视频约束前缀 + 现有完整组内容 + `分镜ID@路径` 映射，镜头未缺失乱序 | `FAIL-FVID-PROMPT` |
| `FIELD-FVID-04` | frame reference manifest | 只绑定真实 `6-图像/A-分镜画面` 图片；缺图移除空槽位 | `FAIL-FVID-REF` |
| `FIELD-FVID-05` | LibTV YAML / submit plan | 有图走上传后建会话，无图走纯文本建会话，参数符合 `$libTV` | `FAIL-FVID-LIBTV` |
| `FIELD-FVID-06` | queue ledger / session ids | 多任务均有 queue row、sessionId 或明确失败原因、next_action | `FAIL-FVID-QUEUE` |
| `FIELD-FVID-07` | results / report | generated / submitted / querying / failed / skipped 状态清楚 | `FAIL-FVID-REPORT` |

## Field Master

| field_id | owner | canonical file | must contain | fail code |
| --- | --- | --- | --- | --- |
| `FIELD-FVID-01` | input lock | `第N集-group-shot-index.json` / report | 项目根、集号、`4-分组`、视频输出根 | `FAIL-FVID-INPUT` |
| `FIELD-FVID-02` | group and shot extraction | `第N集-group-shot-index.json` | `group_id`、`shot_id`、source heading、source shot label、body hash | `FAIL-FVID-SHOT-ID` |
| `FIELD-FVID-03` | prompt assembly | `第N集-video-prompts.md` | LibTV 前缀、完整组正文、`shot_id@path` 与 `@图N` 映射说明 | `FAIL-FVID-PROMPT` |
| `FIELD-FVID-04` | reference binding | `第N集-reference-manifest.json` | frame image paths or missing_optional reasons without empty slots | `FAIL-FVID-REF` |
| `FIELD-FVID-05` | LibTV handoff | `第N集-libtv-batch.yaml` | command type、prompt、reference_images、output path、poll | `FAIL-FVID-LIBTV` |
| `FIELD-FVID-06` | queue tracking | `第N集-libtv-queue.md` | queue_id、group_id、sessionId、remote_status、next_action | `FAIL-FVID-QUEUE` |
| `FIELD-FVID-07` | convergence | `执行报告.md` | verdict、处理范围、失败/跳过与返工入口 | `FAIL-FVID-REPORT` |

## Thought Pass Map

| pass_id | focus field | core question | action | evidence |
| --- | --- | --- | --- | --- |
| `PASS-FVID-01` | `FIELD-FVID-01` | 本轮处理哪个项目、集号、分镜组和分镜范围 | 锁定 mode、读取项目上下文 | input manifest |
| `PASS-FVID-02` | `FIELD-FVID-02` | 如何从 `4-分组` 保真提取组正文并建立四段式 ID | 解析 `## x-y-z` 与组内 `分镜N` / 已有 `分镜ID` | group-shot index |
| `PASS-FVID-03` | `FIELD-FVID-03` | 如何保证 prompt 直接承接现有组内容 | 添加固定视频约束，接入完整组正文和参照映射 | prompt markdown |
| `PASS-FVID-04` | `FIELD-FVID-04` | 每个四段式 `分镜ID` 是否有对应分镜画面图 | 按 shot_id 查 `6-图像/A-分镜画面` | reference manifest |
| `PASS-FVID-05` | `FIELD-FVID-05` | YAML 如何转换为 $libTV skill scripts 命令 | 有图选 `libtv_session_with_uploaded_references`，无图选 `libtv_session_text_only` | batch YAML / command preview |
| `PASS-FVID-06` | `FIELD-FVID-06` | 批量任务如何后台并发且可追踪 | 建 ledger、提交、记录 sessionId | queue ledger |
| `PASS-FVID-07` | `FIELD-FVID-07` | 输出如何闭环并可返工 | 汇总审查、失败和跳过原因 | execution report |

## Pass Table

| pass_id | pass standard | fail code | rework entry |
| --- | --- | --- |
| `PASS-FVID-01` | 必需输入可读，输出根明确 | `FAIL-FVID-INPUT` | `types/type-map.md` |
| `PASS-FVID-02` | 每个 `group_id` 和 `shot_id` 唯一且可回指源标题和组内分镜 | `FAIL-FVID-SHOT-ID` | `references/group-shot-source-contract.md` |
| `PASS-FVID-03` | prompt 以固定视频约束起笔，现有组内容作为主体，镜头未缺失乱序 | `FAIL-FVID-PROMPT` | `references/group-shot-source-contract.md` |
| `PASS-FVID-04` | 参照图路径真实存在；缺图移除空槽位并记录原因 | `FAIL-FVID-REF` | `references/frame-image-binding-contract.md` |
| `PASS-FVID-05` | LibTV YAML 可转为合法 `libtv_session_with_uploaded_references` 或 `libtv_session_text_only` 命令 | `FAIL-FVID-LIBTV` | `references/libtv-handoff-contract.md` |
| `PASS-FVID-06` | 每个提交任务都有 queue row、sessionId 或明确失败原因 | `FAIL-FVID-QUEUE` | `.agents/skills/cli/libTV/SKILL.md` |
| `PASS-FVID-07` | 执行报告记录 verdict、处理范围、失败/跳过与返工入口 | `FAIL-FVID-REPORT` | `review/review-contract.md` |

## Root-Cause Execution Contract (Mandatory)

出现失败时必须沿链路上溯：

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> AGENTS.md / skill-工作车间`

优先修复：

1. 组或镜无法追溯、正文截断或改写：回到 `references/group-shot-source-contract.md` 与 `steps/frame-reference-video-workflow.md`。
2. 四段式 ID 错配、分镜画面图错绑、路径不存在、猜测引用或缺图仍写占位：回到 `references/frame-image-binding-contract.md`。
3. YAML 无法转换为 LibTV submit plan、子命令选择错误、参照图超过 LibTV 可承受参照数量未处理或参数越权：回到 `references/libtv-handoff-contract.md` 与 `.agents/skills/cli/libTV/SKILL.md`。
4. 并发提交丢 `sessionId`、queue ledger 漂移或下载半截文件误判成功：回到 `.agents/skills/cli/libTV/CONTEXT.md`。
5. 输出格式不一致：回到 `templates/output-template.md`。
6. 同类失败可复用：沉淀到同目录 `CONTEXT.md`，稳定后晋升到本文件或分区规范。

## Output Contract

- Required output: 组级视频 prompt 包、镜级分镜画面参照 manifest、LibTV batch YAML、LibTV queue ledger、submit/result JSON、逐集执行报告；若执行下载，还应包含本地视频文件。
- Output format: Markdown prompt / report / queue ledger + YAML batch config + JSON manifest / plan / result；生成视频为 LibTV 返回的 MP4 或等价视频文件。
- Output path: `projects/aigc/<项目名>/7-视频/A-分镜画面参照/第N集/`，其中 prompt、manifest、batch YAML、queue、result、报告与视频均在该集目录或其 `videos/` 子目录下。
- Naming convention: prompt 文档命名 `第N集-video-prompts.md`；索引命名 `第N集-group-shot-index.json`；参照清单命名 `第N集-reference-manifest.json`；LibTV 配置命名 `第N集-libtv-batch.yaml`；队列命名 `第N集-libtv-queue.md`；结果命名 `第N集-libtv-results.json`；执行报告命名 `执行报告.md`；视频命名 `<分镜组ID>.mp4`，例如 `1-1-1.mp4`。
- Completion gate: 目标分镜组均可从 `4-分组` 回指；四段式 `分镜ID` 均可回指组内分镜；每条 prompt 完整保留组正文主体；YAML 参照图只绑定真实分镜画面图片并移除缺图空槽位；生成前已通过 `LIBTV_ACCESS_KEY credential check`；批量任务均有 queue ledger；执行 LibTV 时遵循 `.agents/skills/cli/libTV` 的提交、轮询、查询与下载门禁；审查结果为 `pass` 或 `pass_with_todo`。

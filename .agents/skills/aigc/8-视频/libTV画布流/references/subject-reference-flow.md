# Subject Reference Flow

主体参照流是 `libTV画布流` 的默认路线。本文件只定义计划层合同：从 `5-分组` 抽取分镜组、绑定主体参照图、生成 CLI handoff plan、建立审查证据。真实 LibTV 画布操作由最新版 `.agents/skills/cli/libTV` 执行。

## Source Object

基本处理对象：

```text
projects/aigc/<项目名>/5-分组/第N集.md
```

`5-分组` 是本技能的主要信息来源；不得回到 `4-摄影`、`3-Detail` 或更早阶段重写分镜组内容，除非用户显式要求修复上游。

处理粒度：

- 每个 `## x-y-z` 是一条可计划的 LibTV 分镜组视频任务。
- 完整提取组正文和底部 fenced YAML；同步提取组底 YAML 的 `时长估算`，形成 `duration_estimate_seconds`。
- 每个分镜组正文直接作为视频 prompt 的剧情主体，不重写剧情、镜头顺序、台词或动作结果。
- LLM 只负责裁决提取范围、保真组织、缺口说明和审查，不得扩写或改写剧情事实。
- `## x-y-z~x-y-z` 组间连接件默认忽略，不进入视频 prompt、YAML 主体槽位、主体参照 manifest、LibTV job 或视频文件命名。

## YAML Subject Baseline

只从组底 fenced YAML 读取主体：

```yaml
角色:
  - 令狐冲
  - 任盈盈
场景:
  - 海雾村山道
道具:
  - 酒葫芦
时长估算: 约14秒
```

正文泛词、环境描写中的普通名词不自动升级为主体参照对象。名称命中多个候选图片时，先把候选图发送到当前窗口作为可加载上下文执行视觉消歧；无法唯一判定才进入 `ambiguous`。

组底 fenced YAML 必须完整保留在 `video_node.params.prompt` 底部，同时投影到：

- `subject_bindings`
- `duration / duration_source`
- manifest、submit plan 和 queue record
- `cli_handoff.reference_bindings_for_tool_params_only`

## Subject Binding Table

证据工件和 CLI handoff plan 必须包含固定标题 `主体绑定表` 或等价结构化参考绑定表：

```yaml
主体绑定表:
  - yaml_name: 令狐冲
    category: 角色
    canvas_node_name: CHAR-005-令狐冲.png
    node_key: 5a9b2d1e-eb41-4ae9-a93d-9d0d5a67355c
    url: https://libtv-res.liblib.art/claw/.../CHAR.png
    usage: 按参考图保持同一男性武侠人物，作为交手主角之一
```

绑定表只用于工具参数、参考图映射、左侧连线和审查证据，不得整体复制进 `video_node.params.prompt`。最新版 CLI 的稳定主体引用机制固定为：

1. 按 canonical reference order 生成 `planned_left_input_edges[]`，并在每条记录中固定保存 `stable_subject_id / yaml_name / category / node_key / assetId / url`。
2. 用 `libtv node <视频节点> --left <主体图节点>` 或 `--left-add <主体图节点>` 把主体图节点按计划顺序逐张连到视频节点左侧；第一张建立左侧输入，后续逐张追加，保留每一步 `node_key` 证据。
3. 新建或更新视频节点后先查询节点，不得立即 `--run`；此时 prompt 可以是 draft prompt，不作为最终生成 prompt。
4. 从查询结果中的 `data.params.imageList[]` 或等价左侧输入顺序读取真实 runtime 图片顺序，用 `node_key + assetId/url` 反查稳定主体 ID，生成 `runtime_image_placeholder_map[]`。
5. 在 `video_node.params.prompt` 中只能使用已经由 `runtime_image_placeholder_map[]` 证明的 `{{Image 1}}`、`{{Image 2}}` 等官方占位；计划顺序和 runtime 顺序不一致时，默认按 runtime map 自动回写 prompt、manifest、submit plan 和 queue record。
6. 决定性检查固定在最终节点参数、左侧输入和远端 prompt 都写定之后、`--run` 之前；只检查这一次远端查询到的 `data.params.imageList[] + data.params.prompt`，不得只检查本地 prompt 文件。若远端 prompt 出现 `{{Portrait N}}`、`主体绑定表`、参考图清单、执行锁或诊断文本，必须先尝试自动清理并重写最终 prompt；只有 CLI 无法写回、远端继续不可控改写或主体无法唯一回指时，才进入 `needs_rework / prompt_hygiene_failed`。

旧 UI `@` 说法在本技能中只作为历史称呼；交付和执行必须使用最新版 CLI 可验证的 `--left/--left-add + {{Image N}}` 机制。

## Runtime Image Placeholder Gate

`planned_left_input_edges[]` 是提交意图，不是 `{{Image N}}` 的最终真源。LibTV 可能在视频节点 `data.params.imageList[]` 中按内部规则重排图片，因此每个新视频生成都必须执行一次决定性门槛：

1. 按 canonical reference order 逐张 `create/update` 视频节点并连接参考图，但不执行 `--run`。
2. 查询该视频节点，保存原始 `data.params.imageList[]`、等价左侧输入顺序或 CLI 可返回的图片参数证据；此查询用于生成 runtime map，不是最终放行查询。
3. 逐项用 `node_key`、`assetId`、`url` 回查 `主体绑定表` 与 active registry，生成：

```yaml
runtime_image_placeholder_map:
  - image_index: 1
    placeholder: "{{Image 1}}"
    stable_subject_id: C003
    yaml_name: 莉迪亚·沃斯
    category: 角色
    node_key: 86f7d0d9-68df-4762-9c3d-6ab4ddbbe121
    assetId: asset-...
    url: https://...
```

4. 按 `runtime_image_placeholder_map[]` 生成最终 prompt：`{{Image N}}` 只插入底部 fenced YAML 的 `角色 / 场景 / 道具` 条目主体名后，必须来自 runtime map，而不是主体在正文、YAML 或计划数组中的自然顺序。
5. 决定性查询必须发生在最终节点参数、左侧输入和 `params.prompt` 都写定之后、`--run` 之前；用该次 `data.params.imageList[]` 确认 `runtime_image_placeholder_map[]` 未漂移，确保远端 `data.params.prompt` 中每个 YAML 主体条目后的 `{{Image N}}` 指向正确图片，且分镜正文没有被插入占位符。
6. 同一次决定性查询还必须确认远端 prompt 无 `{{Portrait N}}`、绑定表、参考图清单、执行锁、路径或诊断文本。
7. 在 submit plan、queue record 和执行报告中记录 `queried_runtime_image_map_verified=true`、`final_remote_prompt_queried_after_last_prompt_write=true`、`remote_prompt_hygiene_verified=true` 后，才允许执行 `--run`。

若任一 `{{Image N}}` 无法唯一回指稳定主体 ID，runtime 顺序与 prompt 中主体语义不一致，或远端 prompt hygiene 不通过，先进入自动修复分支：按 runtime map 重写 prompt、清理 prompt 污染、必要时重建左侧输入。只有缺失/歧义主体、CLI 无法写回、远端继续不可控改写、参考图审核失败等不可自动修复条件，才记录 `needs_rework / runtime_image_map_mismatch` 或 `needs_rework / prompt_hygiene_failed`，不得进入 `--run`。

## Canvas Node Name Matching

主体参照匹配必须优先使用当前 LibTV 画布中已经存在的规范命名图片节点，而不是先扫描本地生成目录或按文件枚举顺序猜测。

匹配顺序固定为：

1. 查询目标 `projectUuid` 下的现有 `image` 节点；如任务限定分组，同时查询目标分组内节点。
2. 读取项目级设计清单，建立 `YAML 主体名 -> 设计 ID / canonical_name / source_aliases / design_file` 映射：
   - `projects/aigc/<项目名>/6-设计/角色/design-manifest.yaml`
   - `projects/aigc/<项目名>/6-设计/场景/design-manifest.yaml`
   - `projects/aigc/<项目名>/6-设计/道具/design-manifest.yaml`
   - 必要时补读对应 `1-清单/*.md`，处理中文 YAML 名与英文 canonical 名之间的别名关系。
3. 对画布图片节点名执行确定性匹配：
   - `id` 前缀全等优先，如 `C002-*`、`S001-*`、`PROP-015-*`。
   - 其次 `canonical_name` / `name` / `source_aliases` 规范化全等。
   - 再其次使用用户显式主体绑定表中的 `yaml_name -> node_key`。
4. 只有画布现有节点没有唯一命中时，才检查 `libtv-canvas-active-registry.json` 中同 `projectUuid::category::yaml_name` 的 active 记录。
5. 只有画布节点和 active registry 都不能唯一命中，才进入本地 `6-设计/*/3-生成` 兜底上传流程。

不得把以下信息作为主体匹配真源：

- `find` / `ls` / 本地文件扫描返回的自然顺序。
- 画布 edges 返回数组顺序。
- 上传时间、创建时间或节点在 UI 中的视觉排列。
- 中文主体名与英文文件名的模糊子串猜测，除非已被设计清单、清单文件或用户显式绑定表确认。

若同一 YAML 主体命中多个画布图片节点，必须先把候选节点名、node key、URL 和可视图作为歧义证据写入 manifest；能通过设计 ID 或视觉检查唯一确认时再绑定，仍无法确认则进入 `ambiguous`，不得随机选第一个。

## Canonical Reference Order

传入 LibTV 的所有参考数组必须使用同一个 canonical order，而不是上传顺序：

1. YAML `角色` 列表原顺序。
2. YAML `场景` 列表原顺序。
3. YAML `道具` 列表原顺序。

预算裁决先决定哪些主体进入本轮参考图；排序再按上述 YAML 展示顺序保留选中主体的相对位置。`subject_bindings`、CLI handoff 的参考绑定表、`planned_left_input_edges[]`、`source_node_keys`、`source_node_url_mapping` 和计划层参考数组必须一致采用该顺序。创建视频节点后，`data.params.imageList[]` 的实际顺序才是 `{{Image N}}` 的最终 runtime 真源。

`{{Image N}}` 编号来自查询到的 runtime `data.params.imageList[]` 或等价左侧输入顺序，不是自然语言推断。计划层必须先把 canonical order 投影为：

```yaml
planned_left_input_edges:
  - image_index: 1
    placeholder: "{{Image 1}}"
    yaml_name: 令狐冲
    category: 角色
    node_key: 5a9b2d1e-eb41-4ae9-a93d-9d0d5a67355c
    canvas_node_name: CHAR-005-令狐冲.png
    url: https://...
  - image_index: 2
    placeholder: "{{Image 2}}"
    yaml_name: 任盈盈
    category: 角色
    node_key: 9d0d5a67355c-...
    canvas_node_name: CHAR-006-任盈盈.png
    url: https://...
```

主体语义仍以 `stable_subject_id + yaml_name + category + node_key + assetId/url` 绑定为准；`Image N` 只有在 runtime 图片顺序已查询验证时才可作为 prompt 内引用。

不得按以下顺序生成或解释参考绑定：

- 上传顺序。
- 画布节点创建时间。
- 本地文件扫描顺序。
- 未经验证的 `Image N` / `Portrait N` / 缩略图排列。
- 先生成数组再把第 N 张图回填给第 N 个主体。

## Prompt Assembly Contract

可执行模板见 `templates/libtv-remote-prompt-template.md`。

必须分层：

1. `cli_handoff_plan`
   - 包含 `executor_skill=.agents/skills/cli/libTV`、`projectUuid`、目标 group、视频节点名称、`modeType`、`duration`、`resolution`、`ratio`、下载策略、参考图绑定、左侧连线计划和预期证据。
   - 明确 `allow_libtv_prompt_optimization=false`，除非用户显式要求远端优化。
   - 明确 `video_node.params.prompt` 严格等于 `VIDEO_PROMPT`，不得把执行参数、主体绑定表、缺失/排除原因或文件路径复制进 prompt。
   - 参考数组按 canonical reference order 传入，即 YAML `角色` 原顺序 -> YAML `场景` 原顺序 -> YAML `道具` 原顺序；该顺序只代表计划意图，不直接决定 prompt 的最终 `{{Image N}}`。
   - 新建视频节点时默认按 canonical order 逐张传入参考图：第一张使用 `--left <node_key>` 建立左侧输入，后续使用 `--left-add <node_key>` 顺序追加；更新既有视频节点时，必须先清理会造成编号漂移的旧左侧输入，再按 canonical order 追加。节点创建/更新后必须查询 `data.params.imageList[]` 或等价左侧输入顺序，生成 `runtime_image_placeholder_map[]`，再回写/确认 prompt。
2. `video_node.params.prompt`
   - 只能包含 `## x-y-z` 下的 Markdown 正文 + 底部完整 fenced YAML 内容；已验证 `{{Image N}}` 占位只允许出现在底部 YAML 的主体条目中。
   - 不包含 `YAML主体清单`、`主体绑定表`、参考图清单、执行锁、生成参数、文件路径、missing/excluded 诊断、审计说明或 `{{Portrait N}}` 历史占位。
   - 底部 YAML 必须完整保留原字段和值，包括 `字数统计`、`时长估算`、`角色`、`场景`、`道具` 等；不得只摘要成主体清单。
   - 每个已绑定 YAML 主体只在底部 fenced YAML 的 `角色 / 场景 / 道具` 条目主体名后插入对应占位，例如 `- 令狐冲 {{Image 1}}`；分镜组正文中的主体名不插入占位。
   - `{{Image N}}` 必须来自已查询验证的 `runtime_image_placeholder_map[]`，不得手写未登记编号；占位插入只服务参考图绑定，不改变原文剧情、句序、镜头顺序、动作结果或风格描述。
   - 不得追加 `其中，...` 复述段。
   - 不得删除或摘要上游关于机位高度、低角度、贴地前景、前景虚化、手持微晃、透视拉伸、观众发现过程、遮挡缓慢拉出等观看选择信息。

禁止项：

- 不得在 `video_node.params.prompt` 头部另写总结式创作指令。
- 不得重复追加 `StyleBible`、`StyleBible_Summary` 或相同音频约束；分镜组正文已有风格/声音要求时以正文为准。
- 不得把执行诊断、审核失败、fallback 决策或本地路径写入 prompt。
- 不得把缺失主体改写成泛化描述来继续提交。
- 不得让执行层依据上传顺序、未验证图片编号、`{{Portrait N}}` 或计划层数组顺序推断主体身份；编号只能来自已查询验证的 runtime `data.params.imageList[]` 或等价左侧输入顺序。

## Reference Generation Mode

主体参照流的视频任务必须以参考驱动方式计划。

- 只要本组 `libtv_images_count > 0`，计划必须声明“全能参考 / 多图主体参考生成视频”。
- 只要本组 `libtv_images_count > 0`，标准字段必须为 `modeType=mixed2video`。
- 如用户显式指定其他 `modeType`，必须先按 `types/type-map.md` 归一为标准称谓，并在 manifest、submit plan、queue record 和 CLI handoff 中保持一致。
- CLI handoff 必须逐项列出每张进入 LibTV 的参考图：计划层 `planned_image_index / yaml_name / category / node_key / assetId / URL / 用途`，以及查询后的 `runtime_image_index / placeholder`。
- CLI handoff 必须把所有参考图节点作为视频节点左侧输入连接；`{{Image N}}` 编号必须与查询到的 runtime `data.params.imageList[]` 或等价左侧输入顺序一致。
- 不得让执行层从自然语言自行推断参考图，也不得在有可用参考图时计划 `text2video` / 纯文生视频。
- 若 LibTV/Seedance 对某张参考图返回预处理或审核失败，默认状态为 `needs_rework / reference_asset_review_failed`；不得静默降级为无参考图纯文生视频。只有用户当前轮显式授权无参考图继续时，才允许提交 text2video fallback。

## Prompt Optimization Policy

- 默认不需要 LibTV 远端提示词优化或镜头压缩。
- `allow_libtv_prompt_optimization` 默认必须为 `false`。
- 只有用户显式要求远端优化时才改为 `true`。
- opt-in 必须记录在 submit plan、queue 和 report 中。
- 未 opt-in 时，CLI handoff 必须要求 `video_node.params.prompt` 直接使用 `5-分组` 现有组正文 + 完整 YAML，不得要求远端重排、摘要、压缩或改写剧情事实。
- 若查询发现实际节点 prompt 被压缩改写为优化版单段 prompt，应标记为 `needs_rework / remote_prompt_rewritten`；后续重提必须使用 prompt 锁定计划。

## Reference Reuse And Upload

同一 LibTV `projectUuid/projectID` 画布内，已经按同一 YAML 主体名成功上传并登记为 active 的主体图 URL 可直接复用，不要求每次重新从本地生成目录 fresh resolve 或按本地指纹命中。

active 登记的 canonical 路径固定为：

```text
projects/aigc/<项目名>/8-视频/libTV画布流/libtv-canvas-active-registry.json
```

registry schema 由 `templates/canvas-active-registry.schema.json` 定义。active 记录必须以 `projectUuid::category::yaml_name` 为 `registry_key`，且至少包含 `yaml_name / category / canvas_node_name / node_key / url / active / status / source_type / last_verified_at`。

稳定主体映射库的 canonical 路径固定为：

```text
projects/aigc/<项目名>/8-视频/libTV画布流/stable-subject-mapping.json
```

该映射库用于跨视频任务稳定绑定 `stable_subject_id -> yaml_name/category/canvas_node_name/node_key/assetId/url`。每个新视频生成前必须先读取或建立该文件；若画布资源被替换，旧主体记录不得删除，应标记 `active=false/status=replaced` 或在历史区保留，并新增 active 记录。

同名登记歧义的判定：

- 同一 `projectUuid + category + yaml_name` 存在多条 `active=true` 记录。
- 记录的 `canvas_node_name` 与当前 YAML 名或显式主体绑定表明显不一致。
- URL、`node_key` 或画布节点详情无法互相印证。

出现歧义时不得随机选择；先把候选图发送到当前窗口作为可加载上下文执行视觉消歧，仍不能唯一确认才进入 `ambiguous`。

只有以下情况才检查本地设计生成目录并计划上传：

- 缺少 active URL。
- 同名登记歧义。
- 图片被调整/更换。
- 用户明确要求“替换/更新/重新上传”。

本地目录：

```text
projects/aigc/<项目名>/6-设计/角色/3-生成
projects/aigc/<项目名>/6-设计/场景/3-生成
projects/aigc/<项目名>/6-设计/道具/3-生成
```

需要新上传时：

- 多视图优先。
- 没有多视图就主图。
- 都没有就空着并从参照图片数组中移除。
- 本地图片路径、候选集合和消歧证据只写入 manifest / submit plan，不写进 prompt 正文。

上传或手工绑定成功后必须更新 active registry；替换/更新时旧记录标记为 `active=false` 且 `status=replaced`，新记录写入 `active=true`。

## Evidence Artifacts

每个非连接件分镜组必须形成固定证据链：

```text
projects/aigc/<项目名>/8-视频/libTV画布流/libtv-canvas-active-registry.json
projects/aigc/<项目名>/8-视频/libTV画布流/stable-subject-mapping.json
projects/aigc/<项目名>/8-视频/libTV画布流/第N集/<分镜组ID>-subject-reference-manifest.json
projects/aigc/<项目名>/8-视频/libTV画布流/第N集/<分镜组ID>-libtv-submit-plan.json
projects/aigc/<项目名>/8-视频/libTV画布流/第N集/<分镜组ID>-queue-record.json
projects/aigc/<项目名>/8-视频/libTV画布流/第N集/<分镜组ID>-执行报告.md
```

artifact owner：

- `canvas-active-registry.json`：同一 LibTV 画布内主体图 active 状态真源。
- `stable-subject-mapping.json`：项目级稳定主体 ID 到画布资源 `node_key/assetId/url` 的映射库。
- `subject-reference-manifest.json`：本组主体绑定、候选、本地路径、消歧证据、预算排除、`planned_left_input_edges[]` 和进入 LibTV 的 `images[] / mixedList` 计划真源。
- `libtv-submit-plan.json`：本组 prompt 来源、duration/spec、下载策略、远端优化授权、计划层参考图和查询后的 `runtime_image_placeholder_map[]` 占位映射。
- `queue-record.json`：提交状态、`projectUuid`、`groupNodeKey`、`video_node_key`、执行 skill、命令摘要、`queried_runtime_image_map_verified`、下载状态和阻断原因。
- `执行报告.md`：面向用户的简短中文结果摘要。

`templates/subject-reference-manifest.schema.json`、`templates/submit-plan-template.md` 与 `templates/queue-record-template.md` 是对应模板。执行中如果只做 `prompt_only`，也应生成 plan/manifest 或在报告中说明未落盘原因。

## Reference Budget Decision

提交 LibTV 前必须执行参照预算裁决：

- 单组进入 `images[]` / `mixedList` 的图片最多 9 张。
- 超过时角色和场景优先。
- 先排除道具。
- 其次排除重复、不必要或可由源文本保留的次要主体。
- 在 manifest / submit plan 记录 `excluded_from_libtv_images` 或 `excluded_due_to_budget`。
- 无法合理压缩到 9 张以内时状态为 `needs_rework / reference_budget_unresolved`，不得提交。

## Duration Projection

规则固定：

| YAML 时长估算 | LibTV duration |
| --- | --- |
| `<= 4s` | `4s` |
| `4s < value < 15s` | `value` |
| `>= 15s` | `15s` |

缺失时长估算时：

1. 按组内 `分镜明细` 秒数求和估算。
2. 区间时长优先取上限。
3. 仍无法确定时回退 15 秒并记录 `duration_source=fallback_default`。

每组必须输出：

```yaml
duration_estimate_seconds: 14
duration_source: yaml_duration_estimate
duration: 14
```

## Default Specs

- `resolution=720p`
- `ratio=16:9`
- `download=false`

用户显式指定时可覆盖。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 任务是否默认进入 `subject_reference_flow`，且没有在无显式指令时切到分镜参照流或其他路线？ | `REV-LIBTVCANVAS-01` | `FAIL-ROUTE` | `N1 Intake` | route note、selected type package、用户指令摘录 |
| 每个视频任务是否可回指 `5-分组/第N集.md` 的单个 `## x-y-z` 分镜组正文与完整 fenced YAML？ | `REV-LIBTVCANVAS-02` | `FAIL-GROUP-SOURCE` | `N2 Group Extraction` | group source path、group_id、原文摘录 hash 或行号、YAML 摘录 |
| `## x-y-z~x-y-z` 连接件是否被默认忽略，没有进入视频 prompt、主体槽位、manifest、LibTV job 或文件命名？ | `REV-LIBTVCANVAS-02` | `FAIL-GROUP-SOURCE` | `N2 Group Extraction` | excluded connector list、manifest absence、queue/report skipped reason |
| prompt 主体是否直接采用 `5-分组` 组正文，没有回到早期阶段重写剧情、镜头顺序、台词或动作结果？ | `REV-LIBTVCANVAS-09` | `FAIL-SOURCE-FIDELITY` | `N2 Group Extraction` / `N3e Prompt Assembly` | source fidelity diff、params.prompt 与组正文对照、无上游重写记录 |
| 主体清单是否只来自组底 YAML 的 `角色 / 场景 / 道具`，没有把正文泛词、子串或猜测名升级为主体？ | `REV-LIBTVCANVAS-10` | `FAIL-YAML-SUBJECT` | `N3 Subject Binding` | YAML subject baseline、excluded generic terms、manifest `subject_candidates` |
| `主体绑定表` 是否包含 `stable_subject_id / planned_image_index / yaml_name / category / canvas_node_name / node_key / assetId / URL / usage`，且已验证 `{{Image N}}` 占位只进入 `video_node.params.prompt` 的底部 YAML 主体条目？ | `REV-LIBTVCANVAS-03` | `FAIL-BINDING` | `N3 Subject Binding` / `N3e Prompt Assembly` | handoff plan 绑定表、manifest `subject_bindings`、prompt hygiene check |
| 参考图计划数组、绑定表、左侧连线和稳定主体 ID 是否统一使用 canonical reference order，并在运行前由 runtime `imageList` 生成最终占位符映射？ | `REV-LIBTVCANVAS-04` / `REV-LIBTVCANVAS-16` | `FAIL-ORDER-SAFETY` / `FAIL-RUNTIME-IMAGE-MAP` | `N3 Subject Binding` / `N5 CLI Handoff` | canonical order、`planned_left_input_edges[]`、`runtime_image_placeholder_map[]`、queried node `data.params.imageList[]` 对照 |
| 有可用参考图时是否计划为 `modeType=mixed2video`，没有静默降级为纯文生视频？ | `REV-LIBTVCANVAS-14` | `FAIL-REFERENCE-MODE` | `N4 Duration/Spec` | submit plan `modeType`、reference count、fallback authorization |
| submit plan 是否把真实执行交给 `.agents/skills/cli/libTV`，而不是在本技能内执行？ | `REV-LIBTVCANVAS-07` | `FAIL-OFFICIAL-HANDOFF` | `N5 CLI Handoff` | `cli_handoff.executor_skill`、command plan、scripts 目录无 provider bridge |

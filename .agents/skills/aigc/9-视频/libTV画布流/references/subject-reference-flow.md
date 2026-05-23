# Subject Reference Flow

主体参照流是本技能默认路线。

## Source Object

基本处理对象：

```text
projects/aigc/<项目名>/6-分组/第N集.md
```

`6-分组` 是本技能的主要信息来源；不得回到 `5-摄影`、`3-Detail` 或更早阶段重写分镜组内容，除非用户显式要求修复上游。

处理粒度：

- 每个 `## x-y-z` 是一条可提交 LibTV 的分镜组视频任务。
- 完整提取组正文和底部 fenced YAML；同步提取组底 YAML 的 `时长估算`，形成 `duration_estimate_seconds`。
- 每个分镜组正文直接作为 prompt 的剧情主体提交，不重写剧情、镜头顺序、台词或动作结果。
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

正文泛词、环境描写中的普通名词不自动升级为主体参照对象。

不得用正文泛词、子串或猜测名自动扩展主体列表。名称命中多个候选图片时，先把候选图发送到当前窗口作为可加载上下文执行视觉消歧；无法唯一判定才进入 `ambiguous`。

组底 fenced YAML 必须完整保留在 `create_generation_task.params.prompt` 底部，同时还必须被投影到证据工件和参数：

- 外层 handoff message 的参考图绑定表
- `duration / duration_source`
- manifest、submit plan 和 queue record

## Subject Binding Table

外层 handoff message 和证据工件必须包含固定标题 `主体绑定表` 或等价结构化参考绑定表：

```yaml
主体绑定表:
  - yaml_name: 令狐冲
    category: 角色
    canvas_node_name: CHAR-005-令狐冲.png
    node_key: 5a9b2d1e-eb41-4ae9-a93d-9d0d5a67355c
    url: https://libtv-res.liblib.art/claw/.../CHAR.png
    usage: 按参考图保持同一男性武侠人物，作为交手主角之一
```

绑定表必须随 handoff message 提交给 LibTV Agent IM，用于构造 `source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 和画布 `@` 资产引用。绑定表不得被复制进 `create_generation_task.params.prompt`。

## Canonical Reference Order

传入 LibTV 的所有参考数组必须使用同一个 canonical order，而不是上传顺序：

1. YAML `角色` 列表原顺序。
2. YAML `场景` 列表原顺序。
3. YAML `道具` 列表原顺序。

预算裁决先决定哪些主体进入本轮参考图；排序再按上述 YAML 展示顺序保留选中主体的相对位置。`subject_bindings`、handoff message 的参考绑定表、`source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 必须一致采用该顺序。数组顺序只是辅助一致性，主体语义仍以 `yaml_name + category + node_key + URL` 绑定为准。

不得按以下顺序生成或解释参考绑定：

- 上传顺序。
- 画布节点创建时间。
- 本地文件扫描顺序。
- `Image N` / `Portrait N` / 缩略图排列。
- 先生成数组再把第 N 张图回填给第 N 个主体。

## Prompt Assembly Contract

提交给 LibTV Agent IM 的远端 handoff message 和视频节点 `params.prompt` 必须分层：

可执行模板见 `templates/libtv-remote-prompt-template.md`。

1. 外层 handoff message
   - 可包含 `把全部工作流和结果都放在画布上`、`全能参考 / 多图主体参考生成视频`、`modeType=mixed2video`、`duration / resolution / ratio / download=false`、`allow_libtv_prompt_optimization=false`、禁止优化锁定句、参考图绑定表和“不要按图片顺序匹配”的工具调用要求。
   - 必须明确要求：`create_generation_task.params.prompt` 严格等于 `VIDEO_PROMPT`，不得把 handoff message 的执行锁、生成参数、主体绑定表、缺失/排除原因或文件路径复制进 prompt。
   - 必须明确要求：参考数组按 canonical reference order 传入，即 YAML `角色` 原顺序 -> YAML `场景` 原顺序 -> YAML `道具` 原顺序；数组顺序不得来自上传顺序或画布创建顺序。
2. `create_generation_task.params.prompt`
   - 只能包含 `## x-y-z` 下的 Markdown 正文 + 底部完整 fenced YAML 内容。
   - 不包含 `YAML主体清单`、`主体绑定表`、参考图清单、执行锁、生成参数、文件路径、missing/excluded 诊断或审计说明。
   - 底部 YAML 必须完整保留原字段和值，包括 `字数统计`、`时长估算`、`角色`、`场景`、`道具` 等；不得只摘要成主体清单。
   - 每个已绑定 YAML 主体在分镜组正文第一次出现时，必须在主体名后插入 LibTV 画布 `@` 资产引用 / node mention。
   - 底部 YAML 中对应已绑定主体名后也必须插入同一 `@` 资产引用 / node mention。
   - `@` 引用必须绑定外层参考绑定表中对应主体的 `canvas_node_name / node_key / URL`；不得伪造成普通文本解释、URL 注释、`{{Portrait N}}`、`〔主体参照: ...〕` 或手写图片编号。
   - 当前 CLI `create_session.py` 只发送纯文本消息，不能单独证明 UI 级 `@` 引用已插入；若查询结果、后端工具参数或画布节点引用回显无法证明，必须记录为 `at_asset_mention_unverified`，不得报告为已完全匹配。
   - `@` 引用只用于把原文中的主体名和参考图精准相连；不得改变原文措辞、句序、镜头顺序、台词、动作结果或风格描述。
- 不追加 `其中，...` 复述段。
- 不得删除或摘要上游关于机位高度、低角度、贴地前景、前景虚化、手持微晃、透视拉伸、观众发现过程、遮挡缓慢拉出等观看选择信息；这些属于 `6-分组` 正文的镜头身份和空间感执行信息。

禁止项：

- 不得在 `params.prompt` 头部另写“严格按下列分镜组原文生成...”这类总结式创作指令。
- 不得重复追加 `StyleBible`、`StyleBible_Summary` 或相同音频约束；分镜组正文已有风格/声音要求时以正文为准。
- 不得在尾部再次复制风格、声音、字幕或背景音乐约束。
- 不得把执行诊断、审核失败、fallback 决策或本地路径写入 `params.prompt`。
- 不得把缺失主体改写成泛化描述来继续提交。
- 不得把 `allow_libtv_prompt_optimization=false` 只作为 plan/queue 字段记录而不写入 handoff message 的自然语言锁定。
- 不得让远端 Agent 依据图片上传顺序、图片编号或 `imageList` 顺序推断主体身份；主体身份只能来自主体名后的画布 `@` 资产引用和 `主体绑定表`。

## Reference Generation Mode

主体参照流的视频任务必须以参考驱动方式提交。

- 只要本组 `libtv_images_count > 0`，远端消息必须显式写明：`使用全能参考 / 多图主体参考生成视频`。
- 只要本组 `libtv_images_count > 0`，LibTV/Seedance 2.0 官方标准字段必须显式传入 `modeType=mixed2video`。
- 如用户显式指定其他 `modeType`，必须先按 `types/type-map.md` 归一为标准称谓，并在 manifest、submit plan、queue record、远端 prompt 和实际工具入参中保持一致。
- 外层 handoff message 必须逐项列出每张进入 LibTV 的参考图：`yaml_name / category / node_key / URL / 用途`。
- `主体绑定表`、外层 handoff message 中的参考图列表、manifest 中的 `libtv_images[] / mixedList` 必须一致，且按 canonical reference order 排列。
- 不得让 LibTV 后端从自然语言自行推断参考图，也不得在有可用参考图时提交或诱导 `text2video` / 纯文生视频。
- `allow_libtv_prompt_optimization=false` 只禁止远端改写、压缩或重排 prompt，不代表取消参考图或取消全能参考模式。
- 内部执行诊断和 fallback 说明不得写入 `params.prompt`，例如 `本轮不提交任何参考图 URL`、`参考图审核失败`、`改为纯文生视频`；这些只能写入 manifest、submit plan、queue record 或执行报告。
- 若 LibTV/Seedance 对某张参考图返回预处理或审核失败，默认状态为 `needs_rework / reference_asset_review_failed`，记录失败图片、URL、错误和修复项；不得静默降级为无参考图纯文生视频。只有用户当前轮显式授权无参考图继续时，才允许提交 text2video fallback。

## Prompt Optimization Policy

- 默认不需要 LibTV 远端 Agent 做提示词优化或镜头压缩。
- `allow_libtv_prompt_optimization` 默认必须为 `false`。
- 只有用户显式要求远端优化时才改为 `true`。
- opt-in 必须记录在 submit plan、queue 和 report 中。
- 未 opt-in 时，handoff message 必须要求 `params.prompt` 直接使用 `6-分组` 现有组正文 + 完整 YAML，不得要求远端重排、摘要、压缩或改写剧情事实。
- 未 opt-in 时，handoff message 还必须要求远端保留上游的观看选择信息，包括机位高度、前景/遮挡、透视、手持状态、景深和发现路径；不得把它们压缩成“人物做某动作”的动作摘要。
- 若查询发现 LibTV 远端实际 `params.prompt` 被压缩改写为优化版单段 prompt，应标记为 `needs_rework / remote_prompt_rewritten`；后续重提必须使用提示词锁定句和画布 `@` 资产引用。

## Official Terminology Evidence

当前本仓库可核验的官方/准官方字段是：画布图片节点 `name / data.name`、`node_key`、URL、`imageList / mixedList`、以及节点更新能力 `nodes_connections_batch`。公开资料和本地官方技能包尚未提供“参照图槽位”的稳定标准中文名；因此本技能内部暂用“画布 `@` 资产引用 / node mention（标准名称待官方确认）”，不得把它写成已确认的官方术语。

## Reference Reuse And Upload

同一 LibTV `projectUuid/projectID` 画布内，已经按同一 YAML 主体名成功上传并登记为 active 的主体图 URL 可直接复用，不要求每次重新从本地生成目录 fresh resolve 或按本地指纹命中。

active 登记的 canonical 路径固定为：

```text
projects/aigc/<项目名>/9-视频/libTV画布流/libtv-canvas-active-registry.json
```

registry schema 由 `templates/canvas-active-registry.schema.json` 定义。active 记录必须以 `projectUuid::category::yaml_name` 为 `registry_key`，且至少包含 `yaml_name / category / canvas_node_name / node_key / url / active / status / source_type / last_verified_at`。

同名登记歧义的判定：

- 同一 `projectUuid + category + yaml_name` 存在多条 `active=true` 记录。
- 记录的 `canvas_node_name` 与当前 YAML 名或显式主体绑定表明显不一致。
- URL、`node_key` 或画布节点详情无法互相印证。

出现歧义时不得随机选择；先把候选图发送到当前窗口作为可加载上下文执行视觉消歧，仍不能唯一确认才进入 `ambiguous`。

只有以下情况才检查本地设计生成目录并上传：

- 缺少 active URL。
- 同名登记歧义。
- 图片被调整/更换。
- 用户明确要求“替换/更新/重新上传”。

本地目录：

```text
projects/aigc/<项目名>/7-设计/角色/3-生成
projects/aigc/<项目名>/7-设计/场景/3-生成
projects/aigc/<项目名>/7-设计/道具/3-生成
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
projects/aigc/<项目名>/9-视频/libTV画布流/libtv-canvas-active-registry.json
projects/aigc/<项目名>/9-视频/libTV画布流/第N集/<分镜组ID>-subject-reference-manifest.json
projects/aigc/<项目名>/9-视频/libTV画布流/第N集/<分镜组ID>-libtv-submit-plan.json
projects/aigc/<项目名>/9-视频/libTV画布流/第N集/<分镜组ID>-queue-record.json
projects/aigc/<项目名>/9-视频/libTV画布流/第N集/<分镜组ID>-执行报告.md
```

artifact owner：

- `canvas-active-registry.json`：同一 LibTV 画布内主体图 active 状态真源。
- `subject-reference-manifest.json`：本组主体绑定、候选、本地路径、消歧证据、预算排除和进入 LibTV 的 `images[] / mixedList` 真源。
- `libtv-submit-plan.json`：本组 prompt 来源、duration/spec、下载策略、远端优化授权和官方脚本调用计划。
- `queue-record.json`：提交状态、sessionId/projectUuid/projectUrl、wrapper、官方脚本、下载状态和阻断原因。
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

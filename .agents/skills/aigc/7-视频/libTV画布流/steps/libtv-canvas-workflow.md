# LibTV Canvas Workflow

## N1 Intake

- 判断项目根、集号、分镜组范围和路线。
- 加载选中 `types/` 包。
- 加载 `types/type-map.md` 中的 Seedance 2.0 标准 `modeType` 表；若用户指定模式，先归一到标准称谓。
- Gate: 路线唯一；默认主体参照流。
- Gate: 指定 `modeType` 但无法归一为 `text2video`、`singleImage2video`、`frames2video`、`image2video`、`audio2video` 或 `mixed2video` 时阻断。

## N2 Group Extraction

- 读取 `projects/aigc/<项目名>/4-分组/第N集.md`。
- 只以 `4-分组` 为主要信息来源；不得回到 `3-摄影`、`3-Detail` 或更早阶段重写分镜组内容，除非用户显式要求修复上游。
- 完整提取每个 `## x-y-z` 的正文和 fenced YAML。
- 同步提取组底 YAML 的 `时长估算`，形成 `duration_estimate_seconds`。
- 缺失时按组内 `分镜明细` 秒数求和估算，区间时长优先取上限；仍无法确定时回退 15 秒并记录 `duration_source=fallback_default`。
- 忽略 `## x-y-z~x-y-z` 连接件；连接件不进入视频 prompt、YAML 主体槽位、主体参照 manifest、LibTV job 或视频文件命名。
- Gate: 分镜组正文和 YAML 可追溯；进入 `create_generation_task.params.prompt` 的内容为分镜组正文 + 底部完整 fenced YAML。YAML 还要同步投影到 duration、参考绑定和证据工件。

## N3 Subject Binding

- 从 YAML 的 `角色 / 场景 / 道具` 生成主体清单。
- 同步生成 `canonical_reference_order`：YAML `角色` 列表原顺序 -> YAML `场景` 列表原顺序 -> YAML `道具` 列表原顺序。
- 不得用正文泛词、子串或猜测名自动扩展主体列表。
- 读取 `projects/aigc/<项目名>/7-视频/libTV画布流/libtv-canvas-active-registry.json`；优先复用同一 LibTV `projectUuid/projectID` 画布内按同一 YAML 主体名登记为 active 的主体图 URL。
- active 主键固定为 `projectUuid::category::yaml_name`；若同一主键存在多条 `active=true` 记录，状态为同名登记歧义，不得随机选择。
- 只有缺少 active URL、同名登记歧义、图片被调整/更换或用户明确要求替换时，才检查 `5-设计/*/3-生成` 并上传。
- 新上传时多视图优先，没有多视图就主图；都没有就空着并从参照图片数组中移除。
- 名称命中多个候选时，先把候选图发送到当前窗口作为可加载上下文自动识图匹配，仍不能唯一确认才列入 `ambiguous`。
- 生成 `主体绑定表`。
- 上传或手工绑定成功后更新 active registry；替换/更新时旧记录写为 `active=false/status=replaced`，新记录写为 `active=true/status=active`。
- 本地图片路径、候选集合和消歧证据只写入 manifest / submit plan，不写进 prompt 正文。
- Gate: 每个进入参照图的主体都能由 `yaml_name + node_key + URL` 唯一锁定。
- Gate: `subject_bindings` 排序与 `canonical_reference_order` 一致；不得按上传顺序、画布创建时间或本地文件扫描顺序排序。

## N3b Evidence Artifacts

- 为每个非连接件分镜组写入 `<分镜组ID>-subject-reference-manifest.json`、`<分镜组ID>-libtv-submit-plan.json`、`<分镜组ID>-queue-record.json` 和 `<分镜组ID>-执行报告.md`。
- manifest 记录主体绑定、候选集合、本地路径、视觉消歧证据、进入 LibTV 的 `images[] / mixedList` 和排除项。
- submit plan 记录 prompt 来源、duration/spec、下载策略、远端优化授权、官方脚本计划和 wrapper。
- queue record 记录 sessionId/projectUuid/projectUrl、提交时间、状态、阻断原因和显式下载状态。
- Gate: `allow_libtv_prompt_optimization`、预算排除、active registry 复用和 official handoff 都有固定证据字段。

## N3c Reference Budget

- 单组进入 `images[]` / `mixedList` 的图片最多 9 张。
- 超过时角色和场景优先，先排除道具，其次排除重复、不必要或可由源文本保留的次要主体。
- 在 manifest / submit plan 记录 `excluded_from_libtv_images` 或 `excluded_due_to_budget`。
- 预算筛选后，保留主体必须继续按 `canonical_reference_order` 排列；排除主体只从数组中删除，不改变其余主体的相对顺序。
- Gate: 无法合理压缩到 9 张以内时状态为 `needs_rework / reference_budget_unresolved`，不得提交。

## N3d Reference Mode Lock

- 当 `libtv_images_count > 0` 时，视频提交必须锁定为“全能参考 / 多图主体参考生成视频”。
- 当 `libtv_images_count > 0` 时，标准 `modeType` 必须显式为 `mixed2video`，除非用户明确指定并可验证为其他标准 `modeType`。
- 远端消息必须包含真实参考图 `URL + node_key + yaml_name + 用途`，并与 manifest 的 `libtv_images[] / mixedList` 一致。
- 有可用参考图时不得提交或诱导 `text2video` / 纯文生视频。
- 内部诊断、审核失败、预算排除、fallback 说明只写证据工件，不写入远端创作 prompt。
- Gate: 远端消息中出现 `本轮不提交任何参考图 URL`、`没有参考图`、`改为纯文生视频` 等负面占位句时，必须阻断，不得发送。
- Gate: submit plan、queue record、manifest、远端 prompt 与实际工具入参的 `modeType` 必须一致。
- Gate: 参考图预处理或审核失败时，状态为 `needs_rework / reference_asset_review_failed`；除非用户当前轮显式授权无参考图继续，否则不得 `modeType=text2video` fallback。

## N3e Prompt Assembly

- 远端 handoff message 与 `create_generation_task.params.prompt` 必须分层组装；不得把 handoff message 整段搬进 `params.prompt`。
- 外层 handoff message 包含画布指令、全能参考模式、标准 `modeType`、duration/spec/download、`allow_libtv_prompt_optimization=false`、禁止优化自然语言锁定、参考绑定表和不按图片顺序匹配要求。
- 外层 handoff message 必须声明：`source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 已按 `canonical_reference_order` 排列，且主体语义以 `yaml_name + category + node_key + URL` 为准，不以数组下标为准。
- `create_generation_task.params.prompt` 只能包含干净创作 prompt：`## x-y-z` 下的分镜组正文 + 底部完整 fenced YAML。
- `params.prompt` 不得包含执行锁、生成参数、`YAML主体清单`、`主体绑定表`、参考图清单、missing/excluded 诊断、文件路径或审计说明。
- 底部 YAML 必须完整保留原字段和值；不得只摘要成主体清单。
- 每个已绑定 YAML 主体第一次出现在分镜组正文时，在主体名后插入 LibTV 画布 `@` 资产引用 / node mention；底部 YAML 中对应主体名后也插入同一 `@` 引用。
- `@` 引用必须绑定外层参考绑定表中对应主体的 `canvas_node_name / node_key / URL`；不得伪造成普通文本解释、URL 注释、`{{Portrait N}}`、`〔主体参照: ...〕` 或手写图片编号。
- 当前 CLI 纯文本消息无法单独证明 UI 级 `@` 引用已插入；N6 查询必须检查后端工具参数、画布节点引用回显、`source_node_keys`/URL 映射或等价证据，否则记录 `at_asset_mention_unverified`。
- 不得在 `params.prompt` 头部添加其他总结式创作指令，例如“严格按下列分镜组原文生成...”。
- 不得在头部或尾部重复追加 `StyleBible`、`StyleBible_Summary`、声音、字幕、背景音乐约束；分镜组正文已有同等内容时只保留正文里的那一次。
- 不得添加 `其中，...` 尾部复述段。
- 不得用泛化主体描述替代绑定，例如 `角色与道具按原文生成`、`令狐冲为男性武侠人物`。
- Gate: 发现 handoff message 缺少提示词锁定句或主体参照匹配句，或 `params.prompt` 缺少画布 `@` 资产引用、缺少完整 YAML、包含执行锁/生成参数/绑定表/诊断说明、重复 StyleBible/audio、出现头尾总结式重述或泛化主体替代时，必须阻断，不得发送；若当前调用面无法插入或验证 `@` 引用，必须在 plan/queue 中标记 `at_asset_mention_unverified`。
- Gate: `source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 顺序必须与 `canonical_reference_order` 的选中子集一致；若只符合上传顺序或本地文件顺序，必须阻断。

## N4 Spec Projection

- 从 YAML `时长估算` 得出 `duration`，按 4-15 秒 clamp。
- 默认 `720p`、`16:9`。
- `allow_libtv_prompt_optimization=false`，除非用户显式 opt-in；opt-in 必须写入 submit plan、queue 和 report。
- 保留音频要求，但生成后才可验收音轨。
- Gate: 每条任务都有 duration source 和最终规格。

## N5 LibTV Handoff

- 加载官方 `.agents/skills/cli/libTV`。
- 通过 `scripts/run_libtv_with_env.py` 自动加载仓库根 `.env`，确保 `LIBTV_ACCESS_KEY` 可用。
- wrapper 只转调用 `.agents/skills/cli/libTV/scripts/` 官方脚本，不改变官方脚本逻辑。
- 使用 `create_session.py` 创建或追加会话；查询、切换项目、上传和显式下载同样经 wrapper 转官方脚本。
- handoff message 必须包含画布指令、全能参考模式声明、标准 `modeType`、真实参考图 `URL/node_key`、规格参数和默认不授权远端优化声明；`params.prompt` 必须只包含分镜组正文 + 完整 YAML，并通过 N3e 去重检查。
- Gate: 使用官方脚本，不改写官方调用逻辑。

## N6 Query

- 使用 `query_session.py` 查询状态。
- 生成完成时记录视频 URL、图片 URL、node_key、task_id、sessionId、projectUuid、projectUrl。
- 若查询到 LibTV 远端实际 `create_generation_task.params.prompt` 已被压缩、摘要、重排、改写为优化版单段 prompt，或混入执行锁/生成参数/主体绑定表/诊断信息，记录 `needs_rework / remote_prompt_rewritten_or_polluted`，不得在报告中判定为 prompt fidelity 通过。
- 查询 `source_node_keys`、`source_node_url_mapping`、`imageList/mixedList`：若数组顺序与 `canonical_reference_order` 的选中子集不一致，或任一 URL/node_key 与主体绑定表不一致，记录 `needs_rework / reference_order_or_mapping_mismatch`。
- Gate: 默认不下载。

## N7 Explicit Download

- 只有用户显式要求下载或后续审片需要本地文件时，调用 `download_results.py`。
- 下载目录默认 `projects/aigc/<项目名>/7-视频/libTV画布流/第N集/`。
- Gate: 没有显式下载授权时不得落本地生成物。

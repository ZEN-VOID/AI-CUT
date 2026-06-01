# Context: C-主体参照

本文件是 `8-视频/C-主体参照` 的经验层知识库，不是过程日志。调用本技能时，应在父级 `8-视频` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 视频 prompt 回退到 `3-Detail` 或重新扩写剧情 | 输入真源层 | 回到 `5-分组/第N集.md`，重新提取组正文 | 在 `SKILL.md` 固定 `5-分组` 为主源 | prompt 可逐段回指源组 |
| 主体列表从正文泛词扩展而不是 YAML | 主体基准层 | 丢弃非 YAML 主体，重建 reference manifest | `reference-slot-binding.md` 固定 YAML baseline | manifest 的每个 subject 都能回到组底 YAML |
| 只有 JSON 设计记录却被当作图片参照 | 资产绑定层 | 移除该槽位，列入 missing | 固定“真实图片文件才可绑定” | `bound[].path` 都是存在的图片 |
| 多候选主体未经识图直接取第一个 | 视觉消歧层 | 把候选图片发送到窗口作为可加载上下文，由 LLM 在候选集合内识图选择；仍不唯一则列入 ambiguous | `reference-slot-binding.md` 固定 visual-first disambiguation | manifest 有 `visual_disambiguation[]` 或 unresolved ambiguous |
| 多视图图片存在却选择主图 | 图片优先级层 | 重新按 `多视图 -> 主图` 选择 | 搜索器和 review gate 同步检查 selected_variant | manifest 显示 `selected_variant: multi_view` |
| 单组主体参照超过 LibTV 9 图上限 | 参照预算层 | 重建 submit plan，角色和场景优先，先从道具取舍；被排除主体只保留为源文本约束 | `reference-slot-binding.md` 固定单组 9 图上限与取舍顺序 | `images[]` / `mixedList` 数量 <= 9，manifest 有 `excluded_from_libtv_images` |
| C 主体参照任务用了 `image2video` | provider modeType 层 | 改为 `modeType=mixed2video`，所有主体图进入 `mixedList[{url,type:image}]` | `libtv-handoff.md` 固定 C 专属调用锁 | 远端消息首段出现 `modeType: mixed2video` 和 `mixedList` |
| final 相位已找到并上传图片但 prompt YAML 没有对应 `uploaded_url` | prompt 绑定层 | 回到 `asset_uploads` 与最终 `generation_slots`，将原分镜组 YAML 中对应主体列表项扩展为 `name + reference_index + uploaded_url + portrait_token` | `video-prompt-assembly-contract.md` 固定 draft 不绑定、final 回刷 source-first enriched YAML | prompt 以原 `## group_id` 开头，每个进入生成槽位的 bound subject 均有真实 YAML `uploaded_url` |
| 无参照图仍传空 `upload_file.py` | 命令参数层 | 改走 `libtv_session_text_only`，移除空图片数组 | submit plan schema 禁止空槽位 | uploaded reference list 不含空图片 |
| 远端代理把主体参照生视频改成先做分镜图 / 多段视频 / 合成流程 | LibTV handoff 口径层 | 回刷 `*-libtv-submission.txt` 的 `【LibTV 调用锁定】`，直接声明 `mixed2video + mixedList` | `video-prompt-assembly-contract.md` 固定 `LibTV Remote Opening` | 远端提交文本以 `【LibTV 调用锁定】` 开头，且不含本地路径 |
| 远端画布把多张主体参照图拆成多条单图图生视频后再拼接 | provider modeType 层 | 重新提交到干净画布，明确 `modeType=mixed2video` 和 `mixedList` | C opening 不写复杂劝说，直接锁 Seedance 参数 | 查询消息中的 `create_generation_task` 为 `mixed2video` |
| 画布出现 9 个参照图框体但图片全是空壳，且没有视频生成节点 | handoff payload 层 | 检查 `mixedList` 是否还写着 `参照图N URL` 占位符；必须把上传返回的真实 URL 直接写入严格 JSON `mixedList[{"url": "...", "type": "image"}]` 后再提交 | `video-prompt-assembly-contract.md` 禁止占位符 mixedList | 查询消息出现带真实 URL 的 `create_generation_task`，或明确素材审核失败 |
| 用户确认的成功样本被后续任务误解为 A/B/D 路线 | 路由归属层 | 回到成功样本：一组一任务，直接用 `5-分组` 组正文 + YAML 主体 + 多主体参照 URL 提交给 LibTV 生视频 | C 路线调用开头直接锁定 `modeType=mixed2video` 与 `mixedList` | 远端 `create_generation_task` 为 `mixed2video`；没有 `image2video` 单图入口、storyboard/keyframe 任务或合成任务 |
| 远端消息里混入 `@projects/...` 本地图片路径 | 远端可读性层 | 远端提交只保留 final source-first enriched YAML 的 `uploaded_url`；本地路径只留在 manifest / plan / report | `libtv-handoff.md` 区分 local trace 与 remote handoff，并禁止人工预设 `参照图N` 编号 | `*-libtv-submission.txt` 本地路径关键词扫描无命中，且 final YAML uploaded_url 未丢失 |
| 批量提交后没有 sessionId 台账 | 队列治理层 | 从终端输出或 `query_session` 回填 queue ledger | LibTV 生成模式强制创建 `第N集-libtv-queue.md` | 每个 runnable group 有 queue row |
| 并发任务同时改写报告 | 汇流层 | 每组只写独立结果行，最终统一汇总报告 | workflow 固定 `N9` 汇流写报告 | 报告写入发生在 batch 完成或查询阶段 |
| 单组追加执行把集级 JSON/MD 从单组 schema 改成多组 schema | 持久化粒度层 | 迁移为 `groups/<group_id>/` 原子包，集级文件只保留 summary | output-template 固定 group package 为 canonical truth | 每个组都有独立 manifest / plan / queue / results / report |
| 单组目录平铺大量 `latest-* / corrected-* / followup-* / post-submit-* / upload-*.json` 中间文件 | 持久化噪声层 | 改用 `artifact_mode=compact`：稳定字段写 `reference-manifest.json`，多轮 query/gate 写 `libtv-results.json.attempts[]`；需要排障才展开 `debug/attempts/<attempt_id>/` | output-template 和 libtv-handoff 固定 compact 默认产物模式 | group 根目录只有 canonical 文件；原始过程证据可从 attempts 或 debug 路径追溯 |
| 用户需要打开画布但报告只给裸 `projectUrl` 或只给 `projectUuid` | 输出可用性层 | Markdown 报告和最终回执补 `canvas_link: [打开画布](<projectUrl>)`，JSON 保留 `projectUrl` 并补 `canvasMarkdown` | output-template 和 libtv-handoff 固定可点击画布链接 | queue / report / final response 中能直接点击打开画布 |
| 触发或轮询时远端返回“内容不符合平台规则”且画布没有生成节点 | 平台审核拦截层 | 不中止任务；标记 `platform_policy_rejected / needs_moderation_safe_rerun`，自动执行“平台安全重提”：保留组 ID、镜头顺序、主体参照、时长和声音要求，只对远端提交中的高风险台词/暴力/剥削表述做最小降敏；优先沿用同一 session / projectUuid 追加安全版，若同一会话不可用再新建干净画布 | post-submit gate 检测“内容不符合平台规则”；submit plan / results / report 记录 `moderation_repair`、安全版提交路径和原始拦截原因 | query 后出现生成节点、视频 URL 或明确进入 pending；原始 `5-分组` 源文件不被改写 |
| 远端 assistant 调用 `ask_user` 后停在“请稍候/等待下一条消息”，画布无生成节点 | Agent-IM 交互等待层 | 立刻标记 `stalled_remote_ask_user / no_generation_node`，不要继续等同一 session；用更短 no-ask prompt 新建干净 session | remote opening 固定禁止 ask_user，post-submit gate 强制检测 | query 后无 `ask_user` 工具调用，或失败状态不是 pending |
| 远端 query 中出现 `task_type` 或字符串型 `params` | 远端工具 envelope 观测层 | 只记录 `generation_envelope_variant`，继续按是否有明确 tool error、生成节点、视频 URL、音频证据和主体绑定裁决 | post-submit gate 不把 envelope 变体等同于投递文本失败 | 无明确 tool error 时可进入 pending；主体名+URL绑定仍保留 |
| 远端已调用 `create_generation_task` 且 tool 明确返回 `params is required` | 生成工具错误层 | 标记 `generation_tool_error`，不把该 session 当正常 pending；若 API 允许再追加纠偏，否则新建干净 session或换直达接口 | post-submit gate 只把明确 tool error 判失败，不把 envelope 变体单独判死 | tool 消息无明确错误，或错误被明确记录 |
| 远端 LibTV Agent 在提交后优化提示词、改写台词、删改音效文字、改变主体绑定、改变分镜顺序，或做摘要/重排 | 提示词保真授权层 | 标记 `prompt_fidelity_violation / libtv_optimize_without_opt_in`，新建干净 session，以 `strict_original + transport_only` 和硬锁定事实重新提交 | `video-prompt-assembly-contract.md` 和 `libtv-handoff.md` 固定严格原文模式，默认 `allow_libtv_prompt_optimization=false`，未显式 opt-in 不允许远端优化 | 远端提交开头含严格原文和硬锁定事实；query 中无台词改写、主体错绑或未授权优化/摘要重排 |
| 远端 `params.prompt` 只出现 `{{Image 1}} {{Image 2}}` / `图片1 图片2`，没有主体名称 | 主体参照绑定投影层 | 标记 `subject_reference_name_stripped`，重写 `【直接生成请求】` 为“基于下方【分镜组源文本】原始正文及其 YAML `reference_index + uploaded_url + portrait_token` 主体绑定”，并要求 final source-first enriched YAML 共同作为 prompt 完整体 | `video-prompt-assembly-contract.md` 固定 YAML `name + reference_index + uploaded_url` 绑定，禁止裸图片 token 序列 | query 中 `create_generation_task.params.prompt` 能看到主体名与图片 token/编号/URL 邻近绑定 |
| 提交文本人工写了 `参照图1/2/N`，与 LibTV 导入图片后的真实编号冲突 | 远端编号冲突层 | 重写远端提交，只写主体名 + uploaded URL；若系统自动产生真实编号，再让主体名邻近真实编号 | `video-prompt-assembly-contract.md` 和 `libtv-handoff.md` 禁止人工预设参照图编号 | `*-libtv-submission.txt` 不含人工 `参照图N`；query 中主体名未丢失 |
| 远端主体行逐条重复“生成时保持...”并把缺图/未入预算主体列表写进 LibTV prompt | 远端参照区污染层 | 重写 `libtv-submission.txt`：移除单独主体参照区，使用 final 原分镜组 YAML `uploaded_url`；连续性句只出现一次并并入直接请求；缺图/无可复用 URL/未入预算主体只写本地 manifest / report | `video-prompt-assembly-contract.md` 固定 source-first YAML 和缺图列表禁入规则，validator 扫描禁词、重复连续性句和独立连续性标题 | 远端提交不含 `无独立参照图 / 无可复用 URL / 未进入预算主体 / 不创建空图片槽`，`生成时保持` 只出现一次且位于源文本前，不单列标题 |
| 所有分镜组都被固定提交为 15 秒，短组动作拖长或节奏失真 | 时长投影层 | 回到 `5-分组` 当前组 YAML 的 `时长估算`，重建 `duration_estimate_seconds` 与 `duration_hint`；按 `clamp(估算, 4, 15)` 写入 plan 和远端提交 | `group-source-extraction.md` 和 `libtv-handoff.md` 固定组级时长估算与 4-15 秒 clamp | submit plan 有 `duration_source / duration_estimate_seconds / duration_hint`，远端 `duration` 与 `duration_hint` 一致 |
| 生成结果有视频 URL 但全静音，`task_result.audios` 为空 | 音频控制面缺失层 | 不再以生成前不可验证阻断提交；将该路径标记为 `audio_preflight_unverified_non_blocking`，生成后用音频 URL / `task_result.audios` / `ffprobe` 裁决 | `libtv-handoff.md` 固定音频预检为非阻断风险记录，最终以生成后音频验收闭环 | 生成后 `task_result.audios` 非空、存在音频 URL，或 `ffprobe` 检出 audio stream |
| 每次都按本地指纹重算后才复用同画布已上传主体图，导致批量视频生成被重复上传拖慢 | 传输层复用策略过严 | 在同一 `projectUuid/projectID` 内按 `projectUuid + category + yaml_name` 查 active uploaded URL；命中唯一 active URL 且 project scope 匹配时直接复用 | `reference-slot-binding.md` 固定同画布 active URL 复用；图片调整或用户显式要求替换才进入 `explicit_replace` 重传 | manifest / submit plan 记录 `reuse_policy=same_canvas_active_url` 或 `explicit_replace`；所有 URL `/claw/<projectUuid>/` 与当前画布一致 |
| prompt 中同一主体既在已绑定区又在缺图区，或同一 URL 静默绑定多个主体 | 引用投影一致性层 | 重建 manifest、prompt、submit plan 和远端 handoff；未声明共享关系的重复 URL 直接阻断 | `video-prompt-assembly-contract.md` 固定四件套互证和共享引用显式声明 | `validate-reference-prompt-integrity.py` 无错误，且 `images[] / mixedList / 主体 URL` 集合一致 |
| 上传图片后再切换 LibTV 画布，导致 UI 自动 `图片N` token 与主体说明错位 | LibTV project scope 层 | 废弃该轮提交；先 `change_project.py` 锁定画布，再复用当前画布 active URL 或重新上传并重建 submission | `libtv-handoff.md` 固定 `change_project -> same-canvas active URL reuse / upload_file -> render submission -> create_session`；validator 检查 `/claw/<projectUuid>/` | 每个 uploaded URL 的 claw project 与 submit plan `projectUuid` 一致 |
| post-submit query 实际 `create_generation_task.params.prompt` 与本组 prompt 不一致，出现其他组源文本或其他画布 URL | 远端会话污染层 | 不再沿用共享 session；用当前组 package 新建干净 session，并校验 query 中 prompt 包含当前 `group_id` 的源文本锚点 | `libtv-handoff.md` 要求一组一任务、post-submit gate 解析工具参数而不是只看视频 URL | query 中工具参数可回指当前组主体 URL 和当前组源文本 |
| 用户截图显示 LibTV 视频生成框 UI 缩略图顺序与 YAML / OSS 上传顺序 / 旧 `mixedList` 回显不同 | UI 槽位真源层 | 以 UI 图N / `Portrait N` 为最终 `generation_slots`；用已建立的 `asset_uploads` 反查 name-URL，回刷 YAML 的 `reference_index` 和可选 `portrait_token` 后重提 | `libtv-handoff.md` 固定 UI 槽位优先级；`validate-reference-prompt-integrity.py` 按 `reference_index` 排序校验 YAML URL | 新 query 中最新 `create_generation_task.params.mixedList` 与 UI 槽位顺序一致，远端 prompt 中主体名邻近 `reference_index` / `Portrait N` |
| 初始 `prompt.md` 已提前写入 `reference_index / uploaded_url`，后续 UI 槽位变化时正文和 YAML 全部错绑 | 槽位相位混淆层 | 把本轮 package 退回 draft/final 两相位：draft prompt 只保留原 YAML；确认 UI 图N 或最终 mixedList 后再回刷 final YAML 并重建 submission | `video-prompt-assembly-contract.md` 固定 draft 不绑定、final 回刷；`validate-reference-prompt-integrity.py --phase draft` 允许未绑定 YAML | draft 无空 URL/占位 URL；final YAML 按 `reference_index` 排序后与 `generation_slots`、`images[]`、`mixedList` 一致 |
| prompt YAML 中主体名称与参照图 URL 对不上，或 LibTV 端实际传入图与 YAML `@/uploaded_url` 对应名称错位 | 槽位注册缺失 / 匹配机制缺失 | 不按 submit plan 顺序或手写图号猜测；以 `reference-manifest.json.asset_uploads` 注册 `yaml_name -> uploaded_url`，以 `generation_slots` 注册 `reference_index / mixedList[n] -> uploaded_url -> yaml_name`，再让 prompt YAML、submit plan、远端 mixedList 逐名逐 URL 对齐；不一致时回刷 YAML 后重提 | `reference-slot-binding.md` 新增 Reference Slot Registry；`validate-reference-prompt-integrity.py` 和 `validate-post-submit-reference-order.py` 优先使用 `generation_slots` | final gate 能同时证明 `reference_index=N` 的 name 和 URL 在 YAML、manifest、images[]、mixedList 中完全一致 |

## Repair Playbook

1. 先判断失败属于输入追溯、prompt 组装、主体参照、LibTV handoff、队列台账、输出持久化还是报告闭环。
2. 若问题在剧情事实或镜头内容，回 `5-分组` 源组核对，不在本技能内补写。
3. 若问题在主体槽位，先看组底 YAML，再查 `6-设计/*/3-生成`，不要从正文猜主体。
4. 若问题在图片参照，确认真实图片文件存在，且多视图优先；名称命中多个候选时先把候选图发送到窗口作为可加载上下文做视觉消歧；只有 JSON 不算可上传图片。
4a. 若可用主体图超过单组 9 张，先保留角色和场景，再从道具里取舍；只有当排除道具后仍超过 9 张，才继续排除重复场景、次要群像或可由源文本保留的不必要主体；仍无法合理压到 9 张以内时标记 `needs_rework / reference_budget_unresolved`，不得提交。
5. 若问题在 LibTV submit plan，先看 `.agents/skills/cli/libTV/SKILL.md` 当前 Seedance `modeType` 与参照字段说明，再修 submit plan。
6. 若远端提出“先生成分镜图、分段视频、再合成”的确认门，先判定为 C 路线 route drift；不要确认该计划，先回刷远端 handoff 开头，必要时向同一 session 发送纠偏消息。
7. 若本地或远端产物已经贸然变成“单图生视频”“分镜图/关键帧生成”“多段视频合成”，不要沿该产物继续修；按 C 路线重新提交，复用可确认的 YAML 主体参照图，并显式锁定 `modeType=mixed2video` 与 `mixedList`。
8. 若任务已提交但结果未下载，保留 sessionId，按 queue ledger 调 `query_session.py`，不要重新提交造成重复任务。
8a. 若提交触发后或轮询中发现“内容不符合平台规则”，不要按失败中止，也不要改写 `5-分组` 源文件；自动生成 `libtv-submission-moderation-safe.txt` 或等价安全版远端提交，保留 source-first 事实、主体 URL、`mixedList` 顺序、时长、比例、声音要求和镜头顺序，只对远端可见的高风险辱骂、过细暴力、儿童/老人伤害、女性贩卖/剥削等表达做最小降敏；优先向同一 session 追加安全版，提交后立刻 query 并把 `moderation_repair` 写入 submit plan、queue、results 和报告。
9. 若 query 显示远端 `ask_user` 等待态，不按普通 pending 处理；同一 stalled session 不再作为恢复目标，必须新建干净 session，并使用 no-ask 远端提交文本。
10. 若 query 显示远端优化提示词、改写台词、删改音效文字、改变主体绑定、改变分镜顺序，或把原文改成“重新编排镜头 / 摘要分镜 / 工作流规划”，先看 submit plan 是否 opt-in `controlled_libtv_optimize` 或更强 `libtv_optimize`；未 opt-in 时不沿用该 session，按 `strict_original + transport_only` 和硬锁定事实新建测试 session。
11. 若 query 显示 `params.prompt` 只剩裸图片 token 或裸图片编号，说明主体绑定被弱化；修复时必须把 `【直接生成请求】` 改成基于 final source-first enriched YAML 的原始正文与 YAML `reference_index + uploaded_url + portrait_token` 主体绑定，并要求整段 `【分镜组源文本】` 一起进入 prompt。
11a. 若远端提交里每个主体行都重复 `生成时保持...`，或出现“无独立参照图、无可复用 URL、未进入预算主体、不创建空图片槽”，不要继续沿用该 session；从 manifest 重投影远端提交，主体行缩短为 `类别：主体名，主体 URL 为 URL`，连续性句只并入直接请求一次，缺图列表移回本地报告。
12. 若计划或远端提交把所有组固定为 15 秒，先查 `reference-manifest.json.group_source` 是否保留 `时长估算`；缺失时回 `5-分组` 重新提取。小于等于 4 秒统一用 4 秒，大于等于 15 秒统一用 15 秒，中间值用估算值。
13. 若当前调用面不能在生成前直接控制或验证 `params.enableSound`，记录为 `audio_preflight_unverified_non_blocking` 并继续提交；不要把该状态写成已验证有声，生成后必须用音频 URL、`task_result.audios` 或 `ffprobe` 做验收。
13a. 若生成前音频开关已验证，但视频 URL 出现后 `task_result.audios` 为空或没有音频证据，不能判定成功；先标记 `audio_unverified`，下载后 `ffprobe` 检测音轨，仍无音轨则 `audio_missing` 并重提。
14. 若同一 LibTV 画布内已存在 active uploaded URL，优先按 `projectUuid + category + yaml_name` 复用；若图片调整、更换或用户显式要求替换，再从当前 `6-设计/*/3-生成` 解析图片并重传。任何跨 `projectUuid` URL 或同名多 active URL 无裁决都不得进入远端提交。
15. 若 prompt、manifest、submit plan、remote submission 之间图片引用不一致，先运行 `validate-reference-prompt-integrity.py` 定位；修复时必须从 manifest 重投影四件套，不要手工改单个文件。
15a. 若 LibTV UI 中主体说明和 `图片N` token 对不上，先查 uploaded URL 中的 `/claw/<projectUuid>/` 是否等于 submit plan / queue / session 的 `projectUuid`；若不一致，说明 URL 来自旧画布，必须废弃并按 `change_project -> same-canvas active URL reuse / upload_file -> render submission -> create_session` 重建。
16. 修复后按 `review/review-contract.md` 复核，并在执行报告写清楚 skipped / failed / next_action。

## Reusable Heuristics

- `5-分组` 的组正文已经是生视频 prompt 的主体材料；本技能的价值在于保真组织和参照绑定，而不是再次创作剧情。
- 组底 YAML 是主体参照绑定的唯一默认入口；正文中出现的普通名词不自动变成参照对象。
- 多候选不是立刻阻断：先在候选集合内做窗口图像上下文识图，只有无法唯一确认时才保持 `ambiguous`。
- 单个分镜组给 LibTV 的主体参照图最多 9 张；超过时角色和场景优先，道具先被取舍，未进入 mixedList 的主体仍由 `5-分组` 源文本约束保留。
- LibTV 多主体参照必须落到 `modeType=mixed2video` 与 `mixedList`；prompt 中要直接保留原分镜组，draft 不绑定图N，final 只在 fenced YAML 的对应主体项下注入 `reference_index + uploaded_url + portrait_token`，提交计划负责上传并投影为 `{url,type:image}`。
- 本地 prompt 和远端 LibTV handoff 统一使用 source-first YAML；draft 不绑定图N，final 只回刷 YAML 槽位字段。不要把本地路径发给远端，也不要人工写 `参照图N`，避免和 LibTV 真实导入编号冲突。
- 远端代理容易把“分镜组原文 / 分镜明细”误判为分镜图生产计划；远端提交必须先给出 `【LibTV 调用锁定】` 和准确 `modeType`，再给源文本。
- 远端画布容易把多张参照图误路由成 `image2video`；C 必须直接锁 `modeType=mixed2video`，把图片放进 `mixedList`，不要只写“全能参照”自然语言。
- 用户确认的正确 C 路线不是 A 的“单帧/单图生视频”、不是 B 的“故事板参照”、也不是 D 或剪辑流的“多段视频合成”；它是一条组级主体参照生视频任务，核心闭环是 `5-分组组正文 -> YAML 主体 -> 多主体参照上传 -> 直接连续视频`。
- 参照图缺失不必阻断所有生成；缺图主体移出图片数组并在报告中标注，仍可 prompt-only 生成。
- 并发提交的关键不是把命令同时扔出去，而是每个 group 的 sessionId、远端状态、下载路径和 next_action 都能续查。
- 分镜组是 C 路线的最小执行真源：prompt、参照 manifest、submit plan、queue、results、report 和视频都应落在 `groups/<group_id>/`；集级 `第N集-*` 文件只做汇总，不要在单组追加时把汇总文件变成唯一真源。
- 默认不要把所有中间回显平铺到 group 根目录。长期批量生产时使用 compact 包：`reference-manifest.json` 合并 group source、subject refs、asset uploads 和 generation slots；`libtv-results.json.attempts[]` 合并 change-project、upload、create-session、query、gate 和 rerun 记录；full trace 仅在失败排障或用户要求时写入 `debug/attempts/`。
- 画布 URL 是用户操作入口，不只是机器字段；所有 Markdown 输出和最终回执都给 `[打开画布](projectUrl)`，JSON 里同时保留原始 `projectUrl` 便于脚本续查。
- “内容不符合平台规则”不是普通 pending，也不是任务终止点。它是自动平台安全重提触发器：保留本地 canonical prompt 与源组事实，另写一份远端安全提交，最小降敏可能触发平台拦截的台词/暴力/剥削表述后立即重投，并继续查询同一队列。
- 远端 `ask_user` stall 的典型结构是 assistant `content=""` 且 `toolCalls.name=ask_user`，tool 消息要求展示 question 并等待下一条消息；这不是生成排队，不能标为 `pending_remote_generation`。
- 远端 `create_generation_task` 的 envelope 变体不是投递文本真源。`task_type`、字符串型 `params` 只能作为观测项；只有明确 tool error、`params is required`、`ask_user`、无生成节点超时、主体名绑定丢失或最终无音频/视频证据，才阻断或返工。
- LibTV 的提示词优化在 C 路线中不再是默认能力。默认 `strict_original + transport_only` 且 `allow_libtv_prompt_optimization=false`：远端只能执行上传 URL、`mixedList`、时长、比例、声音等技术投影；画面表达、镜头衔接、动作连贯、光影氛围、台词、旁白、音效文字、主体绑定、分镜顺序和视频参数都必须冻结。任何远端优化、摘要或重新编排都必须来自用户显式 opt-in。
- `【直接生成请求】` 不承载“不生成字幕，不生成背景音乐”句，避免首段过载；这类视频规格保留在 `【视频默认规格】`、源文本或 provider 参数区。
- “主体参照 URL”这个说法容易让远端把图片当成匿名素材，最终 prompt 变成裸 `{{Image N}}`。远端请求应始终要求使用 final source-first enriched YAML 中的原始正文与 `name + reference_index + uploaded_url + portrait_token` 主体绑定共同构成生成 prompt 完整体；提交文本本身不得人工预设 `参照图1/2/N` 编号。
- LibTV 会把上传图片转成自己的 `图片N` token；远端主体参照区越长越容易污染 token 邻近关系。主体行必须短，连续性要求用一次总领式前缀，缺图/未入预算主体不进入远端文本。
- 视频时长是组级技术投影，不是全局固定规格；优先读取组底 `时长估算`，按 4-15 秒 clamp 后提交，避免短组被拖成 15 秒或长组越过 provider 上限。
- 音频预检不再是提交硬阻断；`enableSound:on` 仍应进入远端提交文本，若只能写自然语言“声音开启”，必须记录风险并在生成后用音频 URL、`task_result.audios` 或 `ffprobe` 验收。
- 同画布 active URL 是默认加速项：它只在当前 `projectUuid/projectID` 内复用已经上传过的同名主体图；图片内容调整、更换或用户显式要求替换时才重传。
- LibTV 上传 URL 带画布 project scope。主体参照生成必须先锁画布再上传；如果 URL 的 `/claw/<projectUuid>/` 和会话画布不同，UI 自动生成的 `图片N` token 可能会和主体名错位，即使本地 subject/url 文本顺序看起来正确。
- 图片引用四件套必须整体生成、整体审查：`reference-manifest.json`、`prompt.md`、`libtv-submit-plan.json`、`libtv-submission.txt` 任一处不一致，都应整组重建，而不是局部补丁。
- 当前可靠的 LibTV 多图匹配做法分两层：OSS 上传层只建立 `asset_uploads: name -> uploaded_url`，视频生成层再建立 `generation_slots: 图N / mixedList[n-1] -> uploaded_url -> name`。`reference_index` 属于生成槽位层，不属于 OSS 上传层；提交后读取远端 `create_generation_task.params` 复核实际顺序。
- LibTV `upload_file.py` 的返回值只有裸 URL，不包含素材名。C 路线必须在 `reference-manifest.json` 补足两层映射：`asset_uploads` 证明身份，`generation_slots` 证明图N顺序；人工核对 UI 时以 `generation_slots` 为准，不以单独显示的 `{{Portrait N}}` 反推主体。若实际 `mixedList` 顺序不同，用 URL 反查 name 后回刷 YAML 的 `reference_index` 再重提。
- 只校验 URL 集合或 submit plan 顺序会漏掉“主体名和参照图错位”。final 相位必须把 `generation_slots` 作为注册表：同一 `reference_index` 的 YAML name、YAML uploaded_url、submit plan image name、submit plan URL、远端 mixedList URL 全部相同才算通过。
- 当用户提供视频生成框截图且能看出图N缩略图主体时，截图中的 UI 图N 顺序优先级高于工具层旧 `mixedList` 回显；此时 `upload_index` 应表示生成槽位，另用 `oss_upload_index` / `upload_artifact` 保存原始上传证据，避免再次把上传层和生成槽位层混用。
- `prompt.md` 一开始可以并且应该是未绑定 draft：只保留 `5-分组` 原文和原 YAML，不写空 `reference_index`、空 `uploaded_url` 或 `{{Portrait N}}` 占位。只有拿到最终 `generation_slots` 后，才把 `prompt.md` 回刷为 final，并同步重建 `libtv-submission.txt`、submit plan 与 upload ledger。

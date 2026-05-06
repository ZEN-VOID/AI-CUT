# Context: C-主体参照

本文件是 `7-视频/C-主体参照` 的经验层知识库，不是过程日志。调用本技能时，应在父级 `7-视频` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 视频 prompt 回退到 `3-Detail` 或重新扩写剧情 | 输入真源层 | 回到 `4-分组/第N集.md`，重新提取组正文 | 在 `SKILL.md` 固定 `4-分组` 为主源 | prompt 可逐段回指源组 |
| 主体列表从正文泛词扩展而不是 YAML | 主体基准层 | 丢弃非 YAML 主体，重建 reference manifest | `reference-slot-binding.md` 固定 YAML baseline | manifest 的每个 subject 都能回到组底 YAML |
| 只有 JSON 设计记录却被当作图片参照 | 资产绑定层 | 移除该槽位，列入 missing | 固定“真实图片文件才可绑定” | `bound[].path` 都是存在的图片 |
| 多候选主体未经识图直接取第一个 | 视觉消歧层 | 把候选图片发送到窗口作为可加载上下文，由 LLM 在候选集合内识图选择；仍不唯一则列入 ambiguous | `reference-slot-binding.md` 固定 visual-first disambiguation | manifest 有 `visual_disambiguation[]` 或 unresolved ambiguous |
| 多视图图片存在却选择主图 | 图片优先级层 | 重新按 `多视图 -> 主图` 选择 | 搜索器和 review gate 同步检查 selected_variant | manifest 显示 `selected_variant: multi_view` |
| C 主体参照任务用了 `image2video` | provider modeType 层 | 改为 `modeType=mixed2video`，所有主体图进入 `mixedList[{url,type:image}]` | `libtv-handoff.md` 固定 C 专属调用锁 | 远端消息首段出现 `modeType: mixed2video` 和 `mixedList` |
| 已找到图片但 prompt 主体信息没有追加 `@图片路径` | prompt 绑定层 | 回到 reference manifest 生成 `subject_inline` 并重写主体参照说明 | `video-prompt-assembly-contract.md` 固定路径后缀规则 | prompt 中每个 bound subject 均有 `名称 @路径` |
| 无参照图仍传空 `upload_file.py` | 命令参数层 | 改走 `libtv_session_text_only`，移除空图片数组 | submit plan schema 禁止空槽位 | uploaded reference list 不含空图片 |
| 远端代理把主体参照生视频改成先做分镜图 / 多段视频 / 合成流程 | LibTV handoff 口径层 | 回刷 `*-libtv-submission.txt` 的 `【LibTV 调用锁定】`，直接声明 `mixed2video + mixedList` | `video-prompt-assembly-contract.md` 固定 `LibTV Remote Opening` | 远端提交文本以 `【LibTV 调用锁定】` 开头，且不含本地路径 |
| 远端画布把多张主体参照图拆成多条单图图生视频后再拼接 | provider modeType 层 | 重新提交到干净画布，明确 `modeType=mixed2video` 和 `mixedList` | C opening 不写复杂劝说，直接锁 Seedance 参数 | 查询消息中的 `create_generation_task` 为 `mixed2video` |
| 画布出现 9 个参照图框体但图片全是空壳，且没有视频生成节点 | handoff payload 层 | 检查 `mixedList` 是否还写着 `参照图N URL` 占位符；必须把上传返回的真实 URL 直接写入严格 JSON `mixedList[{"url": "...", "type": "image"}]` 后再提交 | `video-prompt-assembly-contract.md` 禁止占位符 mixedList | 查询消息出现带真实 URL 的 `create_generation_task`，或明确素材审核失败 |
| 用户确认的成功样本被后续任务误解为 A/B/D 路线 | 路由归属层 | 回到成功样本：一组一任务，直接用 `4-分组` 组正文 + YAML 主体 + 多主体参照 URL 提交给 LibTV 生视频 | C 路线调用开头直接锁定 `modeType=mixed2video` 与 `mixedList` | 远端 `create_generation_task` 为 `mixed2video`；没有 `image2video` 单图入口、storyboard/keyframe 任务或合成任务 |
| 远端消息里混入 `@projects/...` 本地图片路径 | 远端可读性层 | 远端提交只保留 `主体名：参照图N <uploaded_url>`，本地路径只留在审核 prompt / plan / manifest | `libtv-handoff.md` 区分 local prompt 与 remote handoff | `*-libtv-submission.txt` 本地路径关键词扫描无命中，且主体名未丢失 |
| 批量提交后没有 sessionId 台账 | 队列治理层 | 从终端输出或 `query_session` 回填 queue ledger | LibTV 生成模式强制创建 `第N集-libtv-queue.md` | 每个 runnable group 有 queue row |
| 并发任务同时改写报告 | 汇流层 | 每组只写独立结果行，最终统一汇总报告 | workflow 固定 `N9` 汇流写报告 | 报告写入发生在 batch 完成或查询阶段 |
| 单组追加执行把集级 JSON/MD 从单组 schema 改成多组 schema | 持久化粒度层 | 迁移为 `groups/<group_id>/` 原子包，集级文件只保留 summary | output-template 固定 group package 为 canonical truth | 每个组都有独立 manifest / plan / queue / results / report |
| 用户需要打开画布但报告只给裸 `projectUrl` 或只给 `projectUuid` | 输出可用性层 | Markdown 报告和最终回执补 `canvas_link: [打开画布](<projectUrl>)`，JSON 保留 `projectUrl` 并补 `canvasMarkdown` | output-template 和 libtv-handoff 固定可点击画布链接 | queue / report / final response 中能直接点击打开画布 |
| 远端 assistant 调用 `ask_user` 后停在“请稍候/等待下一条消息”，画布无生成节点 | Agent-IM 交互等待层 | 立刻标记 `stalled_remote_ask_user / no_generation_node`，不要继续等同一 session；用更短 no-ask prompt 新建干净 session | remote opening 固定禁止 ask_user，post-submit gate 强制检测 | query 后无 `ask_user` 工具调用，或失败状态不是 pending |
| 远端已调用 `create_generation_task` 但 tool 返回 `params is required` | 生成工具参数层 | 标记 `generation_tool_error`，用同 session 追加纠偏，要求使用 `taskType` 而不是 `task_type`，并保持 `params` 顶层字段 | post-submit gate 解析 tool error，不误标为正常 pending | tool 消息无 error，或错误被明确记录 |
| 远端 LibTV Agent 在提交后自行重新编排、摘要或优化分镜 | 提示词保真授权层 | 标记 `prompt_fidelity_violation / libtv_optimize_without_opt_in`，新建干净 session，以 `strict_original + transport_only` 重新提交 | `video-prompt-assembly-contract.md` 和 `libtv-handoff.md` 固定三档模式，默认 `allow_libtv_prompt_optimization=false` | 远端提交开头含 strict 原文锁；query 中无未授权优化版提示词、镜头计划或摘要分镜 |
| 远端 `params.prompt` 只出现 `{{Image 1}} {{Image 2}}` / `图片1 图片2`，没有主体名称 | 主体参照绑定投影层 | 标记 `subject_reference_name_stripped`，重写 `【直接生成请求】` 为“基于【主体参照说明】（包含主体名和主体参照 URL）+【分镜组源文本】”，并要求两者共同作为 prompt 完整体 | `video-prompt-assembly-contract.md` 固定主体名/图片 token 绑定，禁止裸图片 token 序列 | query 中 `create_generation_task.params.prompt` 能看到 `主体名 + 图片 token/编号` 邻近绑定 |

## Repair Playbook

1. 先判断失败属于输入追溯、prompt 组装、主体参照、LibTV handoff、队列台账、输出持久化还是报告闭环。
2. 若问题在剧情事实或镜头内容，回 `4-分组` 源组核对，不在本技能内补写。
3. 若问题在主体槽位，先看组底 YAML，再查 `5-设计/*/3-生成`，不要从正文猜主体。
4. 若问题在图片参照，确认真实图片文件存在，且多视图优先；名称命中多个候选时先把候选图发送到窗口作为可加载上下文做视觉消歧；只有 JSON 不算可上传图片。
5. 若问题在 LibTV submit plan，先看 `.agents/skills/cli/libTV/SKILL.md` 当前 Seedance `modeType` 与参照字段说明，再修 submit plan。
6. 若远端提出“先生成分镜图、分段视频、再合成”的确认门，先判定为 C 路线 route drift；不要确认该计划，先回刷远端 handoff 开头，必要时向同一 session 发送纠偏消息。
7. 若本地或远端产物已经贸然变成“单图生视频”“分镜图/关键帧生成”“多段视频合成”，不要沿该产物继续修；按 C 路线重新提交，复用可确认的 YAML 主体参照图，并显式锁定 `modeType=mixed2video` 与 `mixedList`。
8. 若任务已提交但结果未下载，保留 sessionId，按 queue ledger 调 `query_session.py`，不要重新提交造成重复任务。
9. 若 query 显示远端 `ask_user` 等待态，不按普通 pending 处理；同一 stalled session 不再作为恢复目标，必须新建干净 session，并使用 no-ask 远端提交文本。
10. 若 query 显示远端把原文改成“优化提示词 / 重新编排镜头 / 摘要分镜 / 工作流规划”，先看 submit plan 是否 opt-in；未 opt-in 时不沿用该 session，按 `strict_original + transport_only` 新建测试 session。
11. 若 query 显示 `params.prompt` 只剩裸图片 token 或裸图片编号，说明“主体参照 URL”描述弱化了主体名绑定；修复时必须把 `【直接生成请求】` 改成基于 `【主体参照说明】`，并要求 `【主体参照说明】 + 【分镜组源文本】` 一起进入 prompt。
12. 修复后按 `review/review-contract.md` 复核，并在执行报告写清楚 skipped / failed / next_action。

## Reusable Heuristics

- `4-分组` 的组正文已经是生视频 prompt 的主体材料；本技能的价值在于保真组织和参照绑定，而不是再次创作剧情。
- 组底 YAML 是主体参照绑定的唯一默认入口；正文中出现的普通名词不自动变成参照对象。
- 多候选不是立刻阻断：先在候选集合内做窗口图像上下文识图，只有无法唯一确认时才保持 `ambiguous`。
- LibTV 多主体参照必须落到 `modeType=mixed2video` 与 `mixedList`；prompt 中要把图片作为主体信息后缀写成 `主体名 @图片路径`，提交计划再负责上传并投影为 `{url,type:image}`。
- 本地审核 prompt 用 `主体名 @图片路径`，远端 LibTV handoff 用 `主体名：参照图N <uploaded_url>`；不要把本地路径发给远端。
- 远端代理容易把“分镜组原文 / 分镜明细”误判为分镜图生产计划；远端提交必须先给出 `【LibTV 调用锁定】` 和准确 `modeType`，再给源文本。
- 远端画布容易把多张参照图误路由成 `image2video`；C 必须直接锁 `modeType=mixed2video`，把图片放进 `mixedList`，不要只写“全能参照”自然语言。
- 用户确认的正确 C 路线不是 A 的“单帧/单图生视频”、不是 B 的“故事板参照”、也不是 D 或剪辑流的“多段视频合成”；它是一条组级主体参照生视频任务，核心闭环是 `4-分组组正文 -> YAML 主体 -> 多主体参照上传 -> 直接连续视频`。
- 参照图缺失不必阻断所有生成；缺图主体移出图片数组并在报告中标注，仍可 prompt-only 生成。
- 并发提交的关键不是把命令同时扔出去，而是每个 group 的 sessionId、远端状态、下载路径和 next_action 都能续查。
- 分镜组是 C 路线的最小执行真源：prompt、参照 manifest、submit plan、queue、results、report 和视频都应落在 `groups/<group_id>/`；集级 `第N集-*` 文件只做汇总，不要在单组追加时把汇总文件变成唯一真源。
- 画布 URL 是用户操作入口，不只是机器字段；所有 Markdown 输出和最终回执都给 `[打开画布](projectUrl)`，JSON 里同时保留原始 `projectUrl` 便于脚本续查。
- 远端 `ask_user` stall 的典型结构是 assistant `content=""` 且 `toolCalls.name=ask_user`，tool 消息要求展示 question 并等待下一条消息；这不是生成排队，不能标为 `pending_remote_generation`。
- 远端 `create_generation_task` 工具错误也不能标为正常 pending；尤其是 `params is required`，通常说明远端 agent 的工具参数 envelope 不符合 MCP schema，需要纠偏或换直达接口。
- LibTV 的提示词优化不是 C 路线默认能力。默认只允许 `strict_original + transport_only`：源文本逐字投给生成 prompt，技术层只负责 URL、mixedList 和视频参数；任何重新编排都必须来自用户显式 opt-in。
- “主体参照 URL”这个说法容易让远端把图片当成匿名素材，最终 prompt 变成裸 `{{Image N}}`。远端请求应始终写“【主体参照说明】（包含主体名和主体参照 URL）”，并要求主体参照说明与分镜组源文本共同构成生成 prompt 完整体。

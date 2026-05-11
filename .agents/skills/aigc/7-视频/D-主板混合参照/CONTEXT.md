# Context: D-主板混合参照

本文件是 `7-视频/D-主板混合参照` 的经验层知识库，不是过程日志。调用本技能时，应在父级 `7-视频` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 24000
- hard_limit_chars: 48000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| prompt 只有主体参照，缺少故事板总参照绑定 | prompt 组装层 | 回到 source-first enriched YAML，在 fenced YAML 写入 `故事板参照.uploaded_url`；故事板用途说明放在远端 `【直接生成请求】` | `hybrid-prompt-assembly-contract.md` 固定 source-first YAML 绑定 | prompt 以原组标题起笔，YAML 中出现故事板总参照绑定 |
| 故事板图被写到某个角色或道具后面 | 参照语义层 | 把故事板移回 `storyboard_total_reference` 和 prompt 开头 | `hybrid-reference-binding.md` 区分 total 与 subject role | manifest 中 storyboard role 不是 subject |
| 主体参照只进了 manifest，没有进入对应 YAML 主体项 | prompt 绑定层 | 回到 source-first YAML，给对应角色/场景/道具补 `name + uploaded_url` | review gate 检查 bound subject YAML binding | 每个 bound subject 在 fenced YAML 中可定位 |
| 主体列表从正文泛词扩展而不是组底 YAML | 主体基准层 | 丢弃非 YAML 主体，重建 reference manifest | YAML baseline 固定为主体唯一默认入口 | manifest 的每个 subject 都能回到组底 YAML |
| 没有故事板图却保留空 `@图1` | 空槽位层 | 移除空总参照 marker，记录 `storyboard_missing_optional` | submit plan schema 禁止空图片槽 | prompt 无不存在路径或空 marker |
| 图像总数超过 9 张或 LibTV 当前上限仍静默丢图 | provider handoff 层 | 标记 `reference_over_limit` / `excluded_due_to_budget`；故事板总参照优先保留，其次角色和场景优先，先排除道具，再排除重复、不必要或可由源文本保留的次要主体；无法合理压缩则阻断 | handoff 合同固定 9 图上限检查 | `mixedList` <= 9，submit plan 写明 over_limit 策略 |
| D 混合参照误用 `image2video` 或拆成 B/C | provider modeType 层 | 改为 `modeType=mixed2video`，故事板和主体图统一进入 `mixedList[{url,type:image}]`；无图才走 `text2video` | LibTV handoff 固定 D 专属调用锁 | 查询消息中的 `create_generation_task` 为 `mixed2video` |
| 并发任务同时改写报告 | 汇流层 | 每组只写独立结果行，最终统一汇总报告 | workflow 固定汇流写报告 | 报告写入发生在 batch 完成或查询阶段 |
| LibTV 远端把 D 混合参照拆成 B/C 两条路线、先做新图或多段合成 | LibTV 远端 handoff 口径层 | 回刷 `*-libtv-submission.txt`，首行加入 D 专属 `【LibTV 调用锁定】`，直接锁定 `mixed2video + mixedList` | `hybrid-prompt-assembly-contract.md` 与 `libtv-handoff.md` 固定 Remote Handoff Contract | 远端提交首段出现 `modeType: mixed2video` |
| 远端 `params.prompt` 只出现裸 `{{Image 1}} {{Image 2}}` / `图片1 图片2`，没有故事板身份或主体名称 | 混合参照投影层 | 标记 `hybrid_reference_name_stripped`，重写 `【直接生成请求】` 为“基于下方【分镜组源文本】”，并要求 source-first enriched YAML 的 `故事板参照.uploaded_url` 和主体 `uploaded_url` 与原正文共同作为 prompt 完整体 | `hybrid-prompt-assembly-contract.md` 与 `libtv-handoff.md` 固定混合参照身份/图片 token 绑定，禁止裸图片 token 序列 | query 中 `create_generation_task.params.prompt` 能看到 `故事板总参照/主体名 + 图片 token/编号` 邻近绑定 |
| 提交文本人工写了 `参照图1/2/N`，与 LibTV 导入图片后的真实编号冲突 | 远端编号冲突层 | 重写远端提交，只写故事板身份/主体名 + uploaded URL；若系统自动产生真实编号，再让故事板身份或主体名邻近真实编号 | `hybrid-prompt-assembly-contract.md` 与 `libtv-handoff.md` 禁止人工预设参照图编号 | `*-libtv-submission.txt` 不含人工 `参照图N`；故事板身份和主体名未丢失 |
| LibTV 远端在提交后自行重新编排、摘要或优化分镜 | 提示词保真授权层 | 标记 `prompt_fidelity_violation / libtv_optimize_without_opt_in`，新建干净 session，以 `strict_original + transport_only` 重新提交 | `hybrid-prompt-assembly-contract.md` 与 `libtv-handoff.md` 固定三档模式，默认 `allow_libtv_prompt_optimization=false` | 远端提交开头含 strict 原文锁；query 中无未授权优化版提示词、镜头计划或摘要分镜 |
| 所有分镜组都被固定提交为 15 秒，短组动作拖长或节奏失真 | 时长投影层 | 回到 `4-分组` 当前组 YAML 的 `时长估算`，重建 `duration_estimate_seconds` 与 `duration_hint`；按 `clamp(估算, 4, 15)` 写入 submit plan 和远端提交 | `group-source-extraction.md` 与 `libtv-handoff.md` 固定组级时长估算与 4-15 秒 clamp | submit plan 有 `duration_source / duration_estimate_seconds / duration_hint`，远端 `duration` 与 `duration_hint` 一致 |
| 远端混合参照区写入缺故事板、缺主体图、无缓存 URL 或未入预算列表 | 远端参照区污染层 | 重写远端提交：只列进入 `mixedList` 的故事板/主体名 + URL 短行；缺口和取舍说明只写本地 manifest / submit plan / report | `hybrid-prompt-assembly-contract.md` 和 `libtv-handoff.md` 固定缺口说明禁入远端参照区 | `*-libtv-submission.txt` 不含缺图/无缓存/未入预算/不创建空图片槽说明 |
| 混合参照复用历史上传缓存，导致旧故事板或旧主体图进入 `mixedList` | 缓存真源越权层 | 废弃该轮提交；先从当前 `6-图像/B-分镜故事板` 与 `5-设计/*/3-生成` fresh resolve，再按 `path + 指纹` 判断是否可复用缓存 | `hybrid-reference-binding.md` 固定缓存只作 fresh resolution 之后的传输加速 | 每个 uploaded URL 能回指当前存在本地图片、匹配指纹，且 manifest 有 `resolved_from_current_generation_dir: true` |
| 生成结果有视频 URL 但无音频证据 | 音频控制面缺失层 | 若无法在生成前验证 `create_generation_task.params.enableSound`，阻断为 `blocked_audio_control_unverified`；生成后无音频证据则 `audio_missing` | `libtv-handoff.md` 固定生成前音频控制门和下载后 `ffprobe` 验收 | 生成前可见 `params.enableSound=on/true`，生成后 `task_result.audios` 非空或 `ffprobe` 检出 audio stream |

## Repair Playbook

1. 先判断失败属于输入追溯、prompt 组装、故事板总参照、主体参照、LibTV handoff、队列台账、输出持久化还是报告闭环。
2. 若问题在剧情事实或镜头内容，回 `4-分组` 源组核对，不在本技能内补写。
3. 若问题在故事板图，按 `group_id` 查 `6-图像/B-分镜故事板`，不要把故事板当首帧或主体图。
4. 若问题在主体槽位，先看组底 YAML，再查 `5-设计/*/3-生成`，不要从正文猜主体。
5. 若问题在 prompt，先检查是否 source-first 起笔，再检查故事板和每个 bound subject 是否进入 fenced YAML 的 uploaded_url 绑定。
6. 若问题在 LibTV submit plan，先检查 D 是否锁定 `modeType=mixed2video` 和 `mixedList`，并确认 `mixedList` <= 9 且无人工 `参照图N` 编号；再看 `.agents/skills/cli/libTV/SKILL.md` 当前子命令矩阵和图片上限。
7. 若任务已提交但结果未下载，保留 sessionId，按 queue ledger 调 `query_session.py`，不要重新提交造成重复任务。
8. 修复后按 `review/review-contract.md` 复核，并在执行报告写清楚 skipped / failed / next_action。
9. 若远端代理把 D 任务解释成“先生成故事板/主体图、拆成 B/C 两条任务、多段视频再合成”，先修 `*-libtv-submission.txt` 的 `【LibTV 调用锁定】` 开头和 `mixed2video + mixedList`，再重新提交，不要补跑 B 或 C 路线。
10. 若远端 `params.prompt` 只剩裸图片 token 或裸图片编号，说明 fenced YAML 的混合参照绑定没有进入 prompt 完整体；必须把 `【直接生成请求】` 改成基于下方 `【分镜组源文本】`，并要求原正文 + YAML uploaded_url 绑定一起进入 prompt。
11. 若 query 显示远端把原文改成“优化提示词 / 重新编排镜头 / 摘要分镜 / 工作流规划”，先看 submit plan 是否 opt-in；未 opt-in 时不沿用该 session，按 `strict_original + transport_only` 新建测试 session。
12. 若 submit plan 或远端提交把所有组固定为 15 秒，先查 `第N集-hybrid-group-index.json` 是否保留 `时长估算`；缺失时回 `4-分组` 重新提取。小于等于 4 秒统一用 4 秒，大于等于 15 秒统一用 15 秒，中间值用估算值。

13. 若远端提交包含缺故事板、缺主体图、无缓存 URL、未入预算或空槽说明，先从 manifest 重投影提交文本；这些说明只留本地报告，不进入 LibTV prompt。
14. 若使用上传缓存，先确认故事板或主体已从当前本地生成目录 fresh resolve；再按 `path + source_sha256 + source_size_bytes + source_mtime_ns` 命中缓存。任何按主体名、group_id、文件名或旧 URL 命中的缓存都视为 stale。
15. 若当前调用面不能在生成前直接控制或验证 `params.enableSound`，先阻断为 `blocked_audio_control_unverified`；不要先生成再靠后验收碰运气。

## Reusable Heuristics

- D 的价值是“总参照 + 主体参照同场生效”：故事板约束整组画面连续性，主体图片约束具体角色、场景和道具外观；provider 层必须落到 `mixed2video + mixedList`。
- 故事板总参照应该出现在 prompt 开头，用来定调构图、镜头顺序、站位和节奏；它不是首帧，也不是某个角色的图片。
- 主体参照在本地审核 prompt 中必须落在 fenced YAML 对应主体列表项里，写成 `name + uploaded_url`；远端提交复用该 YAML，不要人工预设 `参照图N`，这样 LibTV 和后续审查都能知道每张图锁定谁且不和真实导入编号冲突。
- 缺故事板或缺个别主体图不必阻断 prompt-only；但空路径、错绑和静默丢图必须阻断或返工。
- 当参考图过多时，单组真实提交给 LibTV 的 `mixedList` 最多 9 张；优先保留故事板总参照和高频核心角色，角色和场景优先，道具先被取舍；压缩策略必须写入报告，不能由脚本静默裁剪。
- `第N集-libtv-submit-plan.json` 是提交前可审查真源；脚本投影是投影，不要让手写命令成为第二真源。
- LibTV 远端只需要 uploaded URL 和直接视频任务指令；本地故事板 / 主体图片路径留在 manifest / 审核 prompt，不能进入 `*-libtv-submission.txt`。
- “参照图 URL”这个说法容易让远端把故事板和主体图当成匿名素材。D 远端请求应始终让 `【分镜组源文本】` 的 fenced YAML 同时持有 `故事板参照.uploaded_url` 和主体 `uploaded_url` 绑定；不得另起混合参照说明段，也不得人工预设 `参照图1/2/N` 编号。
- LibTV 的提示词优化不是 D 路线默认能力。默认只允许 `strict_original + transport_only`：源文本逐字投给生成 prompt，技术层只负责 URL、mixedList 和视频参数；任何重新编排都必须来自用户显式 opt-in。
- 视频时长是组级技术投影，不是全局固定规格；优先读取组底 `时长估算`，按 4-15 秒 clamp 后提交。
- 混合参照远端区只服务图片 token 绑定；缺图、取舍、无缓存说明放本地报告，避免污染 LibTV 的图片引用。
- 上传缓存是高风险加速项，只能在当前本地文件已选定且指纹匹配后跳过重复上传，不能参与“选哪张图”。
- 音频是生成前控制问题，不是单纯交付验收问题；`enableSound` 必须进入真实生成任务参数，`ffprobe` 只是二次验收。

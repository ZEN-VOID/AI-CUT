# Context: B-分镜故事板参照

本文件是 `7-视频/B-分镜故事板参照` 的经验层知识库，不是过程日志。调用本技能时，应在父级 `7-视频` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 30000
- hard_limit_chars: 60000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 视频 prompt 被脚本拼接改写，偏离 `4-分组` 原文 | LLM 主创层 | 停止脚本主创，改为 LLM 保真组织并直接嵌入组正文 | `SKILL.md` 和 `references/group-source-contract.md` 固定“现有内容为主体” | prompt 可回放完整组正文 |
| 分镜组正文提取到下一个组之外、吞入连接件或漏尾部 YAML 前正文 | 组边界层 | 重新按 `## x-y-z` 普通组标题与 `## x-y-z~x-y-z` 连接件标题切块，连接件默认忽略 | 在 group index 记录 source heading、line range、body hash，并确认无连接件进入 prompt | `group_id` 唯一且正文非空 |
| 没有故事板图却写入占位图路径 | 参照绑定层 | 将该组 `reference_images` 置空，并记录 `missing_optional` | 缺图不阻断 text-to-video，不允许占位路径 | YAML 中无不存在路径 |
| 有故事板图却走 `image2video` 把故事板误当首帧 | provider modeType 层 | 改为 `modeType=singleImage2video`，故事板 URL 进入 `imageList[0]` | `libtv-handoff-contract.md` 固定 B 专属调用锁 | 远端提交首段出现 `modeType: singleImage2video` |
| B 路线未锁定 Seedance modeType | provider 路由层 | 有故事板图固定 `modeType=singleImage2video`、`imageList=[storyboard_url]`；无图固定 `text2video` | `libtv-handoff-contract.md` 固定 B 专属调用锁 | 远端消息首段出现 `modeType: singleImage2video` |
| B 路线 imageList 出现多张故事板候选或超过 9 图上限 | 参照预算层 | 回到故事板绑定，只唯一裁决 1 张故事板总参照；无法唯一裁决则阻断 | `libtv-handoff-contract.md` 固定 B 路线单图和 9 图硬上限 | `imageList` 只含 1 张故事板图且 <= 9 |
| 无参照图时仍调用 `libtv_session_with_uploaded_references` 导致必填输入失败 | provider 路由层 | 改为 `libtv_session_text_only` | YAML 根据 `reference_images` 判定 command_type | 无图 job 的 command_type 是 `libtv_session_text_only` |
| 批量并发提交后 sessionId 丢失 | 队列治理层 | 从终端输出、tasks.db 回填 queue ledger | 每个 worker 写独立临时结果，主流程汇流 | ledger 每组有 queue row 和 next_action |
| `query_session` 已成功但下载文件不完整 | 下载层 | 删除半截文件后重试下载，必要时用媒体直链 | 采用 `$libTV` 的下载超时经验 | 本地 MP4 可被读取且大小非零 |
| 多 worker 同时改写 `执行报告.md` | 并发写入层 | 改为 worker 写临时结果，最后单线程汇总 | workflow 固定 N7 并发、N8/N9 汇流 | report 只有一个最终汇总 |
| LibTV 远端把故事板参照任务改成先做故事板/分镜图、拆 panel 或多段合成 | LibTV 远端 handoff 口径层 | 回刷 `*-libtv-submission.txt`，首段加入 B 专属 `【LibTV 调用锁定】` 和 `modeType=singleImage2video` | `references/libtv-handoff-contract.md` 固定 Remote Handoff Contract | 远端提交首段出现 `modeType: singleImage2video` |
| 远端 `params.prompt` 只出现裸 `{{Image 1}}` / `图片1`，没有“故事板总参照”身份 | 故事板参照投影层 | 标记 `storyboard_reference_name_stripped`，重写 `【直接生成请求】` 为“基于下方【分镜组源文本】”，并要求 source-first enriched YAML 的 `故事板参照.uploaded_url` 与原正文共同作为 prompt 完整体 | `references/libtv-handoff-contract.md` 固定故事板身份/图片 token 绑定，禁止裸图片 token | query 中 `create_generation_task.params.prompt` 能看到 `故事板总参照 + 图片 token/编号` 邻近绑定 |
| 提交文本人工写了 `参照图1/2/N`，与 LibTV 导入图片后的真实编号冲突 | 远端编号冲突层 | 重写远端提交，只写故事板总参照 + uploaded URL；若系统自动产生真实编号，再让故事板总参照邻近真实编号 | `references/libtv-handoff-contract.md` 禁止人工预设参照图编号 | `*-libtv-submission.txt` 不含人工 `参照图N`；故事板身份未丢失 |
| LibTV 远端在提交后自行重新编排、摘要或优化分镜 | 提示词保真授权层 | 标记 `prompt_fidelity_violation / libtv_optimize_without_opt_in`，新建干净 session，以 `strict_original + transport_only` 重新提交 | `SKILL.md` 和 `libtv-handoff-contract.md` 固定三档模式，默认 `allow_libtv_prompt_optimization=false` | 远端提交开头含 strict 原文锁；query 中无未授权优化版提示词、镜头计划或摘要分镜 |
| 所有分镜组都被固定提交为 15 秒，短组动作拖长或节奏失真 | 时长投影层 | 回到 `4-分组` 当前组 `时长估算`，重建 `duration_estimate_seconds` 与 `duration_hint`；按 `clamp(估算, 4, 15)` 写入 batch 和远端提交 | `group-source-contract.md` 与 `libtv-handoff-contract.md` 固定组级时长估算与 4-15 秒 clamp | batch 有 `duration_source / duration_estimate_seconds / duration_hint`，远端 `duration` 与 `duration_hint` 一致 |
| 远端故事板参照区写入“缺失/无图/未入预算”等说明 | 远端参照区污染层 | 重写远端提交：只列进入 `imageList[0]` 的故事板总参照 + URL；缺故事板、多候选或排除原因只写本地 manifest / report | `libtv-handoff-contract.md` 固定缺口说明禁入远端参照区 | `*-libtv-submission.txt` 不含缺图/未入预算/不创建空图片槽说明 |
| 生成结果有视频 URL 但无音频证据 | 音频控制面缺失层 | 若无法在生成前验证 `create_generation_task.params.enableSound`，阻断为 `blocked_audio_control_unverified`；生成后无音频证据则 `audio_missing` | `libtv-handoff-contract.md` 固定生成前音频控制门和下载后 `ffprobe` 验收 | 生成前可见 `params.enableSound=on/true`，生成后 `task_result.audios` 非空或 `ffprobe` 检出 audio stream |

## Repair Playbook

1. 先确认当前请求是 `prompt_only`、`single_group_generate`、`episode_batch_generate`、`group_batch_generate`、`query_or_download`、`repair` 还是 `review_only`。
2. 再查 `projects/aigc/<项目名>/4-分组/第N集.md` 是否可读且目标 `group_id` 唯一。
3. 若问题在 prompt 正文，优先回 `references/group-source-contract.md`，不要用脚本补写或摘要替代原组内容。
4. 若问题在参照图，回 `references/storyboard-image-binding-contract.md`，先区分“有图唯一匹配”“无图可跳过”“多图歧义阻断”。
5. 若问题在 LibTV submit plan，回 `references/libtv-handoff-contract.md` 和 `.agents/skills/cli/libTV/SKILL.md`，先确认 `modeType=singleImage2video`、`imageList[0]`、duration、声音开关、上传 URL、`imageList` 只含 1 张故事板图且没有人工 `参照图N` 编号。
6. 若问题在批量执行，先恢复 queue ledger，再查询 LibTV 远端状态，不把终端滚屏当唯一状态来源。
7. 修复后按 `review/review-contract.md` 复核所有 gate，并在最终报告中列出非阻断事项。
8. 若远端代理把 B 任务解释成“先生成故事板图 / 拆分 panel / image2video / 多段合成”，先修 `*-libtv-submission.txt` 的 `singleImage2video` 调用锁，再重新提交，不要补跑 `6-图像/B-分镜故事板`。
9. 若远端 `params.prompt` 只剩裸图片 token 或裸图片编号，说明 fenced YAML 的故事板绑定没有进入 prompt 完整体；必须把 `【直接生成请求】` 改成基于下方 `【分镜组源文本】`，并要求原正文 + YAML `故事板参照.uploaded_url` 一起进入 prompt。
10. 若 query 显示远端把原文改成“优化提示词 / 重新编排镜头 / 摘要分镜 / 工作流规划”，先看 submit plan 是否 opt-in；未 opt-in 时不沿用该 session，按 `strict_original + transport_only` 新建测试 session。
11. 若 batch 或远端提交把所有组固定为 15 秒，先查 group index 是否保留 `时长估算`；缺失时回 `4-分组` 重新提取。小于等于 4 秒统一用 4 秒，大于等于 15 秒统一用 15 秒，中间值用估算值。

12. 若远端提交包含缺故事板、多候选未裁决、未入预算或空槽说明，先从 manifest 重投影提交文本；这些说明只留本地报告，不进入 LibTV prompt。
13. 若当前调用面不能在生成前直接控制或验证 `params.enableSound`，先阻断为 `blocked_audio_control_unverified`；不要先生成再靠后验收碰运气。

## Reusable Heuristics

- 本技能的关键不是“重新写一个视频故事”，而是把已经在 `4-分组` 中裁好的完整组内容稳定交给 LibTV。
- B 路线只有一张 storyboard sheet，总是锁定 `singleImage2video`；这里的单图不是“拆分 panel”或“多段合成”，而是单张故事板总参照进入 `imageList[0]`。
- B 路线天然满足 9 图上限，但仍必须在提交前检查 `imageList`；多张候选只能唯一裁决为 1 张或阻断。
- 缺故事板图时不应停机；这类任务天然可以降级为 `libtv_session_text_only`，但报告要写清没有图片参照。
- `第N集-libtv-batch.yaml` 是提交前的可审查真源；脚本投影是它的投影，不要让手写命令成为第二真源。
- 并发只发生在“提交/查询每个独立 group job”层；报告、结果总表和 queue ledger 的最终收敛必须单线程完成。
- LibTV short polling 不是完成承诺；批量视频默认应以 `sessionId + query_session + queue ledger` 收口。
- LibTV 远端只需要 uploaded URL 和直接视频任务指令；本地故事板图片路径留在 manifest / 审核 prompt，不能进入 `*-libtv-submission.txt`。
- “参照图 URL”这个说法容易让远端把故事板当成匿名图片。B 远端请求应始终让 `【分镜组源文本】` 的 fenced YAML 持有 `故事板参照.uploaded_url` 绑定；不得另起故事板参照说明段，也不得人工预设 `参照图1/2/N` 编号。
- LibTV 的提示词优化不是 B 路线默认能力。默认只允许 `strict_original + transport_only`：源文本逐字投给生成 prompt，技术层只负责 URL、imageList 和视频参数；任何重新编排都必须来自用户显式 opt-in。
- 视频时长是组级技术投影，不是全局固定规格；优先读取组底 `时长估算`，按 4-15 秒 clamp 后提交。
- 故事板远端参照区只服务图片 token 绑定；缺图、多候选、取舍说明放本地报告，避免污染 LibTV 的图片引用。
- 音频是生成前控制问题，不是单纯交付验收问题；`enableSound` 必须进入真实生成任务参数，`ffprobe` 只是二次验收。

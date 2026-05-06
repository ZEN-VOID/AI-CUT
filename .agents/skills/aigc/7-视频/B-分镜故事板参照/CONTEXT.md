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
| 无参照图时仍调用 `libtv_session_with_uploaded_references` 导致必填输入失败 | provider 路由层 | 改为 `libtv_session_text_only` | YAML 根据 `reference_images` 判定 command_type | 无图 job 的 command_type 是 `libtv_session_text_only` |
| 批量并发提交后 sessionId 丢失 | 队列治理层 | 从终端输出、tasks.db 回填 queue ledger | 每个 worker 写独立临时结果，主流程汇流 | ledger 每组有 queue row 和 next_action |
| `query_session` 已成功但下载文件不完整 | 下载层 | 删除半截文件后重试下载，必要时用媒体直链 | 采用 `$libTV` 的下载超时经验 | 本地 MP4 可被读取且大小非零 |
| 多 worker 同时改写 `执行报告.md` | 并发写入层 | 改为 worker 写临时结果，最后单线程汇总 | workflow 固定 N7 并发、N8/N9 汇流 | report 只有一个最终汇总 |
| LibTV 远端把故事板参照任务改成先做故事板/分镜图、拆 panel 或多段合成 | LibTV 远端 handoff 口径层 | 回刷 `*-libtv-submission.txt`，首段加入 B 专属 `【LibTV 调用锁定】` 和 `modeType=singleImage2video` | `references/libtv-handoff-contract.md` 固定 Remote Handoff Contract | 远端提交首段出现 `modeType: singleImage2video` |
| 远端 `params.prompt` 只出现裸 `{{Image 1}}` / `图片1`，没有“故事板总参照”身份 | 故事板参照投影层 | 标记 `storyboard_reference_name_stripped`，重写 `【直接生成请求】` 为“基于【故事板参照说明】（包含故事板身份和参照 URL）+【分镜组源文本】”，并要求两者共同作为 prompt 完整体 | `references/libtv-handoff-contract.md` 固定故事板身份/图片 token 绑定，禁止裸图片 token | query 中 `create_generation_task.params.prompt` 能看到 `故事板总参照 + 图片 token/编号` 邻近绑定 |
| LibTV 远端在提交后自行重新编排、摘要或优化分镜 | 提示词保真授权层 | 标记 `prompt_fidelity_violation / libtv_optimize_without_opt_in`，新建干净 session，以 `strict_original + transport_only` 重新提交 | `SKILL.md` 和 `libtv-handoff-contract.md` 固定三档模式，默认 `allow_libtv_prompt_optimization=false` | 远端提交开头含 strict 原文锁；query 中无未授权优化版提示词、镜头计划或摘要分镜 |

## Repair Playbook

1. 先确认当前请求是 `prompt_only`、`single_group_generate`、`episode_batch_generate`、`group_batch_generate`、`query_or_download`、`repair` 还是 `review_only`。
2. 再查 `projects/aigc/<项目名>/4-分组/第N集.md` 是否可读且目标 `group_id` 唯一。
3. 若问题在 prompt 正文，优先回 `references/group-source-contract.md`，不要用脚本补写或摘要替代原组内容。
4. 若问题在参照图，回 `references/storyboard-image-binding-contract.md`，先区分“有图唯一匹配”“无图可跳过”“多图歧义阻断”。
5. 若问题在 LibTV submit plan，回 `references/libtv-handoff-contract.md` 和 `.agents/skills/cli/libTV/SKILL.md`，先确认 `modeType=singleImage2video`、`imageList[0]`、duration、声音开关和上传 URL。
6. 若问题在批量执行，先恢复 queue ledger，再查询 LibTV 远端状态，不把终端滚屏当唯一状态来源。
7. 修复后按 `review/review-contract.md` 复核所有 gate，并在最终报告中列出非阻断事项。
8. 若远端代理把 B 任务解释成“先生成故事板图 / 拆分 panel / image2video / 多段合成”，先修 `*-libtv-submission.txt` 的 `singleImage2video` 调用锁，再重新提交，不要补跑 `6-图像/B-分镜故事板`。
9. 若远端 `params.prompt` 只剩裸图片 token 或裸图片编号，说明故事板参照身份没有进入 prompt 完整体；必须把 `【直接生成请求】` 改成基于 `【故事板参照说明】`，并要求 `【故事板参照说明】 + 【分镜组源文本】` 一起进入 prompt。
10. 若 query 显示远端把原文改成“优化提示词 / 重新编排镜头 / 摘要分镜 / 工作流规划”，先看 submit plan 是否 opt-in；未 opt-in 时不沿用该 session，按 `strict_original + transport_only` 新建测试 session。

## Reusable Heuristics

- 本技能的关键不是“重新写一个视频故事”，而是把已经在 `4-分组` 中裁好的完整组内容稳定交给 LibTV。
- B 路线只有一张 storyboard sheet，总是锁定 `singleImage2video`；这里的单图不是“拆分 panel”或“多段合成”，而是单张故事板总参照进入 `imageList[0]`。
- 缺故事板图时不应停机；这类任务天然可以降级为 `libtv_session_text_only`，但报告要写清没有图片参照。
- `第N集-libtv-batch.yaml` 是提交前的可审查真源；脚本投影是它的投影，不要让手写命令成为第二真源。
- 并发只发生在“提交/查询每个独立 group job”层；报告、结果总表和 queue ledger 的最终收敛必须单线程完成。
- LibTV short polling 不是完成承诺；批量视频默认应以 `sessionId + query_session + queue ledger` 收口。
- LibTV 远端只需要 uploaded URL 和直接视频任务指令；本地故事板图片路径留在 manifest / 审核 prompt，不能进入 `*-libtv-submission.txt`。
- “参照图 URL”这个说法容易让远端把故事板当成匿名图片。B 远端请求应始终写“【故事板参照说明】（包含故事板身份和参照 URL）”，并要求故事板参照说明与分镜组源文本共同构成生成 prompt 完整体。
- LibTV 的提示词优化不是 B 路线默认能力。默认只允许 `strict_original + transport_only`：源文本逐字投给生成 prompt，技术层只负责 URL、imageList 和视频参数；任何重新编排都必须来自用户显式 opt-in。

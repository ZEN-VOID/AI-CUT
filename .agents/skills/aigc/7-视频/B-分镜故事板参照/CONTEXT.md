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
| 有故事板图却走 `image2video` 把故事板误当首帧 | provider 路由层 | 改为 `libtv_session_with_uploaded_references` 并在 prompt 中声明 `@图1` 是 storyboard reference | `libtv-handoff-contract.md` 固定参照图语义 | command preview 为 `libtv_session_with_uploaded_references upload_file.py` |
| 无参照图时仍调用 `libtv_session_with_uploaded_references` 导致必填输入失败 | provider 路由层 | 改为 `libtv_session_text_only` | YAML 根据 `reference_images` 判定 command_type | 无图 job 的 command_type 是 `libtv_session_text_only` |
| 批量并发提交后 sessionId 丢失 | 队列治理层 | 从终端输出、tasks.db 回填 queue ledger | 每个 worker 写独立临时结果，主流程汇流 | ledger 每组有 queue row 和 next_action |
| `query_session` 已成功但下载文件不完整 | 下载层 | 删除半截文件后重试下载，必要时用媒体直链 | 采用 `$libTV` 的下载超时经验 | 本地 MP4 可被读取且大小非零 |
| 多 worker 同时改写 `执行报告.md` | 并发写入层 | 改为 worker 写临时结果，最后单线程汇总 | workflow 固定 N7 并发、N8/N9 汇流 | report 只有一个最终汇总 |

## Repair Playbook

1. 先确认当前请求是 `prompt_only`、`single_group_generate`、`episode_batch_generate`、`group_batch_generate`、`query_or_download`、`repair` 还是 `review_only`。
2. 再查 `projects/aigc/<项目名>/4-分组/第N集.md` 是否可读且目标 `group_id` 唯一。
3. 若问题在 prompt 正文，优先回 `references/group-source-contract.md`，不要用脚本补写或摘要替代原组内容。
4. 若问题在参照图，回 `references/storyboard-image-binding-contract.md`，先区分“有图唯一匹配”“无图可跳过”“多图歧义阻断”。
5. 若问题在 LibTV submit plan，回 `references/libtv-handoff-contract.md` 和 `.agents/skills/cli/libTV/SKILL.md`，先确认子命令、模型、duration、poll 和图片路径。
6. 若问题在批量执行，先恢复 queue ledger，再查询 LibTV 远端状态，不把终端滚屏当唯一状态来源。
7. 修复后按 `review/review-contract.md` 复核所有 gate，并在最终报告中列出非阻断事项。

## Reusable Heuristics

- 本技能的关键不是“重新写一个视频故事”，而是把已经在 `4-分组` 中裁好的完整组内容稳定交给 LibTV。
- 故事板图是参照，不是第一帧。除非用户明确要求首帧图生视频，默认不要把 storyboard sheet 交给 `image2video`。
- 缺故事板图时不应停机；这类任务天然可以降级为 `libtv_session_text_only`，但报告要写清没有图片参照。
- `第N集-libtv-batch.yaml` 是提交前的可审查真源；脚本投影是它的投影，不要让手写命令成为第二真源。
- 并发只发生在“提交/查询每个独立 group job”层；报告、结果总表和 queue ledger 的最终收敛必须单线程完成。
- LibTV short polling 不是完成承诺；批量视频默认应以 `sessionId + query_session + queue ledger` 收口。

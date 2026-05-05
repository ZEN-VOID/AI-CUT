# Context: D-主板混合参照

本文件是 `7-视频/D-主板混合参照` 的经验层知识库，不是过程日志。调用本技能时，应在父级 `7-视频` 合同之后加载本文件。

## Context Health

- soft_limit_chars: 24000
- hard_limit_chars: 48000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| prompt 只有主体参照，缺少故事板总参照固定开头 | prompt 组装层 | 补入固定开头，说明故事板用于整体构图、镜头顺序和连续性 | `hybrid-prompt-assembly-contract.md` 固定总参照开头 | prompt 首段出现故事板总参照用途 |
| 故事板图被写到某个角色或道具后面 | 参照语义层 | 把故事板移回 `storyboard_total_reference` 和 prompt 开头 | `hybrid-reference-binding.md` 区分 total 与 subject role | manifest 中 storyboard role 不是 subject |
| 主体参照只进了 manifest，没有在对应主体后追加 `@参照图` | prompt 绑定层 | 回到主体段落，给对应角色/场景/道具补 `@<path>` 或 marker 映射 | review gate 检查 bound subject inline marker | 每个 bound subject 在 prompt 中可定位 |
| 主体列表从正文泛词扩展而不是组底 YAML | 主体基准层 | 丢弃非 YAML 主体，重建 reference manifest | YAML baseline 固定为主体唯一默认入口 | manifest 的每个 subject 都能回到组底 YAML |
| 没有故事板图却保留空 `@图1` | 空槽位层 | 移除空总参照 marker，记录 `storyboard_missing_optional` | submit plan schema 禁止空图片槽 | prompt 无不存在路径或空 marker |
| 图像总数超过 LibTV 当前上限仍静默丢图 | provider handoff 层 | 标记 `reference_over_limit` 并让用户选择压缩、分段、阻断或降级 | handoff 合同固定图片上限检查 | submit plan 写明 over_limit 策略 |
| D 混合参照误用 `image2video` 或拆成 B/C | provider modeType 层 | 改为 `modeType=mixed2video`，故事板和主体图统一进入 `mixedList[{url,type:image}]`；无图才走 `text2video` | LibTV handoff 固定 D 专属调用锁 | 查询消息中的 `create_generation_task` 为 `mixed2video` |
| 并发任务同时改写报告 | 汇流层 | 每组只写独立结果行，最终统一汇总报告 | workflow 固定汇流写报告 | 报告写入发生在 batch 完成或查询阶段 |
| LibTV 远端把 D 混合参照拆成 B/C 两条路线、先做新图或多段合成 | LibTV 远端 handoff 口径层 | 回刷 `*-libtv-submission.txt`，首行加入 D 专属 `【LibTV 调用锁定】`，直接锁定 `mixed2video + mixedList` | `hybrid-prompt-assembly-contract.md` 与 `libtv-handoff.md` 固定 Remote Handoff Contract | 远端提交首段出现 `modeType: mixed2video` |

## Repair Playbook

1. 先判断失败属于输入追溯、prompt 组装、故事板总参照、主体参照、LibTV handoff、队列台账、输出持久化还是报告闭环。
2. 若问题在剧情事实或镜头内容，回 `4-分组` 源组核对，不在本技能内补写。
3. 若问题在故事板图，按 `group_id` 查 `6-图像/B-分镜故事板`，不要把故事板当首帧或主体图。
4. 若问题在主体槽位，先看组底 YAML，再查 `5-设计/*/3-生成`，不要从正文猜主体。
5. 若问题在 prompt，先检查固定开头，再检查每个 bound subject 是否在对应主体后有 `@参照图`。
6. 若问题在 LibTV submit plan，先检查 D 是否锁定 `modeType=mixed2video` 和 `mixedList`；再看 `.agents/skills/cli/libTV/SKILL.md` 当前子命令矩阵和图片上限。
7. 若任务已提交但结果未下载，保留 sessionId，按 queue ledger 调 `query_session.py`，不要重新提交造成重复任务。
8. 修复后按 `review/review-contract.md` 复核，并在执行报告写清楚 skipped / failed / next_action。
9. 若远端代理把 D 任务解释成“先生成故事板/主体图、拆成 B/C 两条任务、多段视频再合成”，先修 `*-libtv-submission.txt` 的 `【LibTV 调用锁定】` 开头和 `mixed2video + mixedList`，再重新提交，不要补跑 B 或 C 路线。

## Reusable Heuristics

- D 的价值是“总参照 + 主体参照同场生效”：故事板约束整组画面连续性，主体图片约束具体角色、场景和道具外观；provider 层必须落到 `mixed2video + mixedList`。
- 故事板总参照应该出现在 prompt 开头，用来定调构图、镜头顺序、站位和节奏；它不是首帧，也不是某个角色的图片。
- 主体参照必须跟随对应主体名出现，写成 `主体名 @图片路径` 或 `主体名 @图N`，这样 LibTV 和后续审查都能知道每张图锁定谁。
- 缺故事板或缺个别主体图不必阻断 prompt-only；但空路径、错绑和静默丢图必须阻断或返工。
- 当参考图过多时，优先保留故事板总参照和高频核心角色；压缩策略必须写入报告，不能由脚本静默裁剪。
- `第N集-libtv-submit-plan.json` 是提交前可审查真源；脚本投影是投影，不要让手写命令成为第二真源。
- LibTV 远端只需要 uploaded URL 和直接视频任务指令；本地故事板 / 主体图片路径留在 manifest / 审核 prompt，不能进入 `*-libtv-submission.txt`。

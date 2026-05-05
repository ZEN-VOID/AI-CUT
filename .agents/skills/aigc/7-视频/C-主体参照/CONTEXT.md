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
| LibTV 多参照任务用了 `image2video` 单图入口 | provider 命令层 | 改为 `libtv_session_with_uploaded_references` 并在主体信息后写 `@图片路径` | `libtv-handoff.md` 固定多参照路由 | submit plan 命令与参照数量一致 |
| 已找到图片但 prompt 主体信息没有追加 `@图片路径` | prompt 绑定层 | 回到 reference manifest 生成 `subject_inline` 并重写主体参照说明 | `video-prompt-assembly-contract.md` 固定路径后缀规则 | prompt 中每个 bound subject 均有 `名称 @路径` |
| 无参照图仍传空 `upload_file.py` | 命令参数层 | 改走 `libtv_session_text_only`，移除空图片数组 | submit plan schema 禁止空槽位 | uploaded reference list 不含空图片 |
| 批量提交后没有 sessionId 台账 | 队列治理层 | 从终端输出或 `query_session` 回填 queue ledger | LibTV 生成模式强制创建 `第N集-libtv-queue.md` | 每个 runnable group 有 queue row |
| 并发任务同时改写报告 | 汇流层 | 每组只写独立结果行，最终统一汇总报告 | workflow 固定 `N9` 汇流写报告 | 报告写入发生在 batch 完成或查询阶段 |

## Repair Playbook

1. 先判断失败属于输入追溯、prompt 组装、主体参照、LibTV handoff、队列台账、输出持久化还是报告闭环。
2. 若问题在剧情事实或镜头内容，回 `4-分组` 源组核对，不在本技能内补写。
3. 若问题在主体槽位，先看组底 YAML，再查 `5-设计/*/3-生成`，不要从正文猜主体。
4. 若问题在图片参照，确认真实图片文件存在，且多视图优先；名称命中多个候选时先把候选图发送到窗口作为可加载上下文做视觉消歧；只有 JSON 不算可上传图片。
5. 若问题在 LibTV submit plan，先看 `.agents/skills/cli/libTV/SKILL.md` 当前子命令矩阵，再修 submit plan。
6. 若任务已提交但结果未下载，保留 sessionId，按 queue ledger 调 `query_session.py`，不要重新提交造成重复任务。
7. 修复后按 `review/review-contract.md` 复核，并在执行报告写清楚 skipped / failed / next_action。

## Reusable Heuristics

- `4-分组` 的组正文已经是生视频 prompt 的主体材料；本技能的价值在于保真组织和参照绑定，而不是再次创作剧情。
- 组底 YAML 是主体参照绑定的唯一默认入口；正文中出现的普通名词不自动变成参照对象。
- 多候选不是立刻阻断：先在候选集合内做窗口图像上下文识图，只有无法唯一确认时才保持 `ambiguous`。
- LibTV 多主体参照更适合 `libtv_session_with_uploaded_references`；prompt 中要把图片作为主体信息后缀写成 `主体名 @图片路径`，提交计划再负责把同一批路径传给 `upload_file.py`。
- 参照图缺失不必阻断所有生成；缺图主体移出图片数组并在报告中标注，仍可 prompt-only 生成。
- 并发提交的关键不是把命令同时扔出去，而是每个 group 的 sessionId、远端状态、下载路径和 next_action 都能续查。

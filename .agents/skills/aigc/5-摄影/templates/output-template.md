# Output Template

## Output Contract Alignment

- Required output: 逐集摄影稿 `projects/aigc/<项目名>/5-摄影/第N集.md` 与阶段 `执行报告.md`。
- Output format: Markdown，完整保留上游编导稿，并在每个画面句子下方新增 `分镜明细：` 块；该字段名为下游兼容保留，内容语义固定为“运镜摄影设计”。
- Output path: `projects/aigc/<项目名>/5-摄影/第N集.md`、`projects/aigc/<项目名>/5-摄影/执行报告.md`。
- Naming convention: 逐集文件命名 `第N集.md`；每个分镜明细块内 `分镜N` 从 1 开始连续编号。
- Completion gate: 画面性句子覆盖、节拍合理、逐画面点归属清楚、画面节奏张弛得当、连续观看段落按需形成 `sequence_density_curve` 并记录 `density_curve_summary`、每个 `分镜N` 已内部完成 `shot_duration_decision` 并以 `分镜N（约X秒）:` 显式落盘、已应用短剧·AIGC 默认压缩偏置且 `约3秒` 以上有必要性证据、对白/旁白台词量已进入时值预算、上游高潮/爽点/高光承托已完成峰值分镜强化、内部完成临近至少前 3 个画面单位连续性回看，必要时形成段落级 `sequence_profile` 与 `unit_ownership_map` 但不改变逐句落盘边界，`shot_design_plan` 已完成 references 汇流、必要摄影参数和运镜策略已在内部锁定，分镜明细呈现动态变化、时值取舍、注意力转移、功能性影视投影、非复述型分镜、AI 视频执行稳定性、AIGC 下游可消费 payload 和自然中文表达，专业可执行、原文保真；不得输出抽象主题、心理结论、世界观解释、导演阐释、不可执行的气氛口号、随机好看句、画面内容拆写/复述、参数清单、模板句法、完整提示词分栏模板、命令式负向词、跨块外溢或失主镜头；若 review 或 validator 发现阻断项，已在 `5-摄影` 阶段内直接最小修复并复审通过，或明确记录阻断来源且不得推进下游。

## Episode Frontmatter

```yaml
---
项目名: <项目名>
集数: 第N集
stage: 5-摄影
source_performance_path: projects/aigc/<项目名>/4-表演/第N集.md
output_path: projects/aigc/<项目名>/5-摄影/第N集.md
cinematography_mode: visual_sentence_cinematography_injection
visual_matching_policy: label_and_semantic_visual_unit
sequence_alignment_policy: internal_sequence_profile_preserve_visual_unit_ownership
sequence_density_curve_policy: internal_tempo_beats_density_ramp_peak_recovery_slots
beat_policy: one_beat_point_one_storyboard_cut
peak_shot_policy: strengthen_existing_peak_visual_unit
duration_policy: short_drama_aigc_bias_explicit_approx_seconds_with_dialogue_budget
ai_video_execution_policy: camera_first_direction_referenced_lighting_result_microdynamic
non_paraphrase_policy: source_sentence_subtraction_keeps_camera_decision
language_policy: preserve_directing_text_add_shot_details
camera_design_scope: internal_camera_continuity_and_handoff_only
review_status: <pending|pass|needs_repair>
repair_status: <not_needed|repaired|blocked>
re_review_status: <not_needed|pass|needs_repair|blocked>
---
```

## Visual Unit Injection

```markdown
<原画面句子字段>：<原文完整保留>
分镜明细：
分镜1（约X秒）: <用自然中文写当前节拍的影视功能、可见主体、动作相位、镜头先行的运镜方式/速度/停点、显式时长对应的读秒/停顿/快速通过理由、构图锚点、方向参照、光线可见结果、必要表演微动态和下游可消费点；删除上游原句已有主体、动作、道具和事实后，仍能读出摄影机如何看、动、停、转焦、布光或交接；短剧·AIGC 模式下优先让镜头在 short/standard 内成立，约3秒以上必须有台词、读秒、表演变化、复杂调度、空间重置或高点证据；只显式写最关键的摄影选择。>
<仅当存在第二个真实节拍点时写 分镜2（约X秒）；若一个镜头已完成观看策略，停在 分镜1。关键揭示、动作分相、群像扩散、对白承托或高点承托可继续写 分镜3/分镜4，但每一镜都必须提供新的信息、动作相位、运镜变化、空间关系、情绪压力、台词承托、时值理由或交出锚点。>
```

若当前画面命中 `sequence_density_curve` 的 `set_piece_chain_slot` 或 `sound_cut_pattern`，可扩展到 `分镜5/分镜6`；每一镜必须有独立起点、撞点、动作结果、声音打点或反应落点，并且高密度链条后要有恢复、反压或交出锚点。该例外不得变成所有高点的固定模板。

`分镜明细：` 块内禁止写主题寓意、心理结论、世界观解释、导演阐释或不可执行的气氛口号；这些只能作为内部判断，最终必须转译为可见的运镜、摄影美学或可消费交出锚点。组间或跨场景创意转场不在本阶段落盘。

段落级连续运镜只作为内部 `sequence_profile` 使用。逐集正文必须按画面句子逐点落 `分镜明细：`：当前块只能写正上方画面句子拥有的主体、动作、道具/文字/身体锚点和对白承托；可以保留上一块交来的入口或给下一块留下可见交出锚点，但不得把后文主体动作、对白反应、记忆段、道具揭示或跨场景连接方案提前写进当前块。

每个 `分镜N（约X秒）` 必须能反推内部 `continuity_profile -> camera_grammar_plan -> functional_projection_plan -> paraphrase_subtraction_check -> ai_video_prompt_execution_profile -> shot_design_plan`：为什么有这一镜、为什么在这个顺序、从哪里进入，景别/视角/景深/焦点/镜头类型/构图/光色为什么这样变化，摄影机如何运动或为什么不动、何时停、为什么快速通过或读秒停留、是否承载对白/旁白、为什么没有被继续压短、落在哪里、如何交给下一镜或下一画面，以及下游图像/视频应消费哪些主体、动作、构图、光色、空间、时值、运镜信息、方向参照、光线结果和表演微动态。若只能写成“推进加强压迫感”之类短句，视为计划缺失，必须回到 `N6.2-CAMERA-GRAMMAR`、`N6.4-FUNCTIONAL-PROJECTION` 或 `N6.5-SHOT-PLAN`；若去掉源句事实后只剩景别词、顺序词或空泛效果词，视为画面内容拆写/复述，必须回到 `N6.4-FUNCTIONAL-PROJECTION` 重建 `paraphrase_subtraction_check`；若无法判断镜头长短、短剧·AIGC 压缩是否成立或台词量是否够用，必须回到 `N5.2-DURATION`。若连续分镜读起来像参数清单、提示词分栏或模板填空，视为自然成稿失败，必须回到 `N7-INJECT`。

模板中的可选分镜行不是占位硬要求。生成时必须先完成内部 `shot_count_decision` 和逐镜 `shot_duration_decision`，避免把所有画面句子写成固定 2 镜，也避免所有镜头同长同速；如果画面承载对白/旁白，必须先估算台词量下限，再决定 `约X秒`；短剧·AIGC 模式下 `约3秒` 以上镜头必须单独证明，不能由“慢推”“氛围”“电影感”自动成立；执行报告需记录分镜数量分布、镜头时值抽样或复判结论。

## Report Template

```markdown
# 5-摄影 执行报告

## 输入

- source_performance_path: projects/aigc/<项目名>/4-表演/第N集.md
- output_path: projects/aigc/<项目名>/5-摄影/第N集.md

## 覆盖

- 处理集数：
- 画面性句子数量：
- 分镜明细块数量：
- 分镜数量分布：
- density_curve_summary：
- set-piece 链条复判：
- 2 镜集中复判：
- review_status：

## Review Result

- 画面匹配：
- 节拍分析：
- 画面节奏：
- 段落密度曲线：
- 镜头时值：
- 短剧·AIGC 时值压缩：
- 对白台词量预算：
- 段落观看意图与逐点归属：
- 分镜数量分布：
- 高潮分镜：
- 思维·执行节点完整：
- 摄影语法变化：
- shot_design_plan 汇流：
- 功能性影视投影：
- 源句复述扣除测试：
- AI 视频执行稳定性：
- AIGC 下游可消费性：
- 分镜计划投影：
- 运镜摄影设计纯度：
- 分镜明细专业性：
- 自然成稿：
- 摄影执行参数：
- 动态流畅性：
- 临近画面连续性：
- 原文保真：
- 直接修复项：
- 复审结果：
- 下游许可：
- 残余风险：
```

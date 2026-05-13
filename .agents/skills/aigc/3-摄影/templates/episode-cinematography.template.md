# Episode Cinematography Template

```markdown
---
项目名: <项目名>
集数: 第N集
stage: 3-摄影
source_directing_path: projects/aigc/<项目名>/2-编导/第N集.md
output_path: projects/aigc/<项目名>/3-摄影/第N集.md
cinematography_mode: visual_sentence_cinematography_injection
visual_matching_policy: label_and_semantic_visual_unit
sequence_alignment_policy: internal_sequence_profile_preserve_visual_unit_ownership
beat_policy: one_beat_point_one_storyboard_cut
peak_shot_policy: strengthen_existing_peak_visual_unit
duration_policy: explicit_approx_seconds_with_dialogue_budget
ai_video_execution_policy: camera_first_direction_referenced_lighting_result_microdynamic
language_policy: preserve_directing_text_add_shot_details
camera_design_scope: internal_camera_continuity_and_handoff_only
review_status: pending
---

【剧本正文】

### 场景1：内景/外景 场所 - 日/夜

环境描写：<原文画面句子>
分镜明细：
分镜1（约X秒）: <用自然中文写当前节拍的影视功能、可见主体、动作相位、景别/视角/景深/焦点/镜头类型中的关键变化、镜头先行的运镜方式/速度/停点、显式时长对应的读秒/停顿/快速通过理由、构图锚点、方向参照、光线可见结果、必要表演微动态、连续性交接和下游可消费点；只显式写最关键的摄影选择，不粘贴完整视频提示词分栏。>
<可选：只有存在第二个真实节拍点时才写 分镜2（约X秒）；若一个镜头已完成观看策略，不补第二镜。关键揭示、动作分相、群像扩散、对白承托或高点承托可继续写 分镜3/分镜4，但每一镜都必须提供新的观看策略和时值理由。>

<!-- 若相邻画面单位共享空间、道具链、声音链、动作链、记忆插入或视觉母题，段落级 `sequence_profile` 只作为内部计划；此处仍只写正上方画面句子拥有的信息，不能吞入后文画面点。 -->
```

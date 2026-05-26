# Episode Cinematography Template

```markdown
---
项目名: <项目名>
集数: 第N集
stage: 5-摄影
source_performance_path: projects/aigc/<项目名>/4-表演/第N集.md
output_path: projects/aigc/<项目名>/5-摄影/第N集.md
cinematography_mode: visual_sentence_cinematography_injection
visual_matching_policy: label_and_semantic_visual_unit
sequence_alignment_policy: internal_sequence_profile_preserve_visual_unit_ownership
beat_policy: one_effective_trigger_one_storyboard_cut
peak_shot_policy: strengthen_existing_peak_visual_unit
duration_policy: short_drama_aigc_bias_explicit_approx_seconds_with_dialogue_budget
scene_visual_constraint_policy: composition_layout_method_lighting_color_camera_params_per_scene_internal_only
shot_detail_dimension_policy: should_have_then_write_no_force_no_fabricate
prop_shot_admission_policy: interaction_or_key_information_or_necessary_environment_only
ai_video_execution_policy: camera_first_direction_referenced_lighting_result_microdynamic
non_paraphrase_policy: source_sentence_subtraction_keeps_camera_decision
language_policy: preserve_directing_text_add_shot_details
camera_design_scope: internal_camera_continuity_and_handoff_only
review_status: pending
---

【剧本正文】

### 场景1：内景/外景 场所 - 日/夜

<从上游 4-表演 保留的环境描写/画面描写等原始字段>

环境描写：<原文画面句子>
分镜明细：
分镜1（约X秒）: <用自然中文写当前节拍的影视功能、可见主体、动作相位，以及画面中自然存在的维度信息点（角色情绪/肢体语言/语气/镜头意识等表演维度、陪体/前景/背景动态、景别/视角/景深/焦点/镜头运动等技术维度、光影变化与反射、节奏同步等——应有则有，没有不必强制），以及景别/视角/景深/焦点/镜头类型中的关键变化、镜头先行的运镜方式/速度/停点、显式时长对应的读秒/停顿/快速通过理由、构图锚点、方向参照、光线可见结果、必要表演微动态、连续性交接和下游可消费点；道具、倒影、反射、涟漪、餐具/杯子/纸张/桌面等物件细节只有在角色互动、关键信息/规则/证据/危险源或必要环境交代时才写成焦点；删除上游原句已有主体、动作、道具和事实后，仍应保留可执行摄影决策，不能只是画面内容拆写/复述；短剧·AIGC 模式下优先用 short/standard 成立，约3秒以上必须有台词、读秒、表演变化、复杂调度、空间重置或高点证据；只显式写当前画面中存在的信息，不虚构不存在的维度，不粘贴完整视频提示词分栏或维度标签列表。>
<可选：只有存在第二个有效触发点时才写 分镜2（约X秒）；快节奏平台默认一个有效触发点可成一镜。若一个镜头已完成观看策略，不补第二镜。关键揭示、动作分相、群像扩散、对白承托、平台钩子、AIGC 执行重置或高点承托可继续写 分镜3/分镜4，但每一镜都必须提供新的观看策略和时值理由。>

<!-- 若相邻画面单位共享空间、道具链、声音链、动作链、记忆插入或视觉母题，段落级 `sequence_profile` 只作为内部计划；道具链必须有互动、关键信息或必要环境理由；此处仍只写正上方画面句子拥有的信息，不能吞入后文画面点。 -->
```

---

## 示例 1：单镜低信息环境建立

```markdown
环境描写：冷白日光灯压在课桌表面，黑窗帘封住全部窗户，黑板上还留着上一节课的粉笔字。

分镜明细：
分镜1（约2秒）: 镜头从日光灯管的嗡鸣白光下降，经过黑窗帘的褶皱边缘，停在空荡课桌的第一排；桌面铅笔灰在冷白光下闪一下。
```

> 低信息环境块只需 1 镜；短剧·AIGC 模式下不把环境建立拖成长停，2 秒内完成起点、落点和可消费视觉锚点。场景视觉约束（构图布局、光源、色彩、摄影技术参数）在内部裁决，不在成稿中输出。

---

## 示例 2：对白场景焦点接力（非固定镜数）

```markdown
对白（苏红叶，低语/压迫）："你以为规则是写给你看的？"
对白画面：苏红叶的手指停在课桌边缘，红指甲压住木质纹理；林寂的视线从她的手指缓慢上移到她的嘴角。

分镜明细：
分镜1（约2秒）: 长焦压缩后排课桌，镜头贴近苏红叶停在桌沿的手指，红指甲在冷白灯下压住木纹；背景黑板字退成一片冷白。
分镜2（约2秒）: 焦点从手指滑到林寂的眼睛，他的瞳孔里映出一抹红色倒影，嘴角微微收紧。
```

> 对白画面（约 9 字台词 + 约 3 秒对白预算）；本例选择手指压力与听者反应承托潜台词，不代表对白必须两镜或必须给说话者特写。分镜 1 的落点（手指）成为分镜 2 的入口（焦点从手指滑走）。

---

## 示例 3：三镜动作序列（动作分相递进）

```markdown
角色动作：林寂猛地推开教室门，走廊里回荡着脚步声的余波，他停在门框边喘息。

分镜明细：
分镜1（约1秒）: 教室门被猛力推开，门框撞到墙壁的瞬间，镜头从门缝内侧跟随门板向右甩开，冷白光泻进走廊。
分镜2（约1.5秒）: 走廊视角，林寂从门口冲入画面左侧，长焦把身后的教室门框压成冷白矩形；肩膀被喘息顶起。
分镜3（约1.5秒）: 镜头从他僵住的肩膀后拉，露出走廊尽头的黑暗和墙上的规章制度告示牌，呼吸声落在空走廊里。
```

> 动作分相（推门 -> 冲入走廊 -> 停住喘息），每镜一个独立动作结果。短剧·AIGC 模式下动作镜压短，靠硬落点和后拉交代空间，不把喘息拖成氛围长镜。

---

## 示例 4：高点 held 镜头（读秒 + 反应）

```markdown
道具特写：黑板上的粉笔字开始自行改变，新的规则从原有笔画中生长出来。

分镜明细：
分镜1（约3秒）: 极慢推轨向黑板表面，镜头从右上角粉笔字的粗粝质感贴近，白色粉笔灰在灯光下闪烁；笔画末端开始延伸，新笔画从旧笔画里挤出来。
分镜2（约2秒）: 镜头钉在新生文字末端，焦点拉到黑板反光里的瞳孔倒影；倒影轻轻颤动，背景日光灯嗡鸣突然变响。
```

> 高点（规则入侵）允许进入 held，但短剧·AIGC 模式下先压到 3 秒读清变化，再用 2 秒反应落点承接。分镜 1 的落点（新生文字末端）成为分镜 2 的入口（焦点从文字拉到反光）。光线写成可见结果（粉笔灰闪烁、黑板反光中的瞳孔倒影），不写抽象"诡异"。

---

## 示例 5：内部 shot_design_plan 计划结构

```markdown
<!-- 内部计划示意（不进入正文落盘）：

shot_design_plan:
  visual_unit: "黑板上的粉笔字开始自行改变，新的规则从原有笔画中生长出来"
  shot_count_decision: >
    2 镜。第一镜建立文字变化的可见过程（信息揭示），
    第二镜承接角色反应并将信息钉在瞳孔反光上（表演承托 + 道具锚点）。
    如果只用 1 镜，观众会缺少"信息落到角色身上"的落点。
  shots:
    - trigger: 文字笔画开始生长
      start: 黑板右上角粉笔字的粗粝质感
      path: 极慢推轨向文字生长点
      duration: held (约3秒) -- 文字变化需要可见读秒时间；短剧·AIGC 模式下先压到 3 秒，缩短到 1.5 秒会让观众来不及看到笔画延伸
      end: 新笔画末端
	      handoff: 焦点开始拉向黑板反光
	      paraphrase_subtraction_check: 删除"粉笔字改变/规则生长"事实后，仍保留极慢推轨、微距质感、焦点拉移和反光交接
	      unit_ownership_check: 只服务当前画面句子的"粉笔字自行改变"
    - trigger: 信息完成显影
      start: 新文字末端
      path: 焦点从文字拉到黑板反光中的瞳孔倒影
      duration: standard (约2秒) -- 反应落点；缩短到 1 秒会丢失瞳孔颤抖的细节
      end: 瞳孔倒影颤抖
	      handoff: 交给下一个画面句子
	      paraphrase_subtraction_check: 删除"新文字/瞳孔倒影"事实后，仍保留焦点从文字到反光的转交和反应钉镜
	      unit_ownership_check: 不吞入后文角色动作或对白反应
-->
```

> `shot_design_plan` 是内部计划，不进入正文。它展示了 `shot_count_decision`（为什么 2 镜）、逐镜 `trigger/start/path/duration/end/handoff`、`unit_ownership_check` 和时值理由。正文只写示例 4 中的自然分镜文字。

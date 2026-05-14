# Episode Cinematography Template

```markdown
---
项目名: <项目名>
集数: 第N集
stage: 3-摄影
source_directing_path: projects/aigc/<项目名>/4-表演/第N集.md
output_path: projects/aigc/<项目名>/5-摄影/第N集.md
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

---

## 示例 1：单镜低信息环境建立

```markdown
环境描写：冷白日光灯压在课桌表面，黑窗帘封住全部窗户，黑板上还留着上一节课的粉笔字。

分镜明细：
分镜1（约3秒）: 镜头从日光灯管的嗡鸣白光缓慢下降，经过黑窗帘的褶皱边缘，最终停在空荡课桌的第一排，桌面上的铅笔灰在冷白光下有细微反光。
```

> 低信息环境块只需 1 镜；运动有起点（灯管）和落点（桌面），速度为"缓慢下降"，时值 3 秒被下降路径吃掉。

---

## 示例 2：双镜对白身体锚点（快慢接力）

```markdown
对白（苏红叶，低语/压迫）："你以为规则是写给你看的？"
对白画面：苏红叶的手指停在课桌边缘，红指甲压住木质纹理；林寂的视线从她的手指缓慢上移到她的嘴角。

分镜明细：
分镜1（约3秒）: 长焦压缩后排课桌，镜头慢慢贴近苏红叶停在桌沿的手指，红指甲在冷白灯下显得格外刺眼；背景黑板字退成一片冷白。
分镜2（约2秒）: 焦点从苏红叶的手指滑到林寂的眼睛，他的瞳孔里映出手指的红色倒影，嘴角微微收紧。
```

> 对白画面（约 9 字台词 + 约 4 秒对白预算）；分镜 1 为 standard（3 秒），分镜 2 为 short（2 秒），形成快慢接力。分镜 1 的落点（手指）成为分镜 2 的入口（焦点从手指滑走）。

---

## 示例 3：三镜动作序列（动作分相递进）

```markdown
角色动作：林寂猛地推开教室门，走廊里回荡着脚步声的余波，他停在门框边喘息。

分镜明细：
分镜1（约2秒）: 教室门被猛力推开，门框撞到墙壁的瞬间，镜头从门缝内侧跟随门板的运动向右甩开，日光灯的白光从门缝泻进走廊。
分镜2（约2秒）: 走廊视角，林寂的身影从门口冲入画面左侧，长焦压缩让他身后的教室门框变成一个冷白色矩形；他的喘息让肩膀起伏。
分镜3（约2秒）: 镜头从林寂僵住的肩膀缓慢后拉，露出走廊尽头的黑暗和墙壁上的规章制度告示牌，他的呼吸在安静的走廊里逐渐可闻。
```

> 动作分相（推门 -> 冲入走廊 -> 停住喘息），每镜一个独立动作结果。分镜 1 的落点（门板甩开）成为分镜 2 的入口（走廊视角看门口）；分镜 2 的落点（肩膀起伏）成为分镜 3 的入口（从肩膀后拉）。

---

## 示例 4：高点 held 镜头（读秒 + 反应）

```markdown
道具特写：黑板上的粉笔字开始自行改变，新的规则从原有笔画中生长出来。

分镜明细：
分镜1（约4秒）: 极慢推轨向黑板表面，镜头从黑板右上角粉笔字的粗粝质感开始，白色粉笔灰在灯光下微微闪烁；文字笔画的末端开始肉眼可见地延伸，新笔画从旧笔画中挤出来，像活物在蠕动。
分镜2（约3秒）: 镜头停在新生文字的末端，焦点慢慢拉到黑板表面的反光上，可以看到角色的瞳孔倒影在反光中微微颤抖；背景里日光灯嗡鸣声突然变得更响。
```

> 高点（规则入侵）使用 held 镜头（4 秒）给文字变化足够的读秒时间；分镜 2 为 standard（3 秒）承接反应。分镜 1 的落点（新生文字末端）成为分镜 2 的入口（焦点从文字拉到反光）。光线写成可见结果（粉笔灰闪烁、黑板反光中的瞳孔倒影），不写抽象"诡异"。

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
      duration: held (约4秒) -- 文字变化需要可见读秒时间；缩短到 2 秒会让观众来不及看到笔画延伸
      end: 新笔画末端
      handoff: 焦点开始拉向黑板反光
      unit_ownership_check: 只服务当前画面句子的"粉笔字自行改变"
    - trigger: 信息完成显影
      start: 新文字末端
      path: 焦点从文字拉到黑板反光中的瞳孔倒影
      duration: standard (约3秒) -- 反应读秒；缩短到 1 秒会丢失瞳孔颤抖的细节
      end: 瞳孔倒影颤抖
      handoff: 交给下一个画面句子
      unit_ownership_check: 不吞入后文角色动作或对白反应
-->
```

> `shot_design_plan` 是内部计划，不进入正文。它展示了 `shot_count_decision`（为什么 2 镜）、逐镜 `trigger/start/path/duration/end/handoff`、`unit_ownership_check` 和时值理由。正文只写示例 4 中的自然分镜文字。

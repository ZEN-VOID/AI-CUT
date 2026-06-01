# Episode Cinematography Template

```markdown
---
项目名: <项目名>
集数: 第N集
stage: 4-摄影
source_motion_path: projects/aigc/<项目名>/3-运动/第N集.md
fallback_source_writing_directing_path: projects/aigc/<项目名>/2-编导/第N集.md
output_path: projects/aigc/<项目名>/4-摄影/第N集.md
cinematography_mode: integrated_storyboard_picture
visual_matching_policy: label_and_semantic_visual_unit_to_storyboard_picture
duration_policy: short_drama_aigc_continuous_time_ranges_with_dialogue_budget
language_policy: preserve_dialogue_and_facts_upgrade_visual_fields_to_storyboard_picture
review_status: pending
---

【剧本正文】

### 场景1：内景/外景 场所 - 日/夜

<从上游原样保留的非画面字段、对白、音效或场景信息>

<原画面性字段标题>：
[0-2秒] <增量融合原画面事实和镜头语言：先保留当前画面的主体、动作/表演、心理/思考反应外化、姿态/服装/空间/文字/光线等必须可见事实，再写机位/构图/焦点/光线、运镜路径、速度和落点。>
[2-4秒] <仅当存在第二个有效触发点、观看结果、对白承托或叙事节奏价值时追加；上一段落点必须成为本段入口，本段末尾要留下下一字段可消费的姿态、视线、声音、光色或空间入口。>
```

> 输出中必须原样保留上游画面性字段标题，但字段正文直接展开为 `[起始秒-结束秒]` 时间段；不要另起统一的 `分镜画面：` 字段，也不要保留“原字段正文 + 附加摄影说明”的双正文。这些画面性字段的原始可见事实必须融合进对应时间段文字；`心理反应/心理变化/情绪反应/思考反应/角色思考/认知变化/内心反应` 也必须先转译为可见表演微动态，再进入时间段。不要把原描述摘要成更短的摄影说明；摄影语言必须作为新增观看路径叠加到原事实上。当前格式还承担连续性：同字段内上一段落点接下一段入口，相邻字段之间上一字段末段交给下一字段首段，但不得因此跨块吞入后文动作或对白反应。

## 示例 1：单段低信息环境建立

```markdown
环境描写：
[0-2秒] 镜头从日光灯管的嗡鸣白光下降，掠过封死黑窗帘的褶皱，停在空荡课桌第一排；桌面铅笔灰在冷白光下闪了一下。
```

## 示例 2：对白场景焦点接力

```markdown
对白（苏红叶，低语/压迫）："你以为规则是写给你看的？"

对白画面：
[0-2秒] 长焦压缩后排课桌，镜头贴近苏红叶停在桌沿的手指，红指甲在冷白灯下压住木纹；她的低语从画外压进来，背景黑板字退成一片冷白。
[2-4秒] 焦点从她的手指滑到林寂的眼睛，他的视线缓慢上移到她嘴角，瞳孔里映出一抹红色倒影，嘴角微微收紧。
```

## 示例 3：三段动作分相

```markdown
角色动作：
[0-1秒] 教室门被猛力推开，镜头从门缝内侧跟着门板向右甩开，冷白光泻进走廊。
[1-2.5秒] 走廊视角里，林寂从门口冲入画面左侧，长焦把身后的教室门框压成冷白矩形；肩膀被喘息顶起。
[2.5-4秒] 镜头从他僵住的肩膀后拉，露出走廊尽头的黑暗和墙上的规章制度告示牌，呼吸声落在空走廊里。
```

## 内部计划示意

```markdown
<!-- 内部计划，不进入正文：
shot_design_plan:
  visual_unit: "<上游画面句子>"
  source_visible_fact_map:
    must_preserve_facts: ["<必须保留的原画面可见事实>"]
    psychological_reaction_visualization_map: ["<心理/思考反应 -> 眼神/呼吸/面部肌肉/肩颈/手部/站姿/身体距离/注意力停滞/环境或道具接触>"]
    fact_to_segment_binding: ["<事实 -> 秒点/焦点/构图/运镜/光线变化>"]
  shot_count_decision: "2 段，因为第一段建立动作结果，第二段承接反应和交出点。"
  format_continuity_surface:
    segment_link: "<字段内上一段落点 -> 下一段入口>"
    field_link_chain: "<上一字段末段交出点 -> 当前字段首段入口；当前字段末段 -> 下一字段入口>"
  segments:
    - time_range: "0-2秒"
      trigger: "<触发点>"
      camera_path: "<运镜路径>"
      duration_reason: "<时值理由>"
      handoff: "<交出点>"
    - time_range: "2-4秒"
      trigger: "<第二触发点>"
      camera_path: "<运镜路径>"
      duration_reason: "<时值理由>"
      handoff: "<交出点>"
-->
```

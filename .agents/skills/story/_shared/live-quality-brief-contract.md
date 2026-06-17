# Live Quality Brief Contract

本文件是 `story2026` 的写前实时质量导向合同。它定义在正式创作（N5-CREATIVE-DRAFT / P4-CREATIVE-POLISH）前生成的轻量级质量简报的标准格式和生成规则，从"写完再查"变为"写前就知道要注意什么"。

本文件不拥有正文写权，不是独立阶段。质量简报嵌入创作 context，仅 3-5 条带优先级的提示，不增加显著 token 消耗。

## Core Principle

写前质量简报的目的是让创作者在动笔前就有质量意识，而不是在写完后才发现问题。简报基于三类信息来源动态生成：

1. **前章验收反馈**：前一章（或前卷最后一章）验收中的薄弱维度热修复提示
2. **题材特化提醒**：基于 `north_star.genre_contract` 和当前章 planning 的题材特化质量导向
3. **人物状态热点**：基于人物状态追踪器（如有）的当前出场人物快速参考

简报不替代创作，不替代 planning/contract/reference，只是让 LLM 在创作时有"此刻特别需要注意什么"的聚焦。

## Brief Format

```yaml
live_quality_brief:
  chapter_ref: "第N卷/第N章"
  rhythm_mode: "势能式 | 动能式 | 浪能式"
  prior_chapter_weak_spots:  # 前一章验收中的薄弱维度
    - dimension: "prose_reader_pull"
      score: 4
      hint: "前章读感偏弱，本章注意句群起伏和章末钩子"
  genre_specific_reminders:  # 题材特化提醒
    - category: "scene_function"
      hint: "本章为悬疑章开场，注意线索可见性和公平误导，不一次性揭秘"
    - category: "character_presence"
      hint: "避免脸色捷径和表演腔，人物反应由具体压力和欲望驱动"
  character_hotspots:  # 需要特别注意的人物
    - character: "主角A"
      current_state: "刚失去关键物件X，对人物B有未消化的愤怒"
      writing_note: "当前对话中应有回避和微攻击，而非直白表达"
    - character: "配角B"
      current_state: "能力刚突破第三层，处于不稳定期"
      writing_note: "行动时应有不稳定的表现（误触、计算偏差），不写满状态"
  quick_reminders:  # 快速提醒
    - "避免脸色捷径：用动作/呼吸/视线/空间退让替代脸红/脸白"
    - "保持POV限制：心理描写不越出当前视角角色的感知范围"
```

## Generation Rules

### 3-初稿 (N4 → N5 转换)

在 `N4-SUPERVISION` → `N5-CREATIVE-DRAFT` 之间生成质量简报：

**信息来源：**
1. `prior_chapter_weak_spots`：读取前一章（同卷或上一卷最后一章）的 `stage_acceptance_packet.dimension_scores`，筛选 score ≤ 5 的维度，生成 1-2 条热修复提示
2. `genre_specific_reminders`：基于当前章 planning 的 `scene_function`、`rhythm_mode`、`payoff_type`，读取对应题材/场景功能的特化提醒
3. `character_hotspots`：基于人物状态追踪器或角色卡+前文，筛选当前章出场且处于高压力/变化中的角色（限 2-3 人）
4. `quick_reminders`：基于题材和章型，从预定义的全局提醒池中选 2-3 条

**Token 控制：** 简报总字数控制在 500 字以内（YAML 格式），不加载额外文件。

### 4-润色 (P3 → P4 转换)

在 `P3-REPAIR-PLAN` → `P4-CREATIVE-POLISH` 之间生成质量简报：

**信息来源：**
1. `prior_chapter_weak_spots`：读取当前章初稿验收中的薄弱维度
2. `repair_patch_focus`：基于 `repair_plan` 中的 affected span 和坏点类型，生成聚焦提示
3. `genre_specific_reminders`：基于当前章的题材和场景功能
4. `quick_reminders`：特化到润色场景（如"保持初稿句群骨架"、"注意AI腔具体坏点"）

## Quick Reminder Pool

### 通用提醒池

| 提醒 | 触发条件 |
| --- | --- |
| `避免脸色捷径：用动作/呼吸/视线/空间退让替代脸红/脸白` | 人物题材、言情、甜宠 |
| `保持POV限制：心理描写不越出当前视角角色的感知范围` | 任何题材 |
| `场景颗粒少而准：选1-2个感官细节服务冲突/信息/关系，不做五感清单` | 任何题材 |
| `章末应有牵引：从本章既有压力自然长出钩子，不靠生硬断章` | 任何题材 |
| `对白带意图：试探/回避/施压/诱导，而不是纯信息说明` | 人物题材、言情 |
| `节拍有层次：动作交锋应有站位/力量/材质/代价/余波，不只写"两人交手"` | 武侠、玄幻、动作 |
| `线索可见：伏笔信息应在叙事中可被读者注意，不能只靠事后解释` | 悬疑、侦探 |
| `压力有代价：角色的选择应伴随可感知的代价，不无代价完成任务` | 任何题材 |
| `信息递进：每300-500字应有新信息、新压力或新观察，不做静态描写` | 任何题材 |
| `保留初稿骨架：润色只修坏处，不把全文磨平成平均短句` | 4-润色 场景 |

### 场景功能特化提醒

| 场景功能 | 提醒 |
| --- | --- |
| `action_combat` | 注意攻防节拍、站位距离、材质响应和动作代价，不写成镜头参数 |
| `romance_relationship` | 注意对白潜台词、身体距离、欲望与回避的张力，不写成脸红模板 |
| `horror_suspense` | 注意信息延迟、感官选择、威胁遮蔽，不靠形容词喊恐怖 |
| `mystery_clue` | 注意线索可见性、公平误导、视角限制，不让作者口吻提前解释 |
| `realism_pressure` | 注意制度/社会后果、物件证据、身份语言，不无代价胜利 |

## Owner Routing

| task_shape | owner | output |
| --- | --- | --- |
| 初稿创作前生成质量简报 | `3-初稿` (N4→N5 转换) | `live_quality_brief` YAML |
| 润色前生成质量简报 | `4-润色` (P3→P4 转换) | `live_quality_brief` YAML |
| 调整提醒池内容 | 本文件 `_shared/live-quality-brief-contract.md` | 更新提醒池 |

## Hard Rules

1. 质量简报不得替代 planning、north_star 或 reference contract 的约束力；它不是新规则源。
2. 简报条目数硬上限为 5 条（prior_chapter_weak_spots 1-2 + genre_specific 1-2 + quick_reminders 1-2），不得无限堆积。
3. 简报总字数硬上限为 500 字。
4. character_hotspots 不可包含"应该爱谁""应该恨谁"等越权创作指令；只陈述当前状态事实。
5. 若前章验收包不存在（如卷首章），prior_chapter_weak_spots 可为空，质量简报仍正常生成。
6. 质量简报仅供参考；创作者可以在合理判断下忽略某些提示，不影响验收 PASS/FAIL 判定。

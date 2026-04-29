# Chapter Planning Contract

本文件承载 `story-plan-chapter-level` 的章级业务细则。入口、输入边界、动态引用和最终 Output Contract 仍由同目录 `SKILL.md` 拥有。

## Canonical Sources

- `../SKILL.md`
- `../CONTEXT.md`
- `../../_shared/fractal-planning-layout-contract.md`
- `../../_shared/fractal-planning-output-contract.md`
- `../../_shared/timeline-design-contract.md`
- `../../_shared/suspense-design-contract.md`
- `../../_shared/rhythm-design-field-matrix.md`
- `../../../_shared/core-constraints.md`
- `../../../_shared/character-planning-bridge.md`
- `../../../_shared/chapter-rhythm-handoff-contract.md`
- `references/chapter-payoff-rules.md`
- `references/chapter-rhythm-rules.md`
- `templates/chapter-planning.template.md`
- `projects/story/<项目名>/2-卷章/整体规划.md`
- `projects/story/<项目名>/2-卷章/第N卷/卷规划.md`
- `projects/story/<项目名>/1-设定/**/*.json`

## Parent Positioning

本 child 负责：

- 锁章标题
- 锁本章故事概要
- 锁本章时间推进
- 锁本章冲突
- 锁本章爽点设计
- 锁本章悬念开关
- 锁本章节奏曲线
- 锁 `selected_pack / selected_mode`
- 锁 `mode_selection_reason`
- 锁 `payoff_type / rhythm_intensity / previous_next_contrast`
- 锁七步职责映射与四个节奏义务
- 区分义务段位与建议写法
- 锁本章登场人物 / 主要场景 / 关键道具
- 锁本章任务线
- 锁本章线索
- 锁本章伏笔
- 锁章末达成与规避

它不负责：

- 越权改写卷级职责
- 越权重写整部总纲
- 直接写正文、对白、叙述段落或正文桥段

## Business Requirement Analysis Contract

| analysis_slot | 当前结论 |
| --- | --- |
| `business_goal` | 把卷级规划继续放大到单章执行蓝图，但仍停留在规划层。 |
| `business_object` | `2-卷章/第N卷/第N章.md`、所属 `2-卷章/第N卷/卷规划.md`、`2-卷章/整体规划.md`、`Cards` 真源。 |
| `constraint_profile` | 章级时间推进必须继承卷级 `本卷时间线`，锁清章前状态、章内可见时间跨度、事件顺序、幕后同步事件、章末状态与下一章 handoff；章级爽点必须按 `references/chapter-payoff-rules.md` 与 `types/payoff-genre-type-map.md` 锁清读者期待、上承 promise、类型画像、角色锚点、爽点形态、通用差异轴、蓄势、兑现动作、满足差值、夸张逻辑、代价余波与余味牵引；章级悬念开关必须继承卷级 `本卷悬念开关`，锁清读者可知、角色可知、需要隐藏、误导/疑阵、揭秘、只埋不揭、章末压力与正文禁区；高超对决额外锁定对决差异轴；章级节奏必须按 shared handoff contract 锁清 `selected_pack / selected_mode / mode_selection_reason / payoff_type / rhythm_intensity / previous_next_contrast / 七步职责映射 / 规划义务 / 义务段位 / 建议写法`，并继续延续“七步结构 + 动静结合”方法论。 |
| `success_criteria` | drafting 读取 `第N卷/第N章.md` 时，可以清楚知道这一章在故事世界里何时发生、事件按什么顺序推进、读者允许知道什么、角色知道或误判什么、正文不能提前说明什么、章末造成什么状态变化、该推进什么、留下什么、避开什么，并知道本章支流任务是当章汇聚、延后转挂，还是继续保留开放。 |

## Required Headings

1. `章标题：`
2. `本章故事概要：`
3. `本章时间推进：`
4. `本章冲突：`
5. `本章爽点设计：`
6. `本章悬念开关：`
7. `本章节奏曲线：`
8. `本章登场人物：`
9. `本章主要场景：`
10. `本章关键道具：`
11. `本章任务线`
12. `章末达成：`
13. `本章线索：`
14. `本章伏笔`
15. `规避：`

## Hard Rules

1. `本章时间推进` 必须写明 `chapter_start_state / visible_time_span / event_order / parallel_hidden_events / chapter_end_state / handoff_to_next_chapter`。
2. `本章时间推进` 必须继承卷级 `本卷时间线`，不得静默改变本章在卷级 `chapter_chronology` 中的位置。
3. `本章冲突` 必须说明本章表层冲突、深层冲突与本章冲突状态变化。
4. `本章爽点设计` 必须写明 `reader_desire / promise_source / genre_payoff_profile / character_anchor / payoff_mode / payoff_variation_axis / build_up / delivery_action / satisfaction_delta / exaggeration_logic / cost_or_aftershock / aftertaste_hook`，并能回指本章冲突、卷级 promise、类型画像、读者期待和角色个性；若 `payoff_mode` 包含高超对决，还必须写明 `duel_variation_axis`。
5. `本章悬念开关` 必须写明 `上承卷级悬念 / 本章读者可知 / 本章角色可知 / 本章悬念线程动作 / 本章需要隐藏的 / 本章误导/疑阵 / 本章揭秘的 / 本章只埋不揭的 / 章末悬念压力 / 本章悬念负载 / 正文禁止上帝视角说明`。
6. `本章悬念线程动作` 必须写清每条命中悬念线程的 `suspense_id / priority / status_before / next_action / status_after / dependency / reader_state_delta / pov_state_delta`。
7. `本章悬念负载` 必须说明本章重点操作的主/次/局部悬念数量；若超过一主二局部，必须说明负载理由和读者微兑现。
8. `本章悬念开关` 必须约束 `本章线索 / 本章伏笔 / 本章节奏曲线 / 建议写法`，不得让 drafting 直接写出被隐藏的真相。
9. `本章节奏曲线` 必须写明 `selected_pack / selected_mode / mode_selection_reason / payoff_type / rhythm_intensity / previous_next_contrast / 七步职责映射 / 规划义务 / 义务段位 / 建议写法`，并附 Mermaid 图。
10. `payoff_type` 与 `micro_payoff` 必须消费 `本章爽点设计`，不得另起一套读者满足判断。
11. `本章任务线` 必须至少写清 `上承卷级任务 / 主线 / 支线 / 支流角色 / 汇聚动作 / 未汇聚任务去向`。
12. `本章线索` 负责当前章可见信息推进，并必须服从 `本章读者可知 / 本章揭秘的`。
13. `本章伏笔` 必须拆成 `铺设 / 兑现`，允许某一项为空，但段落必须存在；只埋不揭的信息必须在 `本章悬念开关` 中有对应约束。
14. `规划义务` 中必须显式锁定 `entry_promise / conflict_axis / micro_payoff / exit_hook`。
15. `义务段位` 只写必须兑现的结构义务，不得把建议写法偷渡成硬法律。
16. `建议写法` 只提供推荐编排，不得直接写正文句段。
17. 章级文件只能写规划，不得直接写对白、叙述段落或正文桥段。
18. 任何章级局部修订都必须以上游卷级文档为直接上下文、部级文档为总上下文；缺任何一层都不得落盘。

## Mermaid Requirement

章级 Mermaid 图至少要显出起势、转折、升级、高潮与尾钩。默认骨架为：

```mermaid
flowchart TD
    A["入场"] --> B["推动"]
    B --> C["转折"]
    C --> D["发展"]
    D --> E["升级"]
    E --> F["高潮"]
    F --> G["尾钩"]
```

## Planning-Only Boundary

章级允许写结构义务、场面功能、人物任务、信息推进和建议写法；不允许写可直接进入正文的对白、叙述段、段落桥接或文面句子。

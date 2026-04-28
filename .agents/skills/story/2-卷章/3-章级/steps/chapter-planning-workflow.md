# Chapter Planning Workflow

本文件承载章级 planning 的思维与执行一体化节点。节点必须同时表达判断、动作、证据、路由和 gate。

## Topology

章级采用 hybrid topology：前段强制串行回读，中段可在人物/场景/道具/任务线与信息层之间交叉校正，末段统一汇流到 review gate。

```mermaid
flowchart TD
    A["N1 上游回读"] --> B["N2 章脊锁定"]
    B --> C["N3 冲突画像"]
    C --> D["N4 爽点设计"]
    D --> E["N5 节奏 handoff"]
    E --> F{"资源与信息分支"}
    F --> G["N6 人物/场景/道具/任务线"]
    F --> H["N7 线索/伏笔"]
    G --> I["N8 章末达成与规避"]
    H --> I
    I --> J["Review Gate"]
    J --> K{"pass?"}
    K -->|"Yes"| L["落盘或返回 patch"]
    K -->|"No"| M["返回失败 owner"]
    M --> B
```

## Thinking-Action Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-UPSTREAM-REREAD` | 锁定本章上游职责 | 项目根、卷号、章号、`整体规划.md`、目标卷 `卷规划.md` | 完整回读上游，确认本章所属卷职责、任务从属和章划分位置 | `upstream_profile` | `N2-CHAPTER-SPINE` | 上游文档存在且目标章位置可确认 |
| `N2-CHAPTER-SPINE` | 锁章标题与故事概要 | `upstream_profile`、旧章规划或用户局部要求 | 生成或修订章标题、起点、推进、转向、章末状态 | `chapter_spine` | `N3-CHAPTER-CONFLICT` | 概要可支撑 drafting 起盘但未写正文 |
| `N3-CHAPTER-CONFLICT` | 锁本章冲突 | `chapter_spine`、卷级冲突和任务线 | 提炼表层冲突、深层冲突与冲突状态变化 | `conflict_profile` | `N4-CHAPTER-PAYOFF` | 冲突状态有变化，不只是静态描述 |
| `N4-CHAPTER-PAYOFF` | 设计章级爽点 | `chapter_spine`、`conflict_profile`、卷级 promise、`genre_payoff_profile`、任务欠账、角色/关系/信息欠账、近邻章爽点、角色最小投影或 `card_path` | 锁 `reader_desire / promise_source / genre_payoff_profile / character_anchor / payoff_mode / payoff_variation_axis / build_up / delivery_action / satisfaction_delta / exaggeration_logic / cost_or_aftershock / aftertaste_hook`；若是高超对决，额外锁 `duel_variation_axis`；并按类型画像及动能式、势能式或浪能式裁定主爽点形态 | `payoff_profile` | `N5-CHAPTER-RHYTHM` | 爽点能回指类型画像、读者期待、上游 promise 和角色个性；与近邻高潮点有差异轴；有可验证兑现动作，有状态差与余味牵引；夸张但合情理，未写成正文 |
| `N5-CHAPTER-RHYTHM` | 绘制章级节奏 handoff | `chapter_spine`、`conflict_profile`、`payoff_profile`、shared rhythm contract | 锁 `selected_pack / selected_mode / mode_selection_reason / payoff_type / rhythm_intensity / previous_next_contrast / 七步职责映射 / 规划义务 / 义务段位 / 建议写法` 并附 Mermaid 图 | `rhythm_handoff` | `N6-CHAPTER-ELEMENTS` 与 `N7-INFO-LAYER` | handoff slots 齐全，mode 选择有证据，payoff 与爽点设计一致，强度可复核，前后章波形有承接，建议写法未变正文 |
| `N6-CHAPTER-ELEMENTS` | 收束人物、场景、道具与任务线 | `rhythm_handoff`、`payoff_profile`、Cards 真源、卷级任务线 | 输出本章登场人物、主要场景、关键道具、主支线任务、支流角色、汇聚动作和未汇聚去向 | `chapter_resources` | `N8-CHAPTER-CLOSE` | 任务可上溯卷级，支流不悬空 |
| `N7-INFO-LAYER` | 分离线索与伏笔 | `chapter_spine`、`rhythm_handoff`、`payoff_profile`、上游信息承诺 | 写本章可见信息推进、伏笔铺设、伏笔兑现判断 | `info_layer` | `N8-CHAPTER-CLOSE` | 线索与伏笔不混写，铺设/兑现槽位存在 |
| `N8-CHAPTER-CLOSE` | 锁章末达成与规避 | 所有节点产物 | 汇总章末达成、禁飞区，按模板落盘或输出 patch | `chapter_plan` | `review/chapter-planning-review.md` | 必填标题齐全，无正文越界 |

## Branch And Merge Rules

- `N1 -> N2 -> N3 -> N4 -> N5` 是固定串行主干，不得并行绕过。
- `N6` 与 `N7` 可以交叉校正，但必须在 `N8` 汇流。
- 任一节点发现上游职责冲突时，回到 `N1` 重新核对，不在章级静默改写卷级。
- 任一节点输出正文句段时，回到该节点重写为 planning 语言。

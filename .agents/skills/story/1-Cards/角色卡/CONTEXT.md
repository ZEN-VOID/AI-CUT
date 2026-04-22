# CONTEXT.md

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 角色很多但撞位 | role bucket | 先修 `narrative_function`，再补设定 | 角色职责先于人设浓度 | 主角色能说明自己推进哪类戏 |
| 成长时间线变成事件流水账 | timeline contract | 改写为成长阶段与认知转折 | 固定 `experience_timeline + timeline_anchor` 双锚点 | 时间线能回答“角色因此变成什么” |
| 主角成长只有一句“变强了”，没有技能/心路/情感三轴 | growth system contract | 拆成 `growth_contract.axes.*` 与 `current_state.growth_state.*` 双层 | 主角卡默认强制启用三轴成长系统；长期 ceiling 放 core，当前态放 current_state | 角色卡能同时回答“长期要成为什么”和“现在走到哪了” |
| loopback 写回后只看到 history，当前成长态没更新 | growth actualization split | 同步回写 `current_state.growth_state`、`experience_timeline.axis_stage_map` 与 `history[].growth_delta` | 把成长 actualization 固定成三写位，而不是只 append prose 历史 | query 能直接回答主角现在三轴走到哪 |
| 专属物接口空心 | downstream interface | 回补 `exclusive_item_hooks` | 角色卡先留接口，物品卡再做适配 | 专属物能一眼看出角色归属 |
| 角色卡只剩索引没有全剧集角色真源 | source contract | 回到 `one-character-one-json`，逐角色落正式卡 | 禁止把多角色合并到单一大 JSON | `1-Cards/2-角色卡/**/角色名.json` 能逐个被引用 |
| 角色桶和角色属性标识不一致 | cast marker mapping | 以 bucket 回写 `cast_markers` 并校验唯一主标识 | 角色桶与属性标识共治，不允许一个角色同时多主标 | `group` 与 `cast_markers.primary_alignment` 一致 |
| 只有关系边 JSON 没有正式图谱输出 | graph projection | 生成 `角色关系图谱.md` 并补文字摘要 | 关系图谱固定成为角色索引的 side output | Markdown 同时包含文字说明和 Mermaid |
| 规划阶段把角色卡整份复制进 planning 文档或兼容 `story_map` | cross-stage bridge | 只输出最小角色/关系投影，完整人物事实留在角色卡侧 | 用 `story/_shared/character-planning-bridge.md` 固定“projection only”规则 | planning 文档与兼容 `story_map` 都只保留 refs 与最小 planning hooks |
| 增量修复把角色卡缩成单集临时视角 | full-series scope | 回补 `card_scope=full-series` 与全书角色覆盖 | 角色卡允许增量刷新，但不允许缩窄业务作用域 | 单卡 `card_scope.scope_type` 恒为 `full-series` |
| 人物有设定感但弧光发虚 | shaping bridge | 回到 `Desire / Flaw / Wound / Need / Change` 五维重写结构字段 | 先补 `wound + need + change_payoff`，再写 prose | 主角卡能回答“他为什么会这样，最后变成什么” |
| 反派只有坏没有成立逻辑 | antagonist mirror | 回补 `mirror_axis` 与 `self_justification` | 反派至少成立镜像关系或自我正义其一 | 反派卡不再只剩“阻碍主角” |
| 女主或配角可替换性太高 | role setpiece | 回补 `highlight_moment` 或 `memory_point` | 重要角色必须有高光或记忆点结构槽 | 读卡时能一眼记住她/他凭什么存在 |

## Repair Playbook

1. 先判分桶，再判关系，再判成长，再判专属物接口。
2. 若无法一句话说明“为什么是角色问题”，先退回父技能。
3. 先修结构，再补风格表达。
4. 遇到角色太多时，先锁全剧集 roster，再做局部角色润色。
5. 图谱问题优先修 `relationship_edges` 和 bucket，再修 Markdown 投影层。
6. 人物扁平时，优先检查 `wound / need / mirror_axis / highlight_moment / memory_point` 是否缺位，而不是先堆外貌描写。
7. 主角成长发虚时，先问这次变化属于 `技能 / 心路 / 情感` 哪一轴，再决定是补长期合同还是补当前 validated 状态。

## Reusable Heuristics

- 角色卡最值钱的是职责、关系和成长，不是设定名词数量。
- `exclusive_item_hooks` 越早稳定，物品卡越不容易模板化。
- `cast_markers` 不是展示性标签，而是角色卡、索引分桶和关系图谱节点标注的共享真源。
- `角色关系图谱.md` 适合做关系投影，不适合承载角色新增事实；新事实仍应先回写单角色 JSON。
- 跨到 `2-Planning` 时，最稳的做法是导出最小 projection，而不是把角色卡再复制成一份 planning 版角色卡。
- 增量模式下也要把角色卡当全剧集对象维护，不能把角色收缩成“本章出场名单”。
- 主角塑形最容易漏的是 `wound` 和 `need`；只写欲望与缺陷，角色通常仍会像设定板。
- 主角成长系统最容易失真的是把“剧情发生了什么”误写成“角色因此变成了什么”；前者进 history，后者才进 growth_state。
- 反派一旦没有 `mirror_axis`，就容易退化成纯功能阻碍物。
- 女主的“不是花瓶”最好写成 `highlight_moment`，配角的“不是工具人”最好写成 `memory_point` 或独立压力。

# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-编剧` 的经验层知识库，不是第二份主合同。
- 调用同目录 `SKILL.md` 时必须同时加载本文件。
- 本文件只沉淀可复用判断经验、失败模式和修复打法；不改写 `SKILL.md` 的输入、输出、gate 或模块授权。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
last_checked_at: 2026-06-04
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 剧本像小说复述 | 小说转译层 | 回 `N3`，把陈述拆成画面、动作、对白、独白、声音或道具证据 | `narration_to_voice_adaptation_map` 必须留证 | 删除旁白后观众仍能理解关键行动 |
| 节奏只有“快、爽、燃” | 节奏承托层 | 回 `N4`，为每个节奏机制补 source anchor 和承托字段 | 节奏机制必须绑定题材/叙事画像 | 任一节奏点都能在正文找到字段 |
| 高潮变成新增剧情结果 | 保真与高潮层 | 回 `N5`，只强化上游已有高点的声画和行动落点 | `climax_treatment_map` 区分 source fact 与 treatment | 高潮删去强化后，上游结果仍不变 |
| 尾钩只是抽象悬念 | 集末落点层 | 回 `N5`，改成最后可见/可听/可感受的小落点 | 尾钩必须记录 hook_type 和下一集未闭合问题 | 观众能说出“最后看到/听到/感到什么” |
| 声画同步写成分离清单或旧式锚点标题 | 字段投影层 | 回 `N6`，删除 `【声画同步锚点】`，把声音字段就近配对为 `对白画面/独白画面/内心独白画面/旁白画面/音效画面` | `audio_visual_pairing_map` 是正文内嵌证据，不只在报告里 | 正文中每条声音出现时，下一条或相邻字段有对应画面承托 |
| 同一画面被相邻字段重复表述 | 字段连续性层 | 回 `N6`，把同一时刻/同一主体/同一动作链的画面字段合并，或写明主体、空间、时间、信息变化的分界条件 | 正式写回必须留 `same_frame_continuity_map` | 下游按字段分组时不会把同一可见承托拍成两个画面 |
| 误把 imported director 规则当导演稿 | 模块边界层 | 回 `Imported Reference Adaptation Contract`，只保留承托，不写导演/表演/镜头 | `GATE-SCR-14` 阻断下游越权 | 正文无机位、景别、运镜、prompt |
| 报告只写“已参考”但无执行证据 | 报告证据层 | 回 `N8`，补 `Execution Decision Trace`、`Reference Execution Matrix`、`Rule Evidence Map`、`N/A Justification`、`Repair Log` | `GATE-SCR-16` 把缺失证据列为阻断项 | 每份触发 reference 都有 applied_to/evidence_in_output 或 n/a_reason |

## Repair Playbook

1. 先锁 source、集号、输出路径和改写授权。
2. 检查 `reference_load_manifest` 是否包含用户指定 8 个 copied references 和新增节奏合同。
3. 检查题材画像是否能解释节奏，不解释就回 `N2`。
4. 检查场景标题是否包含天气后缀；未知天气用 `天气待定` 并报告 followup。
5. 对新增对白/独白逐条查 source anchor、voice owner、知识依据和语音预算。
6. 对每个节奏机制查承托字段；无承托就删机制或补正文落点。
7. 检查相邻画面字段是否其实是同一拍摄单位：同一主体、同一停顿、同一手部动作、同一道具状态、同一声源反应要合并；只有主体/空间/时间/信息/节奏功能变化时才保留连续字段。
8. 高潮只强化已有事件的声画/情绪/行动，不改结果。
9. 尾钩必须落在最后可感对象上，不接受“悬念拉满”类总结。
10. 报告服务修复和下游交接，必须能回指正文位置。
11. 报告不得写自由散文式“思考过程”；必须写可审计的 `Execution Decision Trace` 和 `Reference Execution Matrix`。

## Reusable Heuristics

- 好的短剧节奏不是更短，而是更少无功能信息、更早暴露压力、更晚完全解释答案。
- 小说里的“他终于明白了”通常不能直接进剧本；要转成角色看见证据、听见声音、说出一句话或改变动作。
- 字段越多不等于画面越清楚；如果两个字段描述同一可见事实，下游更可能误拆拍摄单位，应优先合并成一个信息密度更高的画面字段。
- 爽点不是角色赢了，而是压迫关系被观众看见地反转。
- 迷你彩蛋尾钩适合过渡集；大反转尾钩适合冲突集。不要在每集硬造大反转。
- AIGC 视频下游最怕漂移：人物、地点、声音、物件和状态要在剧本字段里提前交代清楚。
- 防偷懒的关键不是要求“全量套规则”，而是要求全量审计、选择性触发和 N/A 必证；报告里没有证据的位置，通常就是下次返工入口。

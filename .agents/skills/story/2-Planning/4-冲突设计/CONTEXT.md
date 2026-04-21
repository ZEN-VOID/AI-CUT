# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-冲突设计` 子技能包的局部经验层，只服务 `2-Planning` Step 4。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 冲突只剩情绪词，没有归属关系 | child contract | 回到 owner / pressure source | 在子技能中固定 owner gate | board 能说明谁压迫谁 |
| 强冲突过早耗尽，没有梯度 | escalation contract | 回修 escalation ladder | 在输出中保留 release window 与阶段压力 | 后续任务系统仍有驱动力 |
| 冲突没有挂回 chapter board | patch writeback | 补 `board.conflicts` refs | 固化本 child 的 board conflict ownership | 下游不再失去章节冲突入口 |
| 冲突 thread 直接复制人物/关系正文 | cross-stage bridge | 把冲突说明压回 `character_refs / relationship_edge_refs` | 共享桥固定冲突 child 只写引用，不写第二份关系卡 | `conflict_threads` 保持对抗结构，不膨胀成设定文档 |

## Repair Playbook

1. 先看 story spine 是否稳定。
2. 再锁 owner 与 pressure source。
3. 再写升级链与解决窗口。
4. 收尾把冲突 refs 挂回 board。

## Reusable Heuristics

- 冲突 child 的价值不在“写多少打架”，而在“让对抗归属与梯度可追踪”。
- 如果 board 上看不到 conflict refs，后续任务链通常会漂成被动应对。
- 强冲突过早耗尽，往往不是内容太弱，而是 Step 4 提前把梯度用光了。
- 冲突最好绑在“哪对角色关系正在被扭曲”上，而不是额外再造一份人物背景说明。
- 进入卷分片模式后，冲突 master 仍留 global，章节冲突挂载与窗口细节必须落 slice；不要两边各保一份完整 conflict payload。

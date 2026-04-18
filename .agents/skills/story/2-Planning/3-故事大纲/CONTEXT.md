# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `3-故事大纲` 子技能包的局部经验层，只服务 `2-Planning` Step 3。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨 child 的脊柱/长线连续性经验仍回写到 `2-Planning/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 只有卷摘要，没有整书脊柱 | child contract | 回到主问题与 outline spine | 在子技能中先锁主问题再写卷推进 | 4-7 能共享同一主干 |
| 转折像事件堆叠，不改结构方向 | turning-point gate | 重写 `major_turns` 的改向逻辑 | 固化“转折必须改变人物/局势/预期” | board 事件不再平铺 |
| chapter board 只有容器，没有主干事件 | patch writeback | 把主干事件 refs 挂回 `bundled_elements.events` | 固化本 child 对 board events 的 ownership | 后续 child 能在同一 board 继续叠加 |

## Repair Playbook

1. 先看 Step 1-2 是否真的站稳。
2. 再锁主问题与 outline spine。
3. 再把卷推进和关键转折压到 chapter board。
4. 收尾检查后续长线是否有明确挂点。

## Reusable Heuristics

- Step 3 的高杠杆不在“写更多剧情”，而在“让所有后续长线挂在同一条主干上”。
- 如果转折不能改向，后续冲突/任务/线索都会变成外挂层。
- 章节容器稳了但 board 没事件，说明 Step 3 还没有真正完成 progressive commit。

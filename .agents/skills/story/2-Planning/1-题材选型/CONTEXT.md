# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `1-题材选型` 子技能包的局部经验层，只服务 `2-Planning` Step 1。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨 child 的连续性经验仍优先回写到 `2-Planning/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 题材选型只剩标签堆叠 | child contract | 回到题材承诺句与主副题材配比裁决 | 在子技能合同固化四层承诺与禁飞区 | `Planning/全息地图.json` 能解释后续结构为什么成立 |
| 副题材越权改写主题材方向盘 | boundary control | 降回 `主驱动 + 辅增压` 结构 | 在输出中显式区分主副题材职责 | 后续 child 不再出现双主题材互抢 |
| 题材知识被复制进本 child | asset layering | 改回读取共享 `templates/genres/` | 把共享资产边界写成子技能硬合同 | 本 child 不维护私有 trope 库 |

## Repair Playbook

1. 先抽取读者承诺、平台语义与禁飞区三类硬信号。
2. 再判定主题材负责什么，副题材具体增压什么。
3. 若题材知识不足，按需读取共享 `templates/genres/`，不在本地复制。
4. 收尾确认 Step 2-8 能从本 child 读取到明确 hooks。

## Reusable Heuristics

- 题材 child 最常见的失败不是“想得太少”，而是“什么都想要”，最后没有方向盘。
- 真正有效的副题材必须能改变章节、冲突、任务或线索中的至少一层。
- 平台热词可以帮助包装，但不能反客为主改写核心题材承诺。

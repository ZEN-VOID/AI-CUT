# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `类型卡` 子技能包的局部经验层，只服务 `1-Cards/类型卡`。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨 cards 的连续性经验优先回写到 `1-Cards/CONTEXT.md`；跨阶段导入经验再回写到 `2-Planning/CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 类型卡只剩标签堆叠 | child contract | 回到题材承诺句与主副题材配比裁决 | 在子技能合同固化四层承诺与禁飞区 | `1-Cards/5-类型卡/总题材/类型总卡.json` 能解释后续规划为什么成立 |
| 副题材越权改写主题材方向盘 | boundary control | 降回 `主驱动 + 辅增压` 结构 | 在输出中显式区分主副题材职责 | 后续 child 不再出现双主题材互抢 |
| 题材判断被外部题材包、目录知识或旧模板树绑架 | asset layering | 改回只读取当前项目设定与人工要求 | 把“类型卡只接受手动题材判断”写成硬合同 | 本 child 不依赖任何题材包目录或自动映射 |

## Repair Playbook

1. 先抽取读者承诺、平台语义与禁飞区三类硬信号。
2. 再判定主题材负责什么，副题材具体增压什么。
3. 若题材信息不足，只回到项目当前设定与用户要求补充，不借外部题材包补脑。
4. 收尾确认 `2-Planning` 父层能从本卡稳定导入 `story_promise / genre_corridor / navigation_rules`。

## Reusable Heuristics

- 类型卡最常见的失败不是“想得太少”，而是“什么都想要”，最后没有方向盘。
- 真正有效的副题材必须能改变章节、冲突、任务或线索中的至少一层。
- 平台热词可以帮助包装，但不能反客为主改写核心题材承诺。
- 进入卷分片模式后，题材方向盘应先稳定在 `1-Cards/5-类型卡`，不要为了“planning root 更完整”去绕过 cards 真源。
- 当前 `类型卡` 是手动题材真源，不再读取旧题材包目录或旧 `templates/genres/`。

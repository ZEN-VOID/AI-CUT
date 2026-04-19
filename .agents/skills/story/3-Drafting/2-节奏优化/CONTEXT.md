# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `2-节奏优化` 的局部经验层，只服务 `3-Drafting` Step 2。
- 先读 `SKILL.md`，再读本文件。
- 跨题材节奏策略优先沉到根级 `3-Drafting/CONTEXT.md` 或共享 reference。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 正文事件齐全，但像流水账 | pulse design | 建立 pulse map 后重排段落 | 在子技能固定“先画脉冲，再改节奏” | 章内能识别多个推进脉冲 |
| 为了加快节奏把必要信息删空了 | pacing over-cut | 恢复必要因果，再压缩无效重复 | 把“保逻辑再调节奏”写成硬规则 | 读者仍能答出因果链 |
| 章末没有牵引力 | hook density | 回到章末一段补未闭合期待或局面变化 | 在 pulse map 中强制标章末 hook 区 | 章末存在继续阅读驱动力 |
| 为了追求更有劲的节奏硬塞新招式/新道具/新规则 | core-constraints projection | 撤销新增设定，回到既有规划与设定物理内做重排 | 在 step 内新增“法律/物理审计”节点 | 节奏提升不依赖新设定 |
| 节奏变快了，但本章不再回应上章承诺 | chapter promise loss | 恢复承接段或把回应前移，不得把承诺剪没 | 在约束投影阶段显式锁“上章承诺回应位” | 本章仍能回答承接了什么 |
| 开头裁字后仍然迟迟不进冲突/风险 | weak opening pulse | 前移有效脉冲，削弱长解释段 | 把“开头尽早进入风险/强情绪”纳入 soft projection | 前段已有清晰冲突、风险或强情绪 |
| 章末只剩平收，没有未闭合期待 | flat ending after pacing | 追加代价余波、未闭合问题或下一步压力 | 章末 hook 区设为 pulse map 必填位 | 章末留有继续阅读驱动力 |
| 项目已启用 type-pack，但 Step 2 仍只按通用节奏规则做重排 | step-specific pack drop | 在本 step 显式读取 drafting pack projection，把 `required_hooks / hard_fail_signals` 写入 process log | 固定“Step 2 既守通用节奏，也守 pack 节奏钩子”的双层合同 | 快节奏/规则类 pack 在 Step 2 会表现出不同的节奏 gate |

## Repair Playbook

1. 先锁 `2-Planning/全息地图.json` 本章义务、上章承诺回应位和 `core-constraints` 的三大定律，再进入节奏判断。
2. 先标所有推进点，再看哪些段在重复同一种功能。
3. 若整章都很平，优先补“局面变化”而不是补更多说明。
4. 若前段过满后段发空，优先重新分配脉冲，而不是简单裁字。
5. 每次 rewrite 后都回查：是否还可读、是否仍有推进、是否还回应了承诺、是否靠新增设定作弊。

## Reusable Heuristics

- 节奏优化不是单纯加速，而是让读者感到“这一章一直在变”。
- 网文章节最常见的拖沓，不是字多，而是连续几个段落承担同一种叙事功能。
- 真正的节奏优化先守住“规划真源即法律”，再动段落收放；先破法律再谈速度，基本都会把章改空。
- 若一个“更快”的版本需要引入新设定才成立，那不是节奏优化，而是越权改戏。
- pack 对 Step 2 的介入点不该是“再加一套题材说明”，而是把哪些段必须删、哪些牵引必须保、哪些 fail signal 不能碰说清楚。
